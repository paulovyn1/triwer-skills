# Ambiente e armadilhas já vividas (testado no Windows)

`python <skill>/scripts/preflight.py` checa tudo abaixo em um comando e imprime a correção exata.

## Ferramentas
- **ffmpeg 8.x full** (winget Gyan.FFmpeg) com `rubberband`, `afftdn`, `arnndn`, `deesser`, `sidechaincompress`, `loudnorm`.
- **Node ≥ 20** (Remotion 4.0.x). Projeto Remotion por vídeo (copiar `template/remotion`). Porta própria nos renders
  (`REMOTION_PORT`, padrão 3090): se a 3000 estiver ocupada por outro app, o Remotion lê a página errada.
- **yt-dlp** (trechos do YouTube, comentários) e **Chrome** (prints de página) para `references/fontes-reais.md`.
- **venv de ferramentas** `~/Developer/video-tools` (uv, Python 3.12): onnxruntime, opencv-python-headless, numpy, soundfile, noisereduce,
  scipy, librosa, pyloudnorm, faster-whisper, requests, pillow. **Um interpretador só**: todo script desta skill se reexecuta sozinho nele
  (`_cfg.py`), então qualquer `python` serve para chamá-los; `EDICAO_SEM_VENV=1` desliga. (No C3 o Python do sistema não tinha `requests`
  e o venv não tinha `faster-whisper`: 3 erros por vídeo até unificar.)
- **video-use** clonado em `~/Developer/video-use` (registrado como skill; usamos só `helpers/timeline_view.py` e as 12 regras duras do SKILL.md).
- **faster-whisper** (CPU, no venv; CUDA falha: `cublas64_12.dll`).
- **Chrome Headless Shell compartilhado** em `~/Developer/video-tools/chrome-headless-shell` (o `remotion.config.ts` e o `stills.mjs` do template já
  apontam pra ele; evita baixar 120 MB por vídeo). Se não existir, o Remotion baixa sozinho; copie `node_modules/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/*` pra lá uma vez.
- **GROQ_API_KEY** no ambiente (transcrição). Sem chave ElevenLabs.
- Modelo de recorte `rvm_mobilenetv3_fp32.onnx`: baixado sozinho por `matte_rvm.py` para `~/Developer/video-tools/models/`.

## Regras do ambiente
- **Disco do TEMP cheio** derruba o render do Remotion (ENOSPC: ele copia o `public/` e o bundle de ~500 MB para o TEMP). Com pouco
  espaço, `TEMP`/`TMP` numa pasta de um disco com espaço (`ambiente.json → temp_render`, ou `<edit>/_tmp`), apagar `remotion-v4*` do TEMP,
  e avisar os agentes de painel no prompt.
- `PYTHONUTF8=1` em todo comando Python (acentos no console Windows).
- Rodar os scripts de **dentro de `edit/`** (ou `EDIT_DIR=<edit>`); eles leem `projeto.json` de lá.
- Heredoc no Bash do Windows estraga barra invertida/acento em alguns casos: gravar o script com a ferramenta de arquivo e rodar o arquivo.
- A skill `video-use` é de terceiros e opcional: instalar só com autorização do usuário.
- A pasta desta skill é substituída a cada atualização: preferências, estilos próprios, `ambiente.json` e kits de cliente
  ficam fora dela (`scripts/preferencias.py onde`).
- Bundle do Remotion pesa ≈ 500 MB no TEMP: um bundle só para vários stills (`stills.mjs`), nunca `npx remotion still` por frame.

## Erros conhecidos
| Sintoma | Causa | Correção |
|---|---|---|
| Transcrição com trecho longo faltando ou repetindo o prompt | `prompt` no Whisper | não usar prompt |
| Legenda atrasa aos poucos | `render.py` do video-use gerou frames a mais | `extract_base.py` (frames exatos) |
| `Legenda fora de sincronia em "x"` | SCRIPT diverge do words.json | ajustar o texto do cue ou `texto.correcoes` |
| `ENOSPC` no render | disco do TEMP cheio | TEMP/TMP num disco com espaço |
| Texto "atrás" aparece acima da cabeça | `paddingTop` não bate com o enquadramento | medir topo da cabeça num still, ajustar `BehindText` |
| Fontes cheias de "almost Arial" | fonte web não carregou | usar `@remotion/google-fonts` (bloqueia o render até carregar) e olhar o still |
| `afftdn` deixa voz "de lata" | `nr` alto demais | ≤ 15; ruído pesado → `arnndn` |
| Estalo nos cortes de áudio | sem fade | `extract_base.py` já aplica 30 ms |
| Pessoa recortada PARADA por vários quadros (texto atrás) e o texto parece "outra fonte" | `OffthreadVideo` lendo `webm` VP9 com alfa repete quadros | recorte em **PNG por quadro** (`matte_rvm.py` já gera em `public/fg/`); conferir com `verificar.py final` |
| `cv2.imread` não abre PNG | caminho com acento (ex.: `Edição`) | `cv2.imdecode(np.fromfile(...))` |
| MP4 final com 2 quadros a menos | `-shortest` na muxagem | `entregar.py` já não usa; ele compara com `cuts.json` |
| `copiar template` apagou `words.json`/`cuts.json` | `cp -r` sobrescreve | `montar_motion.py` não sobrescreve nada |
