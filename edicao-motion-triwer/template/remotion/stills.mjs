// Renderiza vários stills com um bundle só.
// Uso: node stills.mjs <pastaSaida> <escala> [--comp P14] <frame> [frame...]
//   sem --comp: composição "Criativo" (vídeo inteiro, quadros globais)
//   com --comp: um painel isolado (quadros LOCAIS do painel) -> usado pelos subagentes de painel
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const SHARED = path.join(os.homedir(), "Developer", "video-tools", "chrome-headless-shell", "chrome-headless-shell.exe");
const browserExecutable = fs.existsSync(SHARED) ? SHARED : undefined;

const [, , outDir, scaleArg, ...rest] = process.argv;
let comp = "Criativo";
const frames = [];
for (let i = 0; i < rest.length; i++) {
  if (rest[i] === "--comp") comp = rest[++i];
  else frames.push(Number(rest[i]));
}
fs.mkdirSync(outDir, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
// porta própria: a 3000 costuma estar ocupada por outro app (dev server) e o Remotion lê a página errada
const port = Number(process.env.REMOTION_PORT || 3090);
const composition = await selectComposition({ serveUrl, id: comp, browserExecutable, port });
const prefix = comp === "Criativo" ? "m" : `${comp}_f`;
for (const f of frames) {
  await renderStill({
    serveUrl,
    composition,
    browserExecutable,
    port,
    frame: f,
    output: path.join(outDir, `${prefix}${String(f).padStart(4, "0")}.png`),
    scale: Number(scaleArg),
  });
  process.stdout.write(`${f} `);
}
console.log("ok");
