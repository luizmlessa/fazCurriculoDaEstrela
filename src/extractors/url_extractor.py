"""Extrator de texto a partir de URLs."""
import logging
import re

import requests
from bs4 import BeautifulSoup, Tag

from .base import ExtratorBase

logger = logging.getLogger(__name__)


class URLExtractor(ExtratorBase):
    """Extrai o texto útil de uma página web.

    Remove menus, rodapés, headers, cookies e outros ruídos comuns
    em páginas de vagas (especialmente LinkedIn).
    """

    PADROES_RUIDO = [
        r"cookie", r"banner", r"modal", r"popup", r"navbar",
        r"footer", r"header", r"sidebar", r"menu", r"sign-in", r"signin",
        r"login", r"toast", r"tooltip", r"nav-",
    ]

    LINHAS_RUIDO = {
        "apply", "sign in", "join now", "join to apply", "email or phone",
        "password", "show", "forgot password?", "new to linkedin?",
        "user agreement", "privacy policy", "cookie policy",
        "skip to main content", "join or sign in to find your next job",
        "save", "show more", "show less",
    }

    # Marcadores que indicam FIM do conteúdo útil (LinkedIn)
    MARCADORES_FIM = [
    "Similar jobs",
    "People also viewed",
    "Similar Searches",
    "Explore top content",
    "Set alert",
    "Referrals increase your chances",
    "Mid-Senior level",
    "Full-time",
]

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def extrair(self, url: str) -> str:
        try:
            logger.info(f"Baixando URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # 1. Remove tags estruturais
            for tag_name in ["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            # 2. Remove elementos com classes/ids de ruído
            elementos_ruido = []
            for elemento in soup.find_all(True):
                if not isinstance(elemento, Tag):
                    continue
                classes = " ".join(elemento.get("class") or []).lower()
                id_elem = (elemento.get("id") or "").lower()
                if any(re.search(p, classes) or re.search(p, id_elem) for p in self.PADROES_RUIDO):
                    elementos_ruido.append(elemento)

            for elemento in elementos_ruido:
                try:
                    elemento.decompose()
                except Exception:
                    pass

            # 3. Extrai texto
            texto = soup.get_text(separator="\n")
            linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]

            # 4. Filtra linhas ruído
            linhas = [l for l in linhas if l.lower() not in self.LINHAS_RUIDO]

            # 5. CORTA a partir de marcadores de fim (LinkedIn)
            for i, linha in enumerate(linhas):
                if linha in self.MARCADORES_FIM:
                    logger.info(f"Cortando a partir do marcador: {linha}")
                    linhas = linhas[:i]
                    break

            # 6. Remove duplicatas consecutivas
            resultado = []
            anterior = None
            for linha in linhas:
                if linha != anterior:
                    resultado.append(linha)
                anterior = linha

            texto_limpo = "\n".join(resultado)
            logger.info(f"{len(texto_limpo)} caracteres extraídos de {url}")
            return texto_limpo

        except Exception as e:
            logger.error(f"Erro ao extrair URL {url}: {e}")
            raise