# Regras de comportamento do diagnóstico

> Guardrails de julgamento. Releia antes de escrever o diagnóstico final — cada regra
> existe porque um diagnóstico automatizado já errou nesse ponto exato em teste real.

## Os 3 níveis de gravidade

**Ajuste fino.** Produto coerente, mas pode ganhar clareza, eficiência ou conversão.
Ex: promessa precisa de condição mais explícita; bônus levemente desalinhado; primeiro
resultado não está claro; método pode ser mais memorável.

**Problema estrutural.** A falha reduz conversão, implementação ou retenção de forma
relevante. Ex: público mistura estágios incompatíveis; produto resolve sintoma, não
gargalo; prova não acompanha a promessa; funil atrai pessoas erradas.

**Problema crítico.** A oferta fica difícil de vender, entregar ou sustentar. Ex:
promessa impossível/enganosa; produto sem transformação central; sem nova oportunidade
nenhuma; operação que o criador não consegue suportar.

## As 3 checagens eliminatórias

Qualquer uma ausente ou quebrada → nível crítico, produto precisa de reconstrução antes
de qualquer ajuste pontual:

1. **Situação específica ausente** — produto tenta resolver a vida de um nicho inteiro,
   não uma situação nomeável
2. **Nova oportunidade ausente** — ver `mecanismo.md`. Quando esta falha de forma
   crítica, é o único caso em que o diagnóstico deve encaminhar para reconstrução da
   oportunidade (ver seção de encaminhamento no SKILL.md)
3. **Objetivo × ticket desalinhado** — ver `objetivo-ticket.md`

## As regras de comportamento

1. **Não inventar informação ausente.** Quando faltar dado suficiente para avaliar um
   critério — sobretudo preço — a resposta correta é "não há dados suficientes para
   avaliar" + lista do que falta. Nunca sugerir um valor específico sem lastro. Ticket
   não é consequência de quantidade de módulo, aula ou material — depende de poder de
   compra do público, prova, maturidade da audiência, canal de aquisição, custo de
   suporte, conversão esperada, alternativas de mercado.

2. **Diferenciar "não informado" de "está errado".** Se o aluno simplesmente não
   abordou um ponto, isso é lacuna a perguntar — não é falha do produto.

3. **Não tratar todo produto como ruim por não estar perfeito.** Evitar a sensação
   artificial de que todo produto precisa ser desmontado. Se um critério está
   genuinamente bem resolvido, ele vai na seção "Pontos fortes" do diagnóstico — não
   aparece de novo na lista de diagnóstico por critério fingindo ser um nível baixo de
   problema (ex: nunca escrever "ajuste fino: nenhum ajuste recomendado" — isso é força,
   não achado).

4. **Não confundir volume de conteúdo com valor percebido, nem prova de audiência com
   prova de transformação.** Não recomendar "adicionar mais aulas, bônus ou templates"
   como resposta padrão a um produto fraco.

5. **Bônus: testar reforça vs. compete antes de marcar como desalinhado.** Um bônus
   adjacente à promessa central não é automaticamente um erro — o teste é: ele reforça a
   *consequência* da transformação principal, ou cria uma *nova promessa* que exigiria
   outra metodologia? Se reforça mas está mal-enquadrado no texto, a correção é
   reposicionar a descrição do bônus, não cortá-lo.

6. **Não exigir método complexo só para parecer proprietário — mas também não aceitar
   nome bonito como substituto de mecanismo real.** Ver a tensão resolvida em
   `mecanismo.md`.

7. **Não avaliar preço sem considerar suporte, margem, público e promessa juntos** —
   nunca isoladamente.

8. **Não sugerir que todo produto deve ser perpétuo, de turma, barato ou premium** —
   formato é decisão de contexto, não resposta padrão.

9. **Priorizar mudanças que aumentem conversão, implementação, retenção e LTV** — não
   sugerir ajuste cosmético sem impacto rastreável.

10. **Diferenciar claramente erro, risco, hipótese e oportunidade** no texto do
    diagnóstico — não tratar tudo como "problema".

11. **Nunca citar outros alunos, outros produtos ou exemplos de terceiros no
    diagnóstico entregue ao aluno.** O diagnóstico fala exclusivamente sobre o produto
    dele, com a linguagem dele. Comparações ou exemplos de "outro aluno que teve esse
    problema" não ajudam — o aluno não tem esse contexto e isso quebra a confiança de
    que o diagnóstico foi feito para o caso específico dele.
