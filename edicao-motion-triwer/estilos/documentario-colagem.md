# Documentário Colagem (`documentario-colagem`)

Papel claro com grão, fotos e filmes de arquivo recortados ou em meio-tom, anotação à mão, ícones simples que se mexem, e uma
palavra por vez no centro da página enquanto a voz conta a história.

## Quando usar / quando não
- **Usar** para história real, personagem histórico ou do mercado, fato curioso ("ninguém lembra que...") e origem de algo que todo
  mundo usa. A emoção é de descoberta e revelação.
- **Não usar** sem material real da história (foto, filme, documento). Com imagem inventada, vira slide.

## Precisa ter
- Narração de 150 a 170 palavras/min.
- De 8 a 15 peças de material real: foto de arquivo, filme de época, documento (patente, carta, jornal antigo) e objeto atual
  que liga a história ao presente.
- Ícones simples desenhados em código.

## Assinatura
- **Mundo e fundo:** papel off-white (#ebe8e1) com fibra e grão, alternando com preto carvão (#0d0d0d) e um terceiro fundo
  temático (azul-céu chapado, planta técnica, sala). Arquivo em P&B ou colorizado, com meio-tom.
- **Tipografia:** serifa itálica condensada e pequena (Instrument Serif itálico) para a palavra que acompanha a fala.
  Sans caixa-alta (Inter 600) para frase de "documento" digitada com cursor. Manuscrita só na anotação com seta.
  Uma cor de destaque (vermelho #e0574f) nos ícones.
- **Texto × cena:**
  - quando o texto é protagonista: uma palavra por vez, centralizada, pequena, sobre papel liso, trocando a cada palavra
    falada ("Just" / "Making" / "Films");
  - quando a imagem é protagonista: a palavra vira anotação ao lado da foto, com seta desenhada;
  - frase-título em serifa no topo do ícone ("designed a Communication System").
- **Transições:** corte seco no tempo forte em cerca de 60% delas (o estilo é mais cortado que os outros); `corte-por-forma`
  nas viradas narrativas (a torre desenhada é amassada e vira a bola de papel na lixeira dos militares que ignoraram a ideia);
  troca de cor do mesmo objeto (torpedo cinza vira vermelho); `rajada` curta.
- **Ritmo (referência):** 45 cortes/min, plano médio de 1,3 s (0,1 a 3,7 s), fala a 157 palavras/min.
- **Áudio:** trilha cinematográfica baixa, tecla de máquina de escrever na digitação, papel amassando, golpe grave nas
  revelações, pulso eletrônico nas ondas dos ícones.

## Tipos de cena
| id | Cena | Protagonista | Como se faz |
|---|---|---|---|
| `palavra-no-papel` | 1 palavra em serifa itálica no centro do papel, trocando no tempo de cada palavra | texto | `FundoPapel` + `PalavrasNaFala` (modo "uma por vez") + `Grao` |
| `recorte-anotado` | foto de arquivo recortada sobre papel + anotação à mão com seta curva | imagem | `Cartao` (sem moldura, sombra suave) + `Caneta forma="seta"` + texto em serifa |
| `arquivo-meio-tom` | filme ou foto de arquivo com meio-tom e zoom lento, título em serifa entrando no meio | imagem | vídeo/imagem + `MeioTom` + `Foco` + `Escrever` |
| `planta-tecnica` | desenho de patente ou planta como fundo, frase caixa-alta digitada com cursor e seleção azul | texto | imagem da planta (domínio público) + `Escrever cursor="barra"` |
| `icone-vivo` | ícone plano desenhado (torre com ondas pulsando, torpedo) sobre papel ou fundo chapado | equilíbrio | SVG próprio + ondas concêntricas animadas + título em serifa |
| `chips-empilhando` | rótulos tipo interface (Wi-Fi / Bluetooth / GPS) entrando um a um no tempo da fala, em fundo escuro com ondas | texto | `Pilula` x N, cada uma em `at("palavra")` |
| `datas-rolando` | anos se sucedendo (1950, 1955, 1965, 1990) em serifa, com desfoque entre eles | texto | `PalavrasNaFala` + `Foco` |
| `objeto-isolado` | objeto atual (roteador, celular) iluminado em fundo escuro + título caixa-alta | imagem | foto recortada + `Vinheta` forte |
| `quadro-na-parede` | foto do personagem em moldura na parede + frase final embaixo, em serifa | imagem → texto | `Cartao moldura="borda"` dourada + `PalavrasNaFala` |
| `lixeira` (exemplo de `corte-por-forma`) | o objeto da cena anterior amassado cai numa lixeira, em foto | imagem | composição de 2 recortes + queda com mola |

## Receita técnica
- Blocos: `FundoPapel`, `Grao` (forca 0,10), `Vinheta` (0,35), `MeioTom` (tam 5) no arquivo, `PalavrasNaFala`, `Escrever`,
  `Caneta`, `Cartao`, `Pilula`, `Foco`, `Rajada`.
- Fontes: Instrument Serif (itálico), Inter (600, caixa-alta, tracking 0,04em), Caveat (anotação).
- Paleta: papel #ebe8e1, tinta #1b1b1b, carvão #0d0d0d, destaque #e0574f, azul de interface #2b8fd6.
- Arquivo colorizado ganha grão extra e leve tremor (1 a 2 px).
- Palavra no papel: corpo de 54 a 64 px, para ficar pequena e elegante. O vazio em volta é o efeito.

## Onde buscar o material
Internet Archive (Prelinger, cinejornais), Wikimedia Commons (fotos históricas, patentes), Biblioteca do Congresso (EUA) e
arquivos nacionais. Trecho de entrevista ou filme antigo pelo YouTube com `baixar_trecho.py`, com crédito na tela. O
objeto atual vem de banco gratuito ou de foto própria, recortado.

## Erros que matam o estilo
- Palavra no centro grande demais ou em negrito: perde a elegância.
- Foto "de banco" moderna e colorida no meio do arquivo.
- Ícone com cara de clip-art (gradiente, 3D). O ícone é plano e com linha.
- Mais de uma cor de destaque.
- Arquivo sem crédito.

## Checagem antes de entregar
- Cortes/min entre 30 e 50.
- Cada palavra no papel entra a ±2 quadros da fala.
- Pelo menos 2 cenas de material real a cada 10 s.
- Nenhum quadro sem grão.

## Origem
Referência de 32 s: 24 cortes, plano médio de 1,28 s, 157 palavras/min, −14,2 LUFS, 1,6 transiente/s.
