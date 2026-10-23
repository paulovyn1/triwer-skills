# Publicação e entrega

## Vercel (link para aprovar ou divulgar)

Só com terminal e com a Vercel CLI logada (`vercel whoami`). Se não estiver,
peça ao aluno para rodar `vercel login`. Não tente fazer o login por ele.

**Não instale nada na máquina para publicar.** A Vercel recebe o código, roda o
`npm install` e o build na nuvem e publica. Instalar localmente só para isso
gasta minutos (às vezes trava) e não muda o resultado.

1. Confirme que o `.vercelignore` tem `node_modules`, `dist` e
   `package-lock.json`. O `package-lock.json` sai porque, se uma instalação
   local foi interrompida, ele fica incompleto e quebra o build na nuvem.
2. Na pasta do projeto: `vercel --prod --yes --name <nome-do-projeto>`.
   Use um nome novo para a página de links (por exemplo `links-<nome>`), separado
   da página de vendas, para um deploy não sobrescrever o outro.
3. A saída da CLI pode vir só como JSON. Confira com `vercel ls <nome>` se o
   status está `Ready`.
4. **Pegue o endereço certo.** O endereço com hash
   (`<nome>-a1b2c3-<time>.vercel.app`) costuma pedir login (responde 302). O
   que vai para o aluno é o de produção, `https://<nome>.vercel.app`. Confira
   que ele responde 200 e mostra o título certo:
   `curl -s -o /dev/null -w '%{http_code}' https://<nome>.vercel.app`
5. Para atualizar depois, rode o mesmo comando na mesma pasta (a pasta `.vercel`
   guarda o projeto). O endereço continua o mesmo.

Modo HTML na Vercel: funciona igual, sem build. A pasta com `index.html` e
`img/` é publicada como está.

## Outra hospedagem

- HTML: subir `index.html` e `img/`.
- React: subir o conteúdo de `dist/`. Para subpasta, compilar com
  `npx vite build --base=/caminho/`.

## Pacote para quem vai implementar

1. **`dist/` sem instalar nada (React publicado na Vercel)**: baixe a versão que
   está no ar. Ela é idêntica ao build.
   ```
   B=https://<nome>.vercel.app
   mkdir -p dist/assets
   curl -sf $B/ -o dist/index.html
   for a in $(grep -oE '/assets/[^"]+' dist/index.html | sort -u); do curl -sf $B$a -o dist$a; done
   for a in $(cat dist/assets/*.css dist/assets/*.js | grep -oE '/assets/[A-Za-z0-9._-]+\.(woff2?|webp|png|svg)' | sort -u); do curl -sf $B$a -o dist$a; done
   cp -r public/img dist/img
   ```
   Se o projeto foi compilado localmente, use o `dist/` do build.
2. **LEIA-ME**: copie `assets/LEIA-ME-modelo.md` para a raiz do projeto como
   `LEIA-ME.md` e preencha. O que não pode faltar: o link publicado, os links
   pendentes, onde trocar cada coisa e o aviso de que trocar texto ou link só no
   `dist/` não funciona no React (precisa compilar de novo, ou rodar
   `vercel --prod`).
3. **Zip**: `python scripts/empacotar.py <pasta-do-projeto> <saida.zip>`. Ele
   deixa de fora `node_modules`, `.vercel`, `.git` e `package-lock.json`, e grava
   os caminhos com barra normal. Não use o Compress-Archive do Windows: ele grava
   barra invertida e o zip abre errado no Mac.
4. Diga ao aluno o caminho exato do zip e o que mandar para quem vai
   implementar.
