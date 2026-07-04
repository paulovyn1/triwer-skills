# Ecossistema de Skills Triwer (Notion "Segundo Cérebro") — Plano de Implementação

> **Para quem for executar isso (humano ou agente):** este documento é um plano por
> blocos. Cada bloco é ~independente e deve ser executado como uma sessão de trabalho
> própria (idealmente com o skill `writing-plans` gerando um sub-plano detalhado
> daquele bloco específico antes de codar, e `requesting-code-review`/teste manual
> ao final). Não pule o BLOCO 0 — ele contém decisões de arquitetura que todos os
> outros blocos assumem como verdadeiras. Onde uma tarefa depende de material que só
> o usuário (Paulo) tem, ela está marcada **BLOQUEADOR — aguardando input do usuário**
> e não deve ser adivinhada.

**Objetivo:** Transformar o Notion de cada aluno da Triwer em um "segundo cérebro"
progressivamente configurado por uma família de skills do Claude, acionadas na ordem
em que o aluno avança nos módulos do curso. Cada skill lê/grava num Notion pessoal do
aluno (cópia de um template Triwer), evitando retrabalho e generalismo no conteúdo
gerado. O conjunto deve ser instalável (a) via um único comando para Claude Code/
Desktop, que baixa e instala todas as skills de uma vez, e (b) como pacotes
individuais para upload manual na tela de Skills do claude.ai, para alunos que não
usam Claude Code.

**Arquitetura:** Cada skill é uma pasta independente em `~/.claude/skills/<nome>/`
com um `SKILL.md` (orquestrador), arquivos de referência lidos sob demanda, e um
`memoria.md` local criado no primeiro uso (nunca sobrescrito em updates). O Notion do
aluno é a fonte de verdade entre sessões; os arquivos locais são cache/atalho. Uma
nova skill, `onboarding-triwer`, roda primeiro e resolve/grava as URLs das páginas e
databases essenciais do Notion, para que as demais skills não precisem "procurar" a
cada uso (economia de tokens e de chamadas ao Notion).

**Convenções herdadas do que já existe no repositório** (`carrossel-triwer/SKILL.md`,
`cta-triwer/SKILL.md`): frontmatter YAML com `name`/`description`/`compatibility`/
`metadata`; seção "REGRA GERAL DE LEITURA DE ARQUIVOS"; "BOOT — EXECUTAR SEMPRE AO
INICIAR"; "ONBOARDING — APENAS NO PRIMEIRO USO"; etapas numeradas; "REGRAS QUE NÃO
MUDAM" em tabela; seção "INSTALAÇÃO" com estrutura de pastas + comandos mac/Windows;
`VERSION` na raiz da skill; instaladores em `scripts/instalar-<skill>-mac.sh` e
`scripts/instalar-<skill>-windows.ps1` que baixam de
`https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/...` e nunca
sobrescrevem `memoria.md`. Todo bloco novo abaixo deve seguir essas convenções, não
reinventar.

---

## Mapa de skills — estado atual x alvo

| Skill | Pasta (alvo) | Status hoje | Papel no ecossistema |
|---|---|---|---|
| Onboarding | `onboarding-triwer/` | **não existe — criar** | Duplica/liga o Notion modelo, personaliza a home, resolve e grava URLs essenciais, encaminha para Forge |
| Estilo (Forge) | `estilo-forge/` | Existe, funcional | Fábrica que gera `estilo-[nome]/SKILL.md` sob medida (voz do aluno) |
| Avaliação de Produto/Serviço (Dr. House) | `dr-house-triwer/` | **✅ concluído (03/07/2026)** | Diagnostica a cadeia causal do produto/serviço (público→preço), gera HTML de diagnóstico que alimenta o `sexy-triwer` |
| Zettelkasten do Aluno | `notion-zettelkasten-si/` | **✅ concluído (03/07/2026)** — não estava no plano original | Transforma qualquer conversa com Claude em notas conectadas no Acervo Notion do aluno |
| Oráculo | `oraculo-triwer/` | **não existe — migrar de agente GPT** | Mapeia e cadastra o público em profundidade (`Meu Público`) |
| Sexy | `sexy-triwer/` | **não existe — migrar de agente GPT** | Constrói a promessa do produto/serviço (`Produtos > subpágina`) |
| Prisma | `prisma-triwer/` | **✅ concluído (02/07/2026)** | Escava e formula o Viés Bruto Central (posicionamento) do aluno via conversa socrática, grava em "Quem sou eu". **Não mexe em "Meu Público"** — isso é integralmente da `oraculo-triwer` (ver nota no Bloco 3) |
| Extração de Histórias | `historias-triwer/` | **✅ concluído (02/07/2026)** | Detecta relatos em qualquer conversa e cadastra em "Histórias Inevitáveis" — mesma estrutura de campos que `carrossel-triwer` já consome |
| MDI | `mdi-triwer/` | **✅ concluído (02/07/2026)** | Cruza Meu Público + Histórias + Oportunidade Sexy + Viés para preencher a database "MDI — BASE GERAL" e gerar briefs de conteúdo |
| Carrossel | `carrossel-triwer/` | **✅ revisado (02/07/2026), v4.0** | Gera carrosséis DOPA — onboarding próprio removido, delega para onboarding/prisma/oráculo-triwer |
| CTA | `cta-triwer/` | **✅ revisado (02/07/2026), v4.0** | Decide Manychat/isca e escreve slides 09-10 — onboarding próprio removido, lê `iscas_db_url`/`produtos_db_url` da memória |
| Obsidian Zettelkasten | `obsidian-zettelkasten/` | Existe, mas é sobre **Obsidian**, não Notion | Fora do escopo deste ecossistema — ver Bloco 0.3 |

Ordem de acionamento pretendida pelo aluno, conforme módulos do curso:
`onboarding-triwer → estilo-forge → dr-house-triwer (avaliação) → oraculo-triwer →
sexy-triwer → prisma-triwer → historias-triwer (contínuo, sob demanda) →
mdi-triwer → carrossel-triwer → cta-triwer`.

Ordem de **construção** recomendada (dependência técnica, não pedagógica) é a usada
nos blocos abaixo: primeiro a fundação (onboarding + decisões), depois as skills que
mais desbloqueiam as outras.

---

## BLOCO 0 — Decisões de arquitetura e pré-requisitos (bloqueador para todo o resto)

Nenhum outro bloco deve começar a implementação antes deste estar resolvido — as
decisões aqui definem convenções que todas as skills novas vão seguir.

### 0.1 — Decidir o mecanismo de memória persistente

**✅ CONFIRMADO PELO USUÁRIO (02/07/2026):** Notion como fonte de verdade +
`memoria.md` local como cache, sem depender de `CLAUDE.md`. O texto abaixo é a
justificativa já validada — segue como documentação de apoio.

**Problema:** o aluno propôs salvar as URLs essenciais do Notion no `CLAUDE.md` do
projeto. Isso não funciona de forma uniforme: `CLAUDE.md` é um conceito de **Claude
Code / Claude Desktop** (arquivo de projeto/usuário lido automaticamente). No
**claude.ai** (skills feitas por upload, para quem "for usar o Claude normal"), não
existe `CLAUDE.md` — só os arquivos empacotados dentro da própria skill. Se a memória
depender de `CLAUDE.md`, os alunos que usam claude.ai ficam sem memória persistente.

**Decisão recomendada:** manter e generalizar o padrão que `carrossel-triwer` e
`cta-triwer` já usam — `memoria.md` dentro da própria pasta da skill
(`~/.claude/skills/<skill>/memoria.md`), criado no onboarding daquela skill, nunca
sobrescrito por updates. Regra adicional a partir de agora:

- **O Notion é a fonte de verdade.** Toda skill deve ser capaz de funcionar (mais
  lenta, com mais buscas) mesmo se `memoria.md` não existir ou não persistir —
  reconstruindo o essencial via `notion_search`/`notion_fetch`. Isso já é o
  comportamento do `cta-triwer` (Passo 3 do BOOT) e deve virar regra padrão em todas
  as skills novas.
- **`memoria.md` é cache, não dependência.** Serve só para economizar chamadas —
  guarda URLs/IDs já resolvidos e preferências do aluno.
- **Não usar `CLAUDE.md` do projeto para nada que precise funcionar em claude.ai.**
  Se, no futuro, alguém quiser um atalho *só* para uso via Claude Code, isso pode ser
  um adicional opcional — nunca o único caminho.
- **Evitar arquivo central compartilhado entre skills** (ex.: uma pasta
  `_triwer-dados/notion-config.md` lida por todas). Motivo: não há garantia de que o
  ambiente de skills do claude.ai permita leitura de arquivos fora da própria pasta
  da skill (não verificado — ver tarefa 0.2). Cada skill grava sua própria cópia das
  URLs relevantes no seu próprio `memoria.md`. Duplicação de 5-6 linhas de URL é
  aceitável; incerteza de leitura cross-skill não é.

**Ação:** `onboarding-triwer`, ao final do seu fluxo, deve **gravar as URLs
essenciais no `memoria.md` de cada skill Triwer já instalada na máquina** (verificar
quais pastas existem em `~/.claude/skills/*-triwer/` e escrever/atualizar a seção
"Configuração do Notion" de cada uma). Skills instaladas depois do onboarding
resolvem sozinhas via Notion no próprio primeiro boot (fallback já é o padrão).

- [ ] Confirmar esta decisão com o usuário antes do Bloco 1 (pode ser confirmação
  rápida em chat, não precisa de novo documento).

### 0.2 — Verificar persistência de arquivos em claude.ai (skills por upload)

**✅ RESPONDIDO PELO USUÁRIO (02/07/2026):** para quem usa claude.ai com o Notion
conectado, a skill busca as informações direto do Notion, do mesmo jeito que faz em
Claude Code/Desktop. Ou seja, a arquitetura da decisão 0.1 já cobre esse caso —
`memoria.md` é só um acelerador quando existe; quando não persiste (claude.ai), a
skill simplesmente sempre resolve via Notion (mais chamadas, mesmo resultado).
**Isso remove o bloqueio** — nenhuma skill deve ter um caminho que só funciona com
`memoria.md` presente; toda leitura de URL/estado tem que ter fallback de busca no
Notion. Isso já é regra de design a partir daqui, não precisa mais de teste manual
antes de continuar.

- [ ] (Opcional, não bloqueador) Em algum momento, testar na prática se `memoria.md`
  realmente persiste em claude.ai — só para saber se vale a pena manter a lógica de
  cache lá ou se pode ser simplificado (não afeta o design, é otimização futura).

### 0.3 — Higienizar repositórios git aninhados

**✅ CONFIRMADO PELO USUÁRIO (02/07/2026):** `obsidian-zettelkasten` fica em
repositório **separado** — não deve subir junto com o repositório atual de skills.
Boa notícia: já verificado que o `.gitignore` da raiz **já ignora essa pasta**
corretamente (`obsidian-zettelkasten/` está listado, com o comentário "Repositórios
independentes (têm GitHub próprio)"). Ou seja, nenhuma ação é necessária para
`obsidian-zettelkasten` — já está isolado como deveria. Nenhum trabalho deste plano
deve tocar nela.

**O que ainda precisa de ação é só `estilo-forge/`:** ela **deve sim** fazer parte
deste repositório principal (é parte do pipeline: onboarding aponta para ela), mas
hoje tem um `.git` interno próprio e **não está no `.gitignore`** — então
`git status` mostra `estilo-forge/` como `??` (não rastreado). Isso quebra os
instaladores que baixam via `raw.githubusercontent.com/.../main/...`, porque o
conteúdo dela nunca foi de fato commitado no histórico deste repositório.

- [x] Rodado `git log`/`git fetch` dentro de `estilo-forge/.git` (02/07/2026):
  único commit (`471cb37 — feat: primeira versão — estilo-forge v1.0.0`), já
  presente e idêntico no remoto `github.com/paulovyn1/estilo-forge` — nada a
  preservar, histórico já existe naquele repositório separado.
- [x] `estilo-forge/.git` removido — conteúdo agora são arquivos normais.
- [x] `git add estilo-forge` rodado na raiz — arquivos **staged**, aguardando
  confirmação do usuário para o commit (ver seção de commit pendente no rodapé
  da sessão).

### 0.4 — Acesso de leitura ao schema real do Notion modelo

**BLOQUEADOR — precisa de input do usuário.** Várias skills novas (Oráculo, Sexy,
Extração de Histórias, MDI) precisam saber **exatamente** quais campos/propriedades
existem nas databases do Notion modelo (`Meu Público`, `Produtos`, `Histórias
Inevitáveis`, `MDI`) para gravar corretamente. Hoje este projeto não tem conexão
MCP com Notion ativa nesta sessão, nem uma cópia do schema em arquivo.

- [ ] Usuário conectar o MCP do Notion nesta sessão de trabalho (ou nas sessões dos
  blocos 4/6/7 especificamente), **ou** exportar/colar a estrutura de campos de cada
  database relevante (nome da propriedade + tipo + opções de select, quando houver).
- [ ] Para cada database abaixo, produto final desta tarefa é uma lista de campos
  documentada (pode virar a seção "Schema" de referência de cada skill):
  - `Meu Público` (usada por Oráculo e, de forma leve, por Prisma)
  - `Produtos` + subpágina de produto individual (usada por Sexy)
  - `Histórias Inevitáveis` (usada por Extração de Histórias, já parcialmente
    referenciada em `carrossel-triwer/SKILL.md` linhas 320-368, mas sem lista de
    campos)
  - `Depoimentos` (usada por `cta-triwer`, `sexy-triwer` e `prisma-triwer` — URL
    já resolvida pelo `onboarding-triwer` desde 02/07/2026, mas o schema de campos
    ainda não foi levantado)
  - `MDI` (usada pela skill MDI — o aluno pediu explicitamente para "ler a página do
    template modelo" antes de desenhar essa skill)
  - `Quem sou eu` (usada por Prisma e já parcialmente coberta por
    `carrossel-triwer/referencias/orientacoes-quem-sou-eu.md`)

### 0.5 — Coletar materiais de origem pendentes (lista consolidada)

**BLOQUEADOR — precisa de input do usuário, um item por skill nova:**

- [ ] **Oráculo:** exportar as instruções/prompt do agente GPT atual (system
  prompt + qualquer arquivo de conhecimento anexado).
- [ ] **Sexy:** exportar as instruções/prompt do agente GPT atual (idem).
- [x] **Prisma:** ✅ recebido e integrado em 02/07/2026 (ver Bloco 3).
- [ ] **Avaliação de Produto/Serviço:** aguardar entrega da Milena (critérios de
  avaliação). Sem data definida — tratar como item de backlog, não como bloco ativo
  (ver Bloco 8).
- [x] **Link do Notion modelo para duplicação — ✅ CONFIRMADO (02/07/2026):**
  ```
  https://triwer.notion.site/Template-Perfil-do-Aluno-3588e7e25d248106b767e8eaaba3e47f?source=copy_link
  ```
  Esta é a URL a ser usada no passo 2 do `onboarding-triwer` (Bloco 1) e a que deve
  substituir a referência genérica `https://triwer.notion.site` no `README.md` e em
  `carrossel-triwer/SKILL.md` (linha 80, mensagem de fallback "Notion não
  conectado").

### 0.6 — Convenção de nomes das novas pastas de skill

Nomes provisórios usados neste plano (ajustar livremente, é só para não deixar
`TBD` nos caminhos de arquivo):

| Nome funcional (como o aluno vai chamar) | Pasta/slug técnico | Comando |
|---|---|---|
| Onboarding | `onboarding-triwer` | `/onboarding-triwer` |
| Oráculo | `oraculo-triwer` | `/oraculo-triwer` |
| Sexy | `sexy-triwer` | `/sexy-triwer` |
| Prisma | `prisma-triwer` | `/prisma-triwer` |
| Extração de Histórias | `historias-triwer` | `/historias-triwer` |
| MDI | `mdi-triwer` | `/mdi-triwer` |
| Avaliação de Produto/Serviço (Dr. House) | `dr-house-triwer` | `/dr-house-triwer` |
| Zettelkasten do Aluno | `notion-zettelkasten-si` | (comportamento contínuo, sem comando) |

**✅ CONFIRMADO PELO USUÁRIO (02/07/2026):** nomes aprovados sem alteração, incluindo
`sexy-triwer`. Usar esses slugs literalmente em todos os caminhos de arquivo dos
blocos seguintes.

### 0.7 — Convenção padrão: "Gate de Onboarding"

Toda skill do ecossistema (exceto a própria `onboarding-triwer`) deve, no seu passo
de BOOT, checar se o onboarding já foi feito **antes** de seguir para qualquer outra
lógica. Texto-padrão a ser reaproveitado literalmente em cada `SKILL.md` novo/
revisado:

```
### Passo 0 — Verificar onboarding

Tente ler `~/.claude/skills/onboarding-triwer/memoria.md`.

- **Se existir e tiver `onboarding_completo: true`:** prossiga normalmente.
- **Se não existir, ou existir sem essa confirmação:** exiba:

> Antes de usar esta skill, você precisa concluir a configuração inicial do seu
> Notion. Isso leva poucos minutos e só precisa ser feito uma vez.
>
> Rode `/onboarding-triwer` primeiro, depois volte aqui.

  Aguarde. Não prossiga com a lógica principal da skill sem o onboarding
  concluído — as demais etapas dependem de URLs do Notion que só o onboarding
  resolve e grava.
```

- [ ] Este bloco de texto entra literalmente (ajustando o nome da skill que o chama)
  em: `oraculo-triwer`, `sexy-triwer`, `prisma-triwer`, `historias-triwer`,
  `mdi-triwer`, `dr-house-triwer`, `notion-zettelkasten-si`, e nas versões revisadas de `carrossel-triwer` e
  `cta-triwer` (Bloco 2).

### 0.8 — Ciclo padrão de construção de skill (referenciado por todos os blocos)

Como skills são artefatos de prompt/markdown, não código com testes automatizados, o
ciclo de qualidade equivalente ao TDD aqui é:

1. **Levantar requisitos** — confirmar que os bloqueadores daquela skill (materiais
   de origem, schema Notion) foram resolvidos. Não escrever `SKILL.md` com campos
   adivinhados.
2. **Rascunhar o `SKILL.md`** seguindo a convenção herdada (frontmatter, REGRA GERAL
   DE LEITURA DE ARQUIVOS, BOOT com Gate de Onboarding, ONBOARDING se aplicável,
   ETAPAS, HANDOFF se a skill passa bastão para outra, REGRAS QUE NÃO MUDAM,
   INSTALAÇÃO).
3. **Testar manualmente** — rodar uma conversa simulando um aluno real (dados
   fictícios), validar: o Gate de Onboarding barra corretamente sem onboarding; o
   boot lê índice antes de conteúdo completo (economia de tokens); a gravação no
   Notion só acontece após confirmação explícita do aluno; o handoff (se houver)
   tem todos os campos que a próxima skill espera.
4. **Ajustar** com base no teste.
5. **Empacotar** — criar `VERSION` (iniciar em `1.0.0`), adicionar aos scripts de
   instalação individual e ao instalador em lote (Bloco 9), atualizar `README.md` da
   raiz.

Cada bloco abaixo assume este ciclo e só detalha o que é **específico** daquela
skill (para não repetir os 5 passos genéricos oito vezes).

### 0.9 — Texto-padrão: como conectar o Notion (pesquisado em 02/07/2026)

**Origem:** documentação oficial da Notion
([developers.notion.com/guides/mcp/get-started-with-mcp](https://developers.notion.com/guides/mcp/get-started-with-mcp))
e busca sobre o fluxo atual do claude.ai. Isso **substitui** o texto genérico e
desatualizado que hoje existe em `carrossel-triwer/SKILL.md` (linhas 70-82, bloco
"⚠️ Notion não conectado") e o equivalente implícito em `cta-triwer/SKILL.md`.

**Limitação importante para todo o ecossistema:** o Notion MCP usa **OAuth por
usuário** e não suporta autenticação por token fixo (bearer token). Isso significa
que **nenhuma skill consegue conectar o Notion automaticamente** — cada aluno
precisa, ele mesmo, passar pelo fluxo de autorização uma vez por conta. Toda skill
só pode **detectar e instruir**, nunca pular essa etapa manual do aluno.

**Bloco de texto a reutilizar literalmente** (trocar `[CLIENTE]` pelo contexto —
Claude Desktop, claude.ai ou Claude Code — quando souber qual o aluno está usando; se
não souber, mostrar as três opções):

```
⚠️ Notion não conectado

Esta skill precisa do conector do Notion ativo para ler e gravar no seu Notion
pessoal.

**Se você usa o Claude Desktop (app instalado):**
1. Abra Configurações → Connectors (Conectores)
2. Clique em "Add Connector" (Adicionar conector)
3. Cole esta URL: https://mcp.notion.com/mcp
4. Complete a autorização (OAuth) selecionando o workspace com a sua cópia do
   template Triwer
Disponível nos planos Pro, Max, Team e Enterprise.

**Se você usa o claude.ai (navegador):**
1. Clique no seu ícone de perfil (canto superior direito) → Settings
2. No menu à esquerda, clique em Connectors
3. Clique em "Browse connectors" e procure "Notion" na categoria Web
4. Clique no "+" ao lado do Notion
5. Autorize via OAuth e selecione o workspace/página do seu template Triwer

**Se você usa o Claude Code (terminal):**
1. Rode: claude mcp add --transport http notion https://mcp.notion.com/mcp
2. Rode: /mcp
3. Siga o fluxo de autorização (OAuth) no navegador que abrir

Depois de conectar, volte e me avise para eu continuar.
```

**Nota de troubleshooting a incluir também** (aparece quando o Notion está
conectado mas uma busca específica falha com "object not found" — geralmente porque
o workspace conectado não é o mesmo da cópia do template, ou a página não foi
compartilhada com o conector): orientar o aluno a abrir a página no Notion, clicar
no menu "•••" → "Add connections" (Adicionar conexões) → selecionar o conector do
Claude.

- [x] Substituído o bloco "⚠️ Notion não conectado" em `carrossel-triwer/SKILL.md`
  pelo texto-padrão (02/07/2026), incluindo a URL real do template.
- [x] Adicionado o mesmo texto-padrão em `cta-triwer/SKILL.md` (02/07/2026), antes
  do fallback para arquivo local. De quebra, corrigido um bug pré-existente: a
  skill referenciava `referencias/iscas-exemplo.md` em duas linhas, mas o arquivo
  real no repositório é `referencias/iscas-local.md` — corrigido nas duas
  ocorrências.
- [ ] Usar este texto-padrão como Passo 1 do BOOT de `onboarding-triwer` (Bloco 1) —
  é o primeiro obstáculo possível de todo o pipeline, faz sentido resolver ali antes
  de mais nada.
- [ ] Reutilizar em todas as skills novas (Blocos 3-8) no lugar de escrever uma
  mensagem de fallback diferente em cada uma.

---

## BLOCO 1 — `onboarding-triwer` (nova — fundação de tudo)

Depende de: Bloco 0 completo (em especial 0.4 parcialmente — schema de "Dados
Essenciais" — e 0.5 último item, URL do template).

**Status (02/07/2026):** `SKILL.md`, `VERSION` e os instaladores
(`scripts/instalar-onboarding-mac.sh`/`.ps1`) já criados, cobrindo todo o fluxo
funcional descrito abaixo. **Ainda falta:** o passo "Definição de pronto" — testar
manualmente o fluxo do início ao fim com dados fictícios e um Notion real
conectado — e a propagação real (E7) só pode ser validada quando houver pelo menos
uma outra skill `*-triwer` instalada ao lado para checar a escrita cruzada de
`memoria.md`.

**Arquivos:**
- Criar: `onboarding-triwer/SKILL.md`
- Criar (no primeiro uso do aluno, não neste momento): `onboarding-triwer/memoria.md`
- Criar: `onboarding-triwer/VERSION` (conteúdo: `1.0.0`)
- Criar: `scripts/instalar-onboarding-mac.sh` e `scripts/instalar-onboarding-windows.ps1`
  (copiar o padrão de `scripts/instalar-carrossel-*`, trocando os paths)

**Fluxo funcional obrigatório** (etapas numeradas dentro do `SKILL.md`, na ordem):

1. **Apresentação** — explica o que vai acontecer e quanto tempo leva (~5-10 min),
   nos moldes do `O1` de `carrossel-triwer`.
2. **Verificar conexão com o Notion** — tentar uma busca simples. Se a ferramenta
   `notion` não estiver disponível, exibir o texto-padrão definido em **0.9** (com as
   três opções — Claude Desktop, claude.ai, Claude Code) e aguardar o aluno conectar
   antes de seguir. Como o Notion MCP exige OAuth por usuário (0.9), a skill nunca
   deve tentar contornar essa etapa.
3. **Verificar se o aluno já tem o Notion modelo duplicado.**
   - Perguntar se já duplicou. Se sim, pedir a URL da página principal.
   - Se não: **primeiro tentar duplicar via MCP do Notion**, se a ferramenta
     disponível suportar duplicação de página/template programaticamente (checar na
     prática quais tools o conector Notion expõe nesta sessão — anotar o resultado
     no `SKILL.md` como comentário de implementação). Se **não** for possível via
     API, cair no fallback manual: enviar o link do template confirmado em 0.5
     (`https://triwer.notion.site/Template-Perfil-do-Aluno-3588e7e25d248106b767e8eaaba3e47f?source=copy_link`)
     e orientar o aluno a clicar em "Duplicar" para o workspace dele, depois colar a
     URL da cópia.
   - Validar a URL (tentar acessar/buscar). Se inválida, pedir novamente. Se der
     "object not found" mesmo com Notion conectado, usar a nota de troubleshooting de
     0.9 (página não compartilhada com o conector).
4. **Resolver a estrutura interna** — reaproveitar a lógica já validada em
   `carrossel-triwer/SKILL.md` (seção `O2`, linhas 126-142): localizar "Dados
   Essenciais" dentro da página principal, e a partir dela resolver os links reais
   de "Quem sou eu", "Meu Público", além de (novo, não coberto ainda em nenhuma skill
   existente) "Histórias Inevitáveis", "Produtos", "MDI" e "Central de Conteúdo".
   Guardar todas essas URLs.
5. **Personalizar a página inicial:**
   - Perguntar o nome do aluno → atualizar o título/campo de nome da home.
   - Orientar a trocar a foto de capa/perfil pela foto do aluno (Notion não permite
     upload de imagem arbitrária via API na maioria dos casos — confirmar limite
     técnico real do conector durante a implementação; se não for possível via API,
     apenas orientar o aluno a trocar manualmente e seguir).
   - Perguntar o @ do Instagram → atualizar o campo/link correspondente na home.
   - Perguntar se já tem uma pasta de Google Drive com fotos para produção de
     conteúdo:
     - Se sim: pedir o link e substituir no campo correspondente do Notion.
     - Se não: orientar a criar uma pasta agora no Drive (passo a passo curto) e
       explicar que pode ser alimentada aos poucos — não travar o onboarding
       esperando ela ser preenchida, só o link precisa existir.
6. **Gravar memória** — criar `onboarding-triwer/memoria.md` com, no mínimo:
   ```markdown
   # Memória — Onboarding Triwer
   _Última atualização: [data]_

   onboarding_completo: true

   ## Aluno
   - Nome: [nome]
   - Instagram: [@arroba]
   - Drive de fotos: [URL]

   ## Notion — URLs essenciais
   - Página principal: [URL]
   - Dados Essenciais: [URL]
   - Quem sou eu: [URL]
   - Meu Público (DB): [URL]
   - Histórias Inevitáveis (DB): [URL]
   - Produtos (DB): [URL]
   - MDI (DB ou página): [URL]
   - Central de Conteúdo: [URL]
   ```
   Em seguida, **replicar essas mesmas URLs no `memoria.md` de toda skill
   `*-triwer` já instalada** em `~/.claude/skills/` (conforme decisão 0.1) —
   criando a seção "Configuração do Notion" daquele arquivo se ainda não existir, ou
   atualizando se existir.
7. **Encaminhar para o próximo passo** — orientar o aluno a rodar `/estilo-forge`
   para criar a skill de tom de voz personalizada, explicando em 1-2 frases por que
   isso importa antes de gerar qualquer conteúdo.

**Regras que não mudam (tabela a incluir no `SKILL.md`):**
- Nunca gravar nada no Notion sem antes mostrar ao aluno o que vai ser escrito e
  esperar confirmação.
- Nunca inventar uma URL — se não conseguir resolver algum link automaticamente,
  perguntar diretamente ao aluno.
- `memoria.md` só é criado/marcado como `onboarding_completo: true` no fim do fluxo
  completo, não em passos intermediários (evita meia-configuração ser lida como
  "pronta" por outra skill).

**Definição de pronto:** rodar o onboarding do início ao fim com dados fictícios,
confirmar que `memoria.md` da própria skill e de pelo menos uma outra skill instalada
(`carrossel-triwer`, por exemplo) recebem as URLs corretas.

---

## BLOCO 2 — Revisar `carrossel-triwer` e `cta-triwer` (remover onboarding duplicado)

Depende de: Bloco 1 completo (o Gate de Onboarding só faz sentido depois que
`onboarding-triwer` existe).

**✅ CONCLUÍDO (02/07/2026).** Revisão
cuidadosa feita a pedido do usuário. Além do que este bloco já previa, achado
um bug real pré-existente: o `memoria.md` (O6) da versão antiga já listava
"Histórias Inevitáveis (DB)" e "Depoimentos (DB)" como campos esperados, mas o
onboarding antigo (O2) **nunca resolvia essas duas URLs** — só resolvia Dados
Essenciais, Quem sou eu e Meu Público. Ou seja, a skill prometia campos que
nunca eram preenchidos. Resolvido estruturalmente pela delegação ao
`onboarding-triwer`, que agora resolve as 9 URLs essenciais de uma vez.

Também executado (não previsto neste bloco originalmente, mas consequência
direta): os arquivos `referencias/orientacoes-quem-sou-eu.md` e
`referencias/orientacoes-publico.md` foram **removidos** de
`carrossel-triwer` (o primeiro estava obsoleto — a `prisma-triwer` real usa
"Viés Bruto Central", estrutura totalmente diferente; o segundo já tinha sido
migrado para `oraculo-triwer` no Bloco 4). Instaladores
(`scripts/instalar-carrossel-mac.sh`/`.ps1`) atualizados para não baixar mais
esses dois arquivos. `README.md` recebeu correção pontual (não é o Bloco 9.3
completo) para não descrever uma estrutura de arquivos que não existe mais.

**✅ `cta-triwer` também concluído (02/07/2026).** Achados adicionais nesta
skill:
- **`iscas_db_url` nunca era resolvida pelo onboarding novo** — ela é
  específica de `cta-triwer` (database "Iscas gerais" dentro de "Central de
  ativos") e não tinha sido mapeada nos Blocos 1/7 anteriores. Adicionada ao
  `onboarding-triwer` agora.
- O onboarding antigo (O2) de `cta-triwer` **re-buscava a database "Produtos"
  via `notion_search`** mesmo essa URL já sendo resolvida pelo
  `onboarding-triwer` — mesmo padrão de duplicação de trabalho já corrigido em
  `carrossel-triwer`.
- **Bug de contrato de handoff:** `cta-triwer` descrevia o campo `modo` do
  handoff como se contivesse "o nome do aluno", mas no handoff real de
  `carrossel-triwer` `modo` é a string fixa `"aluno"` — o nome está em
  `nome_usuario`, campo separado. Corrigido a descrição do PASSO 0.

**Ainda pendente:** teste manual de ponta a ponta do pipeline completo
(onboarding → prisma/oráculo → carrossel → cta) com Notion real conectado.

**Arquivos:**
- Modificar: `carrossel-triwer/SKILL.md` (seções `BOOT`, linhas 52-95, e todo o
  bloco `ONBOARDING`, linhas 97-313)
- Modificar: `cta-triwer/SKILL.md` (seções `BOOT`, linhas 32-61, e todo o bloco
  `ONBOARDING`, linhas 63-114)
- Atualizar: `README.md` (raiz) — remover a frase "Na primeira vez que cada skill for
  usada, o onboarding dela iniciará automaticamente" e substituir pela orientação de
  rodar `/onboarding-triwer` primeiro.

**O que sai de cada skill (já é responsabilidade do onboarding novo):**
- `carrossel-triwer`: resolução de `dados_essenciais_url`, `quem_sou_eu_url`,
  `meu_publico_db_url` (etapas `O2`) — a skill passa a **ler essas URLs prontas** do
  seu próprio `memoria.md` em vez de resolvê-las.
- `carrossel-triwer`: preenchimento de "Quem sou eu" do zero (etapa `O3` completa) —
  isso vira responsabilidade da skill Prisma (Bloco 3). `carrossel-triwer` só
  **verifica se está preenchido**; se não estiver, orienta a rodar `/prisma-triwer`
  em vez de conduzir o preenchimento ela mesma.
- `carrossel-triwer`: preenchimento de perfis de público do zero (etapa `O4`
  completa) — vira responsabilidade da skill Oráculo (Bloco 4). Mesma lógica: só
  verifica e, se vazio, orienta `/oraculo-triwer`.
- `cta-triwer`: resolução de `Iscas gerais` e `Produtos` (etapas `O1`/`O2`) — passa a
  ler do `memoria.md` já preenchido pelo onboarding.

**O que permanece em cada skill (é específico dela, não do onboarding geral):**
- `carrossel-triwer` etapa `O5` (verificar skill de estilo/Forge) — mantém, mas passa
  a ser um `Passo` do BOOT em vez de bloco de "ONBOARDING", já que a essa altura o
  Gate de Onboarding geral já garantiu o resto.
- `cta-triwer` — toda a lógica de iscas (`padroes-de-iscas.md`, detecção de isca
  nova) não muda.

**Novo `BOOT` de `carrossel-triwer` (substituir integralmente as linhas 52-95 e
remover o bloco `ONBOARDING` das linhas 97-313, preservando apenas a lógica de
verificação de "Quem sou eu" / público vazios e o encaminhamento para Prisma/
Oráculo):**

```
## BOOT — EXECUTAR SEMPRE AO INICIAR

### Passo 0 — Verificar onboarding
[colar o texto-padrão da decisão 0.7]

### Passo 1 — Carregar memória
Leia `~/.claude/skills/carrossel-triwer/memoria.md` (já populado pelo onboarding
com as URLs do Notion). Carregue em memória de trabalho.

### Passo 2 — Verificar conexão Notion
[mantém igual ao atual, linhas 63-83]

### Passo 3 — Verificar "Quem sou eu" e "Meu Público"
Acesse rapidamente (via índice/summary, não a página inteira) `quem_sou_eu_url` e
`meu_publico_db_url` da memória.
- Se "Quem sou eu" estiver vazio: oriente a rodar `/prisma-triwer` antes de
  continuar (não gere conteúdo sem isso — a voz fica genérica).
- Se "Meu Público" estiver vazio: oriente a rodar `/oraculo-triwer` antes de
  continuar.
- Se ambos preenchidos: siga para o Passo 4.

### Passo 4 — Carregar índices locais
[mantém igual ao atual, linhas 84-93]
```

**Definição de pronto:** rodar `carrossel-triwer` sem `onboarding-triwer/memoria.md`
existente → deve barrar e orientar. Rodar com onboarding feito mas "Quem sou eu"
vazio → deve orientar Prisma e não seguir. Rodar com tudo preenchido → deve ir direto
para a Etapa 0 de geração, sem nenhuma pergunta de configuração.

- [ ] Repetir a mesma verificação/edição equivalente para `cta-triwer`.
- [ ] Depois de editado, revalidar manualmente os dois pipelines completos
  (`carrossel-triwer` → `cta-triwer`) com o handoff JSON — confirmar que nada que o
  handoff espera dependia de um campo que só existia no onboarding removido.

---

## BLOCO 3 — `prisma-triwer` (skill existente — revisar e integrar ao Notion)

Depende de: Bloco 0.5 (arquivos da skill Prisma atual) e Bloco 0.4 (schema de
"Quem sou eu").

**✅ CONCLUÍDO (02/07/2026).** Usuário trouxe a versão final da skill, feita
pela Milena Camila — o "Agente de Escavação do Viés Magnético", entregue como
pasta `prisma-si/` (nome original, ligado à marca "Sim Inevitável"). Usuário
optou por renomear para `prisma-triwer/` para ficar no padrão do restante do
ecossistema (a metodologia interna continua mencionando "Sim Inevitável" —
isso é conteúdo, não muda).

**Correção de escopo em relação ao que este plano assumia originalmente:**
a skill real da Milena **não faz** "preenchimento leve de Meu Público" — ela é
100% focada em escavar e gravar o "Viés Bruto Central" em "Quem sou eu". Como
a `oraculo-triwer` (Bloco 4) já cobre "Meu Público" de forma completa, essa
lacuna não existe de verdade — o texto deste plano foi corrigido no Mapa de
Skills para não prometer algo que a skill entregue não faz.

**3 bugs reais corrigidos no `SKILL.md` original antes de integrar:**
1. **Dependência de `CLAUDE.md`** para achar o link do Notion do aluno — viola
   diretamente a decisão 0.1 (Notion como fonte de verdade + `memoria.md`
   como cache, sem `CLAUDE.md`, porque claude.ai nem tem esse conceito).
   Trocado por leitura de `quem_sou_eu_url` do `memoria.md` próprio, populado
   pelo `onboarding-triwer`.
2. **URLs fixas (hardcoded)** para "Central de histórias" e "Central de
   depoimentos" — pareciam ser do workspace pessoal de testes, quebrariam
   para qualquer outro aluno. Trocadas por `historias_db_url` e
   `depoimentos_db_url` lidos da memória; se não resolvidos, a linha é
   omitida em vez de usar um link fixo.
3. **`depoimentos_db_url` nunca era resolvida por nenhuma skill** — nem
   `carrossel-triwer`, nem o `onboarding-triwer` que eu tinha construído no
   Bloco 1. Corrigido: `onboarding-triwer/SKILL.md` (Etapa E4) e seu
   `memoria.md` de exemplo agora também resolvem e gravam
   `depoimentos_db_url`, propagada como as demais URLs.

**Adições de padronização** (sem alterar a metodologia/conteúdo da Milena, que
foi preservada 100% verbatim): Gate de Onboarding (0.7), verificação de
conexão com o Notion (0.9) com fallback para entregar o documento só na
conversa se o Notion não estiver conectado, confirmação explícita antes de
gravar (a versão original salvava logo após "entregar na conversa", sem um
"posso salvar?" formal), `memoria.md` e seções "REGRA GERAL DE LEITURA DE
ARQUIVOS" / "REGRAS QUE NÃO MUDAM" / "INSTALAÇÃO" no padrão do ecossistema.

**Consequência para o Bloco 2 (ainda não executado):** o arquivo
`carrossel-triwer/referencias/orientacoes-quem-sou-eu.md` (5 seções: História
pessoal, O que faço hoje, Cases e resultados, Dificuldades passadas, Valores e
posição) **fica obsoleto** quando o Bloco 2 remover o onboarding O3 do
`carrossel-triwer` — a `prisma-triwer` real usa uma estrutura totalmente
diferente ("Viés Bruto Central", 6 seções). Quando o Bloco 2 for executado:
apagar esse arquivo de referência (não tenta reconciliar as duas
estruturas) e trocar o fallback de "Quem sou eu vazio" em `carrossel-triwer`
para simplesmente orientar `/prisma-triwer`, sem ler nenhum arquivo de
orientação próprio.

**Definição de pronto:** ainda falta o teste manual de ponta a ponta com
Notion real conectado — em especial validar que `replace_content` (ou
equivalente) funciona como esperado na página "Quem sou eu".

---

## BLOCO 4 — `oraculo-triwer` (nova — migrar de agente GPT)

Depende de: Bloco 0.5 (prompt do GPT Oráculo) e Bloco 0.4 (schema de "Meu Público").

**✅ CONCLUÍDO (02/07/2026).** Usuário enviou o prompt do agente GPT original.
O bloqueador 0.4 (schema de "Meu Público") foi resolvido sem precisar de MCP
do Notion nesta sessão: o projeto já tinha a estrutura real documentada em
`carrossel-triwer/referencias/orientacoes-publico.md` (tabela-índice + 5
seções fixas por perfil), usada em produção pelo `carrossel-triwer`. Esse
arquivo foi migrado (copiado, com nota de origem) para
`oraculo-triwer/referencias/orientacoes-publico.md` — quando o Bloco 2 for
executado, remover a cópia de `carrossel-triwer` para não haver duas fontes.

3 decisões de escopo foram levadas ao usuário antes de escrever a skill (o
agente original tinha 6 tópicos, 2 deles fora do escopo de "mapear público"
no ecossistema novo):
- Geração de ideias de conteúdo/carrossel (item 4 do agente original) →
  **removida do escopo do Oráculo**, é exclusividade da `mdi-triwer`.
- "Como encontraram o produto" (item 5) → **incorporada como 1 frase dentro
  da seção "Quem é"** de cada perfil, sem criar campo/seção nova (preserva
  compatibilidade com o que `carrossel-triwer` já lê).
- Ideias de novos produtos (item 6) → **removida do escopo** por completo.

`oraculo-triwer/SKILL.md`, `VERSION`, `referencias/orientacoes-publico.md` e
instaladores mac/Windows criados. Falta apenas o teste manual de ponta a
ponta com uma planilha real e Notion conectado.

~~**BLOQUEADOR — não iniciar sem o prompt/instruções do agente GPT atual.**~~

**Arquivos (quando o material chegar):**
- Criar: `oraculo-triwer/SKILL.md`
- Criar: `oraculo-triwer/referencias/` com os arquivos de conhecimento que o agente
  GPT usa hoje (se houver — transcrever/adaptar, não copiar formato específico do
  GPT Builder).
- Criar: `oraculo-triwer/VERSION` (`1.0.0`)
- Criar: `scripts/instalar-oraculo-mac.sh` e `scripts/instalar-oraculo-windows.ps1`

**Tarefas de análise (antes de escrever a versão final, conforme pedido explícito do
usuário — "primeiro tem que ser feita uma análise para ver se a gente precisa
alterar algo"):**
- [ ] Ler o prompt atual do GPT e listar: (a) o que já funciona bem e deve ser
  preservado literalmente, (b) o que é specific do ChatGPT (referências a "GPTs",
  "Custom Instructions", formato de mensagem) e precisa virar linguagem neutra de
  skill, (c) gaps — o prompt atual provavelmente não fala nada sobre Notion, Gate de
  Onboarding, nem sobre ler índice antes de página cheia; isso é 100% novo a
  adicionar.
- [ ] Apresentar essa análise (pode ser uma seção temporária no topo do rascunho do
  `SKILL.md`, removida depois) antes de finalizar a skill.

**Fluxo funcional obrigatório (após a análise, a estrutura final deve ter):**
1. Gate de Onboarding (0.7).
2. BOOT: ler `memoria.md` próprio (URLs), ler índice/resumo da database "Meu
   Público" (nomes de perfis já cadastrados, sem abrir páginas individuais).
3. Corpo migrado do agente GPT: entrevista/extração do perfil de público ideal
   (o método em si, preservado do agente original após a adaptação de linguagem).
4. Antes de gravar: apresentar ao aluno um resumo do perfil identificado e pedir
   confirmação — mesmo padrão de "nunca escrever no Notion sem confirmação" usado em
   todas as outras skills.
5. Gravar na database "Meu Público" (subpágina "Meu Público" dentro de "Dados
   Essenciais", conforme resolvido pelo onboarding) — respeitando os campos exatos
   levantados no Bloco 0.4, e sem apagar o que Prisma (Bloco 3) já tiver criado para
   aquele perfil (atualizar em vez de sobrescrever).
6. `memoria.md`: registrar quais perfis já foram aprofundados pelo Oráculo (para não
   repetir trabalho à toa se o aluno rodar de novo).

**Definição de pronto:** rodar com um caso fictício de principio ao fim, incluindo
tentar rodar duas vezes seguidas para o mesmo perfil e confirmar que a segunda vez
identifica que já existe e pergunta se é para atualizar, não duplicar.

---

## BLOCO 5 — `sexy-triwer` (nova — migrar de agente GPT)

Depende de: Bloco 0.5 (prompt do GPT Sexy) e Bloco 0.4 (schema de "Produtos" +
subpágina de produto).

**✅ CONCLUÍDO (02/07/2026).** Usuário enviou o prompt do agente GPT original.
Análise feita (gaps identificados: zero integração Notion, reinterrogava do
zero o que Oráculo/Prisma já mapeiam, sem Gate de Onboarding, sem checklist
formal de validação da proposta, headlines conceitualmente diferentes do
catálogo MH00X do `carrossel-triwer` — precisava de nota explícita para não
confundir os dois sistemas). `sexy-triwer/SKILL.md`, `VERSION` e instaladores
mac/Windows criados. Escreve como conteúdo de página na subpágina do produto
(não como propriedades de database — contorna o bloqueio 0.4, que só afeta
sincronização de propriedades estruturadas, refinamento futuro). Falta apenas
o teste manual de ponta a ponta com Notion real (não pode ser feito nesta
sessão sem conexão MCP ativa).

~~**BLOQUEADOR — não iniciar sem o prompt/instruções do agente GPT atual.**~~

Mesma estrutura de tarefas do Bloco 4 (análise antes de finalizar, gate de
onboarding, leitura de índice antes de página cheia, confirmação antes de gravar),
adaptada para o objetivo desta skill:

**Arquivos:**
- Criar: `sexy-triwer/SKILL.md`
- Criar: `sexy-triwer/referencias/` (material de apoio migrado do GPT, se houver)
- Criar: `sexy-triwer/VERSION` (`1.0.0`)
- Criar: `scripts/instalar-sexy-mac.sh` e `scripts/instalar-sexy-windows.ps1`

**Especificidades:**
- [ ] BOOT deve perguntar (ou ler do handoff, se vier de outra skill futuramente)
  **qual produto/serviço** está em pauta, já que "Produtos" é uma database com
  múltiplas entradas — não presumir que existe só um produto.
- [ ] Gravação final acontece na **subpágina daquele produto específico** dentro da
  database "Produtos" (conforme a URL resolvida pelo onboarding + a entrada
  escolhida nesta etapa), não na página raiz de "Produtos".
- [ ] Vale tanto para produto quanto para serviço — a skill não deve ter lógica
  condicional diferente para os dois, é o mesmo fluxo de construção de promessa.

**Definição de pronto:** rodar com um produto fictício e um serviço fictício,
confirmar que a promessa gerada é salva na subpágina correta em ambos os casos.

---

## BLOCO 6 — `historias-triwer` (nova — extração de histórias)

**✅ CONCLUÍDO (02/07/2026).** Schema da página individual não foi confirmado
via Notion (0.4 seguia bloqueador), mas foi inferido com segurança a partir
de como o próprio `carrossel-triwer` já consome uma história (Etapa 4, Bloco
3 — Virada — Ato 1/2/3: fundo do poço, decisão contraditória, resultado
inesperado; mais o campo `dados_brutos` do handoff JSON). A skill usa
exatamente essa estrutura (Conflito/Fundo do poço, Decisão contraditória,
Resultado inesperado, Dados brutos) para não criar um formato divergente do
que a skill consumidora espera. Único ponto sem confirmação real: as opções
fixas do campo "Tipo" (select/multi-select) — a skill tenta ler as opções já
existentes na database antes de perguntar ao aluno, em vez de inventar uma
lista.

Diferença de design em relação às outras skills: esta precisa funcionar como
**comportamento contínuo** (detecta histórias em qualquer conversa, não só
quando chamada por comando), no mesmo espírito do `obsidian-zettelkasten` já
existente no projeto (que é "comportamento padrão obrigatório" sempre que uma
ferramenta é usada). Não duplica/conflita com a detecção que já existe
embutida em `carrossel-triwer` (Etapa 1) — as duas usam a mesma estrutura de
campos; `carrossel-triwer` continua conduzindo quando a detecção acontece
dentro de uma sessão dele, e `historias-triwer` cobre o resto (e o uso
direto).

`historias-triwer/SKILL.md`, `VERSION` e instaladores mac/Windows criados.
`historias_db_url` já estava resolvida desde o Bloco 1, nenhum ajuste
necessário no `onboarding-triwer` desta vez.

**Refinamento pós-conclusão (02/07/2026):** o usuário notou que `carrossel-
triwer` (Etapa 1) mantinha uma cópia própria da lógica de cadastro de
histórias, agora redundante. Ajustado para delegação: `carrossel-triwer`
continua conduzindo a *detecção* na própria conversa (evita trocar de skill
no meio da criação do post), mas o *cadastro em si* passou a ler
`historias-triwer/SKILL.md` (seção "CADASTRAR A HISTÓRIA") em vez de manter
texto duplicado — DRY entre as duas skills. `carrossel-triwer` v4.0 → v4.1,
`historias-triwer` v1.0 → v1.1. `VERSION` de `carrossel-triwer` e `cta-triwer`
também alinhados ao metadata (estavam presos em `1.0.0` desde antes deste
plano — inconsistência pré-existente, corrigida de passagem).

---

## BLOCO 7 — `mdi-triwer` (nova — Máquina de Demanda Infinita)

**✅ CONCLUÍDO (02/07/2026), fora de ordem** (Bloco 6/`historias-triwer` ainda
não existe — `mdi-triwer` lê a database "Histórias Inevitáveis" diretamente
via Notion, não depende da skill `historias-triwer` em si, só dos dados; se a
database estiver vazia porque ninguém rodou a skill ainda, degrada
graciosamente para entrevista, mesmo padrão usado em `sexy-triwer` quando
"Meu Público" está vazio).

Usuário trouxe o prompt do agente GPT MDI original **e** o schema real da
database "MDI — BASE GERAL" (algo que nenhum outro bloco teve de graça —
normalmente é bloqueador 0.4). Achados da análise:

- O agente original **entrevistava do zero**, sem olhar nada do que já existe
  no Notion — inconsistente com o resto do ecossistema já construído. A nova
  versão carrega Meu Público (Oráculo), Histórias Inevitáveis, a Oportunidade
  Sexy (Sexy) e o Viés Bruto Central (Prisma) antes de perguntar qualquer
  coisa, usando a técnica investigativa original só para validar/aprofundar
  o que falta.
- **Descoberta de schema:** existe uma database "Conteúdos" (linkada pela MDI
  via relation) que nenhuma skill resolvia ainda. Adicionada a
  `onboarding-triwer` como `conteudos_db_url`.
- Renomeado `mdi_url` → `mdi_db_url` em todo o ecossistema (era genérico
  demais; agora sabemos que é uma database específica, "MDI — BASE GERAL",
  dentro da página "[MDI] Máquina de Demanda Infinita").
- A relation "PERFIL" da MDI provavelmente aponta para "Meu Público", mas
  isso não foi confirmado no schema — a skill verifica em tempo real na
  primeira gravação e avisa o aluno se divergir, em vez de assumir.
- Geração de conteúdo ao final (7 ideias, +5 se aprovado) mantida do agente
  original, mas deixada explicitamente como **briefs** (headline + formato +
  resumo) — não gera o carrossel/reels completo, isso continua exclusivo da
  `carrossel-triwer`. Mesma nota de "headlines diferentes do catálogo MH00X"
  usada em `sexy-triwer` foi replicada aqui.
- Relation "Conteúdos" da MDI fica vazia até existir conteúdo real — evita
  vínculo antecipado sem substância.

`mdi-triwer/SKILL.md`, `VERSION` e instaladores mac/Windows criados. Falta o
teste manual de ponta a ponta com Notion real, e a confirmação em produção do
schema da database "Conteúdos" (campos exatos ainda não vistos).


Depende de: Bloco 6 (histórias precisam existir para ter o que cruzar) e Bloco 4
(público precisa existir, mesma razão), além do Bloco 0.4 — **e especificamente
precisa da leitura da página/template do MDI no Notion**, que o próprio usuário
apontou como pré-requisito ("o ideal é que você leia também essa página do template
modelo para entender quais são os campos a serem preenchidos").

**BLOQUEADOR — não escrever esta skill sem antes ler o template real do MDI no
Notion** (via MCP nesta sessão, ou export do usuário). Adivinhar os campos aqui é
especialmente arriscado porque o próprio usuário chamou atenção para isso
explicitamente.

**Arquivos:**
- Criar: `mdi-triwer/SKILL.md`
- Criar: `mdi-triwer/VERSION` (`1.0.0`)
- Criar: `scripts/instalar-mdi-mac.sh` e `scripts/instalar-mdi-windows.ps1`

**Fluxo funcional obrigatório:**
1. Gate de Onboarding (0.7).
2. BOOT: ler índice de "Histórias Inevitáveis" (campos resumo) e índice de "Meu
   Público" (nomes + estágio) — nunca páginas completas no boot.
3. Cruzar histórias x perfis de público para sugerir tópicos de conteúdo — a lógica
   exata de "bons tópicos" deve ser definida a partir da leitura do template real do
   MDI (Bloco 0.4/bloqueador acima), não inventada aqui.
4. Apresentar as sugestões ao aluno antes de preencher qualquer campo — mesmo padrão
   de confirmação prévia das demais skills.
5. Preencher a aba/database "MDI" do Notion com os campos exatos do template.
6. Registrar em `memoria.md` quais tópicos já foram sugeridos/preenchidos, para não
   repetir na próxima execução.

**Definição de pronto:** rodar com histórias e públicos fictícios já cadastrados,
confirmar que a skill cruza os dois corretamente e preenche o MDI só após aprovação.

---

## BLOCO 8 — `dr-house-triwer` (avaliação de produto — entregue pela Milena)

**✅ CONCLUÍDO (03/07/2026).** A Milena entregou a skill pronta — nome real
`dr-house-triwer` (não `avaliacao-triwer`, nome provisório usado antes de
existir). Metodologia (14 critérios de diagnóstico, escavação em 8 blocos,
output em HTML com radar SVG) preservada 100% — é trabalho dela, não foi
reescrita. Só integração ao padrão do ecossistema:

- **Bug real corrigido:** `references/salvamento.md` usava `CLAUDE.md` para achar
  o Notion do aluno (mesmo bug já corrigido em `prisma-triwer`) e navegava ao
  vivo por "Acervo → Referências" buscando notas por título. Trocado por leitura
  direta de `quem_sou_eu_url`, `historias_db_url`, `meu_publico_db_url` e
  `produtos_db_url` da memória (já resolvidas pelo `onboarding-triwer`).
- Nome antigo `vies-triwer` → `prisma-triwer`; `notion-zettelkasten` →
  `notion-zettelkasten-si` (nome real da skill, ver Bloco 8.5).
- Adicionado BOOT (Gate de Onboarding + verificação de Notion — não bloqueante
  para a escavação em si, só para a Fase 4 de salvamento), `compatibility`,
  `metadata`, `memoria.md`, `VERSION`, seção INSTALAÇÃO, instaladores
  mac/Windows.
- **Integração nova:** o Dr. House gera um HTML de diagnóstico pensado para
  alimentar o `sexy-triwer` numa conversa seguinte — mas o `sexy-triwer` não
  sabia disso. Adicionada leitura desse HTML (se anexado) na Etapa 2 do
  `sexy-triwer`, como fonte de contexto adicional.

Falta apenas o teste manual de ponta a ponta (escavação → HTML → salvamento no
Notion → handoff pro Sexy) com um caso real.

---

## BLOCO 8.5 — `notion-zettelkasten-si` (nova — não estava no plano original)

**✅ CONCLUÍDO (03/07/2026).** Usuário adicionou esta skill diretamente no
projeto — é a adaptação, para o Notion de qualquer aluno, da lógica que já
existe em `obsidian-zettelkasten` (vault fixo da Milena). Aqui o "vault" é o
Acervo do Notion do aluno, que varia de cópia para cópia do template, então a
skill precisa localizar a própria estrutura antes de escrever.

**2 bugs reais corrigidos antes de integrar:**
1. **Pasta duplicada:** o projeto tinha
   `notion-zettelkasten-si/notion-zettelkasten-si/SKILL.md` — uma pasta dentro
   da outra, provavelmente de um zip extraído incorretamente. Achatada para
   `notion-zettelkasten-si/SKILL.md`.
2. **Cache de IDs gravado dentro do próprio `SKILL.md`** — todo instalador
   Triwer sobrescreve `SKILL.md` a cada atualização (só `memoria.md` é
   protegido). Isso apagaria o cache do aluno na primeira atualização da
   skill. Corrigido: cache agora vai para `memoria.md`.

**Outros ajustes:** nome antigo `vies-triwer` → `prisma-triwer` (3 ocorrências);
"Meu Público" e "Quem sou eu" agora lidas da memória do `onboarding-triwer` em
vez de redescobertas via busca a cada workspace (só as páginas específicas
desta skill — Caixa de Entrada, Referências, Literatura, Permanentes, Autores,
Âncoras, Anotações — continuam sendo descobertas por ela mesma, ninguém mais
usa essas); oferta de gravar instrução no `CLAUDE.md` do aluno marcada como
exclusiva de Claude Code/Desktop (claude.ai não tem esse arquivo — a skill
funciona sem isso, é só um bônus). Adicionado `compatibility`, `metadata`,
seção INSTALAÇÃO, `VERSION`, instaladores mac/Windows.

**Achado que retroalimentou o Bloco 1:** esta skill descreve com mais precisão
onde "Quem sou eu" e "Meu Público" vivem (dentro de "Acervo" → "Referências",
itens marcados `Tipo: 🔓 Essencial`) do que a descrição genérica que o
`onboarding-triwer` tinha ("dentro de Acervo"). Atualizada a wording da Etapa
E4 do `onboarding-triwer` para refletir isso.

Falta o teste manual de ponta a ponta com um Notion de aluno real.

---

## BLOCO 9 — Empacotamento e distribuição

**✅ CONCLUÍDO (03/07/2026).**

- **9.1:** em vez de refatorar a lógica de download de cada instalador
  individual numa função compartilhada (o que exigiria reescrever os 11 já
  existentes), `scripts/instalar-tudo-mac.sh`/`.ps1` **encadeia os
  instaladores individuais já prontos e testados** (baixa e executa cada um
  via `bash <(curl ...)` / `Invoke-Expression`) — mais simples, zero
  duplicação, e cada instalador individual continua funcionando sozinho sem
  mudança. Reporta no final quais skills falharam, se alguma falhar, sem
  interromper as demais.
- **Bug encontrado e corrigido de passagem:** o instalador da `estilo-forge`
  (`estilo-forge/scripts/instalar-*`) ainda apontava para o repositório
  antigo dela (`github.com/paulovyn1/estilo-forge`), de antes do Bloco 0.3
  trazer os arquivos para dentro do `triwer-skills`. Corrigido para o
  repositório principal.
- **9.2:** criado `scripts/empacotar-zips.ps1`/`.sh` (ferramenta do
  mantenedor, gera `.zip` de cada skill em `dist/`, que fica no
  `.gitignore`). **O formato exato aceito pela tela de Skills do claude.ai
  não foi validado na prática** — documentado como ressalva explícita no
  README, não assumido como certo.
- **9.3:** `README.md` reescrito do zero — lista as 11 skills, os 3 caminhos
  de instalação (lote / individual / manual claude.ai), estrutura instalada
  atualizada, ordem recomendada de uso, e uma seção nova "Para o mantenedor"
  apontando para este plano e o script de empacotamento.

### 9.1 — Instalador único para Claude Code/Desktop

**Arquivos:**
- Criar: `scripts/instalar-tudo-mac.sh`
- Criar: `scripts/instalar-tudo-windows.ps1`

**Conteúdo:** refatorar a lógica repetida dos instaladores individuais
(`scripts/instalar-carrossel-*`, `scripts/instalar-cta-*`, e os novos de cada bloco
acima) para uma função/loop compartilhado que recebe a lista de skills a instalar e
repete o mesmo processo (checar versão remota, comparar com instalada, baixar
arquivos, nunca sobrescrever `memoria.md`, salvar `VERSION`). Ao final, roda o
onboarding automaticamente ou orienta o aluno a digitar `/onboarding-triwer`.

Lista de skills a incluir no loop (nomes conforme Bloco 0.6, ajustar se mudarem):
`onboarding-triwer`, `estilo-forge` (já existe — só entra na lista, sem trabalho
extra), `oraculo-triwer`, `sexy-triwer`, `prisma-triwer`, `historias-triwer`,
`mdi-triwer`, `carrossel-triwer`, `cta-triwer`, `dr-house-triwer`, `notion-zettelkasten-si`.

**Comando final para o aluno** (documentar no `README.md`), no mesmo estilo dos já
existentes:
```powershell
irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-tudo-windows.ps1 | iex
```
```bash
curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-tudo-mac.sh | bash
```

- [ ] Manter os instaladores individuais existentes (não depreciar) — o README já
  documenta a filosofia de "instale só o que precisar"; o instalador em lote é uma
  opção adicional, não substitui os individuais.

### 9.2 — Pacotes individuais para upload manual (claude.ai)

**BLOQUEADOR PARCIAL — confirmar antes o formato aceito pela tela de Skills do
claude.ai** (zip da pasta da skill? Só o `SKILL.md`? Limite de tamanho/quantidade de
arquivos?). Não documentado neste repositório ainda.

- [ ] Verificar manualmente na interface do claude.ai o que a tela de "Skills"
  aceita como upload.
- [ ] Uma vez confirmado o formato, criar um passo de empacotamento (pode ser um
  script simples `scripts/empacotar-zips.sh`/`.ps1`, ou só instrução manual no
  README) que gera um `.zip` por skill a partir da pasta correspondente, para
  download direto do GitHub (ex.: página de Releases do repositório, com um `.zip`
  por skill anexado a cada release) ou de uma pasta `dist/` versionada.
- [ ] Atualizar `README.md` com uma seção "Instalação manual via claude.ai"
  equivalente à seção "Instalação manual" que já existe para cópia de pasta local
  (linhas 129-137 do README atual), mas apontando para o fluxo de upload de zip.

### 9.3 — Atualizar `README.md` da raiz

- [ ] Reescrever a seção "O que está incluído" listando todas as skills do
  ecossistema (não só carrossel e CTA).
  ["Instalação"] passa a ter três caminhos: individual (já existe), em lote (novo,
  9.1), manual via claude.ai (novo, 9.2).
- [ ] Atualizar "Estrutura instalada" com as novas pastas.
- [ ] Adicionar uma seção curta explicando a ordem recomendada de uso pelo aluno
  (a mesma sequência do "Mapa de skills" no topo deste plano), já que agora existem
  dependências entre skills (ex.: Prisma/Oráculo antes de Carrossel).

---

## Ordem de execução recomendada (resumo)

```
Bloco 0 (decisões + bloqueadores) — obrigatório primeiro, mesmo que parcial
   │
   ├─→ Bloco 1 (onboarding-triwer)
   │        │
   │        ├─→ Bloco 2 (revisar carrossel-triwer e cta-triwer) [✅ concluído 02/07]
   │        │
   │        ├─→ Bloco 3 (prisma-triwer)         [✅ concluído 02/07]
   │        ├─→ Bloco 4 (oraculo-triwer)         [✅ concluído 02/07]
   │        ├─→ Bloco 5 (sexy-triwer)            [✅ concluído 02/07]
   │        ├─→ Bloco 6 (historias-triwer) [✅ concluído 02/07]
   │        │        │
   │        │        └─→ Bloco 7 (mdi-triwer) [✅ concluído 02/07, fora de ordem]
   │        │
   │        └─→ Bloco 9 (empacotamento) — pode rodar incrementalmente
   │
   └─→ Bloco 8 (dr-house-triwer) [✅ concluído 03/07] + Bloco 8.5 (notion-zettelkasten-si) [✅ concluído 03/07]
```

Blocos 3, 4 e 5 podem ser trabalhados em qualquer ordem entre si (todos bloqueados
apenas pelo material de origem chegar) — não há dependência técnica entre eles.

---

## Perguntas em aberto para o usuário (consolidado de todos os blocos)

_Atualizado em 02/07/2026 — itens 1 a 4 e 7 já resolvidos, ver detalhe em cada
subseção do Bloco 0._

1. ~~Confirmar a decisão de arquitetura de memória (0.1)~~ — ✅ Notion como fonte de
   verdade + `memoria.md` local por skill como cache, sem depender de `CLAUDE.md`.
2. ~~`obsidian-zettelkasten` continua no mesmo repositório?~~ — ✅ Não, fica em
   repositório separado; já está corretamente no `.gitignore` deste projeto, nenhuma
   ação necessária.
3. ~~Nomes definitivos das novas pastas de skill (0.6)~~ — ✅ Aprovados como estavam,
   incluindo `sexy-triwer`.
4. ~~URL do template Notion modelo~~ — ✅
   `https://triwer.notion.site/Template-Perfil-do-Aluno-3588e7e25d248106b767e8eaaba3e47f?source=copy_link`
5. **Ainda pendente:** fornecer os materiais bloqueadores listados em 0.5 — prompt
   do GPT Oráculo, prompt do GPT Sexy, arquivos da skill Prisma existente. Usuário já
   confirmou que vai coletar; Blocos 3, 4 e 5 ficam parados até chegarem.
6. **Resolvido via pesquisa, não mais pergunta:** as instruções de conexão do Notion
   MCP para Claude Desktop, claude.ai e Claude Code foram levantadas e documentadas
   na nova seção **0.9**, com o texto-padrão pronto para uso em todas as skills.
   Ponto de atenção que **continua exigindo confirmação do usuário mais adiante**:
   o Notion MCP usa OAuth por usuário (sem token fixo), então nenhuma skill pode
   conectar automaticamente — isso é uma limitação do produto Notion, não algo que dá
   para contornar em código.
7. ~~Testar persistência de arquivos em claude.ai (0.2)~~ — ✅ Não bloqueia mais: o
   usuário confirmou que, com o Notion conectado em claude.ai, a skill busca a
   informação direto do Notion do mesmo jeito que em Claude Code/Desktop. Continua
   como item opcional de otimização futura, não como bloqueador.

**Novas perguntas que surgiram durante a pesquisa da 0.9 (não bloqueiam o Bloco 0,
mas valem confirmar antes do Bloco 9 — empacotamento):**

8. O plano do aluno precisa ser Pro/Max/Team/Enterprise para usar Connectors no
   Claude Desktop (achado da documentação oficial, seção 0.9). Isso já é premissa do
   curso (o README atual já lista "Plano pago do Claude" como requisito), mas vale
   confirmar se isso deve ficar mais explícito na comunicação do onboarding — alunos
   no plano Free não conseguem conectar o Notion de jeito nenhum.
9. Formato de upload aceito pela tela de Skills do claude.ai (Bloco 9.2) — ainda não
   verificado na prática, segue como bloqueador só daquele bloco específico.
