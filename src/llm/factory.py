"""Factory de provedores de LLM."""
from .base import LLMProviderBase
from .ollama_provider import OllamaProvider


class LLMFactory:
    """Cria instâncias de provedores de LLM baseado no tipo solicitado."""

    @staticmethod
    def criar(tipo: str = "ollama", **kwargs) -> LLMProviderBase:
        """Retorna uma instância do provedor apropriado.

        Args:
            tipo: Identificador do provedor ("ollama", futuramente "openai").
            **kwargs: Argumentos extras repassados ao construtor.

        Returns:
            Instância de LLMProviderBase.

        Raises:
            ValueError: Se o tipo de provedor não for suportado.
        """
        if tipo == "ollama":
            return OllamaProvider(**kwargs)
        raise ValueError(f"Provider desconhecido: {tipo}")