"""Implementação do provedor de LLM usando Ollama local."""

import logging

import requests

from src.config import Config
from src.exceptions import (
    LLMConnectionError,
    LLMModelError,
    LLMTimeoutError,
)

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
                "num_ctx": 4096,
            },
        }

        logger.info(f"Chamando Ollama ({self.modelo}, temp={self.temperature})...")

        try:
            response = requests.post(self.url, json=payload, timeout=600)

        except requests.ConnectionError as e:
            raise LLMConnectionError(
                f"Não foi possível conectar ao Ollama em {self.url}. "
                "Verifique se ele está rodando (rode `ollama serve` num terminal)."
            ) from e

        except requests.Timeout as e:
            raise LLMTimeoutError(
                f"Ollama demorou mais de 10 minutos para responder. "
                f"Modelo '{self.modelo}' pode estar travado ou muito pesado."
            ) from e

        if response.status_code == 500:
            erro_texto = self._extrair_erro_500(response)
            raise LLMModelError(
                f"Ollama retornou erro 500 ao carregar o modelo '{self.modelo}'.\n"
                f"Motivo provável: {erro_texto}\n"
                "Dica: se for 'cudaMalloc failed: out of memory', o modelo não cabe "
                "na sua GPU. Use um modelo menor (ex: qwen2.5-coder:7b)."
            )

        if response.status_code == 404:
            raise LLMModelError(
                f"Modelo '{self.modelo}' não encontrado no Ollama. "
                f"Rode: ollama pull {self.modelo}"
            )

        if response.status_code != 200:
            raise LLMModelError(
                f"Ollama retornou status {response.status_code} inesperado. "
                f"Detalhe: {response.text[:300]}"
            )

        try:
            return response.json()["response"]
        except (KeyError, ValueError) as e:
            raise LLMModelError(
                f"Resposta do Ollama veio em formato inesperado: {response.text[:300]}"
            ) from e

    @staticmethod
    def _extrair_erro_500(response) -> str:
        """Tenta extrair a mensagem real do erro 500 do Ollama."""
        try:
            dados = response.json()
            return dados.get("error", "erro desconhecido")
        except Exception:
            texto = response.text.lower()
            if "cuda" in texto and "out of memory" in texto:
                return "VRAM insuficiente (cudaMalloc failed)"
            if "out of memory" in texto:
                return "memória insuficiente"
            return response.text[:200] or "erro desconhecido"
