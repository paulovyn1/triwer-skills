# Atualização de versão: o que fazer quando a remota é mais nova

Lido no BOOT (passo 0) **só** quando a 1ª entrada do CHANGELOG publicado tem versão mais nova que o `VERSION` local.
Se as versões forem iguais ou a busca falhar, este arquivo nem é aberto.

## Remota mais nova, sem tag `[CRITICAL]`
Avisar em uma linha e seguir o BOOT normalmente, **sem bloquear**:

> Há uma versão nova da edicao-motion-triwer disponível (v[local] → v[remota]). Não é obrigatório atualizar agora, mas recomendo rodar
> o instalador quando puder.

## Remota mais nova, com tag `[CRITICAL]`
Parar o BOOT aqui. Explicar em 2 ou 3 linhas, pelo resumo da entrada do CHANGELOG, por que essa versão corrige algo importante,
e mostrar como atualizar:

- **Windows (PowerShell):**
  `irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-edicao-motion-windows.ps1 | iex`
- **Mac/Linux:**
  `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-edicao-motion-mac.sh | bash`
- **Quem baixou o .zip pela Fábrica de Conteúdos:** baixar o .zip novo e extrair por cima de
  `~/.claude/skills/edicao-motion-triwer/`.

Como a skill roda no Claude Code, oferecer rodar o comando pelo usuário (só depois de ele concordar). Aguardar a confirmação de
que atualizou antes do passo 1 do BOOT. Se ele insistir em seguir mesmo assim, atender, mas deixar claro que não é o recomendado.

Atualizar não apaga preferências, estilos próprios, `ambiente.json` nem kits de cliente: tudo isso fica fora da pasta da skill
(`~/.claude/edicao-motion-triwer/` e as skills `edicao-<cliente>`).
