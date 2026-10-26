import React from "react";
import { AbsoluteFill, random, useCurrentFrame } from "remotion";
import { Captions } from "./layers/Captions";
import { Pessoa } from "./layers/Pessoa";
import { Knock } from "./layers/Knock";
import { Panels } from "./layers/Panels";
import { Sound } from "./layers/Sound";
import { C } from "./theme";

/** grão de filme bem leve (muda a cada 2 frames) */
const Grain: React.FC = () => {
  const f = useCurrentFrame();
  const seed = Math.floor(f / 2);
  const x = Math.round(random(`gx${seed}`) * 160);
  const y = Math.round(random(`gy${seed}`) * 160);
  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
        opacity: 0.07,
        mixBlendMode: "overlay",
        backgroundImage:
          "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")",
        backgroundPosition: `${x}px ${y}px`,
      }}
    />
  );
};

export const Main: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.navy }}>
    <Pessoa />
    <Knock />
    <Panels />
    <Captions />
    <Grain />
    <Sound />
  </AbsoluteFill>
);
