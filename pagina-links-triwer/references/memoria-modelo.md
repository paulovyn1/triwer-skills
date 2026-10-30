# Memória e onboarding rápido

Lido no BOOT (passo 1). Serve para a skill não perguntar duas vezes a mesma
coisa e para aprender o gosto do aluno a cada correção.

O arquivo vive em `~/.claude/skills/pagina-links-triwer/memoria.md`. Os
instaladores nunca sobrescrevem esse arquivo.

## Onboarding rápido (só se `memoria.md` não existe)

Faça as perguntas abaixo **numa mensagem só**, pulando o que já está em
`~/.claude/skills/onboarding-triwer/memoria.md` (nome, Instagram, pasta de
fotos) ou que o aluno já disse na conversa. Depois grave o arquivo.

1. Como você quer aparecer na página: nome e @ do Instagram?
2. Você já mexeu com código ou hospedagem, ou prefere um arquivo que abre com
   dois cliques? (define HTML único ou React, ver `formatos.md`)
3. Onde essa página vai ficar: Vercel, no site que você já tem, ou ainda não sabe?
4. Onde ficam seus materiais: a pasta com logo, fotos e cores da marca (caminho
   no computador ou link do Drive)? Se ainda não tem, a gente define as cores
   na Fase 4.

Descubra sem perguntar: se existe skill de estilo (`~/.claude/skills/estilo-*/SKILL.md`)
e se o conector do Notion está ativo.

## Formato do `memoria.md`

```markdown
# Memória — Página de Links Triwer
_Última atualização: [data]_

## Perfil
- Nome na página: [nome]
- Instagram: [@arroba]
- Nível técnico: [iniciante | já usa Node/hospedagem]
- Formato preferido: [HTML único | React]
- Onde a página fica: [Vercel | site próprio | indefinido]

## Fontes e caminhos (onde achar o que a skill precisa)
- Materiais da marca (logo, fotos, cores): [caminho ou link]
- Pasta onde salvar as páginas: [caminho]
- Notion do aluno: ver ~/.claude/skills/onboarding-triwer/memoria.md
- Skill de estilo: [estilo-nome | nenhuma]
- Página de vendas de referência (mesma marca): [caminho ou link]

## Entregas feitas
- [data] | [nome da página] | [pasta/arquivo] | [link publicado]

## Preferências registradas (aprendidas com as correções do aluno)
- [data] Quando [situação], [faça X] (não [Y])

## Pendências
- [links "#" ainda sem destino, imagens provisórias]
```
