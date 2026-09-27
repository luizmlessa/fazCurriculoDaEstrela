"""Writer que salva output em formato Markdown."""
import logging

from .base import WriterBase

logger = logging.getLogger(__name__)


class MarkdownWriter(WriterBase):
    """Salva conteúdo como arquivo .md (UTF-8)."""

    def escrever(self, conteudo: str, caminho: str) -> None:
        """Escreve o conteúdo em um arquivo Markdown.

        Args:
            conteudo: Texto a ser escrito.
            caminho: Caminho de destino do arquivo.

        Raises:
            Exception: Se houver falha na escrita.
        """
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
            logger.info(f"Arquivo salvo em {caminho}")
        except Exception as e:
            logger.error(f"Erro ao escrever {caminho}: {e}")
            raise