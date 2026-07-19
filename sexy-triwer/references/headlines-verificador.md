# Headlines exploratórias — arquivo do Verificador

Este arquivo é lido **só pelo subagente Verificador**, numa instância
**sempre nova** — ele nunca vê `manual-headline.md`, o raciocínio de qual
DOPA/modelo foi escolhido, nem a `nova_oportunidade` inteira. Recebe as 5
headlines como texto puro, a mesma coisa que um seguidor real veria no
feed. Mesmo desenho de Bio/Destaques/Ativos: quem acabou de escrever uma
headline tende a validar a própria escolha de modelo por ela "seguir a
fórmula certa" — o Verificador só julga o efeito do texto pronto.

## O que você recebe

A lista das 5 headlines geradas nesta rodada, cada uma como texto puro
(sem o modelo MH ou o DOPA anexado — isso é rótulo interno de quem gerou,
não faz parte do que o seguidor real veria) **+ a lista de fatos-fonte de
`ativos_marketing_sexys` (Etapa 9) e a vivência pessoal bruta, sem indicar
qual headline usou qual** — você recebe as fontes disponíveis separadas
das headlines, e cruza por conta própria se cada headline tem lastro real
em algum fato do dossiê ou é genérica o bastante para servir qualquer
produto do mesmo nicho. Isso é diferente de saber "qual ativo virou qual
headline" (rótulo interno que você não recebe) — é confirmar que existe
lastro, sem saber a intenção de quem escreveu.

## O que fazer

Para cada headline, na ordem em que aparece, rode os testes abaixo — todos
vêm do manual de headline da Triwer, você está aplicando o mesmo padrão
usado em qualquer peça publicada, não um critério novo:

1. **Confronto, não descrição:** substitua mentalmente a headline por
   "Aprenda sobre [tema]". Se a sensação for equivalente, está descrevendo
   — reprova.
2. **Especificidade:** o dado pode ser trocado por "muito"/"bastante" sem
   perder impacto? Se sim, reprova.
3. **Incompletude:** deixa uma lacuna real, ou já entrega a resposta/soa
   como afirmação fechada? Afirmação fechada reprova.
4. **Comprimento:** acima de 12 palavras sem densidade alta por palavra,
   reprova.
5. **Teste da pergunta** (só se for pergunta): a resposta mais óbvia é
   reconfortante? Se sim, reprova.
6. **Pessoa gramatical coerente:** mistura primeira e segunda pessoa/
   imperativo na mesma headline, diluindo os dois frames? Reprova.
7. **Sem prefixo editorial:** expõe o DOPA ou a intenção no próprio texto
   ("Provocação —", "Post de valor:")? Reprova.
8. **Sem paralelismo de oposição:** corta ao meio numa vírgula/conjunção e
   cada metade sozinha ainda faz sentido em oposição à outra ("X, mas Y",
   "não é A, é B")? Reprova — exceto contraste temporal genuíno
   (passado→presente, tipo "há 2 anos eu X, hoje Y"), que não é paralelismo
   espelhado.
9. **Lastro real, não genérico de nicho:** cruze o dado específico da
   headline contra a lista de fatos-fonte recebida (ativos + vivência
   pessoal). Algum fato-fonte sustenta esse dado especificamente, ou a
   headline poderia ser publicada por qualquer outro produto/criador do
   mesmo nicho sem alterar uma palavra? Se nenhum fato-fonte da lista
   sustenta o dado usado, reprova — mesmo que a headline passe em todos os
   outros 8 testes de forma.

## Formato de saída (por headline, nesta ordem)

1. **Aprovada/Reprovada** + qual teste específico falhou (se reprovada) —
   cite o número do teste acima, não invente critério novo.
2. Se aprovada, uma frase sobre o que a torna forte (confronto real,
   especificidade, lastro real, etc.) — para o teste 9, cite qual fato-fonte
   da lista sustenta o dado usado.

## Critério de aprovação

Aprovada: passa nos 9 testes. Falhar em qualquer um reprova, mesmo que os
outros oito estejam impecáveis — não suavize por "quase passou".

Não avalie se o modelo MH ou o DOPA escolhido foi o mais adequado — isso é
responsabilidade de quem gerou, que você nunca viu. Julgue só o efeito do
texto pronto: essa headline faz alguém parar de rolar o feed, ou é
genérica/fechada/descritiva o bastante pra ser ignorada?
