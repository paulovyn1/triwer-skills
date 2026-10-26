// Identidade visual PADRÃO (neutra). O kit do cliente substitui este arquivo (montar_motion.py --kit copia assets/theme.tsx).
// Manter os mesmos nomes exportados (C, F, PanelBg, Tape...): os painéis e camadas usam essas chaves.
import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame } from "remotion";
import { loadFont as loadOutfit } from "@remotion/google-fonts/Outfit";
import { loadFont as loadManrope } from "@remotion/google-fonts/Manrope";
import { loadFont as loadSerif } from "@remotion/google-fonts/InstrumentSerif";

export const FPS = 30;
export const W = 1080;
export const H = 1920;
export const PANEL_H = 960; // painel da metade de cima

export const C = {
  navy: "#111216",
  navy2: "#17191f",
  navy3: "#1f222a",
  line: "#c9ccd4",
  blue: "#3b82f6",
  blue2: "#7aa7ff",
  yellow: "#ffd23f",
  ink: "#f3f4f6",
  muted: "#a3a7b3",
  red: "#ff4d4d",
  black: "#0b0b0b",
};

const outfit = loadOutfit("normal", { weights: ["400", "600", "700", "800", "900"], subsets: ["latin", "latin-ext"] });
const manrope = loadManrope("normal", { weights: ["400", "600", "700", "800"], subsets: ["latin", "latin-ext"] });
const serif = loadSerif("italic", { weights: ["400"], subsets: ["latin", "latin-ext"] });

export const F = {
  display: outfit.fontFamily, // títulos e legenda base (pesos 600-900)
  body: manrope.fontFamily, // textos menores dentro das ilustrações
  serif: serif.fontFamily, // destaque emocional, sempre italic 400
};

/** segundos -> frames */
export const sec = (s: number) => Math.round(s * FPS);

export const easeOut = Easing.bezier(0.22, 1, 0.36, 1);
export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);

/** 0→1 com ease-out entre dois frames */
export const prog = (frame: number, from: number, dur: number, easing = easeOut) =>
  interpolate(frame, [from, from + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing });

/** mola padrão de entrada (pop) */
export const pop = (frame: number, from: number, fps = FPS, damping = 12, stiffness = 180) =>
  spring({ frame: frame - from, fps, config: { damping, stiffness, mass: 0.6 } });

/** Fundo de planta (blueprint) usado em todos os painéis: azul-marinho + grade + vinheta + grão */
export const PanelBg: React.FC<{ height?: number; children?: React.ReactNode }> = ({ height, children }) => {
  const f = useCurrentFrame();
  // a grade desliza devagar e o brilho respira: nenhum painel fica 100% parado (painel "morto" lê como travado)
  return (
    <AbsoluteFill
      style={{
        height: height ?? "100%",
        backgroundColor: C.navy,
        backgroundImage: `linear-gradient(rgba(185,205,240,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(185,205,240,0.06) 1px, transparent 1px)`,
        backgroundSize: "56px 56px",
        backgroundPosition: `${(f * 0.45) % 56}px ${(f * 0.3) % 56}px`,
        overflow: "hidden",
      }}
    >
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at 50% 40%, rgba(11,127,240,${0.22 + 0.04 * Math.sin(f / 17)}) 0%, rgba(13,21,38,0) 60%)`,
        }}
      />
      {children}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 160px rgba(0,0,0,0.55)", pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};

/** oscilação suave (px) pra elementos que ficam parados na tela: bob(frame, fase, amplitude, período em quadros) */
export const bob = (f: number, phase = 0, amp = 4, period = 64) => Math.sin(((f + phase) / period) * Math.PI * 2) * amp;

/** envelopa o conteúdo do painel com flutuação + respiração leves (use nos painéis novos; os do C2 já têm a deles) */
export const Float: React.FC<{ amp?: number; children?: React.ReactNode }> = ({ amp = 5, children }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        transform: `translate(${bob(f, 11, amp * 0.5, 91)}px, ${bob(f, 0, amp, 67)}px) scale(${1 + 0.008 * Math.sin(f / 31)})`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

/** Faixa de destaque (fita) atrás de uma palavra */
export const Tape: React.FC<{ children: React.ReactNode; size?: number; style?: React.CSSProperties }> = ({
  children,
  size = 64,
  style,
}) => (
  <span
    style={{
      display: "inline-block",
      background: C.yellow,
      color: C.black,
      fontFamily: F.display,
      fontWeight: 800,
      fontSize: size,
      lineHeight: 1.05,
      padding: "0.06em 0.32em",
      textTransform: "uppercase",
      letterSpacing: "-0.01em",
      boxShadow: "0 10px 30px -10px rgba(245,217,10,0.55)",
      ...style,
    }}
  >
    {children}
  </span>
);
