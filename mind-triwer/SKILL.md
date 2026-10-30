---
name: mind-triwer
description: >
  Gera mapas mentais prontos para importar no MindMeister (arquivo .mind), com
  as cores da marca do próprio expert (ou um cinza neutro), principalmente como material de
  apoio para aula ao vivo, live ou apresentação. Estrutura o conteúdo em blocos,
  argumentos e casos, escreve cada nó no tom do próprio expert, gera o arquivo
  sem precisar de API ou login e, quando o mapa já foi personalizado no
  MindMeister, entrega só o ramo novo para colar. Use quando o aluno pedir
  "mapa mental", "transforma isso em mapa", "material da minha live em mapa",
  "quero ver isso num mapa", mencionar MindMeister ou ".mind", ou quando a skill
  criar-aula-triwer pedir o material de uma aula ao vivo. NÃO usar para slides,
  carrossel ou documento de texto.
compatibility: Claude Code, Claude Desktop (precisa executar Python)
metadata: "v1.1.0, outubro 2026. Histórico em CHANGELOG.md."
---

# Mind Triwer

Gera arquivos `.mind` para o MindMeister. Um `.mind` é um ZIP com um `map.json` dentro. O gerador pronto está em `assets/gen_map.py`: você escreve o conteúdo do mapa num arquivo Python simples, roda o gerador e entrega o arquivo para o aluno arrastar no MindMeister.

Neste arquivo, "o expert" é o aluno que está usando a skill.

Idioma: português brasileiro. Se o expert tiver uma skill de estilo própria (por exemplo `estilo-[nome]`), use-a no texto dos nós.

---

## BOOT, executar sempre ao iniciar

0. **Verificação de versão:** leia o arquivo `VERSION` desta skill, que é a versão local. Tente buscar `https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/mind-triwer/CHANGELOG.md` com a ferramenta de acesso à web do ambiente. Se não conseguir acessar, siga sem dizer nada. Se a entrada mais recente for igual à local, siga. **Só se a remota for mais nova:** leia e siga `references/atualizacao-versao.md`.
1. **Memória:** leia `~/.claude/skills/mind-triwer/memoria.md`, se existir. Ela guarda o tom do expert, as cores do mapa, onde ficam os arquivos, os mapas já gerados e as preferências aprendidas nas correções. Se não existir, rode o onboarding rápido de `references/memoria-modelo.md` (uma mensagem só) e crie o arquivo antes do primeiro mapa. Se a skill `criar-aula-triwer` estiver instalada, leia também `~/.claude/skills/criar-aula-triwer/memoria.md` (aula de referência e pasta de materiais) e não pergunte de novo o que já está lá.
2. **Ambiente:** esta skill precisa executar Python (Claude Code ou Claude Desktop com ferramentas de arquivo). No claude.ai sem execução de código, avise que o arquivo `.mind` não pode ser gerado ali e ofereça entregar o outline em Markdown para o expert montar à mão.

---

## Passo 1. Coletar o conteúdo

Se o mapa vem de uma aula montada pela `criar-aula-triwer`, use o roteiro aprovado. Se não, pergunte o título central, os blocos e os pontos de cada bloco, ou peça o material bruto (transcrição, anotação, outline).

## Passo 2. Estruturar antes de escrever

Este é o passo que decide se o mapa serve. Leia antes:
- `references/metodo-granularidade.md`: forma da árvore (lista paralela x linha de raciocínio, profundidade, tamanho)
- `references/escrita-do-no.md`: tom do texto do nó e o que da fala entra no mapa

Regras que mais quebram mapas:
- Cada passo de raciocínio é um nó filho, nunca empilhado no mesmo nó
- Mínimo de 4 níveis de profundidade; mapas reais de aula chegam a 8 a 10
- Antes de escrever um bloco, liste os 2 a 4 ramos paralelos (ângulos diferentes da mesma tese) e só então desça em cada um
- Nó pai abre o raciocínio, filho entrega o conteúdo. Nunca fechar um nó com frase de efeito
- Nunca colocar interação com o chat como nó
- Nomes próprios e 1ª pessoa do expert preservados

Mostre ao expert a estrutura de ramos (blocos e ramos de cada um) antes de escrever o texto final dos nós, quando o mapa for grande.

## Passo 3. Escrever o conteúdo e gerar o arquivo

1. Copie `assets/gen_map.py` para uma pasta de trabalho.
2. Crie `conteudo.py` na mesma pasta:

```python
def n(title, *kids): return (title, *kids)

MAP = n("Título central",
  n("Abertura",
    n("**Você vai descobrir**",
      n("Primeira promessa da aula"),
      n("Segunda promessa da aula"))),
  n("Contexto importante",
    n("Uma afirmação completa sobre o mercado",
      n("O desdobramento dessa afirmação",
        n("O exemplo ou número que prova")))))
```

3. Rode `python gen_map.py conteudo.py nome-do-mapa.mind` (no Windows, `python -X utf8 ...` evita problema com acentos).
4. Confira o que o gerador imprime: total de nós, tamanho médio dos nós, profundidade, nós com travessão e nós terminando em ponto final. Corrija e gere de novo se precisar.
5. Salve o `.mind` na pasta que o expert indicar e guarde o `conteudo.py` junto: ele é a fonte para qualquer ajuste futuro.

Estilos e tema já estão no gerador. **Cores:** sem configuração, o mapa sai em cinza neutro. Se o expert quer as cores da marca, acrescente no `conteudo.py` a linha `PALETA = {"marca": "1F3A5F", "fundo": "F5F7FA"}` (hex sem `#`, `marca` é a cor das linhas e do texto do nó central, `fundo` é o fundo claro do nó central) e guarde o valor em `memoria.md`. Detalhes técnicos do formato, se precisar mexer: `references/map-template.md` e `references/visual-identity.md` (copiar os blocos literalmente; qualquer alteração quebra a aparência).

## Passo 4. Mapa que o expert já importou e personalizou

Depois que o expert sobe o mapa no MindMeister e personaliza (cores, imagens, prints, ajustes), **nunca gere o mapa inteiro de novo** para incluir algo: reimportar apaga a personalização.

1. Gere um `.mind` separado só com o ramo novo: título central "Ramo novo para copiar", com um único filho que é o nó a ser colado.
2. Diga exatamente onde colar: "importe este arquivo, clique no nó X, copie com Ctrl+C, selecione o nó Y no seu mapa e cole com Ctrl+V".
3. Atualize também o `conteudo.py` completo, para que uma geração futura já inclua o ramo.
4. Nó que vai receber imagem que só o expert tem (print, foto) entra como `[PRINT]`.

Se a sessão tiver uma extensão de navegador conectada (por exemplo Claude in Chrome), dá para tentar editar o mapa direto no MindMeister. Avise o expert antes e pare se a edição não responder em 2 ou 3 tentativas.

## Passo 5. Entrega

- Caminho do arquivo `.mind` e como importar (arrastar no MindMeister ou File → Import)
- Estrutura: número de blocos e de nós
- Slots `[SLOT]` e `[PRINT]` que o expert precisa preencher
- Atualize o `memoria.md` com o tom aprendido e o nome do mapa gerado

## Aprender com as correções do expert

A skill evolui com o jeito de quem a usa. Tudo o que vale para os próximos mapas fica em `memoria.md`:

- **Registrar preferência.** Quando o expert corrigir, recusar ou pedir um ajuste que se aplicaria de novo (tamanho do nó, profundidade, como ele rotula blocos, palavras que ele troca, o que ele nunca quer no mapa), grave uma linha em "Preferências registradas": `[data] Quando [situação], [faça X] (não [Y])`. Avise em uma frase: "Anotei na sua memória: [regra]. Se não quiser que eu lembre disso, é só avisar." Ajuste de um mapa só não vira regra.
- **Aplicar.** Antes de estruturar ou escrever os nós, releia as preferências e o tom do expert e siga. Elas valem mais que os padrões das referências, menos a regra de número real (nunca aproximado nem inventado): se o expert pedir algo que quebre isso, explique e não aplique.
- **Guardar caminhos.** Quando o expert disser onde algo está (pasta dos mapas, mapa de referência), grave em "Fontes e caminhos" e confira ali antes de pedir de novo.
- **Nunca gravar** telefone, e-mail, senha, token, CPF/CNPJ ou dado pessoal de aluno ou cliente. Só caminhos, gostos e regras.
- **Contradição.** Se uma preferência nova contradiz uma antiga, atualize a antiga e avise.
- **Fecho de cada mapa.** Atualize "Mapas gerados", "Pendências" e a data de atualização.

## Arquivos de referência

- `references/memoria-modelo.md`: onboarding rápido e formato do `memoria.md`
- `assets/gen_map.py`: gerador pronto (monta e empacota o `.mind`)
- `references/metodo-granularidade.md`: forma da árvore
- `references/escrita-do-no.md`: tom do nó e o que entra no mapa
- `references/map-template.md` e `references/visual-identity.md`: formato técnico e estilos
- `references/atualizacao-versao.md`: o que fazer quando há versão nova
