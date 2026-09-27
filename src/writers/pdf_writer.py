"""Writer que gera PDF a partir de texto markdown simples."""
import logging
import re

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from .base import WriterBase

logger = logging.getLogger(__name__)


class PDFWriter(WriterBase):
    """Gera PDFs com formatação básica (títulos, bullets e texto).

    Usa a fonte DejaVu Sans (Unicode completo) para evitar problemas
    com caracteres especiais.
    """

    FONTE_REGULAR = "data/fonts/DejaVuSans.ttf"
    FONTE_BOLD = "data/fonts/DejaVuSans-Bold.ttf"

    def escrever(self, conteudo: str, caminho: str) -> None:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("DejaVu", "", self.FONTE_REGULAR, uni=True)
            pdf.add_font("DejaVu", "B", self.FONTE_BOLD, uni=True)
            pdf.set_auto_page_break(auto=True, margin=15)
            largura = pdf.epw

            for linha in conteudo.split("\n"):
                try:
                    self._escrever_linha(pdf, linha.strip(), largura)
                except Exception as e:
                    logger.warning(f"Linha ignorada: {e} | {linha[:60]}")

            pdf.output(caminho)
            logger.info(f"PDF salvo em {caminho}")
        except Exception as e:
            logger.error(f"Erro ao gerar PDF {caminho}: {e}")
            raise

    def _escrever_linha(self, pdf: FPDF, linha: str, largura: float) -> None:
        if not linha:
            pdf.ln(3)
            return

        # Título principal (##)
        if linha.startswith("##"):
            texto = re.sub(r"^#+\s*", "", linha)
            pdf.set_font("DejaVu", "B", 16)
            pdf.ln(2)
            pdf.multi_cell(largura, 8, texto, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("DejaVu", "", 11)
            return

        # Subtítulo (###)
        if linha.startswith("###"):
            texto = re.sub(r"^#+\s*", "", linha)
            pdf.set_font("DejaVu", "B", 13)
            pdf.ln(1)
            pdf.multi_cell(largura, 7, texto, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("DejaVu", "", 11)
            return

        # Bullet
        if linha.startswith(("- ", "* ")):
            texto = linha[2:]
            pdf.set_font("DejaVu", "", 11)
            pdf.multi_cell(
                largura, 6, f"  • {self._limpar_markdown(texto)}",
                new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )
            return

        # Texto normal
        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(
            largura, 6, self._limpar_markdown(linha),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )

    @staticmethod
    def _limpar_markdown(texto: str) -> str:
        texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
        texto = re.sub(r"\*(.+?)\*", r"\1", texto)
        return texto