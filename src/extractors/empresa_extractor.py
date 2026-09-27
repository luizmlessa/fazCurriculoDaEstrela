"""Extrai o nome da empresa a partir do texto da vaga."""
import logging
import re

logger = logging.getLogger(__name__)


class EmpresaExtractor:
    PADROES = [
        r"^(.+?)\s+hiring\s+",
        r"\s+at\s+(.+?)\s+[—\-|]",
        r"^Vaga\s+(?:na|em|para)\s+(.+?)[\n\.,]",
        r"Empresa:\s*(.+?)[\n\.,]",
        r"(?:Trabalhe\s+na|Junte-se\s+[àa])\s+(.+?)[\n\.,]",
    ]

    STOPWORDS = {"linkedin", "brasil", "brazil", "gupy", "vagas"}

    def extrair(self, texto_vaga: str) -> str:
        if not texto_vaga:
            return ""

        primeiras = "\n".join(texto_vaga.splitlines()[:10])

        for padrao in self.PADROES:
            match = re.search(padrao, primeiras, re.MULTILINE | re.IGNORECASE)
            if match:
                empresa = self._limpar(match.group(1))
                if empresa and empresa.lower() not in self.STOPWORDS:
                    logger.info(f"Empresa detectada: {empresa}")
                    return empresa

        logger.warning("Não foi possível detectar o nome da empresa.")
        return ""

    @staticmethod
    def _limpar(empresa: str) -> str:
        empresa = empresa.strip()
        empresa = re.sub(r"\s+", " ", empresa)
        empresa = empresa.strip(".,;:-—|")
        empresa = re.sub(r"\s+(Brasil|Brazil|São Paulo|Rio de Janeiro|SP|RJ)$", "", empresa, flags=re.IGNORECASE)
        return empresa.strip()
