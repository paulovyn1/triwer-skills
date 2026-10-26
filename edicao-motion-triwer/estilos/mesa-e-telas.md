# Mesa e Telas (`mesa-e-telas`)

Interfaces conhecidas recriadas: câmera do celular, notas, mensagens, rede social, busca, app de ranking. A frase da narração vai
sendo digitada nelas. Elas se alternam com objetos reais vistos de cima numa mesa (fita cassete, console portátil, lápis, cartas)
iluminados por sol de janela, e a frase aparece na tela do objeto.

## Quando usar / quando não
- **Usar** para insight de negócio, comportamento digital, dado de pesquisa, "o jeito antigo × o jeito novo", tutorial
  conceitual. A emoção é de clareza moderna.
- **Não usar** em tema emocional ou pessoal (melhor `mural-de-memorias`), nem quando o usuário não quer imitar interface de
  marca. Neste caso, usar interface genérica.

## Precisa ter
- Narração de 170 a 180 palavras/min.
- De 3 a 6 objetos fotografados de cima, de banco ou de foto própria.
- Interfaces recriadas em código (HTML/CSS), sem print.
- Um dado numérico (pesquisa, percentual) se houver.

## Assinatura
- **Mundo e fundo:**
  - interfaces em tela cheia, claras (#f2f2f2) ou escuras (#0b0d10);
  - mesa de madeira ou base de corte quadriculada clara com objetos e sombra de janela forte;
  - inserções em faixa de cinema 16:9 no meio do vertical;
  - marcas de película na borda lateral e grão.
- **Tipografia:** a fonte da própria interface (SF/Inter para iOS, Roboto para Google), sans média (Inter 500). Manuscrita
  ou máquina de escrever só no papel ("Contract"). Destaque por cor da interface: azul do balão, verde do botão, laranja
  do aviso.
- **Texto × cena:**
  - quase todo texto mora dentro de uma interface (campo digitando, balão, item de lista) ou na tela de um objeto;
  - frases soltas só em fundo liso, pequenas, com um objeto 3D entrando entre as palavras ("In today's 🌍 world").
- **Transições:**
  - `continua-digitando` (a frase seguinte começa na mesma interface);
  - `mergulho` (a câmera entra na tela);
  - `cobrir`;
  - `corte-seco` entre mundos (interface ↔ mesa), cerca de 1 a cada 3 s.
- **Ritmo (referência):** 21 cortes/min, plano médio de 2,8 s, fala a 177 palavras/min.
- **Áudio:** trilha lo-fi ou eletrônica leve, teclado digitando, notificação, clique, obturador na câmera do celular, whoosh
  curto nas entradas.

## Tipos de cena
| id | Cena | Protagonista | Como se faz |
|---|---|---|---|
| `interface-digitando` | campo de nota, mensagem ou busca, com a frase digitando no tempo da fala | texto | componente de interface + `Escrever` sincronizado a `at()` |
| `baloes-de-conversa` | balões de mensagem entrando (cinza e azul), com "digitando..." entre eles | texto | balões com entrada de mola + 3 pontos animados |
| `camera-do-celular` | interface da câmera (modos, botão) enquadrando uma cena real com foco quadrado | imagem | moldura de interface por cima de foto ou vídeo + `Foco` |
| `objeto-na-mesa` | objeto visto de cima com sol de janela, frase na tela dele | imagem | foto da mesa + `Cartao` (objeto recortado) + `SombraJanela` (forca 0,55) + texto em `transform` na tela |
| `lousa-na-sala` | sala simples com lousa, frase escrita em giz | texto | imagem da sala + texto com textura de giz + `Escrever` |
| `palavra-com-objeto` | frase curta em fundo liso, com objeto 3D entrando entre duas palavras | texto | `PalavrasNaFala` + imagem recortada com mola |
| `anel-de-progresso` | card escuro com anel de progresso contando (66% → 80%) + rótulo | texto | SVG `circle` com `strokeDashoffset` + `Contador` |
| `pilulas-conectadas` | pílulas coloridas com brilho ligadas por linhas (indicação, recomendação) | equilíbrio | `Pilula` + linhas SVG desenhadas |
| `faixa-cinema` | interface ou cena em 16:9 com barras pretas no vertical | imagem | `Faixa` |
| `busca-final` (CTA) | barra de busca digitando + resultado com o nome da marca | texto | interface de busca genérica + `Escrever` |

## Receita técnica
- Blocos: `Escrever`, `PalavrasNaFala`, `Cartao`, `SombraJanela`, `Faixa`, `Pilula`, `Contador`, `Camera`, `Foco`,
  `Grao` (0,06), `BordaFilme`.
- Interfaces: recriar em JSX com medidas reais de celular (largura útil de 1080 px = 390 pt × 2,77). Logos de terceiros não
  entram. Ícones genéricos (traço) no lugar.
- Objeto na mesa: inclinação de 6 a 14° e sombra dura na direção da janela.

## Onde buscar o material
- Objetos: Pexels ou Pixabay ("top view desk", "flat lay retro", "cassette tape top view", "handheld console flat lay").
- Interfaces: código, nunca print de app real com dado de outra pessoa.
- Dados: fonte real citada no próprio card ("Fonte: Harvard Business Review, 2023").

## Erros que matam o estilo
- Interface com cara de modelo (cores saturadas, sombras exageradas).
- Print real de app com dado de terceiro.
- Digitação fora do tempo da fala.
- Objeto sem sombra coerente com a luz da janela.
- Número sem fonte.

## Checagem antes de entregar
- Cada frase digitada termina até 3 quadros depois da última palavra falada dela.
- Logos e nomes de marca de terceiros só onde o usuário autorizou.
- Faixa 16:9 em no máximo 30% do vídeo.

## Origem
Referência de 37 s: 13 cortes, plano médio de 2,84 s, 177 palavras/min, −14,2 LUFS.
