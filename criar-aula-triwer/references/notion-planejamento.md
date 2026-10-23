# Notion: registro do planejamento da aula

Detalha a etapa 5 do SKILL.md. Só se aplica se o expert usa Notion.

## Onde registrar

Pergunte ao expert onde ficam as aulas do produto dele (uma database "Aulas", uma página do módulo, outro lugar). Se ele colar o link de uma aula existente, use `notion-fetch` nela: a resposta mostra a hierarquia e as propriedades que a database usa. Nunca crie uma database nova sem confirmar.

Ao criar uma página nova, siga as propriedades das aulas vizinhas na mesma database. Leia pelo menos uma aula existente antes, para não inventar propriedade.

## O que vai na página (nunca no material do participante)

- **Conteúdo completo por bloco**, com o contexto de raciocínio
- **Pendências** em lista numerada
- **Contradições resolvidas** durante a pesquisa, com o porquê da decisão
- **Dados brutos** ainda não processados, preservados na íntegra

Nada disso vai para o material final. O Notion carrega processo; o material carrega só o que foi validado.

## `update_content` vs. `replace_content`

- **`update_content`** (busca e substitui) exige que o trecho antigo bata caractere a caractere com o que está salvo. O Notion reformata tabelas, listas e aspas, então trechos longos costumam falhar com "No matches found".
- **`replace_content`** substitui a página inteira. Mais confiável para tabelas, várias seções ou reorganização.

Para corrigir uma frase isolada, use `update_content` com o texto exato lido via `notion-fetch`. Para qualquer reestruturação, use `replace_content`.
