// DADOS POR-VÍDEO (junto com captions.ts e public/*). O resto de src/ é o motor: não mexer.
// Frames de saída, 30 fps.
import cutsJson from "../public/cuts.json"; // gerado por make_edl.py
// import { P01 } from "./panels/P01";       // um import por painel (copiados do kit do cliente ou novos)

export const TOTAL: number = cutsJson.total;
/** frame de saída onde começa cada segmento (jump cut) */
export const CUTS: number[] = cutsJson.cuts;

/** divisão de tela: [frame início da rampa, frame fim da rampa, valor depois]; 0 = pessoa tela cheia, 1 = pessoa na metade de baixo.
 *  Regra: rampa de 7-9 frames terminando em from+9 do painel "top" (entra) e começando 7 frames antes do fim dele (sai). */
export const SPLIT_KEYS: [number, number, number][] = [
  // [55, 64, 1],
  // [123, 130, 0],
];

/** golpes de zoom: [frame, escala de pico, frames pra assentar, frames de ataque (0 = golpe seco, só em frame de corte)] */
export const PUNCH: [number, number, number, number][] = [
  // [0, 1.28, 14, 0], // gancho
];

export type PanelKind = "top" | "cover" | "overlay"; // top 1080x960 (pessoa embaixo) | cover 1080x1920 | overlay 1080x1920 transparente
export type PanelDef = { id: string; from: number; to: number; kind: PanelKind; C: React.FC };

export const PANELS: PanelDef[] = [
  // { id: "P01", from: 55, to: 130, kind: "top", C: P01 },
];
