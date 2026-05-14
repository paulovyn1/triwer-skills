# Triwer Skills

Skills para o Claude Desktop que criam posts de carrossel para Instagram usando o Método DOPA da Triwer.

**Versão atual:** 1.0.0

---

## O que está incluído

### carrossel-triwer
Cria posts de carrossel para o feed do Instagram seguindo o framework DOPA (Descoberta, Oportunidade, Provocação, Autoridade). Conecta com seu Notion para usar suas histórias, perfis de público e depoimentos como base de dados.

### cta-triwer
Decide se o carrossel deve ter Manychat, escolhe a isca certa e escreve os slides 09-10 finais. Especialista em criar e sugerir novas iscas quando necessário.

As duas skills são parte do mesmo pipeline — o carrossel-triwer passa o handoff para a cta-triwer automaticamente.

---

## Instalação

### Mac / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/triwer/triwer-skills/main/scripts/instalar-mac.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/triwer/triwer-skills/main/scripts/instalar-windows.ps1 | iex
```

O instalador:
- Verifica se já há uma versão instalada
- Só atualiza se houver versão mais nova
- Preserva seus dados pessoais (memória e iscas locais) em atualizações
- Instala as duas skills juntas

---

## Atualizar

Rode o mesmo comando de instalação — o script detecta a versão instalada e só baixa se houver atualização.

---

## Requisitos

- **Claude Desktop** instalado ([baixar aqui](https://claude.ai/download))
- **Plano pago do Claude** (Pro ou superior)
- **Notion** com uma cópia do [Template Triwer](https://triwer.notion.site) conectado ao Claude Desktop
- Conexão com internet para instalar

---

## Como conectar o Notion

1. Abra o Claude Desktop
2. Vá em **Configurações → Integrações**
3. Ative o **Notion** e autorize o acesso ao workspace onde está sua cópia do template
4. Reinicie o Claude Desktop

---

## Como usar

Após instalar, abra o Claude Desktop e digite:

```
/carrossel-triwer
```

Na primeira vez, o onboarding iniciará automaticamente para configurar seu ambiente.

---

## Estrutura instalada

```
~/.claude/skills/
├── carrossel-triwer/
│   ├── SKILL.md
│   ├── VERSION
│   ├── memoria.md                  ← criado no onboarding
│   ├── indices/
│   │   ├── modelos-headline.md
│   │   └── modelos-carrossel.md
│   ├── modelos/
│   │   ├── mh/  MH001–MH016
│   │   └── mc/  MC001–MC015
│   └── referencias/
│       ├── manual-headline.md
│       └── outliers-headline.md
│
└── cta-triwer/
    ├── SKILL.md
    ├── VERSION
    ├── memoria.md                  ← criado no onboarding
    └── referencias/
        ├── iscas-regras.md
        ├── padroes-de-iscas.md
        └── iscas-local.md          ← seus dados pessoais
```

> `memoria.md` e `iscas-local.md` são **seus dados pessoais** — nunca sobrescritos em atualizações.

---

## Instalação manual

Se preferir instalar sem o script:

1. Baixe ou clone este repositório
2. Copie a pasta `carrossel-triwer/` para `~/.claude/skills/carrossel-triwer/`
3. Copie a pasta `cta-triwer/` para `~/.claude/skills/cta-triwer/`
4. **Não sobrescreva** `memoria.md` e `iscas-local.md` se já existirem

---

Feito com 🧡 pelo [Triwer](https://triwer.com.br)
