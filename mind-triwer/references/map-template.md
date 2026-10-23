# Referência: map-template

Este arquivo contém os blocos estáticos do `map.json`. Copie-os literalmente —
eles têm IDs fixos do MindMeister e qualquer alteração quebra o tema ou o formato.

---

## Bloco `theme` completo

Cole este bloco no campo `"theme"` do `map.json`:

```json
{
  "name": "meister",
  "root_style": {
    "id": 1572841377,
    "fonts": [
      {"id":1,"name":"Avenir","url":null},
      {"id":2,"name":"Segoe UI","url":null},
      {"id":3,"name":"Helvetica","url":null},
      {"id":4,"name":"Arial","url":null},
      {"id":5,"name":"sans-serif","url":null}
    ],
    "fontSize": 150,
    "boxStyle": 1,
    "color": "3D474D",
    "backgroundColor": null,
    "borderColor": null,
    "bold": true,
    "italic": false,
    "gradient": 0,
    "boxShadow": false,
    "borderWidth": 1,
    "name": null
  },
  "root_children_style": {
    "id": 1572841378,
    "fonts": [
      {"id":1,"name":"Avenir","url":null},
      {"id":2,"name":"Segoe UI","url":null},
      {"id":3,"name":"Helvetica","url":null},
      {"id":4,"name":"Arial","url":null},
      {"id":5,"name":"sans-serif","url":null}
    ],
    "fontSize": 120,
    "boxStyle": 1,
    "color": "3D474D",
    "backgroundColor": null,
    "borderColor": null,
    "bold": false,
    "italic": false,
    "gradient": 0,
    "boxShadow": false,
    "borderWidth": 1,
    "name": null
  },
  "nodes_style": {
    "id": 1572841379,
    "fonts": [
      {"id":1,"name":"Avenir","url":null},
      {"id":2,"name":"Segoe UI","url":null},
      {"id":3,"name":"Helvetica","url":null},
      {"id":4,"name":"Arial","url":null},
      {"id":5,"name":"sans-serif","url":null}
    ],
    "fontSize": 120,
    "boxStyle": 1,
    "color": "3D474D",
    "backgroundColor": null,
    "borderColor": null,
    "bold": false,
    "italic": false,
    "gradient": 0,
    "boxShadow": false,
    "borderWidth": 1,
    "name": null
  },
  "root_selected_color": "00aaff",
  "root_children_selected_color": "00aaff",
  "nodes_selected_color": "00aaff",
  "background": {"image": null, "color": "ffffff", "repeat": true},
  "line": {"color": "18304E", "style": 2},
  "id": 2861357,
  "styles": [],
  "boundary_styles": [],
  "thumbnail": "https://www.mindmeister.com/themes/mm19/meister.svg",
  "colors": ["ffffff", "18304E", "3D474D"]
}
```

---

## Campos estáticos de todo nó (copiar idênticos)

Estes campos têm o mesmo valor em todos os nós — root, filhos e netos:

```json
"task": {"from": null, "until": null, "resource": null, "effort": null, "notify": 1},
"external_task": null,
"attachments": [],
"boundary": null,
"video": null,
"icon": null
```

O campo `image` é `null` por padrão (ver visual-identity.md para nós com imagem).

---

## Array de fontes (dentro de qualquer objeto `style`)

Sempre que um nó tiver `style` não-nulo, incluir este array no campo `fonts`:

```json
"fonts": [
  {"id":1,"name":"Avenir","url":null},
  {"id":2,"name":"Segoe UI","url":null},
  {"id":3,"name":"Helvetica","url":null},
  {"id":4,"name":"Arial","url":null},
  {"id":5,"name":"sans-serif","url":null}
]
```

---

## Campos de nível superior do `map.json` (estrutura completa)

```json
{
  "map_version": "3.0",
  "layout": 1,
  "theme": { ... },
  "custom_colors": ["#421900", "#b3b3b3"],
  "connections": [],
  "slides": [],
  "attachments": [],
  "images": [],
  "root": { ... }
}
```

`map_version`, `layout`, `connections`, `slides`, `attachments`, `images` — nunca alterar.
`custom_colors` — fixo para identidade Triwer.
