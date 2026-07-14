---
name: leitura-ativa
description: >
  Processa uma leitura completa no Obsidian seguindo o método Zettelkasten E atua como
  parceiro socrático para extrair o que está na cabeça de Milena através de perguntas
  exploratórias, transformando reflexões pessoais em notas permanentes do vault. Acionar
  SEMPRE que Milena disser: "quero processar esse artigo", "arquiva essa leitura
  no Obsidian", "li um artigo sobre X", "tenho grifos de uma leitura", "quero fazer notas
  de um texto", "processar leitura", ou qualquer variação de querer transformar uma fonte
  externa em notas do vault. A skill faz DOIS trabalhos em sequência: (1) arquivar o
  conteúdo estruturado no Obsidian e (2) conduzir sessão socrática para gerar notas
  permanentes a partir das impressões pessoais de Milena — as mais valiosas nunca vêm
  do artigo, vêm dela.
compatibility: Claude Desktop, Claude Code, claude.ai
metadata: "v1.0.0 — julho 2026. Histórico completo em CHANGELOG.md."
---

# Leitura Ativa — Zettelkasten + Sessão Socrática

Esta skill tem dois blocos em sequência. Não pule o segundo — ele é onde as notas mais
valiosas são geradas.

---

## BOOT — Passo 0: Verificação de versão

Antes de qualquer coisa, ao iniciar esta skill: leia o arquivo `VERSION` desta skill
(sibling do `SKILL.md`) — essa é a versão local. Em seguida, tente buscar
`https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/leitura-ativa/CHANGELOG.md`
com a ferramenta de acesso à web disponível no ambiente atual (`WebFetch` no Claude
Code/Desktop; navegação/busca nativa no claude.ai). Se não conseguir acessar (sem
internet, sem ferramenta, timeout etc.), não mencione nada e siga direto para o BLOCO 1.

Se conseguir, leia a entrada mais recente (primeira do arquivo) do CHANGELOG remoto e
compare com a versão local:
- **Igual:** siga para o BLOCO 1 sem dizer nada.
- **Remota mais nova, sem tag `[CRITICAL]`:** avise em uma linha, ex.: "💡 Há uma versão
  nova da leitura-ativa disponível (v[local] → v[remota]). Não é obrigatório atualizar
  agora, mas recomendo rodar o instalador quando puder." Depois siga para o BLOCO 1
  normalmente — **não bloqueie**.
- **Remota mais nova, com tag `[CRITICAL]`:** pare aqui. Explique em 2-3 linhas, com base
  no resumo da entrada do CHANGELOG, por que essa versão tem uma correção importante e
  não deve continuar sendo usada, e informe como atualizar:
  - **Claude Code/Desktop:** `irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-leitura-ativa-windows.ps1 | iex` (Windows) ou `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-leitura-ativa-mac.sh | bash` (Mac/Linux).
  - **claude.ai (Skills nativo):** baixar o `.zip` mais recente e reenviar em Settings →
    Capabilities → Skills → Upload skill.
  Aguarde a confirmação de que atualizou antes de seguir para o BLOCO 1. Se insistir em
  prosseguir mesmo assim, atenda, mas deixe registrado que não é o recomendado.

---

## BLOCO 1 — Arquivar o artigo no Obsidian

### Passo 0 — Resolver metadados antes de criar qualquer nota

Confirmar que você tem: título exato, autor completo, publicação e ano. Se faltar algum,
tentar inferir com WebFetch. Se não for possível, perguntar **só os campos que faltam** —
não perguntar o que pode ser inferido.

### Passo 1 — Obter o conteúdo completo

Tente buscar o artigo com WebFetch. Se falhar (site bloqueia bots, paywall, erro 429):
peça que Milena cole o texto completo. Não prossiga com resumo parcial — a nota de
referência precisa do texto completo para extrair todos os links.

### Passo 2 — Criar nota de referência

**Pasta:** `04. 🧩 Recursos/Notas/2. Referência/Artigos/`
**Nome do arquivo:** `[Título do Artigo] — [Autor] ([Publicação], [Ano]).md`

Antes de criar, exibir o frontmatter proposto e pedir confirmação:
> "Vou criar a nota de referência com esses metadados — ok?"
> `title`, `tags`, `source`
Aguardar confirmação. Para notas permanentes individuais, não é necessário confirmar.

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

### Passo 3 — Criar nota do autor

**Pasta:** `04. 🧩 Recursos/Notas/7. Autores/`
**Apenas se o autor ainda não tiver nota no vault** — buscar antes com `search_notes`.

Se o autor for pouco conhecido ou a busca retornar resultados ambíguos, usar apenas as
informações confirmadas no próprio artigo — não inventar dados biográficos.

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

### Passo 4 — Âncoras

Âncora = o assunto tratado, nunca a origem/formato de como o conteúdo chegou ao vault
(isso já é o `type: reference` + pasta `2. Referência/Artigos/`). Não criar âncoras tipo
"estudos" ou "leituras" para agrupar "coisas que eu li" — usar sempre o tema real.

Para cada âncora temática relevante:
1. Se não existir: criar em `01. ⚓ Âncoras/[Nome].md` com lista inicial
2. Se existir: adicionar a nova nota de referência via `append_to_note`

Para ver as âncoras atuais do vault, listar as notas em `01. ⚓ Âncoras/` — a lista
cresce ao longo do tempo e a versão no vault é sempre a mais atual.

Criar nova âncora quando o tema não se encaixar em nenhuma existente e for denso o
suficiente para acumular notas ao longo do tempo.

### Passo 5 — Notas permanentes dos grifos

Se Milena trouxer trechos destacados da leitura, avaliar cada um antes de criar nota:

**Criar nota permanente** quando o trecho:
- Contém uma ideia atômica que se sustenta fora do contexto do artigo
- Pode ser formulado como uma afirmação ou pergunta sem precisar citar a fonte
- Conecta com outros temas do vault ou com experiência pessoal de Milena

**Não criar nota** (apenas registrar como evidência na nota de referência) quando o trecho:
- É suporte para outro argumento, não uma ideia autônoma
- Precisa do contexto do artigo para fazer sentido

**Guardar em `## Questões para explorar`** na nota de referência (prefixado com `?`) quando:
- É uma pergunta aberta sem resposta própria ainda
- Tem potencial mas depende das respostas do Bloco 2 para se tornar nota
No início do Bloco 2, retomar essas questões como ponto de partida adicional para as camadas.

Para cada nota permanente criada:
- Pasta: `04. 🧩 Recursos/Notas/4. Permanentes/`
- Título como afirmação ou pergunta — nunca substantivo solto
- Linkar para âncoras, para a nota de referência, e para outras permanentes relacionadas

---

## BLOCO 2 — Sessão socrática

Este bloco começa depois que tudo foi salvo no Obsidian. O objetivo é aprofundar o
entendimento do argumento — não forçar correlação com vida pessoal ou trabalho.

Milena pode estar lendo qualquer coisa: psicologia, história, política, mitologia, arte.
A sessão serve ao tema, não ao negócio dela.

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
Conectar com outros autores, correntes ou ideias que o vault já tem ou que Milena conhece.
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
- Nomear o padrão que Milena descreveu mas não nomeou — derivar e testar
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
3. Criar a nota permanente em `04. 🧩 Recursos/Notas/4. Permanentes/`
4. Linkar para âncoras relevantes e para outras notas da sessão
5. Continuar a conversa — não pausar para cada nota

### Quando encerrar

Encerrar quando:
- As três camadas foram exploradas
- As últimas 2-3 respostas não geraram novas notas
- Milena sinaliza que quer parar

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

---

## Referência rápida — estrutura do vault

```
04. 🧩 Recursos/Notas/
  └── 2. Referência/Artigos/     → notas de referência de artigos
  └── 3. Literatura/             → sínteses de livros e cursos
  └── 4. Permanentes/            → insights atômicos próprios
  └── 7. Autores/                → uma nota por autor mencionado
01. ⚓ Âncoras/                   → MOCs temáticos
```

Seguir a skill `obsidian-zettelkasten` para todas as operações de escrita no vault —
frontmatter obrigatório, wikilinks inline em toda entidade nomeada, âncora em toda nota
permanente.
