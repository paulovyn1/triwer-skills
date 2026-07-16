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

## 2.3.0 - 2026-07-16
- `references/bio-gerador.md` corrigido em 7 pontos, encontrados testando
  a Etapa 11 (Bio) de ponta a ponta pela primeira vez contra o ciclo
  Gerador→Verificador:
  - Viés magnético (`vies-triwer`/`prisma-si`) não bloqueia mais a etapa —
    o insumo real dos Blocos 3/4 é `nova_oportunidade` (Etapa 6), viés
    externo vira reforço opcional. A maioria dos alunos nunca passou por
    `vies-triwer` quando chega na Sexy.
  - Bloco 5 (prova de autoridade) usa os 5 Sinais de Competitividade (já
    coletados em outra etapa da mesma skill) em vez do binário A/B —
    dentro do mesmo sinal, nomeado vs. agregado agora depende do
    `pilar_dominante` (Vaidade/Soberba/Inveja → nomeado vence; Avareza/
    confiabilidade → agregado pode vencer).
  - 3 linhas é teto, nunca meta — nunca força 3ª linha diluída quando 2
    linhas já cobrem os 5 blocos.
  - Fusão de 2+ blocos na mesma linha vira oração única com conectivo,
    nunca duas frases separadas por ponto (mesmo defeito de paralelismo,
    subtipo novo).
  - Bloco 1 (nome pesquisável) calibrado por `nivel_consciencia`
    (categoria só se o público já a nomeia; senão sintoma/situação), usa
    profissão-resultado nunca técnica/método específico, e nunca leva
    adjetivo de diferencial empilhado.
  - Prova de autoridade nunca narra evento único e passado — 3
    transformações gramaticais testáveis (sujeito 1ª pessoa, quantificador
    plural-genérico, tempo presente/gerúndio) generalizam qualquer caso
    singular em capacidade replicável.
  - Construção "hora de + substantivo + infinitivo cru" banida (agramatical
    sem reflexivo) ao fundir blocos — preferir verbo conjugado direto.
- `SKILL.md`, Etapa 13 (gate) e Etapa 14/template: item de checagem da bio
  sincronizado com as regras acima (não mais "nomeado vs. agregado" cego).
  Resumo final e preenchimento do HTML agora preveem explicitamente o caso
  de bio reprovada 2x — sempre entregue como rascunho "a confirmar" com a
  crítica do Verificador junto, nunca como se fosse aprovada.
- Testado em 6 rodadas Gerador→Verificador (2 casos reais reaproveitados
  de `dexter-triwer`, 1 caso real de produto Sexy já documentado, 1 caso
  real de sessão Sexy anterior) — todas as correções de arquitetura
  confirmadas corrigindo o próprio defeito que motivou cada uma; qualidade
  de prosa sob compressão de caracteres continua sendo o gargalo real, por
  isso a decisão de sempre entregar a bio (aprovada ou não) como material
  para curadoria humana final, nunca como saída definitiva sem revisão.

## 2.2.0 - 2026-07-13
- Etapa 5, Passo 8 novo: teste de incompatibilidade entre os fatos
  declarados do público (definição/papel — ex. "advogado que não entende de
  leis" — e plausibilidade de mercado — ex. "infoprodutor faturando
  R$15-20 mil/mês" junto com relato de comportamento de iniciante perdido).
  Corrige caso real de teste de aluno onde a skill aceitou público
  internamente contraditório sem questionar.
- Etapa 9: teste de origem dos ativos de marketing — as 5 lentes de garimpo
  (promessa, diferencial, pilar, cena, estilo de vida) são ângulos de
  pergunta, não fontes; se várias lentes convergem para o mesmo fato bruto
  do produto, é um ativo só reembalado, não 3-5 itens distintos. Corrige
  caso real onde a lista de ativos era a mesma história de um cliente
  reformulada 5 vezes (print, narrativa, contraste antes/depois etc.).
- Etapa 10, Passo 2 (gate): dois itens novos na checklist de segunda
  passada crítica, espelhando as duas correções acima.
- Template `assets/template-oportunidade-sexy.html`:
  - `#antes-depois` não repete mais a formulação completa da promessa —
    agora recebe um resumo curto (manchete), evitando a mesma frase
    aparecer duas vezes seguidas na página.
  - Contraste do `.bridge-card` (seção `#subpromessa`) e do `.tag.outline`
    reusado fora do `.hero` (seção `#publico`, tags de urgência/nível de
    consciência) blindados com `!important`/regra de contexto — o texto
    claro sobre fundo claro ficava ilegível (visível só ao selecionar).
  - `.numlist` (headlines exploratórias) trocado de `display: grid` para
    `display: flex`: o grid quebrava o texto palavra por palavra em qualquer
    navegador quando o conteúdo do `<li>` misturava `<strong>` + texto solto
    sem wrapper — causa raiz confirmada por teste isolado comparando as duas
    abordagens lado a lado (grid quebrava, flex não). Cada `<li>` agora tem
    um `<div>` com `.headline-modelo` (rótulo do modelo/DOPA) e
    `.headline-texto` (a headline em si) em linhas separadas, não mais
    inline — tentativa anterior de corrigir só com
    `overflow-wrap/word-break/hyphens` não resolvia porque não era a causa.
    Regra `.headline-modelo` também ganhou `font-weight: 700` explícito
    (nunca existiu `.numlist li strong`, diferente de `.checklist li
    strong` — o negrito do rótulo do modelo dependia só do `<strong>` sem
    reforço de CSS, e sumia visualmente mesclado com o resto do texto).
  - Rodapé agora inclui a versão da skill (`[[VERSAO_SKILL]]`, lida do
    `VERSION` no BOOT) — permite identificar depois se um problema
    reportado já foi corrigido em versão mais nova ou se o aluno gerou o
    output já na versão com o furo.

## 2.1.1 - 2026-07-12
- Corrige `description` do frontmatter, que tinha crescido para ~1800
  caracteres na reestruturação da v2.0.0/v2.1.0 e passou a ser rejeitada pelo
  validador de upload do claude.ai (limite de 1024 caracteres) — um aluno
  não conseguiu instalar a skill por causa disso. Descrição reescrita mais
  enxuta (~1000 caracteres), mantendo a metodologia nova e as frases-gatilho.
  Instalações já existentes não são afetadas — só quem ainda não instalou via
  claude.ai precisava dessa correção.

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
