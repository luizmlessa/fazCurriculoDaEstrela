"""Parser da resposta de análise + currículo."""
import logging
import re

logger = logging.getLogger(__name__)


class AnaliseParser:
    """Extrai as seções 'analise' e 'curriculo' da resposta do LLM."""

    def parsear(self, texto: str) -> dict:
        resultado = {"analise": "", "curriculo": ""}

        padrao_analise = re.search(
            r"##\s*An[áa]lise\s*ATS\s*(.*?)(?=##\s*Curr|$)",
            texto,
            re.DOTALL | re.IGNORECASE,
        )
        padrao_curriculo = re.search(
            r"##\s*Curr[íi]culo\s*Adaptado\s*(.*?)$",
            texto,
            re.DOTALL | re.IGNORECASE,
        )

        if padrao_analise:
            resultado["analise"] = padrao_analise.group(1).strip()
        else:
            logger.warning("Seção Análise ATS não encontrada.")

        if padrao_curriculo:
            resultado["curriculo"] = padrao_curriculo.group(1).strip()
        else:
            logger.warning("Seção Currículo Adaptado não encontrada.")

        return resultado
