# Triwer Skills

Ecossistema de skills para Claude (Desktop, Code e claude.ai) que transforma o
Notion de cada aluno da Triwer num "segundo cérebro" — configurado
progressivamente conforme ele avança no curso — e usa essa base para gerar
conteúdo personalizado (carrosséis, CTAs) em vez de genérico.

---

## O que está incluído

13 skills, cada uma com uma responsabilidade específica. A tabela segue a
ordem recomendada de uso — não precisa instalar todas de uma vez, mas cada
skill de conteúdo (Carrossel) depende de algumas anteriores já terem sido
rodadas pelo menos uma vez.

| # | Skill | O que faz |
|---|---|---|
| 1 | **onboarding-triwer** | Primeira a rodar, sempre. Duplica/conecta o Notion modelo, personaliza a home do aluno e resolve as URLs que todas as outras skills usam. |
| 2 | **estilo-forge** | Analisa textos reais do aluno e gera uma skill `estilo-[nome]` que ensina o Claude a escrever com a voz dele, não genérica. |
| 3 | **dexter-triwer** | Brainstorm de produto novo para quem ainda não tem nenhum produto definido — gera 5 ideias distintas (público, promessa esboçada, formato) a partir do que o aluno já sabe fazer. Alternativa ao Dr. House para quem está começando do zero. |
| 4 | **dr-house-triwer** | Diagnostica o produto/serviço do aluno — onde a cadeia público → problema → promessa → mecanismo → prova → preço quebra. Gera um HTML de diagnóstico. |
| 5 | **oraculo-triwer** | Mapeia o público em profundidade a partir de pesquisas reais (planilha) ou pesquisa ativa, e cadastra os perfis no Notion. |
| 6 | **sexy-triwer** | Conduz uma investigação para encontrar a "Oportunidade Sexy" — a promessa única e diferenciada do produto. |
| 7 | **prisma-triwer** | Escavação do Viés Magnético — o que faz o jeito do aluno de trabalhar ser diferente. Vira o documento "Viés Bruto Central". |
| 8 | **historias-triwer** | Comportamento contínuo (não precisa comando): detecta quando o aluno conta um caso real em qualquer conversa e oferece cadastrar. |
| 9 | **mdi-triwer** | Cruza público, histórias e promessa para preencher a Máquina de Demanda Infinita e sugerir ideias de conteúdo. |
| 10 | **carrossel-triwer** | Gera o carrossel completo (framework DOPA) usando tudo que as skills anteriores já mapearam. |
| 11 | **cta-triwer** | Decide se o carrossel leva Manychat, escolhe a isca certa e escreve os slides finais (09-10). |
| — | **notion-zettelkasten-si** | Comportamento contínuo (não precisa comando): transforma qualquer conversa em notas conectadas no Acervo Notion do aluno. |
| — | **leitura-ativa** | Comportamento contínuo (não precisa comando): processa uma leitura completa (artigo, livro, aula, podcast) em notas do Acervo — Obsidian ou Notion, à escolha do aluno — e conduz sessão socrática para transformar reflexão pessoal em notas permanentes. |

`carrossel-triwer` → `cta-triwer` é um pipeline automático (handoff direto).
As demais são independentes entre si, mas leem o que as anteriores já
registraram no Notion — rodar na ordem da tabela evita repetir perguntas.
`dexter-triwer` e `dr-house-triwer` são mutuamente exclusivas na prática:
Dexter é para quem ainda não tem produto, Dr. House para quem já tem um
produto para diagnosticar.

---

## Instalação

Três formas de instalar, dependendo de como você usa o Claude.

### O que os instaladores fazem (leia antes de rodar)

Todo instalador deste repositório (o de "tudo de uma vez" e os individuais)
só baixa arquivos de texto (`.md`, `VERSION`) deste repositório **público**
para `~/.claude/skills/<skill>/` (ou `%USERPROFILE%\.claude\skills\<skill>\`
no Windows). Nenhum deles:

- pede ou coleta credenciais;
- envia dados para qualquer lugar;
- sobrescreve `memoria.md` (seus dados pessoais dentro de cada skill).

Rodar de novo no futuro só baixa de novo os arquivos cuja versão mudou —
o instalador compara a versão instalada com a do repositório antes de
sobrescrever qualquer coisa.

Se o seu Claude (ou você) preferir inspecionar o script antes de rodar —
recomendado, e o próprio Claude Code costuma sugerir isso por padrão diante
de um comando que baixa e executa algo direto da internet — baixe primeiro
e rode depois, em vez do atalho de uma linha só:

**Mac / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-tudo-mac.sh -o instalar-tudo.sh
# leia o arquivo instalar-tudo.sh antes de rodar
bash instalar-tudo.sh
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-tudo-windows.ps1 -OutFile instalar-tudo.ps1
# leia o arquivo instalar-tudo.ps1 antes de rodar
.\instalar-tudo.ps1
```

Os comandos de uma linha só (`| bash` / `| iex`) abaixo continuam funcionando
e fazem exatamente a mesma coisa — são só um atalho para quem já confia no
repositório e não precisa inspecionar antes.

### Opção A — Tudo de uma vez (recomendado para Claude Code/Desktop)

**Mac / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-tudo-mac.sh | bash
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-tudo-windows.ps1 | iex
```

Instala (ou atualiza) as 13 skills em sequência. Rodar de novo no futuro só
atualiza o que tiver versão nova.

### Opção B — Uma skill por vez

Cada skill tem seu próprio instalador — útil se você só quer uma parte do
ecossistema. Padrão do comando:

**Mac / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-<skill>-mac.sh | bash
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-<skill>-windows.ps1 | iex
```

Troque `<skill>` por: `onboarding`, `dexter`, `drhouse`, `oraculo`, `sexy`,
`prisma`, `historias`, `mdi`, `carrossel`, `cta`, `zettelkasten`,
`leitura-ativa`. A `estilo-forge` tem instalador próprio, num caminho
diferente:

```bash
curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/estilo-forge/scripts/instalar-mac.sh | bash
```
```powershell
irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/estilo-forge/scripts/instalar-windows.ps1 | iex
```

### Opção C — claude.ai (upload manual, sem terminal)

Se você não usa Claude Code/Desktop, pode importar cada skill manualmente:

1. Baixe o `.zip` da skill desejada (pasta `dist/`, gerada com
   `scripts/empacotar-zips.ps1` ou `.sh` — ou peça o link de download direto).
2. No claude.ai: **Settings → Capabilities → Skills → Upload skill**.
3. Selecione o `.zip` baixado.
4. Repita para cada skill que quiser usar (comece sempre por
   `onboarding-triwer`).

> O formato exato aceito pela tela de Skills do claude.ai ainda não foi
> validado na prática neste projeto — se o upload falhar, tente extrair o
> `.zip` e subir apenas o `SKILL.md` junto das subpastas, ou avise para
> ajustarmos o script de empacotamento.

O instalador (Opções A e B):
- Verifica se já há uma versão instalada
- Só atualiza se houver versão mais nova
- Preserva seus dados pessoais (`memoria.md`, `iscas-local.md`) em atualizações
- Cada skill é instalada e atualizada de forma independente

---

## Atualizar

Rode de novo o mesmo comando de instalação (Opção A ou B) — o script detecta
a versão instalada e só baixa se houver uma versão mais nova.

---

## Requisitos

- **Claude Desktop**, **Claude Code** ou **claude.ai** ([claude.ai/download](https://claude.ai/download) para o app)
- **Plano pago do Claude** (Pro ou superior) — necessário para conectar o Notion via Connectors
- **Notion** com uma cópia do [Template Perfil do Aluno — Triwer](https://triwer.notion.site/Template-Perfil-do-Aluno-3588e7e25d248106b767e8eaaba3e47f?source=copy_link) — a skill `onboarding-triwer` te guia nisso
- Conexão com internet para instalar

---

## Como conectar o Notion

**Claude Desktop:**
1. Abra Configurações → Connectors (Conectores)
2. Clique em "Add Connector" e cole: `https://mcp.notion.com/mcp`
3. Autorize (OAuth) o workspace onde está sua cópia do template
Disponível nos planos Pro, Max, Team e Enterprise.

**claude.ai (navegador):**
1. Ícone de perfil (canto superior direito) → Settings → Connectors
2. "Browse connectors" → procure "Notion" → clique no "+"
3. Autorize (OAuth) e selecione o workspace/página do template

**Claude Code (terminal):**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
/mcp
```

A skill `onboarding-triwer` detecta se o Notion não está conectado e te guia
por esses mesmos passos automaticamente, na primeira vez que você usá-la.

---

## Como usar

Depois de instalar, sempre comece por:

```
/onboarding-triwer
```

Isso configura seu Notion e libera as demais skills. Ordem recomendada
depois disso:

```
estilo-forge → dexter-triwer (se ainda não tem produto) OU dr-house-triwer
(se já tem um produto para diagnosticar) → oraculo-triwer → sexy-triwer →
prisma-triwer → historias-triwer (roda sozinha, sem comando) → mdi-triwer →
carrossel-triwer → cta-triwer
```

`historias-triwer`, `notion-zettelkasten-si` e `leitura-ativa` não precisam de
comando — depois de instaladas, ficam atentas durante qualquer conversa e
oferecem agir quando fizer sentido (contar um caso real, pedir para salvar
algo no Notion, processar um artigo/livro/aula lido).

`carrossel-triwer` bloqueia a geração se "Quem sou eu" (Prisma) ou "Meu
Público" (Oráculo) ainda estiverem vazios — ele avisa e orienta qual skill
rodar primeiro.

---

## Estrutura instalada

```
~/.claude/skills/
├── onboarding-triwer/       SKILL.md, VERSION, memoria.md
├── estilo-forge/            SKILL.md, VERSION, references/
├── dexter-triwer/           SKILL.md, VERSION, references/, assets/
├── dr-house-triwer/         SKILL.md, VERSION, memoria.md, references/, assets/
├── oraculo-triwer/          SKILL.md, VERSION, memoria.md, referencias/
├── sexy-triwer/             SKILL.md, VERSION, memoria.md
├── prisma-triwer/           SKILL.md, VERSION, memoria.md
├── historias-triwer/        SKILL.md, VERSION, memoria.md
├── mdi-triwer/               SKILL.md, VERSION, memoria.md
├── carrossel-triwer/
│   ├── SKILL.md, VERSION, memoria.md
│   ├── indices/  modelos-headline.md, modelos-carrossel.md
│   ├── modelos/  mh/ MH001–MH016, mc/ MC001–MC015
│   └── referencias/  manual-headline.md, outliers-headline.md
├── cta-triwer/
│   ├── SKILL.md, VERSION, memoria.md
│   └── referencias/  iscas-regras.md, padroes-de-iscas.md, iscas-local.md
├── notion-zettelkasten-si/  SKILL.md, VERSION, memoria.md, references/
├── leitura-ativa/           SKILL.md, VERSION, memoria.md
└── estilo-[seu-nome]/       gerada pela estilo-forge
```

> `memoria.md` e `iscas-local.md` são **seus dados pessoais** — nunca
> sobrescritos em atualizações.

---

## Instalação manual (sem script)

Se preferir copiar os arquivos você mesmo:

1. Baixe ou clone este repositório
2. Copie a pasta da skill desejada para `~/.claude/skills/<nome-da-skill>/`
   (ex.: `carrossel-triwer/` → `~/.claude/skills/carrossel-triwer/`)
3. **Não sobrescreva** `memoria.md` e `iscas-local.md` se já existirem

---

## Para o mantenedor

- `scripts/empacotar-zips.ps1` / `.sh` — gera os `.zip` de cada skill em
  `dist/` (ignorado pelo git), para publicar numa Release do GitHub e
  permitir upload manual no claude.ai (Opção C acima).
- `docs/superpowers/plans/` — plano de arquitetura completo do ecossistema:
  decisões tomadas, bugs encontrados e corrigidos, e o que ainda falta.
- `obsidian-zettelkasten/` fica de fora deste repositório (tem GitHub
  próprio) — é uma ferramenta interna, não faz parte do ecossistema do aluno.

---

Feito com 🧡 pelo [Triwer](https://triwer.com.br)
