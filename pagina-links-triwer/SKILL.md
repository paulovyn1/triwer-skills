---
name: pagina-links-triwer
description: >
  Monta a página de links da bio do aluno (link na bio, estilo Linktree, mas com
  a identidade e as animações de uma página de verdade): levanta todos os links
  que ele tem, pergunta a prioridade de cada um, organiza em seções (um destaque
  grande, cards médios, material gratuito e ícones de redes), escreve os textos
  curtos dos cards a partir do material real, monta em HTML único ou React
  conforme o nível do aluno, publica e entrega o pacote. Use quando o aluno pedir
  "página de links", "link da bio", "link na bio", "linktree", "página pra colocar
  no Instagram com meus links", "juntar meus links numa página", "trocar meu
  linktree por uma página minha" ou quiser reorganizar a página de links por causa
  de um lançamento novo. NÃO usar para página de vendas (pagina-paquera-triwer ou
  pagina-vendas-lancamento-pago), página de captura com formulário ou site
  institucional com várias páginas.
compatibility: Claude Code, claude.ai, Claude Desktop
metadata: "v1.1.0, outubro 2026. Histórico em CHANGELOG.md."
---

# Página de Links Triwer

A página de links é a porta entre o perfil e tudo que o expert vende ou entrega.
A pessoa chega vinda da bio, com pouca paciência, quase sempre no celular. A
página tem um trabalho só: levar essa pessoa ao link que mais importa **agora**.
Por isso ela tem hierarquia. Um item é o grande, poucos são médios, as redes
viram ícones. Página de links com dez botões iguais não aponta para lugar nenhum.

Você conduz o processo em fases. Cada fase termina com algo que o aluno vê e
aprova antes da próxima. A ordem dos links é aprovada antes de qualquer texto, e
os textos antes de qualquer design, porque mudar prioridade depois do layout
pronto obriga a refazer as seções.

Idioma: português brasileiro. Os textos saem na voz do expert. Se ele tiver uma
skill de estilo própria (por exemplo `estilo-[nome]`), use-a. Nunca use a voz de
outra pessoa.

---

## BOOT, executar sempre ao iniciar

0. **Verificação de versão:** leia o arquivo `VERSION` desta skill (sibling do `SKILL.md`), que é a versão local. Tente buscar `https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/pagina-links-triwer/CHANGELOG.md` com a ferramenta de acesso à web do ambiente. Se não conseguir acessar, não mencione nada e siga. Se a entrada mais recente do CHANGELOG remoto for igual à local, siga sem dizer nada. **Só se a remota for mais nova:** leia e siga `references/atualizacao-versao.md`.
1. **Memória:** leia `~/.claude/skills/pagina-links-triwer/memoria.md`, se existir. Ela guarda o perfil do aluno, onde estão os arquivos dele, as páginas já entregues e as preferências aprendidas nas correções. Se não existir, rode o onboarding rápido de `references/memoria-modelo.md` (uma mensagem só) e crie o arquivo.
2. **Notion do aluno (opcional):** leia `~/.claude/skills/onboarding-triwer/memoria.md`, se existir com `onboarding_completo: true`. Dali saem nome, Instagram, pasta de fotos e as URLs do Notion. Não pergunte de novo o que já está lá. Sem o onboarding, siga sem Notion.

---

## Fase 0. Ambiente, nível e onde vai ficar

Confira a memória primeiro e só pergunte o que não estiver lá. Descubra antes de tudo:

1. **Ambiente.** Com ferramentas de arquivo e terminal (Claude Code), dá para
   criar o projeto, publicar e tirar prints. No chat (claude.ai), a entrega é um
   arquivo HTML para baixar.
2. **Nível técnico do aluno.** Pergunte de forma simples se ele já mexeu com
   código ou hospedagem, ou se prefere um arquivo que abre com dois cliques.
3. **Onde a página vai morar.** Vercel, a hospedagem do site dele, ou ainda não
   sabe. Isso muda o pacote final.

Proponha o formato explicando o porquê em uma frase. A tabela de decisão está em
`references/formatos.md`. Depois da escolha, nas fases 5 e 6, leia **só** o
arquivo do modo: `references/modo-html.md` ou `references/modo-react.md`.
Instrução de um formato aplicada no outro quebra a página.

Se o aluno já tem uma página de vendas feita com a gente (por exemplo pela
`pagina-paquera-triwer`), reaproveite tokens, fontes, fotos e componentes dela.
A pessoa que clica no destaque cai na página de vendas, e as duas precisam
parecer da mesma marca.

---

## Fase 1. Inventário de links

Junte **todos** os destinos possíveis antes de decidir qualquer ordem. Siga
`references/coleta-links.md`: de onde puxar (Notion do aluno, bio atual, site,
o que ele disser), as categorias para não esquecer nada e como conferir cada
link.

Para cada link, anote: o que é, para quem é, URL (ou "pendente") e se é pago,
gratuito, contato ou conteúdo.

**Leia o destino antes de descrever.** Abra cada link e entenda o que a pessoa
encontra lá. O texto do card e qualquer animação que represente o material
(etapas, pilares, capítulos) precisam bater com o que existe de verdade. Se a
página do destino não abrir ou não mostrar o conteúdo, pergunte ao aluno em vez
de supor.

Feche a fase com a lista completa e o que está pendente.

---

## Fase 2. Prioridade

Esta é a decisão mais importante da página. Siga `references/prioridade.md`, que
tem as perguntas, o modelo de posições e como resolver empates.

Em resumo, a página tem quatro posições:
- **Destaque** (um só): o que o expert mais quer que cliquem agora.
- **Cards médios** (2 ou 3): os próximos em importância.
- **Gratuito** (um, se houver): a isca, para quem ainda não vai comprar.
- **Redes** (ícones): para onde a pessoa vai seguir o expert.

Pergunte ao aluno, não decida por ele. Mostre a proposta como lista, na ordem em
que vai aparecer na tela, e só siga quando ele aprovar. Link que não entra fica
anotado como "fora desta versão", com o motivo.

---

## Fase 3. Textos dos cards

Escreva o mínimo que faz a pessoa clicar, seguindo `references/textos.md`:
título, uma frase de ganho e um botão com verbo. A frase do topo (hero) sai da
visão do expert, não de uma frase de efeito genérica.

Todo fato vem do material real (Notion, destino do link, produto). Número sem
fonte não entra. O que falta fica entre [colchetes].

Entregue os textos junto com o mapa de posições e espere a aprovação.

---

## Fase 4. Identidade e imagens

A página veste a identidade **do expert**. Siga
`references/identidade-visual.md`: cores e fontes tiradas dos materiais dele
(com licença comercial), uma foto forte para o topo, uma imagem por card e o
elemento gráfico da marca no fundo do destaque.

Confira as fotos contra as regras do aluno (crachá, logo de empresa, tela com
dado sensível).

---

## Fase 5. Montagem

Leia `references/layout-secoes.md` (o desenho e as animações de cada seção,
iguais nos dois modos) e depois o arquivo do modo escolhido. Os dois modos partem
de um modelo pronto em `assets/`. Nunca edite o modelo original da skill: copie
para a pasta do aluno.

Os textos aprovados entram como estão.

---

## Fase 6. Revisão, publicação e entrega

**Confira antes de mostrar**, no celular (360px e 412px) e no desktop, com
`references/checklist-qualidade.md`.

**Publique** se o aluno quiser um link para aprovar ou divulgar. Siga
`references/publicacao.md`. O ponto que mais trava: para publicar na Vercel não
é preciso instalar nada na máquina, porque a Vercel instala e compila na nuvem.
Não rode `npm install` local só para publicar.

**Entregue** o pacote do modo (`scripts/empacotar.py`) com um LEIA-ME a partir
de `assets/LEIA-ME-modelo.md`, o link publicado e a lista do que ainda falta
(links pendentes, imagens provisórias).

Ajustes depois da entrega: leia o estado atual, mude só o que foi pedido,
confira, publique de novo no mesmo endereço.

---

## Aprender com as correções do aluno

A skill evolui com o gosto de quem a usa. Tudo o que vale para as próximas páginas fica em `memoria.md`:

- **Registrar preferência.** Quando o aluno corrigir, recusar ou pedir um ajuste que se aplicaria de novo (ordem dos cards, tom do texto, cor, animação, o que ele nunca quer ver), grave uma linha em "Preferências registradas": `[data] Quando [situação], [faça X] (não [Y])`. Avise em uma frase: "Anotei na sua memória: [regra]. Se não quiser que eu lembre disso, é só avisar." Ajuste de uma página só ("troca essa foto") não vira regra.
- **Aplicar.** Antes de escrever ou montar qualquer coisa, releia as preferências e siga. Elas valem mais que os padrões deste arquivo, menos as "Regras que valem o processo inteiro": se o aluno pedir algo que quebre uma delas (inventar número, por exemplo), explique e não aplique.
- **Guardar caminhos.** Quando o aluno disser onde algo está (pasta de fotos, página de vendas de referência, link publicado), grave em "Fontes e caminhos" ou "Entregas feitas" e confira ali antes de pedir de novo.
- **Nunca gravar** telefone, e-mail, senha, token, CPF/CNPJ ou dado de cliente. Só caminhos, gostos e regras.
- **Contradição.** Se uma preferência nova contradiz uma antiga, atualize a antiga e avise.
- **Fecho de cada entrega.** Atualize "Entregas feitas", "Pendências" e a data de atualização.

---

## Regras que valem o processo inteiro

- **Nunca inventar número, resultado, depoimento ou conteúdo de material.** Se
  o card diz que o material avalia quatro coisas, são as quatro que ele avalia
  de verdade.
- **Um destaque só.** Dois destaques viram nenhum.
- **Link que não existe fica "#" e listado como pendente.** O botão aparece, mas
  não leva a lugar nenhum. Nunca chute uma URL ou um perfil.
- **Telefone pessoal só com o OK do aluno.** WhatsApp na página é público.
- **Motivação privada do expert não entra na página.** Medos, dores pessoais ou
  o motivo de ele querer vender são contexto para você, não texto de card.
- **Sem travessão** (— ou –) em nenhum texto produzido. Use vírgula, dois pontos
  ou ponto.
- **Uma versão nova nunca apaga a anterior.**
