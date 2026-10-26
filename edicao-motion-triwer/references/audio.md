# Áudio: limpeza e equalização da voz, níveis e master

Etapa 4. Entrada `work/voz_cortada.wav`; saída `work/voz_limpa.wav`. A mixagem final (música, efeitos, ducking, master) está em
`musica-mixagem.md`; aqui ficam os números que valem pra tudo.

```
python <skill>/scripts/limpar_voz.py            # padrão; --nr 20 se tiver ruído pesado; --filtro "<cadeia>" pra customizar
```
Imprime espectro de pausas/fala antes e depois por faixa (dB) e LUFS/pico. Conferir: pausa abaixo de −75 dB em 20-500 Hz e fala com
mais energia em 2-8 kHz que antes.

## Cadeia padrão (ordem importa) e por quê

| Passo | Valor | Função |
|---|---|---|
| passa-alta | 85 Hz, 2 polos | tira rumble, vento, manuseio do celular |
| afftdn | nr 12, nf −62, tn 1 | ruído de banda larga, leve (acima de 15 vira "voz de lata") |
| EQ 60 Hz | −6 dB, Q 1 | zumbido de rede/ar-condicionado (50/60 Hz medidos em ~4 dB acima do vizinho no C2) |
| EQ 320 Hz | −3 dB, Q 1,1 | "caixa"/boxy de voz gravada perto de parede |
| EQ 3,2 kHz | +4,5 dB, Q 1,3 | presença/inteligibilidade (celular na rua perde isso) |
| shelf 7,5 kHz | +4 dB | ar/brilho, compensa a compressão do mic do celular |
| de-esser | i 0,35 | contém o "s" que o shelf e a presença realçam |
| compressor | −22 dB, 3:1, 6/90 ms, makeup 3 | nivela sílabas fortes/fracas (Reels é ouvido em ambiente ruidoso) |
| limitador | 0,89 | rede de segurança de pico |

- Diagnóstico antes de mexer: o relatório do script. Se a pausa tiver energia em 1-4 kHz (ventilador, rua), subir `--nr` ou
  trocar por `arnndn` (rede neural do ffmpeg, precisa de modelo `.rnnn`); se tiver tom fixo (zumbido), um `equalizer` estreito no hertz medido.
- Voz gravada no celular ao ar livre, ruído baixo (piso −55 dB): a cadeia padrão bastou.

## Números-alvo (medidos no C2, que ficou bom)

- Stems antes do master: **voz −11,8 LUFS**, **música −28,5 LUFS** (≈ 17 dB abaixo), **efeitos −26,7 LUFS**.
- Ducking: música cede até **6 dB** quando há voz/efeito (2,5:1, ataque 10 ms, soltura 250 ms). Mais que isso ("15-20 dB a cada fala")
  soa como automação, e a pesquisa de mixagem de Reels diz o mesmo.
- Cada efeito pontual: **3 a 8 dB abaixo da voz** na janela de 200 ms em volta (o mix.py não mede isso sozinho; conferir pelo
  script de medição em `entrega.md`). Batimento/impacto de clímax podem encostar na voz (≈ 0 dB), nunca passar.
- Master: loudnorm 2 passadas **−14 LUFS, pico real ≤ −1 dBTP** (saiu −14,0 / −2,0). LRA baixa (1,2 LU) é normal em fala + cama.
- Ouvir em celular antes de publicar: o Claude não ouve; relatar os números e pedir o teste de ouvido ao usuário.

## Armadilhas
- Aplicar a cadeia **depois** do corte (o `extract_base.py` já entrega o WAV cortado com fades de 30 ms): evita o ruído "respirando" entre cortes.
- Não normalizar a voz isolada pra −14: o master é só no final, com tudo somado.
- `afftdn` em arquivo com música embutida destrói a música: a voz é separada antes (nos testes, o áudio original era só voz).
