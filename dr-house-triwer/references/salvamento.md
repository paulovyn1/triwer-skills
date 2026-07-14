# Salvar no Notion do aluno — modelo incremental por checkpoint

> Este arquivo é consultado a partir do **primeiro checkpoint** (fim do Bloco
> 1 da Fase 1), não mais só ao final. Não carregue antes disso — não é
> necessário para conduzir a escavação, só ocupa espaço de contexto à toa
> até ali.

## Por que salvar, e por que incremental

A conversa com o Dr. House frequentemente revela informação nova sobre o
aluno que não estava registrada em lugar nenhum — uma história que ele
contou de passagem, um perfil de público mais preciso do que o que já
estava escrito, um detalhe do produto que não estava cadastrado. Se essa
informação só existir dentro desta conversa, ela se perde.

**Correção de modelo (2026-07-14):** a versão anterior deste arquivo
salvava tudo de uma vez, só depois de o HTML já ter sido gerado (Fase 4).
Isso é arriscado numa Fase 1 potencialmente longa e sem limite de rodadas —
se o contexto estourar no meio da escavação, tudo que ainda não foi salvo
se perde. O modelo correto é salvar **por checkpoint**, ao longo da própria
escavação, nunca esperando o diagnóstico inteiro fechar.

## Quando salvar — 9 checkpoints fixos

Um checkpoint dispara ao final de cada um dos 8 Blocos da Fase 1, e um
nono ao final da Fase 2 (veredito + diagnóstico geral):

1. Fim do Bloco 1 (Criador)
2. Fim do Bloco 2 (Público e situação)
3. Fim do Bloco 3 (Promessa)
4. Fim do Bloco 4 (Mecanismo) — sempre grava o Log de Investigação (ver
   seção própria abaixo), além de qualquer nota de conteúdo
5. Fim do Bloco 5 (Produto e entrega)
6. Fim do Bloco 6 (Preço)
7. Fim do Bloco 7 (Prova)
8. Fim do Bloco 8 (Aquisição)
9. Fim da Fase 2 (veredito de competitividade + diagnóstico geral)

Não colapsar em menos checkpoints (risco de estouro numa Fase 1 longa), não
fragmentar por achado individual dentro de um bloco (reintroduz julgamento
subjetivo sessão a sessão sobre quando parar).

## Quantas notas por checkpoint

O piso é **uma nota-síntese por bloco** — nunca menos. Mas se a síntese do
bloco tiver mais de uma conclusão distinta, divida em notas atômicas
separadas em vez de forçar tudo numa nota-guarda-chuva: mesma regra "uma
nota captura uma ideia" que rege `notion-zettelkasten-si`. Exemplo: se o
Bloco 2 revelar tanto um perfil de público novo quanto um problema de
público misturado, isso é 2 notas, não 1.

## Como grava — HANDOFF para `notion-zettelkasten-si`

Não escreva diretamente com `notion-create-pages`/`notion-update-page`. Ao
fechar um checkpoint:

1. Formule o conteúdo da nota (ou notas) — o que foi descoberto naquele
   bloco, já como tese/conclusão, não como transcrição bruta da conversa
   (a transcrição bruta só se aplica ao Log de Investigação, ver abaixo).
2. Invoque o comportamento da skill `notion-zettelkasten-si` com esse
   conteúdo — ela já resolve a localização do Acervo por workspace, checa
   duplicata antes de criar, tem `Tipo: Central` pronto pra funcionar como
   índice quando aplicável, aplica a diagramação e a disciplina de
   Âncoras/menções inline. Não reimplemente essa mecânica aqui.

Isso substitui o padrão antigo (escrever direto via `notion-update-page`
com `command: update_content`) — a mecânica de escrita fica inteira do lado
de `notion-zettelkasten-si`.

**Fallback se `notion-zettelkasten-si` não estiver disponível no workspace
do aluno:** escreva diretamente com as ferramentas Notion, seguindo a
estrutura das notas já existentes na mesma base como referência de
formato — mas com o mesmo cuidado que já vale em qualquer skill Triwer que
grava no Notion do aluno: `notion-update-page` com `command:
update_content` (inserção pontual, search-and-replace de um trecho
específico) é seguro; `replace_content` apaga a página inteira e a
substitui pelo conteúdo enviado — use `replace_content` **somente** quando
a página for nova ou estiver vazia, nunca numa página que já tem conteúdo
do aluno ou de sessões anteriores. Se criar um banco/database novo (não
uma página simples), sempre marque `is_inline: true` logo depois de criar —
é o padrão de todo banco no workspace do aluno; um banco não-inline quebra
o layout esperado.

## O que o HTML final cita

O HTML gerado na Fase 3 cita **só os nomes dos índices** criados no Acervo
ao longo dos 9 checkpoints — nunca a lista completa de notas atômicas
(isso deixaria o índice redundante e inútil). Se um checkpoint gerou uma
nota do tipo `Central`, é o nome dela que aparece; notas atômicas
individuais não aparecem no HTML, só existem no Acervo.

## O que atualizar em cada checkpoint, e como reconhecer cada nota

**Nota de identidade/viés** (`quem_sou_eu_url`) — checkpoint do Bloco 1
Atualize apenas se a conversa revelou algo novo sobre como o aluno descreve
o que faz de diferente — não duplique o que já está lá. Acrescente, não
substitua, a menos que o que já existe esteja claramente desatualizado.
Esta página é território de escrita da skill `prisma-triwer` — trate como
complemento pontual, não reescrita.

**Base de histórias** (`historias_db_url`) — checkpoint do Bloco 7 (mas
pode surgir em qualquer bloco onde o aluno contar um caso real)
Se o aluno contou algum caso real, com resultado específico, que ainda não
está registrado nessa base, adicione como entrada nova — seguindo a mesma
estrutura de campos que a skill `historias-triwer` usa (Conflito/Fundo do
poço, Decisão contraditória, Resultado inesperado, Dados brutos). Não
reescreva histórias já existentes — só adicione o que é genuinamente novo.

**Database de perfis de público** (`meu_publico_db_url`) — checkpoint do
Bloco 2
Se a escavação revelou uma descrição de público mais precisa do que a que
já está registrada (situação específica, não só demografia), atualize ou
adicione. Se o produto testado revelou que o aluno estava misturando
perfis diferentes — isso também é informação valiosa para registrar, mesmo
que seja um "problema encontrado", não só um dado novo.

**Database de produto** (`produtos_db_url`) — checkpoints dos Blocos 3, 5,
6, 8, e Fase 2
Se o produto diagnosticado nesta sessão ainda não está cadastrado, ou está
desatualizado em relação ao que foi descrito na escavação (preço, formato,
entregáveis), atualize. Mantenha esta nota resumida — é lida por várias
skills (Sexy, carrossel-triwer, criar-aula-triwer), e cada uma paga o custo
de token de ler ela inteira sempre que precisa de contexto de produto.

**Veredito de competitividade** — checkpoint da Fase 2
Registre o veredito (quais dos 5 sinais estão presentes, qual a conclusão
sobre reconstrução ou não) como nota própria — este é o dado que a skill
Sexy vai navegar diretamente ao decidir se precisa reconstruir a
oportunidade antes de trabalhar promessa.

**Log de Investigação — Dr. House (subpágina da nota de produto)** —
checkpoint do Bloco 4, sempre, mesmo que a nota de produto em si não
precise de mudança
Este log existe porque o Bloco 4 (Mecanismo) coleta 3 respostas que a
Seção 1 do HTML resume ou descarta — em especial as respostas 2 ("por que
é diferente do mercado") e 3 ("o que o mercado ensina hoje") raramente
sobrevivem à compressão do resumo, mas são exatamente o material de onde a
skill Sexy extrai diferencial de promessa (o "como" específico por trás do
"o quê" genérico).

Localize a subpágina a partir de `produtos_db_url` — abra a entrada do
produto diagnosticado nesta sessão e procure uma subpágina com esse título
(ou aproximado: "Log de Investigação", "Log Dr. House"). Se não existir
ainda, crie uma como subpágina dela (via HANDOFF para
`notion-zettelkasten-si`, mesma mecânica dos demais checkpoints). Registre,
na íntegra e sem resumir, as 3 respostas do Bloco 4 desta sessão — mesmo
que pareçam repetir o que já foi dito em sessão anterior; cada sessão é um
registro novo, não uma substituição. Se já existir log de sessão anterior,
adicione a entrada nova ao final, com data, não sobrescreva.

Formato de cada entrada:
```
## Sessão [data]
**1. Como funciona (passo a passo):** [resposta literal do aluno]
**2. Por que é diferente do mercado:** [resposta literal do aluno]
**3. O que o mercado ensina hoje:** [resposta literal do aluno]
```

Esta subpágina não é lida por padrão por nenhuma skill — é consultada só
quando o resumo da nota de produto não for suficiente (ex.: a skill Sexy,
ao investigar diferencial de produto, abre este log só se o resumo não
render uma promessa forte). Por isso pode ficar longa e detalhada sem
custar token às leituras normais da ficha.

## Como encontrar o Workspace de Aluno

Use a memória local desta skill (populada no BOOT, Passo 1):

- `quem_sou_eu_url` → nota de identidade/viés ("Quem sou eu" / "Viés Bruto
  Central", preenchida pela skill `prisma-triwer`)
- `historias_db_url` → database "Histórias Inevitáveis"
- `meu_publico_db_url` → database "Meu Público"
- `produtos_db_url` → database "Produtos"

**Se alguma dessas URLs não estiver na memória:** não tente adivinhar o
workspace nem navegar por título — peça a URL diretamente ao aluno, ou
oriente a rodar `/onboarding-triwer` se nenhuma URL foi resolvida ainda.

## Marcação de origem

Ao adicionar conteúdo novo (história, perfil, dado de produto), marque a
origem:

```
> Adicionado em [data de hoje] a partir de uma sessão com o Dr. House.
```

Isso ajuda o aluno (ou você mesmo, numa sessão futura) a distinguir o que
veio de diagnóstico do que ele escreveu manualmente.

## O que não fazer

- Não acumule tudo para salvar só no fim — cada um dos 9 checkpoints grava
  na hora, não em lote depois.
- Não crie nota duplicada quando já existir uma nota próxima do mesmo
  tema — atualize a existente (o HANDOFF para `notion-zettelkasten-si` já
  cobre essa checagem).
- Não invente conteúdo para preencher uma nota vazia além do que a
  conversa realmente revelou.
- Se não encontrar a base de Referências ou qualquer uma das notas
  esperadas, não pare o processo inteiro — avise o aluno no que não foi
  possível salvar automaticamente naquele checkpoint específico e continue
  para o próximo bloco; entregue essa parte como texto para ele colar
  manualmente.
