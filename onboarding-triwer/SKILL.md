---
name: onboarding-triwer
description: >
  Configura o Notion pessoal do aluno como segundo cérebro Triwer: conecta o
  Notion, orienta a duplicar (ou duplica via MCP quando possível) o Template
  Perfil do Aluno, personaliza a página inicial (nome, foto, Instagram, pasta de
  fotos no Drive), resolve e salva as URLs essenciais do Notion (Dados
  Essenciais, Quem sou eu, Meu Público, Histórias Inevitáveis, Produtos, MDI,
  Central de Conteúdo) na memória de todas as skills Triwer já instaladas, e
  encaminha para a skill de estilo (Forge). Use esta skill sempre que o aluno
  instalar as skills Triwer pela primeira vez, disser "onboarding", "configurar
  meu Notion", "primeira vez usando", ou quando qualquer outra skill Triwer
  detectar que o onboarding ainda não foi feito. Deve ser a primeira skill
  Triwer executada por qualquer aluno — todas as outras dependem dela.
compatibility: Claude Desktop, Claude Code, claude.ai
metadata: "v1.1.1 — julho 2026 — adiciona verificação automática de versão no BOOT (ver CHANGELOG.md). v1.1 — julho 2026 — resolve iscas_db_url, mdi_db_url, conteudos_db_url"
---

# Onboarding Triwer

> **Skill desenvolvida pela Triwer.**
> Instalação: `~/.claude/skills/onboarding-triwer/`
>
> Esta skill não gera conteúdo. Ela prepara o terreno para todas as outras —
> resolve e grava, uma única vez, tudo que as demais skills Triwer precisam para
> não ficar procurando no Notion a cada uso.
>
> **Skills do ecossistema que dependem desta:** `estilo-forge`, `oraculo-triwer`,
> `sexy-triwer`, `prisma-triwer`, `historias-triwer`, `mdi-triwer`,
> `carrossel-triwer`, `cta-triwer`, `dr-house-triwer`, `notion-zettelkasten-si`.
>
> **Base de dados:** Notion (Template Perfil do Aluno — Triwer). Cada aluno tem
> sua própria cópia conectada via MCP do Notion.

---

## REGRA GERAL DE LEITURA DE ARQUIVOS

**Memória** (`memoria.md`) → lida sempre no boot, se existir.
**Notion** → lido por partes: primeiro para localizar/validar páginas (títulos),
nunca o conteúdo inteiro de uma página antes de precisar editá-la.
**Este arquivo não tem `indices/` nem `referencias/`** — todo o processo está
contido no próprio `SKILL.md`, por ser um fluxo único e não repetido a cada
sessão.

---

## BOOT — EXECUTAR SEMPRE AO INICIAR

### Verificação de versão (antes do Passo 1)

Leia o arquivo `VERSION` desta skill (sibling do `SKILL.md`) — essa é a
versão local. Em seguida, tente buscar
`https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/onboarding-triwer/CHANGELOG.md`
com a ferramenta de acesso à web disponível no ambiente atual (`WebFetch` no
Claude Code/Desktop; navegação/busca nativa no claude.ai). Se não conseguir
acessar (sem internet, sem ferramenta, timeout etc.), não mencione nada e
siga para o Passo 1.

Se conseguir, leia a entrada mais recente (primeira do arquivo) do CHANGELOG
remoto e compare com a versão local:
- **Igual:** siga para o Passo 1 sem dizer nada.
- **Remota mais nova, sem tag `[CRITICAL]`:** avise em uma linha, ex.: "💡 Há
  uma versão nova da onboarding-triwer disponível (v[local] → v[remota]). Não
  é obrigatório atualizar agora, mas recomendo rodar o instalador quando
  puder." Depois siga para o Passo 1 normalmente — **não bloqueie**.
- **Remota mais nova, com tag `[CRITICAL]`:** pare aqui. Explique em 2-3
  linhas, com base no resumo da entrada do CHANGELOG, por que essa versão
  tem uma correção importante e não deve continuar sendo usada, e informe
  como atualizar:
  - **Claude Code/Desktop:** `irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-onboarding-windows.ps1 | iex` (Windows) ou `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-onboarding-mac.sh | bash` (Mac/Linux).
  - **claude.ai (Skills nativo):** baixar o `.zip` mais recente e reenviar
    em Settings → Capabilities → Skills → Upload skill.
  Aguarde o aluno confirmar que atualizou antes de seguir para o Passo 1. Se
  ele insistir em prosseguir mesmo assim, atenda, mas deixe registrado que
  não é o recomendado.

### Passo 1 — Verificar memória

Tente ler `~/.claude/skills/onboarding-triwer/memoria.md`.

- **Se existir e tiver `onboarding_completo: true`:** o aluno já passou pelo
  onboarding. Exiba:

  ```
  Você já concluiu a configuração inicial em [data da última atualização].

  Quer refazer algum ponto específico? Posso atualizar:
  1. Foto, nome ou Instagram da home
  2. Pasta de fotos do Drive
  3. Reconectar/reresolver as URLs do Notion (se você mudou algo na estrutura)

  Ou digite "tudo" para refazer o processo completo.
  ```

  Execute apenas a parte escolhida, reaproveitando o restante já salvo. Não peça
  de novo o que já está confirmado, a menos que o aluno peça explicitamente.

- **Se não existir:** é o primeiro uso. Vá para o **FLUXO DE ONBOARDING** abaixo.

---

## FLUXO DE ONBOARDING — EXECUTAR NO PRIMEIRO USO (ou quando o aluno pedir "tudo")

### E1 — Apresentação

```
Oi! Sou a skill de Onboarding da Triwer. Vou te ajudar a configurar seu Notion
como o seu segundo cérebro — a base que todas as outras skills Triwer vão usar
para gerar conteúdo com a sua cara, não genérico.

Isso leva uns 5-10 minutos e só precisa ser feito uma vez. Vamos lá?
```

### E2 — Verificar conexão com o Notion

Tente uma busca simples com a ferramenta `notion`.

- **Se disponível:** confirme internamente e siga para E3.
- **Se não disponível:** exiba o texto-padrão de conexão do Notion:

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

  Aguarde confirmação do aluno antes de prosseguir. Não siga sem o Notion
  conectado — nenhuma etapa seguinte funciona sem ele.

### E3 — Duplicar o Template Perfil do Aluno

Pergunte:

```
Você já duplicou o Template Perfil do Aluno da Triwer para o seu Notion?
```

- **Se sim:** peça a URL da página principal da cópia dele. Valide tentando
  acessá-la. Se inválida ou inacessível, explique o motivo mais provável (ex.:
  "object not found" quase sempre significa que a página não foi compartilhada
  com o conector — oriente a abrir a página no Notion, clicar em "•••" → "Add
  connections" → selecionar o conector do Claude) e peça novamente.

- **Se não:** primeiro tente duplicar automaticamente. Verifique se alguma
  ferramenta disponível do conector Notion faz duplicação/cópia de página
  (`duplicate`, `copy page` ou equivalente). Se existir e funcionar, use a URL do
  template abaixo como origem:

  ```
  https://triwer.notion.site/Template-Perfil-do-Aluno-3588e7e25d248106b767e8eaaba3e47f?source=copy_link
  ```

  **Se a ferramenta não existir ou a duplicação falhar** (mais provável — a API
  pública do Notion não costuma expor duplicação de página compartilhada por
  link entre workspaces diferentes), caia no fluxo manual:

  ```
  Para configurar seu Notion, você precisa ter sua própria cópia do template.

  1. Acesse: https://triwer.notion.site/Template-Perfil-do-Aluno-3588e7e25d248106b767e8eaaba3e47f?source=copy_link
  2. Clique em "Duplicate" (Duplicar) no canto superior direito
  3. Escolha o seu workspace do Notion como destino
  4. Depois de duplicar, cole aqui a URL da sua cópia
  ```

  Aguarde a URL. Valide antes de prosseguir.

Registre a URL validada como `notion_base_url`.

### E4 — Resolver a estrutura interna do Notion

Dentro de `notion_base_url`, localize a subpágina **"Dados Essenciais"** (vem
incluída no template). Leia seu conteúdo uma vez — não releia depois.

"Quem sou eu" e "Meu Público" normalmente não ficam fisicamente dentro de "Dados
Essenciais" — aparecem como **links/menções** para páginas que vivem em outro
ponto da estrutura: dentro de "Acervo" → "📚 Referências", como itens marcados
`Tipo: 🔓 Essencial` (achado confirmado pela skill `notion-zettelkasten-si`,
que navega essa mesma estrutura em profundidade). Para cada link de menção
encontrado, abra a página/database referenciada e identifique pelo título:

- página **"Quem sou eu"** → registre a URL real como `quem_sou_eu_url`
- database **"Meu Público"** → registre a URL real como `meu_publico_db_url`

Além disso, localize (a partir da página principal ou de "Dados Essenciais",
seguindo os links de menção do mesmo jeito) e registre:

- database **"Histórias Inevitáveis"** → `historias_db_url`
- database **"Depoimentos"** → `depoimentos_db_url`
- database **"Produtos"** → `produtos_db_url`
- dentro de "Central de ativos", a database **"Iscas gerais"** → `iscas_db_url`
- dentro de "[MDI] Máquina de Demanda Infinita", a database embutida
  **"MDI — BASE GERAL"** → `mdi_db_url`
- database **"Conteúdos"** (linkada pela relation "Conteúdos" da MDI) →
  `conteudos_db_url`
- página **"Central de Conteúdo"** → `central_conteudo_url`

Registre também `dados_essenciais_url`.

**Se "Dados Essenciais" não for encontrada, ou algum dos links acima não
existir:** pergunte ao aluno diretamente pela URL que faltou, uma de cada vez,
em vez de travar o processo inteiro por causa de uma página só. Marque a que
faltou como pendente no `memoria.md` (ver E6) em vez de bloquear o restante.

### E5 — Personalizar a página inicial

```
Agora vou personalizar a home do seu Notion. Preciso de algumas informações:
```

1. **Nome:** "Como você quer que seu nome apareça na página inicial?" →
   atualize o título/campo de nome da home com `notion_base_url`.
2. **Foto:** oriente a trocar manualmente — a API do Notion normalmente não
   permite upload de imagem arbitrária a partir de um arquivo local do aluno:

   ```
   Troque a foto de capa/perfil da sua home pela sua foto — é só clicar na
   imagem atual e fazer upload da sua. Pode fazer isso a qualquer momento,
   não precisa ser agora.
   ```

3. **Instagram:** "Qual é o seu @ do Instagram?" → atualize o campo/link
   correspondente na home com o valor informado (aceite com ou sem "@").
4. **Pasta de fotos no Drive:**

   ```
   Você já tem uma pasta no Google Drive com fotos suas para produção de
   conteúdo?
   ```

   - **Se sim:** peça o link e substitua no campo correspondente da home.
   - **Se não:**

     ```
     Sem problema. Crie agora uma pasta nova no seu Google Drive (pode chamar
     de "Fotos — Conteúdo"), cole o link dela aqui. Não precisa estar cheia
     ainda — você vai alimentando aos poucos, e ela vai servir de banco de
     imagens fácil de acessar quando for produzir conteúdo.
     ```

   Aguarde o link antes de seguir. Registre como `drive_fotos_url`.

**Antes de gravar qualquer uma dessas mudanças no Notion, apresente um resumo e
peça confirmação:**

```
Vou atualizar sua home do Notion com:
- Nome: [nome]
- Instagram: [@arroba]
- Pasta de fotos: [URL do Drive]

Confirma?
```

Só grave após "sim".

### E6 — Salvar memória própria

Crie `~/.claude/skills/onboarding-triwer/memoria.md`:

```markdown
# Memória — Onboarding Triwer
_Última atualização: [data]_

onboarding_completo: true

## Aluno
- Nome: [nome]
- Instagram: [@arroba]
- Drive de fotos: [URL]

## Notion — URLs essenciais
- Página principal: [notion_base_url]
- Dados Essenciais: [dados_essenciais_url]
- Quem sou eu: [quem_sou_eu_url]
- Meu Público (DB): [meu_publico_db_url]
- Histórias Inevitáveis (DB): [historias_db_url]
- Depoimentos (DB): [depoimentos_db_url]
- Produtos (DB): [produtos_db_url]
- Iscas gerais (DB): [iscas_db_url]
- MDI — Base Geral (DB): [mdi_db_url]
- Conteúdos (DB): [conteudos_db_url]
- Central de Conteúdo: [central_conteudo_url]

## Pendências
- [qualquer URL não resolvida em E4, para retomar depois]
```

### E7 — Propagar as URLs para as demais skills Triwer instaladas

Verifique quais pastas existem em `~/.claude/skills/` cujo nome termina em
`-triwer` (ex.: `carrossel-triwer`, `cta-triwer`, `oraculo-triwer` etc. — apenas
as que já estiverem instaladas nesta máquina/conta).

Para cada uma:

- Se já existir um `memoria.md` naquela pasta, abra e atualize (ou crie) a
  seção `## Configuração do Notion` com as mesmas URLs salvas em E6 — sem
  apagar nenhuma outra seção já existente naquele arquivo (preferências,
  histórico de iscas etc. pertencem a cada skill, não mexa nelas).
- Se a pasta existir mas ainda não tiver `memoria.md`, crie um `memoria.md`
  mínimo só com a seção `## Configuração do Notion`.

Isso evita que cada skill precise resolver essas URLs sozinha no primeiro uso
dela — a única coisa que falta a partir daqui é o dado específico daquela
skill (ex.: histórico de iscas, na `cta-triwer`).

### E8 — Encaminhar para o próximo passo

```
Pronto! Seu Notion está configurado. A partir de agora, as outras skills
Triwer vão usar essas informações direto, sem precisar te perguntar de novo.

Próximo passo recomendado: crie sua skill de tom de voz, rodando
/estilo-forge. Ela analisa seus textos reais e ensina o Claude a escrever como
você — não como IA genérica. Leva uns 15-20 minutos, mas só precisa ser feito
uma vez, e todo conteúdo gerado pelas outras skills Triwer vai usar essa voz.

Quer rodar agora ou prefere deixar para depois?
```

Se o aluno quiser deixar para depois, registre como pendência no `memoria.md`
(seção "Pendências") e não insista nas próximas execuções desta skill — quem
lembra o aluno disso é o próprio `carrossel-triwer`, na hora de gerar conteúdo
sem tom de voz definido.

---

## REGRAS QUE NÃO MUDAM

| # | Regra | O que falha quando ignorada |
|---|---|---|
| 1 | Nunca gravar nada no Notion sem antes mostrar ao aluno o que vai ser escrito e esperar confirmação | Aluno perde controle sobre o próprio Notion |
| 2 | Nunca inventar uma URL — se não resolver sozinha, perguntar direto ao aluno | Skills seguintes gravam no lugar errado |
| 3 | Nunca tentar contornar a autenticação OAuth do Notion — cada aluno precisa autorizar manualmente | O conector Notion não suporta token fixo; tentar automatizar isso não funciona e confunde o aluno |
| 4 | `onboarding_completo: true` só é gravado ao final do fluxo completo, nunca em passo intermediário | Outra skill leria onboarding como concluído estando pela metade |
| 5 | Ao propagar URLs (E7) para outras skills, nunca sobrescrever seções que não sejam "Configuração do Notion" | Apagaria preferências e histórico específicos daquela skill |
| 6 | Pasta de fotos do Drive pode ficar vazia — só o link é obrigatório agora | Trava o onboarding por um requisito que é gradual por natureza |

---

## HANDOFF — PARA A PRÓXIMA SKILL

Esta skill não tem handoff estruturado em JSON (não gera conteúdo a ser
consumido diretamente por outra skill). O que ela entrega é o `memoria.md`
próprio e propagado (E6/E7) — as demais skills leem isso no próprio BOOT delas.

---

## INSTALAÇÃO

### Estrutura de pastas

```
~/.claude/skills/onboarding-triwer/
├── SKILL.md
├── VERSION
└── memoria.md                        ← criado automaticamente no primeiro uso
```

### Mac/Linux

```bash
BASE=~/.claude/skills/onboarding-triwer
mkdir -p $BASE

cp SKILL.md $BASE/
cp VERSION $BASE/
```

### Windows

```powershell
$BASE = "$env:USERPROFILE\.claude\skills\onboarding-triwer"
New-Item -ItemType Directory -Force -Path $BASE

Copy-Item SKILL.md $BASE\
Copy-Item VERSION $BASE\
```

### Após instalar

1. Conecte o Notion no seu cliente Claude (Desktop, claude.ai ou Claude Code —
   instruções completas dentro da própria skill, seção E2)
2. Abra uma nova conversa e digite `/onboarding-triwer`
3. Siga o fluxo — leva de 5 a 10 minutos
