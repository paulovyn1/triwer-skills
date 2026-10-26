# Vídeo narrado por cenas (sem pessoa filmada, ou com pouca)

Para os estilos `documentario-colagem`, `pb-neon`, `mural-de-memorias`, `mesa-e-telas` e `prancheta-tecnica`. O vídeo nasce do
roteiro e da narração. Cada frase vira uma cena do estilo escolhido. O `cenas.json` é a fonte única: o principal escreve as cenas
em texto, e o código de cada cena é montado com os blocos.

## Etapas
| # | Etapa | Saída | Portão |
|---|---|---|---|
| N1 | Roteiro em frases curtas (1 ideia por frase, 6 a 14 palavras), com as provas reais marcadas | `roteiro.md` | aprovar roteiro + estilo |
| N2 | Narração: a voz gravada pelo usuário é a melhor. TTS local só se estiver configurado nos dados do usuário (`ambiente.json → tts_local`) e aprovado de ouvido | `work/narracao.wav` | ouvir 15 s antes do resto |
| N3 | Tempos das palavras: `transcribe_groq.py` + `words_out.py` (ou o JSON do TTS) | `motion/public/words.json` | — |
| N4 | Roteiro de cenas: uma linha por cena, com o tipo de cena do cartão, o protagonista, o texto na tela, a transição de entrada, o material e o efeito sonoro | `cenas.json` | aprovar a lista (texto, barato) |
| N5 | Material real (`references/fontes-reais.md`): cada busca devolve uma folha numerada | `edit/fontes/` + `creditos.json` | o usuário escolhe pelos números, se quiser |
| N6 | Cenas em Remotion: blocos de `src/blocos` + o que for próprio da cena (subagente por lote de cenas do mesmo tipo) | `src/cenas/*.tsx` | prévia de 10 a 16 s do trecho mais difícil |
| N7 | Folha de quadros (2 por cena) + `auditar_movimento.py` | `verify/` | — |
| N8 | Música e mix (`musica-mixagem.md`) e entrega (`entrega.md`) | `entrega/*.mp4` | A/B/C de música, revisão de efeitos |

## `cenas.json` (formato)
```json
{
  "estilo": "mural-de-memorias",
  "fps": 30,
  "cenas": [
    {
      "id": "c01",
      "de": 0.0,
      "ate": 2.1,
      "frase": "Esse sou eu.",
      "tipo": "jornal-com-foto",
      "protagonista": "imagem",
      "texto": { "palavras": ["eu"], "modo": "legenda", "destaque": { "eu": "sublinhado" } },
      "entrada": "chicote",
      "material": ["fontes/foto_atual.jpg"],
      "sfx": [{ "em": "eu", "som": "caneta riscando papel" }],
      "nota": "círculo de caneta na foto no 'eu'"
    }
  ]
}
```
- `de` e `ate` saem do `words.json` (início da primeira palavra e início da próxima cena). Nunca chutar.
- `tipo` sai da tabela "Tipos de cena" do cartão do estilo. Cena fora do vocabulário só com motivo escrito em `nota`.
- Checagens antes de construir:
  - duas cenas seguidas com o mesmo `tipo` só se forem `camera-continua`;
  - a cada 3 ou 4 cenas, uma com `protagonista: "texto"`;
  - o material existe ou tem busca marcada.

## Como economizar aqui
- O principal escreve o `cenas.json` (texto) e não abre código de cena.
- Os subagentes constroem por **tipo de cena** (todas as `polaroid` de uma vez), porque o código se repete e o custo cai.
- Cena nova = composição de blocos. Se um subagente escrever um efeito que serve a outros estilos, ele vira bloco em
  `src/blocos` e entra na próxima versão da skill.
- A prévia é feita só no trecho mais difícil, antes do vídeo inteiro.
- A verificação é por folha de quadros (`verificar.py stills` ou `stills.mjs`) com QA por subagente Sonnet. O principal só abre
  imagem quando o QA aponta algo.
