# Prancheta Técnica (`prancheta-tecnica`)

O produto aparece visto de cima, numa superfície cinza, cercado de desenho técnico: cotas, réguas, chamadas e linha do tempo
com anos. A câmera gira devagar e o produto troca de versão no mesmo lugar a cada palavra. No final, uma janela de terminal
digita a frase de fechamento. É tudo um plano-sequência, sem cortes.

## Quando usar / quando não
- **Usar** para produto, evolução ("não começou perfeito"), consistência, tecnologia, antes e depois de versões. Vídeo
  curto, de 8 a 20 s, ou abertura de um vídeo maior.
- **Não usar** em vídeo longo (o plano-sequência cansa depois de cerca de 20 s), nem sem um objeto central.

## Precisa ter
- Narração curta e rápida, de 190 a 210 palavras/min.
- De 3 a 6 versões ou variações do objeto (fotos recortadas de cima, mesma escala) e uma frase final de 6 a 10 palavras.

## Assinatura
- **Mundo e fundo:** superfície cinza fosca (#b9bcbf → #6d7074) com vinheta forte e luz de cima. Desenho técnico em branco
  a 70%: retângulo de enquadramento, cotas com setas, régua com marcações e anos, rótulos pequenos ("DEVICE OVERVIEW", "v16").
  No fim, escurece para grafite (#2a2c2f) com letras gigantes desfocadas ao fundo ("SYS END").
- **Tipografia:**
  - grotesca condensada (Space Grotesk 500 ou Oswald) em palavras empilhadas pequenas ao lado do objeto ("this / is / the /
    iPhone");
  - uma palavra em script de traço (Caveat) girada;
  - mono (JetBrains Mono) no terminal, com cursor bloco.
- **Texto × cena:** o objeto é sempre o protagonista. As palavras ficam pequenas, ao lado dele e alinhadas às cotas, e entram
  no tempo da fala. Só o terminal final vira protagonista de texto.
- **Transições:** só `camera-continua` (rotação de 15 a 40° em rz, zoom de 0,9 a 1,15) e `corte-por-forma` (o objeto troca de
  versão no lugar, em 1 a 2 quadros de flash). O mergulho no terminal se faz escurecendo.
- **Ritmo (referência):** 0 cortes em 9 s. Troca de versão a cada 0,5 a 1 s. Fala a 205 palavras/min.
- **Áudio:** trilha eletrônica com pulso, "tic" mecânico em cada troca de versão, tecla no terminal e um grave no fim.

## Tipos de cena
| id | Cena | Protagonista | Como se faz |
|---|---|---|---|
| `produto-com-cotas` | objeto no centro com cotas, régua e anos em volta, câmera girando devagar | imagem | `Camera` (rz de −8 a +30°) + SVG de cotas desenhadas (`pathLength`) + `Cartao` sem moldura com sombra |
| `troca-de-versao` | o objeto vira outra versão no mesmo lugar, no tempo da palavra | imagem | lista de imagens trocando por `at()` + flash branco de 1 quadro (opacidade 0,25) |
| `palavras-ao-lado` | 1 a 4 palavras empilhadas pequenas ao lado do objeto, uma em script girada | equilíbrio | `PalavrasNaFala` (entrada "subir") posicionado em coordenada de mundo |
| `terminal` | janela de terminal com `>>` digitando a frase final e cursor bloco; letras gigantes desfocadas ao fundo | texto | janela em JSX + `Escrever cursor="bloco"` + `Foco` no fundo |

## Receita técnica
- Blocos: `Camera` (o mundo inteiro é a prancheta; perspectiva 2600), `Escrever`, `PalavrasNaFala`, `Foco`, `Vinheta` (0,6),
  `Grao` (0,06).
- Cotas: SVG próprio com linhas de 2 px, setas e texto de 18 a 22 px em mono. As cotas se desenham quando o objeto chega e
  ficam respirando (opacidade de 0,6 a 0,8).
- Versões do objeto: todas com a mesma escala e o mesmo centro (alinhar antes, em Python/PIL, pelo recorte).

## Onde buscar o material
Fotos de produto vistas de cima: imprensa da marca (com permissão), banco gratuito ou `gerar-imagem` para objeto genérico.
Produto de marca de terceiros só com autorização do usuário. Em anúncio pago, nunca.

## Erros que matam o estilo
- Versões em escalas diferentes (o objeto "pula").
- Câmera parada.
- Cota decorativa sem relação com o objeto.
- Texto grande demais ao lado do objeto.
- Vídeo passando de 20 s.

## Checagem antes de entregar
- Centro do objeto estável em ±6 px entre versões.
- Nenhum corte seco.
- Terminal termina de digitar até 3 quadros depois da última palavra.

## Origem
Referência de 9,1 s: 0 cortes, 205 palavras/min, −14,4 LUFS.
