# Template Remotion (motor de edição)

Copiar esta pasta para `<pasta do vídeo>/edit/motion/` e rodar `npm install` (1x por vídeo; usar `TEMP`/`TMP` num disco com espaço, ver references/ambiente.md).

## O que muda por vídeo (só isto)

| Arquivo | Gerado por | Conteúdo |
|---|---|---|
| `public/base.mp4` | `extract_base.py` | vídeo cortado (copiar de `edit/work/`) |
| `public/voz_limpa.wav`, `public/mix_A.wav` | `limpar_voz.py`, `mix.py` | áudio; o Remotion só toca o `mix_*.wav` (a mixagem é feita fora) |
| `public/fg/<quadro>.png` | `matte_rvm.py` | pessoa recortada com alfa, SÓ nos quadros dos cues behind/ghost (nome = frame de saída; webm foi abandonado: congelava) |
| `public/words.json` | `words_out.py` | palavras com tempo de saída |
| `public/cuts.json` | `make_edl.py` | frame de cada corte e total |
| `src/captions.ts` | Claude (roteiro) | estilo de cada frase; ver references/legenda.md |
| `src/timeline.ts` | Claude | `SPLIT_KEYS`, `PUNCH`, `PANELS` |
| `src/panels/*.tsx` | kit do cliente / agente | ilustrações em motion |
| `src/theme.tsx` | kit do cliente | cores `C` e fontes `F` (padrão neutro; o kit do cliente substitui) |

`Sound.tsx` toca `public/mix_A.wav`; para outra versão, trocar a constante `MIX`.
O motor (`Main`, `layers/*`, `layout.ts`, `Root.tsx`) não é editado por vídeo. Camadas especiais são opcionais:
sem cue `behind`/`knock`/`slam`/`ghost` no `captions.ts` elas simplesmente não aparecem.

`src/words.ts`: `useAt()` dá o frame LOCAL do painel em que uma palavra é falada (`at("dobrar")`). `src/theme.tsx`: `PanelBg` (grade que desliza), `bob`, `Float`.
Montagem automática: `python <skill>/scripts/montar_motion.py --kit <kit> --paineis ...` (não sobrescreve).

## Comandos (de dentro de `edit/motion`, com TEMP/TMP num disco com espaço)

```
npx tsc --noEmit                                   # checar tipos
node stills.mjs ../verify/full 0.3 3 58 130 ...    # vários stills com 1 bundle só (barato)
npx remotion render Criativo ../work/video_full.mp4 --muted --codec=h264 --crf=16 --x264-preset=slow
```
Painéis isolados: `npx remotion still P01 ../verify/P01_f20.png --frame=20 --scale=0.4` (cada painel de `PANELS` vira uma composição).
