# Modo HTML único

Leia só este arquivo nas fases 5 e 6 quando o formato escolhido for HTML.

## Montagem

1. Copie `assets/template-links.html` para a pasta do aluno como `index.html`.
   Nunca edite o modelo original da skill.
2. **Tokens**: troque as variáveis em `:root`, incluindo as versões `-rgb`.
   Troque o `<link>` do Google Fonts e `--display` e `--body`. Troque também o
   `theme-color` no `<head>`.
3. **Textos**: substitua cada `[COLCHETE]` pelos textos aprovados. Cada bloco
   está marcado com um comentário `BLOCO`. Bloco sem material: apague o trecho
   inteiro e o item correspondente no menu.
4. **Marca-texto do hero**: `data-faixa="1,2"` marca as palavras de índice 1 e 2
   (começa em 0, pontuação colada conta como parte da palavra). Recalcule
   sempre que a frase mudar.
5. **Faixa do destaque**: a palavra final do título vai dentro do
   `<span class="tape">`. Sem palavra forte, apague o span.
6. **Mídia do destaque**: livro 3D (troque `img/capa.webp`) ou foto em moldura
   (descomente o `<img class="feature-foto">` e apague o bloco do livro).
7. **Mais cards**: duplique um bloco `link-card`, troque o `data-link` (por
   exemplo `card3`) e crie a mesma chave em `CONFIG.links`. Faça o mesmo no menu.
8. **Redes**: apague os `<a class="social">` das redes que o expert não usa.
   Para uma rede nova, copie um ícone de `assets/react-kit/src/components/icons.jsx`.
   O menu copia os ícones do topo sozinho.
9. **Tela do gratuito**: um `<li>` por item, até 5. O contador se ajusta sozinho.
10. **Links**: todos no `CONFIG`, no fim do arquivo.

## Imagens

Pasta `img/` ao lado do HTML: `hero.webp`, `capa.webp`, `card-1.webp`,
`card-2.webp`, `logo.svg`, `favicon.png`. Imagem que ainda não existe fica
invisível em vez de mostrar ícone quebrado.

- Com terminal: `node scripts/otimizar-imagens.mjs <origem> <pasta img>`.
- No claude.ai: peça ao aluno as imagens já leves (JPG ou WebP) e diga o nome
  exato de cada arquivo.

## Revisão

- Com terminal: sirva a pasta (`npx serve <pasta>`) e rode
  `node scripts/prints.mjs <url> <saída>` (precisa de `npm i puppeteer-core`
  numa pasta de ferramentas e de Chrome ou Edge instalado). Olhe os prints com o
  checklist. Abra o menu também (os prints não abrem sozinhos).
- Sem terminal: peça ao aluno para abrir no celular e mandar print do topo, do
  destaque, do gratuito e do menu aberto.

## Publicação e entrega

Veja `publicacao.md`. O pacote é o `index.html` + a pasta `img/` + o LEIA-ME.
