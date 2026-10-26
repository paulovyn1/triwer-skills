# Mural de Memórias (`mural-de-memorias`)

Tudo é físico: página de jornal com a foto da pessoa circulada de caneta, fotos de infância com etiqueta de nome, desenhos na
cortiça, pastas de arquivo com abas ("EU CRIANÇA", "EU ADULTO") e crachás. Há um pôster gigante em vermelho e um mural de
investigação com polaroids, alfinetes e barbante. A luz de janela varre tudo. Uma legenda pequena fica sempre ligada, e
palavras-chave gigantes desfocadas aparecem ao fundo.

## Quando usar / quando não
- **Usar** para história pessoal, origem, "eu era assim", nostalgia, antes e depois de mentalidade, manifesto em primeira pessoa.
  A emoção é afeto, identificação e virada.
- **Não usar** sem fotos e vídeos pessoais reais. Este estilo vive do material da pessoa.

## Precisa ter
- Narração em primeira pessoa, de 170 a 185 palavras/min.
- De 10 a 25 fotos pessoais, com pelo menos 4 vídeos caseiros curtos. Desenhos, cadernos ou objetos antigos, se houver.
- Uma foto atual da pessoa.

## Assinatura
- **Mundo e fundo:**
  - superfícies reais: jornal, cortiça, papel kraft, base de corte verde quadriculada (#1f8a5b), pastas de arquivo bege com
    abas e cartolina vermelha (#c8102e);
  - sombra de janela ou persiana varrendo devagar sobre tudo, com luz quente.
- **Tipografia:**
  - grotesca pesada condensada (Archivo Black ou Anton) para o pôster ("não / tá / nem aí") e para a manchete rasgada;
  - serifa de jornal (Playfair Display) na manchete do jornal;
  - fonte pixel (Silkscreen) na etiqueta de nome, e manuscrita marcador (Caveat Brush ou Permanent Marker) no crachá;
  - legenda corrida em Inter 600, branca, de 34 a 40 px, no centro baixo e sempre ligada.
- **Texto × cena:** três camadas.
  1. Legenda pequena e constante, que acompanha a fala.
  2. Palavra-chave gigante em cinza claro desfocada no topo, atrás de tudo ("legal", "chato", "cabeça").
  3. Texto que é objeto: manchete rasgada com marca-texto amarelo, crachá, aba da pasta.
- **Transições:**
  - `chicote` com borrão para abrir;
  - `rajada` de fotos (13 trocas em 2 s, cerca de 4 quadros cada) para "infância";
  - `cobrir` (aba de pasta, papel), `luz-varre` e `camera-continua` no mural final, num plano-sequência de 12 s
    passeando entre as polaroids.
- **Ritmo (referência):** 30 cortes/min, mas concentrados nas rajadas. O plano mais longo dura 12,8 s, com câmera viajando.
  Fala a 181 palavras/min.
- **Áudio:**
  - trilha afetiva (piano ou indie leve) que cresce na virada ("Mas a boa notícia...");
  - efeitos: papel, alfinete, clique de mouse nas pastas, obturador nas fotos, rasgo no pôster.

## Tipos de cena
| id | Cena | Protagonista | Como se faz |
|---|---|---|---|
| `jornal-com-foto` | página de jornal com foto da pessoa, manchete serifada + círculo e sublinhado de caneta vermelha | imagem | `Cartao` (jornal) + `Caneta forma="circulo"` + `Caneta forma="sublinhado"` + `SombraJanela` |
| `foto-com-nome` | foto antiga em tela cheia com etiqueta pixel do nome | imagem | `Rajada` ou foto única + etiqueta (Silkscreen, fundo preto 60%) |
| `rajada-de-fotos` | 8 a 13 fotos trocando a cada 4 quadros | imagem | `Rajada cada={4}` + clique de obturador a cada 2 trocas |
| `desenhos-na-cortica` | desenhos e papéis na cortiça, câmera deslizando, luz varrendo | imagem | `Camera` + `Cartao` x N + `SombraJanela` |
| `grade-de-videos` | 4 a 6 vídeos caseiros em grade, entrando um a um | imagem | grade CSS com `OffthreadVideo`, entrada com mola |
| `poster-gigante` | 3 palavras enormes ocupando a tela em blocos preto, branco e vermelho, papel rasgado | texto | Archivo Black de 260 a 340 px, blocos com textura de papel |
| `explosao-hq` | estrela de HQ amarela sobre vermelho, rosto dividido (antes/depois), palavras grandes entrando em pulos | texto | SVG da estrela + 2 metades de foto + `PalavrasNaFala` (entrada "mola") |
| `arquivo-de-pastas` | pastas com abas, cursor de mouse clicando "EU CRIANÇA" e crachá subindo com foto e nome à mão | equilíbrio | `Cartao` x N (abas) + cursor SVG + crachá |
| `mural-investigacao` | cortiça com polaroids, alfinetes, barbante vermelho e manchetes rasgadas com marca-texto; câmera passeia | imagem → texto | `Camera` (5 a 7 poses) + `Cartao moldura="polaroid" preso="alfinete"` + `Barbante` + `MarcaTexto` |

## Receita técnica
- Blocos: `Camera`, `Cartao`, `Barbante`, `Caneta`, `MarcaTexto`, `Rajada`, `SombraJanela` (forca 0,4, ângulo −30),
  `Grao` (0,07), `Vinheta` (0,35), `Foco` nas palavras gigantes do fundo (blur de 6 a 10 px, opacidade 0,55).
- Legenda corrida: `PalavrasNaFala` em blocos de 2 a 4 palavras, trocando por bloco, sem caixa nem sombra pesada (só
  `textShadow 0 2px 8px rgba(0,0,0,.6)`).
- Texturas reais (cortiça, jornal, kraft, base de corte): foto de banco gratuito ou `gerar-imagem` em vista de cima, com luz
  neutra. A sombra da janela é feita em código, nunca na imagem.

## Onde buscar o material
- Fotos e vídeos da pessoa: pedir ao usuário, numa pasta só.
- Texturas: Pexels ou Pixabay com termos como "cork board top view", "old newspaper texture", "kraft paper", "cutting mat".
- Jornal: diagramar em código com a manchete real da pessoa. Nunca imitar um jornal real existente com nome e logo.

## Erros que matam o estilo
- Superfície sem luz (sem `SombraJanela`), que fica com cara de colagem digital.
- Polaroid sem sombra e sem rotação.
- Legenda grande disputando com o pôster.
- Rajada longa demais (mais de 2,5 s).
- Mural parado.

## Checagem antes de entregar
- Legenda presente em ≥ 90% do tempo de fala.
- No máximo uma palavra gigante de fundo por cena.
- No mural, câmera em movimento contínuo.
- Fotos pessoais em pelo menos 50% das cenas.

## Origem
Referência de 48,6 s em português: 24 cortes (13 deles numa rajada de 2 s), plano mais longo de 12,8 s, 181 palavras/min,
−14,9 LUFS.
