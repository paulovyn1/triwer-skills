# Aula ao vivo (live, aula aberta, imersão com pitch)

Detalha as etapas 4 e 7 do SKILL.md quando a aula é ao vivo e tem venda no meio.

## Ordem de trabalho

Construir a aula nesta progressão. Cada etapa só começa quando a anterior foi validada pelo expert.

**1. Perguntar antes de escrever qualquer bloco** (de uma vez, numa mensagem só):
- O que o participante precisa ver, entender e sair fazendo ao final da aula? Pedir a lista de objetivos em ordem. Esses objetivos viram o mapa de tempo: cada bloco tem que cumprir pelo menos um
- Como você faz isso hoje no seu negócio? A resposta vira o bloco "como eu faço" e organiza o passo a passo
- Qual aula veio antes? O que ela já cobriu sai do escopo, mas confirmar o recorte com o expert: não cortar uma parte do tema por suposição
- Qual produto entra no pitch e qual é o conceito central dele?
- Quais números reais existem para o bastidor (resultado de uma ação, de um funil, de uma campanha)?
- A aula vai entregar estratégias prontas para copiar?

**2. Reconciliar as fontes** (etapas 1 a 3 do SKILL.md), conferindo todo caso no banco de histórias do expert.

**3. Roteiro de fala em Markdown, em versões.** Entregar a v1 rápido, com `[SLOT]` onde falta dado e no máximo 4 perguntas objetivas no fim. Cada correção do expert gera uma versão nova (`-v2`, `-v3`), nunca sobrescreve a anterior. No fim de cada versão, listar o que mudou, as decisões tomadas por ele e o que falta. Uma pergunta de pressão por versão, mostrando onde a tese pode quebrar.

**4. Material de referência antes do mapa.** Pedir a transcrição e o mapa (ou slides) de uma aula anterior do expert e comparar: o que da fala entrou no material, por quê, e como replicar. Se a skill `mind-triwer` já tiver uma referência de estilo salva para este expert, ler antes de pedir de novo.

**5. Mapa mental** pela skill `mind-triwer`, a partir do roteiro aprovado.

**6. Depois que o expert sobe e personaliza o mapa**, mudança nova entra como ramo separado (ver `mind-triwer`), nunca como mapa regerado.

**7. Pitch por último**, só depois da aula aprovada, lendo o material da oferta nessa hora.

**8. Registro**: planejamento no Notion (etapa 5), aprendizados (etapa 6) e histórias novas no banco de histórias assim que aparecerem na conversa.

## Sequência fixa de 7 movimentos

| # | Movimento | O que precisa acontecer |
|---|---|---|
| 1 | Promessa com história | A promessa entra de forma natural, através de uma história real que faz a pessoa reconhecer o próprio problema. Preferir história do próprio expert |
| 2 | Contexto de mercado | Por que o problema existe para todo mundo agora. Usar o timing do ano quando houver (Black Friday, janeiro, planejamento) |
| 3 | Por que isso acontece | 3 a 5 causas paralelas, nenhuma culpando a pessoa. A última causa planta o conceito central do produto do pitch, sem desenvolver |
| 4 | Como eu faço no meu negócio | Bastidor em 1ª pessoa, com número real. Se o expert descrever como faz hoje, essa descrição vira este bloco e organiza o passo a passo inteiro |
| 5 | Passo a passo, primeira parte | Cada passo tem o PORQUÊ, não só a ação. O porquê é o que dá valor ao método |
| 6 | Pitch | Entra no meio do passo a passo, depois de um "Imagine" que mostra a vida com a solução funcionando |
| 7 | Continua o conteúdo | Os passos restantes, com o mesmo nível de valor de antes do pitch. A aula não vira só pitch |

Fechamento: volta para a história de abertura e termina com uma tarefa de 24 horas. Nada de frase de efeito no fechamento.

## A ponte para o pitch

- A aula sempre amarra no conceito central do produto vendido. Perguntar ao expert qual é esse conceito se não estiver claro (ex.: "ter uma oferta tão específica que a pessoa não encontra igual em outro lugar")
- Plantar esse conceito antes, como a última causa do bloco 3, e retomar na ponte usando uma história que já apareceu na aula. Uma história contada pela metade no início e concluída na ponte funciona bem
- A oferta aparece cedo na abertura, como informação ("vou abrir uma condição especial durante a aula"), nunca como pitch
- O pitch e as condições só são escritos depois que o expert aprovar a aula

## Histórias

- Espalhar histórias por todos os blocos, contadas de forma natural, nunca em bloco separado de "cases"
- Antes de usar qualquer caso, confirmar quem é a pessoa, de onde vieram os dados e se é história do expert ou de cliente
- Nunca atribuir a um caso uma origem que a fonte não confirma
- Número que falta vira `[SLOT: ...]` visível no material, nunca estimativa

## Escrita

- Sem frase de efeito inventada. A história e o dado fecham o ponto. Frases que o expert já usa podem ficar
- Sem instrução de ferramenta quando a aula é de método
- WhatsApp e qualquer contato ativo: só com quem deu permissão

## Estratégias prontas para copiar (opcional)

Quando a aula promete compartilhar as melhores estratégias do expert, entregar em formato que o participante copia sem adaptar: um cronograma dentro do bloco "na prática". Perguntar ao expert se a aula leva isso; não é obrigatório.

- Agrupar por frequência: **Toda semana**, **Em todo fluxo**, **A cada X dias, no mínimo**, **Sempre que acontecer**
- Cada item é uma ação com frequência explícita ("Stories com automação, pelo menos 1x por semana"), nunca um conceito
- Quando existir print do bastidor, deixar um nó `[PRINT]` embaixo do item
- Perguntar ao expert quais estratégias entram e com que frequência. Nunca inventar a frequência
- Usar os nomes internos do método do expert quando ele usar, com a tradução no nó filho

## Material da aula: mapa mental, não roteiro

O material que o expert usa ao vivo é um mapa mental do MindMeister, gerado pela skill `mind-triwer`. O roteiro de fala em Markdown serve para aprovação do conteúdo antes do mapa.

**Vai para o mapa:**
- A tese em uma linha
- Número exato com escopo, sem hesitação
- Estudo de caso em movimentos rotulados (Situação / O que fez / Resultado), quando o caso prova o método
- Combinados e logística que o expert lê em voz alta
- A oferta como informação, na abertura

**Fica só na fala:**
- O detalhe da história que prova a tese (o mapa carrega só a linha que dispara a lembrança)
- Humor, digressões, leitura do chat, perguntas para a audiência

A ordem do mapa é a ordem exata da fala.

**Tamanho:** um mapa de 1 hora de aula tem cerca de 140 nós. Acima de ~200 nós, avisar o expert que algum bloco vai ficar corrido e sugerir onde cortar.
