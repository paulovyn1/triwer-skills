# Agente avaliador do documento-hub — consistência e piso mínimo

Lido na Etapa 6, Passo 5 — pelo subagente avaliador quando `Agent`/`Task`
estiver disponível, ou pela própria conversa principal com o mesmo rigor.
Roda só depois de `nova_oportunidade` fechada — ela é o norte contra o qual
tudo é checado.

**O que o executor recebe:** o documento-hub da sessão inteiro (Etapa 1 em
diante) + este arquivo. Devolve as três checagens abaixo, cada uma com o
achado e o dado-fonte citado.

## Checagem 1 — Inconsistência

Mesmo teste de incompatibilidade da Etapa 5, Passo 8 do SKILL.md, agora
contra o hub inteiro, não só contra o público:

- **Definição/papel:** um fato declarado pressupõe, por definição, outro
  fato que um segundo dado do hub contradiz (ex.: "advogado que não
  entende de leis").
- **Plausibilidade de mercado:** um resultado/ticket/tempo declarado
  normalmente exige, na prática real do nicho, um comportamento ou
  competência que outro fato declarado nega. Improvável não é impossível
  — sinalize para confirmação, nunca resolva sozinho por suposição.

## Checagem 2 — Piso mínimo coberto

- `nova_oportunidade` presente no hub (a ausência de contradição já foi
  garantida pela bateria tripla — aqui só confirme presença).
- Público com situação de vida concreta, não demografia (Etapa 5, Passo 1).
- O que o público deseja e o que não gosta, claramente definido —
  calibração transversal pras 4 categorias de Ativos.
- Ao menos 1 risco de posicionamento (Y) identificado — se a Pergunta 4 da
  Etapa 10 ainda não rodou, sinalize como pendência, não como falha.
- Ao menos 1 fato bruto de qualquer esfera (entrega, gestão, pessoal,
  vivência) — se as Perguntas da Etapa 10 ainda não rodaram, idem:
  pendência, não falha.

## Checagem 3 — Recruzamento antes de declarar lacuna

Antes de aceitar qualquer campo como "ausente", releia o hub inteiro
procurando se outro fato já coletado — em qualquer etapa, com outra
finalidade — responde àquele campo. Só depois desse recruzamento uma
lacuna pode ser aceita como real. Erro já cometido nesta skill: um fato de
credencial coletado para outro fim foi lido como "esfera vazia" na
vivência pessoal, quando já respondia a ela.

## Formato de retorno

Para cada checagem: **OK / Pendência / Falha**, com uma frase por achado
citando o dado-fonte do hub (ou a ausência dele após o recruzamento). Não
proponha correção de conteúdo — quem decide o que fazer com cada achado é
a conversa principal, que conhece o aluno.
