# Estrutura de referência e como estudar uma referência

## Por que isto existe
Na primeira versão da página que originou esta skill, o esqueleto foi
reaproveitado de uma página anterior do mesmo expert, só com o conteúdo trocado.
O aluno rejeitou: "ficou idêntica, era para estar na estrutura da referência".
A causa foi ler a referência só em texto, sem ver o layout. Texto diz o que tem
na página. Só o screenshot diz como ela se organiza, e a estrutura é o que o
aluno pediu para copiar.

## Como estudar uma referência (sempre, antes da copy)
1. Abra a página no navegador (Claude in Chrome ou print) e role de cima a baixo
   com screenshots a cada ~700px. Se o aluno só mandou texto, peça o link.
2. Liste as seções **na ordem**, com: o que a seção afirma, que componente usa
   (caixas numeradas, cartões brancos, pílulas em loop, texto gigante, lista com
   valor riscado) e se o fundo é claro ou escuro.
3. Anote o ritmo: a referência alterna painéis escuros arredondados e seções
   claras com grade de pontos. Esse alternar é parte da identidade da estrutura.
4. Só então escreva o que cada seção vai dizer com o conteúdo do aluno.

Se o aluno diz "a estrutura é essa", a ordem e os componentes da referência
valem mais do que qualquer página anterior dele. Mantenha a identidade visual
dele (cores, fontes, logo), mas não o esqueleto das páginas antigas.

## A estrutura validada (página de curso de ticket médio, 17 blocos) mapeada para o kit

| # | Na referência | No kit (`Sections.jsx`) | Fundo |
|---|---|---|---|
| 1 | Cabeçalho com logo e botão fixo | `Nav` (botão sem preço) | claro |
| 2 | Hero centralizado: headline, subtítulo, cartão de vídeo vertical, microtexto, botão | `Hero` (headline, subtítulo, player da VSL, botão) | claro |
| 3 | Frase de identificação + chamada para o resultado | `Ident` (3 frases curtas) | painel escuro |
| 4 | Galeria de cases com resultado em destaque | `Provas` (3 cartões) + botão | painel escuro |
| 5 | Texto gigante que acende no scroll | `Giant` | claro |
| 6 | "O que é" + 3 caixas numeradas | `Travas` e `OQueE` (3 caixas brancas) | painel escuro |
| 7 | "Para quem é" com pílulas de profissões em loop e cartão branco | `ParaQuem` | painel escuro |
| 8 | Depoimentos por nicho (prints) | `Depoimentos` (só aparece se houver) | painel escuro |
| 9 | N etapas em cartões brancos grandes, cada uma com "Resultado Esperado" | `Etapas` | painel escuro |
| 10 | Palavra "BÔNUS" gigante ao fundo + cartões de bônus | `Bonus` | claro + cartões escuros |
| 11 | Recapitulando: lista com valor riscado, barra de total, cartão de preço | `Oferta` | claro |
| 12 | "Pode ser recuperado em..." com casos | `Custo` (a conta do custo de ficar parado) | painel escuro |
| 13 | Selo de garantia + texto | `Garantia` | claro |
| 14 | Criador + "onde ela já esteve" | `Criador` | painel escuro |
| 15 | FAQ em acordeão | `FAQ` | claro |
| 16 | Fechamento + botão final | `Fechamento` | painel escuro |
| 17 | Rodapé | `Footer` | claro |

O kit acrescenta duas coisas que a referência não tem e que valem a pena: uma
faixa de autoridade logo depois do hero e uma seção de materiais (`Material`).
Se a referência de um novo aluno for outra página, refaça esta tabela com a
estrutura dela e adapte `App.jsx` (React) ou a ordem das seções do HTML, em vez de forçar esta.
