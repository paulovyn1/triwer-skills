# Identidade visual

A estrutura vem da referência. A identidade vem do aluno: cores, fontes e logo
dele, nunca as de outra marca. O kit usa a identidade do exemplo (navy, azul e
amarelo), então a primeira tarefa de montagem é trocar os tokens.

## Tokens (bloco `:root` de `src/styles.css`)
| Token | Uso |
|---|---|
| `--navy`, `--navy-2`, `--navy-3` | fundo dos painéis escuros e dos quadros |
| `--blue`, `--blue-2` | destaque de texto (palavras-chave), ícones, selo de garantia, valor da parcela |
| `--yellow` | botão principal, marca-texto, etiquetas, números de caixa |
| `--paper` | fundo claro da página (com grade de pontos) |
| `--ink`, `--ink-2` | texto sobre fundo claro |
| `--grad` | destaque em degradê, ver regra abaixo |

Tire as cores da logo e da capa do produto do aluno: o fundo dos painéis vem da
cor mais escura da marca, o destaque da cor de acento da logo, o botão da cor de
mais contraste com o fundo escuro. Se o aluno trocar a cor da logo, troque o
destaque da página inteira, não só a logo.

## Degradê: um tom só
Degradê de um tom a outro (azul para amarelo, rosa para laranja) parece estranho
quando a paleta da marca não tem essa transição, porque a cor do meio sai suja
(esverdeada). O aluno recusou o degradê azul para amarelo. Regra: **ou só azul,
ou só amarelo**. No kit, `--grad` está com o mesmo tom nas duas pontas. Elementos
de apoio (etiqueta "Resultado Esperado", selo "Bônus incluso") ficam em cor
chapada.

## Fundo e painéis
- Página: fundo `--paper` com grade de pontos (`radial-gradient`), como a
  referência. Não use fundo preto na página inteira, o contraste claro/escuro dos
  painéis é o que organiza a leitura.
- Painéis escuros: cantos bem arredondados, brilho radial azul no topo, margem
  lateral pequena. Dentro deles, cartões brancos para o que precisa ser lido com
  destaque (caixas numeradas, etapas, cartão da pílula).

## Fontes
- Verifique a licença de toda fonte da marca. "Personal Use" ou "Demo" não vai
  para página de venda. Escolha no Google Fonts uma de desenho parecido e avise.
- O kit usa Outfit (títulos) e Manrope (texto) via `@fontsource-variable`,
  embutidas, sem requisição externa.

## Imagens
- Foto do expert no ambiente de trabalho dele (palco, operação, escritório), uma
  a cada duas ou três seções. Retrato na seção do criador.
- Logo em SVG de preferência. No fundo claro, o kit escurece a logo com
  `filter: brightness(.15)`. Se a logo do aluno já tiver versão escura, use ela.
- Cuidado com crachá, logo de empresa e tela com dado: cruze com as regras de
  confidencialidade do aluno (por exemplo, não citar a empresa atual).
- Os quatro cartões "onde ele já esteve" usam fotos do expert com legendas
  reais. A foto é ilustrativa, a legenda é o fato. Se o aluno tiver foto
  específica de cada marco, use.
- Otimize tudo com `scripts/otimizar-imagens.mjs` (WebP, até ~1200px).
- `public/img/grid.webp` do kit é a textura de grade dos quadros e do player.
  Troque por um elemento da capa do aluno se houver.
