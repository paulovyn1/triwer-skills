# Como usar o template HTML V2 do relatorio

> Leia este arquivo na Fase 3, ao gerar o HTML. Nao carregue antes: ele so importa na hora de montar o arquivo final.

## Regra principal

O arquivo `assets/template-diagnostico.html` e o template oficial V2 da skill. Copie esse arquivo via terminal para o destino final e edite somente placeholders `{{ASSIM}}` e blocos repetiveis marcados por comentarios HTML. Nao redesenhe secoes, nao recrie CSS e nao troque a estrutura visual.

Depois de copiar o template, leia tambem:

- `VERSION`, para preencher `{{VERSAO_SKILL}}`.
- `assets/hero-diagnosticador.b64.txt`, para preencher `{{HERO_PORTRAIT_SRC}}` com `data:image/jpeg;base64,` + conteudo do arquivo.
- `assets/corpo-biometrico.b64.txt`, para preencher `{{CORPO_BIOMETRICO_SRC}}` com `data:image/jpeg;base64,` + conteudo do arquivo.

## Placeholders simples

| Placeholder | Conteudo |
|---|---|
| `{{NOME_PRODUTO}}` | Nome do produto diagnosticado. |
| `{{STATUS_GERAL}}` | Um de: `Pronto para validar`, `Ajustes necessarios`, `Reconstrucao necessaria`. |
| `{{DATA_HOJE}}` | Data por extenso, ex: `20 de julho de 2026`. |
| `{{CRIADOR_NOME}}` | Nome do criador, coletado no Bloco 1. |
| `{{ESPECIALIDADE}}` | Rotulo curto do nicho/especialidade do criador. |
| `{{TICKET_LABEL}}` | Rotulo curto do preco principal, ex: `ticket atual`, `lancamento`, `mentoria`. |
| `{{TICKET_VALOR}}` | Valor principal do produto, com moeda e parcelamento se relevante. |
| `{{DIAGNOSTICO_GERAL}}` | Paragrafo final de diagnostico geral, revelado no envelope. |
| `{{BRIDGE_TEXTO}}` | Encaminhamento para a skill Sexy; sempre presente. |
| `{{VERSAO_SKILL}}` | Valor lido do arquivo `VERSION`, sem hardcode. |
| `{{HERO_PORTRAIT_SRC}}` | Data URI do asset fixo do hero. |
| `{{CORPO_BIOMETRICO_SRC}}` | Data URI do asset fixo do painel biometrico. |
| `{{SINAL_STATUS_CLASSE}}` | Classe CSS derivada de `{{SINAL_CASO}}`: `status-forte`, `status-atencao` ou `status-critico`. |

## Anamnese em ficha

A primeira grande secao e a anamnese do produto. Ela substitui o antigo bloco corrido de contexto.

- Use `BLOCO_FATO` para listas de 3 a 4 fatos por bloco da entrevista. O mesmo placeholder `{{FATO_TEXTO}}` aparece em Criador, Publico, Promessa, Produto, Prova e Aquisicao; em cada ocorrencia, substitua pelo texto daquele bloco especifico.
- `{{ANAMNESE_INSIGHT_P1}}`, `{{ANAMNESE_INSIGHT_P2}}` e `{{ANAMNESE_INSIGHT_FINAL}}` sao sinteses curtas do agente. Nao sao novas perguntas ao aluno.
- `{{MECANISMO_SUBTITULO}}` resume o mecanismo em uma linha. Se o aluno deu duracao/fases, use isso; se nao, sintetize sem inventar numero.
- `ETAPA` x N: repita o bloco marcado para cada passo real do mecanismo. Preencha `{{ETAPA_NUM}}` como `01`, `02`, etc. e `{{ETAPA_LABEL}}` como o nome curto da etapa.
- `{{PRODUTO_BADGE}}` e opcional; use um detalhe objetivo de entrega/acesso. Se nao houver, remova o badge inteiro.
- `PRECO_TIER` x 1-3: preencha ate tres linhas de preco. Se houver menos de tres variacoes, remova as linhas sobrando do template copiado.
- `{{NIVEL_EVIDENCIA}}` deve ser `baixo`, `moderado` ou `forte`, julgado a partir do Bloco 7.
- `LEITURA` x 2: preencha `{{LEITURA_TITULO}}` e `{{LEITURA_TEXTO}}` com duas leituras estrategicas de fechamento da anamnese.

## Painel biometrico

O painel `Sinais vitais do produto` substitui o radar antigo. Nao gere `{{RADAR_SVG}}`; esse placeholder nao existe mais.

Mapeamento fixo dos 4 pilares:

| Pilar | Origem |
|---|---|
| Pilar 1, `Publico e situacao` | Bloco 2. |
| Pilar 2, `Promessa` | Bloco 3. |
| Pilar 3, `Mecanismo` | Bloco 4. |
| Pilar 4, `Prova e preco` | Blocos 6 e 7 combinados. |

Para cada pilar `n` de 1 a 4, preencha:

- `{{PILARn_STATUS}}`: `Forte`, `Ajuste`, `Estrutural` ou `Critico`, alinhado a gravidade dos achados.
- `{{PILARn_STATUS_CLASSE}}`: classe CSS correspondente ao status: `status-forte`, `status-ajuste`, `status-estrutural` ou `status-critico`.
- `{{PILARn_DESCRICAO}}`: 1 a 2 frases de sintese.
- `PILARn_PONTO_BOM` x 2: dois pontos que ja ajudam a oferta.
- `PILARn_PONTO_CRITICO` x 2: dois pontos que mais precisam de ajuste.
- `{{PILARn_CLAREZA}}`, `{{PILARn_ADERENCIA}}`, `{{PILARn_ESPECIFICIDADE}}`: use somente valores 25, 55 ou 85 para evitar falsa precisao. Regra: baixo = 25, medio = 55, alto = 85.

`{{SINAL_CASO}}` e derivado de `{{STATUS_GERAL}}`: `Pronto para validar` -> `Estavel` com `{{SINAL_STATUS_CLASSE}}` = `status-forte`; `Ajustes necessarios` -> `Atencao` com `status-atencao`; `Reconstrucao necessaria` -> `Critico` com `status-critico`.

## Diagnostico geral

`{{DIAGNOSTICO_GERAL}}` vai dentro do envelope interativo. Escreva um paragrafo direto, com o veredito do caso, sem listar receita de correcao.

## Achados em carrossel

Inclua apenas criterios com achado real, ordenados por gravidade: critico, estrutural, ajuste fino. Para cada achado, repita os tres blocos correspondentes na mesma ordem e indice:

- `ACHADO_CARD` x N, com `data-index` sequencial comecando em `0`.
- `DOT` x N, com o mesmo `data-index`.
- `ACHADO_PANEL` x N, com o mesmo `data-index`.

Preencha:

| Placeholder | Conteudo |
|---|---|
| `{{CRITERIO_NUM}}` | Numero 1-15 do criterio em `references/criterios.md`. |
| `{{CRITERIO_NOME}}` | Nome do criterio. |
| `{{GRAVIDADE_ICONE}}` | `▲` para critico, `●` para estrutural, `■` para ajuste fino. |
| `{{GRAVIDADE_LABEL}}` | `Problema critico`, `Problema estrutural` ou `Ajuste fino`. |
| `{{ACHADO_O_QUE}}` | O que esta acontecendo, baseado no que o aluno disse. |
| `{{ACHADO_POR_QUE}}` | Impacto em conversao, implementacao, retencao ou operacao. |

Nao inclua uma secao separada de pontos fortes. Pontos positivos aparecem dentro do painel biometrico em `PILARn_PONTO_BOM`.

## Encaminhamento para Sexy

A secao final junta o bridge e as perguntas em aberto. Ela e sempre incluida.

- `{{BRIDGE_TEXTO}}`: explique por que o proximo passo natural e levar o caso para a skill Sexy.
- `PERGUNTA` x N: repita a linha para cada pergunta em aberto. Preencha `{{PERGUNTA_NUM}}` como `01`, `02`, etc. e `{{PERGUNTA_TEXTO}}` com a pergunta.

## Checklist antes de entregar

- Remova comentarios auxiliares do template copiado que ainda contenham exemplos de placeholders, depois confira que nenhum placeholder `{{...}}` ficou no HTML final.
- Os blocos repetiveis foram duplicados/removidos no arquivo copiado, nao deixados como comentario de exemplo.
- `{{HERO_PORTRAIT_SRC}}` e `{{CORPO_BIOMETRICO_SRC}}` viraram data URIs validas.
- `{{VERSAO_SKILL}}` veio do arquivo `VERSION`.
- O HTML final continua autocontido e pode ser anexado na conversa com a skill Sexy.
