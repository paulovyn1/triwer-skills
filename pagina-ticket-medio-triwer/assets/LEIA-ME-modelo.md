# Página de vendas: [Nome do produto], de [Nome do expert]

[Projeto React + Vite com animações em Motion | Arquivo HTML único com a pasta `img/`].

No ar: [URL publicada]

## O que falta preencher

[Lista do que ainda está vazio ou "#", um por linha: link do checkout, WhatsApp
da equipe, CNPJ, link da VSL, depoimentos, fonte dos números de mercado.]

## Onde trocar cada coisa

[React] Tudo que muda sem mexer no layout fica em `src/config.js`: links, preço,
parcelas, dias de garantia, empresas, conta do custo e depoimentos.
Os textos ficam em `src/components/Sections.jsx` (e `Hero.jsx` para o topo).
Imagens em `public/img/`. Cores e fontes em `src/styles.css`, bloco `:root`.

[HTML] Links, preço, parcelas, garantia, empresas, conta do custo e depoimentos
ficam no bloco `CONFIG`, no fim do `index.html`. Textos direto no HTML. Imagens na
pasta `img/` ao lado do arquivo. Cores no bloco `:root` do `<style>`.

O preço só aparece no bloco "Recapitulando" e no cartão de preço. Não ponha
preço no topo, nos botões nem na descrição da página.

## Como publicar depois de mudar algo

[React] Os textos e links ficam dentro do código compilado, então trocar só na
pasta `dist/` não funciona. Edite os arquivos acima e:

- **Vercel:** rode `vercel --prod` nesta pasta. A Vercel instala, compila e
  publica sozinha, sem `npm install` na máquina.
- **Outra hospedagem:** com Node 18+, rode `npm install` e `npm run build` e suba
  o conteúdo de `dist/`. Para subpasta: `npx vite build --base=/caminho/`.

A pasta `dist/` deste pacote é a versão que está no ar hoje.

[HTML] Suba `index.html` e a pasta `img/` em qualquer hospedagem estática. Para
mudar algo, edite o arquivo e suba de novo.

## Rodar local
[React]
```
npm install
npm run dev      # abre em http://localhost:5173
```
[HTML] Abra o `index.html` no navegador (duplo clique).

## Fontes
[Fontes usadas e licença. Se a fonte da marca não tinha licença comercial, dizer
qual foi usada no lugar e por quê.]
