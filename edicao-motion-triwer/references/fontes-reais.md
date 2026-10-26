# Material real: onde buscar, como escolher, como creditar

Ler na etapa de material, junto com o cartão do estilo. Toda busca devolve **texto ou uma folha numerada**: nunca abrir candidato
por candidato. Créditos de tudo que for baixado vão para `edit/fontes/creditos.json`. Os scripts gravam isso sozinhos.

## Ordem de preferência
1. Material da própria pessoa ou marca (fotos, vídeos, prints do próprio negócio).
2. Fonte pública real com crédito: matéria, entrevista, arquivo histórico, comentário público.
3. Banco gratuito com cara orgânica.
4. Imagem gerada (`gerar-imagem`), só para objeto, textura ou metáfora. Nunca como prova, e nunca imitando pessoa real.

## Trecho de fala de pessoa conhecida (YouTube)
- `baixar_trecho.py achar "<url>" "<frase>"` lê a legenda sem baixar nada e devolve o tempo exato.
- `baixar_trecho.py baixar "<url>" --de X --ate Y` baixa só o pedaço.
- Para achar o vídeo: entrevista, podcast, palestra ou programa de TV. Preferir a fonte original (canal do programa ou da
  pessoa), nunca reupload.
- Uso:
  - em conteúdo orgânico, trecho curto (até cerca de 10 s), com crédito na tela ("Nome · Programa/Canal, ano") e com
    comentário ou contexto em volta;
  - nunca cortar de um jeito que mude o sentido da fala.
- **Anúncio pago: não usar** imagem ou voz de pessoa famosa. Sugere endosso, fere direito de imagem e a plataforma reprova.
  No lugar, usar cartão de citação com a frase e a fonte, ou dado público.

## Vídeo e foto de banco com cara orgânica
`buscar_stock.py buscar "<termo em inglês>" --organico [--vertical] [--tipo foto]` gera a folha numerada; depois
`buscar_stock.py baixar <candidatos.json> 3,7`.

| Banco | Bom para | Licença |
|---|---|---|
| Internet Archive (archive) | filme antigo, cinejornal, Prelinger (domínio público), comercial de época | ver cada item; muitos são domínio público |
| Wikimedia Commons (commons) | foto histórica, documento, patente, mapa | por arquivo (CC-BY pede crédito; PD não) |
| Pexels (pexels) | cena atual, pessoas, objetos, texturas | livre, sem crédito obrigatório (chave grátis) |
| Pixabay (pixabay) | cena atual, objeto, textura | livre, sem crédito obrigatório (chave grátis) |
| Mixkit (manual, mixkit.co/free-stock-video) | cenas curtas em boa resolução | livre para uso comercial |

**Termos que trazem cara orgânica** (em inglês): `handheld`, `pov`, `candid`, `vlog`, `phone footage`, `home video`, `35mm`,
`film grain`, `natural light`, `window light`, `top view`, `flat lay`, `close up hands`, `street`, `messy desk`, `night city`.

**Evitar** (cara de banco): `business people`, `team meeting`, `handshake`, `smiling woman laptop`, `success`, `corporate`.

**Tratamento obrigatório** (tira a cara de banco):
- enquadramento fechado;
- cor do estilo (dessaturar ou esquentar);
- grão;
- 2 a 3 s no máximo;
- velocidade levemente alterada (0,9 a 1,1x);
- inserção em faixa de cinema ou recorte com sombra, em vez de tela cheia crua.

## Prints de matéria e notícia
`capturar_print.py "<url>" saida.png --escala 2` (Chrome headless, sem login).

**Portais brasileiros primeiro:**
- notícias gerais: G1, Folha, Estadão, UOL, CNN Brasil;
- negócios e economia: Exame, Valor, InfoMoney, Forbes Brasil, Época Negócios, PEGN;
- marketing: Meio & Mensagem, B9, Mundo do Marketing;
- tecnologia: Tecmundo, Olhar Digital, Canaltech, Mobile Time;
- pequenos negócios e pesquisas oficiais: Sebrae, IBGE, Agência Brasil.

**Estrangeiro só quando não houver em português:** mostrar a tradução na tela com "tradução livre" + veículo e data
originais. Recriar o recorte com o texto traduzido é melhor que mostrar o print em inglês.

**Regras:**
- Veículo e data legíveis por pelo menos 1 s.
- Recorte fiel. Não inventar manchete nem editar texto de matéria real.
- Se o site bloquear o print: `https://r.jina.ai/<url>` traz o texto puro, para recriar o recorte com o texto exato e a fonte.
- Post de rede social vira **cartão de citação** (texto, autor, rede e data), nunca imitação de print da rede.

## Comentários reais (voz do público)
- `buscar_comentarios.py youtube "<url>" --filtro "cansad|sozinh|burnout"` traz os comentários de um vídeo brasileiro do tema,
  ordenados por curtidas.
- `buscar_comentarios.py hn "<termo>"` busca no Hacker News, em inglês.
- Reddit e X costumam bloquear robô. Usar só se o usuário mandar o link ou o print.
- **Privacidade:** pessoa comum aparece só com iniciais (o script já anonimiza), sem foto e sem @. Pessoa pública com nome
  é permitida.

## Material de arquivo histórico
Internet Archive (Prelinger Archives, cinejornais), Wikimedia Commons, Library of Congress (loc.gov, muita coisa em domínio
público), Arquivo Nacional e Brasiliana Fotográfica (fotos históricas do Brasil, ver a licença de cada uma). Patentes antigas:
Google Patents, cujo desenho é público.

## Checagem antes de usar
- Licença conferida e registrada em `creditos.json`.
- Crédito na tela quando a licença pede ou quando é fala de terceiro.
- Nada de pessoa famosa em anúncio pago.
- Pessoa comum anonimizada.
- Matéria e print fiéis, com veículo e data.
