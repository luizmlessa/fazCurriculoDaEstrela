"""Parser da resposta da carta."""
import logging
import re

logger = logging.getLogger(__name__)


class CartaParser:
    """Extrai o texto da carta da resposta do LLM."""

    def parsear(self, texto: str) -> str:
        padrao = re.search(
            r"##\s*Carta\s+de\s+Apresenta[çc][ãa]o\s*(.*?)$",
            texto,
            re.DOTALL | re.IGNORECASE,
        )
        if padrao:
            return padrao.group(1).strip()

        logger.warning("Marcador da carta não encontrado, usando resposta inteira.")
        return texto.strip()
