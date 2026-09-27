"""Implementação do provedor de LLM usando Ollama local."""
import logging

import requests

from config import Config

from .base import LLMProviderBase

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProviderBase):
    """Provedor que se comunica com o Ollama rodando localmente."""

    def __init__(self, url: str | None = None, modelo: str | None = None):
        """Inicializa o provedor com URL e modelo configuráveis.

        Args:
            url: Endpoint da API do Ollama. Padrão: Config.OLLAMA_URL.
            modelo: Nome do modelo a ser utilizado. Padrão: Config.OLLAMA_MODEL.
        """
        self.url = url or Config.OLLAMA_URL
        self.modelo = modelo or Config.OLLAMA_MODEL

    def gerar_resposta(self, prompt: str) -> str:
        """Envia o prompt ao Ollama e retorna a resposta.

        Args:
            prompt: Texto do prompt.

        Returns:
            Resposta gerada pelo modelo.

        Raises:
            requests.RequestException: Em falhas de comunicação.
        """
        payload = {"model": self.modelo, "prompt": prompt, "stream": False}
        try:
            logger.info(f"Chamando Ollama ({self.modelo})...")
            response = requests.post(self.url, json=payload, timeout=300)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logger.error(f"Erro ao chamar Ollama: {e}")
            raise