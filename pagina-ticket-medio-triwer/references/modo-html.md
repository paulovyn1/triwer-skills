# Modo HTML (arquivo único)

Leia só este arquivo nas fases 4 e 5 quando o formato escolhido for HTML. Não
precisa de terminal para montar: no claude.ai, o resultado é o arquivo
`index.html` mais a pasta `img/`, entregues para baixar. Com terminal (Claude
Code), o fluxo é o mesmo, com mais conferências.

## 1. Montar a partir do modelo
1. Copie `assets/template-pagina.html` para `index.html` e a pasta `assets/img/`
   para `img/` ao lado dele. A pasta `img/` do modelo tem imagens provisórias
   (`expert-1.svg`..`expert-4.svg`, `expert-bio.svg`, `logo.svg`) e a textura
   `grid.webp` usada nos quadros e no player.
2. **Tokens de cor**: no `<style>`, bloco `:root`. Troque pelos da marca do aluno
   (ver `identidade-visual.md`). As fontes vêm do Google Fonts no `<head>`; para
   outra fonte, troque o `<link>` e as variáveis `--display` e `--body`.
3. **Textos**: o modelo é uma página inteira escrita com exemplo anonimizado,
   cada pendência entre [colchetes]. Troque tudo pela copy aprovada. Seções que o
   aluno não terá (por exemplo, depoimentos) ficam escondidas ou saem do arquivo.
4. **Títulos animados**: o atributo `data-words` anima o título palavra por
   palavra, e `data-hl="frase"` destaca em cor a frase indicada. Escreva a frase
   exatamente como está no título, com a pontuação, porque a busca é por palavra.
   Se a frase não bate, nada é destacado (sem erro), então confira a cor.
5. **Bloco `CONFIG`** (fim do arquivo): links (checkout, WhatsApp, VSL), CNPJ,
   preço, parcelas, dias de garantia, conta do custo, empresas, subáreas,
   materiais e depoimentos. Essas listas geram o HTML sozinhas. Tudo que o aluno
   trocará depois fica ali.
6. **Etapas**: cada etapa é um `<article class="etapa reveal">`. Copie e cole um
   por módulo ou semana.
7. **Imagens**: coloque as do aluno em `img/`, ajuste os `src` e otimize
   (`node scripts/otimizar-imagens.mjs <origem> img`, se tiver Node; sem Node,
   WebP até ~1200px de largura por qualquer conversor).
8. **Depoimentos**: preencha `DEPOIMENTOS` no `CONFIG` e a seção aparece. Vazio, ela
   fica escondida. Nunca preencha com texto inventado.

## 2. Revisar
Abra o `index.html` (em Claude Code, sirva a pasta com
`python -m http.server 8765 --directory <pasta>` e abra no navegador; abrir por
duplo clique também funciona). Rode `python scripts/conferir-restos.py <pasta>`
para listar [colchetes] restantes, travessões, números zerados no `CONFIG` e preço
fora da ancoragem. Depois confira com `references/checklist-qualidade.md`, em
1440px, 412px e 360px. Sem terminal, diga ao aluno o que conferir no celular dele
e peça um print se algo parecer estranho.

## 3. Entrega
- **Arquivo e pasta**: `index.html` e `img/`. Zip com
  `python scripts/empacotar.py <pasta> <saida.zip>` (no claude.ai, entregue os
  arquivos para baixar).
- **LEIA-ME**: copie `assets/LEIA-ME-modelo.md` e preencha a parte do modo HTML:
  onde trocar links e preço (bloco `CONFIG`), que a página abre por duplo clique e
  como publicar.
- Para publicar em hospedagem estática, suba os dois itens. Na Vercel, sem build:
  `references/publicacao.md`.

## Limites do modo HTML
- As fontes vêm do Google Fonts: sem internet, a página usa a fonte do sistema.
  Para embutir, baixe os arquivos `.woff2` e use `@font-face`.
- O botão magnético e a física de mola do React não existem aqui. O resto do
  comportamento (entrada ao rolar, título palavra por palavra, texto gigante,
  contagem, loops, FAQ, selo girando) existe.
- Mudar a estrutura (ordem de seções) é editar o HTML. Fazer isso em várias
  páginas do mesmo aluno é motivo para migrar para o React.
