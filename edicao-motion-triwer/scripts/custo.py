"""Mede o custo em tokens de cada etapa da edição, lendo o transcript da conversa do Claude Code (opcional, mas recomendado).

Uso (de dentro de edit/):
    python custo.py marca "1-cortes"     # no INÍCIO de cada etapa (grava horário UTC em edit/custo/marcas.jsonl)
    python custo.py relatorio            # tabela por etapa (tokens, contexto médio por mensagem, duração, % do total) e total por modelo

A sessão é detectada sozinha na 1ª marca (o .jsonl mais recente em ~/.claude/projects/*/) e fica gravada; subagentes entram juntos.
Unidade "eq" = tokens equivalentes de entrada: entrada×1 + escrita de cache×2 + leitura de cache×0,1 + saída×5 (pesos aproximados de
preço; vale a PROPORÇÃO entre etapas e entre vídeos, não o valor absoluto). Modelos diferentes têm preços diferentes: compare o eq
dentro do mesmo modelo e veja a coluna por modelo.
Lição do C3: o grosso do custo é "leitura de cache" = nº de mensagens × tamanho do contexto. Menos mensagens > respostas menores.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import datetime
import json
import sys
import time
from pathlib import Path

from _cfg import EDIT

W = dict(inp=1.0, cw=2.0, cr=0.1, out=5.0)
DIR = EDIT / "custo"
MARCAS = DIR / "marcas.jsonl"
PROJ = Path.home() / ".claude" / "projects"


def agora() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def ts(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def sessao_atual() -> Path:
    cands = sorted(PROJ.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not cands:
        raise SystemExit("nenhum transcript em ~/.claude/projects")
    if time.time() - cands[0].stat().st_mtime > 300:
        print("AVISO: o transcript mais recente não foi atualizado nos últimos 5 min; confira se é a conversa certa:", cands[0])
    return cands[0]


def marcas() -> list:
    if not MARCAS.exists():
        return []
    return [json.loads(l) for l in MARCAS.read_text(encoding="utf-8").splitlines() if l.strip()]


def marca(etapa: str) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    ms = marcas()
    sess = ms[0]["sessao"] if ms and ms[0].get("sessao") else str(sessao_atual())
    with MARCAS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": agora(), "etapa": etapa, "sessao": sess}, ensure_ascii=False) + "\n")
    print(f"marca {etapa} | sessão {Path(sess).stem[:8]}…")


def eventos(sess: Path) -> list:
    files = [sess] + sorted((sess.parent / sess.stem).glob("**/*.jsonl"))
    seen, ev = set(), []
    for fp in files:
        sub = fp != sess
        for line in fp.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                d = json.loads(line)
            except Exception:
                continue
            m = d.get("message") or {}
            u = m.get("usage")
            if d.get("type") != "assistant" or not u:
                continue
            k = (m.get("id"), fp.name)
            if k in seen:
                continue
            seen.add(k)
            ev.append((ts(d["timestamp"]), sub, u, m.get("model", "?")))
    ev.sort(key=lambda x: x[0])
    return ev


def soma(lst: list) -> dict:
    r = dict(inp=0, cw=0, cr=0, out=0, n=0)
    for _, _, u, _ in lst:
        r["inp"] += u.get("input_tokens", 0)
        r["cw"] += u.get("cache_creation_input_tokens", 0)
        r["cr"] += u.get("cache_read_input_tokens", 0)
        r["out"] += u.get("output_tokens", 0)
        r["n"] += 1
    r["eq"] = sum(r[k] * W[k] for k in W)
    r["ctx"] = (r["inp"] + r["cw"] + r["cr"]) / r["n"] if r["n"] else 0
    return r


def relatorio() -> None:
    ms = marcas()
    if not ms:
        raise SystemExit("sem marcas: rode `custo.py marca \"0-ambiente\"` no início")
    ev = eventos(Path(ms[0]["sessao"]))
    lim = [ts(m["t"]) for m in ms] + [datetime.datetime.now(datetime.timezone.utc)]
    rows = []
    for i, m in enumerate(ms):
        lst = [e for e in ev if lim[i] <= e[0] < lim[i + 1]]
        rows.append((m["etapa"], soma(lst), (lim[i + 1] - lim[i]).total_seconds() / 60, lst))
    tot = sum(r[1]["eq"] for r in rows) or 1
    print(f"{'etapa':<30}{'msgs':>5}{'ctx/msg':>9}{'saída':>8}{'eq mil':>8}{'%':>6}{'min':>6}")
    for n, r, mins, _ in rows:
        print(f"{n:<30}{r['n']:>5}{r['ctx'] / 1000:>8.0f}k{r['out']:>8}{r['eq'] / 1000:>8.0f}{100 * r['eq'] / tot:>6.1f}{mins:>6.0f}")
    allev = [e for _, _, _, lst in rows for e in lst]
    t = soma(allev)
    print(f"{'TOTAL':<30}{t['n']:>5}{t['ctx'] / 1000:>8.0f}k{t['out']:>8}{t['eq'] / 1000:>8.0f}")
    por = {}
    for e in allev:
        por.setdefault(e[3] + (" (subagente)" if e[1] else ""), []).append(e)
    print("por modelo:", "; ".join(f"{k}: {len(v)} msgs, {soma(v)['eq'] / 1000:.0f} mil eq" for k, v in por.items()))
    (DIR / "relatorio.txt").write_text("\n".join(f"{n}\t{r['n']}\t{r['eq']:.0f}\t{mins:.0f}" for n, r, mins, _ in rows), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "marca":
        marca(sys.argv[2])
    elif len(sys.argv) >= 2 and sys.argv[1] == "relatorio":
        relatorio()
    else:
        print(__doc__)
