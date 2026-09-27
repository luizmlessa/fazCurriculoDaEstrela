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
- Liste TODAS as tecnologias, ferramentas e metodologias mencionadas na VAGA. NÃO escolha apenas as que o candidato tem.
- Para CADA uma, marque: ✅ (existe no currículo) ou ❌ (não existe).
- É OBRIGATÓRIO ter pelo menos 1 ❌ se a vaga pede algo que o currículo não tem.
- Se você listou 10 itens e todos são ✅, você está errado. Revise a vaga novamente.
- NUNCA liste algo que está apenas no currículo (ex: Python) como lacuna.
- Calcule o match score: (total de ✅ / total geral) × 100.
- Liste TODAS as lacunas (❌), sem exceção.
- EXEMPLO DE SAÍDA ESPERADA:
  - Java ✅
  - Spring Boot ✅
  - Spring Data ❌
  - MySQL ✅
  - Redis ✅
  - RabbitMQ ❌
  - SQS ❌
  - Kubernetes ✅

PARTE 2 — Currículo adaptado:
- Reescreva o currículo, mantendo TODOS os fatos originais.
- Destaque as competências que a vaga pede E QUE JÁ EXISTEM.

ESTRUTURA OBRIGATÓRIA DO CURRÍCULO:
- A PRIMEIRA linha deve ser EXATAMENTE: `# Luiz Miguel Lessa Ricci`
- A SEGUNDA linha deve ser o título profissional (ex: `Desenvolvedor Backend | Java, Spring Boot, REST APIs`)
- A TERCEIRA linha em diante deve ter o bloco de contato (telefone, email, LinkedIn, GitHub)
- Use `##` para cada seção: `## RESUMO PROFISSIONAL`, `## EXPERIÊNCIA PROFISSIONAL`, `## FORMAÇÃO ACADÊMICA`, `## CERTIFICAÇÕES`, `## COMPETÊNCIAS TÉCNICAS`
- Use `- ` para bullets

ATENÇÃO aos nomes das empresas (copie letra por letra):
- Global Hitss (com dois "s" no final)
- TQI
- HeadMind Partners

PARTE 3 — Carta de apresentação:
- 3 parágrafos.
- Mencione o nome da empresa (extraia da vaga).
- Conecte 2 pontos específicos da vaga com sua experiência real.

REGRAS CRÍTICAS DA CARTA:
- Use linguagem neutra SEM parênteses de gênero.
- Substitua OBRIGATORIAMENTE:
  - "entusiasmado(a)" → "motivado"
  - "pronto(a)" → "preparado"
  - "ansioso(a)" → "interessado"
  - "animado(a)" → "motivado"
- NUNCA mencione tecnologias que não estão no CURRÍCULO ORIGINAL.
- Se a vaga pede uma tecnologia que o candidato não tem, NÃO finja que tem.
- A carta deve reforçar apenas o que o candidato JÁ SABE.

REGRAS OBRIGATÓRIAS GERAIS:
1. Mantenha EXATAMENTE os nomes das empresas, datas e formação.
2. NÃO invente empresas, faculdades, certificações ou tecnologias.
3. Se uma tecnologia da vaga não está no currículo, NÃO mencione no currículo adaptado, apenas na análise.
4. NÃO invente métricas (percentuais, anos, quantidades).

FORMATO DE SAÍDA (use exatamente estes marcadores):

## Análise ATS
[palavras-chave com ✅/❌, match score, lacunas]

## Currículo Adaptado
[currículo começando com `# Luiz Miguel Lessa Ricci` na primeira linha]

## Carta de Apresentação
[carta de 3 parágrafos]
"""