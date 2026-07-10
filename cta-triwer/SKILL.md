---
name: cta-triwer
description: >
  Decide se um carrossel da Triwer deve ou não ter Manychat, escolhe a isca
  certa baseada no tema e DOPA, e reescreve os slides 09-10 com a CTA final.
  Acionar SEMPRE após carrossel-triwer (e estilo se instalado), ou
  isoladamente para revisar ou trocar a CTA de qualquer post existente.
  Busca iscas no Notion do aluno como fonte principal. Usa arquivo local
  como fallback quando Notion não estiver conectado. Detecta iscas novas
  mencionadas na conversa e oferece cadastrá-las no Notion automaticamente.
compatibility: Claude Desktop, Claude Code, claude.ai
metadata: "v4.0.1 — julho 2026 — adiciona verificação automática de versão no BOOT (ver CHANGELOG.md). v4.0 — julho 2026 — onboarding delegado ao onboarding-triwer"
---

# CTA Triwer

Decide se o carrossel tem Manychat, escolhe a isca certa e entrega os
slides 09-10 finais. Não reescreve o resto do carrossel — só o final.

---

## REGRA GERAL DE LEITURA DE ARQUIVOS

**Memória** (`memoria.md`) → lida sempre no boot, mantida em cache.
**Regras** (`referencias/iscas-regras.md`) → lida sempre no boot.
**Padrões de iscas** (`referencias/padroes-de-iscas.md`) → lida APENAS ao criar ou avaliar isca nova.
**Iscas locais** (`referencias/iscas-local.md`) → lida só se Notion não estiver disponível.
**Notion** → fonte principal de iscas. Lida sob demanda após identificar o produto.

---

## BOOT — EXECUTAR SEMPRE AO INICIAR

### Verificação de versão (antes do Passo 0)

Leia o arquivo `VERSION` desta skill (sibling do `SKILL.md`) — essa é a
versão local. Em seguida, tente buscar
`https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/cta-triwer/CHANGELOG.md`
com a ferramenta de acesso à web disponível no ambiente atual (`WebFetch` no
Claude Code/Desktop; navegação/busca nativa no claude.ai). Se não conseguir
acessar (sem internet, sem ferramenta, timeout etc.), não mencione nada e
siga para o Passo 0.

Se conseguir, leia a entrada mais recente (primeira do arquivo) do CHANGELOG
remoto e compare com a versão local:
- **Igual:** siga em frente sem dizer nada.
- **Remota mais nova, sem tag `[CRITICAL]`:** avise em uma linha, ex.: "💡 Há
  uma versão nova da cta-triwer disponível (v[local] → v[remota]). Não é
  obrigatório atualizar agora, mas recomendo rodar o instalador quando
  puder." Depois siga normalmente — **não bloqueie**.
- **Remota mais nova, com tag `[CRITICAL]`:** pare aqui. Explique em 2-3
  linhas, com base no resumo da entrada do CHANGELOG, por que essa versão
  tem uma correção importante e não deve continuar sendo usada, e informe
  como atualizar:
  - **Claude Code/Desktop:** `irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-cta-windows.ps1 | iex` (Windows) ou `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-cta-mac.sh | bash` (Mac/Linux).
  - **claude.ai (Skills nativo):** baixar o `.zip` mais recente e reenviar
    em Settings → Capabilities → Skills → Upload skill.
  Aguarde o aluno confirmar que atualizou antes de seguir. Se ele insistir em
  prosseguir mesmo assim, atenda, mas deixe registrado que não é o
  recomendado.

### Passo 0 — Verificar onboarding

Tente ler `~/.claude/skills/onboarding-triwer/memoria.md`.

- **Se existir e tiver `onboarding_completo: true`:** prossiga.
- **Se não existir, ou sem essa confirmação:** exiba:

  > Antes de usar esta skill, você precisa concluir a configuração inicial do
  > seu Notion. Isso leva poucos minutos e só precisa ser feito uma vez.
  >
  > Rode `/onboarding-triwer` primeiro, depois volte aqui.

  Aguarde. Não prossiga sem o onboarding concluído.

### Passo 1 — Carregar memória

Tente ler `~/.claude/skills/cta-triwer/memoria.md`.

- **Se existir:** carregue os dados em memória de trabalho — especialmente
  `iscas_db_url` e `produtos_db_url`. Vá para o Passo 2.
- **Se não existir** (instalação feita depois do onboarding, ou onboarding
  não propagou): leia `~/.claude/skills/onboarding-triwer/memoria.md`
  diretamente, extraia `iscas_db_url` e `produtos_db_url` da seção "Notion —
  URLs essenciais", e crie `~/.claude/skills/cta-triwer/memoria.md` com elas
  (formato do Passo 4 abaixo). Não pergunte essas URLs ao aluno — já foram
  resolvidas no onboarding.

### Passo 2 — Carregar regras

Leia sempre:
```
~/.claude/skills/cta-triwer/referencias/iscas-regras.md
```

Mantenha em memória de trabalho. Não reler na mesma sessão.

### Passo 3 — Verificar Notion

Verifique se a ferramenta `notion` está disponível.

- **Se disponível:** confirme internamente. Fonte principal de iscas será o Notion.
- **Se não disponível:** exiba:

  > ⚠️ **Notion não conectado**
  >
  > Esta skill precisa do conector do Notion ativo para ler e gravar no seu Notion pessoal.
  >
  > **Se você usa o Claude Desktop (app instalado):**
  > 1. Abra Configurações → Connectors (Conectores)
  > 2. Clique em "Add Connector" (Adicionar conector)
  > 3. Cole esta URL: `https://mcp.notion.com/mcp`
  > 4. Complete a autorização (OAuth) selecionando o workspace com a sua cópia do template Triwer
  > Disponível nos planos Pro, Max, Team e Enterprise.
  >
  > **Se você usa o claude.ai (navegador):**
  > 1. Clique no seu ícone de perfil (canto superior direito) → Settings
  > 2. No menu à esquerda, clique em Connectors
  > 3. Clique em "Browse connectors" e procure "Notion" na categoria Web
  > 4. Clique no "+" ao lado do Notion
  > 5. Autorize via OAuth e selecione o workspace/página do seu template Triwer
  >
  > **Se você usa o Claude Code (terminal):**
  > 1. Rode: `claude mcp add --transport http notion https://mcp.notion.com/mcp`
  > 2. Rode: `/mcp`
  > 3. Siga o fluxo de autorização (OAuth) no navegador que abrir
  >
  > Posso continuar sem o Notion, usando um banco de iscas local como rascunho.

  Depois disso, carregue o fallback local:
  ```
  ~/.claude/skills/cta-triwer/referencias/iscas-local.md
  ```

### Passo 4 — Formato de `memoria.md`

Se precisou criar `memoria.md` no Passo 1, use este formato:

```markdown
# Memória — CTA Triwer
_Última atualização: [data]_

## Configuração do Notion
- Iscas gerais (DB): [iscas_db_url]
- Produtos (DB): [produtos_db_url]

## Preferências registradas
- [preferências que o usuário expressar durante o uso]

## Iscas com bom histórico de conversão
- [isca] | [tema] | [DOPA] | [data]

## Iscas com histórico fraco
- [isca] | [tema] | [DOPA] | [data]

## Pendências
- [itens pendentes]
```

---

## PASSO 0 — LER O HANDOFF

Ao receber o handoff da `carrossel-triwer`, extraia:

```
modo                → confirma que é o pipeline do aluno (sempre "aluno")
nome_usuario        → nome do aluno, só para referência
dopa                → define a lógica de decisão de Manychat
tema_do_post        → base para escolha da isca
produto_relacionado → filtra o banco de iscas no Notion
rascunho             → o carrossel a finalizar
```

> **Correção (02/07/2026):** a versão anterior descrevia `modo` como se
> contivesse o nome do aluno. No handoff real do `carrossel-triwer`, `modo` é
> sempre a string fixa `"aluno"` — o nome está em `nome_usuario`, campo
> separado. Corrigido acima.

Se acionada isoladamente (sem handoff), colete esses dados do usuário antes de continuar.

---

## PASSO 1 — BUSCAR ISCAS NO NOTION

### Se Notion conectado (fonte principal)

Com base no `produto_relacionado` do handoff, busque na database "Iscas gerais" (`iscas_db_url` da memória) filtrando pelo campo `Produto`:

```
notion_fetch([iscas_db_url da memória])
→ filtrar por Produto = [produto_relacionado]
→ filtrar por Status = "✅ Ativa"
```

Leia apenas os campos: `Nome`, `Código Manychat`, `O que entrega`, `Objetivo MC`, `Status`, `Produto`.

**Se nenhuma isca ativa for encontrada para o produto:** expanda a busca para iscas sem produto vinculado, depois para iscas de categoria temática próxima.

### Se Notion não conectado (fallback local)

Use o arquivo `referencias/iscas-local.md` já carregado no boot. Identifique a seção que corresponde ao `produto_relacionado` e use as iscas ativas dessa seção.

---

## PASSO 2 — DECIDIR SE TEM MANYCHAT

Baseado no DOPA e no objetivo do post, consulte as regras do arquivo `iscas-regras.md` e aplique:

| DOPA | Objetivo do post | Decisão padrão |
|---|---|---|
| Descoberta | Alcance + novos seguidores | SEM MC se alcance for prioridade. COM MC Captação se quiser leads. |
| Oportunidade | Conversão em intenção de compra | COM MC sempre. |
| Provocação | Engajamento da base | SEM MC se objetivo for comentários. COM MC se for campanha ativa. |
| Autoridade | Fechar objeções | SEM MC se o post gera DM espontâneo. COM MC se quiser direcionar para funil. |

Se houver dúvida sobre a intenção, pergunte ao usuário antes de decidir.

---

## PASSO 3 — ESCOLHER A ISCA

Com as iscas carregadas no Passo 1, aplique os critérios em ordem:

1. **Próximo passo natural** — a isca entrega a continuação direta do que o post ensinou. Nunca produto diferente do tema.
2. **Objetivo MC compatível** — o objetivo da isca bate com a decisão do Passo 2. Prioridade: Isca/Engajamento > Captação > Looping > Venda.
3. **Status ✅ Ativa** — isca com ⚠️ Verificar só usar se for a única opção, avisando o usuário para confirmar.
4. **Código curto e temático** — 2 a 6 letras relacionadas ao tema. Nunca genérico ("INFO", "MAIS", "QUERO").

**Se nenhuma isca existente encaixar:** leia o arquivo de padrões e sinalize ao usuário:

```
~/.claude/skills/cta-triwer/referencias/padroes-de-iscas.md
```

Depois ofereça criar uma nova com base nos padrões:

```
Não encontrei uma isca que encaixe bem nesse tema. Posso criar uma agora
e cadastrar no seu Notion. Quer tentar? Me diz o que você entregaria
no direct para quem comentar o código.
```

### Detecção de isca nova na conversa

Durante toda a sessão, fique atento: se o usuário **mencionar uma entrega específica, material, documento ou recurso** que não consta no banco de iscas, leia o arquivo de padrões para avaliar o potencial da isca:

```
~/.claude/skills/cta-triwer/referencias/padroes-de-iscas.md
```

Depois sinalize:

```
Você mencionou [material/recurso]. Isso poderia virar uma isca nova.
Posso cadastrar no seu Notion agora com as informações que você passou?
```

Se aceitar: colete Nome, Código sugerido, O que entrega, Objetivo MC, Produto relacionado → crie a entrada na database "Iscas gerais" → atualize a memória com a nova isca.

---

## PASSO 4 — ESCREVER OS SLIDES 09-10

### Com Manychat

**Slide 09:**
```
Vou te entregar [nome específico da isca] no direct
[complemento em 1 linha — o que vai receber]
é só comentar aqui
```

**Slide 10:**
```
[CÓDIGO]
↑ comenta essa palavra
```

### Sem Manychat

**Opção A — Pergunta (Provocação):**
```
[Pergunta direta relacionada ao tema]
Me conta nos comentários ⬇️
```

**Opção B — Salvar/seguir (Descoberta de alto alcance):**
```
Salva esse post para não perder
e me segue para os próximos
```

**Opção C — Sem CTA explícita (Autoridade com DM natural)**
Slide 09 e 10 ficam com reflexão ou convite leve — sem código, sem comando.

---

## PASSO 5 — ENTREGA

```
DECISÃO: [COM MC — objetivo: X] ou [SEM MC — motivo: Y]
ISCA ESCOLHIDA: [nome] | Código: [CÓDIGO] | Fonte: [Notion / local]
MOTIVO: [1 frase explicando por que essa isca]

[SLIDE 09]
[texto]

[SLIDE 10]
[texto]
```

---

## PASSO 6 — PÓS-GERAÇÃO

### 6.1 — Isca nova detectada não cadastrada

Se durante a sessão foi detectada isca nova que o usuário adiou cadastrar:

```
Lembra que você mencionou [material]? Ainda não está no banco.
Cadastro agora no Notion? Leva 30 segundos.
```

### 6.2 — Atualizar memória

Se o usuário fizer uma correção sobre a isca escolhida, ou se a isca tiver histórico de conversão notável, pergunte:

```
Posso salvar essa informação na memória para usar nas próximas vezes?
```

Se aceitar → atualize `memoria.md` nas seções "Iscas com bom histórico" ou "Preferências registradas" com data de atualização.

---

## REGRAS QUE NÃO MUDAM

| # | Regra | O que falha quando ignorada |
|---|---|---|
| 1 | Isca sempre sobre o tema do post — nunca sobre o produto direto | Parece propaganda, não conteúdo |
| 2 | Produto aparece dentro do Manychat — nunca no slide 09 ou 10 | Post vira anúncio |
| 3 | Código em linha isolada — sempre | Leitura dificulta e conversão cai |
| 4 | Isca inativa não pode ser usada sem confirmação do usuário | Gera confusão operacional |
| 5 | Prioridade: Isca/Engajamento > Captação > Looping > Venda | Conversão média cai |
| 6 | Entrega específica e nomeada — nunca "mais informações" | Taxa de comentário cai |
| 7 | Isca nova detectada → sempre oferecer cadastrar no Notion | Banco de iscas não cresce |
| 8 | Memória atualizada apenas com confirmação do usuário | Privacidade e controle |

---

## INSTALAÇÃO

### Estrutura de pastas

```
~/.claude/skills/cta-triwer/
├── SKILL.md
├── memoria.md                        ← criado/propagado automaticamente
└── referencias/
    ├── iscas-regras.md               ← lida no boot
    ├── padroes-de-iscas.md           ← lida ao criar isca nova
    └── iscas-local.md                ← fallback quando Notion offline
```

### Mac/Linux

```bash
BASE=~/.claude/skills/cta-triwer
mkdir -p $BASE/referencias

cp SKILL.md $BASE/
cp referencias/iscas-regras.md $BASE/referencias/
cp referencias/padroes-de-iscas.md $BASE/referencias/
cp referencias/iscas-local.md $BASE/referencias/
```

### Windows

```powershell
$BASE = "$env:USERPROFILE\.claude\skills\cta-triwer"
New-Item -ItemType Directory -Force -Path "$BASE\referencias"

Copy-Item SKILL.md $BASE\
Copy-Item referencias\iscas-regras.md $BASE\referencias\
Copy-Item referencias\padroes-de-iscas.md $BASE\referencias\
Copy-Item referencias\iscas-local.md $BASE\referencias\
```

### Após instalar

1. Complete o `/onboarding-triwer` antes, se ainda não fez
2. Abra uma nova conversa e digite `/cta-triwer`
