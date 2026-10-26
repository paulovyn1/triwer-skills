# Painéis de motion graphics: quem faz, como reaproveitar, como verificar

Etapa 4, a mais cara. Medido no C3 Opus (tudo no principal): 42% do custo, e depois dela cada mensagem relia 320-330 mil tokens porque
o código dos painéis e as folhas de contato ficavam na conversa. Regra desde a 0.3.0: **o código de painel nunca entra no contexto principal**.

## Quem faz o quê
| Trabalho | Quem | Por quê |
|---|---|---|
| Decidir painéis, batidas e textos (portão 2) | principal (Opus) | criativo; é texto curto |
| Painel inédito ou adaptação que muda a animação | **subagente Opus**, 1 por painel (2 se forem simples), em paralelo, em segundo plano | qualidade de motion é Opus; o TSX fica no contexto dele |
| Adaptar painel do kit só trocando texto e tempo (`warp`) | **subagente Sonnet** | mecânico; o brief diz exatamente o que trocar |
| QA das folhas de contato do vídeo inteiro | **subagente Sonnet** | checklist objetivo; o principal não lê imagem |
| Efeitos sonoros dos painéis | o próprio subagente do painel (`PXX.sfx.json`) | quem desenhou sabe o que bate; busca no acervo todo |

## Fluxo (4 chamadas no principal)
1. `python montar_motion.py --kit <kit> --paineis P10,P13 --novos P14,P15,P16:overlay` (copia os do kit, cria stub dos inéditos).
   Escrever `timeline.ts` com TODOS os painéis (já compila com os stubs).
2. Para cada painel, gravar `edit/briefs/PXX.md` a partir de `template/brief_painel_item.md` (15-30 linhas: tipo, janela, fala com
   palavra@quadro local, batidas, textos exatos, compliance, ponto de partida no kit).
3. Disparar os subagentes **numa mensagem só**, em segundo plano (`run_in_background`), cada um com o prompt:
   `Leia <skill>/template/BRIEF_PAINEL.md e siga para o painel PXX: brief em <edit>/briefs/PXX.md. Projeto em <edit>/motion. Skill em <skill>.`
   - inédito/animação: `Agent(model="opus")`; adaptação só de texto/tempo: `Agent(model="sonnet")`.
   - Esperar as notificações (não fazer polling). Cada um devolve ≤ 8 linhas: pousos, sons, caminho da folha, pendência.
4. `python montar_sfx.py` (junta os `PXX.sfx.json` + entradas de painel + legenda + golpes) e `python verificar.py stills`; passar as
   folhas a um subagente Sonnet de QA com o checklist abaixo e ler só a lista de defeitos. Defeito em painel → mandar mensagem ao
   subagente daquele painel (SendMessage) com a correção; ele ainda tem o contexto.

Checklist do QA (prompt do subagente Sonnet): "Leia <edit>/verify/sheet_*.png. Para cada quadro, liste só defeitos objetivos: texto cortado
na borda, sobreposição de texto com texto, legenda em cima de painel ou do botão de CTA, elemento fora da área segura (y < 70 ou > 880 no
painel de cima; 380 px de baixo e 140 px da direita na tela cheia), fonte que parece outra (serifada genérica, Arial), estado final vazio,
rótulos encavalados. Responda 'quadro mNNNN: defeito' ou 'nenhum defeito'. Não comente estética."

## Reaproveitar painel do kit com outra fala
- **Painel com `useAt`** (C3 opus em diante): troque as palavras-gatilho (`at("fora")` → `at("perdido")`) e os textos. Pronto.
- **Painel do C2 (tempos fixos)**: copie, troque os textos e ponha `const frame = warp(useCurrentFrame(), MAP);` (`src/warp.ts`).
  MAP = [[quadro_novo, quadro_original], ...] ligando a palavra nova à palavra original que dispara a mesma animação: os quadros originais
  estão em `<kit>/paineis-c2/POUSOS.md` (palavra@quadro local + constantes do topo do arquivo). 3-5 pontos bastam. Ex. (P10 no C3):
  `[[0,0],[44,20],[64,40],[108,99],[122,113],[140,127]]`.
- Painel novo que for para o kit: tempos SEMPRE por `useAt` (ou um bloco BEATS no topo) e rótulos com limite de largura anotado.

## Planejar (portão 2)
Para cada frase que merece ilustração: o que aparece, quando pousa (palavra), tipo. Frase de ligação fica só com a pessoa + legenda.
≈ 60% `top`, 1-2 `cover`, 1 `overlay` de CTA. Nunca dois painéis iguais em estrutura seguidos; respiro de 1-3 s só com a pessoa entre
grupos. Provas reais (fotos, logos, dados): só o que o cliente tem e o kit autoriza.

## Tipos e geometria
- `top` 1080×960; `cover` 1080×1920 (conteúdo y 230-1450, x 70-960); `overlay` 1080×1920 transparente.
- Container (`layers/Panels.tsx`): entra deslizando em 9 quadros, sai em 7; `cover` faz fade 6 + escala 1,06→1.

## Verificação que vale para todos
`auditar_movimento.py` (dentro do `verificar.py final`): ≤ 3% de quadros parados, maior trecho parado ≤ 3, sem salto seco. Estado final
visível ≥ 14 quadros antes do `to` (o `verificar.py stills` inclui o quadro `to-8` para pegar isso).
