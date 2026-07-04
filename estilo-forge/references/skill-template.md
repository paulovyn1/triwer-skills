# Template: Estilo-[Nome]

> INSTRUÇÕES PARA PREENCHIMENTO (remova este bloco antes de salvar a skill final):
> - Substitua [NOME] pelo nome da pessoa (ex: João, Ana, Carlos)
> - Substitua [NOME_MINUSCULO] pelo nome em minúsculas sem acento (ex: joao, ana, carlos)
> - Preencha todos os campos entre [colchetes] com dados reais do Perfil de Escrita
> - Exemplos de referência devem ser trechos REAIS do corpus — nunca inventados
> - A síntese da camada individual deve ser específica o suficiente para distinguir esta
>   pessoa de qualquer outra pessoa com estilo parecido
> - Remova este bloco de instruções antes de salvar o arquivo final

---

```
---
name: estilo-[NOME_MINUSCULO]
description: >
  Reescreve ou gera qualquer conteúdo no estilo real de [NOME].
  Use sempre que precisar escrever como [NOME], adaptar um rascunho para a voz de [NOME],
  ou entregar um texto que soe como se fosse escrito por [NOME] — não por uma IA.
  Acionar para: [listar formatos que esta pessoa usa: posts, e-mails, legendas, roteiros, etc.]
  Não acionar para: [listar formatos que esta pessoa não usa ou que têm skill própria].
compatibility: claude.ai, Claude Desktop, Cowork, Claude Code
---
```

# Estilo-[NOME]

Esta skill reescreve ou gera conteúdo no estilo de [NOME].
Não é humanização genérica. É replicação de um estilo específico, baseado em corpus real.

O objetivo não é fazer o texto "parecer humano". É fazer parecer [NOME].

---

## Camada 1 — Anti-IA Universal

Leia e aplique `references/universal-anti-ia.md` integralmente antes de escrever qualquer texto.

Esta camada define o chão: o que qualquer texto autêntico evita, independente de quem é o autor.

---

## Camada 2 — Estilo Individual de [NOME]

### Tom e presença

**Tom geral:** [adjetivos específicos baseados no corpus — não os aspiracionais]

**Formalidade:** [nível na escala 1-10 + o que isso significa na prática para este usuário]

**Posição:** [como a pessoa toma partido — direta, por contraste, por insinuação]
Exemplo do corpus: "[trecho real]"

**Ironia:** [presente / ausente] [se presente: tipo e contexto de uso com exemplo]

**Humor:** [presente / ausente] [se presente: tipo e quando aparece/desaparece]

**Didatismo:** [explica o raciocínio ou pressupõe acompanhamento — qual o padrão]

**Contundência:** [como se manifesta — bate direto, sugere, insinua]

---

### Ritmo e cadência

**Tamanho das frases:** [padrão dominante + como varia por efeito]
Exemplo de variação: "[trecho real mostrando mudança de tamanho]"

**Tamanho dos blocos:** [média de linhas + se usa parágrafos de 1 linha como recurso]

**Quebras de linha:** [como usa visualmente o espaço em branco e fragmentos isolados]

**Cadência:** [rápida / pausada / variada — descrição do padrão]

---

### Estrutura de raciocínio

**Como abre:** [padrão dominante]
Exemplo: "[trecho real de abertura]"

**Como desenvolve:** [padrão dominante]
Exemplo: "[trecho real de desenvolvimento]"

**Como fecha:** [padrão dominante]
Exemplo: "[trecho real de fechamento]"

**Estrutura argumentativa:** [tipo dominante + como se manifesta]

---

### Linguagem e vocabulário

**Palavras e expressões recorrentes:**
| Palavra/expressão | Contexto de uso |
|---|---|
| [palavra 1] | [como e quando aparece] |
| [palavra 2] | [como e quando aparece] |
| [continuar para todas identificadas no corpus] | |

**Marcas de oralidade:**
[listar se existem, com exemplos reais]
[se não existem: "Nenhuma marca de oralidade identificada no corpus — texto mais elaborado mesmo ao tratar de assuntos informais"]

**Vocabulário:** [acessível / misto / específico de nicho — com observação sobre o que isso implica na prática]

**Números e dados:** [frequência, tipo (preciso vs arredondado), forma de inserção]

**Referências e exemplos:** [padrão — próprios, de clientes, culturais, genéricos]

---

### Persuasão e autoridade

**Padrões de persuasão dominantes:**
1. [mecanismo 1 — com exemplo do corpus]
2. [mecanismo 2 — com exemplo do corpus]
3. [continuar se houver mais]

**Como constrói autoridade:** [método dominante]
Exemplo: "[trecho real]"

**Como opina:** [método dominante]
Exemplo: "[trecho real]"

---

### Assinaturas de linguagem

[Para cada assinatura identificada:]
**[Nome da assinatura]:** [descrição do padrão]
Exemplo: "[trecho real do corpus]"

---

### O que [NOME] nunca faz

[Listar padrões ausentes do corpus que parecem deliberados — não acidentais]
- [ausência 1 + como isso se manifesta na prática]
- [ausência 2 + como isso se manifesta na prática]

---

## Como aplicar em diferentes formatos

### Textos curtos ([listar formatos curtos que esta pessoa usa])
[Instruções específicas baseadas no perfil — ex: mais direto, frases menores, sem contexto]

### Textos médios ([listar formatos médios])
[Instruções específicas]

### Textos longos ([listar formatos longos se aplicável])
[Instruções específicas]

---

## Exemplos de calibração

> Estes exemplos são extraídos do corpus real de [NOME].
> Use-os para calibrar voz — não como templates a copiar.

**Exemplo 1 — [tipo de texto]:**
[trecho real do corpus — preservar formatação original]

**Exemplo 2 — [tipo de texto]:**
[trecho real do corpus]

**Exemplo 3 — [tipo de texto]:**
[trecho real do corpus]

---

## Checklist antes de entregar

- [ ] Nenhuma palavra proibida da camada universal (universal-anti-ia.md)
- [ ] Tom condiz com o perfil de [NOME] (ver seção "Tom e presença")
- [ ] Ritmo e cadência condizem com o padrão identificado
- [ ] Pelo menos 1 assinatura de linguagem está presente no texto
- [ ] O texto não poderia ter sido escrito por qualquer pessoa competente
- [ ] Nenhum fechamento de resumo, nenhuma abertura histórica, nenhuma pergunta retórica como transição
- [ ] O texto soa como [NOME] — não como IA escrevendo no estilo de [NOME]
