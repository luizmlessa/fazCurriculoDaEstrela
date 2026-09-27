"""Prompt para carta de apresentação."""


class CartaPromptBuilder:
    def __init__(self, curriculo: str, vaga: str, empresa: str):
        self.curriculo = curriculo
        self.vaga = vaga
        self.empresa = empresa or "a empresa"

    def construir(self) -> str:
        return f"""Você é um especialista em cartas de apresentação.

=== CURRÍCULO ===
{self.curriculo}
=== FIM ===

=== VAGA ===
{self.vaga}
=== FIM ===

NOME DA EMPRESA: {self.empresa}

TAREFA: Escreva uma carta de apresentação de 3 parágrafos.

ESTRUTURA:
- Parágrafo 1: interesse na vaga + quem você é profissionalmente.
- Parágrafo 2: 2 pontos concretos da sua experiência REAL que conectam com a vaga.
- Parágrafo 3: fechamento + disponibilidade.

REGRAS CRÍTICAS:
1. Mencione "{self.empresa}" no primeiro parágrafo. NÃO escreva "a empresa mencionada" ou "sua empresa".
2. Use SOMENTE tecnologias e experiências que estão no CURRÍCULO acima.
3. NUNCA invente tecnologias, empresas, projetos ou métricas.
4. Se a vaga pede algo que não está no currículo, NÃO mencione.
5. Linguagem neutra SEM parênteses de gênero:
   - entusiasmado(a) → motivado
   - pronto(a) → preparado
   - ansioso(a) → interessado
6. Português brasileiro.

FORMATO DE SAÍDA (use EXATAMENTE este marcador):

## Carta de Apresentação
[texto da carta terminando com:

Atenciosamente,
Luiz Miguel Lessa Ricci]
"""
