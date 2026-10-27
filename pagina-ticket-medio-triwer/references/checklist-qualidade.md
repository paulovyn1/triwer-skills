# Checklist antes de entregar

Cada item é um erro que já aconteceu ou uma correção que o aluno pediu. Confira
com print ou navegador em 1440px, 412px e 360px.

## Estrutura
- [ ] A ordem e os componentes seguem a referência que o aluno indicou (tabela de
      `referencia-estrutura.md`), não as páginas antigas dele.
- [ ] Fundo claro com painéis escuros alternados. Página inteira escura é erro.

## Preço e oferta
- [ ] **Nenhum preço fora da ancoragem.** Busque `R$`, `297` (o valor real do
      produto), `12x` e `preço` em `src/` e `index.html`. Só podem aparecer em
      `Oferta` (lista e cartão), na conta do custo (que vem depois do preço) e
      em valores de mercado.
- [ ] Sem faixa de aviso no topo e sem barra fixa de preço no celular.
- [ ] Botão sem preço, com o resultado ("Quero [resultado desejado]"), igual em todos.
- [ ] Parcela grande, "ou à vista" pequeno. A soma das parcelas foi conferida
      com o aluno e bate com o checkout.
- [ ] Garantia: o número de dias é o que o aluno confirmou, igual no selo, no
      texto, nos selos do preço, no FAQ e no fechamento. Busque `dias` e o número
      antigo.
- [ ] Bônus sem preço nos cartões, sem terceira pessoa ("com o [nome]").

## Texto
- [ ] Headline e subheadline idênticas ao que o aluno ditou.
- [ ] O nome do método só aparece depois da seção "O que é".
- [ ] **Palavras grudadas em título animado**: copie um título e cole num
      bloco de notas. Tem de sair com espaços.
- [ ] Destaque na palavra certa em cada título (índice começa em 0).
- [ ] Tratamento consistente (tu/você) e sem empilhar "Tu" nas primeiras dobras
      (`estilo-copy.md`). Comandos no imperativo.
- [ ] Nenhum travessão (— ou –). `scripts/conferir-restos.py` busca.
- [ ] Nenhuma sobra do exemplo do kit (`conferir-restos.py`).
- [ ] Nome do produto igual em título da aba, hero, oferta e FAQ.
- [ ] Números de mercado com fonte, ou marcados "a confirmar" na entrega.

## Componentes
- [ ] Player da VSL parece player, e sem link não leva a lugar nenhum.
- [ ] Faixa de autoridade logo depois do hero, com empresas permitidas pelo aluno.
- [ ] Texto gigante acende palavra por palavra ao rolar.
- [ ] FAQ abre e fecha, um por vez.
- [ ] Todos os botões levam ao mesmo lugar (checkout ou `#oferta`).
- [ ] Seção de depoimentos some se a lista está vazia.
- [ ] Menu fixo legível sobre painel escuro.

## Layout
- [ ] Sem rolagem horizontal em 360px.
- [ ] Quadros das etapas e dos bônus empilham bem no celular.
- [ ] Gradiente de um tom só, sem passar de uma cor para outra.

## Imagens e regras
- [ ] Fotos sem crachá, logo ou dado que quebre regra do aluno (empresa atual).
- [ ] Fontes com licença comercial.
- [ ] Logo e fotos nas versões mais recentes.

## Específico do modo HTML
- [ ] `index.html` abre com a pasta `img/` ao lado e nenhuma imagem quebra.
- [ ] Console do navegador sem erro. O bloco `CONFIG` está com vírgulas e aspas
      certas: um erro ali apaga as listas e os preços da página.
- [ ] `data-hl` bate com o título (a frase destacada aparece na cor de destaque).
- [ ] Seção de depoimentos escondida se `DEPOIMENTOS` estiver vazio.

## Entrega
- [ ] Publicado e com resposta 200 no endereço de produção.
- [ ] Zip gerado com `scripts/empacotar.py`, com LEIA-ME e `dist/`.
- [ ] Lista do que falta: checkout, WhatsApp, CNPJ, link da VSL, depoimentos,
      fontes dos números de mercado.
