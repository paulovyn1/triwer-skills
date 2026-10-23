# Modo React

Leia só este arquivo nas fases 4 e 5 quando o formato escolhido for React.
Exige terminal (Claude Code) e Node 18 ou mais novo.

## Montagem
1. Crie a pasta do projeto onde o aluno indicar:
   ```
   npm init -y
   npm i react@18.3.1 react-dom@18.3.1 motion@11.18.2
   npm i -D vite@6.3.5 @vitejs/plugin-react@4.5.2
   ```
   Fontes: pacotes `@fontsource-variable/<fonte>` importados no `main.jsx`, para
   não depender de requisição externa.
2. Copie os componentes de `assets/react-kit/` para `src/components/`:
   - `ui.jsx`: `Reveal` (entra ao rolar), `Words` (título palavra por palavra,
     `highlight` por índice), `CountUp`, `CTA` (botão magnético, lê
     `CHECKOUT_URL` de `../config.js`), `Label`, `Tape` (marca-texto que
     desenrola), `brl`.
   - `BookMockup.jsx`: livro 3D a partir da capa (`src`), inclina com o cursor.
   - `Calculadora.jsx`: abas, modo digitar, contagem. Recebe `cenarios`,
     `textos` e `multiplicador` por props.
3. **CSS**: as classes desses componentes são as mesmas do template HTML
   (`assets/template-pagina.html`). Copie de lá só os blocos `Tokens`,
   `Tipografia`, `Botões`, `Livro 3D`, `Calculadora` e o que for usar, para o
   `src/styles.css`. Atenção a três diferenças:
   - em React, a palavra animada não depende da classe `.in`: troque o bloco
     `.word { transform... }` por `.word { display: inline-block; }`;
   - o livro do kit já anima a flutuação e a inclinação pelo `motion`: no CSS
     copiado, apague o `animation: flutua` de `.livro-flutua` e o `transform` de
     `.livro`, senão os dois movimentos brigam;
   - na calculadora, o kit já cuida da entrada das células: apague o
     `opacity: 0` de `.calc-celula` e de `.calc-depois`;
   - mantenha `margin-right` em `.word-mask`, senão as palavras grudam.
4. Envolva o app em `<MotionConfig reducedMotion="user">`.
5. Crie `src/config.js` com `CHECKOUT_URL`, `WHATSAPP_URL`, `PRECO_DE`,
   `PRECO_POR`, `CNPJ` e as listas (empresas, páginas internas, cenários da
   calculadora). Quem implementa troca tudo num lugar só.
6. Monte as seções em componentes (`Hero.jsx`, `Sections.jsx`), na ordem de
   `estrutura-copy.md`, seguindo `layout-secoes.md`.
7. Imagens em `public/img/`, otimizadas com
   `node scripts/otimizar-imagens.mjs <origem> public/img`.

## Revisão
`npx vite build` e `npx vite preview --port 4173` (em segundo plano), depois
`node scripts/prints.mjs http://localhost:4173 <saída>`. Olhe cada print com o
checklist. Recompile depois de cada ajuste.

## Entrega
- Zip do projeto **sem** `node_modules` e `.vercel`, **com** `dist/` compilado.
- `LEIA-ME.md` na raiz: como rodar (`npm install`, `npm run dev`), como compilar,
  como subir só a `dist/` numa hospedagem estática, como compilar para subpasta
  (`npx vite build --base=/caminho/`), onde trocar links, preço e imagens, e
  quais fontes foram usadas e por quê.
- Diga ao aluno o caminho exato do zip e o que mandar para quem vai implementar.
