"""Orquestrador do pipeline de adaptação de currículos."""
import logging
import os

from src.exceptions import ExtractionError, ParserError, WriterError
from src.extractors.empresa_extractor import EmpresaExtractor
from src.extractors.factory import ExtratorFactory
from src.finders.file_finder import FileFinder
from src.llm.base import LLMProviderBase
from src.parsers.analise_parser import AnaliseParser
from src.parsers.carta_parser import CartaParser
from src.prompts.analise_prompt import AnalisePromptBuilder
from src.prompts.carta_prompt import CartaPromptBuilder
from src.writers.base import WriterBase

logger = logging.getLogger(__name__)


class ResumePipeline:
    """Orquestra: extração, 2 chamadas ao LLM, e geração de PDFs.

    Chamada 1: currículo + análise ATS
    Chamada 2: carta de apresentação (com nome da empresa extraído)
    """

    def __init__(self, llm: LLMProviderBase, writer: WriterBase, finder: FileFinder):
        self.llm = llm
        self.writer = writer
        self.finder = finder
        self.empresa_extractor = EmpresaExtractor()
        self.analise_parser = AnaliseParser()
        self.carta_parser = CartaParser()

    def executar(self, fonte_vaga: str, pasta_saida: str = "data/output") -> None:
        os.makedirs(pasta_saida, exist_ok=True)

        logger.info("=== Iniciando Pipeline ===")

        # Etapa 1: extração
        try:
            caminho_curriculo = self.finder.encontrar_curriculo()
            curriculo = ExtratorFactory.criar(caminho_curriculo).extrair(caminho_curriculo)
            vaga = ExtratorFactory.criar(fonte_vaga).extrair(fonte_vaga)
        except Exception as e:
            raise ExtractionError(f"Falha na extração: {e}") from e

        # Etapa 2: extrair empresa (determinístico, sem LLM)
        empresa = self.empresa_extractor.extrair(vaga)

        # Etapa 3: chamada 1 — análise + currículo
        logger.info("--- Chamada 1: Análise ATS + Currículo ---")
        prompt_analise = AnalisePromptBuilder(curriculo, vaga).construir()
        resposta_analise = self.llm.gerar_resposta(prompt_analise)

        try:
            secoes = self.analise_parser.parsear(resposta_analise)
        except Exception as e:
            raise ParserError(f"Falha ao parsear análise: {e}") from e

        # Etapa 4: chamada 2 — carta
        logger.info("--- Chamada 2: Carta de Apresentação ---")
        prompt_carta = CartaPromptBuilder(curriculo, vaga, empresa).construir()
        resposta_carta = self.llm.gerar_resposta(prompt_carta)

        try:
            carta = self.carta_parser.parsear(resposta_carta)
        except Exception as e:
            raise ParserError(f"Falha ao parsear carta: {e}") from e

        # Etapa 5: geração de PDFs
        logger.info("--- Gerando PDFs ---")
        try:
            self.writer.escrever(secoes["analise"], f"{pasta_saida}/analise-ats.pdf")
            self.writer.escrever(secoes["curriculo"], f"{pasta_saida}/curriculo-adaptado.pdf")
            self.writer.escrever(carta, f"{pasta_saida}/carta-apresentacao.pdf")
        except Exception as e:
            raise WriterError(f"Falha ao gerar PDFs: {e}") from e

        logger.info("=== Pipeline concluído ===")
        logger.info(f"Empresa detectada: {empresa or '(não identificada)'}")
        logger.info(f"Outputs em: {pasta_saida}/")