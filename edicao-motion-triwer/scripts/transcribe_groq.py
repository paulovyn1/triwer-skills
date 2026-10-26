"""Transcrição palavra a palavra via Groq (whisper-large-v3), salva no formato do Scribe
para os helpers do video-use (pack_transcripts.py, render.py) lerem sem mudança.

Uso: python transcribe_groq.py <video> [--edit-dir DIR]
"""
from __future__ import annotations

import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

URL = "https://api.groq.com/openai/v1/audio/transcriptions"
# Prompt em estilo verbatim: induz o Whisper a manter hesitações e repetições.
PROMPT = "Então, é... eu, eu vou, vou te falar, né? Hum, tipo assim, ahn... logística, supply chain."


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--edit-dir", type=Path, default=None)
    args = ap.parse_args()
    video = args.video.resolve()
    edit = (args.edit_dir or video.parent / "edit").resolve()
    out = edit / "transcripts" / f"{video.stem}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        print(f"cached: {out}")
        return
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        sys.exit("GROQ_API_KEY ausente")
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.flac"
        subprocess.run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
                        "-c:a", "flac", str(wav)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(wav, "rb") as f:
            r = requests.post(URL, headers={"Authorization": f"Bearer {key}"},
                              files={"file": ("a.flac", f, "audio/flac")},
                              data=[("model", "whisper-large-v3"), ("language", "pt"),
                                    ("response_format", "verbose_json"), ("temperature", "0"),
                                    
                                    ("timestamp_granularities[]", "word"),
                                    ("timestamp_granularities[]", "segment")],
                              timeout=600)
    if r.status_code != 200:
        sys.exit(f"Groq {r.status_code}: {r.text[:500]}")
    g = r.json()
    words = []
    prev_end = None
    for w in g.get("words", []):
        s, e = float(w["start"]), float(w["end"])
        if prev_end is not None and s > prev_end:
            words.append({"text": " ", "start": prev_end, "end": s, "type": "spacing",
                          "speaker_id": "speaker_0"})
        words.append({"text": w["word"].strip(), "start": s, "end": e, "type": "word",
                      "speaker_id": "speaker_0"})
        prev_end = e
    payload = {"language_code": "pt", "text": g.get("text", ""), "words": words,
               "segments": g.get("segments", []), "engine": "groq/whisper-large-v3"}
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"saved {out} ({sum(1 for w in words if w['type'] == 'word')} palavras)")


if __name__ == "__main__":
    main()
