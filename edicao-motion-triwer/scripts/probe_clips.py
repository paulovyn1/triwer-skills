"""Transcreve janelas curtas isoladas (Groq whisper-large-v3) pra checar gaguejo/repetição pontual."""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

src = sys.argv[1]
wins = [tuple(map(float, w.split(":"))) for w in sys.argv[2:]]
key = os.environ["GROQ_API_KEY"]
for a, b in wins:
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "c.flac"
        subprocess.run(["ffmpeg", "-y", "-ss", str(a), "-to", str(b), "-i", src, "-ac", "1", "-ar", "16000",
                        "-c:a", "flac", str(f)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(f, "rb") as fh:
            r = requests.post("https://api.groq.com/openai/v1/audio/transcriptions",
                              headers={"Authorization": f"Bearer {key}"},
                              files={"file": ("c.flac", fh, "audio/flac")},
                              data=[("model", "whisper-large-v3"), ("language", "pt"),
                                    ("response_format", "verbose_json"), ("temperature", "0"),
                                    ("timestamp_granularities[]", "word")], timeout=120)
        j = r.json()
        ws = " ".join(f"{w['word'].strip()}[{a + w['start']:.2f}-{a + w['end']:.2f}]" for w in j.get("words", []))
        print(f"{a:.2f}-{b:.2f}: {ws}")
