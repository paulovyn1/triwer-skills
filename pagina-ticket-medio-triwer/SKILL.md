---
name: pagina-ticket-medio-triwer
description: >
  Constrói a página de vendas de um produto de ticket médio (curso gravado,
  programa ou mentoria em grupo de R$ 100 a R$ 1.000) com VSL no topo: estuda a
  página de referência do aluno, coleta os insumos, escreve a copy (preço só na
  ancoragem, botões de resultado, etapas, bônus, garantia), aprova com o aluno,
  monta a página (HTML único ou React, conforme o nível dele) na identidade
  dele, publica na Vercel e entrega o zip para quem vai implementar. Use quando o aluno pedir "página de vendas do meu
  curso", "página do produto de ticket médio", "landing do meu curso gravado",
  "página na estrutura dessa referência", "página com VSL" ou "faz uma página
  igual a essa", mesmo sem citar ticket médio. NÃO usar para produto paquera de
  ticket baixo (pagina-paquera-triwer), lançamento pago com evento
  (pagina-vendas-lancamento-pago), high ticket consultivo, página de links
  (pagina-links-triwer) ou captura gratuita.
compatibility: Claude Code, claude.ai e Claude Desktop (React exige terminal)
metadata: "v1.2.0, outubro 2026. Histórico em CHANGELOG.md."
---

# Página Ticket Médio Triwer

O produto de ticket médio pede mais convencimento que o paquera e menos que a
high ticket: o lead frio paga algumas centenas de reais sem conversar com
ninguém. A página faz isso em camadas: o lead se reconhece, vê prova, entende
por que está travado, conhece o método, vê tudo que leva, só então vê o preço, e
não corre risco. Pular uma camada ou mostrar o preço cedo faz o lead decidir sem
saber o que compra.

Você conduz o processo em seis fases (de 0 a 5). Cada fase termina com algo que o aluno vê
e aprova antes da próxima. Copy aprovada não é reescrita em silêncio, e o design
não começa sem copy aprovada, porque mudar texto depois do layout pronto custa o
dobro.

Idioma: português brasileiro. O texto da página sai na voz do expert (o aluno),
em primeira pessoa. Se ele tiver uma skill de estilo própria (`estilo-[nome]`),
use-a. Nunca use a voz de outra pessoa.

---

## BOOT, executar sempre ao iniciar

0. **Verificação de versão:** leia o arquivo `VERSION` desta skill (sibling do `SKILL.md`), que é a versão local. Tente buscar `https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/pagina-ticket-medio-triwer/CHANGELOG.md` com a ferramenta de acesso à web do ambiente. Se não conseguir acessar, não mencione nada e siga. Se a entrada mais recente do CHANGELOG remoto for igual à local, siga sem dizer nada. **Só se a remota for mais nova:** leia e siga `references/atualizacao-versao.md`.
1. **Memória:** leia `~/.claude/skills/pagina-ticket-medio-triwer/memoria.md`, se existir. Ela guarda o perfil do aluno, as regras dele, onde estão os arquivos, as páginas já entregues e as preferências aprendidas nas correções. Se não existir, rode o onboarding rápido de `references/memoria-modelo.md` (uma mensagem só) e crie o arquivo.
2. **Notion do aluno (opcional):** leia `~/.claude/skills/onboarding-triwer/memoria.md`, se existir com `onboarding_completo: true`. Dali saem nome, Instagram, pasta de fotos e as URLs do Notion (Quem sou eu, Meu Público, Histórias, Depoimentos, Produtos). Não pergunte de novo o que já está lá. Sem o onboarding, siga sem Notion e use a entrevista curta de `references/coleta.md`.

---

## Fase 0. Onde estou e o que o aluno quer copiar

Confira a memória primeiro e só pergunte o que não estiver lá.

1. **Ambiente e nível do aluno.** Com ferramentas de arquivo e terminal (Claude
   Code) dá para montar, compilar, olhar a página no navegador e publicar. No
   chat (claude.ai) a entrega é um arquivo HTML para baixar. Pergunte de forma
   simples se o aluno já mexeu com código, Node ou hospedagem, ou se prefere um
   arquivo que abre com dois cliques.
2. **Formato.** Proponha **HTML único** (claude.ai ou aluno que nunca programou) ou
   **projeto React** (só Claude Code, só se o aluno ou quem implementa souber
   rodar `npm`), explicando o porquê em uma frase. Detalhes em
   `references/formatos.md`. Anote o modo escolhido: nas fases 4 e 5 leia **só**
   o arquivo do modo (`references/modo-html.md` ou `references/modo-react.md`).
   Instrução de um formato aplicada no outro quebra a página (caminho de imagem,
   componente que não existe, comando que o aluno não tem).
3. **Referência.** Pergunte qual página o aluno quer usar de estrutura (link ou
   print). **Estude por screenshot, nunca só por texto**, seguindo
   `references/referencia-estrutura.md`. O erro mais comum é reaproveitar o
   esqueleto de uma página antiga do próprio expert quando o aluno queria a
   estrutura da referência. Se ele não tem referência,
   proponha a estrutura de 17 blocos da tabela desse arquivo.
4. **Quem implementa depois.** Pergunte quem vai receber o zip (dev do aluno,
   sócio, agência). Isso muda só a entrega, não a montagem.

---

## Fase 1. Coleta

Junte tudo antes de escrever, seguindo `references/coleta.md` (Notion do aluno
se o conector estiver ativo, entrevista curta se não).

Três itens da oferta nunca podem ser supostos, porque cada um já virou erro
real: **garantia em dias** (a ficha do produto dizia um prazo, o aluno confirmou
outro, e o errado apareceu em vários lugares da página), **parcelamento** (12 parcelas somando mais que o à vista só fecha se
o checkout cobra juros) e **valores de referência dos bônus**. Pergunte, anote
a resposta do aluno e use essa, mesmo que um briefing diga outra coisa.

Feche a fase com um resumo do que você tem e do que falta.

---

## Fase 2. Copy

Escreva seguindo `references/estrutura-copy.md` (ordem das seções e regras de
conteúdo) e `references/estilo-copy.md` (tratamento tu/você, tom). Leia os dois
antes de começar.

As regras que mais pesam, e o porquê de cada uma, estão no topo de
`estrutura-copy.md`: preço só na ancoragem, botões de resultado e não de método,
nome do método só depois de apresentado, terceira pessoa só na seção do criador,
garantia com um número só, nada de motivação privada do aluno. Releia essa lista
antes de entregar.

Headline, subheadline e qualquer frase que o aluno ditar entram **exatamente**
como ele escreveu. Pendências ficam entre [colchetes], nunca preenchidas com
suposição. Prova sem fonte não entra.

Entregue a copy em um arquivo (markdown), com um bloco "Notas de produção (não
publicar)" no fim (pendências, números sem fonte, divergências, regras do aluno
aplicadas). Se o aluno usa Notion, ofereça salvar como **página nova** no banco
que ele indicar; nunca sobrescreva uma página já entregue. Cada rodada de ajuste
vira versão nova (v2, v3...) e a anterior fica intacta.

Quando o aluno editar, leia a versão dele antes de mexer de novo e preserve as
mudanças. Só siga para o design quando ele disser que a copy está aprovada.

---

## Fase 3. Identidade e insumos visuais

A página veste a identidade **do aluno**. Siga `references/identidade-visual.md`:
tokens a partir da logo e da capa, fontes com licença comercial, degradê de um
tom só, fotos do expert, e o cuidado com crachá, logo de empresa e dados que
quebrem uma regra de confidencialidade dele (por exemplo, a empresa atual).

Peça: logo (SVG de preferência), fotos do expert em contexto de trabalho, capa do
produto se houver, e confirme os nomes de empresas que podem aparecer.

---

## Fase 4. Montagem

Leia `references/layout-secoes.md` (o que cada seção faz e as armadilhas) e o
arquivo do modo escolhido: `references/modo-html.md` (parte de
`assets/template-pagina.html`) ou `references/modo-react.md` (parte de
`assets/react-kit/`). Nos dois, o modelo é uma página inteira que funciona,
escrita com texto de exemplo anonimizado entre [colchetes]: troque tudo pela copy
aprovada e rode `scripts/conferir-restos.py` antes de mostrar qualquer coisa.

A copy aprovada entra como está. Os rótulos fixos que já vêm no modelo estão
no tratamento "tu": passe para o tratamento do aluno (`memoria.md`) ou troque
pela copy. Se o layout pedir um texto que não existe na
copy (rótulo de seção, selo), ele precisa ser neutro e sem promessa nova nem
preço.

---

## Fase 5. Revisão e entrega

**Confira antes de mostrar**, em 1440px, 412px e 360px, com
`references/checklist-qualidade.md` (há itens específicos do modo HTML). Ali estão os erros que já aconteceram:
preço fora da ancoragem, palavras grudadas em título animado, "Tu" empilhado,
menu ilegível sobre painel escuro, garantia com dias diferentes em lugares
diferentes. Use o navegador (Claude in Chrome) ou `scripts/prints.mjs` e olhe
cada tela. Sem terminal, diga ao aluno o que conferir no celular dele.

**Publique só se o aluno pedir.** Siga `references/publicacao.md`: Vercel sem
instalar nada, confirmação do endereço de produção, zip com
`scripts/empacotar.py` e LEIA-ME de `assets/LEIA-ME-modelo.md`. Devolva ao
aluno o caminho exato do zip, o link publicado e a lista do que falta (checkout,
WhatsApp, CNPJ, link da VSL, depoimentos, fonte dos números de mercado).

Ajustes depois da entrega: leia o estado atual, mude só o pedido, procure o item
no projeto inteiro (um pedido de uma palavra costuma estar em vários lugares),
recompile, confira, entregue de novo.

---

## Aprender com as correções do aluno

A skill evolui com o gosto de quem a usa. Tudo o que vale para as próximas páginas fica em `memoria.md`:

- **Registrar preferência.** Quando o aluno corrigir, recusar ou pedir um ajuste que se aplicaria de novo (tom da copy, tratamento "tu"/"você", cor, animação, seção que ele nunca quer, palavra que ele não usa), grave uma linha em "Preferências registradas": `[data] Quando [situação], [faça X] (não [Y])`. Avise em uma frase: "Anotei na sua memória: [regra]. Se não quiser que eu lembre disso, é só avisar." Ajuste de uma página só ("troca essa foto") não vira regra.
- **Aplicar.** Antes de escrever ou montar qualquer coisa, releia as preferências e siga. Elas valem mais que os padrões deste arquivo e das referências, menos as "Regras que valem o processo inteiro": se o aluno pedir algo que quebre uma delas (inventar número, preço fora da ancoragem), explique e não aplique.
- **Guardar caminhos e regras.** Quando o aluno disser onde algo está (pasta de materiais, página de referência, link publicado) ou uma regra dele (o que nunca pode aparecer), grave em "Fontes e caminhos", "Regras do aluno" ou "Entregas feitas" e confira ali antes de pedir de novo.
- **Nunca gravar** telefone, e-mail, senha, token, CPF/CNPJ ou dado de cliente. Só caminhos, gostos e regras.
- **Contradição.** Se uma preferência nova contradiz uma antiga, atualize a antiga e avise.
- **Fecho de cada entrega.** Atualize "Entregas feitas", "Pendências" e a data de atualização.

---

## Regras que valem o processo inteiro

- **Nunca inventar número, depoimento, preço de referência, bônus ou prazo de
  garantia.** Prova inventada derruba a confiança que a página tenta construir,
  e o aluno responde por ela.
- **Preço só na ancoragem**, nunca em topo, hero, botão ou meta description.
- **Provas sempre específicas**: número exato, prazo, desfecho.
- **Motivação privada do aluno não entra na página.**
- **Sem travessão** (— ou –) em nenhum texto produzido.
- **Estrutura da referência manda sobre páginas antigas do aluno.**
- **Uma versão nova nunca apaga a anterior.**
