# Identidade visual do aluno

A página precisa parecer do aluno, então os tokens saem dos materiais dele, nunca
de um tema padrão.

## De onde tirar as cores
1. **Capa do produto**: geralmente define o fundo (claro ou escuro), a cor de
   destaque e uma cor de alerta (faixa, selo, marca-texto).
2. **Logo**: define a cor de destaque principal. Se o aluno trocar a cor da
   logo, troque a cor de destaque da página inteira, não só a logo.
3. **Redes do aluno** (prints de posts): confirmam o clima (sóbrio, vibrante, editorial).

Monte no máximo 5 tokens:

| Token | Uso |
|---|---|
| `--fundo` | fundo da página |
| `--fundo-2` | cards e blocos |
| `--destaque` | palavras destacadas, ícones, números de etapa |
| `--alerta` | botão principal, faixa, preço, resultado da calculadora |
| `--texto` / `--texto-suave` | corpo e legendas |

O botão principal usa a cor de mais contraste com o fundo (normalmente `--alerta`).
Confira o contraste do texto do botão (preto ou branco, o que ler melhor).

## Elementos gráficos
Puxe um elemento da capa para o fundo da página (um padrão de linhas, um grid,
uma textura, uma forma). Ele dá unidade sem precisar de imagem nova. Se o aluno
tirar um elemento da capa (ícones, por exemplo), tire também da página.

## Fontes
- Verifique a licença de toda fonte da marca. "Personal Use Only", "Demo" ou
  "Trial" não podem ir para uma página que vende.
- Nesse caso, escolha no Google Fonts uma fonte com o mesmo desenho (geométrica,
  humanista, serifada) e avise o aluno, com a alternativa de comprar a licença.
- Uma fonte para títulos e outra para texto. Evite as genéricas (Arial, Roboto,
  Inter) quando a marca tem personalidade.

## Imagens
- **Hero**: foto do expert no ambiente do trabalho dele, ao lado do mockup do produto.
- **Ao longo da página**: palestrando, em ação, um quadro ou material dele, retrato.
  Uma foto a cada duas ou três seções, alternando lado.
- **Mockup**: o livro/guia em 3D é montado com a capa em imagem (o template já faz).
- **Páginas internas**: prints reais deslizando em faixa. Sem prints, prévias
  desenhadas, marcadas como provisórias.
- **Cuidado com o que aparece na foto**: crachá, logo de empresa, tela com dado.
  Cruze com as regras do aluno antes de usar.
- Otimize tudo (WebP, até ~1200px de largura, foto de fundo até ~1500px).
