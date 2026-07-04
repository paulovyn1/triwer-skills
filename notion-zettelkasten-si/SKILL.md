---
name: notion-zettelkasten-si
description: >
  Comportamento padrão para capturar o conteúdo de uma conversa com Claude e transformá-lo
  em notas permanentes no Acervo Notion (modelo Zettelkasten) de um aluno do Sim Inevitável,
  usando o Workspace de Aluno — Perfil do Aluno. Acionar quando o aluno pedir para "salvar
  no meu Notion", "registra isso no Acervo", "processa essa aula/leitura", "atualiza meu
  Notion com isso", "guarda essa ideia", ou qualquer variação de querer que o conhecimento
  da conversa não se perca e vire parte do acervo permanente. Também acionar na primeira
  vez que a skill for usada num workspace novo — nesse caso, rodar primeiro o passo de
  Configuração inicial. Não é para: escrever copy, carrossel, ou preencher a Ficha de
  Produto do zero (isso é trabalho de outras skills) — aqui a skill só captura, classifica
  e conecta conhecimento dentro do Acervo já existente.
compatibility: Claude Desktop, Claude Code, claude.ai
metadata: "v1.1 — julho 2026 — adaptado ao padrão do ecossistema (onboarding, memoria.md)"
---

# Skill: Notion Zettelkasten — Acervo do Aluno (Sim Inevitável)

## O que essa skill é

Esta skill é a versão para alunos do Sim Inevitável da lógica de `obsidian-zettelkasten`
da Milena — mesmo método, suporte diferente. A diferença estrutural mais importante:
o vault da Milena é fixo e conhecido de antemão (por isso está hardcoded na skill dela).
O Notion do aluno **não é** — cada aluno duplicou o mesmo template, mas os IDs de página
mudam para cada cópia. Por isso, antes de qualquer escrita, a skill precisa **localizar**
a estrutura dentro do workspace específico em que está rodando (ver Passo 0).

O princípio de fundo é o mesmo em ambas: **toda nota é um nó em uma rede. Criar sem
conectar é criar lixo.** Uma nota isolada, sem âncora, sem menção a outras páginas, é
tão inútil no Notion do aluno quanto seria no vault da Milena — pior ainda, porque o
aluno não tem o hábito de arrumar depois.

---

## BOOT — EXECUTAR SEMPRE AO INICIAR

### Passo 0a — Verificar onboarding

Tente ler `~/.claude/skills/onboarding-triwer/memoria.md`.

- **Se existir e tiver `onboarding_completo: true`:** prossiga.
- **Se não existir, ou sem essa confirmação:** exiba:

  > Antes de usar esta skill, você precisa concluir a configuração inicial do
  > seu Notion. Rode `/onboarding-triwer` primeiro, depois volte aqui.

  Aguarde. Não prossiga sem o onboarding concluído — esta skill não tem como
  localizar o Acervo do aluno sem isso.

### Passo 0b — Verificar conexão com o Notion

Tente uma busca simples com a ferramenta `notion`. Se não disponível, use o
texto-padrão de conexão (mesmo bloco usado por todas as skills Triwer —
Claude Desktop: Settings → Connectors → `https://mcp.notion.com/mcp`;
claude.ai: Settings → Connectors → Notion; Claude Code:
`claude mcp add --transport http notion https://mcp.notion.com/mcp` → `/mcp`)
e aguarde confirmação antes de continuar.

## Passo 0 — Localizar a estrutura do Acervo (só na primeira vez por workspace)

**Correção (02/07/2026):** a versão anterior desta skill redescobria "Meu
Público" e "Quem sou eu" via `notion-search` a cada workspace novo, e gravava
o cache de IDs **dentro do próprio `SKILL.md`**. Os dois pontos foram
corrigidos: essas duas URLs já são resolvidas uma vez pelo `onboarding-triwer`
(reaproveite em vez de buscar de novo), e o cache agora vai para
`~/.claude/skills/notion-zettelkasten-si/memoria.md` — **nunca para o
`SKILL.md`**, porque todo instalador Triwer sobrescreve `SKILL.md` a cada
atualização da skill (só `memoria.md` é preservado). Gravar cache no
`SKILL.md` significava perder tudo na primeira atualização.

1. Leia `~/.claude/skills/notion-zettelkasten-si/memoria.md`, se existir —
   ela já traz `meu_publico_db_url` e `quem_sou_eu_url` (propagadas pelo
   onboarding) e o cache das páginas específicas desta skill, se já
   localizadas antes.
2. Se `meu_publico_db_url` ou `quem_sou_eu_url` não estiverem lá, leia
   `~/.claude/skills/onboarding-triwer/memoria.md` diretamente e extraia-as
   de lá — não busque por título, elas já têm URL resolvida.
3. Localize as páginas **específicas desta skill** (que nenhuma outra skill
   Triwer usa) por nome via `notion-search`, dentro da página "Acervo" do
   workspace atual, **só na primeira vez** (ou se o cache existir mas uma
   URL não resolver mais — aí refaça a busca só daquela página):

| Página | Como achar |
|---|---|
| **Acervo** | busca por "Acervo" — é a página-mãe, ícone de arquivo |
| **📥 Caixa de Entrada** | dentro do Acervo |
| **📚 Referências** | dentro do Acervo — é onde "Meu Público" e "Quem sou eu" também vivem, como itens marcados `Tipo: 🔓 Essencial` |
| **🎓 Literatura** | dentro do Acervo |
| **💡 Permanentes** | dentro do Acervo |
| **👤 Autores** | dentro do Acervo |
| **⚓ Âncoras** | database de relation usada por todas as anteriores |
| **🪶 Anotações** (produto) | dentro da página "Produtos", fora do Acervo |

4. Grave tudo em `~/.claude/skills/notion-zettelkasten-si/memoria.md`:

```markdown
# Memória — Notion Zettelkasten SI
_Última atualização: [data]_

## Configuração do Notion (propagada pelo onboarding-triwer)
- Meu Público (DB): [meu_publico_db_url]
- Quem sou eu: [quem_sou_eu_url]

## Cache de IDs do Acervo — [nome do workspace]
- Acervo: [URL]
- Caixa de Entrada: [URL]
- Referências: [URL]
- Literatura: [URL]
- Permanentes: [URL]
- Autores: [URL]
- Âncoras: [URL]
- Anotações (produto): [URL]
```

Note: `quem_sou_eu_url` é preenchida pela skill `prisma-triwer` — esta skill
nunca escreve nela.

Se essa for a primeira execução no workspace, depois de localizar tudo,
pergunte ao aluno:

> "Quer que eu adicione uma instrução no seu CLAUDE.md (ou nas instruções do
> projeto) para, sempre que eu identificar algo importante sobre seu público,
> produto ou método durante nossas conversas, te perguntar se quer que eu
> salve no seu Acervo do Notion?"

**Isso só se aplica a quem usa Claude Code ou Claude Desktop** — claude.ai
não tem arquivo de instruções de projeto, então pule esta pergunta nesse
caso; a skill funciona normalmente sem ela, só não ganha esse lembrete extra
fora de quando é explicitamente chamada. Se o aluno aceitar (em Code/
Desktop), adicione a instrução ao `CLAUDE.md` do projeto dele. É opt-in —
nunca ativar esse comportamento automático sem confirmação.

---

## Passo 1 — Classificar o tipo e o destino

O Acervo do aluno tem um fluxo de maturação com 3 estágios, mais duas categorias que
ficam fora do fluxo:

```
📥 Caixa de Entrada  →  📚 Referências / 🎓 Literatura  →  💡 Permanentes
                                                          ↑
                                              👤 Autores (não segue o fluxo)
```

| Tipo | Quando usar | Onde entra |
|---|---|---|
| `inbox` | Captura bruta, ideia solta, ainda não processada | `📥 Caixa de Entrada` |
| `referência` | Conteúdo externo pontual: post, print, exemplo, dado, case de outra marca | `📚 Referências` |
| `literatura` | Síntese de fonte externa estudada a fundo: aula, curso, livro, artigo longo, transcrição | `🎓 Literatura` |
| `permanente` | Insight próprio do aluno — o que ele entendeu, acredita ou descobriu, com uma tese clara | `💡 Permanentes` |
| `autor` | Qualquer pessoa citada pela primeira vez — mentor, autor, cliente, concorrente, entrevistador | `👤 Autores` |

**Regra de ouro:** insight sobre o próprio negócio do aluno (algo que ele percebeu sobre
o público dele, o método dele, uma decisão de produto) é quase sempre `permanente` — não
precisa vir de fonte externa. A "fonte" nesse caso pode ser "Conversa com Claude". Isso é
diferente de simplesmente arquivar algo que alguém de fora disse (isso é `referência` ou
`literatura`).

**Uma nota permanente captura UMA ideia.** Se a conversa gerou 2+ ideias distintas, criar
2+ notas — nunca uma nota "guarda-chuva".

### Páginas essenciais — atualizar, nunca duplicar

Antes de criar qualquer nota nova, checar se o assunto já tem uma página fixa e "🔓
Essencial" no template:

- Assunto é sobre **quem é o público, uma fala de cliente, um perfil de comprador** →
  atualizar a database **Meu Público** (dentro de Referências), não criar nota solta em
  Permanentes. Se o perfil descrito já existe como item da base, complementar o item
  existente; se é um perfil novo, criar item novo na base "Meu Público" (não na Caixa de
  Entrada).
- Assunto é sobre **o produto do aluno** (promessa, ticket, transformação, gancho) →
  atualizar a database **🪶 Anotações** dentro de "Produtos", ou a Ficha do Produto
  específica se ela já existir para aquele produto. Não duplicar em Permanentes.
- Assunto é sobre **quem o aluno é** (viés, posicionamento) → não mexer. Essa página é
  território da skill `prisma-triwer`. Se a conversa gerar algo relevante para ela, avisar
  o aluno para rodar aquela skill, não escrever diretamente.

Isso replica a mesma lógica de "checar duplicata antes de criar" da skill do Obsidian —
só que aqui a duplicata mais comum não é "nota parecida já existe", é "já existe uma
página estrutural pronta para receber exatamente esse tipo de dado".

---

## Passo 2 — Preencher a página

Cada database tem suas próprias propriedades — usar `notion-fetch` na data source (feito
uma vez no Passo 0, ou reconsultado se o schema mudou) para confirmar os campos antes de
criar. Preencher o máximo de propriedades relevantes, não só o título. Campos típicos por
tipo:

- **Caixa de Entrada**: `Nome`, `Tipo` (💡 Ideia / 📖 Leitura / 🎧 Áudio-Vídeo / 💬
  Fala-Citação / 🔗 Link), `Fonte`, `Status` (sempre `📥 Para processar` ao criar), `Âncoras`
- **Referências**: `Nome`, `Tipo` (📗 Livro / 📄 Artigo / 🎥 YouTube-Vídeo / 🎙️ Podcast /
  💬 Citação / 📐 Teoria / 📝 Prompt-Script), `Meu destaque` (o trecho mais útil — é o campo
  que a IA vai reler depois, não deixar vazio), `Autor` (relation), `Âncoras`
- **Literatura**: seguir o mesmo padrão de Referências — a database interna tem schema
  próprio, conferir ao vivo
- **Permanentes**: `Nome` (a tese da nota em uma frase — nunca um substantivo solto),
  `Força` (🌱 Semente ao criar; 🌿 Crescendo/🌳 Madura só quando o aluno já trabalhou a
  ideia antes), `Tipo`, `Origem` (de onde veio o insight — pode ser "Conversa com Claude
  — [data]"), `Âncora`, `Produto Triwer` se aplicável
- **Autores**: `Nome`, `Por que acompanhar` (o que essa pessoa especificamente ensina ou
  representa), `Link`, `Âncora`(s) temática(s)

O corpo da página segue o Manual de Diagramação Triwer — ver `references/diagramacao.md`
antes de escrever qualquer bloco de texto. Não é obrigatório usar todos os elementos do
manual em toda nota (a maioria das notas do Acervo é curta), mas os que valem sempre:

- Nunca um bloco de texto corrido gigante — parágrafos curtos, 1 a 3 linhas
- Callout cinza no topo quando a nota precisa de uma frase de contexto antes do conteúdo
- Negrito em conceitos-chave, nomes de produto, números — nunca para decorar
- Um H2 por seção quando a nota tiver mais de um bloco de ideia

---

## Passo 3 — Conexões (o passo que não pode faltar)

No Obsidian isso é feito com `[[wikilink]]`. No Notion do aluno, a mecânica equivalente
tem duas ferramentas diferentes — usar a certa para cada caso:

### 3a. Âncora obrigatória — relation, não texto

Toda página em Caixa de Entrada, Referências, Literatura, Permanentes ou Autores precisa
de pelo menos **uma Âncora** preenchida via a property de relation `Âncoras`/`Âncora` da
própria database (é o equivalente Notion de tag — não é texto livre, é link real para um
item da database `⚓ Âncoras`).

Antes de criar uma Âncora nova, checar (via `notion-fetch` na database de Âncoras) se já
existe uma que serve semanticamente. Só criar uma Âncora nova quando nenhuma das
existentes cobre o tema — igual à regra do Obsidian: **as Âncoras populam a base
progressivamente**, cada nota nova é oportunidade de reforçar uma âncora existente antes
de inventar outra. Se estiver criando a primeira Âncora do aluno para um tema, dar um
nome de conceito central e reaproveitável (ex: "Vendas orgânicas", não "Post sobre
vendas de terça-feira").

### 3b. Menções inline — toda entidade nomeada no corpo do texto

Além da Âncora (que é property), toda pessoa, produto ou página do Acervo mencionada
**dentro do corpo da nota** deve virar uma menção real de página Notion (`<mention-page
url="...">`), não texto solto. É a mesma disciplina do wikilink inline no Obsidian:

- Ruim: "conversei com o Alfredo sobre isso, ele é referência em copy"
- Correto: mencionar a página do Alfredo (criando-a em Autores primeiro, se ainda não
  existir) e usar a menção no texto, não o nome em texto puro

Se a entidade mencionada ainda não tem página no Acervo, criar a página dela primeiro
(como semente, se for autor ou conceito que merece nota própria) e então mencionar — nunca
deixar um nome importante como texto puro quando existe (ou deveria existir) uma página
para ele.

### 3c. Atualizar páginas existentes (links de entrada)

Depois de criar a nota nova, verificar se alguma página já existente do Acervo deveria
apontar de volta para ela — a Âncora usada é o primeiro lugar a checar: se a Âncora ainda
não tem uma lista de páginas relacionadas no corpo, esse é o momento de começar a
populá-la. Prioridade: Âncora usada > outras Permanentes do mesmo tema > página de
Produto relacionada.

---

## Passo 4 — Índices em vez de páginas gigantes (economia de tokens)

Nunca deixar uma database do Acervo crescer sem estrutura de navegação — o objetivo é
que uma IA (este próprio Claude, em sessão futura) consiga achar a informação relevante
sem precisar ler o Acervo inteiro.

- As databases (Caixa de Entrada, Referências, Literatura, Permanentes, Autores, Âncoras)
  já funcionam como índice por natureza — são tabelas com propriedades filtráveis, não
  precisam de índice adicional.
- Onde a skill deve ativamente evitar página gigante: se uma nota permanente está
  crescendo para virar um `Tipo: Central` (property já existe no schema de Permanentes
  para isso), ela deve funcionar como página-índice — corpo curto que aponta, via menção,
  para as sub-notas relacionadas, em vez de acumular todo o conteúdo na própria página.
  Dividir cedo é mais barato que reorganizar depois.
- Ao ler o Acervo para checar duplicata ou contexto, ler só o necessário: a database
  relevante (via query filtrada, não full fetch) e a página específica candidata — nunca
  todas as páginas do Acervo de uma vez.

---

## Passo 5 — Relatório (sempre ao final)

```
✅ [Nome da nota] · tipo: permanente · Força: 🌱 Semente · página: [link]
📎 Âncora: [Nome da Âncora]
🔗 Mencionado em: [páginas que passaram a linkar para essa nota]
⚠️ Pendências: [se houver — ex: página essencial que precisa de outra skill]
```

---

## Regras invioláveis

1. Nunca criar página sem preencher a Âncora — se nenhuma existente serve, criar uma
   nova antes de salvar a nota.
2. Nunca duplicar — se o assunto já tem página essencial (Meu Público, Ficha de Produto,
   Anotações de Produto) ou nota parecida em Permanentes, atualizar em vez de criar.
3. Nunca escrever em "Quem sou eu" — território exclusivo da skill `prisma-triwer`.
4. Nunca usar título genérico em Permanentes — a tese da ideia em uma frase, nunca um
   substantivo solto.
5. Toda entidade nomeada no corpo da nota vira menção de página — nunca nome importante
   como texto puro quando existe (ou deveria existir) página para ela.
6. Seguir a formatação do Manual de Diagramação Triwer (`references/diagramacao.md`) —
   parágrafos curtos, negrito com propósito, callouts com moderação.
7. Antes de escrever pela primeira vez num workspace novo, rodar o Passo 0 completo e
   (só em Claude Code/Desktop) oferecer a instrução opt-in de captura automática
   no CLAUDE.md do aluno — pular essa oferta em claude.ai, que não tem esse arquivo.
8. Sem cache válido em `memoria.md` para o workspace atual → buscar por nome antes de
   qualquer escrita, nunca assumir URLs de outro aluno ou do vault da Milena. Nunca
   gravar esse cache dentro do `SKILL.md` — instaladores sobrescrevem esse arquivo a
   cada atualização.

---

## Referências
- `references/diagramacao.md` → regras completas de formatação visual (Manual de
  Diagramação Triwer, adaptado)

---

## INSTALAÇÃO

### Estrutura de pastas

```
~/.claude/skills/notion-zettelkasten-si/
├── SKILL.md
├── VERSION
├── memoria.md                        ← criado automaticamente no primeiro uso
└── references/
    └── diagramacao.md
```

### Mac/Linux

```bash
BASE=~/.claude/skills/notion-zettelkasten-si
mkdir -p $BASE/references

cp SKILL.md $BASE/
cp VERSION $BASE/
cp references/diagramacao.md $BASE/references/
```

### Windows

```powershell
$BASE = "$env:USERPROFILE\.claude\skills\notion-zettelkasten-si"
New-Item -ItemType Directory -Force -Path "$BASE\references"

Copy-Item SKILL.md $BASE\
Copy-Item VERSION $BASE\
Copy-Item references\diagramacao.md $BASE\references\
```

### Após instalar

1. Complete o `/onboarding-triwer` antes, se ainda não fez
2. Não precisa rodar por comando — a partir daqui, sempre que você pedir para
   salvar algo no Notion, esta skill entra em ação
3. Na primeira vez, ela localiza a estrutura do seu Acervo (leva alguns
   segundos a mais só nessa primeira execução)
