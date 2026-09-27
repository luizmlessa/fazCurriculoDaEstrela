"""Interface base para writers de output."""
from abc import ABC, abstractmethod


class WriterBase(ABC):
    """Contrato para todos os writers de output."""

    @abstractmethod
    def escrever(self, conteudo: str, caminho: str) -> None:
        """Escreve o conteúdo no destino especificado.

        Args:
            conteudo: Texto a ser escrito.
            caminho: Caminho de destino.
        """
        pass