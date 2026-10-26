# Recorte de Jornal (`recorte-de-jornal`)

Fundos de papel bege com grão, preto carvão com riscos de luz e vermelho profundo. Por cima vêm recortes de matéria real
(manchete, faixa de categoria vermelha, trecho com marca-texto), fotos recortadas com etiqueta pendurada e print com caixa
vermelha. A legenda tem dois níveis: palavras de ligação pequenas em sans e a palavra-chave enorme em serifa.

## Quando usar / quando não
- **Usar** para notícia, polêmica, caso de mercado, "olha o que saiu na imprensa", análise de pessoa pública. A emoção é de
  urgência e prova.
- **Não usar** sem pessoa filmada e sem matérias reais. Só com motion e imagens geradas, fica artificial: a força do estilo é
  a pessoa falando rápido e as provas reais.

## Precisa ter
- Pessoa falando, de 200 a 250 palavras/min. Narração forte só se houver muito material real.
- De 4 a 8 matérias ou prints reais (em português, ou traduzidos com a fonte).
- Fotos de pessoas ou produtos citados (com direito de uso).

## Assinatura
- **Mundo e fundo:**
  - papel bege (#e9e1d3) com grão e vinheta;
  - preto carvão (#141414) com riscos de luz horizontais (glitch leve);
  - vermelho profundo (#8f0f12 → #3d0607);
  - foto P&B desfocada atrás do texto.
  - No começo, a tela vem dividida: pessoa em cima, imagem embaixo.
- **Tipografia:** palavras de ligação em Inter de 44 a 52 px (branco ou preto). Palavra-chave em serifa de display enorme, de
  150 a 220 px (DM Serif Display ou Instrument Serif itálico), quase sempre com a pontuação da fala. Palavra corrigida riscada
  em vermelho.
- **Texto × cena:** a legenda é palavra por palavra no tempo da fala, em 2 níveis. As matérias são protagonistas quando
  aparecem, e a legenda encolhe para o canto.
- **Transições:** cortes a cada 1 a 2 s (pessoa ↔ prova), `cobrir` (recorte entrando por cima), `chicote` curto com glitch nas
  sequências rápidas, grave de impacto nas viradas.
- **Ritmo (referência):** troca visual a cada 1 a 2 s, fala a cerca de 250 palavras/min.
- **Áudio:** voz dominante (−14 LUFS, LRA 7), grave de impacto (boom) nas viradas, whoosh e glitch agudo nas transições rápidas,
  trilha baixa.

## Tipos de cena
| id | Cena | Protagonista | Como se faz |
|---|---|---|---|
| `pessoa-e-legenda` | pessoa falando com legenda de 2 níveis por cima | imagem + texto | pipeline de `fala-dinamica` com o tema deste estilo |
| `materia-com-marca-texto` | recorte da manchete real, faixa de categoria vermelha, trecho com marca-texto | imagem | print real (`capturar_print.py`) recortado + `MarcaTexto` + `Cartao` |
| `foto-com-etiqueta` | foto recortada com etiqueta de produto pendurada (código de barras, "O MAIS CARO") | imagem | `Cartao` + etiqueta em JSX com balanço (rotação de mola) |
| `print-com-caixa` | print de perfil ou post com caixa vermelha destacando a frase | imagem | print + retângulo desenhado (`Caneta forma="x"` ou borda animada) |
| `mosaico-com-numero` | mosaico de fotos + número grande ("1,9 mi") | texto | grade de imagens + `Contador` |
| `palavra-riscada` | palavra dita e corrigida, riscada em vermelho | texto | `Caneta forma="risco"` sobre a palavra |

## Receita técnica
- Blocos: `PalavrasNaFala` (2 níveis: lista de palavras-chave com estilo próprio), `FundoPapel`, `Grao` (0,09),
  `Vinheta` (0,45), `MarcaTexto`, `Caneta`, `Cartao`, `Chicote`, `Contador`.
- Riscos de luz no preto: 2 ou 3 linhas horizontais de 1 a 3 px, brancas a 30%, deslocando por quadro, com aberração leve.
- Legenda e matéria nunca disputam: com matéria na tela, a legenda vai para 36 px no terço inferior.

## Onde buscar o material
Portais brasileiros primeiro (lista em `references/fontes-reais.md`). Matéria estrangeira entra com tradução na tela, "tradução
livre" e a fonte (veículo e data). Post de rede social vira **cartão de citação** (texto + autor + data), nunca imitação de
print da rede.

## Erros que matam o estilo
- Matéria inventada ou print falso.
- Sem fonte visível.
- Palavra-chave em toda palavra (perde o efeito).
- Muitas cores além de bege, preto e vermelho.
- Recriar o estilo sem pessoa e sem prova real.

## Checagem antes de entregar
- Toda prova com veículo e data legíveis na tela por pelo menos 1 s.
- Palavra-chave em no máximo 1 a cada 3 palavras.
- Grave em cada virada marcada no roteiro.

## Origem
Referência de 22,8 s: troca visual a cada 1 a 2 s, cerca de 250 palavras/min, −14,1 LUFS.
