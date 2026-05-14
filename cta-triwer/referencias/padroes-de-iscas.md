# Padrões de Iscas — Triwer
_Arquivo: padroes-de-iscas.md — v1.0_
_Lido pela skill cta-triwer APENAS quando for criar ou avaliar uma isca nova._
_Baseado em análise de 9 fluxos reais com dados de performance._

---

## O que este arquivo é

Guia de criação de iscas baseado em padrões extraídos de fluxos reais do Manychat.
Não é uma lista de iscas prontas — é o que faz uma isca funcionar ou não.

A skill lê este arquivo quando:
- O usuário não tem isca adequada para o tema do post
- O usuário quer criar uma isca nova
- A skill detectou menção de entrega nova durante a conversa

---

## O que realmente decide se uma isca performa bem

Os dados dos 9 exemplos analisados provam que **o volume de acionamentos não é decidido pela isca em si — é decidido pelo que acontece antes do direct.**

### Fator 1 — A objeção precisa ser quebrada no post, não no fluxo

A isca com maior taxa de entrada de todos os exemplos (91%) tinha os slides do carrossel dizendo explicitamente: "não precisa de mega rotina nem de vídeo." Quem chegou ao direct já tinha a objeção removida.

**Regra:** identifique qual é a principal objeção de quem seguiria a isca mas não comentaria. Quebra essa objeção no post antes de apresentar o código.

### Fator 2 — A promessa precisa ser pessoal e específica

As iscas com as maiores taxas de botão (86-91%) usaram uma das duas estruturas:
- "o mesmo [recurso] que eu utilizo" — acesso ao método pessoal
- "lista de formas de [resultado específico]" — entrega nomeada com clareza

As iscas com menores taxas (59-61%) usaram promessas amplas como "poderoso demais pra caber aqui" — funciona, mas converte menos na entrada.

**Regra:** "o mesmo checklist que eu uso em todas as campanhas" performa melhor que "uma ferramenta poderosa." Especificidade > grandiosidade.

### Fator 3 — Número ou resultado concreto na promessa

Iscas que combinaram acesso ao método pessoal + resultado com número tiveram volume e taxa acima da média:
- "o mesmo script que eu utilizo" → 374 acionamentos, 86%
- "o mesmo funil SIMPLES que eu uso para vender de R$197 a R$12.000" → 176, 75%
- "mapa para faturar em 7 dias via stories" → 200, 79%

**Regra:** se tiver número ou resultado, use. Se não tiver, substitua por especificidade de método ("passo a passo", "sequência", "framework").

### Fator 4 — O código como declaração de intenção

Dois padrões de código foram identificados:

**Código técnico curto** (CVT, TRM, GDP, 1BF) — cria facilidade de digitação e identidade de isca. Funciona bem.

**Código como frase de intenção** ("quero a lista", "quero a lista") — filtra ativamente quem quer aquilo específico. A isca SDS com "quero a lista" teve 715 entradas e 91% de taxa. O comentário já era um ato de comprometimento.

**Regra:** para iscas de alto volume, código curto funciona. Para iscas que precisam de audiência altamente qualificada, frase de intenção converte melhor no botão.

---

## Os 5 tipos de isca identificados

### Tipo 1 — Isca de Acesso (texto direto no MC)

**O que é:** o recurso chega como texto dentro do Manychat logo após o botão.
**Melhor para:** scripts, checklists, sequências, passo a passo textual.
**Exemplos:** OFVL (script), 1BF (checklist), Lista SDS (lista de formas).
**Característica:** entrega rápida + fluxo continua para aquecimento e oferta.
**Taxa de botão média:** 83-91%.

**Como criar:**
- Defina o recurso como texto estruturado (bullets, numeração ou parágrafos curtos)
- Entregue na segunda mensagem, logo após o botão
- Continue o fluxo com aquecimento antes da oferta

---

### Tipo 2 — Isca Episódica (conteúdo em partes no MC)

**O que é:** o conteúdo é entregue em etapas dentro do Manychat, com botão para avançar entre partes.
**Melhor para:** frameworks com múltiplos pilares, métodos em etapas, sequências que precisam de comprometimento progressivo.
**Exemplos:** A007 (7 pilares), GDP (3 níveis), TRM (sequência trampolim).
**Característica:** cada etapa pede um clique → qualifica quem está engajado de verdade.
**Taxa de botão médio:** 59-81%. Entrada moderada, retenção alta.

**Como criar:**
- Estruture em 2-4 partes com nomes claros ("Nível 1", "Cena 2", "Pilar 1")
- Cada parte termina com pergunta de identificação antes de avançar
- Reserve a oferta ou bônus para o final de quem completou tudo
- Opcional: easter egg para quem chega até o fim

---

### Tipo 3 — Isca com Link Externo (vídeo-aula ou página)

**O que é:** o Manychat entrega um link para acessar o conteúdo fora do Instagram (site, página de captura, vídeo).
**Melhor para:** vídeo-aulas, materiais mais ricos, conteúdo que precisa de contexto maior.
**Exemplos:** F7D (link para vídeo-aula no site), DESEJO (imagens + link).
**Característica:** o Manychat serve como "corredor" — entrega um aperitivo e depois redireciona.
**Taxa de clique no link:** 84% de quem chegou até ele.

**Como criar:**
- Entregue um aperitivo primeiro (imagem do framework, texto resumido)
- Posicione o link como "a Chefia fez um vídeo explicando melhor, ela liberou por 24h"
- Use UTM no link para rastrear conversões
- Urgência: "disponível por tempo limitado" funciona para aumentar clique imediato

---

### Tipo 4 — Isca de Diagnóstico (quiz ou perguntas personalizadas)

**O que é:** a isca não é um conteúdo fixo — é um diagnóstico personalizado baseado nas respostas do usuário.
**Melhor para:** quando o público está em estágios diferentes e a isca certa depende do perfil.
**Exemplos:** Quiz SI (funil ideal por momento), GDP parcialmente.
**Característica:** entrada moderada (61%), mas retenção altíssima e qualidade de lead superior.

**Como criar:**
- Promessa: "descubra [X] ideal para o seu momento" — não "vou te dar Y"
- Perguntas: 3-5 perguntas com botões de resposta (não campo de texto livre)
- Cada resposta salva em campo customizado → permite segmentação futura
- Resultado personalizado baseado nas respostas
- O produto aparece como "próximo passo natural" do diagnóstico

---

### Tipo 5 — Isca Experiencial (o fluxo demonstra o que ensina)

**O que é:** a isca não entrega o conteúdo separado — o próprio fluxo aplica o método enquanto o explica.
**Melhor para:** quando o método pode ser demonstrado conversacionalmente.
**Exemplo:** 1BF (checklist de antecipação — o bot usou as estratégias enquanto as explicava).
**Característica:** o momento "percebi que você fez isso comigo" gera impacto de autoridade máximo.

**Como criar:**
- Mapeie as etapas do método que será ensinado
- Construa o fluxo de forma que cada mensagem aplique uma etapa do método
- Planeje a revelação: "as perguntas que eu te fiz eram exatamente a estratégia"
- É o tipo mais complexo de criar — reserve para métodos que funcionam bem em conversa

---

## Como escolher o tipo certo

```
O conteúdo da isca é um recurso único (texto, lista, script)?
→ Tipo 1 — Isca de Acesso

O conteúdo tem múltiplas partes ou pilares?
→ Tipo 2 — Isca Episódica

O conteúdo precisa de mais contexto do que cabe em texto de MC?
→ Tipo 3 — Link Externo

O público está em estágios diferentes e a isca ideal varia por perfil?
→ Tipo 4 — Diagnóstico

O próprio método pode ser demonstrado na conversa?
→ Tipo 5 — Experiencial
```

---

## O que fazer dentro do fluxo depois de entregar a isca

Todos os fluxos com bom volume de conversão seguiram este padrão após a entrega:

1. **Entrega imediata** — nunca demorar para entregar o que foi prometido
2. **Aquecimento por identificação** — "você também sente isso?" com botão sim/não
3. **Prova social** — depoimento ou screenshot de resultado de aluno
4. **Transição natural** — "foi assim que ela foi de X para Y" antes de apresentar o produto
5. **Oferta** — apresentada como "próximo passo" de quem recebeu a isca, nunca como interrupção
6. **Saída elegante** — para quem recusou: sem insistência, sem pressão
7. **Lembrete opcional** — "quer que eu te lembre amanhã?" — 73% disseram sim quando foi oferecido

---

## Como apresentar a isca no post (o que acontece antes do direct)

Este é o fator mais ignorado e o mais decisivo.

### O que a narrativa do post precisa fazer antes de apresentar o código:

1. **Mostrar o problema** — a situação que a isca resolve (não falar da isca ainda)
2. **Gerar identificação** — o leitor precisa pensar "isso sou eu"
3. **Quebrar a objeção principal** — o motivo pelo qual alguém poderia não comentar
4. **Apresentar a isca como consequência** — não como produto, como "então decidi liberar"
5. **Código em slide isolado** — com comando claro e simples

### Frases que funcionam para apresentar a isca:

- "Decidi liberar o mesmo [recurso] que eu utilizo"
- "Esse é poderoso demais para caber neste carrossel, comenta [código]"
- "Liberado 🔓 [contexto de recompensa ou meta]"
- "Vou te entregar a estrutura para você no direct"
- "Quer ver na prática como fazer isso? Comenta [código]"

### Frases que funcionam menos:

- "Comenta [código] para receber mais" — genérico
- "Acessa o link da bio" — perde o mecanismo do Manychat
- Qualquer promessa que poderia ser de qualquer post de qualquer pessoa

---

## Como criar uma isca nova do zero

Use este processo quando o usuário não tiver isca adequada:

**Passo 1 — Identificar o tema do post**
O que o post ensinou ou mostrou? Qual é o próximo passo natural de quem leu?

**Passo 2 — Definir o formato de entrega**
O recurso existe (texto, vídeo, imagem)? Consulte os 5 tipos acima.

**Passo 3 — Nomear a isca com especificidade**
Evite nomes genéricos. Use o padrão: "[o que entrega] + [para quem] + [resultado esperado]"
- Ruim: "Estratégias de stories"
- Bom: "Lista de formas de se conectar com sua audiência mesmo sem vídeo"
- Bom: "Script para construir oferta irresistível para produtos de R$97"

**Passo 4 — Criar o código**
- 2 a 6 letras temáticas: relacionadas ao tema da isca, fáceis de digitar
- Ou frase de intenção para iscas que precisam de público mais qualificado
- Nunca: INFO, MAIS, QUERO, ACESSO

**Passo 5 — Definir o tipo de fluxo**
Com base no tipo de isca escolhido, estruturar:
- Mensagem de abertura (confirmação do que comentou + botão)
- Entrega da isca
- Aquecimento pós-entrega
- Transição para o produto
- Saída elegante para quem recusou

**Passo 6 — Sugerir cadastro no Notion**
Após definir a isca, sempre oferecer para cadastrar na database "Iscas gerais" do Notion do usuário.
