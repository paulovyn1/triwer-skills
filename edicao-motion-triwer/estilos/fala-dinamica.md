# Fala Dinâmica (`fala-dinamica`)

Pessoa falando para a câmera, com legenda que interage com ela: texto gigante atrás da cabeça, knockout (vídeo dentro das letras),
slam e palavra por palavra. Painéis de motion graphics entram na metade de cima ou em tela cheia, na identidade da marca. Há
zoom nos cortes. É o pipeline completo da skill (etapas 0 a 6 do SKILL.md).

## Quando usar / quando não
- **Usar** em Reels, anúncio ou VSL curta de quem grava falando, que é a maioria dos vídeos de criador e de cliente.
- **Não usar** quando não há gravação da pessoa (ver os estilos narrados no `INDICE.md`).

## Precisa ter
- Vídeo vertical da pessoa (celular serve), com voz limpa.
- Identidade da marca (kit do cliente).
- De 3 a 8 ideias de painel no roteiro.

## Assinatura
- **Mundo e fundo:** o vídeo da pessoa com zoom alternado nos cortes. Painéis em fundo da marca.
- **Tipografia:** a do kit do cliente (display pesada + serifa itálica de destaque).
- **Texto × cena:** a legenda base é palavra por palavra. Efeito forte (behind, knock, slam, stack) só nas frases de impacto.
  Painéis com uma ideia cada, pousando na palavra.
- **Transições:** cortes de fala (jump cut com zoom), painéis entrando com movimento, `puxar-foco` na entrada do behind.
- **Ritmo:** o da fala da pessoa depois dos cortes de silêncio, de 170 a 220 palavras/min. Algo novo a cada 1,5 a 3 s.
- **Áudio:** voz tratada, trilha por emoção (1 a N faixas), efeitos literais com gatilho visível.

## Tipos de cena
Vocabulário de legenda em `references/legenda.md` (build, slam, stack, behind, knock, ghost) e de painéis em
`references/paineis.md`. Os tipos de cena dos outros estilos podem virar painel (ex.: `interface-digitando` de `mesa-e-telas`
como painel de cima).

## Receita técnica
Template padrão (`template/remotion`): `layers/Pessoa.tsx`, `Captions`, `Knock`, `Panels`. Blocos de `src/blocos` dentro dos
painéis.

## Onde buscar o material
Kit do cliente (fotos, logos). Provas e prints conforme `references/fontes-reais.md`.

## Erros que matam o estilo
- Legenda estática.
- Efeito forte em toda frase.
- Painel parado.
- Recorte da pessoa congelado.
- Efeito sonoro sem gatilho.

## Checagem antes de entregar
`verificar.py final`, `auditar_movimento.py` (≤ 3% parado) e a revisão de efeitos numerada.
