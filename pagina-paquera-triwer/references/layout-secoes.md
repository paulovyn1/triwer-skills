# Layout das seções e animações

O desenho abaixo vale para os dois modos (HTML e React).
Use como mapa; o arquivo do modo diz como construir.

Princípio: **uma ideia de movimento forte e o resto discreto**. A página não é
um parque de diversões. A entrada do hero é o momento mais orquestrado; daí para
baixo, cada bloco só aparece com suavidade quando entra na tela.

## Estrutura

| Seção | Layout | Movimento |
|---|---|---|
| Barra do topo | Faixa cor `--alerta`, texto em caixa alta | Rola sem parar (marquee) |
| Menu | Logo à esquerda, botão "Garantir por R$ Y" à direita, fixo no topo | Ganha fundo com blur ao rolar |
| Hero | Duas colunas: texto (selo, headline, sub, botão) e visual (foto do expert + mockup sobreposto no canto inferior esquerdo da foto) | Headline entra palavra por palavra; elemento gráfico da capa se desenha no fundo; mockup inclina com o cursor e flutua; foto com parallax leve |
| Currículo | Faixa com logos/nomes em cinza | Carrossel contínuo |
| 3 benefícios | Três cards com ícone | Entram em sequência |
| Identificação | Texto + foto inclinada levemente | Foto com parallax; frase final com marca-texto que "desenrola" |
| Objeção | Foto + texto (lado invertido) | Fala do público em destaque |
| Conta | Card central grande | Calculadora: abas, números aparecendo em sequência, resultado contando de zero |
| Cenário futuro | Texto + foto | Número grande contando |
| Método | Cards numerados em linha, ligados por linha tracejada | Linha se desenha conforme rola; cards sobem no hover |
| Comparação | Duas colunas lado a lado, a do produto destacada | Itens deslizam das laterais |
| Conteúdo | Mockup + lista; faixa de páginas abaixo; escada de etapas | Páginas deslizam na horizontal conforme a rolagem; degraus entram um por um, o último em `--alerta` |
| Para quem é | 4 cards | Entrada em sequência |
| Resultados | 2 cards grandes | Números contando |
| Valor | Texto estreito centralizado | Marca-texto no investimento |
| Oferta | Card largo: mockup + lista com pontilhado + preço gigante + botão | Brilho de fundo respirando; preço contando |
| Garantia | Selo circular + texto | Texto do selo girando devagar |
| Bio | Foto fixa (sticky) à esquerda, marcos em linha do tempo à direita | Foto com parallax; marcos entram em sequência |
| FAQ | Acordeão | Abre com altura animada; "+" gira para "×" |
| WhatsApp | Faixa com botão secundário | |
| Rodapé | Logo, @, links | |
| Barra fixa no celular | Preço + botão, aparece depois do hero | Sobe ao passar do hero |
| Régua lateral (desktop largo) | Linha vertical com as etapas do método | Ponto acompanha a rolagem |

## Botões
- Principal: cor `--alerta`, caixa alta, seta num círculo à direita, brilho
  passando de tempos em tempos, segue levemente o cursor.
- Secundário: contorno, para menu e WhatsApp.
- Todo botão de compra aponta para o mesmo link (checkout). Sem checkout ainda,
  ele rola até a oferta.

## Celular (onde mais quebra)
- Uma coluna; fotos com largura máxima ~520px, centralizadas.
- **Hero**: a foto ocupa a largura toda. O mockup fica pequeno (cerca de 30% da
  largura da foto), **dentro do quadrante inferior esquerdo da foto**, sem passar
  do centro e sem tocar no rosto. A legenda com o nome vai para o canto inferior
  direito, com largura limitada para não encostar no mockup. Parallax desligado
  no hero do celular para os dois não se cruzarem ao rolar.
- Calculadora: células empilhadas, operadores girados.
- Barra fixa de compra com o preço numa linha só (em tela de 360px, esconda o
  preço riscado).
- Régua lateral escondida.

## Acessibilidade e desempenho
- Respeite `prefers-reduced-motion`: sem marquee, sem giro, sem brilho.
- Imagens com `alt` descritivo, `loading="lazy"` abaixo do hero, `width` e `height`.
- Pré-carregue a capa e a foto do hero.
- Contraste de texto sobre fundo escuro: corpo claro, legendas no máximo um tom
  abaixo.
