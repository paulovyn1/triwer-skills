# Validar padrões contra casos reais

Um padrão só é confiável depois de sobreviver a uma tentativa real de derrubá-lo com um caso concreto. Detalha a etapa 3 do SKILL.md.

## O ciclo

1. **Propor a hipótese a partir de poucos dados**, deixando claro que ainda é hipótese.
2. **Testar contra um caso específico e nomeado.** Não pergunte "isso parece certo?"; pergunte "isso bate com o caso do cliente X?".
3. **Deixar o expert contestar.** Quando ele disser "não, foi diferente", esse é o dado mais valioso da etapa.
4. **Não aceitar a contestação como ponto final.** Pergunte o mecanismo: "o que exatamente está acontecendo aqui, e isso é diferente do que eu assumi?".
5. **Reescrever a hipótese para incorporar a exceção.** O padrão final fica mais preciso porque absorveu a objeção.

## Exemplo de execução (aula sobre bio do Instagram)

Os casos abaixo são ilustrativos, inventados para mostrar o ciclo. Na sua aula, use casos reais e nomeados do expert.

**Rodada 1, filtro de exclusão.** Hipótese inicial: a bio precisa de um filtro demográfico, tipo "para mulheres". Testando contra a bio de um mentorado do expert ("para quem quer sair do amadorismo"), a primeira leitura classificou a frase como filtro fraco.

O expert contestou: a frase excluía sim, quem acha isso besteira. Em vez de recuar para "ok, é filtro", a pergunta que destravou foi: "isso é o mesmo tipo de corte que 'para mulheres' faz, ou é diferente?". A resposta: a frase cortava por **estágio** (não fala com iniciante) e por **autopercepção** (só ressoa em quem já se sente amador).

Resultado: o padrão final virou "filtro fino (estágio, comportamento, autopercepção) vs. filtro grosso (categoria, demografia, fácil de copiar)", uma distinção que a hipótese original nem tinha.

**Rodada 2, prova de autoridade.** Hipótese inicial com só 3 casos: "nome fraco e número fraco tendem a andar juntos". Ao adicionar um caso sem número nenhum na bio, a pergunta foi o motivo, sem assumir resposta.

Apareceu uma variável nova: em nichos onde "vendedor de curso" prejudica a imagem, a autoridade vem de credencial de mercado (tempo, ineditismo, parceria), não de número de alunos. Testado contra mais dois casos antes de virar regra, e o expert ainda acrescentou uma segunda causa: às vezes a pessoa evita número de alunos para não ser vista só como "professor". O padrão final tem duas causas, e só apareceu porque o teste não parou na primeira confirmação.

## Sinais de que a hipótese ainda não está pronta

- Menos de 5 ou 6 casos reais nomeados
- Toda evidência vem da mesma pessoa ou do mesmo nicho
- A hipótese nunca foi contestada (a pergunta provavelmente não foi específica o bastante)
- Ainda cabe em "sim ou não": padrões reais costumam ganhar uma segunda dimensão quando testados
