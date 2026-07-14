# Changelog — dr-house-triwer

Este arquivo é lido automaticamente pela própria skill (verificação de
versão no BOOT, em `SKILL.md`) para avisar o aluno quando há uma versão mais
nova disponível. Formato de cada entrada, sempre com a mais recente no topo:

```
## <versão> [CRITICAL] - <data>
- resumo objetivo da mudança
```

A tag `[CRITICAL]` (opcional) é o que faz a skill **bloquear** o uso até o
aluno atualizar, em vez de só avisar. Só use em correções que mudam o
resultado entregue ao aluno — não em ajustes cosméticos.

Histórico anterior à v1.1.1 está condensado no campo `metadata` do
frontmatter do `SKILL.md` (não duplicado aqui).

---

## 1.3.0 - 2026-07-14
- Adiciona **veredito de competitividade** — critério 15 e 4ª checagem
  eliminatória (`references/competitividade.md`, novo): testa se o produto
  tem sinal suficiente, entre os 5 sinais (sinais que deu certo, estilo de
  vida, validação externa, volume percebido, resultado quantificável), para
  competir de frente no mercado genérico do nicho declarado — ou precisa de
  reconstrução via especificidade antes de qualquer ajuste pontual.
- Bloco 1 da escavação ganha sequência obrigatória de 5 perguntas
  investigativas para captar os sinais de competitividade, formuladas por
  hipótese de nicho (não pergunta genérica de "o que você tem pra
  mostrar").
- Salvamento no Notion deixa de ser tudo-de-uma-vez na Fase 4 e vira
  **incremental por checkpoint**: 9 checkpoints fixos (fim de cada um dos 8
  blocos da Fase 1 + fim da Fase 2), gravando via HANDOFF para
  `notion-zettelkasten-si` em vez de escrita direta
  (`references/salvamento.md` reescrito).
- Encaminhamento ao Sexy deixa de ser condicional à falha de mecanismo —
  agora é sempre presente no HTML (`BRIDGE_CARD_SEXY`), com texto que varia
  conforme alguma eliminatória tenha falhado (nomeia qual) ou nenhuma tenha
  falhado (reforça que quase sempre há refinamento de oferta a fazer).
- Rodapé do HTML gerado passa a exibir a versão da skill
  (`{{VERSAO_SKILL}}`, lida de `VERSION`), para permitir auditoria de qual
  versão gerou cada diagnóstico entregue a um aluno.

## 1.2.0 - 2026-07-12
- Adiciona seção "Log de Investigação — Dr. House" em `references/salvamento.md`:
  cria/atualiza sempre uma subpágina da nota de produto (localizada via
  `produtos_db_url`, sem navegação nova) registrando na íntegra as 3 respostas
  do Bloco 4 (Mecanismo) de cada sessão — especialmente as respostas 2 e 3, que
  o resumo do HTML costuma descartar e são exatamente o material de onde a
  skill Sexy extrai diferencial de promessa. Append por sessão, nunca
  sobrescreve. Consultado sob demanda pela skill Sexy, não lido por padrão.

## 1.1.1 - 2026-07-10
- Adiciona verificação automática de versão no BOOT: a skill agora compara
  sua própria versão com a mais recente publicada neste arquivo e avisa o
  aluno quando há atualização disponível (ou bloqueia, se marcada como
  `[CRITICAL]`).
