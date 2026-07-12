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
