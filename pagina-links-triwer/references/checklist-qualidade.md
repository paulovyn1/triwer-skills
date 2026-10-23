# Checklist antes de entregar

Confira com print em 360px, 412px e desktop, com o menu aberto e fechado.

Sobre os prints: o Chrome em modo invisível não abre janela com menos de ~500px.
Um print com `--window-size=412,...` desenha a página em 500px e corta, e parece
que a página estoura a largura. Use `scripts/prints.mjs` (ele emula a tela do
celular) ou coloque a página dentro de um `<iframe width="360">` e fotografe a
moldura. Animações com atraso podem sair pela metade no print: se algo sumiu,
confira de novo antes de mexer no código.

## Conteúdo
- [ ] Um destaque só. A ordem na tela é a que o aluno aprovou.
- [ ] Todo card descreve o que o destino realmente tem (nome, promessa, itens da
      tela do gratuito conferidos no destino).
- [ ] Nenhum número, prazo ou resultado sem fonte.
- [ ] Perfis de rede confirmados pelo aluno (nenhuma arroba tirada de foto ou
      arquivo antigo sem confirmação).
- [ ] Nenhum travessão. Nenhuma frase reescrita depois de aprovada.
- [ ] Nome do expert e dos produtos iguais em todo lugar (aba, topo, menu, cards).

## Links
- [ ] Cada botão leva ao destino certo. Externos abrem em nova aba.
- [ ] Links pendentes estão em "#" (não fazem nada ao clicar) e listados na
      entrega. Nenhuma URL chutada.
- [ ] O menu tem os mesmos links da página, na mesma ordem.
- [ ] WhatsApp no formato `wa.me`, com número que o aluno autorizou.

## Visual
- [ ] **Palavras do hero não grudam.** O bloco de cada palavra precisa de
      `margin-right` (já está nos modelos). Se mudou o CSS, confira.
- [ ] Marca-texto na palavra certa (índice começa em 0).
- [ ] Texto do hero sobre a parte escura, sem cobrir o rosto.
- [ ] Sem rolagem horizontal no celular.
- [ ] Ícones das redes visíveis no topo **e** no menu.
- [ ] Nenhuma cor da paleta de exemplo dos modelos sobrou (azul-marinho, azul,
      amarelo), a não ser que seja a da marca.
- [ ] Imagens em WebP, leves. Nenhuma imagem quebrada.
- [ ] Fontes com licença comercial.

## Publicação e pacote
- [ ] O link entregue é o de produção, responde 200, abre sem login.
- [ ] O zip abre com pastas certas (caminhos com barra normal), sem
      `node_modules`.
- [ ] O LEIA-ME tem o link publicado, os pendentes e onde trocar cada coisa.
