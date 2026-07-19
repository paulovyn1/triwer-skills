# Hero de página de vendas — arquivo do Gerador

Este arquivo é lido **só pelo subagente Gerador**, nunca pelo Verificador —
o Verificador precisa simular alguém que nunca viu o dossiê e julga só o
efeito do hero pronto (ver `hero-verificador.md`).

**Leia este arquivo na Etapa 12**, depois de já ter `nova_oportunidade` e
`subpromessa` (Etapa 6), `papel_esteira` (Etapa 3), `urgencia_compra`
(Etapa 5), `diferencial_produto` completo (Etapa 4, texto integral — não o
nome do produto nem um resumo de uma frase) e `ativos_marketing_sexys`
(Etapa 9) — hero de página de vendas nunca é escrito solto, é a mesma
promessa já fechada, só que testada num formato diferente (headline +
subheadline de conversão, não headline de post).

## Erro real já cometido — nunca infira o inimigo a partir do nome do produto

**`diferencial_produto` (Etapa 4) é obrigatório no pacote, não opcional —
sem ele, o Gerador tende a inventar um inimigo que soa plausível pelo nome
do produto, mas erra o mecanismo real.** Caso real (Priscilla Vassão,
2026-07-19): o pacote de entrada trazia só "Método Subtrativo e Aditivo de
modelagem em cera... sem depender de modelista terceirizado" — o Gerador
leu isso e escreveu contra o inimigo "terceirização da produção". Errado:
o produto ensina modelagem em cera como **técnica de criação** (fluidez e
complexidade que outros métodos de modelagem não permitem); a fundição
final continua sendo terceirizada normalmente, é prática padrão do
mercado, nunca foi a fricção que o produto resolve. O inimigo real era a
limitação técnica de outros métodos de criação, não a terceirização de
etapa nenhuma. As duas headlines geradas contra o inimigo errado
pareceram fortes e específicas, e mesmo assim promoviam uma promessa
desalinhada do que o produto de fato ensina — nenhum dos 8 testes do
Verificador pega esse erro, porque ele testa forma e lastro em fato, não
se o fato usado descreve o mecanismo certo (o Verificador não tem acesso
ao dossiê completo do produto, só à lista de fatos-fonte que o Gerador
decidiu repassar).

**Regra derivada:** antes de escrever qualquer headline com estrutura de
contraste ("pare de X, faça Y" / "X não é mais necessário"), confirme
contra `diferencial_produto` que X é de fato o que o produto substitui ou
resolve — nunca o que soa como oposto do nome/categoria do produto. Se
`diferencial_produto` não deixar claro qual é o inimigo real, pergunte-se
"o que especificamente esse mecanismo entrega que os alternativos não
entregam" antes de nomear qualquer contraste — headline sem essa checagem
pode passar em todos os 8 testes do Verificador e ainda vender uma
promessa que o produto não cumpre.

## O que é o hero, e o que ele não é

Hero é **só três elementos**: headline, subheadline, botão. Não é a
narrativa completa da página de vendas (dor, mecanismo, prova social,
preço) — isso é outro material, fora do escopo desta etapa. Não confundir
com as headlines exploratórias da Etapa 10 (aquelas testam a promessa em
formato de gancho de post/carrossel; esta etapa testa a mesma promessa em
formato de headline de conversão de página, onde o leitor já chegou
querendo saber do produto, não precisa ser fisgado pra parar de rolar).

## Passo 0 — Classificar o registro da promessa (decide a fórmula inteira)

Antes de escrever qualquer headline, rode os dois testes abaixo — a
fórmula certa depende inteiramente do resultado, aplicar a fórmula errada
produz um hero que soa certo mas erra o mecanismo de decisão do leitor.

### Teste A — Dor urgente ou decisão considerada?

Não é ticket que decide — é o tipo de decisão de compra que o produto
pede. Produto de dor urgente (a pessoa precisa resolver agora, decide no
impulso) pede promessa **utilitária** — quantidade pode ser a própria
promessa central. Produto de decisão considerada (a pessoa vai pensar,
comparar, se imaginar) pede promessa **aspiracional** — quantidade vira
prova, nunca a frase principal.

- Sinal de dor urgente: o produto resolve um "não sei o que fazer agora"
  imediato (ex.: SDS — "50 roteiros prontos pra nunca mais ficar sem
  saber o que postar", quantidade **é** a promessa).
- Sinal de decisão considerada: o produto entrega uma transformação que a
  pessoa vai visualizar/comparar antes de decidir (a maioria dos produtos
  Sexy — mentorias, cursos, posicionamento).

**A maioria dos produtos trabalhados nesta skill é decisão considerada** —
mas não assuma, confira contra `urgencia_compra` (Etapa 5) e o que
`nova_oportunidade` promete. Se houver dúvida real entre os dois, prefira
decisão considerada (é o padrão mais seguro pro tipo de produto que passa
pela investigação completa da Sexy) e sinalize a dúvida no formato de
saída.

### Teste B — Se decisão considerada: quem decide, não só quem paga

Só roda este teste se o Teste A classificou como decisão considerada — em
dor urgente, quem sente a dor decide sozinho e no impulso, não há segunda
camada. Pergunta: **quem de fato decide a compra pode não ser quem
assina o cartão** (ex.: pacote de plantas de arquitetura — quem paga é
frequentemente o marido, quem decide de fato é a esposa que vai viver a
casa). Se o dossiê já tem essa distinção (`publico_promessa` inclui
`quem_decide`, coletado na Etapa 5), o hero mira em quem decide, não em
quem assina.

### Teste C — Registro Paquera ou Estrela?

Cheque `papel_esteira` (Etapa 3). Promessa tática, simples, objetiva é
registro **Paquera** — headline curta, resultado direto, sem rodeio
aspiracional. Promessa de identidade/transformação é registro **Estrela**
— headline aspiracional, e **pede subheadline técnica** (a subpromessa
concreta que sustenta o sonho).

Exemplo real de calibração (curso de costura): Paquera = "aprenda a
costurar do zero com 5 pontos simples em uma semana" (curto, objetivo).
Estrela = "vista uma peça que você mesma fez e escute 'onde você
comprou?'" (aspiracional, identidade) + subheadline técnica ("nunca mais
vista uma roupa desajustada, aprenda numa comunidade a desenvolver as
peças que você sempre sonhou").

## Passo 1 — Honestidade vs. credibilidade (dois testes diferentes, os dois obrigatórios)

**Honestidade:** se o aluno executar o que está no produto, ele é capaz
de chegar a esse resultado? Existe case/depoimento real que prova? Se
sim, a promessa é honesta — mesmo em ticket baixo, mesmo soando ousada.
Ticket e formato não entram nesse teste, só execução → resultado.

**Credibilidade (teste separado, roda depois):** mesmo uma promessa
honesta pode soar grande demais pro contexto/ticket e ser duvidada de
cara. Quando isso acontecer, **o resultado forte não sai da narrativa —
desce um nível**: da headline central para a subheadline, ou para a
prova/case (fora do escopo desta etapa, mas sinalize no formato de saída
se identificar isso). A headline central sempre otimiza pro crível
primeiro; o resultado mais forte reforça depois, não abre.

Exemplo real: produto de R$97 que de fato aumenta ~40% a conversão de
lançamento (alunos que faturaram R$70 mil) — se essa fosse a headline,
seria duvidada. A headline honesta e crível virou "Saiba exatamente o que
postar durante o seu lançamento"; o resultado financeiro forte foi para a
subheadline.

## Passo 2 — Número na headline: status ou esforço?

Se o Teste A/C classificou como aspiracional (Estrela), número ainda pode
voltar pra headline central — mas só um tipo específico.

- **Número que reforça (status/resultado) — pode ir na headline central:**
  "atendi mais de 4.000 alunos", "faturei X com essa mesma sequência" —
  prova que a pessoa vai *ser algo*.
- **Número que enfraquece (esforço/processo) — nunca vai na headline
  central, é peso morto de bastidor:** "curadoria de 60 fornecedores
  testados", "100+ aulas" — prova que o criador *trabalhou muito*, não
  que o comprador vai chegar a algum lugar. Regra-mãe: nunca vender os
  pregos e o martelo, vender o quadro pronto na parede.
- **Combinação mais forte de todas (quando existir no dossiê):** número
  de status + prova de resultado juntos — ex.: "os mesmos 50 roteiros que
  me fizeram sair de R$3 mil pra R$50 mil por mês, sem anúncio". Combina
  utilidade objetiva com prova de que funciona de verdade — mais sexy que
  qualquer um dos dois sozinho. Priorize esse tipo de número se
  `ativos_marketing_sexys` tiver algum candidato assim.

## Passo 3 — A fórmula de headline (dor urgente/utilitária ou aspiracional/Estrela)

**Fórmula base (qualquer registro):** `[verbo de transformação] +
[resultado específico] + [tempo/mecanismo curto]`.

Verbos que abrem headline forte: Transforme / Descubra / Aprenda / Domine
/ Garanta / Pare de / Em vez de. Evitar verbos fracos: Conheça, Entenda,
Explore — soam a curso, não a mudança de estado.

**Padrão de contraste comprimido em uma frase** — antes/depois em dois
substantivos ou verbos opostos, sempre que houver material real pra
sustentar os dois lados (nunca invente o lado negativo, precisa ser algo
real que `publico_promessa`/`diferencial_produto` já sustentam):
"rezando" × "lucrando" / "like" × "Pix" / "lead frio" × "lead
qualificado" / "depende do aluno" × "executa pelo aluno".

**Subheadline em registro Estrela** (obrigatória quando o Teste C
classificou aspiracional): reforça com o dado técnico/concreto que
sustenta o sonho da headline — é onde entra o resultado forte que desceu
no Passo 1, o número de status do Passo 2, ou o "sem X, sem Y, sem Z" que
constrói alívio antes do botão.

**Linha de suporte opcional, abaixo do botão** (só se o dossiê sustentar):
um fato curto de prova social/tempo de mercado — "funciona há 2 anos, sem
tráfego" — nunca inventado, sempre puxado de `ativos_marketing_sexys`.

## Formato de saída

```
Registro identificado: [Utilitário/dor urgente | Aspiracional/Estrela | Paquera]
(se houve dúvida real no Teste A ou B, sinalize aqui em vez de decidir sozinho)

Headline: [texto]
Subheadline: [texto — obrigatória se Estrela, opcional se Paquera/utilitário]
Linha de suporte (opcional): [texto, só se houver fato real de ativos que sustente]

Por que funciona: [1-2 frases citando qual regra de doutrina foi aplicada —
honestidade/credibilidade, status/esforço, contraste comprimido, etc.]
```

Gere **2 propostas de hero**, não 1 — a mesma promessa testada em dois
ângulos diferentes (ex.: um mirando a dor mais aguda do público, outro
mirando o resultado mais forte disponível), nunca duas variações
superficiais da mesma frase.

## Regras que nunca mudam

- **Nunca é a narrativa completa da página** — só headline + subheadline
  + linha de suporte opcional. Dor, mecanismo, prova social e preço não
  são desta etapa.
- **Nunca inventa contraste, número ou fato de prova** — todo elemento
  concreto vem de `nova_oportunidade`, `ativos_marketing_sexys` ou
  `publico_promessa` já coletados. Mesma regra de "nunca invente dado" da
  Etapa 6 Passo 0.
- **Nunca usa vocabulário de auditoria** ("identificamos", "veredito") —
  mesma regra geral de tom da estrutura v4.
- **Nunca duplica `nova_oportunidade` literalmente** — o hero é a mesma
  promessa reformulada pro formato headline+subheadline de conversão, não
  um copy-paste do campo de promessa.
