# Checklist antes de entregar

Cada item aqui é um erro que já aconteceu numa página real. Confira com print em
1440px, 412px e 360px.

## Texto
- [ ] **Palavras grudadas em título animado.** Quando o título é quebrado em
      palavras dentro de blocos `inline-block`, o espaço entre elas some. A
      correção é dar `margin-right: 0.24em` ao bloco de cada palavra.
- [ ] **Destaque na palavra certa.** Destaques por índice erram fácil (o índice
      começa em 0 e pontuação conta como parte da palavra). Confira cada título.
- [ ] Copy na página igual à aprovada: nenhuma frase reescrita, nenhum preço a mais.
- [ ] Nenhum travessão.
- [ ] Nome do produto igual em todo lugar (título da aba, oferta, FAQ, lista).

## Componentes
- [ ] **Aba ativa visível.** Se o fundo da aba ativa é um elemento posicionado
      dentro do botão, uma regra genérica para os filhos (`button span {position:
      relative}`) pode anular o `position: absolute` dele e o fundo some.
- [ ] Calculadora: troca de aba reinicia os números; modo "digitar" mostra aviso
      se o valor de cima for menor; o resultado final é exato (sem arredondar no
      meio da animação na hora do print, espere ela terminar).
- [ ] FAQ abre e fecha; só um aberto por vez.
- [ ] Todos os botões de compra levam ao mesmo lugar.

## Layout
- [ ] **Elemento lateral fixo (régua, selo) não encosta no conteúdo** em 1366 e 1440px.
      Se encostar, esconda os rótulos e mantenha só os pontos.
- [ ] **Hero no celular:** o mockup não cobre o rosto do expert nem a legenda.
- [ ] Nada estoura a largura no celular (sem rolagem horizontal).
- [ ] Barra fixa do celular não cobre o botão da oferta no fim da página.

## Imagens e regras
- [ ] Fotos sem crachá, logo ou dado que quebre regra do aluno.
- [ ] Logo e capa nas versões mais recentes que o aluno mandou.
- [ ] Fontes com licença de uso comercial.
- [ ] Prévias desenhadas de páginas internas estão sinalizadas como provisórias.

## Entrega
- [ ] Links, CNPJ e WhatsApp: preenchidos ou listados como pendentes.
- [ ] Pacote montado como o arquivo do modo pede.
