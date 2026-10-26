// Câmera e layout: divisão de tela (painel em cima, pessoa embaixo) e zoom nos jump cuts.
import { interpolate } from "remotion";
import { easeInOut, easeOut } from "./theme";
import { CUTS, PUNCH, SPLIT_KEYS } from "./timeline";


export const splitAt = (f: number) => {
  let v = 0;
  for (const [a, b, to] of SPLIT_KEYS) {
    if (f >= b) v = to;
    else if (f >= a) {
      const from = v;
      return interpolate(f, [a, b], [from, to], { easing: easeInOut });
    }
  }
  return v;
};

/** desloca o vídeo pra baixo: rosto (y≈860) vai pro centro da metade de baixo */
export const SPLIT_SHIFT = 520;


export const segmentIndex = (f: number) => {
  let i = 0;
  for (let k = 0; k < CUTS.length; k++) if (f >= CUTS[k]) i = k;
  return i;
};

/** escala do vídeo da pessoa no frame f (alternância por corte + drift + golpes) */
export const zoomAt = (f: number) => {
  const i = segmentIndex(f);
  const a = CUTS[i];
  const b = CUTS[i + 1] ?? a + 60;
  const base = i % 2 === 0 ? 1.0 : 1.11;
  const drift = interpolate(f, [a, b], [0, 0.03], { easing: easeInOut, extrapolateRight: "clamp" });
  let punch = 0;
  for (const [pf, peak, settle, attack] of PUNCH) {
    // o golpe só vale dentro do segmento onde começou (sumir no meio do plano seria um pulo visível)
    if (f < pf || segmentIndex(pf) !== i) continue;
    const p =
      attack > 0
        ? interpolate(f, [pf, pf + attack], [0, peak - base], { easing: easeInOut, extrapolateRight: "clamp" })
        : interpolate(f, [pf, pf + settle], [peak - base, 0.06], { easing: easeOut, extrapolateRight: "clamp" });
    punch = Math.max(punch, p);
  }
  const z = base + drift + punch;
  return 1 + (z - 1) * (1 - splitAt(f));
};

export const captionY = (f: number) => interpolate(splitAt(f), [0, 1], [1330, 960]);
