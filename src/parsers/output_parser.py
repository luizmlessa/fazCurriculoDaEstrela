"""Parser da resposta do LLM."""
import logging
import re

logger = logging.getLogger(__name__)


class OutputParser:
    """Extrai as seções estruturadas da resposta do LLM."""

    def parsear(self, texto: str) -> dict:
        """Retorna dict com 'analise', 'curriculo' e 'carta'."""
        resultado = {"analise": "", "curriculo": "", "carta": ""}

        padroes = {
            "analise": r"##\s*An[áa]lise ATS\s*(.*?)(?=##\s*Curr|$)",
            "curriculo": r"##\s*Curr[íi]culo Adaptado\s*(.*?)(?=##\s*Carta|$)",
            "carta": r"##\s*Carta de Apresenta[çc][ãa]o\s*(.*?)$",
        }

        for chave, padrao in padroes.items():
            match = re.search(padrao, texto, re.DOTALL | re.IGNORECASE)
            if match:
                resultado[chave] = match.group(1).strip()
            else:
                logger.warning(f"Seção '{chave}' não encontrada na resposta.")

        return resultado