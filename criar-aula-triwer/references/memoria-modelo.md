# Memória e onboarding rápido

Lido no BOOT (passo 2). Serve para a skill não perguntar duas vezes a mesma
coisa e para aprender o gosto do expert a cada correção.

O arquivo vive em `~/.claude/skills/criar-aula-triwer/memoria.md`. Os
instaladores nunca sobrescrevem esse arquivo.

## Onboarding rápido (só se `memoria.md` não existe)

Faça as perguntas abaixo **numa mensagem só**, pulando o que já está em
`~/.claude/skills/onboarding-triwer/memoria.md` (nome, URLs do Notion) ou que o
expert já disse na conversa. Depois grave o arquivo.

1. Qual é o seu produto principal e que tipo de aula você dá nele: curso
   gravado, mentoria, comunidade, aula aberta ou live com venda?
2. Onde você registra suas aulas hoje: Notion (database "Aulas" ou página do
   módulo), uma pasta no computador ou outro lugar?
3. Você usa o MindMeister para as aulas ao vivo? (se não, o material ao vivo sai
   como roteiro em Markdown, sem o `.mind`)
4. Em que pasta devo salvar roteiros e materiais das aulas?
5. Você tem o roteiro, o mapa ou os slides de uma aula anterior para eu usar
   como referência do seu jeito de montar aula? (peça o arquivo; ele também
   alimenta o `mind-triwer`)

Descubra sem perguntar: se existe skill de estilo (`~/.claude/skills/estilo-*/SKILL.md`),
se o conector do Notion está ativo e se a skill `mind-triwer` está instalada
(`~/.claude/skills/mind-triwer/`).

## Formato do `memoria.md`

```markdown
# Memória — Criar Aula Triwer
_Última atualização: [data]_

## Perfil
- Produto principal: [nome] ([curso | mentoria | comunidade | aula aberta | live com venda])
- Usa MindMeister: [sim | não]

## Fontes e caminhos (onde achar o que a skill precisa)
- Onde ficam as aulas no Notion: [URL da database ou página do módulo | não usa]
- Pasta de roteiros e materiais: [caminho]
- Aula de referência (roteiro, mapa ou slides): [caminho]
- Banco de histórias: ver ~/.claude/skills/onboarding-triwer/memoria.md
- Skill de estilo: [estilo-nome | nenhuma]
- Identidade visual do material em HTML: [arquivo | pasta onde está documentada]

## Aulas construídas
- [data] | [tema da aula] | [ao vivo | gravada] | [versão do roteiro aprovada] | [pasta]

## Preferências registradas (aprendidas com as correções do expert)
- [data] Quando [situação], [faça X] (não [Y])

## Pendências
- [[SLOT] abertos, casos a confirmar, lacunas registradas]
```
