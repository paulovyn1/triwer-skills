import React from "react";
import { Composition } from "remotion";
import { Main } from "./Main";
import { DemoBlocos } from "./blocos/Demo";
import { PANELS, TOTAL } from "./timeline";
import { H, PANEL_H, W } from "./theme";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Criativo" component={Main} durationInFrames={TOTAL} fps={30} width={W} height={H} />
      {/* vitrine dos blocos dos estilos (teste visual: node stills.mjs <saida> 0.4 --comp DemoBlocos 0 30 60 ...) */}
      <Composition id="DemoBlocos" component={DemoBlocos} durationInFrames={210} fps={30} width={W} height={H} />
      {/* cada painel isolado, pra testar com `npx remotion still Pxx` */}
      {PANELS.map((p) => (
        <Composition
          key={p.id}
          id={p.id}
          component={p.C}
          durationInFrames={p.to - p.from}
          fps={30}
          width={W}
          height={p.kind === "top" ? PANEL_H : H}
        />
      ))}
    </>
  );
};
