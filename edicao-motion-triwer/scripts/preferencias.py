"""Preferências que a skill aprende com cada usuário (pasta de dados fora da skill; ver _dados.py).

    python preferencias.py iniciar [--nome "Fulano"]     cria a pasta de dados (preferencias.md, ambiente.json, estilos/, ...)
    python preferencias.py onde                          mostra a pasta e o que tem nela
    python preferencias.py mostrar [--estilo id] [--cliente nome] [--tudo]
        só as regras que valem para ESTE vídeo (globais + do estilo + do cliente), agrupadas por seção. É o que a skill lê
        no começo de cada vídeo: barato, sem abrir o arquivo inteiro.
    python preferencias.py registrar "<regra>" --tipo gosto|evitar|processo|audio|estilos|ambiente
        [--estilo id] [--cliente nome] [--origem "vídeo X"]
        grava a regra (com data) na seção certa. Não duplica regra igual.
    python preferencias.py estilos                       lista os estilos da skill e os próprios do usuário (o próprio vence)

Quando registrar: o usuário pediu um ajuste que revela GOSTO ou PADRÃO ("não gosto de X", "sempre faça Y", "isso ficou
robótico", "prefiro..."), e não um conserto pontual daquele vídeo. Na dúvida, registrar com --cliente ou --estilo (escopo menor).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dados import DADOS  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
ARQ = DADOS / "preferencias.md"
SECOES = {
    "gosto": "## Gosto (fazer)",
    "evitar": "## Evitar",
    "processo": "## Processo (como trabalhar comigo)",
    "audio": "## Áudio e voz",
    "estilos": "## Estilos",
    "ambiente": "## Ambiente",
}
TAG = re.compile(r"\[(estilo|cliente):([^\]]+)\]")


def slug(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def iniciar(nome: str | None) -> None:
    DADOS.mkdir(parents=True, exist_ok=True)
    (DADOS / "estilos").mkdir(exist_ok=True)
    if not ARQ.exists():
        txt = (SKILL / "template" / "preferencias.md").read_text(encoding="utf-8")
        if nome:
            txt = txt.replace("# Preferências de edição", f"# Preferências de edição de {nome}", 1)
        ARQ.write_text(txt, encoding="utf-8")
    amb = DADOS / "ambiente.json"
    if not amb.exists():
        det = {
            "cache": str(Path.home() / ".cache" / "edicao-motion-triwer"),
            "temp_render": None,
            "venv_python": None,
            "porta_remotion": 3090,
            "ffmpeg": shutil.which("ffmpeg"),
            "node": shutil.which("node"),
            "yt_dlp": shutil.which("yt-dlp"),
            "tts_local": None,
            "_obs": "caminhos desta máquina; null = padrão. temp_render: pasta com espaço para os renders (TEMP/TMP).",
        }
        amb.write_text(json.dumps(det, ensure_ascii=False, indent=1), encoding="utf-8")
    for nome_arq, txt in {
        "referencias.md": "# Vídeos de referência por estilo\n\n| estilo | vídeo | observação |\n|---|---|---|\n",
        "termos_pessoais.txt": "# um termo por linha (nome, marca, cliente, caminho). checar_pessoal.py procura na skill antes de compartilhar\n",
    }.items():
        if not (DADOS / nome_arq).exists():
            (DADOS / nome_arq).write_text(txt, encoding="utf-8")
    onde()


def onde() -> None:
    print(DADOS)
    if DADOS.exists():
        for p in sorted(DADOS.rglob("*")):
            if p.is_file():
                print("  ", p.relative_to(DADOS), f"({p.stat().st_size} B)")
    else:
        print("  (não existe; rodar: preferencias.py iniciar)")


def linhas_por_secao() -> dict[str, list[str]]:
    if not ARQ.exists():
        return {}
    sec, out = None, {}
    for ln in ARQ.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            sec = ln.strip()
            out.setdefault(sec, [])
        elif sec and ln.strip().startswith("- "):
            out[sec].append(ln.strip())
    return out


def vale(ln: str, estilo: str | None, cliente: str | None) -> bool:
    tags = TAG.findall(ln)
    if not tags:
        return True
    for k, v in tags:
        if k == "estilo" and (not estilo or slug(v) != slug(estilo)):
            return False
        if k == "cliente" and (not cliente or slug(v) != slug(cliente)):
            return False
    return True


def mostrar(estilo: str | None, cliente: str | None, tudo: bool) -> None:
    if not ARQ.exists():
        print(f"sem preferências ainda ({ARQ}). Rodar: preferencias.py iniciar")
        return
    total = 0
    for sec, lns in linhas_por_secao().items():
        ok = lns if tudo else [x for x in lns if vale(x, estilo, cliente)]
        if ok:
            print(sec)
            print("\n".join(ok))
            total += len(ok)
    proprio = DADOS / "estilos" / f"{estilo}.md" if estilo else None
    if proprio and proprio.exists():
        print(f"\n(estilo próprio do usuário: {proprio} substitui estilos/{estilo}.md da skill)")
    print(f"\n[{total} regra(s) para estilo={estilo or '-'} cliente={cliente or '-'}]")
    if sum(len(v) for v in linhas_por_secao().values()) > 60:
        print("AVISO: mais de 60 regras; consolidar (juntar repetidas, apagar as que a mais nova contradiz).")


def registrar(regra: str, tipo: str, estilo: str | None, cliente: str | None, origem: str | None) -> None:
    if not ARQ.exists():
        iniciar(None)
    alvo = SECOES[tipo]
    tags = (f"[estilo:{slug(estilo)}] " if estilo else "") + (f"[cliente:{cliente.strip()}] " if cliente else "")
    linha = f"- {tags}{regra.strip()} ({dt.date.today().isoformat()}" + (f", {origem})" if origem else ")")
    txt = ARQ.read_text(encoding="utf-8")
    nucleo = slug(regra)
    if any(slug(TAG.sub("", x)).startswith(nucleo[:60]) for v in linhas_por_secao().values() for x in [y[2:] for y in v]):
        print("já registrada (nada mudou):", regra)
        return
    lns = txt.splitlines()
    if alvo not in lns:
        lns += ["", alvo, ""]
    i = lns.index(alvo) + 1
    while i < len(lns) and not lns[i].startswith("## "):
        i += 1
    while i > 0 and not lns[i - 1].strip():  # encosta na última regra da seção
        i -= 1
    lns.insert(i, linha)
    ARQ.write_text("\n".join(lns) + "\n", encoding="utf-8")
    print("registrada:", linha)


def estilos() -> None:
    base = {p.stem: p for p in (SKILL / "estilos").glob("*.md") if not p.stem.startswith("_") and p.stem not in ("INDICE", "gramatica")}
    prop = {p.stem: p for p in (DADOS / "estilos").glob("*.md")} if (DADOS / "estilos").exists() else {}
    for k in sorted(set(base) | set(prop)):
        p = prop.get(k) or base[k]
        titulo = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        print(f"{k:22} {'(próprio)' if k in prop else '        '} {titulo}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("iniciar")
    a.add_argument("--nome")
    sub.add_parser("onde")
    sub.add_parser("estilos")
    m = sub.add_parser("mostrar")
    m.add_argument("--estilo")
    m.add_argument("--cliente")
    m.add_argument("--tudo", action="store_true")
    r = sub.add_parser("registrar")
    r.add_argument("regra")
    r.add_argument("--tipo", required=True, choices=list(SECOES))
    r.add_argument("--estilo")
    r.add_argument("--cliente")
    r.add_argument("--origem")
    x = ap.parse_args()
    if x.cmd == "iniciar":
        iniciar(x.nome)
    elif x.cmd == "onde":
        onde()
    elif x.cmd == "estilos":
        estilos()
    elif x.cmd == "mostrar":
        mostrar(x.estilo, x.cliente, x.tudo)
    else:
        registrar(x.regra, x.tipo, x.estilo, x.cliente, x.origem)


if __name__ == "__main__":
    main()
