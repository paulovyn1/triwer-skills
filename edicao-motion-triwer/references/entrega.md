# Render, verificação e entrega

Entrada: `motion/` completo + `mix_<A|B|C>.wav`. Saída: `../entrega/<nome> - trilha X.mp4` + revisão de efeitos numerada.

## Passo a passo
```
python verificar.py stills                      # ANTES do render: lint + folhas dos quadros de pouso (QA por subagente Sonnet: references/paineis.md)
python verificar.py stills --quadros 222,615    # rodada de correção: só esses quadros, 1 folha
python entregar.py all "Nome" --render          # segundo plano (run_in_background), ≈ 5-8 min
python verificar.py final                       # sem caminho = .mp4 mais novo de ../entrega
```
`entregar.py`: renderiza `work/video_full.mp4` (`--muted`, CRF 16), confere `quadros == total`, muxa cada trilha **sem `-shortest`**,
mede LUFS/pico, gera `verify/final_sheet.png` (12 quadros do arquivo final: 1 imagem), roda `verificar.py final`, gera a **revisão de
efeitos** (vídeo numerado + página de escuta, `revisar_sfx.py`), registra as músicas entregues para o cliente e apaga `edit/_tmp`
(chegava a 9,6 GB). Só 1 versão: `entregar.py A "Nome"`. Correção só de áudio (efeito/música): `mix.py X` + `entregar.py X "Nome"` sem `--render`.
- Formato: H.264 1080×1920 30 fps, AAC 320 kbps 48 kHz, faststart (≈ 200 MB); canal com limite: recomprimir cópia com `-crf 20`.

## Verificação (barata; sem imagem avulsa)
1. Folhas do `stills` e `final_sheet.png`: texto cortado/estourando, painel cortado, legenda escondida ou em cima do botão, fonte errada.
2. Bordas de corte suspeitas: `python bordas.py <t>` (energia em volta) ou `timeline_view.py` do video-use.
3. Áudio por números: `medir_mix.py`, LUFS/pico do entregar. **Não afirmar que "soa bem"**: pedir teste de ouvido no celular.
4. 1ª e última palavra legendadas, CTA longe da interface, nenhum nome de empresa/pessoa fora do que o kit autoriza.

## Fechar
- `edit/project.md`: sessão, decisões, "Outstanding", o que o usuário aprovou/rejeitou.
- Limpar o que sobrar: `edit/clips_graded` e `edit/audio/_cache` quando o vídeo estiver aprovado (o `_tmp` o entregar já apaga).
- Regra nova: gosto do usuário → `preferencias.py registrar`; defeito recorrente ou técnica melhor → esta skill; marca → kit do cliente.
  Painel novo aprovado vai para `<kit>/paineis-<vídeo>/` com tempos por `useAt` e nome sem colisão.
- Entregar ao usuário: caminho do arquivo, 3 linhas do que há de especial, números medidos, o vídeo de efeitos numerados + a página de
  escuta, e **o que não foi verificado** (áudio por ouvido).
