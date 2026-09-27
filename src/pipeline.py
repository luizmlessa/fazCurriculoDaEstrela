"""Orquestrador do pipeline de adaptação de currículos."""
import logging
import os

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

        logger.info("--- Localizando Currículo ---")
        caminho_curriculo = self.finder.encontrar_curriculo()
        curriculo = ExtratorFactory.criar(caminho_curriculo).extrair(caminho_curriculo)

        logger.info("--- Lendo Vaga ---")
        vaga = ExtratorFactory.criar(fonte_vaga).extrair(fonte_vaga)

        logger.info("--- Construindo Prompt ---")
        prompt = ResumePromptBuilder(curriculo, vaga).construir()

        logger.info("--- Chamando LLM ---")
        resposta = self.llm.gerar_resposta(prompt)

        logger.info("--- Parseando Resposta ---")
        secoes = self.parser.parsear(resposta)

        logger.info("--- Gerando Análise ATS ---")
        self.writer.escrever(secoes["analise"], f"{pasta_saida}/analise-ats.pdf")

        logger.info("--- Gerando PDF do Currículo ---")
        self.writer.escrever(secoes["curriculo"], f"{pasta_saida}/curriculo-adaptado.pdf")

        logger.info("--- Gerando PDF da Carta ---")
        self.writer.escrever(secoes["carta"], f"{pasta_saida}/carta-apresentacao.pdf")

        logger.info("=== Pipeline concluído ===")
        logger.info(f"Outputs em: {pasta_saida}/")