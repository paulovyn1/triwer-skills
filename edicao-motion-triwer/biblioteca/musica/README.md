# Biblioteca de música (Mixkit)

Licença Mixkit Stock Music: uso comercial e anúncio online liberados, sem crédito; proibido em CD/DVD/jogo/TV/rádio
(conferido em 19/10/2026 em mixkit.co). Os `.mp3` não ficam no repo: o áudio vai para o cache (`ambiente.json → cache`, pasta `musica/`) e para
`edit/music_cand/` só quando escolhido.

- `indice.json`: todas as faixas encontradas nas páginas de categoria do Mixkit (título, duração, tags `[tipo, slug, nome]` de humor,
  gênero, instrumento e tag). Gerar/atualizar: `python scripts/indexar_musicas.py`.
- `analise.json`: por faixa, BPM, tom (Camelot), confiança, energia 0-8/8-30/30-90 s, curva de energia a cada 5 s, pulso e brilho.
  Gerar/atualizar: `python scripts/indexar_musicas.py --analisar` (segundo plano, ≈ 4 s por faixa; apaga o mp3 depois de medir).
- `scripts/emocoes.py`: as 11 emoções e como cada faixa pontua (tags + modo + andamento). `scripts/escolher_musica.py` usa tudo isso.
- Músicas já entregues por cliente: `<dados>/musicas_usadas.json` (pasta de dados do usuário, fora da skill; `_dados.py`).
- Legado: `mixkit_index.txt` (227 faixas) e `scan_mixkit_40.json` (40 faixas medidas à mão no C2), mantidos só como histórico.
