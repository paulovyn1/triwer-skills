// Tira prints da página rolando de cima a baixo, em desktop e celular.
// Uso: node prints.mjs <url> <pasta-saida> [caminho-do-chrome]
// Precisa de: npm i puppeteer-core  (e Chrome ou Edge instalado)
import puppeteer from "puppeteer-core";
import fs from "node:fs";

const [, , url, out, chromeArg] = process.argv;
if (!url || !out) { console.log("Uso: node prints.mjs <url> <pasta-saida> [chrome]"); process.exit(1); }
const candidatos = [chromeArg,
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome", "/usr/bin/chromium"].filter(Boolean);
const chrome = candidatos.find((c) => fs.existsSync(c));
if (!chrome) { console.log("Chrome não encontrado. Passe o caminho como 3º argumento."); process.exit(1); }

const telas = [["desktop", 1440, 900], ["cel412", 412, 915], ["cel360", 360, 780]];
const b = await puppeteer.launch({ executablePath: chrome, headless: true, args: ["--hide-scrollbars"] });
for (const [nome, w, h] of telas) {
  const dir = `${out}/${nome}`; fs.mkdirSync(dir, { recursive: true });
  const p = await b.newPage(); await p.setViewport({ width: w, height: h });
  const erros = []; p.on("pageerror", (e) => erros.push(e.message));
  await p.goto(url, { waitUntil: "networkidle0" });
  await new Promise((r) => setTimeout(r, 2600));
  const total = await p.evaluate(() => document.documentElement.scrollHeight);
  let i = 0;
  for (let y = 0; y < total; y += h) {
    await p.evaluate((y) => scrollTo(0, y), y);
    await new Promise((r) => setTimeout(r, 2200)); // espera as animações de entrada terminarem
    await p.screenshot({ path: `${dir}/${String(++i).padStart(2, "0")}.png` });
  }
  const estouro = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  console.log(`${nome}: ${i} prints${estouro ? " | ATENÇÃO: rolagem horizontal" : ""}${erros.length ? " | erros: " + erros.join("; ") : ""}`);
  await p.close();
}
await b.close();
