# Biblioteca de painéis

- **Blocos genéricos** (servem a qualquer estilo e cliente): `template/remotion/src/blocos`, com câmera contínua, texturas, luz de
  janela, foco, aberração, palavras no tempo da fala, máquina de escrever, caneta, marca-texto, contador, pílula, cartão/polaroid,
  barbante, rajada, faixa de cinema e chicote. A vitrine fica em `blocos/Demo.tsx`.
- **Painéis prontos de um cliente** ficam no kit dele (`<kit>/paineis-<vídeo>/`), com os tempos por `useAt` e um `POUSOS.md` quando
  forem reaproveitados com outra fala (`src/warp.ts`).
- **Próxima fase** (conforme os vídeos pedirem): painel que servir a 2 clientes vira componente **parametrizado** aqui (props: textos,
  cores, tempos), com exemplo de uso e os quadros de efeito sonoro. Candidatos já vistos: checklist, pilha de cards, comunicado,
  carimbo, cronômetro, escada, contador, parede de logos, ciclo, player, CTA em pílula.
