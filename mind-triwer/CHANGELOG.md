# Changelog

## 1.1.0 (2026-10-30)
- Cores do mapa configuráveis: `PALETA = {"marca": ..., "fundo": ...}` no `conteudo.py`. Sem a linha, o mapa sai em cinza neutro (antes saía sempre em marrom e creme). Quem já personalizou o mapa no MindMeister não é afetado.
- Memória do expert (`memoria.md`): onboarding rápido de 4 perguntas, tom do expert, cores, caminhos e mapas gerados (`references/memoria-modelo.md`).
- Aprende com as correções: toda correção que vale para os próximos mapas vira regra em `memoria.md`.
- Exemplos genéricos: `metodo-granularidade.md` e `escrita-do-no.md` agora usam exemplos ilustrativos, sem trechos de aulas ou casos reais, e os marcadores de voz passam a vir do mapa do próprio expert.

## 1.0.0 (2026-10-23)
- Primeira versão pública: gerador .mind multiplataforma em Python, estrutura de árvore por granularidade, tom do nó a partir do mapa do próprio expert, regras do que da fala entra no mapa e entrega de ramo separado para mapas já personalizados no MindMeister.
