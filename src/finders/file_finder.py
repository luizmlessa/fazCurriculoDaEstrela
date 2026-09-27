"""Localiza arquivos de currículo na pasta de dados."""
import glob
import logging
import os

logger = logging.getLogger(__name__)


class FileFinder:
    """Encontra o arquivo de currículo mais recente em uma pasta.

    Aceita padrões como 'curriculo*', 'cv*', '*resume*'.
    """

    PADROES = ["curriculo*", "cv*", "resume*"]

    def __init__(self, pasta: str = "data"):
        self.pasta = pasta

    def encontrar_curriculo(self) -> str:
        """Retorna o caminho do currículo mais recente.

        Returns:
            Caminho completo do arquivo.

        Raises:
            FileNotFoundError: Se nenhum arquivo for encontrado.
        """
        for padrao in self.PADROES:
            arquivos = glob.glob(os.path.join(self.pasta, padrao))
            arquivos = [a for a in arquivos if a.lower().endswith((".pdf", ".docx", ".txt"))]
            if arquivos:
                mais_recente = max(arquivos, key=os.path.getmtime)
                logger.info(f"Currículo encontrado: {mais_recente}")
                return mais_recente
        raise FileNotFoundError(f"Nenhum currículo encontrado em {self.pasta}/")