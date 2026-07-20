# Preenchimento do template HTML — Página de resultado

Lido na Etapa 8/15, quando for de fato montar o HTML final. O resultado
desta skill é sempre entregue como página HTML, nunca como texto puro na
conversa — nunca como Claude Artifact, em nenhuma hipótese (ver Etapa 8 e
REGRAS ESTRUTURAIS no SKILL.md).

## Template-base

`~/.claude/skills/sexy-triwer/assets/template-oportunidade-sexy.html`. Parta
sempre desse arquivo — nunca gere a página do zero, em nenhum ambiente.

**Com execução de código disponível** (Claude Code, Claude Desktop, ou
claude.ai com a capability de execução de código/criação de arquivos
ativada — o ambiente roda a skill dentro de um sandbox com acesso real ao
`assets/template-oportunidade-sexy.html`, igual nos três produtos, desde
que a capability esteja ligada): copie o arquivo via comando de
terminal/script para o destino final — **não o leia inteiro antes de
copiar.** O bloco `<style>` tem centenas de linhas de CSS que não precisam
entrar no contexto; o comando de cópia duplica tudo sem custo de token.
Depois de copiado, edite só os placeholders `[[CAMPO]]` no arquivo de
destino (find-and-replace direto no arquivo, sem reabrir o `<style>` pra
revisão).

**Sem execução de código disponível** (a capability estar desligada em
algum ambiente, ou ter caído no meio de uma sessão): não há como copiar um
arquivo em disco sem passar pelo contexto da conversa. Nesse caso, leia o
template uma única vez, mas trate o bloco `<style>` como **conteúdo opaco a
preservar byte a byte** — nunca o reescreva, resuma ou "explique" de volta.
Gere a página de saída como texto/código para o aluno copiar e salvar
manualmente (mesma regra de "nunca vire Artifact" da Etapa 8), fazendo só a
substituição literal de cada `[[CAMPO]]` pelo valor correspondente,
preservando o restante do arquivo — HTML, `<style>` e `<script>` —
caractere por caractere. Se o ambiente também não permitir gerar um bloco
de código desse tamanho de uma vez, sinalize a limitação ao aluno em vez de
reconstruir o template de memória.

Em qualquer um dos dois caminhos, a regra abaixo (Fidelidade obrigatória)
vale sem exceção.

## Fidelidade obrigatória

O bloco `<style>` do template (cores, fontes, nomes de classe) é a
identidade visual Triwer, a mesma usada pelo `dr-house-triwer`. Nunca altere
variáveis de cor, fontes, espaçamento ou crie classes novas. Só o conteúdo
textual muda.

## Regra geral: campo canônico vs. placeholder de renderização

Esta skill guarda o estado em **objetos e coleções** (`perfil_criador`,
`ativos_marketing_sexys`, `headlines_exploratorias`, `destaques_instagram`,
`hero_pagina_vendas`, `pontuacao_pilares_antes`/`depois`,
`feedbacks_verificadores`, `manychat_simulado`, `bonus_*` — contratos
completos em cada etapa do `SKILL.md`). O HTML indexa essas coleções em
placeholders numerados (`ATIVO_1_TEXTO`, `HEADLINE_1_MODELO`, `EIXO_1_LABEL`
etc.) — **os placeholders numerados são slots de renderização, nunca o
estado canônico da skill.** Se precisar reconstruir ou revisar um dado,
volte ao objeto/coleção da etapa correspondente, nunca ao HTML já gerado.

## Preenchimento campo a campo

### Perfil do Criador (seção `#publico`, aba Produto)

De `perfil_criador` (consolidado na Etapa 15, coletado desde a Etapa 2):

```text
[[CRIADOR_RESUMO]]      ← perfil_criador.resumo
[[CRIADOR_BIO]]         ← perfil_criador.bio
[[CRIADOR_AUTORIDADE]]  ← perfil_criador.autoridade
[[CRIADOR_HISTORIA]]    ← perfil_criador.historia
[[CRIADOR_DIFERENCIAL]] ← perfil_criador.diferencial
[[CRIADOR_PROVA]]       ← perfil_criador.prova_principal
[[CRIADOR_ORIGEM]]      ← perfil_criador.origem_prova_principal
```

`[[PROVAS_SOCIAIS_COM_ORIGEM]]` recebe `perfil_criador.provas_sociais_com_origem`
formatada como lista corrida (prova — origem), nunca uma tabela ou JSON cru.
Se a lista estiver vazia, escreva "nenhuma prova social coletada nesta
sessão" em vez de deixar a área em branco.

### Produto e promessa (mesma seção, campos ao redor)

```text
[[NOME_DO_PRODUTO]]       ← produto_atual
[[FORMATO_PRODUTO]]       ← formato_produto (Etapa 3)
[[PAPEL_ESTEIRA]]         ← papel_esteira (Etapa 3)
[[PRODUTO_ENTREGA]]       ← descricao_produto (Etapa 3) — alias visual; internamente use sempre `descricao_produto`
[[NOVA_OPORTUNIDADE]]     ← nova_oportunidade (Etapa 6)
[[A_NOVA_OPORTUNIDADE_RESUMO]] ← versão-manchete curta de nova_oportunidade, pro painel "antes/depois" (#antes-depois)
[[COMO_ERA_ANTES]]        ← a frase/resumo de como o produto era descrito antes da investigação (Etapa 3/4, "estado antigo")
[[SUBPROMESSA]]           ← subpromessa (Etapa 6) — só preencha se papel_esteira = Estrela/registro aspiracional; nos demais casos, deixe o campo com um traço ("—") em vez de placeholder vazio, já que a seção não é mais condicional-removível no template atual (é um campo de valor dentro da ficha, não uma `<section>` própria)
[[DIFERENCIAL_PRODUTO]]   ← diferencial_produto (Etapa 4)
[[ANGULO_ESCOLHIDO]]      ← angulo_escolhido (Etapa 6, Passo 0)
[[SINTESE_DOR_REAL]]      ← sintese_dor_real (Etapa 5, Passo 7)
[[PALAVRAS_CHAVE_ESTRATEGICAS]] ← palavras_chave_estrategicas (Etapa 6)
[[PILAR_DOMINANTE]]       ← pilar_dominante (Etapa 5)
[[PILARES_SECUNDARIOS]]   ← pilares_secundarios (Etapa 5)
[[URGENCIA_COMPRA]]       ← urgencia_compra (Etapa 5)
```

`[[FEEDBACK_VERIFICADOR_NOVA_OPORTUNIDADE]]` (dentro do `<details>`
recolhível da mesma seção) ← `feedbacks_verificadores.nova_oportunidade.parecer`.
Mantenha o bloco `<details>` sempre fechado por padrão (sem atributo
`open`) — é conteúdo de aprofundamento, não a primeira coisa que o aluno lê.

### Alvo/público (aba Alvo — DOR/DESEJO/OBJEÇÃO/arquétipo)

Campos já existentes no template (`ARQUETIPO_PUBLICO`, `DOR_1-3`,
`DESEJO_1-3`, `OBJECAO_1-2`, `NIVEL_DESEJO_LABEL`, `NIVEL_CONSCIENCIA`,
`PUBLICO_ALVO`, `PUBLICO_ALVO_RESUMO`) vêm de `publico_promessa`,
`nivel_consciencia` e da síntese de dor/desejo/objeção já coletada nas
Etapas 2 e 5 — nenhum contrato novo aqui, são campos de texto direto, sem
coleção. `DOR_1-3`/`DESEJO_1-3` são sempre 3 (não uma coleção de tamanho
variável); `OBJECAO_1-2` são sempre 2.

### Pilares do desejo — radar antes/depois (seção `#ativos`)

De `pontuacao_pilares_antes` (Etapa 5) e `pontuacao_pilares_depois` (Etapa 14):

```text
EIXO_N_LABEL        ← nome do pilar N (mesma ordem de pilares-do-desejo/INDEX.md — pilar_1 = Gula, ..., pilar_7 = Avareza)
EIXO_N_NOTA_ANTES   ← pontuacao_pilares_antes[pilar_N]
EIXO_N_NOTA_DEPOIS  ← pontuacao_pilares_depois[pilar_N].nota
```

O template tem 7 slots completos (`EIXO_1` a `EIXO_7`) — preencha todos os
7 pilares sempre, mesmo quando a nota "depois" repete a nota "antes" (pilar
sem elevação real). Nunca deixe um `EIXO_N_NOTA_DEPOIS` vazio — se não
houve elevação, o valor é a própria nota "antes" repetida, nunca um
placeholder sem preencher.

### Seção `#ativos` — narrativa (`ativos_marketing_sexys`)

Cada item aprovado de `ativos_marketing_sexys` é um parágrafo corrido,
nunca campos separados: preenche `[[ATIVO_N_TEXTO]]` com `texto` já pronto
(formato definido em `ativos-gerador.md`). Quando um mesmo `fato_fonte`
render mais de um uso, cada uso é seu próprio bloco, nunca fundidos.

- **Os 5 primeiros aprovados** vão em `[[ATIVO_1_TEXTO]]` a
  `[[ATIVO_5_TEXTO]]` — composição principal.
- **Itens a partir do sexto** vão nos cards `.extra-asset` do bloco
  "Recursos adicionais" (`[[ATIVO_6_TEXTO]]` a `[[ATIVO_10_TEXTO]]`), cada
  card já numerado no HTML ("06 · Recurso adicional" etc.). Esses 5 slots
  extras são o teto físico atual do template — se houver menos de 5 itens
  extras, **remova os cards `<article class="extra-asset">` sobrando**
  (do fim pra trás), nunca deixe um card com `[[ATIVO_N_TEXTO]]` sem
  preencher. Se houver mais de 10 aprovados no total, os excedentes ficam
  de fora do HTML mas continuam completos no resumo da Etapa 15/Notion —
  nunca invente um 11º card sem o placeholder existir fisicamente.
- Se o funil de Ativos não bateu o piso de 2 aprovados, siga "Se sobrarem
  menos de 2 aprovados" em `ativos-gerador.md` — os itens `sugestao`
  substituem os aprovados nos slots principais, deixando claro no texto
  que são sugestões, não ativos prontos.

### Headlines (`#headlines`)

Cada uma de `headlines_exploratorias` preenche dois campos separados, não
um só: `[[HEADLINE_N_MODELO]]` (ex.: "MH004 — Autoridade") e
`[[HEADLINE_N_TEXTO]]` (o texto da headline, sem aspas extras — o layout
de post já fornece a moldura visual). `[[NOME]]` (usado no cabeçalho de
cada post simulado) é o nome/@ do Criador, não um campo por headline —
preencha uma vez, reaproveitado nos 5 posts.

### Destaques do Instagram (`#destaques` ou seção equivalente)

Cada item `aprovado` de `destaques_instagram` preenche um par
`[[DESTAQUE_N_TITULO]]`/`[[DESTAQUE_N_TEXTO]]` (`texto_explicativo`, nunca
o `fato_fonte` bruto). O template tem 3 cards fixos — **se o gate só
sustentou 2 destaques**, remova o terceiro `<article class="highlight-card">`
inteiro (nunca deixe título/texto vazios no card). Nunca force um terceiro
fraco só para preencher o slot.

`[[FEEDBACK_VERIFICADOR_BIO_DESTAQUES]]` (dentro do `<details>` desta
seção) ← `feedbacks_verificadores.bio_destaques.parecer` — cobre os dois
artefatos (Bio + Destaques) com um parecer só; não invente um segundo
bloco de feedback separado.

### Bio do Instagram

`[[BIO_INSTAGRAM]]` ← `bio_instagram` (texto único, já fechado pelo
protocolo Gerador/Verificador da Etapa 11).

### Hero da página de vendas (`#pagina-vendas`)

De `hero_pagina_vendas` (sempre 2 opções, A e B):

```text
[[HERO_PAGINA_VENDAS_A_HEADLINE]]
[[HERO_PAGINA_VENDAS_A_SUBHEADLINE]]
[[HERO_PAGINA_VENDAS_B_HEADLINE]]
[[HERO_PAGINA_VENDAS_B_SUBHEADLINE]]
```

`linha_suporte` e `por_que_funciona` de cada opção **não têm placeholder
físico no template hoje** — não invente um bloco novo para elas; ambas
continuam disponíveis no resumo da Etapa 15 e no Notion. Não crie CTA
dinâmico — o CTA desta seção é sempre visual/estático no template.
`[[FEEDBACK_VERIFICADOR_HERO_PAGINA_VENDAS]]` ← `feedbacks_verificadores.hero_pagina_vendas.parecer`.

### Simulação de ManyChat (`#manychat`)

Cada uma das 10 variáveis de `manychat_simulado` preenche sua própria
`<div class="manychat-message">`, na ordem do roteiro:

```text
MANYCHAT_SAUDACAO → MANYCHAT_AQUECIMENTO → MANYCHAT_PERMISSAO →
MANYCHAT_DEMONSTRACAO → MANYCHAT_PROVA_SOCIAL → MANYCHAT_PITCH →
MANYCHAT_CTA → MANYCHAT_ENTREGA → MANYCHAT_FALLBACK_DUVIDA →
MANYCHAT_FALLBACK_NAO_QUERO
```

Nunca uma variável de texto único corrido — o template já separa cada
bloco em sua própria mensagem visual de chat. Se um bloco ficou sinalizado
como lacuna pelo Gerador (ex.: sem prova social real disponível), preencha
o campo com a lacuna nomeada explicitamente (ex.: "sem prova social
concreta disponível nesta sessão — sugerido incluir depoimento real antes
de publicar"), nunca omita a mensagem nem invente conteúdo.
`[[FEEDBACK_VERIFICADOR_MANYCHAT]]` ← `feedbacks_verificadores.manychat.parecer`.

### Bônus (`#bonus`)

```text
[[BONUS_ANCORA]]   ← bonus_ancora (texto único, proposta + porquê)
[[BONUS_GULA]]     ← bonus_gula (texto único, ou o motivo da dispensa)
[[BONUS_REATIVO]]  ← bonus_reativo (texto único, ou "não aplicável" + motivo)
```

Nunca separe em campos `_proposta`/`_porque` — cada bônus é um texto
único que já carrega os dois.

### `[[VERSAO_SKILL]]` e `[[ANO]]` no rodapé

Preencha `[[VERSAO_SKILL]]` sempre com o conteúdo do arquivo `VERSION`
desta skill lido no BOOT (Passo 0), não com a versão que o aluno pensa ter,
nem com um número fixo — isso permite identificar, em qualquer output
reportado depois, se o problema já foi corrigido em versão mais nova ou se
o aluno estava desatualizado no momento da geração. `[[ANO]]` é o ano
corrente da geração.

## Regras sem exceção

- Nunca deixe `[[CAMPO]]` sem preencher no HTML final — é um marcador de
  template, não um placeholder visível para o aluno.
- Nunca invente um placeholder, seção ou card que não existe fisicamente
  no template no momento do preenchimento — se um artefato desta skill
  ainda não tiver seção correspondente, ele vai só no resumo da Etapa
  15/Notion.
- Blocos `<details>` de feedback do Verificador ficam sempre fechados por
  padrão (sem `open`) — são aprofundamento opcional, não a primeira leitura.
- Cards numerados que sobrarem vazios (ativos extras além do que a lista
  real tem, ou o 3º destaque quando só há 2) são removidos do HTML, nunca
  deixados com o placeholder sem preencher.
- Entrega: gere um HTML autocontido (sem dependências externas além das
  fontes do Google Fonts já referenciadas) e entregue sempre como arquivo
  real — nunca como Claude Artifact, em nenhuma hipótese.
