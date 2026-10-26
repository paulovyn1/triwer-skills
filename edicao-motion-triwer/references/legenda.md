# Legenda dinâmica, texto atrás da pessoa, knockout e layout

Etapas 4-5. Legenda estática foi **rejeitada** nos testes (só serif, só faixa, mistura simples). O padrão aprovado (C2): vocabulário misto,
com efeito forte só nas frases de impacto e palavra por palavra no resto.

## Pipeline

```
python <skill>/scripts/words_out.py     # motion/public/words.json + lista "palavra@frame" (base pro roteiro)
python <skill>/scripts/matte_rvm.py     # SÓ se houver cue "behind"/ghost: PNG com alfa só nas janelas desses cues (≈ 1 min), em motion/public/fg/
python <skill>/scripts/verificar.py lint  # legibilidade do roteiro antes de renderizar: largura do slam (linha 1 a 3,1×: até ~5 letras;
                                          # "COORDENADOR" estourou no C3), largura do stack, behind curto, cue longo, 1 knock
```
Depois o Claude escreve o **roteiro** em `motion/src/captions.ts → SCRIPT` (mostrar ao usuário antes de renderizar: portão 2).

## Sintaxe do roteiro

Cada linha `[modo, "texto", {opções}]` consome as próximas palavras de `words.json` **na ordem**; o resolver confere o texto e falha com
"fora de sincronia" se divergir (corrigir o SCRIPT ou `texto.correcoes` do projeto.json). Marcadores por palavra:
`*palavra` serif itálico amarelo · `#palavra` faixa amarela com texto preto · `^palavra` azul · ` | ` quebra de linha.

| Modo | O que faz | Quando |
|---|---|---|
| `build` | palavra por palavra montando a frase; a palavra falada acende em amarelo | padrão, ≈ 65% do vídeo |
| `slam` | 1ª linha gigante batendo na tela com tremida de câmera | gancho (1x) |
| `stack` | blocos editoriais com tamanhos/fontes diferentes | pedido direto ao espectador ("me escuta aqui") |
| `behind` | texto gigante **atrás da cabeça** (entre o fundo e o recorte da pessoa); `{hold: frame}` segura até um frame | 3-4 palavras-chave de cena ("logística", "invisível", "eu te garanto") |
| `behind` + `{fx: "ghost"}` | fundo borra/escurece e a pessoa fica translúcida; a palavra atravessa o rosto | conceito de sumir/invisibilidade (1x) |
| `knock` | tela preta, as palavras da linha 1 em letras gigantes mostram o vídeo P&B por dentro; linha 0 = cabeçalho; linha de batimento que zera | clímax emocional (1x): ex. "teu esforço / morre ali." |
| `hide` | a fala é coberta por painel/tela cheia: consome palavras sem desenhar legenda | painéis `cover` e overlay de CTA |

Distribuição que funcionou (58 s, 70 cues): 1 slam, 2 stack, 3 behind (1 com ghost), 1 knock, 3 hide, 60 build. Mais que 4 `behind`
cansa; `knock` e `ghost` perdem força se repetidos.

## Estilo (identidade do cliente em `theme.tsx`; abaixo o padrão do primeiro kit, como exemplo)
- Base: Outfit 900, MAIÚSCULAS, 84 px, sombra dura 0 4 0 + difusa; palavra falada em amarelo.
- Emoção: Instrument Serif itálico 400, amarelo, ×1,42 (×2,3 no `stack`).
- Números/prazos/quantidade ("duas horas", "dois minutos", "30 anos", "cinco etapas"): faixa amarela (`#`).
- Posição: centro-baixo (y ≈ 1330) com o vídeo cheio; sobe para y ≈ 960 quando há painel em cima (`captionY` segue o `splitAt`).
- **Zona segura do Reels**: nada importante nos ~140 px da direita e nos últimos ~380 px de baixo (botões e legenda do app).

## Texto atrás da pessoa (`behind`)
- Mecânica: `Pessoa.tsx` desenha `base.mp4` → texto → `fg/<quadro>.png` (recorte com alfa do MESMO quadro, `<Img>`, sem decodificar vídeo) dentro da mesma câmera (zoom/shake).
- Posição vertical: no enquadramento de teste (zoom 1,0) a cabeça começa em y ≈ 460; texto de 1 linha com `paddingTop` 445 fica com as pernas das
  letras escondidas atrás da cabeça (efeito "atrás"). Em enquadramento diferente, medir o topo da cabeça em um still e ajustar o
  `paddingTop` em `BehindText` (linha única 445, duas linhas 250, ghost 640).
- Recorte: Robust Video Matting (ONNX, CPU). Conferir um still sobre fundo amarelo (cabelo e mãos limpos) antes de seguir; falhas
  comuns: mão rápida em frente ao rosto, fundo muito parecido com a roupa. Se ficar ruim, reduzir o uso (só `build`).
- Vídeo com **música/ruído visual** de fundo (galpão, árvores) não atrapalha; fundo transparente/vidro sim.

- **Legibilidade (aprendido no C3)**: a cabeça cobre o centro do texto. `behind` de **1 linha com ≤ 10 letras** vira "NÃ▮ ▮XISTE": use **2 linhas**
  (`"posicionar | como líder"`, o texto sobe acima da cabeça) ou `slam`. Linha ≤ 9 letras: a linha grande é ajustada a 800 px (com zoom 1,3 estoura).
  Mesma família da legenda (Outfit 900, sombra dura, sem esticar). `verificar.py lint` avisa.
- **Recorte parado = bug**: o recorte lido de `webm` VP9 repetia quadros e a pessoa "congelava" por 5-13 quadros (visto num teste). Hoje é PNG por
  quadro; depois do render rodar `verificar.py final` (sequências de quadros parados fora do knock = defeito).
- `knock`: **uma fileira por linha do roteiro** (`"sem gastar | um centavo | a mais."` = cabeçalho + 2 fileiras com fonte própria, ≤ 268 px).

## Divisão de tela e zoom (`timeline.ts`)
- `SPLIT_KEYS [início da rampa, fim da rampa, valor depois]`: 0 = pessoa tela cheia, 1 = pessoa na metade de baixo (deslocada 520 px).
  Rampa de 7-9 frames; entra terminando em `painel.from + 9`, sai começando 7 frames antes de `painel.to`. Durante `cover`, voltar a 0.
- `PUNCH [frame, escala de pico, assentar, ataque]`: golpe seco só em frame de corte (senão o salto aparece); push-in (ataque > 0)
  para falas contemplativas.
- Efeitos de câmera extras já no motor: tremida (`shake`) no slam e no clímax do knock, P&B no knock, vinheta, grão de filme leve.

## Verificação (1 comando)
`python <skill>/scripts/verificar.py stills` escolhe sozinho os quadros de pouso (painéis, slam, behind, knock, 1º/último), renderiza 1 lote e monta
as folhas de contato (12 quadros cada): ler só `verify/sheet_N.png`. Corrigir texto cortado, sobreposição com painel e palavra fora da zona segura.
