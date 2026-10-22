# Changelog — carrossel-triwer

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

Histórico anterior à v4.1.1 está condensado no campo `metadata` do
frontmatter do `SKILL.md` (não duplicado aqui).

---

## 4.2.0 - 2026-10-22
- O modelo de carrossel (MC) passa a mandar na estrutura; os 5 blocos viram
  estrutura padrão para quando nenhum MC encaixa.
- Novos testes de escrita sim/não antes de entregar: travessão, frase por
  linha, frase de efeito, gancho "mas...." sem continuidade, troca de 1ª
  pessoa no meio da história, "gerar desejo", reação vaga do público.
- Novo modo adaptação: cola um post validado e a skill mantém a estrutura
  com tema e história novos.
- Regras novas: MC006 com o leitor como sujeito, Provocação com promessa
  implícita nos slides 02 e 03, post de urgência de evento.
- Código Manychat no formato 3 letras + 2 números (ex.: FUN01).
- Modelos atualizados: MC016 novo; variantes novas em MH002, MH003 e MH015.

## 4.1.1 - 2026-07-10
- Adiciona verificação automática de versão no BOOT: a skill agora compara
  sua própria versão com a mais recente publicada neste arquivo e avisa o
  aluno quando há atualização disponível (ou bloqueia, se marcada como
  `[CRITICAL]`).
