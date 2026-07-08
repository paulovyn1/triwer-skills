# Configurar conector do Notion

Use este arquivo apenas quando o Passo 2 do BOOT detectar que o Notion não
está conectado. Na maioria das sessões o Notion já está conectado (onboarding
já feito) e este arquivo nunca precisa ser lido.

Exiba ao aluno:

> ⚠️ **Notion não conectado**
>
> Esta skill precisa do conector do Notion ativo para ler e gravar no seu
> Notion pessoal.
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
>
> Depois de conectar, volte e me avise para eu continuar.

Aguarde confirmação. Esta skill não funciona sem o Notion — a promessa
precisa ser salva na subpágina do produto.
