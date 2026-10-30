# Memória e onboarding rápido

Lido no BOOT (passo 1). Serve para a skill não perguntar duas vezes a mesma
coisa e para aprender o gosto do expert a cada correção.

O arquivo vive em `~/.claude/skills/mind-triwer/memoria.md`. Os instaladores
nunca sobrescrevem esse arquivo.

## Onboarding rápido (só se `memoria.md` não existe)

Faça as perguntas abaixo **numa mensagem só**, pulando o que o expert já disse
na conversa ou o que a skill `criar-aula-triwer` já guardou em
`~/.claude/skills/criar-aula-triwer/memoria.md` (aula de referência, pasta de
materiais). Depois grave o arquivo.

1. Você tem um mapa mental ou slides feitos à mão por você, de uma aula
   anterior? Se tiver, me passe: é a melhor referência do seu tom (ver
   `escrita-do-no.md`).
2. Quer que o mapa use as cores da sua marca? Se sim, qual a cor principal e a
   cor de fundo clara (código hex, por exemplo `1F3A5F` e `F5F7FA`)? Se não,
   uso o cinza neutro padrão.
3. Em que pasta devo salvar os `.mind` e o `conteudo.py` de cada mapa?
4. Você já usa o MindMeister (conta gratuita serve para importar)?

Descubra sem perguntar: se o Python está disponível (`python --version`; no
Windows, `py --version`). Sem Python, avise que o `.mind` não pode ser gerado e
ofereça o outline em Markdown.

## Formato do `memoria.md`

```markdown
# Memória — Mind Triwer
_Última atualização: [data]_

## Perfil
- Nome do expert: [nome]
- Cores do mapa: PALETA = {"marca": "[hex]", "fundo": "[hex]"} (ou "padrão neutro")
- Tem conta no MindMeister: [sim | não]

## Tom do expert (traços tirados do mapa dele)
- Tamanho médio do nó: [curto | médio | longo]
- "pra" ou "para": [qual]
- Imperativo, CAPS, negrito, humor: [o que ele usa e com que frequência]
- Como rotula blocos e estudos de caso: [ex.: Situação / O que fez / Resultado]

## Fontes e caminhos (onde achar o que a skill precisa)
- Pasta dos mapas: [caminho]
- Mapa ou slides de referência: [caminho]
- Skill de estilo: [estilo-nome | nenhuma]

## Mapas gerados
- [data] | [nome do mapa] | [nº de nós] | [pasta do .mind e do conteudo.py] | [personalizado no MindMeister: sim/não]

## Preferências registradas (aprendidas com as correções do expert)
- [data] Quando [situação], [faça X] (não [Y])

## Pendências
- [[SLOT] e [PRINT] ainda abertos por mapa]
```
