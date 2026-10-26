// Vitrine dos blocos (sem nenhum arquivo externo). Serve de teste visual depois de mexer num bloco e de exemplo de uso para quem
// monta cena nova. 210 quadros: mural com câmera contínua → chicote → frase no escuro → faixa de cinema com máquina de escrever.
import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import { F } from "../theme";
import {
  Aberracao, Barbante, Camera, Caneta, Cartao, Chicote, Contador, Escrever, Faixa, Foco, FundoPapel, Grao, MarcaTexto,
  NoMundo, PalavrasNaFala, Pilula, SombraJanela, Vinheta, palavrasManuais,
} from "./index";

const foto = (txt: string, a: string, b: string) => (
  <div style={{ width: "100%", height: "100%", background: `linear-gradient(160deg, ${a}, ${b})`, display: "flex", alignItems: "flex-end", padding: 18, boxSizing: "border-box", color: "#fff", fontFamily: F.display, fontWeight: 800, fontSize: 34 }}>
    {txt}
  </div>
);

const Mural: React.FC = () => {
  const pinos: [number, number][] = [[700, 540], [1500, 980], [820, 1700]];
  return (
    <AbsoluteFill>
      <Camera
        largura={2400}
        altura={2600}
        poses={[
          { f: 0, x: 760, y: 820, s: 1.25, rz: -3 },
          { f: 40, x: 1500, y: 1250, s: 1.15, rz: 2 },
          { f: 80, x: 1150, y: 1450, s: 0.8, rz: 0 },
        ]}
      >
        <FundoPapel cor="#b4844f" manchas={0.45} fibra={0.3} />
        <NoMundo x={480} y={520} rot={-5}>
          <Cartao w={440} h={540} preso="alfinete" entrada={2}>{foto("FOTO 1", "#5b7aa6", "#22324a")}</Cartao>
        </NoMundo>
        <NoMundo x={1290} y={960} rot={4}>
          <Cartao w={440} h={540} preso="alfinete">{foto("FOTO 2", "#b56b45", "#4a2416")}</Cartao>
          <Caneta forma="circulo" w={380} h={360} inicio={44} dur={14} style={{ position: "absolute", left: 30, top: 50 }} />
        </NoMundo>
        <NoMundo x={600} y={1680} rot={-2}>
          <Cartao w={460} h={560} preso="alfinete">{foto("FOTO 3", "#6f8f5a", "#253318")}</Cartao>
        </NoMundo>
        <NoMundo x={1150} y={1820} rot={3} w={900}>
          <div style={{ background: "#f4f1e8", padding: "26px 34px", boxShadow: "0 10px 26px rgba(0,0,0,.35)", fontFamily: F.display, fontWeight: 900, fontSize: 92, lineHeight: 0.95, color: "#151515" }}>
            Criatividade <MarcaTexto inicio={66}>não se perde!</MarcaTexto>
          </div>
        </NoMundo>
        <Barbante pontos={pinos} inicio={10} dur={30} />
      </Camera>
      <SombraJanela forca={0.38} />
    </AbsoluteFill>
  );
};

const Escuro: React.FC = () => {
  const f = useCurrentFrame();
  const palavras = palavrasManuais([["Isso", 0.2], ["não", 0.45], ["é", 0.65], ["decoração.", 0.8], ["É", 1.4], ["ritmo.", 1.6]]);
  return (
    <AbsoluteFill style={{ background: "#070707", alignItems: "center", justifyContent: "center" }}>
      <Aberracao px={3 + (f > 48 && f < 54 ? 5 : 0)}>
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", padding: 90 }}>
          <PalavrasNaFala
            palavras={palavras}
            style={{ fontFamily: F.serif, fontStyle: "italic", fontSize: 104, color: "#bdbdbd", lineHeight: 1.05 }}
            destaque={{ ritmo: { color: "#ff2d2d", fontFamily: F.display, fontStyle: "normal", fontWeight: 800, textShadow: "0 0 18px rgba(255,45,45,.75), 0 0 44px rgba(255,45,45,.4)" } }}
          />
          <div style={{ marginTop: 70, display: "flex", gap: 18, fontFamily: F.display, fontSize: 40 }}>
            <Pilula inicio={20}>Indicação</Pilula>
            <Pilula inicio={26} cor="#d8352a" brilho>Recomendação</Pilula>
          </div>
          <div style={{ marginTop: 50, fontFamily: F.display, fontWeight: 800, fontSize: 150, color: "#f2f2f2" }}>
            <Contador de={66} ate={80} inicio={24} dur={26} sufixo="%" />
          </div>
        </AbsoluteFill>
      </Aberracao>
    </AbsoluteFill>
  );
};

const Terminal: React.FC = () => (
  <Faixa>
    <AbsoluteFill style={{ background: "#2a2c2f" }}>
      <Foco de={0} para={8} inicio={0} dur={1}>
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", fontFamily: F.display, fontWeight: 900, fontSize: 260, color: "rgba(255,255,255,.12)" }}>SYS END</AbsoluteFill>
      </Foco>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div style={{ width: 860, background: "#151617", borderRadius: 14, padding: "26px 30px", boxShadow: "0 20px 50px rgba(0,0,0,.5)", fontFamily: "monospace", fontSize: 40, color: "#e9e9e9" }}>
          {">> "}
          <Escrever texto="ninguém começa pronto." inicio={8} ate={40} cursor="bloco" />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  </Faixa>
);

export const DemoBlocos: React.FC = () => (
  <AbsoluteFill style={{ background: "#000" }}>
    <Sequence durationInFrames={150}>
      <Chicote em={100} a={<Mural />} b={<Sequence from={96}><Escuro /></Sequence>} />
    </Sequence>
    <Sequence from={150}>
      <Terminal />
    </Sequence>
    <Grao forca={0.09} />
    <Vinheta forca={0.4} />
  </AbsoluteFill>
);
