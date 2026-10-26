// Knockout: tela preta com as palavras da linha 1 do cue "knock" em letras gigantes (o vídeo aparece por dentro delas, preto e branco),
// a linha 0 vira o cabeçalho pequeno e uma linha de batimento que zera na primeira palavra grande.
// Formato do cue em captions.ts:  ["knock", "teu esforço | morre ali."]
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CUES } from "../captions";
import { C, F, pop, prog } from "../theme";

const K = CUES.find((c) => c.mode === "knock");
const HEAD = K ? K.words.filter((w) => w.line === 0) : [];
const BIG = K ? K.words.filter((w) => w.line >= 1) : [];
const HIT = BIG[0]?.start ?? 0;
const OUT = K ? K.end - 8 : 0;

const ecgY = (x: number, phase: number, amp: number) => {
  // batimento PQRST repetindo a cada 360 px
  const u = (((x + phase) % 360) + 360) % 360;
  let v = 0;
  if (u > 40 && u < 70) v = -14 * Math.sin(((u - 40) / 30) * Math.PI);
  else if (u > 95 && u < 105) v = 18 * ((u - 95) / 10);
  else if (u >= 105 && u < 118) v = 18 - 150 * ((u - 105) / 13);
  else if (u >= 118 && u < 132) v = -132 + 172 * ((u - 118) / 14);
  else if (u >= 132 && u < 142) v = 40 - 40 * ((u - 132) / 10);
  else if (u > 180 && u < 230) v = -26 * Math.sin(((u - 180) / 50) * Math.PI);
  return v * amp;
};

const strip = (t: string) => t.replace(/[.,]$/, "");

export const Knock: React.FC = () => {
  const f = useCurrentFrame();
  if (!K || f < K.start - 1 || f >= K.end) return null;
  const black = f >= HIT - 1 ? interpolate(f, [OUT, K.end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const amp = interpolate(f, [HIT - 3, HIT + 2], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const phase = (f - K.start) * 26;
  const head = interpolate(f, [K.start, HIT], [140, 940], { extrapolateRight: "clamp" });
  const pts: string[] = [];
  for (let x = 0; x <= 1080; x += 4) {
    const visible = f < HIT ? x <= head : true;
    if (visible) pts.push(`${x},${ecgY(x, phase, x > head - 2 && f < HIT ? 1 : amp)}`);
  }
  const lineColor = f < HIT ? C.red : "#ffffff";
  const fadeTop = interpolate(f, [OUT, K.end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const lineIds = [...new Set(BIG.map((w) => w.line))];
  // várias linhas no roteiro ("sem gastar | um centavo | a mais.") = uma fileira por linha; uma linha só = comportamento antigo (palavras empilhadas)
  const rows = lineIds.length > 1 ? lineIds.map((l) => BIG.filter((w) => w.line === l)) : BIG.length > 2 ? [BIG.slice(0, BIG.length - 1), BIG.slice(-1)] : BIG.map((w) => [w]);
  const rowText = (r: typeof BIG) => r.map((w) => strip(w.text)).join(" ");
  const rowSize = (r: typeof BIG) => Math.min(268, Math.floor((1000 / rowText(r).length) * 1.55));
  const size = lineIds.length > 1 ? 0 : Math.min(268, Math.floor(1000 / Math.max(...rows.map((r) => rowText(r).length)) * 1.55));
  return (
    <>
      {black > 0 && (
        <AbsoluteFill
          style={{ background: `rgba(0,0,0,${black})`, mixBlendMode: "multiply", alignItems: "center", justifyContent: "center", paddingBottom: 60 }}
        >
          <div
            style={{
              fontFamily: F.display, fontWeight: 900, fontSize: size, lineHeight: 0.84, letterSpacing: "-0.04em",
              color: "#fff", textAlign: "center", transform: "scaleY(1.22)",
            }}
          >
            {rows.map((r, i) => {
              const start = r[0].start;
              const p = pop(f, start - 2, 30, 13, 200);
              return (
                <div
                  key={i}
                  style={{
                    ...(size === 0 ? { fontSize: rowSize(r) } : {}),
                    transform: `scale(${interpolate(p, [0, 1], [1.6, 1])})`,
                    opacity: f >= start - 2 ? Math.min(1, p * 2) : 0,
                  }}
                >
                  {r.map((w) => strip(w.text)).join(" ").toUpperCase() + (i === rows.length - 1 ? "." : "")}
                </div>
              );
            })}
          </div>
        </AbsoluteFill>
      )}
      <AbsoluteFill style={{ opacity: fadeTop }}>
        <div
          style={{
            position: "absolute", top: 330, width: "100%", textAlign: "center", fontFamily: F.display, fontWeight: 800,
            fontSize: 74, letterSpacing: "0.02em", color: "#fff", textShadow: "0 6px 26px rgba(0,0,0,0.6)", opacity: prog(f, K.start - 1, 5),
          }}
        >
          {HEAD.slice(0, -1).map((w) => strip(w.text).toUpperCase()).join(" ")}{" "}
          <span style={{ fontFamily: F.serif, fontStyle: "italic", fontWeight: 400, fontSize: 104, color: C.yellow }}>
            {strip(HEAD[HEAD.length - 1]?.text ?? "")}
          </span>
        </div>
        <svg width={1080} height={300} style={{ position: "absolute", top: 1320 }} viewBox="0 -150 1080 300">
          <polyline
            points={pts.join(" ")} fill="none" stroke={lineColor} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round"
            style={{ filter: `drop-shadow(0 0 12px ${lineColor})` }}
          />
          {f < HIT && <circle cx={head} cy={ecgY(head, phase, 1)} r={10} fill="#fff" />}
        </svg>
      </AbsoluteFill>
    </>
  );
};
