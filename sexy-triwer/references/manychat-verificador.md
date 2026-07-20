# Simulação de fluxo ManyChat — arquivo do Verificador

Este arquivo é lido **só pelo subagente Verificador**, numa instância
**sempre nova** — ele nunca vê `manychat-gerador.md`, o raciocínio de
quais ativos/provas foram usados, nem o dossiê completo. Recebe o roteiro
como texto puro, a mesma coisa que um seguidor real leria no direct do
Instagram. Mesmo desenho de Bio/Destaques/Ativos/Headlines/Hero: quem
acabou de escrever o roteiro tende a validar a própria escolha de
conteúdo — o Verificador só julga o efeito do texto pronto.

## O que você recebe

As 10 variáveis de bloco (`manychat_saudacao`, `manychat_aquecimento`,
`manychat_permissao`, `manychat_demonstracao`, `manychat_prova_social`,
`manychat_pitch`, `manychat_cta`, `manychat_entrega`,
`manychat_fallback_duvida`, `manychat_fallback_nao_quero`), cada uma como
texto puro na ordem em que apareceriam na conversa — sem rótulo de qual
ativo/dado-fonte alimentou cada bloco (isso é informação interna de quem
gerou). Leia as 10 em sequência como se fosse a conversa completa que um
seguidor real veria no direct, mesmo elas chegando como campos separados.

## O que fazer

Rode os testes abaixo sobre o roteiro inteiro:

1. **Continuidade, não repetição:** o Bloco 1 (Saudação) e o Bloco 2
   (Aquecimento) presumem que a pessoa já viu o gatilho (post/tema) — ou
   o texto pergunta "você viu que..." / resume o que já foi visto? Se
   resume, reprova.
2. **Permissão antes de revelar:** o Bloco 3 pede licença antes de
   qualquer revelação importante, ou entrega direto? Entregar sem pedir
   permissão reprova.
3. **Sem jargão de automação visível:** aparece alguma palavra técnica de
   configuração de plataforma (tag, UTM, webhook, custom field, planilha,
   "ação") em qualquer bloco de texto que o visitante leria? Se sim,
   reprova — isso não é conversa real, é vazamento de bastidor técnico.
4. **Demonstração é experiência, não lista:** o Bloco 4 mostra o
   mecanismo em ação (algo sendo demonstrado), ou é uma lista de
   features/benefícios disfarçada? Lista disfarçada reprova.
5. **Prova social real ou ausência sinalizada:** o Bloco 5 tem prova
   concreta e nomeada (não vaga, tipo "vários alunos"), ou está
   explicitamente marcado como lacuna? Prova vaga sem ser marcada como
   lacuna reprova — mas bloco ausente/marcado como lacuna real não
   reprova (é honestidade sobre o dossiê, não falha de execução).
6. **Pitch não pede permissão duplicada:** se o Bloco 3 (Permissão) já
   criou expectativa de revelação, o Bloco 6 (Pitch) pede permissão de
   novo logo no início, redundante? Reprova — a pessoa já disse sim, ir
   direto ao pitch.
7. **CTA tem exatamente 3 saídas:** o Bloco 7 oferece sim / dúvida / não
   quero, todas levando a continuação (nenhuma é beco sem saída)? Menos
   de 3 opções, mais de 3 botões, ou uma opção sem continuação, reprova.
8. **Fallback de "não quero" nunca abandona:** o Bloco 9 (não quero) só
   encerra a conversa sem oferecer nada, ou dá uma saída digna (valor,
   conteúdo relacionado)? Abandono seco reprova.
9. **Botões com variação humana:** fora da Saudação (que é sempre botão
   único), os demais blocos com botão usam 2-3 variações de texto pro
   mesmo destino, ou um botão genérico repetido ("Clique aqui", "Saiba
   mais")? Botão genérico reprova.
10. **Lastro real, não genérico:** qualquer número, depoimento ou dado
    específico usado no roteiro (pitch, prova social, demonstração)
    aponta pra um fato que só esse aluno/produto tem, ou poderia servir
    qualquer produto do mesmo nicho? Dado genérico reprova.

## Formato de saída

1. **Aprovado/Reprovado** + qual(is) teste(s) específico(s) falhou(aram)
   — cite o número do teste, não invente critério novo.
2. Se aprovado, uma frase sobre o que torna o roteiro forte (continuidade
   real, permissão bem usada, lastro concreto, etc.).

## Critério de aprovação

Aprovado: passa nos 10 testes. Falhar em qualquer um reprova, mesmo que
os outros nove estejam impecáveis — não suavize por "quase passou".

Não avalie se a estrutura de 9 blocos foi a escolha certa — isso é
responsabilidade de quem gerou, que você nunca viu. Julgue só o efeito do
texto pronto: esse roteiro soa como conversa real de alguém que confia no
Sun/assistente, ou soa como campanha de automação disfarçada de
conversa?
