# Referência: identidade visual do mapa

Estilos exatos validados no MindMeister. O gerador (`assets/gen_map.py`) já
aplica tudo isto; leia só se for mexer no formato à mão.
Copiar os objetos `style` literalmente — incluindo todos os campos `null`.

## Cores

Duas cores definem o mapa. O gerador as lê de `PALETA` no `conteudo.py`
(hex sem `#`); sem `PALETA`, usa o cinza neutro:

| Token | Para que serve | Padrão neutro |
|---|---|---|
| `{marca}` | linhas dos blocos e texto do nó central | `3D474D` |
| `{fundo}` | fundo claro do nó central | `F5F5F5` |

Nos blocos abaixo, `{marca}` e `{fundo}` são esses dois valores.

---

## Root (nó central)

```json
"style": {
  "color": "{marca}",
  "backgroundColor": "{fundo}",
  "borderColor": null,
  "boxStyle": null,
  "bold": false,
  "italic": false,
  "fontSize": null,
  "borderWidth": null,
  "line_position": null,
  "line_width": null,
  "line_type": null,
  "line_color": null,
  "border_style": null,
  "image_color": null,
  "line_style": null,
  "fonts": [
    {"id":1,"name":"Avenir","url":null},
    {"id":2,"name":"Segoe UI","url":null},
    {"id":3,"name":"Helvetica","url":null},
    {"id":4,"name":"Arial","url":null},
    {"id":5,"name":"sans-serif","url":null}
  ],
  "gradient": 0,
  "boxShadow": false,
  "name": null
}
```

Root também tem `"property": {..., "layout": "mind_map"}` — único nó com esse valor.

---

## Nível 1 — Padrão A (rank ímpar: 1, 3, 5…)

Linha grossa rounded. Fundo transparente (sem caixa visível em volta do texto).
`line_color` é sempre `{marca}`.

```json
"style": {
  "color": null,
  "backgroundColor": "transparent",
  "borderColor": "transparent",
  "boxStyle": null,
  "bold": true,
  "italic": false,
  "fontSize": null,
  "borderWidth": null,
  "line_position": null,
  "line_width": 4,
  "line_type": "rounded",
  "line_color": "{marca}",
  "border_style": null,
  "image_color": null,
  "line_style": "solid",
  "fonts": [
    {"id":1,"name":"Avenir","url":null},
    {"id":2,"name":"Segoe UI","url":null},
    {"id":3,"name":"Helvetica","url":null},
    {"id":4,"name":"Arial","url":null},
    {"id":5,"name":"sans-serif","url":null}
  ],
  "gradient": 0,
  "boxShadow": false,
  "name": null
}
```

---

## Nível 1 — Padrão B (rank par: 2, 4, 6…)

Linha simples sem espessura extra. Sem fundo.

```json
"style": {
  "color": null,
  "backgroundColor": null,
  "borderColor": null,
  "boxStyle": null,
  "bold": true,
  "italic": false,
  "fontSize": null,
  "borderWidth": null,
  "line_position": null,
  "line_width": null,
  "line_type": null,
  "line_color": "{marca}",
  "border_style": null,
  "image_color": null,
  "line_style": null,
  "fonts": [
    {"id":1,"name":"Avenir","url":null},
    {"id":2,"name":"Segoe UI","url":null},
    {"id":3,"name":"Helvetica","url":null},
    {"id":4,"name":"Arial","url":null},
    {"id":5,"name":"sans-serif","url":null}
  ],
  "gradient": 0,
  "boxShadow": false,
  "name": null
}
```

---

## Nível 2+ (netos e mais profundos)

```json
"style": null
```

Herda o estilo global definido no `theme.nodes_style`. Não definir nada aqui —
qualquer objeto colocado aqui sobrescreve o herança e pode quebrar a aparência.

---

## Resumo da regra de estilos por rank

| rank | Padrão | line_color |
|------|--------|------------|
| ímpar (1, 3, 5…) | A (rounded) | `{marca}` |
| par (2, 4, 6…) | B (simples) | `{marca}` |

---

## Imagem via URL externa

Usar quando o mapa precisa de imagem mas o arquivo `.bin` não está disponível.
Funciona no MindMeister web. A URL precisa ser pública e estável.

```json
"image": {
  "id": 999000001,
  "url": "https://url-publica-da-imagem.jpg",
  "image_file_id": null,
  "width": 280,
  "height": 210,
  "source": "url",
  "position": null,
  "base_url": "https://url-publica-da-imagem.jpg"
}
```

Incrementar `id` sequencialmente (ex: 999000001, 999000002…).
`url` e `base_url` devem ter o mesmo valor.
Fontes seguras: Google Drive (link público), Imgur, Notion.
