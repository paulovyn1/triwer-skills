# Escolha do formato

Este arquivo serve só para decidir com o aluno. Depois da escolha, leia apenas
`modo-html.md` ou `modo-react.md`.

| | HTML único | Projeto React |
|---|---|---|
| Para quem | Quem nunca programou, ou vai subir num construtor/hospedagem simples | Quem tem alguém técnico, já usa Node, ou já tem a página de vendas em React |
| Ambiente | claude.ai e Claude Code | Só Claude Code |
| Modelo de partida | `assets/template-links.html` | `assets/react-kit/` |
| Como abre | Dois cliques no arquivo | `npm install` e `npm run dev` |
| Como publica | Sobe o arquivo e a pasta `img/` em qualquer hospedagem | Vercel compila sozinha, ou compila e sobe a pasta `dist/` |
| Animações | Entrada ao rolar, título palavra por palavra, livro 3D, cards que inclinam, menu, tela que marca itens | As mesmas, com física de mola mais suave |
| Edição depois | Textos direto no HTML, links no bloco `CONFIG` | Tudo num `src/config.js` só |

## Como perguntar

"Tu prefere receber um arquivo que abre direto no navegador e sobe em qualquer
hospedagem, ou um projeto de código para alguém técnico implementar?"

Se a resposta for "não sei", vá de HTML único. Dá para converter depois.

Se o aluno já tem a página de vendas em React feita com a gente, sugira React:
o mesmo projeto pode publicar as duas, e os componentes já existem.
