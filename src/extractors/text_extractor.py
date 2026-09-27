"""Extrator de texto para arquivos .txt."""
import logging

from .base import ExtratorBase

logger = logging.getLogger(__name__)


class TextExtractor(ExtratorBase):
    """Extrai texto de arquivos plain text (UTF-8)."""

    def extrair(self, caminho: str) -> str:
        """Lê um arquivo .txt e retorna seu conteúdo.

        Args:
            caminho: Caminho do arquivo de texto.

        Returns:
            Conteúdo do arquivo como string.

        Raises:
            Exception: Se houver falha na leitura.
        """
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                texto = f.read()
            logger.info(f"{len(texto)} caracteres extraídos de {caminho}")
            return texto
        except Exception as e:
            logger.error(f"Erro ao ler TXT {caminho}: {e}")
            raise