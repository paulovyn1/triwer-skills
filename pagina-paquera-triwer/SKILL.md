---
name: pagina-paquera-triwer
description: >
  Constrói a página de vendas do produto paquera do aluno (produto de entrada,
  ticket baixo, como e-book, guia, kit ou mini curso, vendido com desconto de
  lançamento): coleta os insumos, escreve a copy no modelo Pitstop, aprova com o
  aluno e monta a página com seções, imagens e animações, em HTML único ou
  React, conforme o nível dele. Use quando o aluno pedir "página do meu
  e-book", "página de vendas do produto paquera", "landing do meu guia",
  "página do livro", "copy e página do meu produto de entrada" ou quiser
  transformar um produto barato em página pronta. NÃO usar para lançamento
  pago com evento (pagina-vendas-lancamento-pago), mentoria high ticket ou
  página de captura gratuita.
compatibility: Claude Code, claude.ai, Claude Desktop
metadata: "v1.0.0, outubro 2026. Histórico em CHANGELOG.md."
---

# Página Paquera Triwer

O produto paquera é a porta de entrada da esteira: barato, rápido de comprar,
feito para a pessoa provar o método do expert antes de qualquer oferta maior.
A página dele tem um trabalho só: fazer alguém que ainda não conhece o expert
confiar o suficiente para pagar pouco agora. Isso pede prova concreta, promessa
clara e uma página bonita o bastante para parecer de quem sabe o que faz.

Você conduz o processo inteiro em cinco fases. Cada fase termina com algo que o
aluno vê e aprova antes da próxima. Copy aprovada não é reescrita em silêncio, e
design não começa sem copy aprovada, porque mudar texto depois do layout pronto
custa o dobro.

Idioma: português brasileiro. O texto da página sai na voz do expert (o aluno),
em primeira pessoa. Se o aluno tiver uma skill de estilo própria (por exemplo
`estilo-[nome]`), use-a. Nunca use a voz de outra pessoa.

---

## Fase 0. Onde estou e com quem estou falando

Antes de qualquer pergunta sobre o produto, descubra duas coisas:

1. **Ambiente.** Se você tem ferramentas de arquivo e terminal (Claude Code), dá
   para criar o projeto, otimizar imagens e tirar prints da página para revisar.
   Se está no chat (claude.ai), a entrega é um arquivo HTML para baixar.
2. **Nível técnico do aluno.** Pergunte de forma simples se ele já mexeu com
   código, Node ou hospedagem, ou se prefere receber um arquivo que abre com dois
   cliques. Use a resposta e o ambiente para propor o formato, explicando o
   porquê em uma frase. Detalhes de cada formato em `references/formatos.md`.

Regra prática: no claude.ai ou com aluno que nunca programou, vá de HTML único.
Projeto React só no Claude Code e só se o aluno (ou quem vai implementar) souber
rodar `npm`.

Anote o modo escolhido. Daqui em diante, nas fases 4 e 5, leia **só** o arquivo
do modo escolhido: `references/modo-html.md` ou `references/modo-react.md`. Não
abra o do outro modo, porque instrução de um formato aplicada no outro quebra a
página (caminho de imagem, componente que não existe, comando que o aluno não
tem).

---

## Fase 1. Coleta

Junte tudo antes de escrever. Copy boa nasce de prova específica, e prova
específica não se inventa.

**Do Notion do aluno (Workspace de Aluno), se o conector estiver ativo.** Busque
por nome dentro do hub dele e leia só o que precisa:
- **Quem sou eu**: viés, história, frases dele, pontas em aberto.
- **Meu Público**: perfis por estágio (Frio, Morno, Quente) e as falas reais.
- **Histórias Inevitáveis**: resultados, conquistas, crenças, com número e desfecho.
- **Depoimentos**: prova social. Se estiver vazio, anote. Não preencha com nada.
- **Produtos**: a ficha do produto paquera (ticket, promessa) e da oferta maior.
- **Permanentes**: procure regras do próprio aluno, como uma regra de
  confidencialidade (por exemplo, nunca citar o nome da empresa junto com um
  número). Essas regras valem acima da copy.

Sem Notion, faça uma entrevista curta e objetiva. As perguntas estão em
`references/coleta.md`.

**Do produto em si.** Peça o arquivo (PDF, link, sumário). Em arquivo grande,
leia o início (capa, prefácio, sumário, sobre o autor) e o fim (conclusão,
próximos passos). O meio só se o aluno autorizar, e avise que as descrições de
capítulo vão precisar de validação dele. Confira se o nome do produto bate entre
capa, arquivo e ficha. Nome divergente é a primeira pergunta.

**Da oferta.** Confirme com o aluno, sem supor:
- preço de lançamento e preço de referência (a ancoragem precisa ser real);
- se existe bônus de verdade (se não existir, a seção sai ou fica marcada);
- qual oferta vem depois da compra (mentoria, curso). Ela vai para a página de
  obrigado, não para esta página, porque oferta maior aqui distrai da compra
  barata;
- garantia e prazo (7 dias é o mínimo legal para compra online);
- links de checkout e WhatsApp, se já existirem.

**Do modelo de página.** Se o aluno tiver um modelo próprio ou uma página
real que já vende (a dele ou de referência), leia antes de escrever. A estrutura
padrão está em `references/estrutura-copy.md`.

Feche a fase com um resumo curto do que você tem e do que falta.

---

## Fase 2. Copy

Escreva seguindo `references/estrutura-copy.md` (ordem das seções e o que cada
uma faz) e `references/estilo-copy.md` (como soa). Leia os dois antes de
começar.

O que não pode faltar:
- **Headline na fórmula do modelo**: verbo de transformação + resultado, um
  facilitador ("com o passo a passo de quem...") e uma separação clara ("separado
  por fases", "por cargo", "por semana"). Ofereça 2 alternativas para teste.
- **Subheadline de validação**: "Validado por..." ou equivalente, com prova real.
- **Prova só com fonte**: todo número vem do Notion, do produto ou de uma fonte
  pública citada no rodapé da seção. Sem fonte, não entra.
- **Um bloco de conta**: mostre em número quanto custa continuar no problema
  (é a seção que vira calculadora interativa no design). Dados de mercado só com
  fonte nomeada.
- **Pendências visíveis**: o que falta fica entre [colchetes] na copy, nunca
  preenchido com suposição.

Entregue a copy em um arquivo (markdown) e, se o aluno usa Notion, ofereça salvar
como página nova no banco que ele indicar. Abaixo do texto da página, inclua um
bloco "Notas de produção (não publicar)" com pendências, divergências encontradas
e regras aplicadas.

**Revisão com o aluno.** Ele vai editar. Quando ele editar direto no Notion ou no
arquivo, leia a versão dele antes de mexer de novo e preserve as mudanças dele.
Cada rodada de ajuste vira versão nova (v2, v3...). A anterior fica intacta,
porque texto aprovado perdido custa retrabalho. Se precisar alterar uma página
que ele mexeu, faça uma cópia de segurança antes.

Só siga para o design quando o aluno disser que a copy está aprovada.

---

## Fase 3. Identidade e insumos visuais

A página veste a identidade **do aluno**, nunca uma identidade padrão. Siga
`references/identidade-visual.md`. Em resumo:

- Tire as cores da capa do produto e da logo dele (fundo, cor de destaque, cor de
  alerta). Se ele mudar uma cor da logo, a cor de destaque da página muda junto.
- Fontes: use as da marca só se a licença permitir uso comercial na web. Fonte
  "Personal Use" ou "Demo" não vai para página de venda. Escolha uma gratuita
  parecida (Google Fonts) e avise.
- Peça as fotos do expert (de preferência em contexto do trabalho dele), a capa
  do produto em imagem, a logo (de preferência SVG) e, se der, prints de páginas
  internas do produto.
- Confira as fotos contra as regras do aluno: crachá, logo de empresa ou tela com
  dado sensível podem quebrar uma regra de confidencialidade dele.
- Se faltarem prints internos, monte prévias desenhadas a partir do sumário e
  avise que elas devem ser trocadas pelos prints reais.

---

## Fase 4. Montagem da página

Leia `references/layout-secoes.md` (o desenho de cada seção, as animações e as
regras de celular, iguais nos dois modos) e depois o arquivo do modo escolhido,
que diz como construir.

A copy aprovada entra como está. Se o layout pedir um texto que não existe na
copy (um rótulo de seção, um selo), ele precisa ser neutro e sem promessa nova.
Nada de preço no hero se a copy não pôs.

---

## Fase 5. Revisão visual e entrega

**Confira antes de mostrar**, em desktop (1440px) e celular (360px e 412px),
usando `references/checklist-qualidade.md`. Ali estão os erros que já
aconteceram de verdade: palavras grudadas em título animado, destaque na palavra
errada, aba ativa invisível, elemento lateral em cima do texto, mockup cobrindo o
rosto do expert no celular. Se você tem terminal, tire prints e olhe cada um
(o arquivo do modo diz como). Sem terminal, diga ao aluno o que conferir no
celular dele e peça um print se algo parecer estranho.

**Entregue** a página no formato do modo (o arquivo do modo diz o que vai no
pacote), salva onde o aluno indicar, e a lista do que ainda falta (links,
depoimentos de leitores, prints, CNPJ).

Ajustes depois da entrega seguem a mesma regra da copy: leia o estado atual,
mude só o que foi pedido, confira com print, entregue de novo.

---

## Regras que valem o processo inteiro

- **Nunca inventar número, depoimento, preço de referência ou bônus.** Prova
  inventada derruba a confiança que a página inteira tenta construir, e o aluno
  responde por ela.
- **Provas sempre específicas**: número exato, prazo, desfecho. "Muitos alunos"
  não prova nada.
- **Motivação privada do aluno não entra na página.** Medos, dores pessoais ou o
  motivo de ele querer vender são contexto para você, não argumento de venda.
- **Sem travessão** (— ou –) em nenhum texto produzido. Use vírgula, dois pontos
  ou ponto.
- **A oferta maior fica para depois da compra.**
- **Uma versão nova nunca apaga a anterior.**
