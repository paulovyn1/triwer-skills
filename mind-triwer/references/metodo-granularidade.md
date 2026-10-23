# Método de granularidade: como um mapa de aula real é estruturado

Extraído por análise estrutural de um mapa real de aula ao vivo de 1 hora (142 nós, profundidade máxima 10, 4 blocos-raiz). Este é o padrão
de referência — qualquer mapa gerado pela skill deve seguir esta lógica, não uma
aproximação por estilo de texto.

---

## Os números que definem o padrão

- **142 nós** para um mapa de ~1 hora de aula com 4 blocos principais
- **Mediana do título de um nó: 26 caracteres. Média: 39.** A esmagadora maioria dos nós
  é uma frase curta — não um parágrafo, não uma citação longa
- **Profundidade não é opcional em 4 níveis — ela É o mapa.** Distribuição real de nós
  por profundidade: nível 3→27 nós, nível 4→46 nós (o pico), nível 5→21, nível 6→14,
  nível 7→10, nível 8→7, nível 9→1. A maior concentração de conteúdo real está nos
  níveis 4-6, não nos blocos de topo
- **Distribuição de filhos por nó:** 76 nós são folha (0 filhos), 29 têm exatamente
  1 filho, 16 têm 2, 12 têm 3, 5 têm 5, 3 têm 4, 1 tem 7. Ou seja: metade dos nós que
  têm filho tem só UM filho — isso é normal e esperado, não um sinal de mapa raso

---

## Os dois modos de nó-pai — a peça que faltava

Todo nó com filhos existe em um destes dois modos. Confundir os dois é o erro mais comum.

### Modo A — Lista paralela (categoria abre itens independentes)

O pai nomeia um conjunto e cada filho é um item real, autônomo, que poderia existir sem
os outros. Não há sequência lógica obrigatória entre os filhos — são opções, exemplos ou
elementos do mesmo grupo.

```
"O que já vimos:"
  -> Como separar e criar ativos
  -> As 3 fases do funil
  -> Como gerar conteúdos infinitos usando o MDI
  -> Funil Trampolim
  -> Super desafio
```

```
"Para ter um bom LUCRO não é suficiente..."
  -> Fazer lançamentos a cada 3 meses
  -> Produzir bons conteúdos no Instagram
  -> Ter uma narrativa super legal
  -> Ter vários produtos de tickets diferentes
  -> Ter sucesso do cliente
  -> Ter comercial
  -> Você vai precisar...
```

Reconhecível porque: o pai termina com ":", "...", ou é um rótulo curto ("Estrutura",
"Estrutura do fluxo") — e os filhos, se reordenados entre si, não quebrariam nada.

### Modo B — Linha de raciocínio (cadeia sequencial, 1 filho por vez)

O pai é uma afirmação ou gancho, e o filho é o PRÓXIMO passo do mesmo pensamento — não
um item de lista, é a continuação direta. Aqui é onde nascem as cadeias de 1 filho
(29 dos 45 nós não-folha do mapa de referência têm exatamente 1 filho).

```
"Ele usa como inicializador caixinhas e dá o poder para a audiência escolher o que ela quer receber"
  -> "A lógica do nosso funil orgânico é uma só: Qual é o próximo passo?"
    -> "Depois de votarem, voltamos para revelar o ganhador e liberar a isca"
      -> "Estamos criando um 2° filtro, quem tem interesse nessa isca"
```

```
"A real é que não existe um momento em que você pode deixar de aprender"
  -> "E o que te trouxe até aqui não é o que vai te levar adiante"
    -> "Te assusta ou tranquiliza?"
```

Reconhecível porque: cada filho não substitui nem compete com os "irmãos" — ele SÓ
existe depois do pai ter sido dito, é o desdobramento direto. Quando esse desdobramento
tem só um caminho lógico, o nó tem 1 filho só — e está certo assim. Forçar 2-3 filhos
aqui criaria ramos falsos.

**Regra prática:** antes de decidir se um nó vira 1 filho ou vira lista de 3-5, pergunte
"esses desdobramentos são itens de um mesmo grupo (Modo A) ou é o pensamento respirando
e continuando (Modo B)?" — a resposta muda a forma da árvore inteira daquele ramo.

---

## O tamanho do nó individual

Um nó de raciocínio real do mapa (nível 2-3, onde a densidade de argumento é maior):

> "Segmenta a audiência para que você possa depois fazer abordagens diferentes"

Isso é uma frase. Uma ideia. Não é um parágrafo com 3 orações fundidas por vírgula.

Quando a ideia real tem 3 partes (motivo + consequência + resultado), ela NÃO vira um nó
de 200 caracteres — vira 3 nós em cadeia (Modo B):

```
"Repara bem nisso"
  -> "Ele não postou mais que antes"
  -> "Ele postou com mais critério sobre o que expor"
    -> "E foi exatamente por isso que o LTV triplicou"
      -> "Porque quem chegava até ele já chegava reconhecendo ele por alguma coisa específica"
```

(exemplo hipotético no estilo do padrão real, para ilustrar o princípio de fatiar em
cadeia em vez de fundir)

---

## Erros documentados nesta skill e como este método os resolve

1. **Nós fragmentados tipo frase de efeito, sem conexão** (o mapa vira coleção de frases soltas): o erro não era ter nós curtos — nós curtos são o padrão certo. O erro era
   cortar a CONEXÃO entre eles, apresentá-los soltos sem que um levasse ao outro pela
   estrutura pai→filho. A correção não é alongar o texto, é encadear em Modo B.

2. **Fundir tudo em parágrafos longos de texto corrido** (correção errada de 2026-08-10):
   isso reduziu o número de nós e destruiu a granularidade — o oposto do padrão real.
   "Soar natural e falado" é uma propriedade do TOM de cada frase, não motivo para
   reduzir quantos nós existem ou aumentar o tamanho de cada um.

3. **Achatar em 2-3 níveis**: o pico real de conteúdo fica nos níveis 4-6. Um bloco que
   para no nível 2 ou 3 está raso — falta descer mais uma ou duas cadeias de raciocínio
   (Modo B) até chegar no exemplo, no número, ou na consequência concreta.

---

## O que a análise estrutural (fanout/profundidade) não mostra — padrões de raciocínio e persuasão

Contar filhos e medir profundidade revela a FORMA da árvore, mas não o que
realmente vai dentro de cada nó. Uma primeira leitura de conteúdo confundiu
vocabulário específico daquela aula (nomes de campo de um fluxo Manychat,
URLs, preço de produto — tudo do tema "funil orgânico" daquele dia) com
padrão real de estilo. Isso foi corrigido: os itens abaixo são só o que se
repete **independente do tema da aula** — mecânica de raciocínio e
persuasão, não vocabulário de um framework específico. Teste para qualquer
achado novo: isso se repetiria numa aula sobre um tema totalmente diferente?
Se a resposta depende de palavras técnicas daquele contexto, não é padrão.

**1. Abre a verdade desconfortável direto, sem suavizar.** "A real é que
não existe um momento em que você pode deixar de aprender" — afirmação
categórica, sem "eu acho", "talvez", "de certa forma". A tese chega inteira
na primeira frase do bloco.

**2. Justifica com 2-3 causas paralelas curtas, depois devolve a tensão
como pergunta em aberto — não resolve, deixa no ar.** "O mercado vai
mudando" / "As pessoas vão mudando" / "E o que te trouxe até aqui não é o
que vai te levar adiante" → "Te assusta ou tranquiliza?". A pergunta não é
retórica-decorativa — é uma pausa real de reflexão que o expert faz ao vivo
antes de continuar. Diferente de pergunta PRO CHAT ("manda no chat", que
nunca vira nó), pergunta retórica de raciocínio
próprio é padrão real e deve ser usada.

**3. Usa a própria experiência como prova, datada com precisão, organizada
em categorias-diagnóstico nomeadas.** "durante UM ANO INTEIRO" ancora no
tempo real. O problema vira uma lista de rótulos-conclusão, não descrição
solta: "Tempo colocado no lugar errado", "Complexidade desnecessária",
"Falta de direção" — cada rótulo é a CONCLUSÃO do diagnóstico, os filhos do
nó são a evidência que sustenta aquela conclusão.

**4. Constrói o argumento por negação antes da afirmação.** "Para ter um
bom LUCRO não é suficiente..." lista tudo que parece certo mas não resolve,
numa enumeração que vai ficando mais genérica e cansativa de propósito, até
estourar em "Você vai precisar..." como o corte que separa o que não basta
do que resolve de verdade.

**5. Fecha o bloco de tensão com transição curtíssima que devolve o
controle pro público — a "trégua" depois de martelar o problema.** "E dito
isso" → "Você está no lugar certo" → "Hoje nós vamos falar de todos esses
pontos, sem exceção". Nós minúsculos que fazem a virada de tom do bloco
inteiro — não decoração, são a dobradiça entre tensão e alívio.

**6. Estudo de caso segue estrutura fixa de 3 movimentos.** Situação
inicial com prova ("vendia MUITO bem em lançamentos") → a insatisfação que
ela sentia apesar da prova ("mas tava cansada de depender só de
lançamentos") → a virada com resultado numérico exato ("18k de faturamento
mensal"). Número real nunca aproximado — nunca inventar dado fictício "pra
parecer completo", mesma regra inegociável de carrossel.

## Posição da virada emocional — depende do arco do dia, não é fixa

Cruzando dois mapas reais (Dia 01 = abertura do workshop, Dia 02 = segunda
manhã do mesmo workshop): no Dia 02 o técnico vem antes da quebra de crença
(fecha o período). No Dia 01 é o oposto — crença/contexto de mercado abre,
técnico vem depois. **Não existe ordem fixa "técnico antes" ou "emocional
antes"** — depende de que posição aquele bloco ocupa no dia inteiro:
abertura de workshop precisa justificar atenção antes de entregar técnico;
fechamento de período já tem audiência comprometida, entrega valor primeiro.
Antes de estruturar um mapa novo, decidir essa posição primeiro.

## Marcadores de voz — tom, humor, ironia (camada própria, não incluída em conteúdo/persuasão)

- **"rs" marca autoironia especificamente sobre a própria estratégia de
  venda** — aparece no momento em que ela confessa abertamente uma tática
  própria, não é decoração aleatória.
- **Aspas têm 3 funções distintas:** jargão/piada interna introduzido sem
  explicar ("inceptions"), discurso direto citando fala de mercado/cliente
  ("Não se escolhe mais um profissional por 'capacidade'"), ou a frase-chave
  que virou o produto/mensagem em si ("Você cuida do seu negócio enquanto eu
  cuido do seu marketing").
- **CAPS e pontuação múltipla (!!!!)** marcam pico de energia vocal — sempre
  em palavra ou frase curta, nunca frase inteira longa.
- **Informalidade ortográfica ("vc", "tbm")** é pontual, em nó de comentário
  rápido/lateral — não substitui a forma completa no mapa inteiro.

## Checklist antes de gerar o script

- [ ] Decidi a posição da virada emocional considerando o lugar desse bloco no arco do dia?
- [ ] Cada bloco de nível 1 tem pelo menos um ramo que desce até nível 6+?
- [ ] Para cada nó com 2+ filhos, os filhos são realmente paralelos (Modo A) — não uma
      sequência forçada em lista?
- [ ] Para cada linha de raciocínio (Modo B), cada passo novo é um nó novo — nada de
      "e depois, e por isso, e então" dentro do mesmo texto?
- [ ] Nenhum nó individual passa de ~1-2 frases curtas? Se passar, fatiar em cadeia.
- [ ] O outline tem MUITOS nós (mapas de aula real ficam na casa de 100-150), não uma
      dúzia de blocos grandes?
- [ ] Marcadores de voz (rs, aspas, CAPS pontual) aplicados com critério pontual — não uniformemente em todo nó?
