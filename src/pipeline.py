"""Orquestrador do pipeline de adaptação de currículos."""
import logging
import os

from src.exceptions import ExtractionError, ParserError, ResumeAIError, WriterError
from src.extractors.factory import ExtratorFactory
from src.finders.file_finder import FileFinder
from src.llm.base import LLMProviderBase
from src.parsers.output_parser import OutputParser
from src.prompts.resume_prompt import ResumePromptBuilder
from src.writers.base import WriterBase

logger = logging.getLogger(__name__)


class ResumePipeline:
    def __init__(self, llm: LLMProviderBase, writer: WriterBase, finder: FileFinder):
        self.llm = llm
        self.writer = writer
        self.finder = finder
        self.parser = OutputParser()

    def executar(self, fonte_vaga: str, pasta_saida: str = "data/output") -> None:
        os.makedirs(pasta_saida, exist_ok=True)

        logger.info("=== Iniciando Pipeline ===")

        # Etapa 1: currículo
        try:
            caminho_curriculo = self.finder.encontrar_curriculo()
            curriculo = ExtratorFactory.criar(caminho_curriculo).extrair(caminho_curriculo)
        except Exception as e:
            raise ExtractionError(f"Falha ao ler o currículo: {e}") from e

        # Etapa 2: vaga
        try:
            vaga = ExtratorFactory.criar(fonte_vaga).extrair(fonte_vaga)
        except Exception as e:
            raise ExtractionError(f"Falha ao ler a vaga: {e}") from e

        # Etapa 3: prompt + LLM
        prompt = ResumePromptBuilder(curriculo, vaga).construir()
        resposta = self.llm.gerar_resposta(prompt)  # LLMError já vem do provider

        # Etapa 4: parser
        try:
            secoes = self.parser.parsear(resposta)
        except Exception as e:
            raise ParserError(f"Falha ao interpretar resposta do LLM: {e}") from e

        # Etapa 5: escritas
        try:
            self.writer.escrever(secoes["analise"], f"{pasta_saida}/analise-ats.pdf")
            self.writer.escrever(secoes["curriculo"], f"{pasta_saida}/curriculo-adaptado.pdf")
            self.writer.escrever(secoes["carta"], f"{pasta_saida}/carta-apresentacao.pdf")
        except Exception as e:
            raise WriterError(f"Falha ao gerar PDFs: {e}") from e

        logger.info("=== Pipeline concluído ===")
        logger.info(f"Outputs em: {pasta_saida}/")