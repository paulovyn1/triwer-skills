# Catálogo de efeitos sonoros (Mixkit, licença "Sound Effects Free": uso comercial, sem crédito)

Este catálogo é só o **atalho** dos sons já aprovados (com nome). O acervo inteiro (~2.700 efeitos do Mixkit) está em `indice_mixkit.json`:
`python scripts/sfx.py buscar "o que se vê na tela"` (português) e use `mixkit:<id>` direto no `sfx.json` (o mix baixa para o cache).
Som novo que agradou e vai se repetir: `sfx.py catalogar mixkit:<id> <nome> "<uso>"` (baixa para esta pasta e acrescenta a linha abaixo).
Ouvir tudo: `python scripts/revisar_sfx.py --catalogo` → `catalogo.html`. Pico = segundos até o pico (o `mix.py` alinha ao quadro sozinho).

| Arquivo | id | dur | pico | Uso |
|---|---|---|---|---|
| `zoom_impact` | 772 | 1,2 s | 0,41 | golpe de zoom, slam do gancho, número que pousa (+300) |
| `impact_deep` | 1143 | 4,1 s | 0,55 | impacto grave de clímax / título pesado (cortar com `max`) |
| `impact_trailer` | 2908 | 4,9 s | 0,93 | clímax de trailer (não usado ainda) |
| `reverse_impact` | 784 | 10 s | 0,12 | inversão pra transições longas |
| `whoosh_fast` | 1492 | 1,3 s | 1,05 | texto que sobe atrás da pessoa, seta que dispara |
| `whoosh_air` | 1489 | 2,3 s | 0,72 | tela cheia entrando, logos entrando |
| `swoosh_small` | 166 | 0,8 s | 0,28 | painel `top` entrando (usar `pan` [0,4, −0,2]) |
| `swoosh_fast` | 3115 | 0,6 s | 0,11 | painel curto entrando |
| `pop_whoosh` | 3005 | 0,18 s | 0,03 | card/etapa surgindo (com `pitch` crescente) |
| `pop_hard` | 2364 | 1,2 s | 0,005 | pouso seco de faixa/rótulo (cortar em `max` 0,4-0,5) |
| `click_check` | 1120 | 0,24 s | 0,10 | check de checklist (pitch +0..+3) |
| `click_ui` | 2568 | 0,2 s | 0,00 | toque no botão, palavra que acende |
| `type_hit` | 1382 | 0,7 s | 0,16 | carimbo ✗, faixa carimbada |
| `tick_fast` | 1063 | 2,5 s | 1,0 | relógio/cronômetro/contagem (cortar em `max`) |
| `tick_single` | 1061 | 0,85 s | 0,4 | tique isolado (baixo nível) |
| `heartbeat` | 490 | 1,1 s | 0,03 | batimento (clímax emocional; 2 batidas com 8 frames) |
| `flatline` | (gerado: seno 1 kHz, 1,6 s, ffmpeg) | 1,6 s | 0 | linha reta do monitor cardíaco |
| `door_shut` | 196 | 0,46 s | 0,10 | porta que fecha |
| `glitch_break` | 2951 | 1,07 s | 0,02 | quebra/erro digital, fantasma |
| `glitch_small` | 2595 | 1,0 s | 0,23 | erro leve ("sem dado", ficou de fora) |
| `shutter` | 1430 | 0,63 s | 0,14 | foto/registro (cover com foto) |
| `riser` | 790 | 2,6 s | 2,5 | cola de transição de música (já embutido no mix) |
| `bell_achievement` | 600 | 2,4 s | 0,05 | conquista, degrau final (nível baixo −17 dB, `hp` 400) |
| `beep_positive` | 221 | 0,56 s | 0,10 | aviso/comunicado positivo |

Para outro cliente/tom: baixar mais por categoria e acrescentar linha aqui (1 por arquivo) com pico medido.
Medir: `ffmpeg -i x.mp3 -af astats` ou o script de pico do `mix.py` (função de detecção por RMS de 5 ms).
