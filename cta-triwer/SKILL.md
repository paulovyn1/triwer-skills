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
compatibility: Claude Desktop, Claude Code
metadata: "v3.0 — maio 2026"
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

### Passo 1 — Verificar memória

Tente ler `~/.claude/skills/cta-triwer/memoria.md`.

- **Se existir:** carregue os dados em memória de trabalho. Especialmente: URL da database de Iscas no Notion e URL da database de Produtos.
- **Se não existir:** é o primeiro uso. Execute o **ONBOARDING** antes de continuar.

### Passo 2 — Carregar regras

Leia sempre:
```
~/.claude/skills/cta-triwer/referencias/iscas-regras.md
```

Mantenha em memória de trabalho. Não reler na mesma sessão.

### Passo 3 — Verificar Notion

Verifique se a ferramenta `notion` está disponível.

- **Se disponível:** confirme internamente. Fonte principal de iscas será o Notion.
- **Se não disponível:** carregue o fallback local:
  ```
  ~/.claude/skills/cta-triwer/referencias/iscas-exemplo.md
  ```
  E informe brevemente: "Notion não conectado — usando banco de iscas local como rascunho."

---

## ONBOARDING — APENAS NO PRIMEIRO USO

Execute quando `memoria.md` não existir.

### O1 — Verificar Notion

Se o Notion estiver conectado, busque automaticamente a página "Central de ativos" e dentro dela a database "Iscas gerais":

```
notion_search("Iscas gerais")
```

- **Se encontrar:** registre a URL da database na memória.
- **Se não encontrar:** oriente o aluno a verificar se fez a cópia do template Triwer corretamente e se a integração do Notion está ativa no Claude.

### O2 — Verificar database de Produtos

Busque a database "Produtos" no Notion:

```
notion_search("Produtos")
```

- **Se encontrar:** registre a URL na memória.
- **Se não encontrar:** registre como pendente.

### O3 — Salvar memória

Crie `~/.claude/skills/cta-triwer/memoria.md`:

```markdown
# Memória — CTA Triwer
_Última atualização: [data]_

## Notion
- Iscas gerais (DB): [URL da database]
- Produtos (DB): [URL da database]

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
modo               → nome do aluno (identifica o pipeline)
dopa               → define a lógica de decisão de Manychat
tema_do_post       → base para escolha da isca
produto_relacionado → filtra o banco de iscas no Notion
rascunho           → o carrossel a finalizar
```

Se acionada isoladamente (sem handoff), colete esses dados do usuário antes de continuar.

---

## PASSO 1 — BUSCAR ISCAS NO NOTION

### Se Notion conectado (fonte principal)

Com base no `produto_relacionado` do handoff, busque na database "Iscas gerais" filtrando pelo campo `Produto`:

```
notion_fetch([URL da DB Iscas gerais da memória])
→ filtrar por Produto = [produto_relacionado]
→ filtrar por Status = "✅ Ativa"
```

Leia apenas os campos: `Nome`, `Código Manychat`, `O que entrega`, `Objetivo MC`, `Status`, `Produto`.

**Se nenhuma isca ativa for encontrada para o produto:** expanda a busca para iscas sem produto vinculado, depois para iscas de categoria temática próxima.

### Se Notion não conectado (fallback local)

Use o arquivo `referencias/iscas-exemplo.md` já carregado no boot. Identifique a seção que corresponde ao `produto_relacionado` e use as iscas ativas dessa seção.

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
├── memoria.md                        ← criado automaticamente
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
1. Confirme que o Notion está conectado no Claude Desktop
2. Abra uma nova conversa e digite `/cta-triwer`
3. O onboarding iniciará automaticamente no primeiro uso
