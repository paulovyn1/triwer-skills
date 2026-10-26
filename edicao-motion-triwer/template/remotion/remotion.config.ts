/**
 * Config do motor de edição. Chrome Headless Shell COMPARTILHADO (~/Developer/video-tools/chrome-headless-shell): evita baixar
 * 120 MB a cada vídeo novo. JPEG 92 nos quadros intermediários (o padrão 80 deixa blocos nos degradês escuros).
 */
import { Config } from "@remotion/cli/config";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const SHARED = path.join(os.homedir(), "Developer", "video-tools", "chrome-headless-shell", "chrome-headless-shell.exe");
if (fs.existsSync(SHARED)) Config.setBrowserExecutable(SHARED);

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(92);
Config.setOverwriteOutput(true);
Config.setDefaultPremountInSeconds(2);
