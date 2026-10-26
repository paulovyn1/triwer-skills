---
name: edicao-motion-triwer
description: Edita vídeo vertical (Reels, anúncio, VSL curta, vídeo narrado) com nível de produção alto e baixo gasto de tokens. Catálogo de estilos de edição com nome fácil (Fala Dinâmica, Recorte de Jornal, Documentário Colagem, P&B Neon, Mural de Memórias, Mesa e Telas, Prancheta Técnica) e como catalogar um estilo novo a partir de um vídeo de referência; texto que compõe a cena no tempo da fala; transições sem corte (câmera contínua, corte por forma, chicote, puxar foco); material real (trecho do YouTube, banco gratuito com cara orgânica, prints de portais brasileiros, comentários); cortes de silêncio e gagueira; voz tratada; legenda animada; painéis de motion; trilha pela emoção; efeitos sonoros com revisão numerada; master −14 LUFS. Aprende as preferências de cada usuário com os pedidos de ajuste (arquivo fora da skill). Acionar quando pedirem para editar, cortar, legendar, animar, dar motion, mixar, montar vídeo narrado, escolher ou catalogar estilo de edição.
compatibility: Claude Code (terminal; precisa de ffmpeg, Node 20+ e Python 3.12 com uv)
metadata: "v0.4.0 — outubro 2026. Versão para alunos. Histórico em CHANGELOG.md."
---

# Edição de vídeo vertical com motion

Esta skill é o **processo genérico**. Três coisas ficam fora dela, para ela poder ser compartilhada:
- a **identidade de cada cliente ou marca**, no kit do cliente (uma skill `edicao-<cliente>`; criar com `references/novo-cliente.md`);
- o **gosto do usuário**, na pasta de dados dele (`scripts/preferencias.py onde`);
- os **estilos próprios** dele, também na pasta de dados.

## Requisitos (conferir com o usuário no primeiro vídeo)
- **Claude Code** no computador (terminal ou extensão do VS Code; Windows, Mac ou Linux). A skill roda scripts e comandos no
  terminal: **não funciona** no chat do Claude Desktop nem no claude.ai.
- **ffmpeg**, **Node 20+** e **Python 3.12 com uv** (o venv de ferramentas é criado com uv). O `preflight.py` mostra o que falta
  e o comando de instalação de cada item.
- **GROQ_API_KEY** (chave grátis em console.groq.com) para a transcrição, e **Chrome** para os prints de página.
- Opcionais: **yt-dlp** (trechos do YouTube), **PEXELS_API_KEY** e **PIXABAY_API_KEY** (chaves grátis, bancos de vídeo e foto),
  skill **video-use** (forma de onda). Sem eles a skill funciona; só perde aquela fonte.
- **Licença do Remotion** (o motor de animação dos vídeos): grátis para pessoa física e empresa de até 3 pessoas. Empresa maior
  precisa da licença paga do Remotion (remotion.dev/license). Avisar o usuário uma vez, no primeiro vídeo.
- A divisão de trabalho abaixo cita Opus e Sonnet. Se o plano do usuário não tiver Opus, usar o melhor modelo disponível.
- Sons e músicas vêm do Mixkit e são baixados na hora do uso (a licença do Mixkit não permite redistribuir os arquivos).

## BOOT (uma vez por sessão)
0. **Versão:** comparar o `VERSION` desta skill com a 1ª entrada do CHANGELOG publicado:
   `curl -fsSL https://raw.githubusercontent.com/paulovyn1/triwer-skills/main/edicao-motion-triwer/CHANGELOG.md | grep -m1 "^## "` (ou a ferramenta de acesso à web na
   mesma URL). Sem acesso, seguir sem dizer nada. Igual à local, seguir. **Só se a remota for mais nova:** ler e seguir
   `references/atualizacao-versao.md`.
1. `python scripts/preflight.py`. FALTA em ffmpeg, node, uv, venv de ferramentas ou GROQ_API_KEY: resolver com o usuário antes
   do primeiro vídeo (o preflight mostra o comando). FALTA em video-use ou yt-dlp não impede o uso (opcionais). Se a pasta de
   dados não existir: `python scripts/preferencias.py iniciar --nome "<nome>"`.

## Começo de todo vídeo (barato, sempre)
1. **Estilo:** ler `estilos/INDICE.md` e escolher pelo tema. Abrir **só** o cartão escolhido + `estilos/gramatica.md`. Se o usuário
   nomear um estilo ("faz no Mural de Memórias"), usar esse.
2. **Preferências:** `python scripts/preferencias.py mostrar --estilo <id> --cliente "<cliente>"`. São regras aprendidas, valem mais
   que o padrão da skill, e a mais nova vale mais que a mais antiga.
3. **Fluxo:** com pessoa filmada → etapas 0 a 6 abaixo. Narrado ou sem pessoa → `references/narrado.md`.

## Aprender com cada ajuste (obrigatório)
Quando o usuário pedir correção ou ajuste que revela **gosto ou padrão** ("não gostei de X", "sempre faça Y", "ficou robótico",
"prefiro..."), registrar na hora, numa linha, sem abrir o arquivo:
`python scripts/preferencias.py registrar "<regra acionável>" --tipo gosto|evitar|processo|audio|estilos|ambiente [--estilo id] [--cliente nome] [--origem "<vídeo>"]`.
Conserto pontual daquele vídeo não vira regra. Na dúvida, registrar com escopo menor (`--cliente` ou `--estilo`). Se o `mostrar`
avisar que passou de 60 regras, consolidar o arquivo: juntar repetidas e apagar as que a mais nova contradiz.

## Estilo novo (o usuário mandou vídeo de referência)
1. `python scripts/analisar_referencia.py "<vídeo>"`. Mede cortes, transições, fala com tempos, ritmo e áudio, e gera folhas de
   quadros rotuladas com tempo + palavra falada + borda vermelha no corte.
2. Ler o `resumo.txt` **antes** das folhas e depois abrir as folhas uma vez. Comparar com o `INDICE.md`: se for variação de um
   estilo existente, anotar a diferença como regra `--estilo`.
3. Se for estilo novo: escrever o cartão com `estilos/_modelo.md` em `<dados>/estilos/<id>.md` (estilo próprio) e registrar o
   caminho do vídeo em `<dados>/referencias.md`. Depois do cartão escrito, **não abrir mais** o vídeo de referência.
4. Estilos próprios ficam na pasta de dados (`<dados>/estilos/`) e sobrevivem às atualizações da skill. Mesmo id de um
   cartão da skill substitui o cartão.

## Divisão de trabalho (qualidade no Opus, o resto fora do contexto)
| Trabalho | Quem |
|---|---|
| Estratégia, estilo, roteiro de cenas/legenda, mapa emocional da música, revisão final | **principal (Opus)** |
| Painel ou cena inédita, ou que muda animação | **subagente Opus** por painel, ou por lote de cenas do mesmo tipo, em paralelo e em segundo plano |
| Adaptar painel ou cena só em texto/tempo; QA das folhas de quadros | **subagente Sonnet** |
| Medir referência, transcrição, cortes, voz, palavras, busca de material, música, mix, render, entrega | **scripts Python** (zero token; o principal lê só a saída) |

## Regras de custo (valem em toda etapa)
1. **Ler só a referência da etapa atual**, só o cartão do estilo escolhido e só as preferências filtradas (`mostrar`).
2. **Código de painel ou cena nunca entra no contexto principal**: é trabalho de subagente. Cena nova = composição dos blocos
   de `template/remotion/src/blocos` (vitrine em `Demo.tsx`).
3. **Imagem custa caro.** Para ver qualquer coisa, usar folha numerada:
   - referência: `analisar_referencia.py`;
   - render: `verificar.py stills` ou `stills.mjs`;
   - material: `buscar_stock.py`.

   O QA das folhas é do subagente Sonnet. Nunca `Read` de quadro solto em série.
4. **Medir antes de olhar:** o que um script mede (cortes/min, sincronia, quadro parado, loudness) não se confere no olho.
5. **Texto antes de código:** roteiro de cenas/legenda aprovado em texto (portão 2) antes de construir. A prévia (10 a 16 s) só
   do trecho mais difícil, e só com estilo novo.
6. **Menos mensagens:** cada mensagem relê todo o contexto. Juntar comandos numa chamada, deixar render/mix/subagentes em segundo
   plano e fazer 1 lote de verificação.
7. **Não reconstruir o motor:** partir de `template/remotion` e dos blocos. Efeito novo que sirva a outros estilos vira bloco.
8. Renders com TEMP/TMP num disco com espaço (`ambiente.json → temp_render`); scripts rodam de dentro de `edit/`.

## Portões de aprovação (perguntar ANTES de gastar; podem ir juntos numa pergunta)
1. **Estilo + estratégia** (janela do vídeo, ritmo, identidade, quantos painéis/cenas) + **mapa emocional da música**.
2. **Roteiro da legenda e lista de painéis**, ou **`cenas.json`** no narrado (texto, nada construído ainda).
3. **Prévia de 10 a 16 s** se o estilo for novo para este usuário ou cliente.
4. **Música:** 2 a 3 versões (A/B/C) com faixas diferentes. O usuário escolhe de ouvido.
5. **Efeitos:** o usuário vê o vídeo de efeitos numerados e responde "#12 b", "#20 tirar".

## Fluxo com pessoa filmada: etapa → ler → rodar
Abrir o kit do cliente primeiro (marca, compliance, painéis prontos). Pasta de trabalho: `<pasta do vídeo>/edit/`.

| # | Etapa | Ler | Rodar (`scripts/`) | Saída |
|---|---|---|---|---|
| 0 | Ambiente e leitura | `ambiente.md` (se o preflight falhar) | `preflight.py`, `preparar.py "<video>"` | `edit/`, `projeto.json`, `work/leitura.txt` |
| 1 | Cortes | `corte.md` | `bordas.py <t...>`, `achar_gagueira.py`, `make_edl.py`, `extract_base.py` | `edl.json`, `work/base.mp4` |
| 2 | Voz | `audio.md` | `limpar_voz.py` | `work/voz_limpa.wav` |
| 3 | Legenda | `legenda.md` | `montar_motion.py --kit ... --paineis ... --novos ...`, `words_out.py`, `matte_rvm.py` (se houver behind), `verificar.py lint` | `words.json`, `captions.ts`, `timeline.ts` |
| 4 | Painéis | `paineis.md` + cartão do estilo | briefs + subagentes, `montar_sfx.py`, `verificar.py stills` + QA Sonnet | `src/panels/*.tsx`, `audio/sfx.json` |
| 5 | Música e mix | `musica-mixagem.md` | `escolher_musica.py`, `mix.py A/B/C`, `medir_mix.py`; efeitos: `sfx.py buscar` | `mix_A/B/C.wav` |
| 6 | Render e entrega | `entrega.md` | `entregar.py all "Nome" --render` (segundo plano), `verificar.py final` | `entrega/*.mp4`, revisão de efeitos |

Material real em qualquer etapa: `references/fontes-reais.md` (`baixar_trecho.py`, `buscar_stock.py`, `capturar_print.py`,
`buscar_comentarios.py`). Bibliotecas de áudio (atualizar de vez em quando, em segundo plano): `indexar_musicas.py` e `indexar_sfx.py`.

## Qualidade que não se negocia (detalhes nas referências)
- **Estilo:** um protagonista por cena; texto que compõe a cena, sincronizado com a fala a ±2 quadros; diagramação variando entre
  cenas; transições do vocabulário da `gramatica.md`; textura orgânica; nada parado por mais de 0,5 s.
- **Cortes:** nunca dentro de palavra; borda com 50 a 80 ms de folga (`bordas.py`); quadros exatos; fade de 30 ms; pausas
  dramáticas mantidas.
- **Voz:** passa-alta + denoise leve + EQ de presença + de-esser + compressor; stem ≈ −11,8 LUFS.
- **Legenda:** vocabulário misto (build, slam, stack, behind, knock, ghost), com efeito forte só nas frases de impacto e fora da
  zona de interface.
- **Painéis e cenas:** uma ideia por painel ou cena; pouso na palavra (`useAt`/`palavrasDe`), nunca linear; estado final visível
  por ≥ 14 quadros; `auditar_movimento.py` com ≤ 3% parado e sem salto seco.
- **Material real:** fonte e data visíveis, licença em `creditos.json`, pessoa famosa nunca em anúncio pago, pessoa comum
  anonimizada.
- **Recorte da pessoa:** PNG por quadro, nunca webm com alfa. `verificar.py final` precisa passar.
- **Música:** escolhida pela emoção de cada trecho (1 a N faixas), diferente a cada vídeo do mesmo cliente, já no groove no 1º
  segundo, ~17 dB abaixo da voz, ducking ≤ 6 dB.
- **Efeitos:** som literal do que aparece, poucos (≈ 0,9/s), cada um com gatilho visível, de 3 a 8 dB abaixo da voz, com revisão
  numerada.
- **Master:** −14 LUFS, pico ≤ −1 dBTP, medido. O Claude não ouve: relatar os números e pedir teste de ouvido no celular.

## Skills relacionadas (consultar só no ponto indicado, se estiverem instaladas)
- **remotion** (skill oficial do Remotion): para o subagente de painel ou cena que precisar (`rules/animations.md`, `timing.md`,
  `text-animations.md`).
- **video-use** (opcional): `helpers/timeline_view.py` (forma de onda).
- Skill de estilo de escrita do usuário (`estilo-[nome]`, gerada pela `estilo-forge`), para copy e legenda. Skill de geração de
  imagem, se houver, para objeto e textura (nunca pessoa real). **motion-design**, se houver, para easing e timing.

## Medir custo (quando pedirem comparação)
`python scripts/custo.py marca "<n>-<etapa>"` no início de cada etapa e `custo.py relatorio` no fim.

## Ao terminar
- Escrever `edit/project.md` (decisões e pendências).
- Registrar as preferências novas (`preferencias.py registrar`).
- Regra técnica nova vira preferência (`--tipo processo`) e regra de marca vai para o kit do cliente. Não editar os arquivos
  desta skill: a pasta é substituída a cada atualização (preferências, estilos próprios e kits ficam fora dela).
