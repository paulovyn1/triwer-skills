# Modo HTML único

Leia só este arquivo nas fases 4 e 5 quando o formato escolhido for HTML.

## Montagem
1. Copie `assets/template-pagina.html` para a pasta do aluno com o nome que ele
   quiser (ex.: `index.html`). Nunca edite o template original da skill.
2. **Tokens**: troque as variáveis em `:root` (cores, `--dst-rgb` e `--alr-rgb`
   em RGB, fontes). Troque o `<link>` do Google Fonts pelas fontes escolhidas.
3. **Copy**: substitua cada `[COLCHETE]` pelo texto aprovado. Seção sem material:
   apague o `<section>` inteiro (cada uma está marcada com um comentário `SEÇÃO`).
4. **Destaques**: `data-hl="2,3"` destaca as palavras de índice 2 e 3 do título
   (começa em 0, pontuação colada conta como parte da palavra). Recalcule em todo
   título que mudar.
5. **Fundo do hero**: troque os traços do `<svg class="hero-fundo">` por um
   elemento gráfico da capa do aluno, ou apague o SVG se a capa não tiver nada
   reaproveitável. Cada traço precisa de `pathLength="1"` para se desenhar.
6. **Calculadora**: edite `CONFIG.calc` no script (cenários com rótulo, valor de
   hoje, valor que poderia ser e legendas; `multiplicador` 12 para mês a ano).
   Se o nicho não for em dinheiro, troque `brl` por um formatador próprio.
7. **Links**: `CONFIG.checkout` e `CONFIG.whatsapp`. Todos os botões de compra
   leem o mesmo link.
8. **Páginas internas**: troque cada `.pg` desenhada por
   `<div class="pg"><img src="img/paginas/01.webp" alt="Página 1"></div>`.

## Imagens
Use a pasta `img/` ao lado do HTML, com os nomes do template (`capa.webp`,
`logo.svg`, `expert-hero.webp`, `expert-2.webp`...). Imagem que ainda não existe
fica invisível em vez de mostrar ícone quebrado.

- Com terminal: otimize com `node scripts/otimizar-imagens.mjs <pasta-origem> <pasta img>`
  (precisa de `npm i sharp` numa pasta de ferramentas).
- No claude.ai: peça ao aluno as imagens já em JPG/WebP leves e diga o nome
  exato de cada arquivo e onde salvar.
- Só embuta imagens em base64 se o aluno precisar de um arquivo único sem pasta.
  Nesse caso, mantenha o total abaixo de ~5 MB.

## Revisão
- Com terminal: sirva a pasta (`npx serve <pasta>` ou `npx http-server`) e rode
  `node scripts/prints.mjs <url> <saída>` (precisa de `npm i puppeteer-core` e de
  Chrome instalado). Ele tira prints em 1440, 412 e 360px rolando a página.
- Sem terminal: peça ao aluno para abrir o arquivo no celular e no computador e
  mandar print do hero, da calculadora e da oferta.

## Entrega
- O `.html` + a pasta `img/`, compactados num zip.
- Diga ao aluno onde trocar os links (bloco `CONFIG` no fim do arquivo).
- Para publicar: qualquer hospedagem estática aceita (subir o zip descompactado).
