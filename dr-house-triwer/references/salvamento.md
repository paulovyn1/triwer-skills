# Salvar no Notion do aluno

> Leia este arquivo só quando chegar na Fase 4 (depois de gerar o HTML). Não carregue
> no início da sessão — não é necessário para conduzir a escavação nem para escrever o
> diagnóstico, e só ocupa espaço de contexto à toa até este momento.

## Por que salvar

A conversa com o Dr. House frequentemente revela informação nova sobre o aluno que não
estava registrada em lugar nenhum — uma história que ele contou de passagem, um perfil de
público mais preciso do que o que já estava escrito, um detalhe do produto que não estava
cadastrado. Se essa informação só existir dentro desta conversa, ela se perde. Depois de
entregar o HTML, salve o que for novo ou mais preciso no Workspace de Aluno dele.

## Como encontrar o Workspace de Aluno

**Correção (02/07/2026):** a versão anterior deste arquivo lia o `CLAUDE.md` do
projeto do aluno para achar o Notion, e navegava ao vivo por Acervo → Referências
buscando notas por título aproximado. Isso tinha dois problemas: `CLAUDE.md` não
existe em claude.ai (quebra a skill para quem não usa Claude Code/Desktop), e as
4 URLs necessárias **já são resolvidas uma vez pelo `onboarding-triwer`** — não
precisa buscar de novo a cada diagnóstico.

Use a memória local desta skill (populada no BOOT, Passo 1):

- `quem_sou_eu_url` → nota de identidade/viés ("Quem sou eu" / "Viés Bruto
  Central", preenchida pela skill `prisma-triwer`)
- `historias_db_url` → database "Histórias Inevitáveis"
- `meu_publico_db_url` → database "Meu Público"
- `produtos_db_url` → database "Produtos"

**Se alguma dessas URLs não estiver na memória:** não tente adivinhar o
workspace nem navegar por título — peça a URL diretamente ao aluno, ou oriente
a rodar `/onboarding-triwer` se nenhuma URL foi resolvida ainda.

## O que atualizar, e como reconhecer cada nota

**Nota de identidade/viés** (`quem_sou_eu_url`)
Atualize apenas se a conversa revelou algo novo sobre como o aluno descreve o que faz de
diferente — não duplique o que já está lá. Acrescente, não substitua, a menos que o que
já existe esteja claramente desatualizado em relação ao que o aluno acabou de dizer.
Esta página é território de escrita da skill `prisma-triwer` — trate como
complemento pontual, não reescrita.

**Base de histórias** (`historias_db_url`)
Se o aluno contou algum caso real, com resultado específico (um cliente, um resultado
próprio, uma prova mencionada no Bloco 7 da escavação) que ainda não está registrado
nessa base, adicione como entrada nova — seguindo a mesma estrutura de campos que a
skill `historias-triwer` usa (Conflito/Fundo do poço, Decisão contraditória,
Resultado inesperado, Dados brutos). Não reescreva histórias já existentes — só
adicione o que é genuinamente novo.

**Database de perfis de público** (`meu_publico_db_url`)
Se a escavação revelou uma descrição de público mais precisa do que a que já está
registrada (situação específica, não só demografia), atualize ou adicione. Se o produto
testado revelou que o aluno estava misturando perfis diferentes — isso também é
informação valiosa para registrar, mesmo que seja um "problema encontrado", não só um
dado novo.

**Database de produto** (`produtos_db_url`)
Se o produto diagnosticado nesta sessão ainda não está cadastrado, ou está desatualizado
em relação ao que foi descrito na escavação (preço, formato, entregáveis), atualize.

## Como escrever a atualização

Use `notion-update-page` com `command: update_content` para inserções pontuais
(search-and-replace de um trecho específico) sempre que possível — evite `replace_content`
em página que já tem conteúdo do aluno, para não apagar histórico por engano. Use
`replace_content` apenas quando a nota inteira for nova ou estiver vazia.

Ao adicionar conteúdo novo (história, perfil, dado de produto), marque a origem:

```
> Adicionado em [data de hoje] a partir de uma sessão com o Dr. House.
```

Isso ajuda o aluno (ou você mesmo, numa sessão futura) a distinguir o que veio de
diagnóstico do que ele escreveu manualmente.

## Se a skill notion-zettelkasten-si estiver disponível

Se o aluno tiver a skill `notion-zettelkasten-si` instalada no workspace dele, use-a para
criar as notas novas (histórias, perfis) em vez de escrever diretamente com
`notion-create-pages` — ela aplica o padrão de formatação e conexão que o restante do
workspace do aluno já segue. Se a skill não estiver disponível, escreva diretamente com
as ferramentas Notion, seguindo a estrutura das notas já existentes na mesma base como
referência de formato.

## O que não fazer

- Não salve nada antes de entregar o HTML ao aluno — o salvamento é o último passo, não
  paralelo à Fase 3.
- Não crie nota duplicada quando já existir uma nota próxima do mesmo tema — atualize a
  existente.
- Não invente conteúdo para preencher uma nota vazia além do que a conversa realmente
  revelou.
- Se não encontrar a base de Referências ou qualquer uma das notas esperadas, não pare o
  processo inteiro — avise o aluno no que não foi possível salvar automaticamente e
  entregue essa parte como texto para ele colar manualmente.
