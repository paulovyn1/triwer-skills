# Changelog — estilo-forge

Este arquivo é lido automaticamente pela própria skill (verificação de
versão antes da Etapa 0, em `SKILL.md`) para avisar o usuário quando há uma
versão mais nova disponível. Formato de cada entrada, sempre com a mais
recente no topo:

```
## <versão> [CRITICAL] - <data>
- resumo objetivo da mudança
```

A tag `[CRITICAL]` (opcional) é o que faz a skill **bloquear** o uso até o
usuário atualizar, em vez de só avisar. Só use em correções que mudam o
resultado entregue — não em ajustes cosméticos.

---

## 1.0.1 - 2026-07-10
- Adiciona verificação automática de versão antes da Etapa 0: a skill agora
  compara sua própria versão com a mais recente publicada neste arquivo e
  avisa o usuário quando há atualização disponível (ou bloqueia, se marcada
  como `[CRITICAL]`).
