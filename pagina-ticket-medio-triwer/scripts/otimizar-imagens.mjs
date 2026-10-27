// Converte as imagens de uma pasta para WebP otimizado.
// Uso: node otimizar-imagens.mjs <pasta-origem> <pasta-destino> [largura-max=1200]
// Precisa de: npm i sharp
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";

const [, , de, para, larg = "1200"] = process.argv;
if (!de || !para) { console.log("Uso: node otimizar-imagens.mjs <origem> <destino> [largura]"); process.exit(1); }
fs.mkdirSync(para, { recursive: true });
for (const f of fs.readdirSync(de)) {
  const ext = path.extname(f).toLowerCase();
  const origem = path.join(de, f);
  if (ext === ".svg") { fs.copyFileSync(origem, path.join(para, f)); console.log(f, "(svg copiado)"); continue; }
  if (![".jpg", ".jpeg", ".png", ".webp", ".avif"].includes(ext)) continue;
  const nome = path.basename(f, ext).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-") + ".webp";
  const info = await sharp(origem).rotate().resize({ width: Number(larg), withoutEnlargement: true }).webp({ quality: 80 }).toFile(path.join(para, nome));
  console.log(nome, `${info.width}x${info.height}`, Math.round(info.size / 1024) + "KB");
}
