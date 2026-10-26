# Música por emoção, efeitos sonoros e mixagem

A trilha acompanha a EMOÇÃO de cada trecho da fala: pode ser 1 faixa ou várias, trocando quando a emoção muda. Cada vídeo usa músicas
diferentes (o mesmo cliente não ouve a mesma faixa duas vezes). Tudo em Python: o Claude só escreve o mapa emocional e revisa números.

## 1. Mapa emocional (no portão 1, junto com a estratégia)
`projeto.json → musica.trechos`, em ordem; `de` em segundos de saída ou "palavra@quadro" (formato do words_out):
```json
"trechos": [
  {"de": 0,        "emocao": "tensao",    "intensidade": 2, "nota": "gancho: MBA caro"},
  {"de": "Eu@747", "emocao": "esperanca", "intensidade": 2, "nota": "virada: o caso do Daniel"},
  {"de": "O@1064", "emocao": "motivacao", "intensidade": 3, "nota": "método e CTA"}
]
```
Emoções (`scripts/emocoes.py`): tensao, misterio, dor, reflexao, confianca, esperanca, motivacao, triunfo, urgencia, leveza, neutro.
Intensidade 1 calma, 2 média, 3 forte. `entrada` opcional por trecho: `dj` (transição de DJ casando andamento), `respiro` (troca de clima
sem casar andamento), `corte` (virada brusca com impacto: usar pouco). Sem `entrada`, o script decide (dj quando andamento ±7% e tom casam).
Trecho < 5 s é fundido ao vizinho (troca rápida demais soa como erro). Mudar de faixa só quando a emoção muda de verdade: 1-3 faixas num
anúncio de 60 s é o normal; mais que isso só em vídeo longo.

## 2. Escolher e mixar (zero token)
```
python escolher_musica.py            # 3 versões (A/B/C) com faixas diferentes entre si -> projeto.json musica.versoes + baixa as faixas
python mix.py A && python mix.py B && python mix.py C     # ≈ 30 s cada; imprime faixas, trocas, ganhos, LUFS
python medir_mix.py A                # efeitos mais altos vs voz, música vs voz
```
- Biblioteca: `biblioteca/musica/indice.json` (todas as faixas do Mixkit com tags de humor/gênero/instrumento) + `analise.json` (BPM, tom
  Camelot, curva de energia a cada 5 s, pulso, brilho). Atualizar de tempos em tempos, do clone do repo: `indexar_musicas.py` e
  `indexar_musicas.py --analisar` (segundo plano). Licença Mixkit: anúncio online ok, sem crédito; não CD/DVD/jogo/TV/rádio.
- Pontuação por trecho: emoção (tags + modo maior/menor + andamento) × 1,6, energia da intensidade numa janela da faixa × 0,8, e
  penalidade forte para faixa já entregue ao mesmo cliente (`~/.claude/edicao-motion-triwer/musicas_usadas.json`, gravado pelo entregar.py).
- O usuário escolhe de ouvido entre A/B/C (portão 4). Ajuste fino: editar `musica.versoes.X.faixas` (trocar id, mudar `entrada`,
  `ganho_db`, `offset_sugerido` em s da faixa) e rodar `mix.py X` de novo.

## 3. O que o mix.py faz em cada troca
- **Início**: cada faixa começa num tempo forte (fase do compasso pelo grave), no trecho dela com a energia da intensidade pedida e sem
  buraco no começo.
- **dj**: a anterior abafa (passa-baixa 19 kHz → 650 Hz em `de − 0,75 → de − 0,2`) e baixa (−3 → −9 dB); a nova entra em `de` sem grave
  (passa-alta 260 Hz) e sobe; no primeiro tempo forte da anterior entre `de + 1,3` e `de + 3,6` acontece a troca de grave (a nova ganha o
  grave, a anterior some em 0,45 s). A nova é esticada (rubberband, sem mudar o tom) para o andamento da anterior se a diferença for ≤ 8%;
  acima disso a entrada vira `respiro`. Riser discreto (−23 dB) termina na troca.
- **respiro**: a anterior abafa e baixa em 1,2 s; a nova já soa baixinho 0,35 s antes do `de` e sobe em 0,85 s (sem vão).
- **corte**: troca seca no `de` + impacto grave (−17 dB) no barramento da música.
- **Sem vão**: depois de montar as faixas, um preenchimento suave (2 passadas, 250 ms) segura a trilha a no máximo ~5,5 dB abaixo da mediana
  de antes de cada troca. O `mix.py` reporta `vao_db` por troca (trilha antes do ducking) e avisa acima de 8 dB. Referência: a troca
  aprovada do C2 mede ≈ 5 dB; as trocas por emoção no teste do C3 ficaram entre 3 e 7 dB.
- Fim: fade nos últimos 0,6 s. Nível: cada faixa normalizada no trecho em que é protagonista para `lufs_musica` (−23) ± 1,5 dB por ponto
  de intensidade; ducking ≤ 6 dB pela voz e pelos efeitos. Envelopes sempre em ordem de tempo (até a 0.2 havia tempos do C2 fixos no código).
- Formato antigo (`musica.pares` + `marcos`) continua funcionando (vira 2 faixas com entrada dj).

## 4. Efeitos sonoros: escolha pelo que se vê, no acervo inteiro
- `audio/sfx.json` sai do `montar_sfx.py`: junta o que cada subagente de painel pediu (`src/panels/PXX.sfx.json`), a entrada de cada painel,
  a legenda (slam, texto atrás, fantasma, knock) e os golpes de zoom. O Claude só revisa (e corta o excesso).
- `file` = nome do catálogo (`biblioteca/sfx/CATALOGO.md`, os já aprovados) ou `mixkit:<id>` (qualquer um dos ~2.700 do índice; baixado
  na hora). Achar: `python sfx.py buscar "porta de vidro fechando"` (aceita português). Som bom que vai se repetir: `sfx.py catalogar`.
- Regra de ouro (aprendida nos testes): som LITERAL do que aparece (tampa de lixeira, impressora, carimbo) e só com gatilho visível; poucos
  (≈ 0,9/s; camadas no mesmo quadro contam 1; `rajada_ok` nas camadas desenhadas do knock); nada para moeda, barra, palavra que acende.
- Envelope em tudo (o mix.py faz): pico no quadro, fade de 3 ms, cauda em `max` com fade, passa-alta `hp`, `pan` fixo ou varredura,
  `pitch` crescente em sequência, −3 dB em 2,8 kHz no barramento. Ganhos: impacto −6 a −9; pop/click −13 a −17; whoosh −10 a −15.

## 5. Revisão pelo usuário (ele não precisa saber o nome de nenhum som)
O `entregar.py` gera, junto com o vídeo, `entrega/revisao/<vídeo> - efeitos numerados.mp4` (cada efeito com "#12 · tampa bate" na tela) e
`edit/revisao/efeitos.html` (quadro, nota, som atual e 3 alternativas a/b/c para ouvir). Ele responde "#12 b", "#20 tirar", "#33 mais
baixo", "#7 mais cedo". Aplicar: `sfx.py trocar 12 b` / `remover 20` / `ganho 33 -3` / `mover 7 -4`, depois `mix.py X` e
`entregar.py X "<nome>"` (só remux, sem render). Catálogo para ouvir tudo: `revisar_sfx.py --catalogo` → `biblioteca/sfx/catalogo.html`.

## 6. Master e medição
loudnorm 2 passadas em −14 LUFS / −1 dBTP. `medir_mix.py`: nenhum efeito pontual acima da voz (exceto clímax ≈ 0 dB), música 15-20 dB
abaixo da voz. O Claude não ouve: relatar números e pedir teste de ouvido no celular.
