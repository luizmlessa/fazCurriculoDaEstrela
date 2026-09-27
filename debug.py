import logging
from src.finders.file_finder import FileFinder
from src.llm.factory import LLMFactory
from src.extractors.factory import ExtratorFactory
from src.prompts.resume_prompt import ResumePromptBuilder

logging.basicConfig(level=logging.INFO)

finder = FileFinder(pasta="data")
caminho = finder.encontrar_curriculo()
curriculo = ExtratorFactory.criar(caminho).extrair(caminho)
vaga = ExtratorFactory.criar("https://www.linkedin.com/jobs/view/4463122444/").extrair("https://www.linkedin.com/jobs/view/4463122444/")

prompt = ResumePromptBuilder(curriculo, vaga).construir()

print("=" * 60)
print("CURRÍCULO EXTRAÍDO:")
print("=" * 60)
print(curriculo)

print("\n" + "=" * 60)
print("VAGA EXTRAÍDA (primeiros 500 chars):")
print("=" * 60)
print(vaga[:500])

resposta = LLMFactory.criar("ollama").gerar_resposta(prompt)

print("\n" + "=" * 60)
print("RESPOSTA BRUTA DO LLM:")
print("=" * 60)
print(resposta)

with open("data/debug-output.md", "w", encoding="utf-8") as f:
    f.write(resposta)