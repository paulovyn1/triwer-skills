# Identidade visual do expert

A página precisa parecer do expert, e da mesma marca da página de vendas dele.
Os tokens saem dos materiais dele, nunca de um tema padrão. Os modelos da skill
vêm com uma paleta de exemplo (azul-marinho, azul e amarelo). Troque sempre.

## Se já existe página de vendas

Copie de lá os tokens de cor, as fontes, o elemento gráfico de fundo e as fotos.
É o caminho mais rápido e garante que quem clica no destaque não sinta que
mudou de site.

## Se não existe

1. **Logo**: define a cor de destaque principal.
2. **Capa do produto principal**: define o fundo (claro ou escuro) e a cor de
   alerta (faixa, selo, botão).
3. **Posts do expert**: confirmam o clima (sóbrio, vibrante, editorial).

## Tokens dos modelos

| Token | Uso |
|---|---|
| `--fundo`, `--fundo-2`, `--fundo-3` | fundo da página, cards e menu (do mais escuro ao mais claro, ou o contrário em tema claro) |
| `--linha` | traços do fundo, bordas, ícones discretos |
| `--destaque`, `--destaque-2` | cor da marca: ícones do menu, botão do card claro, barra da tela animada |
| `--alerta` | botão principal, faixa do título, marca-texto, selo do destaque |
| `--texto`, `--texto-corpo`, `--texto-suave` | títulos, frases dos cards, legendas |
| `--papel` | fundo do card claro |
| `--gratuito-1/2/3` | degradê do card gratuito (três tons da cor de destaque) |
| `--*-rgb` | as mesmas cores em RGB, para transparências. Mude junto. |

O botão principal usa a cor de mais contraste com o fundo (normalmente
`--alerta`). Confira se o texto do botão lê melhor em preto ou em branco.

## Elemento gráfico

O fundo do card de destaque tem traços que se desenham na entrada. Troque pelos
traços de um elemento da marca (padrão da capa, grid, forma do logo). Sem nada
reaproveitável, apague o SVG.

## Fontes

- Verifique a licença de toda fonte da marca. "Personal Use Only", "Demo" ou
  "Trial" não vão para uma página pública.
- Nesse caso, escolha no Google Fonts uma com o mesmo desenho e avise o aluno,
  com a alternativa de comprar a licença.
- Uma fonte para títulos e outra para texto.

## Imagens

| Onde | O que funciona | Tamanho |
|---|---|---|
| Topo (hero) | o expert no ambiente de trabalho, olhando para a câmera, rosto no terço de cima (o texto fica embaixo) | até ~1200px de largura |
| Destaque | capa do produto (vira livro 3D) ou foto em moldura | capa ~900x1440 |
| Card escuro | retrato do expert, fundo escuro | até ~900px |
| Card claro | algo claro e do trabalho dele (quadro, material, bastidor) | até ~900px |
| Logo | SVG, versão para fundo escuro ou claro conforme o tema | |

- Uma foto diferente por posição. Repetir a mesma foto em dois cards parece
  página pela metade.
- Confira cada foto contra as regras do aluno (crachá, logo de empresa, tela).
- Otimize para WebP: `node scripts/otimizar-imagens.mjs <origem> <destino>`
  (precisa de `npm i sharp` numa pasta de ferramentas, fora do projeto).
