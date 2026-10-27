# Modo React

Leia só este arquivo nas fases 4 e 5 quando o formato escolhido for React.
Exige terminal (Claude Code) e Node 18+ para quem for rodar depois. A publicação
não precisa de `npm install` na máquina, ver `publicacao.md`.

## 1. Criar o projeto a partir do kit
1. Pasta de destino: onde o aluno indicar. Copie `assets/react-kit/` inteiro para lá, **inclusive os arquivos
   que começam com ponto** (`.gitignore`, `.vercelignore`). Em PowerShell use
   `robocopy`, que copia ocultos.
2. O kit é uma página que funciona, escrita para outro expert. Trocar texto de
   uma página pronta é mais rápido que escrever do zero, mas exige disciplina:
   - troque **todo** texto de `Sections.jsx` e `Hero.jsx` pela copy aprovada. Os
     títulos usam `T(texto, "frase a destacar")`: o destaque é achado pela frase,
     não por índice, então mudar o título não desloca a cor;
   - preencha `src/config.js` (preço, parcelas, garantia, empresas, custo, links);
   - troque os tokens do `:root` em `styles.css` (ver `identidade-visual.md`);
   - ponha imagens em `public/img/` (logo.svg, fotos, favicon.png, og.jpg). O kit
     traz provisórias (`expert-1.svg`..`expert-4.svg`, `expert-bio.svg`, `logo.svg`):
     troque os arquivos e os caminhos em `Sections.jsx`;
   - atualize `index.html` (título, descrição **sem preço**, og).
3. **Rode `python scripts/conferir-restos.py <pasta-do-projeto>`**. Todo texto
   do kit é exemplo anonimizado em [colchetes], então o script lista o que ainda
   não foi trocado, além de travessões, números zerados no `config.js` e preço
   fora da ancoragem. Ele só pega o que está entre colchetes: leia o
   `Sections.jsx` final inteiro uma vez antes de seguir, para achar frase
   genérica que ficou sem colchete.
4. Remova do projeto o que a estrutura do aluno não usa (seção sem conteúdo some,
   não fica com texto de exemplo) e confira `App.jsx`.

## 2. Compilar e olhar sem `npm install`
O `npm install` local já travou e irritou a aluna. Prefira:
- Se existe um projeto irmão com `node_modules` (outra página da mesma stack),
  copie a pasta: `robocopy <irmao>\node_modules <novo>\node_modules /E /MT:32`.
  Um junction (`mklink /J`) falha em alguns discos.
- Depois: `node_modules/.bin/vite build` (no Windows, `vite.cmd`). Se o build
  quebrar com erro de JSON no `package.json`, o arquivo ganhou BOM: o
  `Set-Content -Encoding utf8` do PowerShell 5.1 grava com BOM. Regrave com
  `[IO.File]::WriteAllText(caminho, texto, (New-Object Text.UTF8Encoding($false)))`.
- Sem projeto irmão e sem vontade de esperar o install: publique direto na
  Vercel (que compila na nuvem) e revise a página no ar.
- Para ver: `vite preview --port 4173` em segundo plano e abra no navegador
  (Claude in Chrome). Ou `node scripts/prints.mjs http://localhost:4173 <saida>`
  (exige `npm i puppeteer-core` e Chrome ou Edge).

## 3. Revisar com o checklist
`references/checklist-qualidade.md`, em 1440px, 412px e 360px. Recompile depois
de cada ajuste. Antes de mostrar ao aluno, confirme que não há preço fora da
ancoragem (o checklist tem a busca).

## 4. Ajustes depois da primeira entrega
Leia o estado atual do arquivo antes de editar (o aluno ou outra pessoa pode ter
mudado). Mude só o que foi pedido, recompile, confira, entregue de novo. Um
pedido que parece de uma palavra pode estar em vários lugares (a garantia
apareceu em cinco): procure no projeto inteiro.
