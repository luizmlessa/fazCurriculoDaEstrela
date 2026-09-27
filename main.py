"""Ponto de entrada do Faz Currículo da Estrela."""
import logging

from src.finders.file_finder import FileFinder
from src.llm.factory import LLMFactory
from src.pipeline import ResumePipeline
from src.writers.pdf_writer import PDFWriter

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    pipeline = ResumePipeline(
        llm=LLMFactory.criar("ollama"),
        writer=PDFWriter(),
        finder=FileFinder(pasta="data"),
    )

    pipeline.executar(
        fonte_vaga="https://www.linkedin.com/jobs/view/4463122444/",
        pasta_saida="data/output",
    )