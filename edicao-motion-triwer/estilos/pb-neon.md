# P&B Neon (`pb-neon`)

Mundo em preto e branco, com uma cor só brilhando (vermelho com glow). Objetos 3D realistas (olho, cérebro, anzol, diamante)
pousam sobre papel quadriculado. A pessoa aparece recortada em P&B num canto. Letra script e sans arredondada se misturam, e a
câmera gira em 3D com formas desfocadas passando na frente.

## Quando usar / quando não
- **Usar** para análise do tipo "o segredo por trás de", estratégia, autoridade explicando um conceito, desconstrução de um caso
  famoso. A emoção é de inteligência e revelação controlada.
- **Não usar** em tema leve ou divertido, nem em vídeo que precisa de muita cor (produto, comida).

## Precisa ter
- Narração firme, de 150 a 170 palavras/min.
- Recorte da pessoa ou personagem (foto P&B, sem fundo).
- De 4 a 8 objetos-metáfora isolados: gerados por IA ou de banco, sempre recortados.
- Prints e miniaturas de prova, se houver.

## Assinatura
- **Mundo e fundo:**
  - papel branco-gelo com grade fina (quadriculado de engenharia);
  - preto profundo para as frases de virada;
  - formas pretas desfocadas em primeiro plano (folhas, hastes, triângulos) passando na frente da câmera;
  - vinheta pesada e aberração cromática vermelho/ciano nas bordas.
- **Tipografia:** script elegante (Great Vibes ou Pinyon Script) para a parte "falada" da frase. Sans arredondada pesada
  (Fredoka 600) para o núcleo da frase. A palavra-chave vai em vermelho (#ff2d2d) com glow e leve desfoque, as demais em
  preto ou cinza.
- **Texto × cena:**
  - quando o objeto é protagonista: a frase fica curta, acima dele, em 2 linhas (script + sans);
  - quando o texto é protagonista: fundo preto, script cinza e a palavra de virada em vermelho brilhando ("It's not
    decoration / It is a pacing tool").
  - As palavras entram com desfoque para nítido, no tempo da fala.
- **Transições:** `camera-continua` e `puxar-foco` dominam (poucos cortes). Rotação 3D da câmera em 5 a 15° entre cenas,
  `mergulho` no preto e `corte-seco` só na entrada das frases no escuro.
- **Ritmo (referência):** 17 cortes/min, mas a câmera nunca para. Plano médio de 3,1 s, fala a 158 palavras/min.
- **Áudio:** trilha grave e minimalista (pulso), whoosh suave nos giros, golpe seco + reverso nas viradas no escuro.

## Tipos de cena
| id | Cena | Protagonista | Como se faz |
|---|---|---|---|
| `retrato-com-nome` | pessoa recortada em P&B no centro, nome em script acima e a frase-gancho embaixo em vermelho | imagem | `Camera` (giro de 8° em rz/ry) + `Cartao` sem moldura + `PalavrasNaFala` + `Aberracao` |
| `objeto-na-grade` | objeto 3D realista sobre papel quadriculado, frase em script + sans acima | equilíbrio | grade CSS + imagem recortada com sombra + `Foco` nas formas da frente |
| `frase-no-escuro` | fundo preto, script cinza e palavra de virada em vermelho com glow | texto | `PalavrasNaFala` (entrada "desfoque") + text-shadow vermelho |
| `parede-de-provas` | prints e miniaturas flutuando em profundidade, frase bold no centro | texto | `Camera` com cartões em z diferentes + `Foco` |
| `pessoa-no-canto` | pessoa recortada no canto inferior + frase grande desfocando e entrando | texto | recorte + `PalavrasNaFala` + luz suave (gradiente) |
| `quadro-de-plano` | papéis presos com fita e ligados por barbante (pesquisa, ideia, roteiro) | equilíbrio | `Cartao preso="fita"` + `Barbante` + `Camera` em travelling |
| `cta-baloes` | balões de mensagem em linha + CTA com a palavra-chave em verde | texto | ícones SVG + `PalavrasNaFala` |

## Receita técnica
- Blocos: `Camera` (perspectiva 1800, giros pequenos), `Foco`, `Aberracao` (px 3, só em cenas curtas), `Vinheta` (0,6),
  `Grao` (0,08), `PalavrasNaFala`, `Cartao`, `Barbante`.
- Grade: `backgroundImage` com 2 linear-gradients, linhas de 1 px a 8% de opacidade e passo de 54 px. Leve deslocamento
  contínuo, nunca parado.
- Glow vermelho: `textShadow: 0 0 18px rgba(255,45,45,.7), 0 0 42px rgba(255,45,45,.35)`.
- Objetos: imagem gerada com fundo verde, recortada, com sombra de contato (elipse desfocada embaixo).

## Onde buscar o material
- Objetos: `gerar-imagem`, gerando sobre fundo verde e recortando.
- Pessoa: foto real recortada, em P&B.
- Prova (miniatura de vídeo, manchete): print real com `capturar_print.py`.

## Erros que matam o estilo
- Uma segunda cor de destaque.
- Objeto sem sombra de contato, que fica "colado".
- Câmera parada.
- Script em frase longa, que fica ilegível no celular (no máximo 4 palavras em script).
- Aberração cromática forte demais.

## Checagem antes de entregar
- Contar os quadros sem movimento de câmera ou foco (nenhum trecho > 0,5 s).
- Uma única cor saturada no vídeo inteiro (amostrar as folhas).
- Script legível em miniatura de 216 px.

## Origem
Referência de 28 s: 8 cortes, plano médio de 3,1 s, 158 palavras/min, −14,8 LUFS, 5 de 8 cortes com golpe de áudio.
