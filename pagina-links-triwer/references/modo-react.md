# Modo React

Leia só este arquivo nas fases 5 e 6 quando o formato escolhido for React.
Exige terminal (Claude Code).

## Montagem

1. Copie a pasta `assets/react-kit/` inteira para onde o aluno indicar.
   Nunca edite o kit original da skill. O kit já traz `package.json` (React 18,
   Motion 11, Vite 6, fontes Outfit e Manrope pelo `@fontsource`),
   `vite.config.js`, `.gitignore` e `.vercelignore`.
2. **Conteúdo**: preencha `src/config.js` com os textos e links aprovados. É o
   único arquivo que muda na maioria dos casos. Ele tem `PERFIL` (topo),
   `DESTAQUE`, `CARDS` (lista, na ordem), `GRATUITO` (ou `null`), `REDES`,
   `FRASE_MENU` e `RODAPE`. Negrito nos textos: `**assim**`.
3. **Ícones**: os nomes válidos estão em `porNome`, no fim de
   `src/components/icons.jsx` (instagram, linkedin, youtube, tiktok, substack,
   whatsapp, site, email, link...). Rede nova: desenhe o SVG no mesmo padrão e
   registre em `porNome`.
4. **Tokens**: troque o bloco `:root` de `src/styles.css`, incluindo as versões
   `-rgb`. Fontes: troque os pacotes `@fontsource-variable/...` no
   `package.json` e os imports em `src/main.jsx`, e as variáveis `--display` e
   `--body`.
5. **Traços do destaque**: a lista `tracos` em `src/App.jsx`. Troque por um
   elemento da marca ou esvazie a lista.
6. **`index.html`**: título da aba, descrição, `theme-color`, imagem de
   compartilhamento.
7. **Imagens** em `public/img/`, com os caminhos usados no `config.js`.
   Otimize com `node scripts/otimizar-imagens.mjs <origem> public/img`.

Se o aluno já tem a página de vendas em React, copie de lá os tokens e as
fontes, e confira se o `BookMockup` dela é o mesmo (o do kit recebe `src` e
`alt` por props).

## Revisão

Para ver a página, é preciso instalar as dependências uma vez (`npm install`).
Em pasta de rede, nuvem sincronizada ou disco lento, isso pode levar muitos
minutos. Se travar, não insista: publique na Vercel (que compila na nuvem) e
revise pelo link publicado.

Com as dependências instaladas: `npx vite build` e `npx vite preview --port 4173`
(em segundo plano), depois `node scripts/prints.mjs http://localhost:4173 <saída>`.
Olhe os prints com o checklist. Abra o menu também.

## Publicação e entrega

Veja `publicacao.md`. O pacote é o projeto sem `node_modules`, com `dist/` e o
LEIA-ME.
