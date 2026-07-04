# estilo-forge

Fábrica de skills de estilo personalizado para o Claude.

O **estilo-forge** não escreve texto — ele **cria uma skill que escreve como você**. Ele analisa textos reais escritos por você, extrai padrões de linguagem, raciocínio e estrutura, e gera uma skill personalizada (`estilo-[seunome]`) que o Claude usa para escrever na sua voz em qualquer projeto.

---

## Como funciona

O processo tem 7 etapas guiadas:

1. **Onboarding** — explica o processo completo
2. **Coleta de corpus** — você reúne textos reais escritos por você (~3.000 palavras ou 10 textos)
3. **Validação** — o corpus é avaliado antes de qualquer análise (volume, variedade, autenticidade)
4. **Análise profunda** — mapeamento de todas as dimensões do seu estilo, com evidências reais
5. **Separação de camadas** — camada universal anti-IA + camada do seu estilo individual
6. **Geração da skill** — sua skill `estilo-[nome]` é criada e instalada em `~/.claude/skills/`
7. **Validação** — textos de teste até você reconhecer a própria voz

---

## Instalação

**Mac / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/paulovyn1/estilo-forge/main/scripts/instalar-mac.sh | bash
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/paulovyn1/estilo-forge/main/scripts/instalar-windows.ps1 | iex
```

O instalador:
- Verifica se já há uma versão instalada
- Só atualiza se houver versão mais nova
- Nunca toca nas skills `estilo-[nome]` que você já gerou

> **Dica:** você também pode simplesmente colar o comando acima numa conversa do Claude Code e pedir: *"instala essa skill pra mim"*. O Claude executa o instalador automaticamente.

---

## Atualizar

Rode o mesmo comando de instalação — o script detecta a versão instalada e só baixa se houver uma versão mais nova.

---

## Requisitos

- **Claude Code** ou **Claude Desktop** instalado ([baixar aqui](https://claude.ai/download))
- **Plano pago do Claude** (Pro ou superior)
- Conexão com internet para instalar

---

## Como usar

Após instalar, abra uma nova conversa e digite:

```
/estilo-forge
```

O onboarding inicia automaticamente. Você também pode acionar com frases como:
- "quero que o Claude escreva como eu"
- "captura meu jeito de escrever"
- "cria um Estilo-[Nome]"

Ao final do processo, sua skill pessoal estará disponível com:

```
/estilo-[seunome]
```

---

## Estrutura instalada

```
~/.claude/skills/
├── estilo-forge/
│   ├── SKILL.md
│   ├── VERSION
│   └── references/
│       ├── analysis-framework.md
│       ├── skill-template.md
│       └── universal-anti-ia.md
│
└── estilo-[seunome]/            ← gerada pelo forge, é só sua
    └── SKILL.md
```

> As skills `estilo-[nome]` geradas são **suas** — nunca são sobrescritas ou alteradas por atualizações do estilo-forge.

---

## Instalação manual

Se preferir instalar sem o script:

1. Baixe ou clone este repositório
2. Copie `SKILL.md`, `VERSION` e a pasta `references/` para `~/.claude/skills/estilo-forge/`

---

Feito com 🧡 pelo [Triwer](https://triwer.com.br)
