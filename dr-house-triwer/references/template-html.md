# Como usar o template HTML do relatório

> Leia este arquivo na Fase 3, ao gerar o HTML. Não carregue antes — só ocupa espaço de
> contexto até esse momento.

## O esqueleto já existe — não regenerar CSS/estrutura do zero

O arquivo `assets/template-diagnostico.html` (dentro desta skill) é o template validado
e aprovado pela Milena — identidade visual Sim Inevitável/Triwer completa (vinho, dourado,
vermelho, bege), com todos os componentes já estilizados. **Copie esse arquivo via
comando de terminal para o destino final — não o leia inteiro.** Ele tem ~300 linhas de
CSS que não precisam entrar no seu contexto; o comando de cópia duplica tudo sem custo de
token. Depois de copiado, edite só os placeholders `{{ASSIM}}` no arquivo de destino —
não invente CSS novo, não redesenhe seções, não troque cores. Esse template já passou por
4 iterações de correção com a Milena; qualquer "melhoria" espontânea de estilo tende a
regredir pra versões piores já descartadas (ver histórico de decisão abaixo, se curioso).

## Placeholders simples (substituição direta de texto)

| Placeholder | Conteúdo |
|---|---|
| `{{NOME_PRODUTO}}` | Nome do produto diagnosticado |
| `{{RESUMO_UMA_LINHA}}` | Formato + público-alvo, extraído do contexto coletado |
| `{{STATUS_GERAL}}` | Um de: "Pronto para validar" / "Ajustes necessários" / "Reconstrução necessária" |
| `{{DATA_HOJE}}` | Data por extenso, ex: "03 de julho de 2026" |
| `{{DIAGNOSTICO_GERAL}}` | O parágrafo de diagnóstico geral (Fase 2) |
| `{{BRIDGE_TEXTO}}` | Sempre presente (pipeline padrão House → Sexy) — ver seção "O bridge para o Sexy" abaixo |
| `{{VERSAO_SKILL}}` | Versão da skill que gerou este HTML — leia do arquivo `VERSION` (sibling do `SKILL.md`) no momento de gerar, nunca hardcode. Vai no rodapé, para auditoria futura do output |

## Blocos repetíveis (os comentários `<!-- X × N -->` no template marcam onde)

- **`BLOCO_CONTEXTO` × 8** — um par `bloco-header` + `<p>` para cada um dos 8 blocos da
  escavação (Fase 1), sempre nesta ordem e numeração: `01 Criador` · `02 Público e
  situação` · `03 Promessa` · `04 Mecanismo` · `05 Produto e entrega` · `06 Preço` ·
  `07 Prova` · `08 Aquisição`.
- **`PONTO_FORTE` × N** — um `<li>` por ponto forte real. Se não houver nenhum ponto
  forte genuíno, não invente um pra preencher — troque a lista inteira por um parágrafo
  simples dizendo que não foi identificado.
- **`ACHADO` × N** — um card por critério com achado real, ordenado por gravidade
  (crítico → estrutural → ajuste fino). Classe e label seguem a tabela abaixo.
- **`BRIDGE_CARD_SEXY`** — bloco sempre incluído, nunca removido (pipeline padrão House →
  Sexy — ver SKILL.md § Encaminhamento e "O bridge para o Sexy" abaixo). O que muda por
  caso é só o texto de `{{BRIDGE_TEXTO}}`.
- **`PERGUNTA` × N** — um `<li>` por pergunta em aberto.

### Tabela de gravidade → classe/label

| Gravidade | `{{GRAVIDADE_CLASSE}}` | `{{GRAVIDADE_ICONE_LABEL}}` |
|---|---|---|
| Crítico | `critico` | `▲ Problema crítico` |
| Estrutural | `estrutural` | `● Problema estrutural` (ou `● Problema estrutural (risco de diferenciação)` quando for especificamente o caso do mecanismo genérico-mas-viável) |
| Ajuste fino | `ajuste` | `■ Ajuste fino` |

Pontos fortes não usam `.achado.forte` como card — eles vivem na lista `.checklist` da
seção própria. O ícone `✓` já está embutido no CSS do `.checklist` (não precisa gerar).

## O bridge para o Sexy — sempre presente, duas ramificações de texto

O `BRIDGE_CARD_SEXY` deixou de ser condicional — a relação House → Sexy é
pipeline padrão em 2 estágios (99% dos alunos vão do House pro Sexy), não
algo que só aparece quando há falha crítica. O que muda é o conteúdo de
`{{BRIDGE_TEXTO}}`:

- **Se qualquer uma das 4 eliminatórias falhou** (situação específica,
  mecanismo próprio, objetivo×ticket, competitividade — ver `regras.md`):
  nomeie qual falhou e por que, e deixe claro que ajuste pontual não
  resolve — o próximo passo é reconstruir a oportunidade com o Sexy antes
  de qualquer outro ajuste fazer sentido.
- **Se nenhuma eliminatória falhou:** não desapareça a seção — reforce que
  quase sempre há refinamento de oferta a fazer, e que o próximo passo
  natural é o Sexy deixar a oportunidade redonda (bônus, julgamento de
  promessa, ativos de marketing), mesmo sem falha estrutural encontrada.

Em nenhum dos dois casos explique como o Sexy funciona por dentro — só
nomeie o encaminhamento.

## O radar (o único componente que exige cálculo, não é placeholder fixo)

Local no template: `{{RADAR_SVG}}`, dentro de `.radar-wrap` na seção `#radar`.

**Regra de inclusão:** só gerar com 3 ou mais critérios com achado real (nunca os 14
sempre). Com menos de 3, remova a seção `.radar-section` inteira e o link "Visão geral"
da `.anchor-bar` — um radar de 1-2 pontos não comunica forma nenhuma.

**Especificação de desenho** (viewBox 500×440, centro em `250,220`, raio máximo ~168px):

1. N eixos = número de critérios com achado. Ângulo de cada eixo = `(360/N) × índice`,
   começando no topo (`-90°`) e seguindo sentido horário.
2. Posição do ponto em cada eixo, do centro pra fora, por gravidade:
   - Crítico → 85% do raio (mais longe do centro — o "pior" fica visualmente saliente)
   - Estrutural → 55% do raio
   - Ajuste fino → 25% do raio
   - Ponto forte → 100% do raio (a régua se inverte aqui: "forte" também fica na borda,
     mas em verde — a leitura correta vem da cor/ícone, não só da distância)
3. Grade de fundo: 4 círculos concêntricos hairline, `stroke="rgba(246,237,221,.15)"`.
4. Forma conectando os pontos: `<polygon>`, `fill="#D5AE66" fill-opacity="0.12"
   stroke="#D5AE66" stroke-width="2" stroke-opacity="0.6"`.
5. Pontos: `<circle r="7">`, `fill` na cor de status (ver tabela abaixo),
   `stroke="#fff" stroke-width="2" stroke-opacity="0.9"`.
6. Labels: `<text>` em `font-family="'Space Mono',monospace" font-size="11"
   letter-spacing="0.5" fill="#F6EDDD" font-weight="700"`, posicionado fora do círculo
   externo, com `text-anchor` ajustado pela posição (start/middle/end conforme o lado do
   eixo). Texto do label: ícone + nome curto do critério em maiúsculas, ex:
   `▲ PREÇO × OBJETIVO`.

**Cores de status para os pontos do radar:**

| Gravidade | Cor do ponto |
|---|---|
| Crítico | `#E52222` |
| Estrutural | `#D5AE66` |
| Ajuste fino | `#B39DDB` |
| Ponto forte | `#3C6B2E` |

Use a amostra `diagnostico-produto-robo-manychat-v4.html` (gerada durante a validação
deste template) como referência de coordenadas reais para um radar de 5 eixos, se for
mais rápido adaptar posições existentes do que recalcular do zero.

## Regras gerais (mesmo fora do que os placeholders cobrem)

- **Nunca usar preto** em lugar nenhum — todo "escuro" é `var(--ink)` (vinho `#2A0200`).
- O dourado precisa aparecer como bloco de peso, não só filete — isso já está garantido
  pelo template (barra de âncoras + hero), não adicionar nem remover esses blocos.
- `<em>` em `<h1>`/`<h2>` já vem estilizado (gradiente dourado no hero, vermelho nos
  títulos de seção) — só usar a tag, não adicionar `style` ou classe extra.
- Sem CDN além do link de fontes do Google — o HTML deve renderizar offline, perdendo
  só a tipografia exata (cai no fallback serif/sans/mono do sistema).

## Histórico de decisão (por que o template é assim, não outra coisa)

Passamos por 4 versões antes de chegar aqui: v1 usava paleta genérica não-relacionada
à marca; v2 tentou "adaptar" a paleta oficial mas ficou com contraste baixo e sem peso
visual; v3 usou os componentes certos (copiados do design system real da reestruturação
do SI) mas com a paleta técnica errada (preto/terracota em vez de vinho/dourado/vermelho
oficiais); v4 corrigiu paleta + deu peso real à marca (hero com "Sim Inevitável" visível,
barra de âncoras dourada, radar em glassmorphism sobre fundo escuro) e foi aprovada.
Não regredir pra nenhuma das versões anteriores.
