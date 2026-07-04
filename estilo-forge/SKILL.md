---
name: estilo-forge
description: >
  Fábrica de skills de estilo personalizado. Guia o processo completo de captura de voz autoral:
  coleta de corpus → validação → análise profunda → geração da skill "Estilo-[Nome]" pronta para uso.
  Use sempre que alguém quiser capturar sua voz de escrita, criar uma skill que escreva como uma
  pessoa específica, treinar Claude no estilo de alguém, ou disser: "cria um Estilo-[Nome]",
  "quero que Claude escreva como eu", "captura meu jeito de escrever",
  "como faço o Claude escrever no meu estilo", "preciso de uma skill de voz para [nome]".
  O output não é texto final — é uma skill nova instalada em ~/.claude/skills/estilo-[nome]/.
  Acione esta skill antes de tentar replicar qualquer estilo de escrita de qualquer pessoa.
compatibility: claude.ai, Claude Desktop, Cowork, Claude Code
---

# estilo-forge

Esta skill não escreve texto. Ela **cria uma skill que vai escrever**.

O output final é um arquivo `~/.claude/skills/estilo-[nome]/SKILL.md` — uma skill personalizada
instalada localmente, treinada na voz real do usuário, não em IA imitando voz humana genérica.

O processo tem **7 etapas obrigatórias em sequência**. Cada etapa é um gatekeeper: a próxima
só começa quando a anterior está completa. Não pule etapas.

---

## ETAPA 0 — Onboarding

Apresente ao usuário o processo completo antes de começar:

**O que esta skill faz:**
Analisa textos reais escritos pelo usuário, extrai padrões reais de linguagem, raciocínio e
estrutura, e gera uma skill personalizada — o "Estilo-[Nome]" — que Claude usa para escrever
como essa pessoa em qualquer projeto.

**O que vai ser entregue:**
Um arquivo `~/.claude/skills/estilo-[nome]/SKILL.md` instalado e pronto. Não uma descrição
de estilo — uma skill operacional invocável com `/estilo-[nome]`.

**O que o usuário precisa preparar:**
Textos reais escritos por ele. Quantidade e formato serão explicados na próxima etapa.

**O que não esperar:**
Esta skill não gera texto agora. O processo tem etapas porque é análise real, não simulação.

Ao final, pergunte: **"Entendido. Quer que eu explique como montar a base de textos?"**

---

## ETAPA 1 — Instrução de coleta de corpus

Instrua o usuário a montar a base autoral. Explique cada item abaixo.

### O que enviar

Textos reais escritos pelo próprio usuário, em qualquer formato:
- Posts (Instagram, LinkedIn, Twitter/X, Facebook)
- E-mails (os que representam a voz natural, não os formais burocráticos)
- Roteiros de vídeos, podcasts, lives
- Legendas de conteúdo
- Newsletters, artigos, blog posts
- Transcrições de aulas, stories falados, webinars
- Copies, páginas de venda, sequências de e-mail
- Mensagens longas em chats, se representativas

### Volume mínimo

**10 textos substanciais** ou **~3.000 palavras no total**.

Textos curtos (menos de 50 palavras) só contam se forem numerosos e consistentes —
um tweet isolado não serve, mas 40 tweets com padrão reconhecível servem.

### Formato recomendado

Um único arquivo TXT com blocos separados por tipo:

```
[POST]
texto do post aqui

[EMAIL]
texto do e-mail aqui

[ROTEIRO]
trecho do roteiro aqui
```

Etiquetar os blocos não é obrigatório — mas ajuda na análise.

### O que NÃO enviar

- Textos escritos majoritariamente por IA (mesmo que revisados pela pessoa)
- Textos muito editados por outras pessoas (ghostwriting pesado)
- Textos genéricos que qualquer pessoa competente poderia ter escrito
- Apenas textos curtos demais para revelar padrão
- Textos excessivamente técnicos se isso não representa o estilo habitual
- Um único formato de texto se a pessoa escreve em múltiplos formatos

### Teste mental para o usuário

"Se alguém lesse esses textos sem saber seu nome, conseguiria reconhecer que é você?"
Sim → provavelmente bom. Não → buscar textos mais representativos.

Ao final: **"Quando tiver os textos, cole aqui ou mande o arquivo TXT."**

---

## ETAPA 2 — Validação do corpus (gatekeeper obrigatório)

Ao receber o corpus, **avalie antes de qualquer análise**. Esta etapa não é opcional.

### Critérios

| Critério | Suficiente | Insuficiente |
|---|---|---|
| Volume | ≥3.000 palavras ou ≥10 textos | <2.000 palavras, poucos textos curtos |
| Variedade | ≥2 formatos distintos | Tudo do mesmo formato e contexto |
| Densidade | Textos com desenvolvimento real | Só bullets, só frases soltas |
| Consistência | Voz reconhecível entre os textos | Voz completamente diferente entre amostras |
| Autenticidade | Marcas pessoais de linguagem presentes | Linguagem perfeitamente homogênea |
| Contaminação IA | Baixa presença de padrões artificiais | Alta presença de portanto, dessa forma, floreio |

### Se insuficiente

**Não prossiga.** Diga o que está faltando — de forma específica:
- "Volume abaixo do mínimo — preciso de pelo menos X palavras a mais"
- "Todos os textos são do mesmo contexto — inclua formatos diferentes"
- "Detectei alto nível de padrões de IA — você tem textos mais antigos ou escritos sem IA?"
- "Os textos são curtos demais para revelar padrão — envie textos com mais desenvolvimento"

### Se suficiente

Confirme: **"Corpus recebido e validado. Iniciando a análise agora."**
Siga para ETAPA 3.

---

## ETAPA 3 — Análise profunda do estilo

**Leia `references/analysis-framework.md` antes de começar.**

Analise o corpus mapeando cada dimensão do framework. A análise deve ser:
- Baseada em evidências reais — cite trechos do corpus sempre que possível
- Específica — nunca use "tom informal" sem explicar o que isso significa para esta pessoa
- Honesta sobre onde há padrão claro e onde há variação legítima

Ao final, produza um **Perfil de Escrita completo** com todas as dimensões preenchidas
e uma síntese de 5-7 frases descrevendo o estilo de forma que qualquer pessoa
consiga aplicá-lo sem ter lido o corpus.

Avise o usuário: **"Análise concluída. Aqui está o Perfil de Escrita:"**
[apresente o perfil completo]

Depois: **"Esse perfil representa bem seu estilo? Tem algo que parece errado ou que estou subestimando?"**

Incorpore correções do usuário antes de avançar.

---

## ETAPA 4 — Separação das camadas

Com o Perfil de Escrita aprovado, monte as duas camadas da skill filho:

### Camada 1 — Universal anti-IA (fixa)

**Leia `references/universal-anti-ia.md`** integralmente.

Esta camada não muda por usuário. Define o que qualquer texto autêntico evita —
padrões de IA que destroem autenticidade independente de quem escreve.

### Camada 2 — Estilo individual (variável)

Construída exclusivamente a partir do Perfil de Escrita da ETAPA 3, com:
- Como esta pessoa escreve
- Como organiza raciocínio
- Recursos de linguagem usados com frequência
- Assinaturas identificadas
- O que replicar, o que evitar

As duas camadas são complementares. A universal define o chão (o que qualquer
escrita humana autêntica evita). A individual define o teto (o que esta pessoa
especificamente faz).

---

## ETAPA 5 — Geração da skill final

**Leia `references/skill-template.md`** como base estrutural.

Preencha cada seção do template com dados reais da análise:
- Nome e descrição da skill filho (`estilo-[primeironome]` em minúsculas sem acento)
- Camada universal (importada do universal-anti-ia.md)
- Camada individual com todas as dimensões mapeadas
- Exemplos reais extraídos do corpus (nunca inventados)
- Instruções de aplicação por formato de texto

Ao concluir, use o **Write tool** para salvar:

```
Caminho: ~/.claude/skills/estilo-[nome]/SKILL.md
```

Confirme: **"Skill salva em `~/.claude/skills/estilo-[nome]/SKILL.md`. Vamos testar agora."**

---

## ETAPA 6 — Protocolo de validação

Gere **3 textos de teste em formatos diferentes** usando a skill filho recém-criada.
Escolha formatos que o usuário usa na vida real (ex: post curto, e-mail, legenda).

Para cada texto:
1. Mostre o texto gerado
2. Peça comparação com material real do corpus
3. Pergunte: **"Isso soa como você ou ainda tem cara de IA? O que parece errado?"**

### Diagnóstico com base no feedback

Identifique onde está o problema:
- **Ainda soa como IA** → camada universal não está sendo aplicada corretamente
- **Voz não reconhecível** → camada individual incompleta ou com dimensão errada
- **Ritmo errado** → dimensões de cadência precisam revisão
- **Vocabulário estranho** → assinaturas não capturadas ou capturadas errado

### Refinamento

Se há problemas:
1. Identifique as dimensões específicas no Perfil de Escrita que precisam ajuste
2. Corrija a camada individual na skill filho
3. Reescreva as seções com problema no SKILL.md filho
4. Salve a versão revisada via Write tool
5. Gere novos textos de teste e repita o ciclo

A skill filho está pronta quando o usuário reconhecer a própria voz nos textos.

---

## Regras que nunca mudam

- A camada universal anti-IA é sempre importada integral — nunca editada por usuário
- Exemplos na skill filho são sempre reais (do corpus) — nunca gerados ou inventados
- A ETAPA 2 é sempre bloqueante — corpus fraco não avança
- A skill filho não contém referências a outros usuários (não vazar nomes, estilos alheios)
- Nome da skill filho: `estilo-[primeironome]` em minúsculas sem acento (ex: estilo-joao, estilo-ana)
- A skill filho gerada é uma skill operacional — não um documento de referência
