"""Testes para o extrator de arquivos .txt."""
from src.extractors.text_extractor import TextExtractor


def test_extrair_conteudo_de_txt(tmp_path):
    """Garante que o extrator lê corretamente um arquivo TXT."""
    arquivo = tmp_path / "vaga.txt"
    arquivo.write_text("Vaga de Java Pleno", encoding="utf-8")

    resultado = TextExtractor().extrair(str(arquivo))

    assert resultado == "Vaga de Java Pleno"