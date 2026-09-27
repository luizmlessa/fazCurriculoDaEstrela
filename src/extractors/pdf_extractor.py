"""Extrator de texto para arquivos PDF."""
import logging

from pypdf import PdfReader

from .base import ExtratorBase

logger = logging.getLogger(__name__)


class PDFExtractor(ExtratorBase):
    """Extrai texto de arquivos PDF usando a biblioteca pypdf."""

    def extrair(self, caminho: str) -> str:
        """Lê um PDF e retorna todo o texto contido nele.

        Args:
            caminho: Caminho do arquivo PDF.

        Returns:
            Texto completo extraído do PDF.

        Raises:
            Exception: Se houver falha na leitura do arquivo.
        """
        try:
            reader = PdfReader(caminho)
            texto = "".join(p.extract_text() or "" for p in reader.pages)
            logger.info(f"{len(texto)} caracteres extraídos de {caminho}")
            return texto
        except Exception as e:
            logger.error(f"Erro ao ler PDF {caminho}: {e}")
            raise