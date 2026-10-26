// Camada da pessoa: vídeo base + texto ATRÁS dele + recorte (fg com alfa) por cima, tudo na mesma câmera.
import React from "react";
import { AbsoluteFill, Img, interpolate, OffthreadVideo, random, Sequence, staticFile, useCurrentFrame } from "remotion";
import { fitText } from "@remotion/layout-utils";
import { CUES, Cue } from "../captions";
import { SPLIT_SHIFT, splitAt, zoomAt } from "../layout";
import { C, F, H, pop, prog, W } from "../theme";

const PRE = 6; // frames de pré-rolagem do texto atrás (sobe antes da palavra)
const BEHIND = CUES.filter((c) => c.mode === "behind");
const KNOCK = CUES.find((c) => c.mode === "knock");
const SLAM = CUES.find((c) => c.mode === "slam");

const behindWindow = (c: Cue) => ({ from: c.start - PRE, to: c.hold ?? c.end });

/** tremida de câmera (decai) */
const shake = (f: number, at: number, dur: number, amp: number) => {
  if (f < at || f > at + dur) return { x: 0, y: 0 };
  const k = 1 - (f - at) / dur;
  return { x: (random(`sx${f}`) - 0.5) * 2 * amp * k, y: (random(`sy${f}`) - 0.5) * 2 * amp * k };
};

/** quadro do recorte (PNG com alfa gerado por matte_rvm.py, nome = frame de saída): exato, sem decodificar vídeo */
const FgFrame: React.FC<{ from: number }> = ({ from }) => {
  const g = useCurrentFrame() + from;
  return (
    <Img
      src={staticFile(`fg/${String(g).padStart(5, "0")}.png`)}
      style={{ width: W, height: H, filter: "contrast(1.07) saturate(1.08) brightness(1.02)" }}
    />
  );
};

const BehindText: React.FC<{ cue: Cue }> = ({ cue }) => {
  const f = useCurrentFrame() + cue.start - PRE; // frame global
  const lines = Array.from(new Set(cue.words.map((w) => w.line)));
  const ghost = cue.fx === "ghost";
  const last = lines[lines.length - 1];
  return (
    // a cabeça começa em y≈460: o texto desce até ela pra parte de baixo das letras ficar escondida atrás
    // no fantasma o texto atravessa o rosto (aparece "através" dele quando ele some)
    <AbsoluteFill
      style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: ghost ? 640 : lines.length > 1 ? 250 : 445 }}
    >
      {lines.map((ln) => {
        const ws = cue.words.filter((w) => w.line === ln);
        const txt = ws.map((w) => w.text.replace(/[.,]$/, "")).join(" ").toUpperCase();
        const big = ln === last;
        const { fontSize } = fitText({ text: txt, withinWidth: big ? 800 : 580, fontFamily: F.display, fontWeight: 900 });
        const t0 = ws[0].start - PRE;
        const p = pop(f, t0, 30, 14, 140);
        const y = interpolate(p, [0, 1], [140, 0]);
        return (
          <div
            key={ln}
            style={{
              fontFamily: F.display,
              fontWeight: 900,
              fontSize: Math.min(fontSize, big ? 300 : 120),
              lineHeight: 0.92,
              letterSpacing: "-0.03em",
              color: big && cue.hold ? C.yellow : "#fff",
              opacity: prog(f, t0, 5),
              transform: `translateY(${y}px)`,
              textShadow: "0 6px 0 rgba(0,0,0,0.32), 0 18px 50px rgba(0,0,0,0.35)",
              filter: ghost ? `blur(${interpolate(f, [cue.start, cue.end], [0, 2], { extrapolateRight: "clamp" })}px)` : undefined,
              whiteSpace: "nowrap",
            }}
          >
            {txt}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

export const Pessoa: React.FC = () => {
  const f = useCurrentFrame();
  const z = zoomAt(f);
  const s = splitAt(f);
  const sl = SLAM ? shake(f, SLAM.start, 8, 18) : { x: 0, y: 0 };
  const knockHit = KNOCK?.words.find((w) => w.line === 1)?.start;
  const sk = knockHit != null ? shake(f, knockHit, 7, 14) : { x: 0, y: 0 };

  // fantasma no "invisível": fundo borrado/escuro, pessoa (recorte) piscando transparente
  const ghostCue = CUES.find((c) => c.fx === "ghost");
  const g = ghostCue && f >= ghostCue.start && f < ghostCue.end ? prog(f, ghostCue.start, 4) : 0;
  const ghostFlicker = g && ghostCue
    ? interpolate(f - ghostCue.start, [0, 6], [0.7, 0.12], { extrapolateRight: "clamp" }) + (random(`gf${f}`) > 0.75 ? 0.25 : 0)
    : 1;

  // preto e branco no "teu esforço morre ali" até "eu passei por isso"
  const bw = KNOCK && f >= KNOCK.start - 2 && f < KNOCK.end + 4 ? 1 : 0;
  const baseFilter = [
    "contrast(1.07) saturate(1.08) brightness(1.02)",
    g ? `blur(${14 * g}px) brightness(${1 - 0.45 * g}) saturate(${1 - 0.6 * g})` : "",
    bw ? "grayscale(1) contrast(1.25) brightness(0.85)" : "",
  ].join(" ");

  return (
    <AbsoluteFill
      style={{
        transform: `translate(${sl.x + sk.x}px, ${SPLIT_SHIFT * s + sl.y + sk.y}px) scale(${z})`,
        transformOrigin: "50% 42%",
      }}
    >
      <OffthreadVideo src={staticFile("base.mp4")} muted style={{ width: W, height: H, filter: baseFilter }} />
      {BEHIND.map((c) => {
        const { from, to } = behindWindow(c);
        return (
          <Sequence key={c.start} from={from} durationInFrames={to - from} layout="none">
            <AbsoluteFill>
              <BehindText cue={c} />
            </AbsoluteFill>
            <AbsoluteFill style={{ opacity: c.fx === "ghost" ? ghostFlicker : 1 }}>
              <FgFrame from={from} />
            </AbsoluteFill>
          </Sequence>
        );
      })}
      {/* vinheta leve no vídeo */}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 220px rgba(0,0,0,0.45)", pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
