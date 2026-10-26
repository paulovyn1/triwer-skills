"""Segunda opinião local (faster-whisper) com palavras e tempos: relógio mais preciso das bordas e detector de gaguejo/repetição.

Uso: python fw_check.py work/orig.wav [small] [transcripts/fw_small_words.json]
O áudio é decodificado aqui (librosa, 16 kHz) e entregue como array: não depende do PyAV, cuja versão 19 quebrou o
`decode_audio` do faster-whisper 1.2 ("metadata_errors"); antes isso falhava em silêncio dentro do preparar.py.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import json
import sys

import librosa
import numpy as np
from faster_whisper import WhisperModel

path = sys.argv[1]
size = sys.argv[2] if len(sys.argv) > 2 else "small"
audio = librosa.load(path, sr=16000, mono=True)[0].astype(np.float32)
m = WhisperModel(size, device="cpu", compute_type="int8")
segs, info = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False,
                          condition_on_previous_text=False, temperature=0,
                          initial_prompt="Ééé... então, eu, eu, ahn, é... Pa-para de... hum.")
out = []
for s in segs:
    for w in s.words:
        out.append(f"{w.word.strip()}[{w.start:.2f}-{w.end:.2f}]")
print(" ".join(out))
if len(sys.argv) > 3:
    segs2, _ = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False,
                            condition_on_previous_text=False, temperature=0)
    json.dump([{"text": w.word.strip(), "start": w.start, "end": w.end} for s in segs2 for w in s.words],
              open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
