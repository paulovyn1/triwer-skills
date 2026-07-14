# Changelog — leitura-ativa

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

---

## 1.0.0 - 2026-07-14 - versão inicial publicada
- Primeira publicação da skill no ecossistema Triwer. Parceira socrática de
  leitura ativa com Zettelkasten no Obsidian: arquiva o artigo em nota de
  referência (Bloco 1) e conduz sessão socrática em três camadas para gerar
  notas permanentes a partir das impressões pessoais do aluno (Bloco 2).
  Depende da skill `obsidian-zettelkasten` já instalada.
