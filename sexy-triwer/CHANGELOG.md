# Changelog — sexy-triwer

Este arquivo é lido automaticamente pela própria skill (Passo 0 do BOOT, em
`SKILL.md`) para avisar o aluno quando há uma versão mais nova disponível.
Formato de cada entrada, sempre com a mais recente no topo:

```
## <versão> [CRITICAL] - <data>
- resumo objetivo da mudança
```

A tag `[CRITICAL]` (opcional) é o que faz a skill **bloquear** o uso até o
aluno atualizar, em vez de só avisar. Só use em correções que mudam o
resultado entregue ao aluno — não em ajustes cosméticos.

Histórico anterior à v1.10.1 está condensado no campo `metadata` do
frontmatter do `SKILL.md` (não duplicado aqui).

---

## 1.10.2 [CRITICAL] - 2026-07-10
- Corrige um erro na Etapa 6A que permitia a skill sugerir volume de
  aulas/módulos como ativo de marketing válido mesmo com o pilar Preguiça,
  contradizendo a regra já estabelecida na v1.10. Quem estiver na v1.10.1 ou
  anterior deve atualizar antes de gerar uma nova Oportunidade Sexy, para não
  produzir um resultado inconsistente.

## 1.10.1 - 2026-07-10
- Adiciona o Passo 0 de verificação de versão no BOOT: a skill agora compara
  sua própria versão com a mais recente publicada neste arquivo e avisa o
  aluno quando há atualização disponível (ou bloqueia, se marcada como
  `[CRITICAL]`).
