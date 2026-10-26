// Transições que não parecem corte. As outras (câmera contínua, puxar foco, luz que varre, cobrir) saem dos blocos Camera,
// Foco, SombraJanela e Cartao com entrada; ver estilos/gramatica.md.
import React, { useId } from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

/** Chicote (whip pan): no quadro `em` a cena A sai e a B entra, com borrão de movimento só na direção do movimento. */
export const Chicote: React.FC<{
  em: number;
  dur?: number;
  direcao?: "esq" | "dir" | "cima" | "baixo";
  borrao?: number;
  a: React.ReactNode;
  b: React.ReactNode;
}> = ({ em, dur = 8, direcao = "esq", borrao = 55, a, b }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const id = "ch" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const p = interpolate(f, [em - dur / 2, em + dur / 2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.7, 0, 0.3, 1),
  });
  if (p <= 0) return <AbsoluteFill>{a}</AbsoluteFill>;
  if (p >= 1) return <AbsoluteFill>{b}</AbsoluteFill>;
  const horiz = direcao === "esq" || direcao === "dir";
  const sinal = direcao === "esq" || direcao === "cima" ? -1 : 1;
  const dist = horiz ? width : height;
  const bl = Math.sin(p * Math.PI) * borrao;
  const tr = (v: number) => (horiz ? `translateX(${v}px)` : `translateY(${v}px)`);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <svg width="0" height="0" style={{ position: "absolute" }}>
        <filter id={id} x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation={horiz ? `${bl.toFixed(1)} 0` : `0 ${bl.toFixed(1)}`} />
        </filter>
      </svg>
      <AbsoluteFill style={{ filter: `url(#${id})` }}>
        <AbsoluteFill style={{ transform: tr(sinal * p * dist) }}>{a}</AbsoluteFill>
        <AbsoluteFill style={{ transform: tr(sinal * (p - 1) * dist) }}>{b}</AbsoluteFill>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
