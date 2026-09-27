"""Orquestrador do pipeline de adaptação de currículos."""
import logging

from extractors.base import ExtratorBase
from llm.base import LLMProviderBase
from prompts.resume_prompt import ResumePromptBuilder
from writers.base import WriterBase

logger = logging.getLogger(__name__)


class ResumePipeline:
    """Orquestra as etapas: extração, prompt, LLM e escrita.

    Todas as dependências são injetadas via construtor, permitindo
    trocar implementações sem alterar o orquestrador.
    """

    def __init__(
        self,
        extrator_curriculo: ExtratorBase,
        extrator_vaga: ExtratorBase,
        llm: LLMProviderBase,
        writer: WriterBase,
    ):
        """Recebe todas as dependências por injeção.

        Args:
            extrator_curriculo: Extrator do arquivo de currículo.
            extrator_vaga: Extrator do arquivo de vaga.
            llm: Provedor de IA.
            writer: Writer de output.
        """
        self.extrator_curriculo = extrator_curriculo
        self.extrator_vaga = extrator_vaga
        self.llm = llm
        self.writer = writer

    def executar(self, caminho_curriculo: str, caminho_vaga: str, caminho_saida: str) -> None:
        """Executa o pipeline completo.

        Args:
            caminho_curriculo: Caminho do PDF do currículo.
            caminho_vaga: Caminho do TXT da vaga.
            caminho_saida: Caminho onde o output será salvo.
        """
        logger.info("=== Iniciando Pipeline ===")

        logger.info("--- Lendo Currículo ---")
        curriculo = self.extrator_curriculo.extrair(caminho_curriculo)

        logger.info("--- Lendo Vaga ---")
        vaga = self.extrator_vaga.extrair(caminho_vaga)

        logger.info("--- Construindo Prompt ---")
        prompt = ResumePromptBuilder(curriculo, vaga).construir()

        logger.info("--- Chamando LLM ---")
        resultado = self.llm.gerar_resposta(prompt)

        logger.info("--- Salvando Resultado ---")
        self.writer.escrever(resultado, caminho_saida)

        logger.info("=== Pipeline concluído ===")