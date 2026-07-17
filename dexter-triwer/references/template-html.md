# Como usar o template HTML da sessão de brainstorm

> Leia este arquivo na Fase 3, ao gerar o HTML. Não carregue antes — só ocupa espaço de
> contexto até esse momento.

## O esqueleto já existe — não regenerar CSS/estrutura do zero

O arquivo `assets/template-dexter.html` (dentro desta skill) é o template validado com a
identidade visual Sim Inevitável/Triwer completa (vinho, dourado, vermelho, bege) — mesma
paleta e componentes-base do template do Dr. House, adaptados para os campos próprios do
Dexter. **Copie esse arquivo via comando de terminal para o destino final — não o leia
inteiro.** Depois de copiado, edite só os placeholders `{{ASSIM}}` no arquivo de destino —
não invente CSS novo, não redesenhe seções, não troque cores.

## Placeholders simples (substituição direta de texto)

| Placeholder | Conteúdo |
|---|---|
| `{{RESUMO_UMA_LINHA}}` | Uma frase resumindo o que a sessão revelou (ex.: área de conhecimento + tipo de público candidato) |
| `{{DATA_HOJE}}` | Data por extenso, ex: "15 de julho de 2026" |
| `{{VERSAO_SKILL}}` | Versão da skill que gerou este HTML — leia do arquivo `VERSION` (sibling do `SKILL.md`) no momento de gerar, nunca hardcode. Vai no rodapé |

## Blocos repetíveis (os comentários `<!-- X × N -->` no template marcam onde)

- **`BLOCO_CONTEXTO` × 4** — um par `bloco-header` + `<p>` para cada um dos 4 blocos da
  Fase 1, sempre nesta ordem e numeração: `01 Conhecimento real` · `02 Público candidato` ·
  `03 Demanda validada` · `04 Restrição de execução`. Conteúdo é a síntese de
  `conhecimento_real` / `publico_candidato` / `demanda_validada` / `restricao_execucao` —
  matéria-prima, não análise.
- **`IDEIA` × 5** — um card por ideia gerada na Fase 2. Cada card usa os placeholders:

| Placeholder | Conteúdo |
|---|---|
| `{{IDEIA_NUM}}` | Número da ideia (1 a 5) |
| `{{IDEIA_NOME}}` | Nome de trabalho da ideia |
| `{{TIPO_CLASSE}}` | Classe CSS conforme o Tipo — ver tabela abaixo |
| `{{IDEIA_TIPO}}` | Paquera / Acelerador / Estrela / Acompanhamento |
| `{{IDEIA_OBJETIVO}}` | Objetivo(s) da Espiral de Produtos, separados por " · " se houver mais de 1 |
| `{{IDEIA_TICKET}}` | Faixa de valor real (ex.: "R$147 a R$247"), nunca só Baixo/Médio/Alto — ver `SKILL.md`, "Eixo 3 — Ticket" |
| `{{IDEIA_DIRECAO}}` | Uma das 5 direções de transformação |
| `{{IDEIA_FORMATO}}` | Formato sugerido |
| `{{IDEIA_PUBLICO}}` | Público (pessoa real, situação de vida) |
| `{{IDEIA_PROMESSA}}` | Esboço de promessa (1-2 frases) |
| `{{IDEIA_BACKLIGHT}}` | Backlight — a situação concreta e incômoda que faz o cliente querer isso agora |
| `{{IDEIA_CENARIO_FUTURO}}` | Cenário futuro — o que fica mais fácil/rápido/seguro/lucrativo depois de aplicar |
| `{{IDEIA_VIES}}` | Viés — a lente/crença do aluno que torna a ideia não-intercambiável com a de um concorrente genérico |
| `{{IDEIA_VERDADE_EXISTENTE}}` | Verdade existente — crença do público que a ideia confronta/reorganiza. Omitir o campo (não o card inteiro) se não houver uma identificável — ver regra abaixo |
| `{{IDEIA_NOVA_OPORTUNIDADE}}` | Nova oportunidade — a formulação final e positiva do novo caminho (não o veredito do teste, o que dizer quando ele passa) |
| `{{IDEIA_LASTRO}}` | Lastro — de onde vem a legitimidade da ideia (experiência, resultado próprio/de terceiro, processo repetido) |
| `{{IDEIA_DE_ONDE_VEM}}` | De onde vem — qual matéria-prima da Fase 1 sustenta a ideia, em linguagem natural |
| `{{IDEIA_PONTO_ATENCAO}}` | Ponto de atenção, se houver — omitir o card `.ponto-atencao` inteiro se não houver risco a nomear |

**Todos os campos de texto livre acima (Backlight, Cenário futuro, Viés, Verdade existente,
Nova oportunidade, Lastro, De onde vem, Ponto de atenção, Esboço de promessa) seguem a
regra "Linguagem do output" do `SKILL.md` (Fase 2): nunca citar nome de variável interna
(`conhecimento_real`, `restricao_execucao`, etc.), nunca citar "matriz de afinidade" ou
"teste de nova oportunidade vs. melhoria" como conceito que o aluno precisa reconhecer.
Traduzir sempre pra uma frase natural. Este é o ponto de maior risco de vazamento de
jargão interno — é o texto que o aluno efetivamente lê e guarda.**

**Se `{{IDEIA_VERDADE_EXISTENTE}}` não tiver uma verdade identificável para aquela ideia**,
não force uma genérica — escreva algo como "ainda não há uma crença clara do público pra
confrontar aqui" em vez de inventar. Diferente do Ponto de atenção, este campo **não deve
ser omitido do card** mesmo quando vazio de conteúdo forte — a ausência em si já é uma
informação relevante pro aluno (ver `SKILL.md`, campo "Verdade existente").

### Agrupamento visual dos campos dentro do card

Com os 6 campos novos, o card de ideia tem 15 campos de texto ao todo — listá-los soltos um
embaixo do outro ficaria comprido e ilegível. O template agrupa em 3 blocos visuais, cada um
com seu próprio subtítulo dentro do card (ver `assets/template-dexter.html`):

1. **Campos base** (sem subtítulo, topo do card): Formato, Público, Esboço de promessa.
2. **"Por que essa ideia faz sentido"**: Backlight, Cenário futuro, Viés.
3. **"De onde isso vem"**: Lastro, Verdade existente, De onde vem.
4. **Nova oportunidade**: campo isolado, logo abaixo de Esboço de promessa — é a formulação
   final que o aluno mais precisa reter, não deveria estar espremida dentro de um grupo.
5. **Ponto de atenção** (sem subtítulo, sempre por último, já com destaque visual próprio):
   inalterado, continua sendo omitido inteiro quando não houver risco a nomear.

Não é obrigatório manter exatamente esses 3 grupos se o conteúdo real de uma sessão pedir
outro agrupamento — mas os 6 campos precisam estar presentes de forma legível (com
respiro visual, não espremidos), nunca listados soltos sem nenhuma organização.

### Tabela de Tipo → classe CSS

| Tipo | `{{TIPO_CLASSE}}` |
|---|---|
| Paquera | `tipo-paquera` |
| Acelerador | `tipo-acelerador` |
| Estrela | `tipo-estrela` |
| Acompanhamento | `tipo-acompanhamento` |

## Regras gerais (mesmo fora do que os placeholders cobrem)

- **Nunca usar preto** em lugar nenhum — todo "escuro" é `var(--ink)` (vinho `#2A0200`).
- `<em>` em `<h1>`/`<h2>` já vem estilizado (gradiente dourado no hero, vermelho nos
  títulos de seção) — só usar a tag, não adicionar `style` ou classe extra.
- Sem CDN além do link de fontes do Google — o HTML deve renderizar offline, perdendo só a
  tipografia exata (cai no fallback serif/sans/mono do sistema).
- Se uma ideia não tiver ponto de atenção real, omita o bloco `.campo.ponto-atencao`
  inteiro — não force um risco genérico só para preencher o card.

## Origem do template

Este template reaproveita a base visual e os componentes já validados em 4 iterações no
template do Dr. House (`dr-house-triwer/assets/template-diagnostico.html`) — mesma
paleta, mesma tipografia, mesmo padrão de hero/anchor-bar/footer. O que muda é a seção
central: em vez de achados por critério, o Dexter usa cards de ideia com pills de
classificação (Tipo/Objetivo/Ticket/Direção). Não regredir para paleta genérica ou CSS
customizado fora deste padrão.
