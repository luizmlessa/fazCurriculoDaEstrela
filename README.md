# ⭐ Faz Currículo da Estrela

Adaptador de currículos para ATS com IA local (Ollama). Gera currículo adaptado, carta de apresentação e análise de match em PDF — tudo rodando na sua máquina.

## Por que existe

Ferramentas como JobStep, Rezi e Kickresume cobram mensalidade pra fazer o que um LLM local resolve. Este projeto nasceu da recusa em pagar por isso.

- **Zero custo** — sem API paga, sem assinatura
- **Privacidade total** — seu currículo nunca sai da sua máquina
- **Open source** — código aberto, fork à vontade
- **Offline** — funciona sem internet (depois de baixar o modelo)

## O que faz

Dado um currículo (PDF ou TXT) e a URL de uma vaga, o pipeline gera 3 arquivos:

| Arquivo | O que é |
|---------|---------|
| `analise-ats.pdf` | Match score, palavras-chave com ✅/❌ e lacunas |
| `curriculo-adaptado.pdf` | Currículo reescrito destacando o que a vaga pede |
| `carta-apresentacao.pdf` | Carta personalizada pra empresa da vaga |

## Arquitetura

O projeto segue SOLID e Design Patterns:
