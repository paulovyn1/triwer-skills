# Escolha do formato

Este arquivo serve só para decidir com o aluno. Depois da escolha, leia apenas
`modo-html.md` ou `modo-react.md`. Instrução de um formato aplicada no outro
quebra a página (caminho de imagem, componente que não existe, comando que o
aluno não tem).

| | HTML único | Projeto React |
|---|---|---|
| Para quem | Quem nunca programou, ou vai colar a página num construtor ou hospedagem | Quem tem alguém técnico para implementar, ou já usa Node |
| Ambiente | claude.ai e Claude Code | Só Claude Code |
| Como abre | Dois cliques no arquivo (a pasta `img/` ao lado) | `npm install` e `npm run dev` |
| Como publica | Sobe `index.html` e `img/` em qualquer hospedagem; na Vercel, sem build | Compila e sobe a pasta `dist/` |
| Animações | Entrada ao rolar, título palavra por palavra, contagem, texto gigante, loops, FAQ | As mesmas, com física de mola e transições mais suaves |
| Edição depois | Texto direto no HTML; links, preço e listas num bloco `CONFIG` | Textos nos componentes; links e preço no `config.js` |
| Fontes | Google Fonts (requisição externa, trocável por arquivos locais) | Embutidas pelo pacote `@fontsource` |

A estrutura, o visual e a copy são os mesmos nos dois formatos: o CSS do HTML é
gerado a partir do `styles.css` do kit React.

## Como perguntar
"Tu prefere receber um arquivo que abre direto no navegador e sobe em qualquer
hospedagem, ou um projeto de código para alguém técnico implementar no teu site?"

Se a resposta for "não sei", ou se o ambiente for o chat (claude.ai), vá de HTML
único. Dá para converter depois colando a copy e os dados no kit React.
