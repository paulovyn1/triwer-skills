# Layout das seções

Cada seção já existe no kit (`Sections.jsx`, estilos em `styles.css`). Este
arquivo diz o que cada uma faz e as decisões que não devem ser desfeitas.

Estes arquivos descrevem as seções pelos nomes do kit React (`Sections.jsx`); no
modo HTML cada uma é uma `<section>` do `template-pagina.html`, na mesma ordem e
com as mesmas classes de CSS.

## Ritmo
Alternar **painel escuro** (`.panel`) e **seção clara**. Um espaçador (`.gap`)
entre painéis seguidos. Largura útil: 1080px em seção clara, 1180px em painel.

## Seção a seção
- **`Nav`**: logo à esquerda, botão `ghost` à direita, fundo claro translúcido e
  fixo. Fundo translúcido escuro faz a logo sumir quando o menu passa sobre um
  painel escuro, por isso o fundo é claro. Sem faixa de aviso no topo e sem
  preço.
- **`Hero`**: headline centralizada com entrada palavra por palavra, subheadline,
  **player da VSL** em 16:9 (tela azul com grade, botão de play amarelo, etiqueta
  "Assista antes de continuar", legenda, barra de controle com tempo 0:00),
  microtexto, botão. O player é ilustrativo até `VIDEO_URL` ter o link; então
  vira um link para o vídeo. Não coloque foto do expert no hero: o espaço é da
  VSL.
- **`Logos`** (faixa de autoridade): título "Um curso só de [área]", subtítulo
  "Seja direcionado pelo mesmo profissional que liderou...", nomes em loop.
- **`Ident`**: painel com título, 3 frases numeradas, fecho com a virada.
- **`Provas`**: 3 cartões. Chip azul/amarelo com o resultado, contagem animada,
  contexto, identificação. Botão embaixo.
- **`Giant`**: texto enorme cujas palavras acendem conforme o scroll
  (`useScroll` + opacidade por palavra).
- **`Travas` / `OQueE`**: caixas brancas numeradas (círculo amarelo saindo do
  canto). `OQueE` abre com um título claro grande antes do painel.
- **`ParaQuem`**: duas fileiras de pílulas em loop, em sentidos opostos, cartão
  interno branco.
- **`Contraste`**: duas colunas, "NÃO é" riscado, "É" em fundo escuro.
- **`Depoimentos`**: some quando `DEPOIMENTOS` está vazio. Nunca preencha com
  texto inventado.
- **`Etapas`**: cartões brancos com texto à esquerda e quadro escuro à direita
  (letra enorme, nome da etapa, semana). No celular o quadro sobe para o topo.
- **`Material`**: grade 3x2 de cartões brancos.
- **`Bonus`**: "BÔNUS" gigante em cinza claro atrás do rótulo, cartões escuros
  com logo pequena, título, selo "Bônus incluso", descrição e quadro à direita.
  Nenhum preço nos cartões.
- **`Oferta`** (ancoragem): título "Recapitulando", linhas com valor riscado em
  vermelho, barra preta "Valor total", cartão branco com a parcela grande em azul
  e o à vista pequeno embaixo. Selos com o prazo de garantia.
- **`Custo`**: painel com três células (hoje → próximo degrau = diferença por
  ano em amarelo) e a pergunta final. Fica depois do preço.
- **`Garantia`**: selo recortado (polígono de 28 pontas) azul com os dias e texto
  em círculo girando em volta, cartão branco.
- **`Criador`**: foto, "Eu sou X. Não quero ser Y." como a objeção do lead na
  voz do expert, texto curto, quatro cartões "onde ele já esteve", faixa de
  empresas.
- **`FAQ`**: acordeão, um aberto por vez, ícone + que gira.
- **`Fechamento`**: painel com dois destinos, a promessa honesta e botão.
- **`Whats`** e **`Footer`**: botão do WhatsApp e rodapé com logo, @ e CNPJ.

## Animações (todas respeitam `prefers-reduced-motion`)
Entrada ao rolar (`Reveal`), título palavra por palavra (`Words`), contagem
(`CountUp`), botão magnético (`CTA`), loop de pílulas e de empresas, brilho que
passa no botão principal. Sem rolagem horizontal em nenhuma largura.

## Armadilhas já vividas
- **Palavras grudadas em título animado.** O espaço entre palavras precisa ser um
  espaço de verdade fora do bloco com `overflow: hidden` (`<Fragment>` com
  `{" "}`). Dar só margem ao bloco faz o texto, quando copiado, sair sem
  espaços ("Setufazotrabalho..."), e o aluno acha que o texto está errado.
- **Destaque por índice.** Contar índices de palavra erra fácil (começam em 0 e a
  pontuação faz parte da palavra). O kit React usa `hl(texto, "frase")` e o
  modo HTML usa `data-hl="frase"`: ambos acham a frase no título. A frase precisa
  bater palavra por palavra, com a pontuação, ou nada é destacado.
- **Menu fixo ilegível** sobre painel escuro: fundo claro opaco.
- **Barra fixa de preço no celular**: não use. Ela mostra o preço antes da
  ancoragem.
