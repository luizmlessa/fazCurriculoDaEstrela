"""Interface web do Faz Currículo da Estrela."""
import logging
import os

import streamlit as st

from src.exceptions import (
    ExtractionError,
    LLMConnectionError,
    LLMModelError,
    LLMTimeoutError,
    WriterError,
)
from src.extractors.factory import ExtratorFactory
from src.finders.file_finder import FileFinder
from src.llm.factory import LLMFactory
from src.pipeline import ResumePipeline
from src.writers.pdf_writer import PDFWriter

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Faz Currículo da Estrela",
    page_icon="⭐",
    layout="centered",
)

st.title("⭐ Faz Currículo da Estrela")
st.caption("Adapta seu currículo para uma vaga específica usando IA local (Ollama).")

# Session state
if "url_validada" not in st.session_state:
    st.session_state.url_validada = None
if "texto_vaga_preview" not in st.session_state:
    st.session_state.texto_vaga_preview = None

# Sidebar
with st.sidebar:
    st.header("Configurações")
    modelo = st.selectbox(
        "Modelo Ollama",
        options=["qwen2.5-coder:7b", "qwen2.5:14b"],
        index=0,
    )
    temperatura = st.slider(
        "Temperatura",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05,
        help="Baixo = fiel ao currículo. Alto = criativo.",
    )

    st.divider()
    st.subheader("Currículo atual")
    pasta_data = "data"
    arquivos_cv = [
        f for f in os.listdir(pasta_data)
        if f.lower().endswith((".pdf", ".txt"))
        and f.lower().startswith(("curriculo", "cv", "resume"))
    ]
    if arquivos_cv:
        st.success(f"✅ {arquivos_cv[0]}")
    else:
        st.error("❌ Nenhum currículo em data/")

# Passo 1: URL
st.subheader("1. URL da vaga")
url_vaga = st.text_input(
    "Cole a URL",
    placeholder="https://www.linkedin.com/jobs/view/...",
    label_visibility="collapsed",
)

col_testar, col_limpar = st.columns([1, 4])
with col_testar:
    testar = st.button("🔍 Testar URL", use_container_width=True)
with col_limpar:
    if st.session_state.url_validada and st.session_state.url_validada != url_vaga:
        st.caption("⚠️ URL mudou desde o último teste. Teste de novo.")

if testar:
    if not url_vaga:
        st.error("Cole uma URL antes.")
    else:
        with st.spinner("Baixando e analisando a vaga..."):
            try:
                texto = ExtratorFactory.criar(url_vaga).extrair(url_vaga)
                st.session_state.url_validada = url_vaga
                st.session_state.texto_vaga_preview = texto
                st.success(f"✅ Vaga baixada com sucesso ({len(texto)} caracteres).")
            except Exception as e:
                st.session_state.url_validada = None
                st.session_state.texto_vaga_preview = None
                st.error(f"❌ Falha ao baixar a URL: {e}")

if st.session_state.texto_vaga_preview:
    with st.expander("👁️ Ver o que foi extraído da vaga", expanded=False):
        st.text_area(
            "Texto da vaga",
            st.session_state.texto_vaga_preview,
            height=400,
            label_visibility="collapsed",
        )

# Passo 2: Gerar
st.subheader("2. Gerar currículo")
url_pronta = st.session_state.url_validada == url_vaga and url_vaga

gerar = st.button(
    "⚡ Gerar",
    type="primary",
    disabled=not url_pronta,
    use_container_width=True,
)

if not url_pronta:
    st.caption("Teste a URL primeiro para liberar o botão de gerar.")

if gerar:
    pasta_saida = "data/output"
    os.makedirs(pasta_saida, exist_ok=True)

    with st.status("Processando...", expanded=True) as status:
        try:
            st.write("🧠 Chamando Ollama...")
            pipeline = ResumePipeline(
                llm=LLMFactory.criar("ollama", modelo=modelo, temperature=temperatura),
                writer=PDFWriter(),
                finder=FileFinder(pasta=pasta_data),
            )
            pipeline.executar(fonte_vaga=url_vaga, pasta_saida=pasta_saida)
            status.update(label="Concluído!", state="complete", expanded=False)
            st.success("✅ Currículo adaptado com sucesso!")

        except LLMConnectionError:
            status.update(label="Ollama desconectado", state="error", expanded=False)
            st.error("🔌 Não foi possível conectar ao Ollama.")
            st.info(
                "Abra um terminal e rode:\n\n"
                "```\nollama serve\n```\n\n"
                "Depois tente gerar novamente."
            )

        except LLMTimeoutError as e:
            status.update(label="Timeout", state="error", expanded=False)
            st.error("⏱️ O Ollama demorou demais para responder.")
            st.info(str(e))

        except LLMModelError as e:
            status.update(label="Modelo com problema", state="error", expanded=False)
            st.error(f"🧠 {e}")
            st.info(
                "**Dicas:**\n"
                "- Se for falta de VRAM, use um modelo menor: **qwen2.5-coder:7b**\n"
                "- Se for modelo não encontrado, rode: `ollama pull <modelo>`\n"
                "- Confira modelos disponíveis: `ollama list`"
            )

        except ExtractionError as e:
            status.update(label="Falha ao extrair dados", state="error", expanded=False)
            st.error(f"📄 {e}")
            st.info(
                "Verifique se:\n"
                "- A URL tá acessível e é uma vaga válida\n"
                "- Tem um arquivo de currículo em `data/`"
            )

        except WriterError as e:
            status.update(label="Falha ao gerar PDF", state="error", expanded=False)
            st.error(f"✍️ {e}")

        except Exception as e:
            status.update(label="Erro inesperado", state="error", expanded=True)
            st.error(f"❌ Erro inesperado: {e}")
            st.exception(e)

# Downloads
pasta_saida = "data/output"
arquivos_saida = {
    "Análise ATS": "analise-ats.pdf",
    "Currículo": "curriculo-adaptado.pdf",
    "Carta": "carta-apresentacao.pdf",
}

if all(os.path.exists(f"{pasta_saida}/{f}") for f in arquivos_saida.values()):
    st.divider()
    st.subheader("📥 Downloads")

    cols = st.columns(3)
    for col, (label, arquivo) in zip(cols, arquivos_saida.items()):
        with open(f"{pasta_saida}/{arquivo}", "rb") as f:
            col.download_button(
                label=f"Baixar {label}",
                data=f,
                file_name=arquivo,
                mime="application/pdf",
                use_container_width=True,
            )

    with st.expander("👁️ Ver análise ATS"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(f"{pasta_saida}/analise-ats.pdf")
            texto = "\n".join(p.extract_text() for p in reader.pages)
            st.text(texto)
        except Exception as e:
            st.warning(f"Não foi possível exibir a prévia: {e}")