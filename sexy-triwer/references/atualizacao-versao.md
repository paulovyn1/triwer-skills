# Atualização de versão — o que fazer quando a remota é mais nova

Lido no BOOT (Passo 0), **somente** quando a entrada mais recente do
CHANGELOG remoto indicar versão mais nova que o arquivo `VERSION` local.
Se as versões forem iguais ou a busca falhar, este arquivo nem é aberto.

## Remota mais nova, sem tag `[CRITICAL]`

Avise em uma linha e siga o BOOT normalmente — **não bloqueie**:

> 💡 Há uma versão nova da sexy-triwer disponível (v[local] → v[remota]).
> Não é obrigatório atualizar agora, mas recomendo rodar o instalador
> quando puder.

## Remota mais nova, com tag `[CRITICAL]`

Pare o BOOT aqui. Explique em 2-3 linhas, com base no resumo da entrada do
CHANGELOG, por que essa versão tem uma correção importante e não deve
continuar sendo usada, e informe como atualizar:

- **Claude Code/Desktop (Windows):**
  `irm https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-sexy-windows.ps1 | iex`
- **Claude Code/Desktop (Mac/Linux):**
  `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/scripts/instalar-sexy-mac.sh | bash`
- **claude.ai (Skills nativo):** baixar o `.zip` mais recente e reenviar em
  Settings → Capabilities → Skills → Upload skill.

Aguarde o aluno confirmar que atualizou antes de seguir para o passo 1 do
BOOT. Se ele insistir em prosseguir mesmo assim, atenda, mas deixe
registrado que não é o recomendado.
