"""Interface base para extratores de texto."""
from abc import ABC, abstractmethod


class ExtratorBase(ABC):
    """Contrato para todos os extratores do pipeline.

    Qualquer nova fonte de dados (PDF, TXT, DOCX, API) deve
    implementar esta interface para ser plugável no pipeline.
    """

    @abstractmethod
    def extrair(self, caminho: str) -> str:
        """Extrai o conteúdo textual de uma fonte.

        Args:
            caminho: Caminho ou referência da fonte de dados.

        Returns:
            Texto extraído como string.
        """
        pass