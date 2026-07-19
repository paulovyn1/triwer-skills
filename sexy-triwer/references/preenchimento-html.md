# Preenchimento do template HTML — Página de resultado

Lido na Etapa 8/13, quando for de fato montar o HTML final. O resultado
desta skill é sempre entregue como página HTML, nunca como texto puro na
conversa — nunca como Claude Artifact, em nenhuma hipótese (ver Etapa 8 e
REGRAS ESTRUTURAIS no SKILL.md).

## Template-base

`~/.claude/skills/sexy-triwer/assets/template-oportunidade-sexy.html`. Parta
sempre desse arquivo — nunca gere a página do zero. **Copie o arquivo via
comando de terminal para o destino final — não o leia inteiro.** O bloco
`<style>` tem centenas de linhas de CSS que não precisam entrar no contexto;
o comando de cópia duplica tudo sem custo de token. Depois de copiado, edite
só os placeholders `[[CAMPO]]` no arquivo de destino.

## Fidelidade obrigatória

O bloco `<style>` do template (cores, fontes, nomes de classe) é a
identidade visual Triwer, a mesma usada pelo `dr-house-triwer`. Nunca altere
variáveis de cor, fontes, espaçamento ou crie classes novas. Só o conteúdo
textual muda.

## Preenchimento campo a campo

Substitua cada `[[CAMPO]]` pelos dados desta sessão (mesmos campos da Etapa
13, incluindo `[[FORMATO_PRODUTO]]` e `[[PAPEL_ESTEIRA]]` definidos na Etapa
3, e `[[PILAR_DOMINANTE]]`, `[[URGENCIA_COMPRA]]` e `[[NIVEL_CONSCIENCIA]]`
definidos na Etapa 5). Repita blocos `.achado.forte` quantas vezes forem
necessárias para os itens de `ativos_marketing_sexys` (Etapa 10 — narrativa
que reforça a oportunidade, não exibição de credencial) e demais provas
coletadas. Se não houver prova social coletada nesta sessão, remova a seção
`#provas` inteira em vez de deixar o campo vazio.

**Seção `#ativos`** — cada item de `ativos_marketing_sexys` é um parágrafo
corrido, nunca campos separados: preenche `[[ATIVO_N_TEXTO]]` com o texto em
prosa já pronto (formato definido em `ativos-gerador.md` — nomeia a
categoria em linguagem natural, explica o porquê, dá a instrução prática,
tudo amarrado). Mínimo 2 blocos, sem teto. Quando um mesmo fato-fonte render
mais de 1 uso (ver `ativos-gerador.md`), cada uso é seu próprio bloco
`[[ATIVO_N_TEXTO]]`, não fundidos num só. Se o funil de Ativos não bateu o
piso de 2, substitua a seção pelos itens de sugestão ("o que reforçaria a
oportunidade, ainda não disponível hoje"), deixando claro que são sugestões,
não ativos prontos.

**`[[VERSAO_SKILL]]` no rodapé** — preencha sempre com o conteúdo do arquivo
`VERSION` desta skill lido no BOOT (Passo 0), não com a versão que o aluno
pensa ter, nem com um número fixo. Isso permite identificar, em qualquer
output reportado depois, se o problema já foi corrigido em versão mais nova
ou se o aluno estava desatualizado no momento da geração.

**Headlines (`#headlines`)** — cada uma preenche dois campos separados, não
um só: `[[HEADLINE_N_MODELO]]` (ex.: "MH004 — Autoridade:") e
`[[HEADLINE_N_TEXTO]]` (o texto da headline entre aspas). Nunca junte os
dois num campo único de novo — o `<li>` do `.numlist` depende dessa
separação em dois elementos (`.headline-modelo` e `.headline-texto`) para
renderizar cada um em sua própria linha.

**Seção `#subpromessa` é condicional** — só inclua no HTML final se
`papel_esteira` = Estrela (a Etapa 6 exige subpromessa nesse caso). Nos
demais papéis, remova a `<section id="subpromessa">` inteira **e** o link
correspondente no `<nav class="anchor-bar">` — nunca deixe link morto no
menu nem seção com `[[SUBPROMESSA]]` vazio.

**`[[BIO_INSTAGRAM]]`** — preenche com `bio_instagram` (Etapa 11): a bio
aprovada, ou, se reprovada 2x (Etapa 11, passo 6), a v2 com aviso visível de
"a confirmar com você" e a crítica do Verificador junto, nunca apresentada
como se fosse a versão final. O template ainda não tem placeholder nem
seção visual dedicados para Bio — até esse trabalho de template ser feito,
inclua a bio como bloco de texto simples dentro de `#provas` ou seção
equivalente já existente, sem inventar CSS novo.

**`[[DESTAQUES_INSTAGRAM]]`** — preenche com `destaques_instagram` (Etapa
11, segundo artefato): a lista de títulos aprovada, ou, se algum título
ficou reprovado 2x, marcado como "a confirmar com você" junto da crítica do
Verificador, mesma regra da Bio. O template também não tem placeholder nem
seção visual dedicados para Destaques — até isso ser feito, inclua a lista
como bloco de texto simples logo abaixo da bio, na mesma seção `#provas` ou
equivalente, sem inventar CSS novo. A ausência de placeholder no template
não dispensa incluir o conteúdo no HTML — só dispensa a formatação visual
dedicada.

## Regras sem exceção

- Nunca deixe `[[CAMPO]]` sem preencher no HTML final — é um marcador de
  template, não um placeholder visível para o aluno.
- Entrega: gere um HTML autocontido (sem dependências externas além das
  fontes do Google Fonts já referenciadas) e entregue sempre como arquivo
  real — nunca como Claude Artifact, em nenhuma hipótese.
