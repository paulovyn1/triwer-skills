# Changelog — dexter-triwer

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

---

## 1.0.0 - 2026-07-15
- Skill criada: Agente de Brainstorm de Produto Novo (Dexter) do Sim
  Inevitável (Triwer). Conduz sessão de brainstorm para aluno sem produto
  definido — 4 blocos de investigação (conhecimento real, público
  candidato, demanda validada, restrição de execução) seguidos de geração
  de 5 ideias distintas.
- Metodologia da **Espiral de Produtos**: 3 eixos independentes por ideia
  (Tipo/Papel — Paquera, Acelerador, Estrela, Acompanhamento; Objetivo —
  Aquisição e Escala, Posicionamento e Autoridade, Lucro e Mantedor de
  Caixa, Recorrência; Ticket, derivado dos outros dois), com matriz de
  afinidade Tipo↔Objetivo como regra de validação, não sugestão solta.
  Substitui a nomenclatura de eixo único do manual-base original — ver
  `references/metodologia.md` para o raciocínio completo da correção.
- **5 direções de transformação** (Entregar pronto, Ensinar a fazer, Fazer
  junto, Analisar ou personalizar, Acompanhar continuamente) como guia de
  geração, garantindo que as 5 ideias sejam genuinamente distintas.
- Cruzamento (interpretar, não descrever) e Fase 2 (gerar as 5 ideias)
  delegados a subagente quando disponível — remove o viés de quem acabou
  de conduzir a entrevista, mesmo padrão da bateria de verificação crítica
  da `sexy-triwer`.
- Teste **nova oportunidade vs. melhoria** aplicado a cada ideia antes de
  apresentar — mesmo teste que a `sexy-triwer` usa para julgar promessa.
- Dexter, Sexy e Dr. House são entradas totalmente independentes — nenhuma
  é pré-requisito de nenhuma outra. Dexter é exclusiva para quem ainda não
  tem produto nenhum; encaminhamento ao Sexy ao final é sugestão de
  continuidade, nunca dependência estrutural.
- Saída sempre em página HTML com identidade visual Triwer (mesma paleta e
  componentes do template do Dr. House), nunca Claude Artifact.
- Salvamento no Notion via HANDOFF para `notion-zettelkasten-si`, só das
  ideias que o aluno confirmar interesse — nunca as 5 automaticamente.
