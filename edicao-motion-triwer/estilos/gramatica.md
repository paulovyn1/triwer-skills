# Gramática comum dos estilos

Vale para qualquer estilo do catálogo. O cartão de cada estilo diz só o que muda. Ler uma vez por vídeo, junto com o cartão escolhido.

## 1. O texto compõe a cena
- O texto faz parte do mundo da cena: escrito numa lousa, num papel, numa tela, num crachá, numa etiqueta, num terminal. Ou a
  própria tipografia vira o cenário, como um pôster gigante ocupando a tela.
- Texto solto por cima da imagem só quando o estilo pede legenda corrida. Nesse caso, a legenda é pequena e neutra, e a palavra
  de ênfase vem separada, grande e em outra camada.
- Na tela vai um recorte da fala (palavras-chave), não a transcrição inteira. A exceção são os estilos com legenda corrida.

## 2. Sincronia com a fala
- Cada palavra que aparece entra no quadro em que é falada, com tolerância de ±2 quadros. Usar os tempos de `words.json`,
  sempre, e nunca chutar tempo.
- O visual pode chegar 2 a 4 quadros antes da palavra, porque o olho lê antes de o ouvido ouvir. Depois da palavra, nunca.
- A troca de cena acompanha o fim de uma ideia (fim de frase ou vírgula forte), não um tempo fixo.

## 3. Dosagem: um protagonista por cena
Toda cena tem um protagonista só. Escolher entre três:

| Protagonista | Quando | Como |
|---|---|---|
| **Imagem** (arquivo, rosto, objeto, prova) | a imagem conta sozinha | texto pequeno: anotação, rótulo ou canto, até 3 palavras |
| **Texto** (frase de impacto, número, virada) | ponto de virada, conclusão, dado | fundo recua (desfoque, escurece, papel liso ou vazio), texto grande, uma cor de destaque |
| **Equilíbrio** (explicação, diagrama) | conceito, comparação, passo a passo | objeto + rótulo curto ao lado, ligados por linha ou seta |

- Nunca dois protagonistas na mesma cena.
- A cada 3 ou 4 cenas, pelo menos uma tem o texto como protagonista, nas viradas.
- Duas cenas seguidas nunca repetem a diagramação do texto (posição, escala e família).

## 4. Diagramação que varia
- **Posição:** centro, terço superior, ao lado do objeto, dentro da interface, na diagonal da mesa ou atrás do objeto (com profundidade).
- **Escala:** uma palavra gigante contra uma frase pequena. Contraste de tamanho de 4x ou mais nas viradas.
- **Família** (cada uma tem um papel):

  | Família | Papel |
  |---|---|
  | serifa itálica | emoção, ironia, memória |
  | grotesca pesada | fato, dado, ordem |
  | manuscrita ou script | voz interna, anotação |
  | mono | sistema, tecnologia, código |
  | pixel | etiqueta, nostalgia digital |

  No máximo 3 famílias por vídeo.
- **Entrada:** máquina de escrever, desfoque para nítido, subir com mola, carimbo, marca-texto passando, caneta circulando, letra
  por letra, ou palavra por palavra no tempo da fala. Variar entre cenas e manter coerência dentro da cena.

## 5. Transições imperceptíveis (nomes usados nos cartões e no `cenas.json`)

| Nome | O que é | Bloco |
|---|---|---|
| `camera-continua` | todas as cenas vivem no mesmo mundo (mural, mesa, prancheta, papel) e a câmera viaja entre elas, sem corte | `Camera` |
| `corte-por-forma` | a forma ou objeto da cena A vira o da B no mesmo lugar (torre amassada vira bola de papel, produto novo vira o antigo) | composição |
| `mergulho` | a câmera entra numa tela, foto ou janela, e a próxima cena está dentro | `Camera` (zoom) + `Foco` |
| `chicote` | deslocamento rápido com borrão direcional, 6 a 8 quadros | `Chicote` |
| `puxar-foco` | a camada A desfoca enquanto a B ganha foco (troca de plano de profundidade) | `Foco` |
| `luz-varre` | sombra de janela ou feixe de luz passa e troca o que está por trás | `SombraJanela` |
| `cobrir` | um objeto entra e cobre a cena (papel deslizando, aba de pasta, mão colocando foto) | `Cartao` com entrada |
| `continua-digitando` | a próxima frase começa a ser digitada na mesma interface | `Escrever` |
| `rajada` | 6 a 12 imagens trocando a cada 4 ou 5 quadros (memória, volume, passagem de tempo) | `Rajada` |
| `corte-seco` | reservado às viradas fortes, sempre com golpe de áudio | — |

Regra: no máximo 1 corte seco a cada 4 trocas, fora das rajadas. O resto se resolve com movimento.

## 6. Textura orgânica (o que tira a cara de modelo pronto)
- Grão de filme animado, fibra de papel, meio-tom em material de arquivo, aberração cromática leve, vinheta.
- Luz natural, como sombra de janela ou persiana, e marcas de película na borda.
- Profundidade de campo (frente e fundo desfocados), sombra projetada real em todo objeto recortado e leve tremor de câmera na mão.
- Imperfeição desenhada: papel rasgado, traço de caneta torto, letra à mão e fita adesiva.
- Imagem gerada por IA ou de banco entra sempre tratada: cor do estilo, grão, recorte com sombra, enquadramento fechado.
  Nunca crua.

## 7. Ritmo
- Mudança visual relevante a cada 1 a 3 s: corte, movimento de câmera ou entrada de elemento.
- Palavra de ênfase a cada 2 a 4 s.
- Nada parado por mais de 0,5 s, exceto um respiro intencional antes de uma virada (até 1 s).
- Narração entre 150 e 200 palavras/min. Acima disso, o texto na tela vira só palavra-chave.

## 8. Áudio
- A voz domina, com a música baixa e contínua.
- Efeito literal do que aparece: tecla na máquina de escrever, papel, alfinete, whoosh no chicote e na câmera rápida,
  grave de impacto nas viradas e clique de interface.
- Densidade de referência: 1 a 1,6 transientes fortes por segundo, incluindo a fala. Master em −14 LUFS.

## 9. Material real conta mais que material inventado
Foto, vídeo e print reais (arquivo histórico, matéria, comentário, trecho de entrevista, foto pessoal) dão credibilidade que nenhuma
ilustração dá. Ordem de preferência:
1. material da própria pessoa ou marca;
2. material real de fonte pública, com crédito;
3. banco gratuito com cara orgânica;
4. imagem gerada, só para objeto ou textura e nunca para "prova".

Onde e como buscar: `references/fontes-reais.md`.
