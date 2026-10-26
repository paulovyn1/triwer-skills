# Catálogo de estilos de edição

Ler este índice para escolher. Depois abrir **só** o cartão escolhido e `gramatica.md`. Estilos próprios do usuário ficam na pasta
de dados dele (`preferencias.py onde` → `estilos/`). O cartão pessoal tem o mesmo formato e, se tiver o mesmo id, vale no lugar
deste.

| Estilo (id) | Cara em uma linha | Pede | Melhor para |
|---|---|---|---|
| **Fala Dinâmica** (`fala-dinamica`) | pessoa falando com legenda que interage com ela (texto atrás da cabeça, knockout, slam) e painéis de motion | pessoa filmada | Reels e anúncio de quem fala para a câmera |
| **Recorte de Jornal** (`recorte-de-jornal`) | papel bege, preto e vermelho; matérias recortadas com marca-texto; palavra-chave enorme em serifa | pessoa filmada (ou narração forte) + matérias reais | notícia, polêmica, caso de mercado, "olha o que saiu" |
| **Documentário Colagem** (`documentario-colagem`) | papel claro com grão; fotos e filmes de arquivo recortados; anotação à mão; uma palavra por vez no centro | narração + material de arquivo | história real, personagem, fato curioso, "ninguém sabe que..." |
| **P&B Neon** (`pb-neon`) | mundo em preto e branco com uma cor brilhando; objetos 3D sobre papel quadriculado; script + sans; câmera girando | narração + recorte da pessoa | análise "por trás de", estratégia, autoridade explicando conceito |
| **Mural de Memórias** (`mural-de-memorias`) | coisas físicas: jornal, polaroids na cortiça, pastas, crachás, pôster gigante; luz de janela; legenda pequena constante | narração + fotos e vídeos pessoais | história pessoal, origem, nostalgia, manifesto em primeira pessoa |
| **Mesa e Telas** (`mesa-e-telas`) | interfaces reais recriadas (câmera, notas, mensagens, busca) e objetos na mesa vistos de cima, com sol de janela | narração | insight de negócio, comportamento digital, dado de pesquisa |
| **Prancheta Técnica** (`prancheta-tecnica`) | produto visto de cima com cotas, réguas e anos; troca de versão no mesmo lugar; terminal digitando | narração curta | produto, evolução, consistência, tecnologia (vídeo curto) |

## Escolha rápida
- Tem **pessoa falando para a câmera** → `fala-dinamica`. Se o assunto for notícia ou matéria, inserir trechos de `recorte-de-jornal`.
- **Narração sem pessoa** → o tema decide:
  - passado ou personagem: `documentario-colagem`;
  - eu ou a minha história: `mural-de-memorias`;
  - conceito ou estratégia: `pb-neon`;
  - mercado digital ou dado: `mesa-e-telas`;
  - produto: `prancheta-tecnica`.
- Dá para misturar no máximo 2 estilos, e só se dividirem o mesmo mundo e a mesma paleta. Exemplo: `fala-dinamica` com inserções
  de `mesa-e-telas` no lugar dos painéis.
- Estilo novo pedido pelo usuário (veio com vídeo de referência): `analisar_referencia.py` → escrever o cartão com `_modelo.md` na
  pasta de dados do usuário. Ver "Estilo novo" no SKILL.md.
