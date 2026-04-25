import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");
const standaloneRoot = join(root, ".next", "standalone");
const standaloneNextRoot = join(standaloneRoot, ".next");
const sourceStatic = join(root, ".next", "static");
const targetStatic = join(standaloneNextRoot, "static");
const sourcePublic = join(root, "public");
const targetPublic = join(standaloneRoot, "public");

function syncDirectory(source, target) {
  if (!existsSync(source)) {
    return;
  }

  rmSync(target, { force: true, recursive: true });
  mkdirSync(target, { recursive: true });
  cpSync(source, target, { recursive: true });
}

mkdirSync(standaloneNextRoot, { recursive: true });
syncDirectory(sourceStatic, targetStatic);
syncDirectory(sourcePublic, targetPublic);
