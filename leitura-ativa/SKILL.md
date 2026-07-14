---
name: leitura-ativa
description: >
  Processa uma leitura completa (artigo, livro, aula, podcast) no Obsidian ou no Notion
  seguindo o método Zettelkasten E atua como parceiro socrático para extrair o que está
  na cabeça do aluno através de perguntas exploratórias, transformando reflexões
  pessoais em notas permanentes do Acervo. Acionar SEMPRE que o aluno disser: "quero
  processar esse artigo", "arquiva essa leitura", "li um artigo sobre X", "tenho grifos
  de uma leitura", "quero fazer notas de um texto", "processar leitura", ou qualquer
  variação de querer transformar uma fonte externa em notas do Acervo. A skill faz DOIS
  trabalhos em sequência: (1) arquivar o conteúdo estruturado (Obsidian ou Notion,
  conforme a preferência do aluno) e (2) conduzir sessão socrática para gerar notas
  permanentes a partir da reflexão pessoal do aluno — as mais valiosas nunca vêm do
  artigo, vêm dessa reflexão.
compatibility: Claude Desktop, Claude Code, claude.ai
metadata: "v1.1.0 — julho 2026. Histórico completo em CHANGELOG.md."
---

# Leitura Ativa — Zettelkasten + Sessão Socrática

Esta skill tem dois blocos em sequência. Não pule o segundo — ele é onde as notas mais
valiosas são geradas. Funciona tanto com Obsidian quanto com Notion — a escolha é feita
uma vez no BOOT (Passo 1) e fica salva para as próximas sessões.

---

## BOOT

### Passo 0 — Verificação de versão

Antes de qualquer coisa, ao iniciar esta skill: leia o arquivo `VERSION` desta skill
(sibling do `SKILL.md`) — essa é a versão local. Em seguida, tente buscar
`https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/leitura-ativa/CHANGELOG.md`
com a ferramenta de acesso à web disponível no ambiente atual (`WebFetch` no Claude
Code/Desktop; navegação/busca nativa no claude.ai). Se não conseguir acessar (sem
internet, sem ferramenta, timeout etc.), não mencione nada e siga direto para o Passo 1.

Se conseguir, leia a entrada mais recente (primeira do arquivo) do CHANGELOG remoto e
compare com a versão local:
- **Igual:** siga para o Passo 1 sem dizer nada.
- **Remota mais nova, sem tag `[CRITICAL]`:** avise em uma linha, ex.: "💡 Há uma versão
  nova da leitura-ativa disponível (v[local] → v[remota]). Não é obrigatório atualizar
  agora, mas recomendo rodar o instalador quando puder." Depois siga para o Passo 1
  normalmente — **não bloqueie**.
- **Remota mais nova, com tag `[CRITICAL]`:** pare aqui. Explique em 2-3 linhas, com base
  no resumo da entrada do CHANGELOG, por que essa versão tem uma correção importante e
  não deve continuar sendo usada, e informe como atualizar:
  - **Claude Code/Desktop:** `irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-leitura-ativa-windows.ps1 | iex` (Windows) ou `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-leitura-ativa-mac.sh | bash` (Mac/Linux).
  - **claude.ai (Skills nativo):** baixar o `.zip` mais recente e reenviar em Settings →
    Capabilities → Skills → Upload skill.
  Aguarde a confirmação de que atualizou antes de seguir para o Passo 1. Se insistir em
  prosseguir mesmo assim, atenda, mas deixe registrado que não é o recomendado.

### Passo 1 — Escolher onde o aluno organiza o Acervo (Obsidian ou Notion)

Leia `~/.claude/skills/leitura-ativa/memoria.md`, se existir.

- **Se já tiver `Destino do Acervo: obsidian` ou `Destino do Acervo: notion` salvo:** use
  essa preferência direto, sem perguntar de novo. Se for Notion, confirme que as URLs das
  databases do Acervo também estão no cache (seção abaixo) antes de seguir — se
  estiverem, vá direto para o BLOCO 1.
- **Se não tiver:** pergunte uma vez, antes de qualquer outra coisa: "Você organiza seu
  Acervo de leituras no Obsidian ou no Notion?" Aguarde a resposta e grave em
  `~/.claude/skills/leitura-ativa/memoria.md`:

  ```markdown
  # Memória — leitura-ativa
  _Última atualização: [data]_

  ## Preferência do aluno
  - Destino do Acervo: obsidian | notion
  ```

Se a resposta for **Obsidian**: siga direto para o BLOCO 1 — nenhum passo extra de
localização é necessário (o vault é resolvido pela skill `obsidian-zettelkasten`).

Se a resposta for **Notion** e as URLs das databases do Acervo ainda não estiverem no
cache:

1. Busque a página "Acervo" no Notion do aluno (mesmo nome usado no template Sim
   Inevitável) com a ferramenta de busca do Notion disponível no ambiente.
2. Dentro dela, localize a database-galeria e resolva os IDs/URLs das databases:
   `📥 Caixa de Entrada`, `🎓 Literatura`, `👤 Autores`, `⚓ Âncoras`, `💡 Permanentes`
   (a database `Comunidade` também pode aparecer ali — é somente leitura, não precisa
   resolver URL dela pra escrita, ver nota de segurança na Referência rápida do Notion).
3. Se não conseguir localizar automaticamente (sem MCP do Notion conectado, busca sem
   resultado, nome de página diferente do padrão), peça a URL da página "Acervo"
   diretamente ao aluno e resolva as databases a partir dela.
4. Grave tudo em `~/.claude/skills/leitura-ativa/memoria.md`, junto da preferência já
   salva:

   ```markdown
   ## Cache de IDs do Acervo Notion
   - Acervo: [URL]
   - Caixa de Entrada: [URL]
   - Literatura: [URL]
   - Autores: [URL]
   - Âncoras: [URL]
   - Permanentes: [URL]
   ```

Depois disso, siga para o BLOCO 1.

---

## BLOCO 1 — Arquivar a leitura (Obsidian ou Notion)

### Passo 0 — Resolver metadados antes de criar qualquer nota

Confirmar que você tem: título exato, autor completo, publicação e ano. Se faltar algum,
tentar inferir com WebFetch. Se não for possível, perguntar **só os campos que faltam** —
não perguntar o que pode ser inferido.

### Passo 1 — Obter o conteúdo completo

Tente buscar o artigo com WebFetch. Se falhar (site bloqueia bots, paywall, erro 429):
peça que o aluno cole o texto completo. Não prossiga com resumo parcial — a nota de
referência precisa do texto completo para extrair todos os links.

### Passo 2 — Criar a nota de referência (Literatura)

Antes de criar, exibir os metadados propostos e pedir confirmação:
> "Vou criar a nota de referência com esses metadados — ok?"
> (Obsidian: `title`, `tags`, `source` do frontmatter — Notion: `Nome`, `Tipo` se
> aplicável, `Autor`, `Data`, `Âncora` da database Literatura)
Aguardar confirmação. Para notas permanentes individuais, não é necessário confirmar.

**Se Obsidian:**

**Pasta:** `04. 🧩 Recursos/Notas/2. Referência/Artigos/`
**Nome do arquivo:** `[Título do Artigo] — [Autor] ([Publicação], [Ano]).md`

Estrutura obrigatória da nota:

```markdown
---
title: "[Título] — [Autor] ([Publicação], [Ano])"
type: reference
date: [hoje]
tags:
  - [tema-1]
  - [tema-2]
status: growing
source: "[URL]"
related: "[[Nome do Autor]]"
---

# [Título] — [[Nome do Autor]] ([Publicação], [Ano])

[Parágrafo de apresentação: quem é o autor, onde publicou, qual é a tese central.]

## Resumo em 3 frases
[O que é. Por que importa. O que muda com isso.]

## Conceito central: [nome do conceito principal]
[Explicação do conceito central com [[wikilinks]] inline em toda entidade nomeada.]

## [Outros conceitos ou argumentos relevantes]
[Um bloco por argumento importante. Usar callout > [!idea] para o insight mais denso.]

## Questões para explorar
[Perguntas abertas dos grifos que não têm resposta própria ainda — retomar no Bloco 2.]
- ? [pergunta aberta]

## Insights extraíveis
- **[Insight 1]** → [[Nota Permanente a criar]]
- **[Insight 2]** → [[Nota Permanente a criar]]

## Notas a criar a partir daqui
- [ ] [[Título como afirmação]] — permanent
- [ ] [[Título como afirmação]] — permanent

## Leitura complementar
[Lista de todos os links citados no artigo com texto âncora e URL.]

### Artigos relacionados sugeridos pela publicação
[Links de artigos sugeridos ao final, se houver.]

## Conexões
- [[Nome do Autor]] — autor do texto
- [[Âncora temática 1]] — âncora temática
- [[Âncora temática 2]] — âncora temática
```

**Se Notion:**

**Database:** `🎓 Literatura`

Antes de criar, buscar na database (pelo cache de `memoria.md`) se já existe uma página
com o mesmo `Nome` — não duplicar.

Propriedades a preencher:
- `Nome` (title): `[Título] — [Autor] ([Publicação], [Ano])`
- `Tipo` (select): escolha entre 🎓 Aula / 📺 Live / 🎤 Evento-Palestra / 🎙️ Podcast /
  📹 Vídeo-aula se a fonte bater com uma dessas opções. **Se for artigo ou livro (sem
  opção correspondente no template — gap conhecido), deixe `Tipo` em branco** e registre
  o tipo real da fonte no corpo da página.
- `Autor` (relation): página do autor em `👤 Autores` (criar antes se ainda não existir —
  ver Passo 3).
- `Data` (date): data de hoje.
- `Âncora` (relation): use sempre a property `Âncora`, **nunca `Tags`** — a base
  `Literatura` tem as duas apontando pra `⚓ Âncoras`, mas `Tags` parece resíduo/duplicata
  do template. Documente essa inconsistência se notar de novo; não tente "consertar" o
  template sozinho.

Como a database `Literatura` não tem campo de texto livre tipo `Fonte`/`URL`, todo o
restante dos metadados (autor completo, publicação, ano, URL) e o conteúdo abaixo vão no
**corpo da página**, seguindo a mesma estrutura do bloco markdown do Obsidian acima —
adaptando o frontmatter YAML para blocos de texto normais do Notion (h1/h2/parágrafo/
lista) e os `[[wikilinks]]` para menções reais de página:

- Parágrafo de apresentação (autor, publicação, tese central — inclui aqui o que seria
  `source`/`type` no Obsidian, já que não há campo pra isso)
- Resumo em 3 frases
- Conceito central (com menções inline pra toda entidade nomeada)
- Outros conceitos/argumentos relevantes
- Questões para explorar (prefixadas com `?`)
- Insights extraíveis
- Notas a criar a partir daqui
- Leitura complementar
- Conexões (menção de página pro autor e pelas âncoras usadas)

### Passo 3 — Criar a nota do autor

**Apenas se o autor ainda não tiver nota/página** — buscar antes.

Se o autor for pouco conhecido ou a busca retornar resultados ambíguos, usar apenas as
informações confirmadas no próprio artigo — não inventar dados biográficos.

**Se Obsidian:**

**Pasta:** `04. 🧩 Recursos/Notas/7. Autores/` — buscar antes com `search_notes`.

```markdown
---
title: "[Nome Completo]"
type: author
date: [hoje]
tags:
  - autor
  - [área de atuação]
status: seedling
related: "[[Nota de referência que originou esta]"
---

# [Nome Completo]

[2-3 frases com o que foi confirmado no artigo. Não inventar o que não foi dito.]

## Trabalhos referenciados no vault
- [[Nota de referência]] — [assunto]

## Conexões
- [[Âncora temática]] — área de atuação
```

**Se Notion:**

**Database:** `👤 Autores` — buscar por `Nome` antes de criar.

Propriedades: `Nome` (title), `Link` (url, se disponível), `Por que acompanhar` (bio
curta com o que foi confirmado no artigo), `Tags` (relation → `⚓ Âncoras` — aqui o nome
da property realmente é `Tags`, diferente da inconsistência documentada em Literatura).

Corpo da página: 2-3 frases confirmadas no artigo (não inventar o que não foi dito) +
menção de página para a nota de Literatura que originou esta.

### Passo 4 — Âncoras

Âncora = o assunto tratado, nunca a origem/formato de como o conteúdo chegou ao Acervo.
Não criar âncoras tipo "estudos" ou "leituras" para agrupar "coisas que eu li" — usar
sempre o tema real.

**Se Obsidian:**

1. Se não existir: criar em `01. ⚓ Âncoras/[Nome].md` com lista inicial (pasta
   `2. Referência/Artigos/`).
2. Se existir: adicionar a nova nota de referência via `append_to_note`.

Para ver as âncoras atuais do vault, listar as notas em `01. ⚓ Âncoras/` — a lista
cresce ao longo do tempo e a versão no vault é sempre a mais atual.

**Se Notion:**

**Database:** `⚓ Âncoras` — buscar (pelo cache de `memoria.md`) se já existe um item com
esse tema.
- Se existir: relacionar a nota de Literatura/Permanente/Autor a ele via a property de
  relation correspondente (`Âncora` em Literatura e Permanentes, `Tags` em Autores).
- Se não existir: criar item novo (`Nome` = tema) e então relacionar.

Em ambos os casos: criar nova âncora só quando o tema não se encaixar em nenhuma
existente e for denso o suficiente para acumular notas ao longo do tempo.

### Passo 5 — Notas permanentes dos grifos

Se o aluno trouxer trechos destacados da leitura, avaliar cada um antes de criar nota:

**Criar nota permanente** quando o trecho:
- Contém uma ideia atômica que se sustenta fora do contexto do artigo
- Pode ser formulado como uma afirmação ou pergunta sem precisar citar a fonte
- Conecta com outros temas do Acervo ou com experiência pessoal de quem está lendo

**Não criar nota** (apenas registrar como evidência na nota de referência) quando o trecho:
- É suporte para outro argumento, não uma ideia autônoma
- Precisa do contexto do artigo para fazer sentido

**Guardar em `## Questões para explorar`** na nota de referência (prefixado com `?`) quando:
- É uma pergunta aberta sem resposta própria ainda
- Tem potencial mas depende das respostas do Bloco 2 para se tornar nota
No início do Bloco 2, retomar essas questões como ponto de partida adicional para as camadas.

Para cada nota permanente criada:

**Se Obsidian:**
- Pasta: `04. 🧩 Recursos/Notas/4. Permanentes/`
- Título como afirmação ou pergunta — nunca substantivo solto
- Linkar via `[[wikilinks]]` para âncoras, para a nota de referência, e para outras
  permanentes relacionadas

**Se Notion:**
- Database: `💡 Permanentes`
- `Nome` (a tese da nota em uma frase — nunca substantivo solto)
- `Força` (select): use `🌱 Semente` como padrão ao criar (tradução de "seedling" — a
  nota amadurece com conexões futuras, não nasce madura; é uma escolha desta skill,
  ajustável se fizer mais sentido diferente). `🌿 Crescendo`/`🌳 Madura` só depois, quando
  o aluno já trabalhou a ideia mais vezes.
- `Origem` (texto livre): cite a nota de Literatura/leitura que originou o insight — não
  existe relation direta de Permanentes para Literatura nesse template.
- `Âncora` (relation): mesma lógica do Passo 4.
- `Fala sobre...` (relation → Autores): só se a nota falar sobre alguém específico.
- Deixe `Tipo` sem preencher — os valores desse campo (Projeto/Manual/Estudo/Central/
  Entregável) são de outro uso do template, não servem pra insight de leitura pessoal.
- Corpo da página: mesma lógica do Obsidian, com menções reais de página (não texto
  puro) para autores e conceitos relacionados.

---

## BLOCO 2 — Sessão socrática

Este bloco começa depois que tudo foi salvo (Obsidian ou Notion). O objetivo é
aprofundar o entendimento do argumento — não forçar correlação com vida pessoal ou
trabalho.

O aluno pode estar lendo qualquer coisa: psicologia, história, política, mitologia,
arte. A sessão serve ao tema da leitura — não ao negócio do aluno.

### Como conduzir

Partir das questões registradas em `## Questões para explorar` na nota de referência.
Se não houver questões registradas, partir dos conceitos centrais identificados no Bloco 1.

**Três camadas de perguntas — nesta ordem:**

**Camada 1 — O argumento em si (1-2 perguntas)**
Explorar onde o argumento é forte, onde é fraco, o que ele pressupõe e não explicita.
- "O que Brown precisa que seja verdade para esse argumento funcionar?"
- "Tem alguma parte que parece conclusão demais — que ela chega rápido demais?"
- "O que esse argumento ignora ou suaviza?"

**Camada 2 — Tensão com outras ideias (1-2 perguntas)**
Conectar com outros autores, correntes ou ideias que o Acervo já tem ou que o aluno já
conhece.
- "Você conhece alguém que argumentaria o oposto? O que diria?"
- "Isso confirma ou contradiz alguma coisa que você já leu?"
- "Qual seria a crítica mais inteligente a esse argumento?"

**Camada 3 — O que o tema abre (1-2 perguntas)**
Perguntar sobre perguntas — o que essa leitura deixa em aberto, o que daria curiosidade
explorar a seguir, qual seria o próximo passo intelectual natural.
- "O que você ficou querendo entender melhor depois de ler isso?"
- "Tem alguma coisa que o livro levantou mas não resolveu?"
- "Se você fosse ler um segundo livro sobre esse tema, o que você buscaria?"

### Regras do comportamento socrático

**Fazer:**
- Virar toda conclusão em pergunta — a conclusão é o começo, não o fim
- Nomear o padrão que o aluno descreveu mas não nomeou — derivar e testar
- Pressionar quando a resposta está incompleta ou parou antes do insight real
- Reconhecimento só quando algo for genuinamente preciso — nomear o que foi bom

**Não fazer:**
- Forçar correlação com vida pessoal ou trabalho — se o tema é Roma, é Roma
- Validar sem questionar: "faz todo sentido" sem perguntar onde quebra
- Encerrar o tema com resumo bonito quando ainda há tensão não explorada
- Elogiar processo: "que reflexão rica" — não serve para nada

**Sinal de que está virando baba ovo:** frases longas com linguagem arredondada depois
de um insight bom. Cortar e reformular em frase curta ou pergunta.

**Quando a resposta não gera nota:**
Se a resposta for vaga, fazer uma pergunta de aprofundamento. Se na segunda tentativa
ainda não houver ideia atômica, avançar — não pressionar uma camada esgotada.

### Transformar respostas em notas

A cada resposta que contiver uma ideia atômica:
1. Identificar a afirmação central
2. Propor um título como afirmação (confirmar se necessário)
3. Criar a nota permanente — mesma mecânica do Bloco 1 Passo 5 (pasta no Obsidian ou
   database `💡 Permanentes` no Notion, conforme o destino escolhido no BOOT)
4. Linkar para âncoras relevantes e para outras notas da sessão
5. Continuar a conversa — não pausar para cada nota

### Quando encerrar

Encerrar quando:
- As três camadas foram exploradas
- As últimas 2-3 respostas não geraram novas notas
- O aluno sinaliza que quer parar

Não encerrar por educação. Se ainda há tensão não explorada, continuar.

---

## Relatório final

Ao final da sessão, apresentar:

```
## ✅ Sessão encerrada

**Notas criadas:**
| Nota | Tipo | Status |
|---|---|---|
| [[Nome]] | reference | growing |
| [[Nome]] | author | seedling |
| [[Nome]] | permanent | evergreen |

**Âncoras atualizadas:** [lista]
**Links salvos na leitura complementar:** [número]
```

No Obsidian, use `[[wikilinks]]` pros nomes das notas nesse relatório. No Notion, use o
link (ou menção) da página no lugar do wikilink, e troque a coluna "Status" pela "Força"
(🌱 Semente / 🌿 Crescendo / 🌳 Madura).

---

## Referência rápida — estrutura do vault (Obsidian)

```
04. 🧩 Recursos/Notas/
  └── 2. Referência/Artigos/     → notas de referência de artigos
  └── 3. Literatura/             → sínteses de livros e cursos
  └── 4. Permanentes/            → insights atômicos próprios
  └── 7. Autores/                → uma nota por autor mencionado
01. ⚓ Âncoras/                   → MOCs temáticos
```

## Referência rápida — estrutura do Acervo (Notion)

```
📥 Caixa de Entrada   → captura bruta (não é destino direto desta skill)
🎓 Literatura         → nota de referência de leituras processadas a fundo — equivalente
                         a "2. Referência/Artigos/" + "3. Literatura/" do Obsidian. Não
                         confundir com 📚 Referências (material raso/swipe-file, fora do
                         escopo desta skill).
👤 Autores            → uma página por autor mencionado
⚓ Âncoras            → temas/MOCs — mesma lógica das âncoras do Obsidian
💡 Permanentes        → insights atômicos próprios
Comunidade            → SOMENTE LEITURA (base pública sincronizada do Triwer) — a skill
                         nunca cria/edita nada ali.
```

Gap conhecido do template: a database `Literatura` não tem opção de `Tipo` para Artigo
nem Livro — deixar o campo em branco nesses casos e registrar o tipo real no corpo da
página (ver Bloco 1, Passo 2).

---

Se Obsidian: seguir a skill `obsidian-zettelkasten` para todas as operações de escrita
no vault — frontmatter obrigatório, wikilinks inline em toda entidade nomeada, âncora em
toda nota permanente.

Se Notion: seguir os mesmos princípios diretamente pelos passos acima — âncora
obrigatória via relation, menção real de página para toda entidade nomeada no corpo,
nunca duplicar página já existente. Não há hoje uma skill Notion separada equivalente à
`obsidian-zettelkasten`; esta própria skill cobre a mecânica Notion nos passos do Bloco 1.
