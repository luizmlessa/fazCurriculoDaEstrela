"""Builder de prompt para adaptação de currículos."""


class ResumePromptBuilder:
    def __init__(self, curriculo: str, vaga: str):
        self.curriculo = curriculo
        self.vaga = vaga

    def construir(self) -> str:
        return f"""Você é um editor de currículos. Sua ÚNICA função é reescrever o currículo abaixo, destacando as palavras-chave da vaga. Você NÃO cria informação nova.

=== CURRÍCULO ORIGINAL ===
{self.curriculo}
=== FIM DO CURRÍCULO ===

=== DESCRIÇÃO DA VAGA ===
{self.vaga}
=== FIM DA VAGA ===

TAREFA (3 partes):

PARTE 1 — Análise ATS:
- Extraia as 10 palavras-chave mais importantes da vaga.
- Para cada palavra, marque: ✅ (existe no currículo) ou ❌ (não existe).
- Calcule o match score: (palavras com ✅ / total) × 100.
- Liste as 3 principais lacunas (o que a vaga pede e o currículo não tem).

PARTE 2 — Currículo adaptado:
- Reescreva o currículo, mantendo TODOS os fatos originais.
- Destaque as competências que a vaga pede E QUE JÁ EXISTEM.

PARTE 3 — Carta de apresentação:
- 3 parágrafos.
- Mencione o nome da empresa (extraia da vaga).
- Conecte 2 pontos específicos da vaga com sua experiência real.
- Termine com call to action.

REGRAS OBRIGATÓRIAS:
1. Mantenha EXATAMENTE os nomes das empresas, datas e formação.
2. NÃO invente empresas, faculdades, certificações ou tecnologias.
3. Se uma tecnologia da vaga não está no currículo, NÃO mencione no currículo, apenas na análise.
4. NÃO invente métricas (percentuais, anos, quantidades).

FORMATO DE SAÍDA (use exatamente estes marcadores):

## Análise ATS
[palavras-chave, match score, lacunas]

## Currículo Adaptado
[currículo reescrito, mantendo TODOS os fatos originais]

## Carta de Apresentação
[carta de 3 parágrafos]
"""