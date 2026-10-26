// Luz e profundidade: sombra de janela varrendo, desfoque animado (puxar foco), aberração cromática.
import React, { useId } from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

/** Sombra de janela/persiana varrendo a cena (luz natural). Multiplica o que está atrás; pôr DEPOIS do conteúdo.
 *  forca 0..1, angulo em graus, velocidade em px/quadro, quente = leve luz alaranjada nas faixas claras. */
export const SombraJanela: React.FC<{ forca?: number; angulo?: number; velocidade?: number; largura?: number; quente?: boolean }> = ({
  forca = 0.42,
  angulo = -28,
  velocidade = 1.1,
  largura = 170,
  quente = true,
}) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const periodo = largura * 3.4;
  const desloc = (f * velocidade) % periodo;
  const s = `rgba(0,0,0,${forca})`;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", overflow: "hidden", mixBlendMode: "multiply" }}>
      {/* luz quente embaixo (branco = neutro no multiply), faixas de sombra por cima */}
      {quente && <AbsoluteFill style={{ background: "linear-gradient(115deg, rgba(255,214,170,1), rgba(255,255,255,1) 65%)" }} />}
      <div
        style={{
          position: "absolute",
          left: -width,
          top: -height,
          width: width * 3,
          height: height * 3,
          transform: `rotate(${angulo}deg) translateX(${desloc}px)`,
          background: `repeating-linear-gradient(90deg, ${s} 0px, ${s} ${largura}px, rgba(0,0,0,0) ${largura * 1.6}px, rgba(0,0,0,0) ${periodo - largura * 0.6}px, ${s} ${periodo}px)`,
          filter: "blur(26px)",
        }}
      />
    </AbsoluteFill>
  );
};

/** Desfoque animado entre dois valores (px), de `inicio` a `inicio + dur` (quadros locais). Use para puxar foco entre camadas. */
export const Foco: React.FC<{
  de?: number;
  para?: number;
  inicio?: number;
  dur?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ de = 16, para = 0, inicio = 0, dur = 12, children, style }) => {
  const f = useCurrentFrame();
  const b = interpolate(f, [inicio, inicio + dur], [de, para], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });
  return <AbsoluteFill style={{ filter: b > 0.15 ? `blur(${b.toFixed(2)}px)` : undefined, ...style }}>{children}</AbsoluteFill>;
};

/** Aberração cromática: separa vermelho e azul em `px` para os lados (filtro SVG, uma renderização só).
 *  Usar em trechos curtos ou com px pequeno (2-4); px pode variar por quadro (ex.: pulso no golpe). */
export const Aberracao: React.FC<{ px?: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ px = 3, children, style }) => {
  const id = "ab" + useId().replace(/[^a-zA-Z0-9]/g, "");
  return (
    <AbsoluteFill style={style}>
      <svg width="0" height="0" style={{ position: "absolute" }}>
        <filter id={id} x="-2%" y="-2%" width="104%" height="104%" colorInterpolationFilters="sRGB">
          <feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
          <feOffset in="r" dx={px} dy="0" result="r2" />
          <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g" />
          <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b" />
          <feOffset in="b" dx={-px} dy="0" result="b2" />
          <feBlend in="r2" in2="g" mode="screen" result="rg" />
          <feBlend in="rg" in2="b2" mode="screen" />
        </filter>
      </svg>
      <AbsoluteFill style={{ filter: `url(#${id})` }}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};
