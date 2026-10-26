# Corte: transcrição, silêncio, respiração, gagueira e repetição

Etapas 1-3 do fluxo. Entrada: o vídeo bruto. Saída: `edl.json`, `work/base.mp4` (frames exatos), `work/voz_cortada.wav`, `work/cuts_map.json`.

## 1. Transcrever e ler (1 comando)

```
cd "<pasta do vídeo>" && PYTHONUTF8=1 python <skill>/scripts/preparar.py "<video.mp4>"
```
Cria `edit/`, `projeto.json` (modelo), `work/orig.wav`, transcreve (Groq whisper-large-v3, palavra a palavra, cacheado) e imprime
`palavra[segundo]` com `<pausa>` entre elas, mais três blocos já calculados: **possíveis tomadas repetidas** (frase dita 2+ vezes: o
CTA regravado 3x do C3), aviso de **tempo fora de ordem** (Groq em trecho com várias tomadas) e **mapa de silêncios ≥ 0,4 s**. Tudo vai também
para `work/leitura.txt` e já roda o faster-whisper (timing). Quando há várias tomadas, a saída já traz a **janela das tomadas segundo o
faster-whisper** (relógio mais preciso): normalmente dispensa `probe_clips`. **Ler só essa saída**, nunca o JSON.
Se aparecer "AVISO: fw_check.py falhou", resolver antes de seguir (sem ele a legenda do trecho de várias tomadas fica fora de tempo).

- Por que Groq: o video-use pede ElevenLabs Scribe (sem chave aqui). Se um dia houver chave, o `transcribe.py` dele é melhor pra
  hesitações ("é", "ahn") porque transcreve verbatim.
- **Nunca passar `prompt` ao Whisper** (tentamos um prompt "verbatim" com "é... hum, tipo assim": alucinou o prompt no meio do
  áudio e pulou 30 s de fala). Sem prompt, `language=pt`, `temperature=0`.
- Segunda opinião automática: o `preparar.py` roda o `fw_check.py` (faster-whisper em CPU, áudio decodificado com librosa: não depende
  do PyAV, que quebrou na versão 19). Serve de relógio mais preciso das bordas (`words_out.py` usa os tempos dele onde as palavras batem,
  inclusive "pra" × "para", "tu" × "você", "cinco" × "5") e de detector de hesitação.

## 2. Decidir a janela e as pausas (leitura de 1 minuto)

Em `projeto.json → corte`:
- `inicio`: 0,1-0,3 s antes da primeira palavra real (a primeira palavra do C2 estava em 1,2 s; `inicio` 1,10). `fim`: logo depois da última.
- `pausas_dramaticas`: `{"tempo_no_original": pausa_total_mantida}` para respiros que devem ficar maiores: depois de frase de impacto
  (0,18-0,22 s), antes de revelação/número (0,40 s). O resto fica apertado (0,12 s no total).
- O limiar é adaptativo: `P70 da fala − 16 dB`. Pega silêncio (≈ −60 dB) e **respiração** (−28 a −40 dB), que um limiar fixo de −35 dB
  deixa passar. Com 16 dB no C2: 23 segmentos, 65,8 → 58,5 s (−11%).
- Cortes mais curtos que ~0,2 s dentro de uma frase soam picotados: `min_pausa` 0,13 + regra de sobra mínima 0,12 já evitam.

## 3. Gagueira, repetição, fala errada

```
python <skill>/scripts/achar_gagueira.py      # candidatos: hesitação só-FW, "eu eu", trecho repetido, palavra esticada, fragmento
python <skill>/scripts/bordas.py 52.4 54.95 57.6 80.9   # onde a fala termina/volta em volta de cada tempo + valor com folga certa
python <skill>/scripts/probe_clips.py work/orig.wav 15.3:17.0   # só se o texto da janela ainda estiver em dúvida (Groq em janela isolada)
```
`words_out.py` já descarta sozinho palavra de trecho removido (inclusive a que o Groq deixava na borda) e corrige o tempo de palavra do Groq
fora de ordem pelo faster-whisper; `descartar`/`retempo` manuais ficam para decisão de texto (palavra que existe mas não deve ir para a
legenda) e alucinação do Groq.
`probe_clips` transcreve **janelas isoladas**: confirma se "ahn/eu eu" é real sem arriscar a alucinação do arquivo todo.
Cada trecho confirmado vira `corte.remover: [[ini, fim], ...]` (tempo do ORIGINAL). Regras:
- Alinhar em limite de palavra, com 50-80 ms de folga (o Whisper desliza 50-100 ms). **Nunca cortar dentro de palavra.**
- Entre as duas tomadas de uma frase repetida, ficar com a **última** (costuma ser a boa) e cortar o começo falso.
- Cortar vício ("né", "tipo") só quando atrapalha; mutilar a cadência dá voz robótica.
- Num dos vídeos de teste a fala já era limpa: a janela útil + pausas bastaram, `remover` vazio. Sempre conferir antes de afirmar isso ao usuário.

Tomada errada no meio (a pessoa regravou o CTA 3x): `corte.remover` pega do fim da última palavra boa até o começo da tomada limpa. Falsa
largada com Whisper que "funde" as duas versões: `texto.descartar: [["E", 51.9], ...]` (palavra + tempo do Groq) e, se o Groq trocar o tempo,
`texto.retempo: [["E", 55.86, 56.33]]` no `projeto.json`. `words_out.py` já descarta sozinho as palavras dentro de `remover`.

## 4. Gerar cortes e base

```
python <skill>/scripts/make_edl.py       # edl.json, work/cuts_map.json, motion/public/cuts.json
python <skill>/scripts/extract_base.py   # work/base.mp4 + work/voz_cortada.wav
```
- Tudo alinhado à grade de frames (30 fps); cada segmento extraído com `-frames:v N` exato; áudio cortado por amostra com fade de 30 ms.
- **Não usar o `render.py` do video-use aqui**: reencoda cada segmento e o concat ganhou +8 frames em 23 cortes, o que desalinha
  legenda e painéis. `extract_base.py` imprime os "frames esperados"; conferir com
  `ffprobe -count_frames -show_entries stream=nb_read_frames work/base.mp4` (deve ser igual).
- `make_edl.py` imprime cada segmento com o frame de saída: guardar, é o mapa pra posicionar painéis e efeitos depois.

## 5. Mascarar os jump cuts

Cortes de silêncio em plano fixo geram saltos. O motor alterna a escala do vídeo a cada corte (1,00 / 1,11) e aplica drift lento (+3%
até o próximo corte), o que faz o salto parecer troca de plano. Golpes de zoom (`PUNCH` em `timeline.ts`) só em frame de corte
(golpe seco) ou como push-in suave (ataque > 0), nas falas-chave: gancho, "me escuta", clímax, CTA. Ver `layout.ts`.

## Checklist antes de seguir
- [ ] edl.json: nº de segmentos coerente (≈ 1 a cada 2,5 s de fala), total em segundos e frames anotado
- [ ] base.mp4: frames lidos == esperados
- [ ] nenhum corte dentro de palavra (conferir 2-3 cortes no `timeline_view.py` do video-use: filmstrip + forma de onda)
