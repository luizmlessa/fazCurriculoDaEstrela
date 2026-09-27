"""Testes para o builder de prompt."""
from src.prompts.resume_prompt import ResumePromptBuilder


def test_prompt_contem_curriculo_e_vaga():
    """Garante que o prompt inclui o currículo e a vaga."""
    curriculo = "Currículo com Java e Spring Boot"
    vaga = "Vaga para Desenvolvedor Java"
    prompt = ResumePromptBuilder(curriculo, vaga).construir()

    assert curriculo in prompt
    assert vaga in prompt
    assert "Palavras-chave" in prompt


def test_prompt_exige_veracidade():
    """Garante que o prompt instrui o LLM a não inventar dados."""
    prompt = ResumePromptBuilder("Java", "Java").construir()
    assert "NÃO invente" in prompt