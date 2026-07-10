---
name: historias-triwer
description: >
  Detecta quando o aluno relata um acontecimento, resultado, situação vivida
  ou caso real — dele ou de um cliente/aluno dele — em QUALQUER conversa, não
  só quando a skill é chamada por comando. Verifica se essa história já está
  cadastrada na database "Histórias Inevitáveis" do Notion e, se não estiver,
  oferece cadastrar (nunca sem confirmação). Também pode ser acionada
  diretamente para cadastrar uma história de propósito ou consultar histórias
  já existentes sobre um tema. Estrutura cada história em conflito, decisão
  contraditória, resultado inesperado e dados brutos — o mesmo formato que a
  `carrossel-triwer` já espera ao ler uma história para o Bloco 3 (Virada).
  Acionar sempre que o aluno contar um caso real, mencionar "essa história eu
  já registrei?", "quero cadastrar um caso", ou compartilhar espontaneamente
  um acontecimento em qualquer contexto da conversa.
compatibility: Claude Desktop, Claude Code, claude.ai
metadata: "v1.1.1 — julho 2026 — adiciona verificação automática de versão no BOOT (ver CHANGELOG.md). v1.1 — julho 2026 — relação de delegação com carrossel-triwer explicitada"
---

# Histórias Triwer

Skill de comportamento contínuo — não é só um fluxo de "rodar uma vez e
pronto". Fica atenta durante toda a conversa (qualquer conversa, não só
quando chamada por `/historias-triwer`) para reconhecer quando o aluno está
contando um caso real que vale virar matéria-prima de conteúdo.

**Nunca interrompe o fluxo principal da conversa** para insistir em cadastro —
oferece uma vez, de forma breve, e segue.

---

## REGRA GERAL DE LEITURA DE ARQUIVOS

**Memória** (`memoria.md`) → lida sempre no boot.
**Notion** → índice da database "Histórias Inevitáveis" (História + Tipo +
Descrição) lido uma vez por sessão e mantido em cache, para checar
duplicidade sem reler a cada história detectada. Páginas individuais só são
lidas quando o aluno pedir para consultar uma história específica.

---

## BOOT — EXECUTAR SEMPRE AO INICIAR

### Verificação de versão (antes do Passo 0)

Leia o arquivo `VERSION` desta skill (sibling do `SKILL.md`) — essa é a
versão local. Em seguida, tente buscar
`https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/historias-triwer/CHANGELOG.md`
com a ferramenta de acesso à web disponível no ambiente atual (`WebFetch` no
Claude Code/Desktop; navegação/busca nativa no claude.ai). Se não conseguir
acessar (sem internet, sem ferramenta, timeout etc.), não mencione nada e
siga para o Passo 0.

Se conseguir, leia a entrada mais recente (primeira do arquivo) do CHANGELOG
remoto e compare com a versão local:
- **Igual:** siga em frente sem dizer nada.
- **Remota mais nova, sem tag `[CRITICAL]`:** avise em uma linha, ex.: "💡 Há
  uma versão nova da historias-triwer disponível (v[local] → v[remota]). Não
  é obrigatório atualizar agora, mas recomendo rodar o instalador quando
  puder." Depois siga normalmente — **não bloqueie**.
- **Remota mais nova, com tag `[CRITICAL]`:** pare aqui. Explique em 2-3
  linhas, com base no resumo da entrada do CHANGELOG, por que essa versão
  tem uma correção importante e não deve continuar sendo usada, e informe
  como atualizar:
  - **Claude Code/Desktop:** `irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-historias-windows.ps1 | iex` (Windows) ou `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-historias-mac.sh | bash` (Mac/Linux).
  - **claude.ai (Skills nativo):** baixar o `.zip` mais recente e reenviar
    em Settings → Capabilities → Skills → Upload skill.
  Aguarde o aluno confirmar que atualizou antes de seguir. Se ele insistir em
  prosseguir mesmo assim, atenda, mas deixe registrado que não é o
  recomendado.

### Passo 0 — Verificar onboarding

Tente ler `~/.claude/skills/onboarding-triwer/memoria.md`.

- **Se existir e tiver `onboarding_completo: true`:** prossiga.
- **Se não existir, ou sem essa confirmação:** exiba (só quando a skill for
  acionada diretamente — se for detecção passiva no meio de outra conversa,
  não interrompa com isso; apenas não ofereça cadastro até o onboarding
  existir):

  > Antes de usar esta skill, você precisa concluir a configuração inicial do
  > seu Notion. Rode `/onboarding-triwer` primeiro.

### Passo 1 — Carregar memória

Tente ler `~/.claude/skills/historias-triwer/memoria.md`.

- **Se existir:** carregue `historias_db_url` e o histórico de sessão.
- **Se não existir:** leia `~/.claude/skills/onboarding-triwer/memoria.md`,
  extraia `historias_db_url`, crie `memoria.md` local (formato no fim deste
  arquivo).

### Passo 2 — Verificar conexão com o Notion

Tente uma busca simples com a ferramenta `notion`.

- **Se disponível:** confirme internamente.
- **Se não disponível e a skill foi acionada diretamente:** exiba:

  > ⚠️ **Notion não conectado**
  >
  > Esta skill precisa do conector do Notion ativo para consultar e gravar
  > suas histórias.
  >
  > **Se você usa o Claude Desktop (app instalado):**
  > 1. Abra Configurações → Connectors (Conectores)
  > 2. Clique em "Add Connector" (Adicionar conector)
  > 3. Cole esta URL: `https://mcp.notion.com/mcp`
  > 4. Complete a autorização (OAuth) selecionando o workspace com a sua cópia
  >    do template Triwer
  >
  > **Se você usa o claude.ai (navegador):**
  > 1. Ícone de perfil (canto superior direito) → Settings → Connectors
  > 2. "Browse connectors" → procure "Notion" → clique no "+"
  > 3. Autorize via OAuth e selecione o workspace/página do seu template
  >
  > **Se você usa o Claude Code (terminal):**
  > 1. Rode: `claude mcp add --transport http notion https://mcp.notion.com/mcp`
  > 2. Rode: `/mcp`

  Se for detecção passiva (o aluno não chamou a skill, só contou um caso):
  não exiba esse aviso — apenas não ofereça cadastro nesta sessão.

### Passo 3 — Carregar índice de histórias

Leia da database `historias_db_url` apenas os campos `História`, `Tipo` e
`Descrição` (mesmo padrão econômico usado pelo `carrossel-triwer` na Etapa
0.1). Mantenha em cache pela sessão inteira — não reler.

---

## COMPORTAMENTO CONTÍNUO — DETECÇÃO EM QUALQUER CONVERSA

### O que conta como "história"

Um relato de um acontecimento real — algo que de fato aconteceu, com uma
situação, uma decisão ou um resultado — não uma opinião genérica, não uma
explicação teórica, não uma descrição de processo sem evento concreto.

**Conta como história:** "Teve uma aluna minha que quase desistiu porque
achava que não tinha talento, e três meses depois ela fechou o primeiro
contrato de R$5 mil." "Eu mesmo, no início, gastava 6 horas por post e quase
larguei tudo até descobrir X."

**Não conta:** "Eu acho que consistência é importante." "Meu público costuma
ter dificuldade com precificação." (isso é percepção/padrão, não um caso —
pertence ao `oraculo-triwer`, não aqui.)

### Ao detectar

1. **Checar duplicidade** contra o índice carregado no Passo 3 (por tema e
   personagens envolvidos, não só por texto literal).
2. **Se já existir uma história muito parecida:** não ofereça cadastro de
   novo. Se for relevante ao momento, mencione brevemente que já está
   registrada — não insista.
3. **Se for nova:** ao final do que o aluno está dizendo (nunca no meio,
   cortando o raciocínio), ofereça:

   ```
   Percebi que você mencionou [resumo em 1 linha do acontecimento]. Isso
   ainda não está no seu banco de histórias. Posso cadastrar agora? (leva
   30 segundos)
   ```

4. **Se o aluno recusar ou ignorar:** não pergunte de novo na mesma sessão
   sobre a mesma história. Registre como "oferecida, não aceita" na memória
   de trabalho da sessão (não precisa persistir entre sessões).

---

## CADASTRAR A HISTÓRIA (após aceite)

Colete os campos abaixo. **Não faça isso como formulário** — se o relato já
trouxe boa parte da informação organicamente, apenas confirme e complete o
que faltar, uma pergunta por vez.

| Campo | O que é | Vai para |
|---|---|---|
| História | Nome curto e memorável do caso | Tabela-índice |
| Tipo | Categoria da história | Tabela-índice — ver nota abaixo |
| Descrição | Resumo em 1-2 linhas | Tabela-índice |
| Conflito / Fundo do poço | A situação ruim, com detalhes específicos | Página individual |
| Decisão contraditória | O que pareceu errado, arriscado ou contraintuitivo na hora | Página individual |
| Resultado inesperado | O que contrariou a expectativa — com número ou prova se houver | Página individual |
| Dados brutos | Números e provas específicas mencionadas | Página individual |

Esta é exatamente a estrutura que `carrossel-triwer` já espera ao ler uma
história para montar o Bloco 3 (Virada — Ato 1/2/3). Não crie um formato
diferente.

> **Nota sobre o campo Tipo:** as opções fixas desse campo (se é select ou
> multi-select com valores pré-definidos no Notion) não foram confirmadas.
> Ao criar a entrada, tente ler as opções já existentes na database antes de
> perguntar ao aluno — se já houver um valor parecido cadastrado em outra
> história, reaproveite em vez de criar uma variação nova. Se não conseguir
> listar as opções existentes, pergunte ao aluno como ele classificaria a
> história em 1-2 palavras.

**Regra inviolável:** nunca invente conflito, decisão ou resultado que o
aluno não contou. Se um campo não tiver informação suficiente, pergunte —
não preencha com genérico só para completar a estrutura.

### Confirmar antes de gravar

```
Registro assim?

História: [título]
Tipo: [tipo]
Descrição: [resumo]

Conflito: [conflito]
Decisão: [decisão contraditória]
Resultado: [resultado inesperado]
Dados: [dados brutos]
```

Só grave após aprovação explícita.

### Gravar

Crie a entrada na tabela-índice da database "Histórias Inevitáveis" (História,
Tipo, Descrição) e a página individual com o conteúdo completo. Confirme:

```
Pronto! "[título]" está no seu banco de histórias — já pode ser usada em
carrosséis, na MDI ou onde mais fizer sentido.
```

---

## USO DIRETO DA SKILL

Além da detecção passiva, o aluno pode acionar esta skill de propósito:

- **"Quero cadastrar uma história"** → pule direto para "Cadastrar a
  história" acima; peça o relato primeiro se ainda não foi contado.
- **"Que histórias eu já tenho sobre [tema]?"** → busque no índice carregado
  por relevância temática, liste título + resumo, sem abrir páginas
  individuais a menos que o aluno peça uma específica.
- **"Essa história aqui já está registrada?"** → confira contra o índice e
  responda diretamente.

---

## RELAÇÃO COM `carrossel-triwer`

O `carrossel-triwer` detecta histórias na própria Etapa 1 dele (para não
precisar trocar de skill no meio da criação de um carrossel), mas **delega o
cadastro em si para esta skill** — ele lê a seção "CADASTRAR A HISTÓRIA" deste
arquivo e segue o mesmo processo, em vez de manter uma cópia própria da
lógica. Isso evita divergência: se o método de captura mudar aqui, o
`carrossel-triwer` acompanha automaticamente, sem precisar de edição própria.

Na prática: durante uma sessão de `carrossel-triwer`, é ele quem conduz a
conversa (você não precisa rodar `/historias-triwer` à parte) — mas os campos
coletados, a validação e o formato de confirmação antes de gravar são os
desta skill. Fora de uma sessão de `carrossel-triwer` (qualquer outra
conversa, ou uso direto), esta skill atua sozinha.

---

## Atualizar memória

Atualize `~/.claude/skills/historias-triwer/memoria.md`:

```markdown
# Memória — Histórias Triwer
_Última atualização: [data]_

## Configuração do Notion
- Histórias Inevitáveis (DB): [historias_db_url]

## Preferências registradas
- [qualquer preferência que o aluno expressar durante o uso]
```

---

## REGRAS QUE NÃO MUDAM

| # | Regra | O que falha quando ignorada |
|---|---|---|
| 1 | Nunca interromper o fluxo principal da conversa para insistir em cadastro | Vira ruído em vez de ajuda |
| 2 | Oferecer cadastro uma vez por história, por sessão — não repetir se recusado | Cansa o aluno, soa como bot chato |
| 3 | Checar duplicidade contra o índice antes de oferecer cadastro | Banco de histórias fica com entradas repetidas |
| 4 | Nunca inventar conflito, decisão ou resultado — só o que o aluno contou | História fica genérica, perde a força de caso real |
| 5 | Nunca gravar no Notion sem confirmação explícita do aluno | Aluno perde controle sobre o próprio Notion |
| 6 | Estrutura de campos idêntica à que `carrossel-triwer` já consome | Quebra o Bloco 3 (Virada) de qualquer carrossel que use essa história |
| 7 | "Não conta como história" (opinião, padrão genérico) não deve virar entrada | Polui o banco com material que pertence ao `oraculo-triwer`, não aqui |

---

## INSTALAÇÃO

### Estrutura de pastas

```
~/.claude/skills/historias-triwer/
├── SKILL.md
├── VERSION
└── memoria.md                        ← criado automaticamente no primeiro uso
```

### Mac/Linux

```bash
BASE=~/.claude/skills/historias-triwer
mkdir -p $BASE

cp SKILL.md $BASE/
cp VERSION $BASE/
```

### Windows

```powershell
$BASE = "$env:USERPROFILE\.claude\skills\historias-triwer"
New-Item -ItemType Directory -Force -Path $BASE

Copy-Item SKILL.md $BASE\
Copy-Item VERSION $BASE\
```

### Após instalar

1. Complete o `/onboarding-triwer` antes, se ainda não fez
2. Não precisa rodar por comando — a partir daqui, sempre que você contar um
   caso real numa conversa, esta skill considera se vale oferecer cadastro
3. Para uso direto: digite `/historias-triwer`
