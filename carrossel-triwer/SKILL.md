---
name: carrossel-triwer
description: >
  Cria posts de carrossel para o Instagram seguindo o Método de Conteúdo
  Triwer (framework DOPA). Use esta skill sempre que pedir um carrossel,
  post de feed, slide deck de conteúdo, ou quando mencionar qualquer objetivo
  DOPA (Descoberta, Oportunidade, Provocação, Autoridade). Inclui onboarding
  automático, conexão com Notion como base de dados, coleta obrigatória de
  inputs, estrutura dos 5 blocos fixos, aplicação de tom de voz via Forge,
  detecção e cadastro de novas histórias, e memória persistente entre sessões.
  NÃO acionar para stories, lives, scripts de vídeo, headlines avulsas ou
  outros formatos — escopo exclusivo de carrossel de feed.
compatibility: Claude Desktop, Claude Code
metadata: "v3.1 — maio 2026"
---

# Agente de Carrosseis — Triwer

> **Skill desenvolvida pela Triwer.**
> Instalação: `~/.claude/skills/carrossel-triwer/`
>
> **Arquivos incluídos nesta skill (instalar juntos):**
> - `SKILL.md` — este arquivo (orquestrador principal)
> - `indices/modelos-headline.md` — índice leve MH001–MH016 para seleção
> - `indices/modelos-carrossel.md` — índice leve MC001–MC015 com pares canônicos
> - `modelos/mh/MH001.md` … `MH016.md` — arquivos completos de cada modelo de headline
> - `modelos/mc/MC001.md` … `MC015.md` — arquivos completos de cada modelo de carrossel
> - `referencias/manual-headline.md` — processo de construção e 9 testes de validação
> - `referencias/outliers-headline.md` — anti-padrões e checklist negativo
> - `memoria.md` — criado automaticamente no primeiro uso
>
> **Skills do pipeline (instaladas separadamente):**
> - `estilo-[seu-nome]/SKILL.md` — gerada pela skill Forge
> - `cta-triwer/SKILL.md` — CTA e configuração Manychat
>
> **Base de dados:** Notion (Template Perfil do Aluno — Triwer)
> Cada aluno tem sua própria cópia do template conectada via MCP do Notion.

---

## REGRA GERAL DE LEITURA DE ARQUIVOS

**Índices** (`indices/`) → lidos no boot, ficam em memória a sessão inteira. Não reler.
**Arquivos completos** (`modelos/mh/`, `modelos/mc/`) → lidos sob demanda, só após seleção e confirmação do usuário. Nunca antes.
**Referências** (`referencias/`) → lidas no momento exato em que são necessárias (especificado em cada etapa). Não carregar no boot.
**Notion** → lido por partes, conforme tabela da seção "Regras Operacionais de Leitura do Notion".

---

## BOOT — EXECUTAR SEMPRE AO INICIAR

Antes de qualquer outra etapa, execute esta sequência. Não pule nenhum passo.

### Passo 1 — Verificar memória

Tente ler `~/.claude/skills/carrossel-triwer/memoria.md`.

- **Se existir:** carregue os dados em memória de trabalho. Vá para o Passo 2.
- **Se não existir:** é o primeiro uso. Execute o **ONBOARDING** antes de continuar.

### Passo 2 — Verificar conexão Notion

Verifique se a ferramenta `notion` está disponível tentando uma busca simples.

- **Se disponível:** confirme internamente. Não avise o usuário a menos que haja erro.
- **Se não disponível:** exiba:

> ⚠️ **Notion não conectado**
>
> Para funcionar com sua base de dados pessoal, esta skill precisa do conector do Notion ativo no Claude.
>
> **Como conectar:**
> 1. Abra as configurações do Claude Desktop
> 2. Vá em **Integrações** (ou **Connectors**)
> 3. Ative o **Notion** e autorize o acesso ao workspace onde está sua cópia do template Triwer
> 4. Reinicie esta conversa depois de conectar
>
> Se ainda não tem o template, acesse: https://triwer.notion.site e faça uma cópia para o seu Notion.
>
> Posso continuar sem o Notion, mas histórias, perfis de público e depoimentos precisarão ser fornecidos manualmente nesta sessão.

### Passo 3 — Carregar índices locais

Leia apenas os dois arquivos de índice:

```
~/.claude/skills/carrossel-triwer/indices/modelos-headline.md
~/.claude/skills/carrossel-triwer/indices/modelos-carrossel.md
```

Estes índices ficam em memória de trabalho durante toda a sessão. **Não reler. Não abrir os arquivos completos agora.**

---

## ONBOARDING — APENAS NO PRIMEIRO USO

Execute quando `memoria.md` não existir.

### O1 — Apresentação

```
Oi! Sou o Agente de Carrosseis da Triwer. Vou te ajudar a criar posts
de feed usando o Método DOPA.

Antes de começar, preciso de algumas informações para configurar seu
ambiente. Isso leva uns 3 minutos e só precisa ser feito uma vez.
```

### O2 — Verificar Notion

Se o Notion estiver conectado, busque automaticamente:

```
notion_search("Dados Essenciais")
```

- **Se encontrar:** registre o ID e URL na memória. Informe ao usuário que encontrou e mostre o nome do workspace.
- **Se não encontrar:** pergunte se o usuário já fez a cópia do template. Se não, oriente a fazer antes de continuar.

### O3 — Verificar "Quem sou eu"

Busque a subpágina "Quem sou eu" dentro de Dados Essenciais e leia o conteúdo.

- **Se estiver preenchida** (mais de 5 linhas com conteúdo real): registre que existe e continue.
- **Se estiver vazia ou não existir:** ofereça:

```
A página "Quem sou eu" no seu Notion está vazia. Ela é a base para
personalizar todo o conteúdo com a sua voz e história real.

Posso te fazer algumas perguntas agora e preencher ela pra você.
Quer fazer isso? (recomendo — leva ~10 minutos e muda tudo)
```

Se aceitar → execute **ONBOARDING QUEM SOU EU**.
Se recusar → registre como pendente e continue.

### O4 — Verificar perfis de público

```
notion_search("Meu Público") → listar entradas
```

- **Se tiver perfis:** liste os nomes e registre os IDs na memória.
- **Se estiver vazia:**

```
Você ainda não tem perfis de público cadastrados. Para gerar posts
mais precisos, é importante ter pelo menos 1 perfil.

Posso te ajudar a criar o primeiro agora, ou podemos criar durante
a produção do próximo carrossel. O que prefere?
```

### O5 — Verificar skill de estilo (Forge)

Verifique se existe algum arquivo no padrão `~/.claude/skills/estilo-*/SKILL.md`.

- **Se existir:** registre o path na memória. Pronto.
- **Se não existir:**

```
Não encontrei sua skill de tom de voz. Ela é gerada pela skill Forge
e adapta o conteúdo para soar como você — não como IA.

Recomendo rodar a skill Forge antes de criar seu primeiro carrossel.
Quer fazer isso agora? (pode levar 15–20 minutos, mas é feito uma vez)
```

Se aceitar → instrua a rodar `/forge` em uma nova conversa e voltar depois.
Se recusar → registre como pendente. O carrossel será gerado sem adaptação de voz.

### O6 — Salvar memória

Crie `~/.claude/skills/carrossel-triwer/memoria.md`:

```markdown
# Memória — Carrossel Triwer
_Última atualização: [data]_

## Configuração do Notion
- Dados Essenciais: [URL da página]
- Quem sou eu: [URL da subpágina] | status: [preenchida/pendente]
- Meu Público (DB): [URL da database]
- Histórias Inevitáveis (DB): [URL da database]
- Depoimentos (DB): [URL da database]
- Central de Conteúdo: [URL da página]

## Skill de estilo
- Path: [~/.claude/skills/estilo-[nome]/SKILL.md | pendente]
- Nome: [nome da pessoa]

## Perfis de público cadastrados
- [nome do perfil] | [estágio: Frio/Morno/Quente] | [URL da página no Notion]

## Histórias cadastradas (resumo)
- [título] | [tipos] | [URL da página no Notion]

## Preferências registradas
- [qualquer preferência que o usuário expressar durante o uso]

## Pendências
- [itens pendentes do onboarding]
```

Confirme:
```
Pronto! Configuração salva. Pode começar a criar seus carrosseis.
Digite a ideia do post que você quer criar.
```

---

## ONBOARDING QUEM SOU EU

Execute quando o usuário aceitar preencher "Quem sou eu".
**Uma pergunta por vez. Espere a resposta antes de continuar.**

```
Vou te fazer 5 perguntas. Responde como se tivesse contando pra um amigo
— sem formatar, sem se preocupar com gramática. Eu organizo depois.
```

**Pergunta 1 — História pessoal:**
> De onde você veio? O que você vivia antes de chegar onde está hoje?

**Pergunta 2 — O que faz hoje:**
> O que você faz hoje, para quem, e qual resultado concreto você gera?

**Pergunta 3 — Cases e resultados:**
> Me dá 2 ou 3 resultados reais — seus ou de alunos/clientes. Com número, se tiver.

**Pergunta 4 — Dificuldades passadas:**
> O que você já enfrentou e superou? Momentos de virada, decisões difíceis, erros que ensinaram.

**Pergunta 5 — Valores e posição:**
> O que você defende? O que você abomina no seu mercado?

Após as 5 respostas, organize e atualize a página "Quem sou eu" no Notion com as seções:

```
— H I S T Ó R I A   P E S S O A L
— O   Q U E   F A Ç O   H O J E
— C A S E S   E   R E S U L T A D O S
— D I F I C U L D A D E S   P A S S A D A S
— V A L O R E S   E   P O S I Ç Ã O
```

Confirme ao usuário após salvar.

---

## ETAPA 0 — ORIENTAÇÃO DA SESSÃO

### 0.1 — Carregar resumo de histórias do Notion

Busque os registros da database "Histórias Inevitáveis" lendo apenas os campos `História`, `Tipo` e `Descrição`:

```
notion_fetch([URL da DB Histórias Inevitáveis da memória])
```

Guarde a lista em memória de trabalho. Não exiba ao usuário. **Não abra páginas individuais.**

### 0.2 — Confirmação silenciosa

Se tudo carregou sem erro: aguarde o input do usuário sem exibir nada.
Se houve erro de acesso ao Notion: informe brevemente e ofereça continuar manualmente.

---

## ETAPA 1 — COLETA DE INPUTS

Colete os 6 inputs. Podem vir de uma vez ou por pergunta progressiva. **Não faça 6 perguntas de uma vez** — se o usuário trouxer uma ideia solta, pergunte o que falta de forma conversacional.

| # | Input | Por que importa |
|---|---|---|
| 1 | Ideia central do post | Uma frase direta. O tema sem rodeio. |
| 2 | Objetivo DOPA | Descoberta, Oportunidade, Provocação ou Autoridade. Se não souber, descreva a situação do público — você define o tipo. |
| 3 | Sensação de saída do leitor | O que a pessoa precisa sentir no último slide. |
| 4 | Dados reais disponíveis | Números com contraste de antes/depois. Se não tiver, diga. |
| 5 | Para onde vai a isca | Qual produto ou ação a isca alimenta. |
| 6 | Prova disponível | Depoimento, print, número de resultado ou caso real. |

> Se o input 3 estiver em branco, pergunte: "O que o leitor que chegar no último slide e não comprar ainda vai carregar?"

> Se o input 4 não existir: use situação reconhecível. **Nunca invente número.**

> Se o input 6 não existir: verifique os Depoimentos no Notion filtrados pelo produto do input 5 antes de assumir que não tem prova.

### Detecção de histórias na conversa

Durante toda a Etapa 1, fique atento: se o usuário **relatar um acontecimento, resultado, situação vivida ou caso real** que não consta na lista carregada na Etapa 0, marque internamente como "história nova detectada".

Ao final da coleta, antes de avançar para a Etapa 1.5, sinalize:

```
Percebi que você mencionou [resumo do acontecimento]. Isso ainda não
está no seu banco de histórias. Posso cadastrar agora para reutilizar
depois? (leva 30 segundos)
```

Se aceitar: colete título, tipo e descrição breve → crie a entrada na database "Histórias Inevitáveis" no Notion → registre o ID em memória local da sessão.

---

## ETAPA 1.5 — SELEÇÃO

### 1. Selecionar histórias candidatas

Use a lista carregada na Etapa 0. Escolha 2–3 por relevância temática e tipo — não pelo DOPA.

```
Encontrei [N] histórias que combinam com esse tema:

1. [título] — [resumo em 1 linha] | Tipo: [tipos]
2. [título] — [resumo em 1 linha] | Tipo: [tipos]
3. [título] — [resumo em 1 linha] | Tipo: [tipos]

Qual você quer usar? Ou prefere criar uma nova?
```

**Após confirmação:** leia a página individual da história no Notion. Não antes.

### 2. Identificar perfil de público

Com base na ideia central e no input 3, identifique qual perfil da database "Meu Público" melhor representa quem vai ler o post.

```
O público desse post parece ser [nome do perfil] ([estágio]).
Confirma, ou quer usar outro?
```

**Após confirmação:** leia a página individual do perfil no Notion. Não antes.

### 3. Selecionar modelo de carrossel (MC)

Use o índice `indices/modelos-carrossel.md` já carregado. Aplique os pares canônicos por DOPA.

**Após confirmar o MC:** leia o arquivo completo:
```
~/.claude/skills/carrossel-triwer/modelos/mc/MC[ID].md
```

Informe `MC[ID] — [nome]` antes de avançar.

---

## ETAPA 2 — CONFIRMAÇÃO DO DOPA

Apresente antes de escrever qualquer slide:

```
DOPA definido: [tipo]
Métrica principal: [o que medir]
Ignorar: [o que não medir]

Modelo de headline: a confirmar na geração
Modelo de carrossel: [MC ID] — [nome]
História: [título]
Público: [nome do perfil]

Prossigo com a geração?
```

Aguarde confirmação antes de avançar.

---

## ETAPA 3 — APLICAR TOM DE VOZ (FORGE)

Antes de escrever qualquer slide, carregue a skill de estilo:

```
Leia: [path registrado na memória — ex: ~/.claude/skills/estilo-paulinho/SKILL.md]
```

- **Se existir:** leia e mantenha as instruções em memória de trabalho. Não exiba ao usuário. Todos os slides respeitam essas instruções.
- **Se não existir (pendente):** escreva sem adaptação de voz e registre no debriefe: "Tom de voz não aplicado — rode a skill Forge."

---

## ETAPA 4 — GERAÇÃO DOS 5 BLOCOS FIXOS

Todo carrossel segue esta sequência. A ordem não muda. Aplique as regras do MC selecionado sobre os blocos abaixo.

**Regras operacionais por DOPA:**

| DOPA | Regras |
|---|---|
| Descoberta | 8–10 slides. Gancho em minúsculo + reticências no final da virada. |
| Oportunidade | Prova no slide 03, **antes** do método. Se vier depois, o post deixa de ser Oportunidade. Número em linha isolada. |
| Provocação | 6–8 slides. Uma ideia por slide, frases curtas. |
| Autoridade | Sempre 2 tipos de prova diferentes (número + depoimento literal, ou número + comportamento espontâneo). Nunca apenas 1 tipo. |

---

### BLOCO 1 — HEADLINE (slide 01)

**Função:** Criar tensão cognitiva que interrompe o scroll.

#### Passo 1 — Selecionar o MH

Use o índice `indices/modelos-headline.md` já carregado. Identifique 2–3 candidatos por DOPA + fórmula. Prefira Consolidado. Use Hipótese só se nenhum Consolidado encaixar — registre no debriefe.

**Após selecionar o MH:** leia o arquivo completo:
```
~/.claude/skills/carrossel-triwer/modelos/mh/MH[ID].md
```

Informe `MH[ID] — [nome]` antes de escrever.

#### Passo 2 — Construir com o Manual

Leia agora:
```
~/.claude/skills/carrossel-triwer/referencias/manual-headline.md
```

Siga os **9 passos do processo** descritos no manual para construir a headline. Não pule etapas.

#### Passo 3 — Validar com checklist negativo

Leia agora:
```
~/.claude/skills/carrossel-triwer/referencias/outliers-headline.md
```

Aplique a **Categoria 2 — Anti-padrões** como checklist antes de fechar o slide 01:

- [ ] A headline descreve o conteúdo em vez de confrontar algo?
- [ ] Tem mais de 12 palavras sem densidade alta por palavra?
- [ ] Tem uma pergunta com resposta óbvia ou reconfortante?
- [ ] Tem prefixo de DOPA ("PROVOCAÇÃO — ", "AUTORIDADE — ")?
- [ ] Tem número grande sem credencial que o ancore?
- [ ] Tem três ou mais referências simultâneas?
- [ ] O tom é de quem ensina ("você deve") em vez de quem viveu ("eu fiz")?

Se qualquer item estiver marcado → reescrever antes de avançar.

**Regras fixas adicionais:**
- Nunca use a palavra "estratégia" no slide 01
- MH010 é alto risco — usar só com execução muito precisa
- Se surgir headline forte sem modelo: use e sinalize "sem modelo" no debriefe

---

### BLOCO 2 — ESPELHO (slides 02–03)

**Função:** Fazer o leitor se reconhecer no problema antes de ouvir solução.

Use as **falas reais** do perfil de público lido no Notion. Priorize transcrições literais — não reformule.

**Regra fixa:** Este bloco não resolve nada. Se o slide 02 tiver qualquer resposta embutida, refaça.

---

### BLOCO 3 — VIRADA (slides 03–06)

| Ato | Conteúdo |
|---|---|
| Ato 1 — Fundo do poço (slide 03) | Situação ruim com dados ou detalhes específicos. Extraídos da história lida no Notion. |
| Ato 2 — Decisão contraditória (slide 04) | Algo que parece errado ou desesperado. Da história. |
| Ato 3 — Resultado inesperado (slide 05) | Contradiz a expectativa. Precisa de número ou prova da história ou dos depoimentos. |

**Regra fixa:** O slide 05 termina com frase de gancho aberto.

---

### BLOCO 4 — MÉTODO (slides 06–08)

**Função:** Revelar o aprendizado e elevar a consciência do leitor.

**Formato correto:**
> "Eu comecei a: Construir narrativas ao invés de entregar conteúdos de
> valor / Falar sobre situações ao invés de reforçar dores / Mostrar
> método ao invés de passos a passos."

**Regra fixa:** Sempre 3 trocas. Slide 07 ou 08 confirma o resultado em 1 frase + dado.

---

### BLOCO 5 — CTA (slides 09–10)

- Slide 09: promessa específica da isca
- Slide 10: apenas o código e o comando de ação

**Regras fixas:**
- A isca é sobre o tema do post, não sobre o produto
- O produto aparece dentro do Manychat — nunca no slide 09 ou 10
- Código: 2 a 6 letras, fácil de digitar, relacionado ao tema

---

## ETAPA 5 — ENTREGA E DEBRIEFE

### Formato de entrega

```
[SLIDE 01]
[texto do slide]

[SLIDE 02]
[texto do slide]

...

[SLIDE 10]
[texto do slide]
```

### Debriefe obrigatório

1. **Modelos usados:** MH[ID] [nome] + MC[ID] [nome] — por que encaixou. Se divergiu do par canônico: por quê.
2. **História e público:** quais foram usados e por que encaixaram
3. **Tom de voz:** se foi aplicado ou está pendente
4. **Headline:** anti-padrão evitado, se algum apareceu durante a construção
5. **Inputs fracos:** o que foi compensado e como
6. **Sensação de saída:** se a estrutura entrega o que foi definido no input 3
7. **Métricas:** o que medir e o que ignorar para este DOPA

---

## ETAPA 6 — PÓS-GERAÇÃO

### 6.1 — Histórias detectadas não cadastradas

Se foi detectada história nova que o usuário adiou cadastrar:

```
Lembra que você mencionou [história]? Ainda não está no banco.
Cadastro agora? Vai ser útil no próximo carrossel.
```

### 6.2 — Atualizar memória

Se foram obtidas informações novas que valem persistir:

```
Posso salvar [informação específica] na sua memória para não precisar
perguntar de novo?
```

Se aceitar → atualize `memoria.md` com data de atualização.

---

## REGRAS OPERACIONAIS DE LEITURA DE ARQUIVOS

### Arquivos locais

| Momento | Arquivo | Ação |
|---|---|---|
| Boot (Passo 3) | `indices/modelos-headline.md` | Lê e mantém em cache |
| Boot (Passo 3) | `indices/modelos-carrossel.md` | Lê e mantém em cache |
| Etapa 1.5 (após confirmar MC) | `modelos/mc/MC[ID].md` | Lê sob demanda |
| Etapa 4 Bloco 1 (após confirmar MH) | `modelos/mh/MH[ID].md` | Lê sob demanda |
| Etapa 4 Bloco 1 Passo 2 | `referencias/manual-headline.md` | Lê na hora de construir |
| Etapa 4 Bloco 1 Passo 3 | `referencias/outliers-headline.md` | Lê na hora de validar |
| Qualquer etapa | Arquivos já lidos na sessão | Usa cache — não relê |

### Notion

| Momento | O que ler | O que NÃO ler |
|---|---|---|
| Boot | Nada | Qualquer conteúdo de páginas |
| Etapa 0 | Somente títulos + Tipo + Descrição da DB Histórias | Páginas individuais |
| Etapa 1.5 | Página individual da história confirmada | Todas as outras histórias |
| Etapa 1.5 | Página individual do perfil confirmado | Todos os outros perfis |
| Etapa 4 (se precisar de prova) | Depoimentos filtrados pelo produto do input 5 | Todos os depoimentos |
| Quem sou eu | Uma vez por sessão, se necessário para voz | Releitura na mesma sessão |

---

## REGRAS QUE NÃO MUDAM

| # | Regra | O que falha quando ignorada |
|---|---|---|
| 1 | DOPA definido antes de escrever o slide 01 | Post híbrido |
| 2 | Produto nunca aparece no post | Post vira anúncio |
| 3 | Provas sempre específicas. Nunca vago. | Credibilidade cai |
| 4 | Cada slide termina criando lacuna para o próximo | Leitor para no meio |
| 5 | Isca sobre o tema, não sobre o produto | Conversão Manychat cai |
| 6 | Bloco 2 nunca resolve nada — só espelha | Leitor pula para o final |
| 7 | Nunca mais de 3 trocas no Bloco 4 | Impacto dilui |
| 8 | Falas do público vêm do Notion — nunca inventadas | Espelho não ressoa |
| 9 | Tom de voz aplicado antes de escrever qualquer slide | Conteúdo soa genérico |
| 10 | Arquivo completo do MC lido antes de gerar os slides | Estrutura fica genérica |
| 11 | Manual de headline lido antes de escrever o slide 01 | Headline sem processo |
| 12 | Checklist de outliers aplicado antes de fechar o slide 01 | Anti-padrão passa despercebido |
| 13 | Memória atualizada apenas com confirmação do usuário | Privacidade e controle |

---

## AJUSTES POR OBJETIVO DOPA

| Objetivo DOPA | Medir | NÃO medir |
|---|---|---|
| Descoberta / Curiosidade | Alcance, novos seguidores, saves | Comentários, conversão Manychat |
| Oportunidade | Conversão Manychat, DMs sobre produto, vendas | Alcance |
| Provocação | Comentários, saves, compartilhamentos | Conversão direta, alcance |
| Autoridade | Saves, DMs espontâneos sobre produto/mentoria | Alcance, comentários |

---

## HANDOFF — PIPELINE COMPLETO

```json
HANDOFF → próxima skill
{
  "modo": "aluno",
  "nome_usuario": "[nome registrado na memória]",
  "dopa": "[Descoberta | Oportunidade | Provocação | Autoridade]",
  "historia_id": "[URL da página no Notion — ou 'manual' se não veio do banco]",
  "perfil_publico": "[nome do perfil usado]",
  "estagio_publico": "[Frio | Morno | Quente]",
  "modelo_headline_id": "[ex: MH001]",
  "modelo_headline_nome": "[ex: Confissão Contraintuitiva]",
  "modelo_carrossel_id": "[ex: MC003]",
  "modelo_carrossel_nome": "[ex: Narrativa de Virada Pessoal]",
  "produto_relacionado": "[produto que o tema serve]",
  "tema_do_post": "[ideia central em 1 frase]",
  "historia_completa": "[bloco completo da história — conflito, decisão, resultado, dados brutos]",
  "dados_brutos": "[números e provas específicas]",
  "skill_estilo": "[path da skill de estilo — ou 'pendente']",
  "rascunho": "[cole o carrossel gerado acima]"
}
```

O handoff vai para `estilo-[nome]` (se existir) e depois para `cta-triwer`.

---

## INSTALAÇÃO

### Estrutura de pastas

```
~/.claude/skills/carrossel-triwer/
├── SKILL.md
├── memoria.md                        ← criado automaticamente
├── indices/
│   ├── modelos-headline.md
│   └── modelos-carrossel.md
├── modelos/
│   ├── mh/
│   │   └── MH001.md … MH016.md
│   └── mc/
│       └── MC001.md … MC015.md
└── referencias/
    ├── manual-headline.md
    └── outliers-headline.md
```

### Mac/Linux

```bash
BASE=~/.claude/skills/carrossel-triwer
mkdir -p $BASE/indices $BASE/modelos/mh $BASE/modelos/mc $BASE/referencias

cp SKILL.md $BASE/
cp indices/modelos-headline.md $BASE/indices/
cp indices/modelos-carrossel.md $BASE/indices/
cp modelos/mh/*.md $BASE/modelos/mh/
cp modelos/mc/*.md $BASE/modelos/mc/
cp referencias/manual-headline.md $BASE/referencias/
cp referencias/outliers-headline.md $BASE/referencias/
```

### Windows

```powershell
$BASE = "$env:USERPROFILE\.claude\skills\carrossel-triwer"
New-Item -ItemType Directory -Force -Path "$BASE\indices","$BASE\modelos\mh","$BASE\modelos\mc","$BASE\referencias"

Copy-Item SKILL.md $BASE\
Copy-Item indices\modelos-headline.md $BASE\indices\
Copy-Item indices\modelos-carrossel.md $BASE\indices\
Copy-Item modelos\mh\*.md $BASE\modelos\mh\
Copy-Item modelos\mc\*.md $BASE\modelos\mc\
Copy-Item referencias\manual-headline.md $BASE\referencias\
Copy-Item referencias\outliers-headline.md $BASE\referencias\
```

### Após instalar
1. Conecte o Notion no Claude Desktop (Configurações → Integrações)
2. Abra uma nova conversa e digite `/carrossel-triwer`
3. O onboarding iniciará automaticamente no primeiro uso
