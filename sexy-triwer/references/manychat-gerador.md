# Simulação de fluxo ManyChat — arquivo do Gerador

Este arquivo é lido **só pelo subagente Gerador**, nunca pelo Verificador —
o Verificador precisa simular alguém que nunca viu o dossiê e julga só o
efeito do roteiro pronto (ver `manychat-verificador.md`).

**Leia este arquivo na Etapa 13**, depois de já ter `nova_oportunidade` e
`subpromessa` (Etapa 6), `ativos_marketing_sexys` (Etapa 9),
`bonus_ancora`/`bonus_gula` (Etapa 7) e `hero_pagina_vendas` (Etapa 12) —
o fluxo simula como a mesma promessa já validada se desdobraria numa
conversa de venda no direct do Instagram, nunca uma etapa nova de
descoberta.

## O que é esta simulação, e o que ela não é

Isto é **um roteiro de mensagens** (texto — "quem fala o quê, em que
ordem"), nunca um JSON importável, nunca com tags/UTM/custom fields reais.
É mockup de apresentação pro aluno visualizar como a promessa funcionaria
em conversa — a mesma lógica de "simular a página de vendas/ManyChat"
prevista na estrutura v4. Se o aluno quiser o fluxo de verdade, pronto
pra publicar no ManyChat, isso é trabalho de outra skill
(`manychat-flow-writer`), fora do escopo da Sexy.

**Nunca gere:** ações técnicas de automação (`set_optin`, `add_tag`,
custom fields, UTM, webhook, planilha, condições `IS_UNKNOWN`), blocos de
"Ações" isolados, ou qualquer instrução de configuração de plataforma. O
roteiro é só o que um visitante real leria no direct — texto e botões.

## Fonte deste método

Framework validado em `manychat-flow-writer` (skill irmã do ecossistema
Triwer, `github.com/paulovyn1/manychat-flow-writer`), especificamente o
**Framework de VENDA** — baseado em 5 fluxos reais de venda (2023-2024)
com vendas rastreadas. Esta etapa usa só os blocos de conteúdo/copy do
framework, removendo os blocos puramente técnicos de automação (que não
significam nada fora do ManyChat real e poluiriam uma simulação de
apresentação).

## Estrutura — 9 blocos de conteúdo, nesta ordem

```
BLOCO 1 — Saudação
BLOCO 2 — Aquecimento (entrega de valor / identificação com a dor)
BLOCO 3 — Permissão ("Posso te dizer/mostrar?")
BLOCO 4 — Demonstração (o produto/mecanismo em ação)
BLOCO 5 — Prova social (depoimento/resultado)
BLOCO 6 — Pitch (benefícios + âncora de preço + urgência)
BLOCO 7 — CTA triplo (Link / Dúvida / Não quero)
BLOCO 8 — Entrega do link (se CTA = Link)
BLOCO 9 — Fallback de dúvida e fallback de não quero
```

Nunca inclua bloco de "Condição de aluno" (não faz sentido numa simulação
sem contato real) nem bloco de ações técnicas entre blocos de conteúdo.

### Bloco 1 — Saudação

Formato fixo, adaptado ao produto/aluno em questão (nunca literalmente
"Sun" — é o vocabulário/persona do Triwer original, a Sexy simula pra
qualquer aluno, então adapte o nome/persona ou deixe genérico
"[assistente]"):

```
"[Saudação animada e acolhedora] Aqui é o [assistente/persona do aluno].

[Confirmação do que a pessoa fez — comentou/clicou em X]
[O que vai ser entregue agora — conectado ao tema do gatilho]

[Instrução simples de como avançar]"

[Botão único: variação curta de "Continuar"]
```

**Regra:** a saudação nunca entrega o conteúdo — só confirma a ação e pede
para clicar. Puxe o "gatilho" (post/tema que leva ao fluxo) de uma das
headlines aprovadas na Etapa 10, ou de `hero_pagina_vendas` — nunca
invente um gatilho solto.

### Bloco 2 — Aquecimento

Entrega de valor ou identificação com a dor real de `publico_promessa`
(Etapa 5) — nunca genérico. Puxe de `ativos_marketing_sexys` quando
houver um ativo que sirva de conteúdo de aquecimento (ex.: tática
replicável vira um mini-ensinamento aqui).

**Regra de continuidade — o fluxo continua o gatilho, não o repete:** a
pessoa acabou de ver o post/gatilho. Nunca pergunte "você viu que..." nem
resuma o que já foi visto — aprofunde, revele o próximo nível.

### Bloco 3 — Permissão

Pergunta curta pedindo licença antes de revelar algo importante ("Posso
te contar...", "Posso te mostrar..."). Nunca entregue direto.

### Bloco 4 — Demonstração

O próprio mecanismo/diferencial do produto em ação — puxe de
`diferencial_produto` (Etapa 4) e `nova_oportunidade`. A prova é a
experiência sendo mostrada, não uma lista de features.

### Bloco 5 — Prova social

Depoimento ou resultado real — puxe de `ativos_marketing_sexys`
(categoria de posição divergente ou cenário de vida) ou de histórias já
coletadas no Notion do aluno. **Nunca invente depoimento ou número.** Se
não houver prova real disponível no dossiê, omita o bloco e sinalize a
lacuna no formato de saída — não force um depoimento fictício.

### Bloco 6 — Pitch

```
1. Identificação narrativa de quem é essa oportunidade (não lista)
2. O que é — descrição prática, nunca genérica
3. Principal diferencial em 1 frase (puxe de nova_oportunidade)
4. Entregáveis principais — lista objetiva, máximo 5 itens
5. Âncora de preço, se houver (puxe de bonus_ancora/bonus_gula)
6. Urgência leve e real — nunca fake (turma limitada, prazo real, se houver)
7. CTA com permissão ("Posso liberar o link?")
```

**Regra:** se um bloco de permissão anterior (Bloco 3) já criou expectativa
de revelação, o pitch não pede permissão de novo antes de começar — só no
fechamento (item 7 acima).

### Bloco 7 — CTA triplo

3 botões, nunca mais: variações curtas de "sim" (leva ao Bloco 8),
"dúvida" (leva ao fallback de dúvida), "não quero" (leva ao fallback de
recusa). Texto de botão: máximo 25 caracteres, nunca genérico ("Clique
aqui", "Saiba mais"), sempre refletindo a resposta emocional esperada.

### Bloco 8 — Entrega do link

Mensagem curta confirmando a liberação + botão apontando pro link de
compra (placeholder, nunca invente URL real).

### Bloco 9 — Fallbacks

**Fallback de dúvida:** empático, oferece ajuda — nunca ignora a dúvida.
**Fallback de "não quero":** nunca abandona — leve, sem pressão, oferece
saída digna (ex.: conteúdo relacionado). Dramático-humorístico funciona
melhor que empático neutro, se o tom do aluno permitir (ver `nova_oportunidade`
e o tom já usado no resto do dossiê Sexy).

## Regras de copy — direct é conversa, não campanha

- **Mensagens curtas:** 1-2 linhas por mensagem, nunca parede de texto.
  Listas de benefícios: máximo 4-5 itens.
- **Botões com variação:** 2-3 opções pro mesmo destino simulam resposta
  humana (nunca botão único fora da saudação).
- **Sem prefixo editorial nem jargão de automação** visível na conversa
  simulada — nunca aparecem palavras como "tag", "UTM", "webhook".
- **Ancoragem de preço, se houver:** sempre mostrar valor percebido antes
  do preço com desconto — puxe de `bonus_ancora` se ele já tiver essa
  estrutura, nunca invente número.
- **Urgência sempre ancorada em algo real** (turma limitada, prazo) —
  nunca urgência fake.
- **Nunca use dado, depoimento, número ou prova que não esteja em
  `ativos_marketing_sexys`, `nova_oportunidade`, `bonus_ancora`/`bonus_gula`
  ou no dossiê já coletado** — mesma regra de "nunca invente" das demais
  etapas desta skill.

## Formato de saída — cada bloco é sua própria variável

**Cada bloco do roteiro é salvo como uma variável nomeada própria, nunca
como um texto único corrido** — o preenchimento do template HTML final
(Etapa 8/15) lê campo a campo; se os 9 blocos saírem como um blob de
texto só, não tem como popular cada seção do template separadamente.
Mesma lógica já usada em `bio_instagram`, `destaques_instagram`,
`hero_pagina_vendas` — cada um desses já é uma variável isolada, não um
parágrafo único.

```
manychat_saudacao: [texto] → [Botão]

manychat_aquecimento: [texto]

manychat_permissao: [texto] → [Botão]

manychat_demonstracao: [texto]

manychat_prova_social: [texto, ou null + nota "sem prova real disponível
no dossiê para este bloco — lacuna sinalizada, não inventado"]

manychat_pitch: [texto completo dos 7 itens da estrutura de pitch]

manychat_cta: [texto] → 3 botões: [Sim] / [Dúvida] / [Não quero]

manychat_entrega: [texto] → [Botão link — placeholder]

manychat_fallback_duvida: [texto]

manychat_fallback_nao_quero: [texto]
```

Guarde as 10 variáveis acima individualmente no documento-hub da sessão
(Etapa 1) — não apenas um resumo consolidado. O agrupamento
`manychat_simulado` citado no `SKILL.md` é a **coleção** dessas 10
variáveis, não um texto corrido separado delas.

Gere **1 versão apenas** (diferente de Headlines/Hero, que geram 2-5
propostas) — o fluxo é uma sequência única de conversa, não variações
paralelas para escolher.
