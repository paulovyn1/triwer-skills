# Layout das seções

Vale para os dois modos. A página é pensada para o celular: coluna única de até
460px, centralizada, com 16px de margem lateral. No desktop ela continua estreita
no centro, sobre o fundo com grid, como um app.

## Ordem na tela

1. **Barra do topo** (fixa): botão de menu à esquerda, logo no centro, botão de
   compartilhar à direita.
2. **Hero**: card alto com a foto do expert, degradê escuro embaixo e, por cima
   dele, rótulo, frase grande com marca-texto e ícones das redes. Embaixo do
   card, um entalhe com uma seta que pula, chamando para rolar.
3. **Destaque**: card grande com um entalhe no topo segurando o selo
   ("Lançamento"). Dentro: traços da marca se desenhando, o livro 3D (ou foto em
   moldura), título com faixa, frase e botão cheio.
4. **Cards médios**: texto à esquerda, foto à direita sumindo num degradê.
   Alterne tom escuro e tom claro para dar ritmo.
5. **Gratuito**: card colorido com entalhe "Gratuito". Dentro: uma tela branca
   (como um app) que vai marcando os itens do material com uma barra de
   progresso, depois título grande, frase, botão claro e nota "100% gratuito".
6. **Rodapé**: uma linha de direitos reservados.

**Menu** (abre pelo botão do topo): painel que desce do alto com fundo
desfocado atrás. Lista todos os links da página com ícone, nome e etiqueta,
depois a frase de fechamento com marca-texto e os ícones das redes.

O entalhe (selo do destaque e do gratuito, seta do hero) é um recorte na cor do
fundo da página. Ele dá a cara de "app" e separa os blocos sem precisar de
linha.

## Animações

| Elemento | Animação | Por quê |
|---|---|---|
| Barra do topo | desce e aparece | primeira coisa, situa a marca |
| Card do hero | cresce de 94% para 100% | entrada com peso, sem demorar |
| Frase do hero | palavra por palavra, subindo de dentro de uma máscara | leva o olho para a visão do expert |
| Ícones das redes | aparecem um a um com mola | depois da frase, para não competir |
| Foto do hero | desce e aproxima ao rolar (parallax) | profundidade |
| Cards | sobem e aparecem quando entram na tela | ritmo na rolagem |
| Traços do destaque | se desenham | identidade da marca em movimento |
| Livro 3D | flutua e inclina seguindo o dedo/cursor | o produto parece objeto |
| Faixa do título | desenrola da esquerda | marca a palavra forte |
| Botões | brilho passando, seguem levemente o cursor, seta gira no hover | chamam o clique |
| Cards médios | inclinam seguindo o cursor, foto aproxima no hover | sensação de toque |
| Tela do gratuito | marca os itens em sequência, em loop, enquanto está visível | mostra o que o material entrega |
| Menu | painel com mola, itens entram um a um | navegação com cara de app |

Tudo respeita "reduzir movimento" do sistema: com ele ligado, a página aparece
pronta, sem animação.

## Regras de celular

- Nada estoura a largura (sem rolagem horizontal).
- O texto do hero fica sobre a parte escura do degradê, nunca sobre o rosto.
- Nos cards médios, o texto ocupa até 72% da largura. Título longo quebra em
  duas linhas, não encolhe.
- Área de toque de botões e ícones com pelo menos 42px.
- No celular não há inclinação por cursor. A inclinação não pode ser a única
  pista de que o card é clicável: a seta e o botão continuam lá.
