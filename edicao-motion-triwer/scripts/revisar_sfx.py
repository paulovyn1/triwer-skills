"""Revisão de efeitos sonoros pelo usuário: cada efeito ganha um NÚMERO que ele vê no vídeo e ouve na página.

Uso (de dentro de edit/, depois do entregar.py):
    python revisar_sfx.py [video.mp4]      # sem caminho: o .mp4 mais novo de ../entrega
Gera:
  1. ../entrega/revisao/<vídeo> - efeitos numerados.mp4: o vídeo com "#12 · tampa bate · door_shut" na tela por ~1 s em cada efeito;
  2. edit/revisao/efeitos.html: uma linha por efeito com o quadro, a nota, o som atual e 3 alternativas (a, b, c) do Mixkit para ouvir;
  3. edit/revisao/alternativas.json (para `sfx.py trocar 12 b`).
O usuário responde no chat: "#12 b", "#20 tirar", "#33 mais baixo", "#7 mais cedo". Aplicar com sfx.py (trocar/remover/ganho/mover),
mix.py e entregar.py <opção> "<nome>" (só remux, sem --render). Catálogo para conhecer os nomes: python revisar_sfx.py --catalogo
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

from _cfg import CACHE_LIB, EDIT, LIB, cfg
from mixkit import baixar, sfx_catalogo, url_sfx
from sfx import buscar, catalogo

SFX = LIB / "sfx"
FONTE = "C\\:/Windows/Fonts/arialbd.ttf" if Path("C:/Windows/Fonts/arialbd.ttf").exists() else "DejaVuSans-Bold.ttf"


def arquivo(ref: str) -> Path:
    if ref.startswith("mixkit:"):
        i = ref.split(":", 1)[1]
        return baixar(url_sfx(i), CACHE_LIB / "sfx" / f"{i}.mp3")
    p = sfx_catalogo(ref, SFX, CACHE_LIB)
    if p:
        return p
    raise FileNotFoundError(ref)


def limpo(s: str) -> str:
    return "".join(ch for ch in s if ch not in "':\\,%;[]=").strip()


def pagina_catalogo() -> None:
    linhas = []
    for r in catalogo():
        f = sfx_catalogo(r["nome"], SFX, CACHE_LIB)
        if f:
            linhas.append(f"<tr><td><b>{r['nome']}</b></td><td>{html.escape(r['uso'])}</td><td><audio controls preload=none src='{f.resolve().as_uri()}'></audio></td></tr>")
    (SFX / "catalogo.html").write_text(CAB.format(t="Catálogo de efeitos") + "<table>" + "".join(linhas) + "</table></body></html>", encoding="utf-8")
    print("catálogo:", SFX / "catalogo.html")


CAB = """<!doctype html><html lang=pt-br><head><meta charset=utf-8><title>{t}</title><style>
body{{font:15px system-ui;background:#0d1526;color:#eef2fb;margin:24px}} table{{border-collapse:collapse;width:100%}}
td{{border-bottom:1px solid #22325a;padding:8px;vertical-align:middle}} img{{width:108px;border-radius:6px}}
.n{{font:800 28px system-ui;color:#f5d90a}} audio{{height:30px;width:210px}} .alt b{{color:#f5d90a}} small{{color:#9aa8c4}}
</style></head><body><h2>{t}</h2>"""

if __name__ == "__main__":
    if "--catalogo" in sys.argv:
        pagina_catalogo()
        sys.exit(0)
    c = cfg()
    p = EDIT / "audio" / "sfx.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    ev = sorted(d["events"], key=lambda e: e["at"])
    prox = max([e.get("n", 0) for e in ev] + [0]) + 1
    for e in ev:  # número estável: quem já tem número mantém
        if not e.get("n"):
            e["n"] = prox
            prox += 1
    d["events"] = ev
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    fps = c.get("fps", 30)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        video = Path(args[0])
    else:
        cands = [v for v in sorted((EDIT.parent / "entrega").glob("*.mp4"), key=lambda v: v.stat().st_mtime, reverse=True)]
        if not cands:
            raise SystemExit("nenhum vídeo em ../entrega")
        video = cands[0]
    rev = EDIT / "revisao"
    (rev / "audio").mkdir(parents=True, exist_ok=True)
    (rev / "img").mkdir(exist_ok=True)

    # 1. vídeo numerado
    filtros, ocupado = [], []  # ocupado[linha] = fim do rótulo que está nela (efeitos próximos ficam em linhas diferentes)
    for e in ev:
        t0, t1 = max(0, (e["at"] - 6) / fps), (e["at"] + 24) / fps
        linha = next((i for i, fim in enumerate(ocupado) if fim <= t0), len(ocupado))
        if linha == len(ocupado):
            ocupado.append(t1)
        else:
            ocupado[linha] = t1
        txt = limpo(f"#{e['n']}  {e.get('note', '')}")[:44] + f"  ({limpo(e['file'])})"
        filtros.append(f"drawtext=fontfile='{FONTE}':text='{txt}':fontsize=36:fontcolor=0xF5D90A:box=1:boxcolor=black@0.85:boxborderw=12:"
                       f"x=(w-tw)/2:y={60 + 70 * linha}:enable='between(t,{t0:.3f},{t1:.3f})'")
    script = rev / "_filtros.txt"
    script.write_text(",\n".join(filtros), encoding="utf-8")
    out_dir = EDIT.parent / "entrega" / "revisao"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{video.stem} - efeitos numerados.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-filter_script:v", str(script),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-c:a", "copy", "-movflags", "+faststart", str(out)], check=True)

    # 2. página com alternativas
    alts, linhas = {}, []
    for e in ev:
        img = rev / "img" / f"{e['n']}.jpg"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{e['at'] / fps:.3f}", "-i", str(video), "-frames:v", "1",
                        "-vf", "scale=216:-1", str(img)], check=False)
        try:
            atual = arquivo(e["file"])
            shutil.copy2(atual, rev / "audio" / f"{e['n']}_atual{atual.suffix}")
            atual_tag = f"<audio controls preload=none src='audio/{e['n']}_atual{atual.suffix}'></audio>"
        except Exception:
            atual_tag = "(arquivo não encontrado)"
        q = e.get("note", "") + " " + e["file"].replace("_", " ")
        cat_id = next((r["id"] for r in catalogo() if r["nome"] == e["file"]), "")
        opcoes = buscar(q, 3, excluir={e["file"], f"mixkit:{cat_id}"})  # nunca oferecer o mesmo som com outro nome
        alts[str(e["n"])] = {}
        cel = []
        for letra, (_, ref, tit, _tags, _dur) in zip("abc", opcoes):
            try:
                f = arquivo(ref)
                shutil.copy2(f, rev / "audio" / f"{e['n']}_{letra}{f.suffix}")
                alts[str(e["n"])][letra] = ref
                cel.append(f"<div class=alt><b>{letra}</b> <small>{html.escape(str(tit))[:34]}</small><br>"
                           f"<audio controls preload=none src='audio/{e['n']}_{letra}{f.suffix}'></audio></div>")
            except Exception:
                continue
        linhas.append(f"<tr><td class=n>#{e['n']}</td><td><img src='img/{e['n']}.jpg'></td><td>{e['at'] / fps:5.2f}s<br>"
                      f"<small>quadro {e['at']}</small></td><td>{html.escape(e.get('note', ''))}<br><small>{html.escape(e['file'])} · {e['gain']} dB</small></td>"
                      f"<td>{atual_tag}</td><td>{''.join(cel)}</td></tr>")
    (rev / "alternativas.json").write_text(json.dumps(alts, ensure_ascii=False, indent=1), encoding="utf-8")
    instr = ("<p>Assista ao vídeo <b>efeitos numerados</b> e responda no chat com o número: <b>#12 b</b> (trocar pela alternativa b), "
             "<b>#20 tirar</b>, <b>#33 mais baixo</b>, <b>#7 mais cedo</b>. Quem decide é o ouvido.</p>")
    (rev / "efeitos.html").write_text(CAB.format(t=f"Efeitos sonoros · {html.escape(c.get('nome', ''))}") + instr +
                                      "<table><tr><th>#</th><th>quadro</th><th>tempo</th><th>o que dispara</th><th>atual</th><th>alternativas</th></tr>"
                                      + "".join(linhas) + "</table></body></html>", encoding="utf-8")
    print("vídeo numerado:", out)
    print("página de escuta:", rev / "efeitos.html")
