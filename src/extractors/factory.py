"""Factory que seleciona o extrator correto baseado na entrada."""
from .base import ExtratorBase
from .pdf_extractor import PDFExtractor
from .text_extractor import TextExtractor
from .url_extractor import URLExtractor


class ExtratorFactory:
    """Decide qual extrator usar baseado no formato da entrada."""

    @staticmethod
    def criar(fonte: str) -> ExtratorBase:
        """Retorna o extrator apropriado para a fonte.

        Args:
            fonte: Caminho de arquivo (.pdf, .txt) ou URL (http/https).

        Returns:
            Instância de ExtratorBase.

        Raises:
            ValueError: Se o tipo de fonte não for suportado.
        """
        if fonte.startswith(("http://", "https://")):
            return URLExtractor()
        if fonte.lower().endswith(".pdf"):
            return PDFExtractor()
        if fonte.lower().endswith(".txt"):
            return TextExtractor()
        raise ValueError(f"Tipo de fonte não suportado: {fonte}")