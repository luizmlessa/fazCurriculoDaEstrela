"""Prompt para análise ATS + currículo adaptado."""


class AnalisePromptBuilder:
    def __init__(self, curriculo: str, vaga: str):
        self.curriculo = curriculo
        self.vaga = vaga

    def construir(self) -> str:
        return f"""Você é um editor de currículos. Sua função é ADAPTAR o currículo abaixo para uma vaga, sem criar informação.

=== CURRÍCULO ORIGINAL ===
{self.curriculo}
=== FIM ===

=== VAGA ===
{self.vaga}
=== FIM ===

TAREFA (2 partes):

PARTE 1 — Análise ATS:
- Liste as 15 principais tecnologias/ferramentas/metodologias mencionadas na VAGA.
- Para cada uma, marque: ✅ (existe no currículo) ou ❌ (não existe).
- O Match Score DEVE ser calculado a partir dos itens listados. Se você listou 10 itens e 7 são ✅, o score é 70%.
- NÃO invente o score. Ele é resultado do cálculo.
- Liste as lacunas (todas com ❌).

FORMATO DA ANÁLISE (siga exatamente):
Java ✅
Spring Boot ✅
Spring Data ❌
MySQL ✅
(continue para todas as tecnologias listadas)
Match Score: X%
Lacunas: item1, item2, item3

PARTE 2 — Currículo Adaptado:
- Reescreva o currículo destacando o que a vaga pede E QUE JÁ EXISTE.
- Mantenha EXATAMENTE: nomes das empresas, datas, formação, certificações.

ESTRUTURA OBRIGATÓRIA:
- Linha 1: # Luiz Miguel Lessa Ricci
- Linha 2: título profissional
- Linha 3+: contato (telefone, email, LinkedIn, GitHub)
- Depois use ## para cada seção, na ordem:
  1. ## RESUMO PROFISSIONAL
  2. ## EXPERIÊNCIA PROFISSIONAL
  3. ## FORMAÇÃO ACADÊMICA
  4. ## CERTIFICAÇÕES
  5. ## COMPETÊNCIAS TÉCNICAS
- Use - para bullets

REGRAS CRÍTICAS DE FIDELIDADE:
- Nomes EXATOS: Global Hitss (dois s), TQI, HeadMind Partners.
- Datas EXATAS:
  - Global Hitss: Set/2023 - Presente
  - TQI: Mai/2022 - Mar/2023
  - HeadMind Partners: Fev/2022 - Mai/2022
- Formação EXATA: Estácio - CST em Análise de Sistemas de Computação (2018 - 2021)
- Certificações EXATAS: copie letra por letra do currículo original.
- Se inventar ou alterar qualquer dado, o resultado será inválido.

ATENÇÃO À SEÇÃO CERTIFICAÇÕES:
- Copie a lista do currículo original LETRA POR LETRA.
- NUNCA coloque tecnologias na seção CERTIFICAÇÕES.

ATENÇÃO À ORTOGRAFIA:
- Microsserviços (não Microservericos)
- Observabilidade
- Mensageria

FORMATO DE SAÍDA (use EXATAMENTE estes marcadores):

## Análise ATS
[tecnologias com ✅/❌ + match score + lacunas]

## Currículo Adaptado
[currículo com estrutura de # e ##]
"""
