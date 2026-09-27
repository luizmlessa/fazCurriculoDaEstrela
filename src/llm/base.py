"""Interface base para provedores de LLM."""
from abc import ABC, abstractmethod


class LLMProviderBase(ABC):
    """Contrato para todos os provedores de IA.

    Permite trocar Ollama por OpenAI, Gemini, Claude etc.
    sem alterar o pipeline.
    """

    @abstractmethod
    def gerar_resposta(self, prompt: str) -> str:
        """Envia um prompt ao modelo e retorna a resposta.

        Args:
            prompt: Texto do prompt a ser enviado.

        Returns:
            Resposta gerada pelo modelo.
        """
        pass