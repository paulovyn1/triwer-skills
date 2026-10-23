# Página de links de [Nome do expert]

[Projeto React + Vite com animações em Motion | Arquivo HTML único].

No ar: [URL publicada]

## O que falta preencher

[Lista dos links ainda em "#", um por linha, com o que precisa ser colocado.]

## Onde trocar cada coisa

[React] Todo o conteúdo (textos, links, ordem dos cards, redes) fica em `src/config.js`.
Imagens em `public/img/`. Cores e fontes em `src/styles.css`, no bloco `:root`.

[HTML] Links no bloco `CONFIG`, no fim do arquivo. Textos direto no HTML.
Imagens na pasta `img/` ao lado do arquivo.

## Como publicar depois de mudar algo

[React] Os textos e links ficam dentro do código compilado, então trocar só na
pasta `dist/` não funciona. Edite `src/config.js` e:

- **Vercel:** rode `vercel --prod` nesta pasta. A Vercel instala, compila e
  publica sozinha, sem `npm install` na máquina.
- **Outra hospedagem:** com Node 18+, rode `npm install` e `npm run build` e
  suba o conteúdo de `dist/`. Para subpasta: `npx vite build --base=/caminho/`.

A pasta `dist/` deste pacote é a versão que está no ar hoje.

[HTML] Suba o arquivo e a pasta `img/` em qualquer hospedagem estática.

## Fontes

[Fontes usadas e licença. Se a fonte da marca não tinha licença comercial, dizer
qual foi usada no lugar e por quê.]
