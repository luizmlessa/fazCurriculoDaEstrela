"""Implementação do provedor de LLM usando Ollama local."""
import logging

import requests

from src.config import Config

from .base import LLMProviderBase

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProviderBase):
    """Provedor que se comunica com o Ollama rodando localmente."""

    def __init__(
        self,
        url: str | None = None,
        modelo: str | None = None,
        temperature: float = 0.1,
    ):
        self.url = url or Config.OLLAMA_URL
        self.modelo = modelo or Config.OLLAMA_MODEL
        self.temperature = temperature

    def gerar_resposta(self, prompt: str) -> str:
        payload = {
            "model": self.modelo,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
            },
        }
        try:
            logger.info(f"Chamando Ollama ({self.modelo}, temp={self.temperature})...")
            response = requests.post(self.url, json=payload, timeout=600)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logger.error(f"Erro ao chamar Ollama: {e}")
            raise