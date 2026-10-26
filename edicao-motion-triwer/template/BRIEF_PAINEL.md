# Instruções do subagente de painel (Opus)

Você é um subagente que constrói UM ou DOIS painéis de motion graphics de um vídeo vertical. O Claude principal já decidiu o roteiro;
sua tarefa está no arquivo de brief que ele indicou (`<edit>/briefs/PXX.md`). Leia, nesta ordem e só isto:
1. o brief do seu painel; 2. `<edit>/motion/src/theme.tsx` (cores `C`, fontes `F`, `PanelBg`, `Tape`, `prog`, `pop`, `bob`, `Float`);
3. `<edit>/motion/src/words.ts` (como usar `useAt`); 4. o arquivo de partida que o brief citar (painel do kit para adaptar), se houver;
5. `<kit>/marca.md` só se o brief pedir algo fora do tema.
Não abra outros painéis, o timeline.ts nem as referências da skill. Não faça perguntas: na dúvida, escolha a interpretação mais óbvia.

## Projeto
- Remotion 4, React 19, TypeScript. Pasta `<edit>/motion`. Seu arquivo: `src/panels/PXX.tsx`, que hoje é um STUB. Substitua o arquivo
  inteiro e exporte `export const PXX: React.FC = () => ...` (sem props). Não edite theme.tsx, Root.tsx, timeline.ts, Main.tsx nem outros painéis.
  Helper que precisar: declare no seu arquivo.
- O painel já está registrado como composição própria (id PXX, duração e tamanho certos): dá para renderizar ele sozinho.
- Imagens: `import { Img, staticFile } from "remotion"` + `staticFile("img/arquivo.webp")`. Aleatório só com `random("seed-PXX-...")`.
  Toda animação vem de `useCurrentFrame()`. Nada de CSS transition/animation nem biblioteca nova. SVG inline para ilustração.

## Tempo: sempre pela palavra falada
`const at = useAt();` e `at("palavra")` = quadro LOCAL em que a palavra é falada (`at("como", 1)` = 2ª ocorrência no vídeo inteiro;
o brief diz qual). Nunca número mágico solto para pouso de fala. Pouso = começar a animação 4-6 quadros antes da palavra.
O container entra deslizando em 9 quadros e sai nos 7 últimos: animações internas a partir do quadro ~4, e **o último elemento importante
(carimbo, faixa, selo) pousa pelo menos 14 quadros antes do fim** (senão ele some com a saída).

## Tipos
- **top** 1080x960: metade de cima; a pessoa continua embaixo. Conteúdo importante entre y 70-880, x 60-1020. Fundo `<PanelBg>`.
- **cover** 1080x1920: tela cheia. Conteúdo entre y 230-1450, x 70-960 (a interface do Reels cobre baixo/direita).
- **overlay** 1080x1920 transparente, por cima do vídeo (sem PanelBg).

## Qualidade cobrada (medida depois por script)
- **Nada parado**: envolva o conteúdo em `<Float>`; tudo que fica na tela respira (`bob`, brilho que percorre, drift 1-3%).
  O auditor reprova painel com > 3% de quadros parados ou trecho parado > 3 quadros.
- **Sem salto seco**: número rola (dígito sobe), cor interpola (`interpolateColors`), nunca `cond ? a : b` em cor/posição.
- Movimento nunca linear: `pop` (mola) para entradas, `prog` (ease-out) para revelações, `easeInOut` para traço que se desenha.
  Uma coisa nova por vez (escalonar 4-6 quadros). Carimbo/impacto: escala 1,6→1 com mola + tremida de 3-4 quadros.
- Identidade do cliente (tema): ≤ 2 cores de destaque por painel, 1 `Tape` no máximo, 1-2 palavras em `F.serif` itálico,
  texto ≥ 30 px, ~35-40% de espaço vazio. Português do Brasil com acento. Sem emoji. Compliance do brief (marcas/nomes proibidos) vale.
- Rótulos: meça a largura (≈ 0,6 × tamanho × letras); rótulo que pode encostar no vizinho → encurte ou quebre a linha. `Tape` dentro de
  cartão: `whiteSpace: "nowrap"` e tamanho que caiba.

## Efeito sonoro do seu painel (você escolhe, pelo que se vê)
Escreva `src/panels/PXX.sfx.json`:
```json
{"eventos": [
  {"palavra": "fora", "nth": 0, "off": 1, "file": "mixkit:2364", "gain": -8, "note": "tampa da lixeira bate"},
  {"local": 36, "file": "type_hit", "gain": -7, "max": 0.5, "note": "carimbo RECUSADO"}
]}
```
- Só eventos com gatilho visível e marcante no SEU painel (carimbo, tampa, porta, check, número que pousa, impressora). A entrada do painel
  (swoosh) já é automática: não repita. Nada para elemento secundário (moeda, barra, palavra que acende). 1-4 eventos por painel.
- Procure o som que combina LITERALMENTE com o que aparece: `python <skill>/scripts/sfx.py buscar "tampa de lixeira batendo"` (busca o
  catálogo e ~2.700 efeitos do Mixkit; aceita português). Use o nome do catálogo ou `mixkit:<id>`.
- Ganhos típicos: impacto −6 a −9; pop/click −13 a −17; whoosh −10 a −15. `pitch` crescente em sequência (+0, +2, +4).

## Verificação (obrigatória, barata)
1. `npx tsc --noEmit` (de dentro de `motion/`): corrija erros do SEU arquivo.
2. Stills do seu painel sozinho, 3 quadros (entrada ~12, meio, fim − 10) num bundle só:
   `node stills.mjs ../verify/PXX 0.5 --comp PXX 12 70 150` e uma folha:
   `python <skill>/scripts/contact.py ../verify/PXX/folha.png 3 360 ../verify/PXX/PXX_f0012.png ...`
   Leia SÓ a folha (1 imagem). Corrija texto cortado, sobreposição, fonte errada (fallback silencioso), contraste, elemento fora da área.
   Máximo 2 rodadas de folha.

## Resposta final (curta: o principal só lê isto)
No máximo 8 linhas por painel: o que ficou (1 linha), os pousos (palavra → o que acontece), quantos eventos de som e quais, o caminho
da folha e qualquer pendência real. Não cole código.
