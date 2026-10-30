# Memória e onboarding rápido

Lido no BOOT (passo 1). Serve para a skill não perguntar duas vezes a mesma
coisa e para aprender o gosto do aluno a cada correção.

O arquivo vive em `~/.claude/skills/pagina-ticket-medio-triwer/memoria.md`. Os
instaladores nunca sobrescrevem esse arquivo.

## Onboarding rápido (só se `memoria.md` não existe)

Faça as perguntas abaixo **numa mensagem só**, pulando o que já está em
`~/.claude/skills/onboarding-triwer/memoria.md` (nome, Instagram, pasta de
fotos, URLs do Notion) ou que o aluno já disse na conversa. Depois grave o arquivo.

1. Como você quer aparecer na página: nome do expert e @ do Instagram?
2. Você já mexeu com código, Node ou hospedagem, ou prefere um arquivo que abre
   com dois cliques? (define HTML único ou React, ver `formatos.md`)
3. Onde a página vai ficar e onde você vende: Vercel, site próprio ou ainda não
   sabe? E o checkout: Hotmart, Kiwify, Eduzz, outra ou ainda não tem?
4. Onde ficam seus materiais: pasta com logo, fotos suas e capa do produto
   (caminho no computador ou link do Drive)?
5. Como você fala com o seu leitor ("tu" ou "você") e existe algo que nunca pode
   aparecer na página (nome da empresa onde trabalha, crachá, número de cliente)?

A referência de estrutura, a garantia, o parcelamento e os bônus **não** entram
aqui: mudam a cada produto e são perguntados na Fase 0 e na Fase 1 toda vez.

Descubra sem perguntar: se existe skill de estilo (`~/.claude/skills/estilo-*/SKILL.md`)
e se o conector do Notion está ativo.

## Formato do `memoria.md`

```markdown
# Memória — Página Ticket Médio Triwer
_Última atualização: [data]_

## Perfil
- Nome do expert: [nome]
- Instagram: [@arroba]
- Nível técnico: [iniciante | já usa Node/hospedagem]
- Formato preferido: [HTML único | React]
- Hospedagem: [Vercel | site próprio | indefinido]
- Plataforma de checkout: [nome | ainda não tem]
- Tratamento com o leitor: [tu | você]
- Quem implementa depois: [o próprio aluno | dev | agência]

## Regras do aluno (valem acima da copy)
- [ex.: nunca citar o nome da empresa junto com número]

## Fontes e caminhos (onde achar o que a skill precisa)
- Materiais da marca (logo, fotos, capa): [caminho ou link]
- Pasta onde salvar copy e página: [caminho]
- Notion do aluno: ver ~/.claude/skills/onboarding-triwer/memoria.md
- Skill de estilo: [estilo-nome | nenhuma]
- Páginas de referência já estudadas: [link | print]

## Entregas feitas
- [data] | [produto] | [versão da copy] | [pasta/arquivo/zip] | [link publicado]

## Preferências registradas (aprendidas com as correções do aluno)
- [data] Quando [situação], [faça X] (não [Y])

## Pendências
- [checkout, WhatsApp, CNPJ, link da VSL, depoimentos, fonte dos números de mercado]
```
