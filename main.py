"""Ponto de entrada do Faz Currículo da Estrela."""
import logging

from src.extractors.pdf_extractor import PDFExtractor
from src.extractors.text_extractor import TextExtractor
from src.llm.factory import LLMFactory
from src.pipeline import ResumePipeline
from src.writers.markdown_writer import MarkdownWriter

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    pipeline = ResumePipeline(
        extrator_curriculo=PDFExtractor(),
        extrator_vaga=TextExtractor(),
        llm=LLMFactory.criar("ollama"),
        writer=MarkdownWriter(),
    )

    pipeline.executar(
        caminho_curriculo="data/curriculo.pdf",
        caminho_vaga="data/vaga.txt",
        caminho_saida="data/output.md",
    )