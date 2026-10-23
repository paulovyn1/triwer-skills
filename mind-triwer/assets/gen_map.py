"""Gerador de .mind para o MindMeister (identidade Triwer).

Uso:
    python gen_map.py conteudo.py saida.mind

`conteudo.py` define MAP com a função n(titulo, *filhos):

    def n(title, *kids): return (title, *kids)
    MAP = n("Título central",
      n("Bloco 1",
        n("Subtópico", n("Detalhe"))))

O script monta o map.json, empacota o .mind (zip com map.json) e imprime
estatísticas para conferência antes de entregar.
"""
import json, runpy, statistics, sys, zipfile

F = [{"id": 1, "name": "Avenir", "url": None}, {"id": 2, "name": "Segoe UI", "url": None},
     {"id": 3, "name": "Helvetica", "url": None}, {"id": 4, "name": "Arial", "url": None},
     {"id": 5, "name": "sans-serif", "url": None}]


def sA(lc):
    return {"color": None, "backgroundColor": "transparent", "borderColor": "transparent", "boxStyle": None,
            "bold": True, "italic": False, "fontSize": None, "borderWidth": None, "line_position": None,
            "line_width": 4, "line_type": "rounded", "line_color": lc, "border_style": None, "image_color": None,
            "line_style": "solid", "fonts": F, "gradient": 0, "boxShadow": False, "name": None}


def sB():
    return {"color": None, "backgroundColor": None, "borderColor": None, "boxStyle": None, "bold": True,
            "italic": False, "fontSize": None, "borderWidth": None, "line_position": None, "line_width": None,
            "line_type": None, "line_color": "421900", "border_style": None, "image_color": None,
            "line_style": None, "fonts": F, "gradient": 0, "boxShadow": False, "name": None}


def sRoot():
    return {"color": "421900", "backgroundColor": "FFF8F3", "borderColor": None, "boxStyle": None, "bold": False,
            "italic": False, "fontSize": None, "borderWidth": None, "line_position": None, "line_width": None,
            "line_type": None, "line_color": None, "border_style": None, "image_color": None, "line_style": None,
            "fonts": F, "gradient": 0, "boxShadow": False, "name": None}


TASK = {"from": None, "until": None, "resource": None, "effort": None, "notify": 1}
THEME = {"name": "meister",
         "root_style": {"id": 1572841377, "fonts": F, "fontSize": 150, "boxStyle": 1, "color": "3D474D", "backgroundColor": None, "borderColor": None, "bold": True, "italic": False, "gradient": 0, "boxShadow": False, "borderWidth": 1, "name": None},
         "root_children_style": {"id": 1572841378, "fonts": F, "fontSize": 120, "boxStyle": 1, "color": "3D474D", "backgroundColor": None, "borderColor": None, "bold": False, "italic": False, "gradient": 0, "boxShadow": False, "borderWidth": 1, "name": None},
         "nodes_style": {"id": 1572841379, "fonts": F, "fontSize": 120, "boxStyle": 1, "color": "3D474D", "backgroundColor": None, "borderColor": None, "bold": False, "italic": False, "gradient": 0, "boxShadow": False, "borderWidth": 1, "name": None},
         "root_selected_color": "00aaff", "root_children_selected_color": "00aaff", "nodes_selected_color": "00aaff",
         "background": {"image": None, "color": "ffffff", "repeat": True}, "line": {"color": "18304E", "style": 2},
         "id": 2861357, "styles": [], "boundary_styles": [],
         "thumbnail": "https://www.mindmeister.com/themes/mm19/meister.svg", "colors": ["ffffff", "18304E", "3D474D"]}

_id = [4000000001]


def build(spec, depth, rank):
    title, kids = spec[0], spec[1:]
    i = _id[0]
    _id[0] += 1
    if depth == 0:
        style, layout, pos = sRoot(), "mind_map", [None, None]
    elif depth == 1:
        style = sA("3D474D") if rank == 1 else (sB() if rank % 2 == 0 else sA("421900"))
        layout, pos = None, [450, (rank - 1) * 400]
    elif depth == 2:
        style, layout, pos = None, None, [900, (rank - 1) * 200]
    else:
        style, layout, pos = None, None, [1350, (rank - 1) * 150]
    children = [build(k, depth + 1, r) for r, k in enumerate(kids, 1)]
    return {"id": i, "title": title, "note": None, "link": None, "pos": pos, "rank": rank if depth else None,
            "style": style, "task": TASK, "external_task": None, "attachments": [], "boundary": None,
            "video": None, "icon": None, "image": None,
            "property": {"id": i + 10000000, "idea_id": i, "layout": layout}, "children": children}


def walk(nd, d=0):
    yield nd["title"], d
    for c in nd["children"]:
        yield from walk(c, d + 1)


def main():
    content, out = sys.argv[1], sys.argv[2]
    root = build(runpy.run_path(content)["MAP"], 0, None)
    doc = {"map_version": "3.0", "layout": 1, "theme": THEME, "custom_colors": ["#421900", "#b3b3b3"],
           "connections": [], "slides": [], "attachments": [], "images": [], "root": root}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("map.json", json.dumps(doc, ensure_ascii=False, indent=2))
    items = list(walk(root))
    lens = [len(t) for t, _ in items]
    print(f"nós: {len(items)} | caracteres por nó: mediana {statistics.median(lens)}, média {round(statistics.mean(lens))} | profundidade máxima: {max(d for _, d in items)}")
    print("com travessão:", [t for t, _ in items if "—" in t])
    print("terminando em ponto final:", [t for t, _ in items if t.endswith(".") and not t.endswith("...")])
    print("arquivo:", out)


if __name__ == "__main__":
    main()
