// Blocos reutilizáveis dos estilos (estilos/*.md). Cena nova = composição destes blocos; código novo só no que é próprio da cena.
// Vitrine e teste visual: composição "DemoBlocos" (src/blocos/Demo.tsx) → node stills.mjs <saida> 0.4 --comp DemoBlocos 0 30 60 ...
export { Grao, Vinheta, FundoPapel, MeioTom, BordaFilme } from "./Textura";
export { SombraJanela, Foco, Aberracao } from "./Luz";
export { Camera, NoMundo, poseEm } from "./Camera";
export type { Pose } from "./Camera";
export { PalavrasNaFala, Escrever, Caneta, MarcaTexto, Contador, Pilula, normalizar } from "./Escrita";
export type { Palavra } from "./Escrita";
export { Cartao, Barbante, Rajada, Faixa, fonte } from "./Objetos";
export { Chicote } from "./Transicao";
export { palavrasDe, palavrasManuais } from "./fala";
