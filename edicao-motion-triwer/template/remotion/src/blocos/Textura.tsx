// Texturas que tiram a cara de "modelo pronto": grão, papel, vinheta, meio-tom, marcas de película.
import React from "react";
import { AbsoluteFill, random, useCurrentFrame } from "remotion";

const ruido = (freq: number, tam: number, oit = 2) =>
  `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='${tam}' height='${tam}'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='${freq}' numOctaves='${oit}' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`;

/** Grão de filme animado (muda a cada `passo` quadros). forca 0..1 (0,05 sutil, 0,12 forte). */
export const Grao: React.FC<{ forca?: number; passo?: number }> = ({ forca = 0.08, passo = 2 }) => {
  const s = Math.floor(useCurrentFrame() / passo);
  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
        opacity: forca,
        mixBlendMode: "overlay",
        backgroundImage: ruido(0.85, 220),
        backgroundPosition: `${Math.round(random(`gx${s}`) * 220)}px ${Math.round(random(`gy${s}`) * 220)}px`,
      }}
    />
  );
};

/** Vinheta (bordas escuras). forca 0..1 */
export const Vinheta: React.FC<{ forca?: number; cor?: string; centroY?: number }> = ({ forca = 0.45, cor = "0,0,0", centroY = 45 }) => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      background: `radial-gradient(ellipse at 50% ${centroY}%, rgba(${cor},0) 42%, rgba(${cor},${forca}) 100%)`,
    }}
  />
);

/** Fundo de papel: cor base + manchas de baixa frequência + fibra fina. Conteúdo vai por cima (children). */
export const FundoPapel: React.FC<{ cor?: string; manchas?: number; fibra?: number; children?: React.ReactNode }> = ({
  cor = "#ebe8e1",
  manchas = 0.28,
  fibra = 0.16,
  children,
}) => (
  <AbsoluteFill style={{ backgroundColor: cor }}>
    <AbsoluteFill style={{ opacity: manchas, mixBlendMode: "multiply", backgroundImage: ruido(0.004, 1100, 3) }} />
    <AbsoluteFill style={{ opacity: fibra, mixBlendMode: "multiply", backgroundImage: ruido(0.55, 300) }} />
    {children}
  </AbsoluteFill>
);

/** Meio-tom (retícula de pontos) por cima de foto/filme de arquivo. tam = passo da retícula em px. */
export const MeioTom: React.FC<{ tam?: number; forca?: number }> = ({ tam = 6, forca = 0.3 }) => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      mixBlendMode: "multiply",
      opacity: forca,
      backgroundImage: "radial-gradient(circle, rgba(0,0,0,0.85) 32%, rgba(0,0,0,0) 36%)",
      backgroundSize: `${tam}px ${tam}px`,
    }}
  />
);

/** Marcas de película nas bordas laterais (texto vertical pequeno + furinhos). Genérico: não usa marca registrada. */
export const BordaFilme: React.FC<{ texto?: string; cor?: string; opacidade?: number }> = ({
  texto = "35MM  400  ▸ 12A",
  cor = "#e8a33c",
  opacidade = 0.55,
}) => {
  const f = useCurrentFrame();
  const lado = (esq: boolean) => (
    <div
      style={{
        position: "absolute",
        top: 0,
        bottom: 0,
        [esq ? "left" : "right"]: 14,
        width: 26,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-around",
        flexDirection: "column",
        opacity: opacidade,
      }}
    >
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          style={{
            writingMode: "vertical-rl",
            transform: esq ? "rotate(180deg)" : undefined,
            color: cor,
            fontFamily: "monospace",
            fontSize: 17,
            letterSpacing: "0.3em",
            translate: `0 ${((f * 0.6) % 40) - 20}px`,
          }}
        >
          {texto}
        </span>
      ))}
    </div>
  );
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {lado(true)}
      {lado(false)}
    </AbsoluteFill>
  );
};
