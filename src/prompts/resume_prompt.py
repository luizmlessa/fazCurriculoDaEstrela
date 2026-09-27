"""Builder de prompt para adaptação de currículos."""


class ResumePromptBuilder:
    """Constrói o prompt enviado ao LLM.

    Separar o prompt em uma classe dedicada facilita ajustes futuros
    e testes unitários sem depender do LLM real.
    """

    def __init__(self, curriculo: str, vaga: str):
        """Inicializa o builder com o currículo e a vaga.

        Args:
            curriculo: Texto do currículo atual.
            vaga: Texto da descrição da vaga.
        """
        self.curriculo = curriculo
        self.vaga = vaga

    def construir(self) -> str:
        """Retorna o prompt formatado para envio ao LLM."""
        return f"""
Você é um especialista em recrutamento técnico e otimização de currículos para ATS.

CURRÍCULO ATUAL:
{self.curriculo}

DESCRIÇÃO DA VAGA:
{self.vaga}

TAREFA:
1. Identifique as 10 palavras-chave mais importantes da vaga.
2. Reescreva os bullets do currículo destacando essas palavras, mantendo a VERACIDADE.
3. Sugira uma carta de apresentação personalizada (máx. 3 parágrafos).

REGRAS:
- NÃO invente experiências.
- Use o formato: Ação + Contexto + Impacto.
- Linguagem técnica e direta.

FORMATO DE SAÍDA:
## Palavras-chave
- ...

## Currículo Adaptado
...

## Carta de Apresentação
...
"""