# Ficha de Produto — Schema do Notion

> Este arquivo documenta a estrutura exata da página de produto no Notion do
> aluno (Template Perfil do Aluno — Triwer). Use-o sempre que precisar criar
> ou atualizar uma Ficha de Produto — nunca tente inferir campos por nome
> genérico, use os nomes exatos abaixo.

---

## Localizar o produto

A partir de `produtos_db_url` (da memória local desta skill), faça um query
na database para encontrar o produto pelo nome:

```
GET https://api.notion.com/v1/databases/{produtos_db_url_id}/query
Body: { "filter": { "property": "Nome", "title": { "contains": "[nome do produto]" } } }
```

- **Se retornar resultado:** a página do produto já existe — abra pelo `id`
  retornado e atualize os campos (ver seções abaixo).
- **Se não retornar resultado:** crie uma página nova na database com `Nome`
  igual ao nome do produto diagnosticado (ver "Criar página nova" abaixo).

---

## Propriedades da database (campos do card no board/tabela)

Estas propriedades ficam no nível da database — preencha via `properties`
ao criar ou atualizar a página:

| Nome exato no Notion | Tipo       | O que o Dr. House preenche                                   |
|----------------------|------------|--------------------------------------------------------------|
| `Nome`               | title      | Nome do produto/serviço diagnosticado                        |
| `Ticket`             | number     | Preço como número (ex: 497 — sem R$, sem ponto de milhar)   |
| `Página de vendas`   | url        | URL da página de vendas, se o aluno informou                 |
| `Palavras-chave`     | multi_select | Palavras-chave da linha editorial, se coletadas             |
| `Ativo?`             | checkbox   | `true` se o produto está sendo vendido ativamente            |

> **Relations** (Histórias, Anotações, Conteúdos, Depoimentos, Ferramentas,
> MDI, Módulos, Projetos, Iscas, Permanentes): **não preencha** estas
> propriedades — são alimentadas por outras skills (historias-triwer,
> carrossel-triwer etc.) e requerem IDs de páginas que o Dr. House não tem.

---

## Corpo da página — seções e campos inline

O corpo de cada página de produto segue uma estrutura de tabelas e callouts
dividida em 4 seções fixas. Ao criar uma página nova, replique esta estrutura.
Ao atualizar uma existente, localize o bloco correto por título de seção e
atualize apenas os callouts/células relevantes.

### Seção `— I D E N T I D A D E`

Tabela de 2 colunas (Campo | Valor). Linhas e campos exatos:

| Campo (coluna 1 — não editar) | O que o Dr. House preenche                                        |
|-------------------------------|-------------------------------------------------------------------|
| `Promessa`                    | A promessa principal coletada no Bloco 3 (Fase 1)                |
| `Sub-promessa`                | Detalhe ou extensão da promessa, se houver                       |
| `Ticket`                      | Valor formatado como texto (ex: "R$ 497") — diferente da property |
| `Formato`                     | Curso / Mentoria / Consultoria / Workshop / Comunidade / outro    |
| `Link da página de vendas`    | URL completa, se o aluno informou                                 |

**Como atualizar:** localize a tabela após o `heading_2` com texto
`"- I D E N T I D A D E"` e edite as células da coluna 2 (índice 1) de
cada linha — nunca edite a coluna 1 (são os rótulos fixos).

### Seção `— T R A N S F O R M A Ç Ã O`

Dois callouts em colunas lado a lado:

| Callout               | O que o Dr. House preenche                                          |
|-----------------------|---------------------------------------------------------------------|
| `Cenário passado:`    | Como o público se sente ANTES do produto — coletado no Bloco 2    |
| `Cenário futuro:`     | Como o público se sente DEPOIS, com o resultado — Bloco 3/promessa |

**Como atualizar:** localize o `column_list` após o `heading_2`
`"- T R A N S F O R M A Ç Ã O"` e edite o rich_text de cada callout.
Preserve o texto do rótulo (`Cenário passado:` / `Cenário futuro:`) como
parte do callout — acrescente o conteúdo depois do rótulo, não substitua.

### Seção `— G A N C H O S`

Dois callouts em colunas lado a lado:

| Callout          | O que o Dr. House preenche                                          |
|------------------|---------------------------------------------------------------------|
| `Maior dor:`     | O que trava o lead hoje — foco técnico. Bloco 2 (Público)          |
| `Maior desejo:`  | O que o lead quer sentir ou ter — foco técnico. Bloco 2/3          |

**Como atualizar:** mesma mecânica da seção Transformação — localize o
`column_list` após o `heading_2` `"- G A N C H O S"`.

### Seção `— L I N H A E D I T O R I A L`

Parágrafo de texto livre logo abaixo dos dois callouts de exemplo. Liste
as palavras-chave separadas por vírgula. Coletadas a partir do diagnóstico
geral (critérios de mecanismo e promessa).

**Como atualizar:** localize o `paragraph` com texto `"Liste as palavras-chave
aqui, separadas por vírgula"` e substitua pelo conteúdo real.

---

## Criar página nova

Quando o produto não existir na database, crie com:

```json
{
  "parent": { "database_id": "[id da produtos_db_url]" },
  "properties": {
    "Nome": { "title": [{ "text": { "content": "[nome do produto]" } }] },
    "Ticket": { "number": [valor numérico] },
    "Página de vendas": { "url": "[URL ou null]" },
    "Ativo?": { "checkbox": true }
  }
}
```

Depois de criar a página, adicione os blocos do corpo replicando a estrutura
das seções acima (Identidade → Transformação → Ganchos → Linha Editorial).
Use o template da Ficha do Produto como referência de estrutura — não invente
blocos fora desta estrutura.

---

## Regras de atualização

1. **Nunca sobrescreva campos já preenchidos com inferência** — só preencha o
   que a escavação real revelou. Se um campo não foi coletado na conversa,
   deixe em branco.
2. **Nunca use `replace_content`** na página de produto — use edição pontual
   de bloco a bloco (`PATCH /v1/blocks/{block_id}`).
3. **Não preencha as relations** (Histórias, MDI, Conteúdos etc.) — são
   gerenciadas por outras skills que têm os IDs corretos.
4. **Sempre apresente ao aluno o que será gravado** antes de gravar e aguarde
   confirmação — mesma regra do onboarding-triwer.
5. Se o produto encontrado na database já tiver campos preenchidos, atualize
   apenas os que a sessão atual revelou algo novo ou diferente — não toque
   no que não mudou.
