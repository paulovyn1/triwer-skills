"""Registro das músicas já entregues, por cliente: o escolher_musica.py pune repetir faixa para o mesmo cliente.

Fica na pasta de dados do usuário, fora da skill (_dados.py): <dados>/musicas_usadas.json
    {"Cliente X": [{"video": "Criativo 2", "data": "2026-10-19", "versao": "A", "ids": ["568", "34"]}, ...]}
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dados import DADOS  # noqa: E402

ARQ = DADOS / "musicas_usadas.json"


def carregar() -> dict:
    return json.loads(ARQ.read_text(encoding="utf-8")) if ARQ.exists() else {}


def ids_da_versao(c: dict, opt: str) -> list:
    m = c.get("musica", {})
    if opt in m.get("versoes", {}):
        return [str(f["id"]) for f in m["versoes"][opt]["faixas"]]
    p = m.get("pares", {}).get(opt)
    return [str(p["tensao"]), str(p["virada"])] if p else []


def registrar_musicas(c: dict, opt: str, data: str) -> None:
    ids = ids_da_versao(c, opt)
    cli = (c.get("cliente") or "sem cliente").strip()
    if not ids:
        return
    d = carregar()
    lst = d.setdefault(cli, [])
    item = {"video": c.get("nome", ""), "data": data, "versao": opt, "ids": ids}
    if not any(x.get("video") == item["video"] and x.get("versao") == opt for x in lst):
        lst.append(item)
        ARQ.parent.mkdir(parents=True, exist_ok=True)
        ARQ.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"música registrada para {cli}: {opt} {ids}")
