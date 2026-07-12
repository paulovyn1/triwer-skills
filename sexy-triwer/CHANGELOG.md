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

## 2.1.0 - 2026-07-12
- Template `assets/template-oportunidade-sexy.html` atualizado para os
  campos novos da v2.0.0: tag de `papel_esteira` no hero, seção
  `#subpromessa` condicional (só quando Estrela, com link de âncora
  correspondente), tags de `urgencia_compra`/`nivel_consciencia` no bloco de
  público, seção `#antes-depois` (contraste do que mudou), classe visual de
  dores/desejos do público trocada de `.checklist` para `.achado` (comunica
  decisão, não levantamento de achados). Referências de etapa mortas
  corrigidas (Etapa 3A → Etapa 3/5, Etapa 6A → Etapa 9).
- Restaurada a proibição absoluta de gerar o resultado como Claude Artifact
  (regra da v1.9/v1.10 tinha sido perdida por engano numa formulação mais
  permissiva durante a reestruturação da v2.0.0) — nunca artifact, em
  nenhuma hipótese, independente do ambiente.

## 2.0.0 [CRITICAL] - 2026-07-12
- Reestruturação causal completa: objetivo → produto → público → julgamento
  → ativos (era investigação solta → formato/pilar → checklist → garimpo de
  ativos). Etapas 3-6 reescritas.
- Etapa 5 nova (público): situação de vida (teste de contexto operacional,
  não demografia), verdade de mercado (3 perguntas de investigação + fluxo
  Meu Público/MDI), urgência de compra + quem decide, nível de consciência,
  teste de esteira contra o portfólio, pilar de desejo (Segurança tratada
  como modificador, nunca dominante).
- Etapa 6 nova: troca de persona (comprador cético) + bateria tripla de
  julgamento da promessa — Verdade (premissa factual, honestidade,
  concorrente), Desejo (registro por urgência/esteira, cena reconhecível,
  pilar, números pelo esforço), Formulação (vocabulário por consciência,
  fala natural, credencial máxima). Calibrada em sessão real com a Milena
  (7 promessas-teste, vereditos comparados contra previsões travadas).
- Etapa 9 (ativos) reformulada como prova de decisão já fechada, não garimpo
  aberto.
- Referência nova `references/esteira.md` (papéis Paquera/Médio
  Ticket/Estrela/Posicionamento e registro de promessa de cada).
- Fallback de diferencial não encontrado restaurado (recomenda
  `/dr-house-triwer` em vez de beco sem saída).
- Validado por subagente cego antes de aplicar (8 correções incorporadas) e
  por 3 testes cegos pós-aplicação (critério de aceite atingido nos 3
  casos — resolveu canibalização de portfólio, reconheceu corretamente
  quando faixa etária ampla NÃO era problema, e bloqueou promessa com
  contradição entre mecanismo vendido e mecanismo real até o produto ser
  recalibrado).

## 1.10.1 - 2026-07-10
- Adiciona o Passo 0 de verificação de versão no BOOT: a skill agora compara
  sua própria versão com a mais recente publicada neste arquivo e avisa o
  aluno quando há atualização disponível (ou bloqueia, se marcada como
  `[CRITICAL]`).
