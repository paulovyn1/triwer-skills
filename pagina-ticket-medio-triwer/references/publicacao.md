# Publicação e entrega

Só publique quando o aluno pedir ("publica", "sobe na Vercel"). Publicar torna a
página pública, então a ordem é: página revisada, aluno aprovou, aluno pediu.

## Vercel
Exige terminal e a Vercel CLI logada (`vercel whoami`). Se não estiver, peça ao
aluno para rodar `vercel login`. Não tente o login por ele.

**Não instale nada na máquina para publicar.** A Vercel recebe o código, roda o
`npm install` e o build na nuvem. Instalar localmente só gasta minutos, às
vezes trava, e não muda o resultado.

1. Confirme que o `.vercelignore` tem `node_modules`, `dist` e
   `package-lock.json` (o kit já vem assim). O lock sai porque, se uma
   instalação local foi interrompida, ele fica incompleto e quebra o build na
   nuvem.
2. Na pasta do projeto: `vercel --prod --yes --name <nome-do-projeto>`. Use um
   nome novo para cada página (por exemplo `<produto>-<expert>`), para um deploy
   não sobrescrever outra página do mesmo cliente.
3. A CLI pode terminar só com JSON. Confira o status com
   `vercel inspect <url-do-deploy>`: deve estar `Ready` e listar os aliases.
4. **Use o endereço de produção, não o do deploy.** O endereço com hash
   (`<nome>-a1b2c3-<time>.vercel.app`) costuma pedir login. O que vai para o
   aluno é o alias `https://<nome>.vercel.app`. Confira que responde 200 e que o
   título é o certo:
   `curl -s -o /dev/null -w '%{http_code}' https://<nome>.vercel.app`
5. Para atualizar, rode o mesmo comando na mesma pasta (a pasta `.vercel` guarda o
   projeto). O endereço continua o mesmo.

**Modo HTML na Vercel:** funciona igual, sem build. A pasta com `index.html` e
`img/` é publicada como está (`vercel --prod --yes --name <nome>` dentro dela). O
`.vercelignore` do kit React não se aplica.

## Outra hospedagem
- **HTML:** suba `index.html` e `img/`.
- **React:** suba o conteúdo de `dist/`. Para subpasta: `npx vite build --base=/caminho/`.

## Pacote para quem vai implementar (o dev do aluno, ou o sócio)
No modo HTML o pacote é `index.html` + `img/` + `LEIA-ME.md`: pule o passo 1 e
gere o zip com o passo 3.

1. **`dist/` (React)**: use o do build local. Sem build local, baixe a versão que está no
   ar (idêntica ao build):
   ```
   B=https://<nome>.vercel.app
   mkdir -p dist/assets
   curl -sf $B/ -o dist/index.html
   for a in $(grep -oE '/assets/[^"]+' dist/index.html | sort -u); do curl -sf $B$a -o dist$a; done
   for a in $(cat dist/assets/*.css dist/assets/*.js | grep -oE '/assets/[A-Za-z0-9._-]+\.(woff2?|webp|png|svg)' | sort -u); do curl -sf $B$a -o dist$a; done
   cp -r public/img dist/img
   ```
2. **LEIA-ME**: copie `assets/LEIA-ME-modelo.md` para a raiz do projeto como
   `LEIA-ME.md` e preencha. Não pode faltar: o link publicado, os pendentes, onde
   trocar cada coisa e o aviso de que mudar texto ou link só no `dist/` não
   funciona (precisa compilar de novo ou rodar `vercel --prod`).
3. **Zip**: `python scripts/empacotar.py <pasta-do-projeto> <saida.zip>`. Ele
   deixa de fora `node_modules`, `.vercel`, `.git` e `package-lock.json`, e grava
   os caminhos com barra normal. Não use o `Compress-Archive` nem o
   `ZipFile.CreateFromDirectory` do Windows PowerShell 5.1: gravam barra
   invertida, e no Mac o arquivo vira um nome só, sem pastas.
4. Salve o zip na pasta de outputs do cliente e diga ao aluno o **caminho
   exato**, o link publicado e o que ainda precisa ser preenchido.

## O que não esquecer de dizer na entrega
- Checkout, WhatsApp, CNPJ e link da VSL ainda vazios, se for o caso.
- Números de mercado que vieram só da ficha do produto, sem fonte.
- A conta do parcelamento, se o checkout ainda não foi configurado.
- O servidor de preview local fica ligado: avise ou encerre.
