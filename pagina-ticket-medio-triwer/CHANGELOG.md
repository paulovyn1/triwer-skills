# Changelog

## 1.2.0 (2026-10-30)
- Verificação de versão no BOOT: compara com o CHANGELOG do GitHub, avisa em uma linha ou bloqueia se a versão nova for `[CRITICAL]` (`references/atualizacao-versao.md`).
- Memória do aluno (`memoria.md`): onboarding rápido de 5 perguntas, regras do aluno, caminhos dos materiais, entregas feitas e preferências. Reaproveita nome, Instagram, pasta de fotos e Notion do `onboarding-triwer`.
- Aprende com as correções: toda correção que vale para as próximas páginas vira regra em `memoria.md` e é aplicada antes da copy e da página seguintes.
- Os rótulos fixos do modelo seguem o tratamento do aluno ("tu" ou "você") e os trechos que contavam casos reais de produção ficaram genéricos.
- Instaladores individuais para Mac e Windows (`instalar-ticket-medio-mac.sh` e `-windows.ps1`) e entrada no instalador "tudo de uma vez".

## 1.1.0 (2026-10-27)
- Modo HTML: `assets/template-pagina.html` (arquivo único, mesma estrutura e mesmo CSS do kit React, com bloco CONFIG e JavaScript simples para as animações), `references/modo-html.md` e `references/formatos.md`.
- Anonimização total: todo texto do kit React e do modelo HTML virou exemplo entre [colchetes], sem nome, empresa, método ou produto de cliente; imagens provisórias; exemplos das referências neutros.
- `hl(texto, "frase")` (React) e `data-hl` (HTML) acham o destaque do título pela frase, em vez de índice.
- `scripts/conferir-restos.py` reescrito: lista [colchetes] pendentes, números zerados no CONFIG, travessão e preço em botão ou meta description; funciona nos dois modos.

## 1.0.0 (2026-10-27)
- Primeira versão: estudo da página de referência, coleta (com confirmação de preço, parcelamento e garantia), copy em 16 seções com regras de preço só na ancoragem e botão de resultado, identidade do expert, montagem em React a partir do kit (estrutura com VSL, painéis escuros, etapas, bônus, ancoragem, conta do custo, garantia), conferência de sobras do exemplo, publicação na Vercel e pacote zip para o time.
