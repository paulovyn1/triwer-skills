---
name: criar-aula-triwer
description: >
  Constrói uma aula completa do produto do aluno (curso, mentoria, comunidade,
  aula aberta, live com venda) a partir de material disperso: transcrições de
  aulas antigas, pesquisas, respostas de IA sobre o que ele já ensinou, histórias
  e resultados reais. Reconcilia fontes que se contradizem, valida padrões contra
  casos reais antes de ensinar como regra, estrutura os blocos com exercício e
  pré-requisito, monta aula ao vivo na sequência de 7 movimentos com pitch no
  meio, entrega o roteiro em versões para aprovação e gera o material final
  (mapa mental via mind-triwer para aula ao vivo, ou HTML para aula gravada).
  Use quando o aluno disser "montar uma aula", "estruturar essa aula", "preparar
  minha live", "preciso desenvolver o módulo X", "transformar essa transcrição
  em aula" ou pedir só uma etapa do processo ("só acha os padrões", "só gera o
  material"). NÃO usar para carrossel, stories, página de vendas ou e-mail.
compatibility: Claude Code, claude.ai, Claude Desktop
metadata: "v1.1.0, outubro 2026. Histórico em CHANGELOG.md."
---

# Criar Aula Triwer

Constrói uma aula do produto do aluno do zero, da pesquisa dispersa até o material pronto para gravar ou dar ao vivo. O valor deste processo não está em organizar conteúdo que já existe. Está em **reconciliar fontes que se contradizem** e **validar padrões contra casos reais antes de ensiná-los como regra**.

Neste arquivo, "o expert" é o aluno que está usando a skill: a pessoa que vai dar a aula. "O participante" é quem vai assistir.

Idioma: português brasileiro. Se o expert tiver uma skill de estilo própria (por exemplo `estilo-[nome]`), use-a para todo texto de fala. Nunca use a voz de outra pessoa.

---

## BOOT, executar sempre ao iniciar

0. **Verificação de versão:** leia o arquivo `VERSION` desta skill (sibling do `SKILL.md`), que é a versão local. Tente buscar `https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/criar-aula-triwer/CHANGELOG.md` com a ferramenta de acesso à web do ambiente. Se não conseguir acessar, não mencione nada e siga. Se a entrada mais recente do CHANGELOG remoto for igual à local, siga sem dizer nada. **Só se a remota for mais nova:** leia e siga `references/atualizacao-versao.md`.
1. **Fontes do expert:** tente ler `~/.claude/skills/onboarding-triwer/memoria.md`. Se existir, use as URLs do Notion do expert (bancos de histórias, público, produtos) como fonte de casos. Se não existir, siga sem Notion e peça as fontes na conversa.
2. **Memória:** leia `~/.claude/skills/criar-aula-triwer/memoria.md`, se existir. Ela guarda o produto do expert, onde ficam as aulas dele, as aulas já construídas e as preferências aprendidas nas correções. Se não existir, rode o onboarding rápido de `references/memoria-modelo.md` (uma mensagem só) e crie o arquivo. Confira a memória antes de pedir qualquer fonte ou caminho de novo.

---

## As 7 etapas

Rode em ordem na primeira vez que constrói uma aula. Se o expert pedir só uma etapa, pule direto para ela, mas avise se as etapas anteriores importam (ex.: gerar o material sem ter validado padrão carrega conteúdo não testado).

### 1. Levantar o material disperso

Peça ou receba tudo que já existe sobre o tema: transcrições, pesquisas, respostas de IA sobre aulas já dadas, a página de planejamento no Notion se existir. Trate como matéria-prima bruta, mesmo que venha bem escrita.

**Dossiê gerado por IA (GPT, NotebookLM) não é fonte de caso.** Esses dossiês misturam casos diferentes sob o mesmo número, trocam a origem de um resultado, atribuem a um aluno a história do próprio expert e afirmam como documentado o que outro dossiê diz que não existe. Todo caso, número ou nome que vier de dossiê precisa ser conferido no banco de histórias do expert (Notion) ou confirmado com ele antes de entrar na aula. O que não bater fica de fora ou vira pergunta.

**A descrição do expert vence o dossiê.** Quando ele contar como faz hoje no próprio negócio, essa descrição vira a espinha da aula, mesmo que reorganize o que já estava estruturado.

Se a aula for ao vivo, siga as perguntas iniciais da seção "Ordem de trabalho" de `references/aula-ao-vivo.md` antes de escrever qualquer bloco.

Se existir página de planejamento no Notion, leia primeiro (ver `references/notion-planejamento.md`).

### 2. Achar consenso real, marcar contradição, marcar buraco

- **O que se repete com o mesmo mecanismo** (não só a mesma palavra)? Termos parecidos para coisas diferentes não são consenso.
- **Onde as fontes se contradizem de fato?** Não decida sozinho qual está certa. Muitas vezes a resposta é "as duas, em camadas diferentes".
- **O que aparece em uma fonte só?** Não descarte nem invente: pergunte se ainda faz parte do método atual.

Leve as descobertas ao expert como perguntas objetivas com opções (`AskUserQuestion` ou equivalente), uma para cada contradição e cada buraco.

### 3. Validar padrão contra casos reais

Quando surgir uma hipótese de padrão, não escreva na aula até testá-la contra um caso real e nomeado: propor a hipótese, testar contra um caso específico, deixar o expert contestar, perguntar o mecanismo exato da contestação e reescrever a hipótese para absorver a exceção.

**Amostra pequena é hipótese, não modelo.** Com 2 ou 3 casos, diga isso ao expert e pergunte se há mais exemplos antes de ensinar como regra. Detalhes e exemplo de execução em `references/validar-padroes.md`.

Se um bloco não tem caso real suficiente, pergunte: resolver agora (mais exemplos) ou registrar como lacuna e seguir?

### 4. Estruturar a aula

- **Pré-requisito explícito no início:** o que o participante precisa ter antes desta aula.
- **Um conceito que amarra todos os blocos**, nomeado logo no início.
- **Blocos com exercício embutido**, ensina e aplica antes de passar para o próximo.
- **Teste ou checklist prático** que o participante usa sozinho depois.
- **Aula ao vivo com pitch:** sequência de 7 movimentos de `references/aula-ao-vivo.md` (promessa com história, contexto de mercado, por que acontece, como eu faço, passo a passo com porquê, pitch, continua o conteúdo). A ordem de trabalho completa está no mesmo arquivo.
- **Fechamento que aponta para a próxima aula**, usando o travamento no exercício como diagnóstico (ver `references/estruturar-aula.md`).

### 5. Registrar o planejamento no Notion (se o expert usa Notion)

A página de planejamento da aula é o registro de **processo**, não o material final: conteúdo completo por bloco, pendências, contradições resolvidas com o porquê, dados brutos ainda não processados. Ver `references/notion-planejamento.md`.

### 6. Registrar o que foi aprendido

Separe em dois tipos e não misture:
- **Conteúdo do método** (um padrão novo, um teste novo): vai para o acervo do expert. Se ele usa o Workspace de Aluno no Notion, use a skill `notion-zettelkasten-si`.
- **Como a aula foi construída** (que pergunta destravou, que erro apareceu): nota separada, sobre processo.

Histórias e resultados novos que aparecerem na conversa vão para o banco de histórias do expert (skill `historias-triwer`, se instalada).

### 7. Gerar o material final

Só depois das etapas 5 e 6.

**Aula ao vivo:** o material de apoio é um mapa mental do MindMeister, gerado pela skill `mind-triwer`. Antes, entregue o roteiro de fala em Markdown para o expert aprovar. As regras do que entra no mapa estão em `references/aula-ao-vivo.md`.

**Aula gravada ou material do participante em HTML:**
- Segue a identidade visual do produto do expert (ver `references/padrao-visual.md`)
- **Nunca** carrega pendência, contradição resolvida, dado bruto ou registro do processo
- Salva na pasta que o expert indicar
- Abre no navegador para conferência antes de entregar

## Aprender com as correções do expert

A skill evolui com o jeito de quem a usa. Tudo o que vale para as próximas aulas fica em `memoria.md`:

- **Registrar preferência.** Quando o expert corrigir, recusar ou pedir um ajuste que se aplicaria de novo (como ele abre uma aula, tamanho dos blocos, tipo de exercício, o que ele nunca fala, como ele nomeia as coisas), grave uma linha em "Preferências registradas": `[data] Quando [situação], [faça X] (não [Y])`. Avise em uma frase: "Anotei na sua memória: [regra]. Se não quiser que eu lembre disso, é só avisar." Ajuste de uma aula só não vira regra.
- **Aplicar.** Antes de estruturar ou escrever qualquer bloco, releia as preferências e siga. Elas valem mais que os padrões deste arquivo e das referências, menos a regra de não inventar caso, número ou nome: se o expert pedir algo que quebre isso, explique e não aplique.
- **Guardar caminhos.** Quando o expert disser onde algo está (pasta das aulas, database do Notion, aula de referência), grave em "Fontes e caminhos" e confira ali antes de pedir de novo.
- **Nunca gravar** telefone, e-mail, senha, token, CPF/CNPJ ou dado pessoal de aluno ou cliente. Só caminhos, gostos e regras.
- **Contradição.** Se uma preferência nova contradiz uma antiga, atualize a antiga e avise.
- **Fecho de cada aula.** Atualize "Aulas construídas", "Pendências" e a data de atualização.

## Arquivos de referência

- `references/memoria-modelo.md`: onboarding rápido e formato do `memoria.md`
- `references/aula-ao-vivo.md`: ordem de trabalho, sequência de 7 movimentos, ponte para o pitch, histórias, estratégias prontas (opcional), escrita e o que entra no mapa
- `references/validar-padroes.md`: o ciclo de testar hipótese contra caso real, com exemplo
- `references/estruturar-aula.md`: anatomia dos blocos e travamento como diagnóstico
- `references/notion-planejamento.md`: como registrar o planejamento da aula no Notion
- `references/padrao-visual.md`: identidade visual do material HTML e bugs conhecidos
- `references/atualizacao-versao.md`: o que fazer quando há versão nova
