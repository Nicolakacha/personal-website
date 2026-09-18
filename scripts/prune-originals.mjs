// Astro emits each imported source photo to dist/_astro at full size, next to the
// resized variants. Nothing links to them, but they would still be publicly
// served, so remove them: the widest file we ship is 1760px (see ResponsiveImage.astro).
// Originals are named `<name>.<8-char hash>.<ext>`; variants add a `_<hash>` suffix.
import { readdirSync, rmSync } from 'node:fs';

const dir = new URL('../dist/_astro/', import.meta.url);
const original = /^[A-Za-z0-9-]+\.[A-Za-z0-9_-]{8}\.(jpe?g|png)$/;
const removed = readdirSync(dir).filter((f) => original.test(f));
for (const f of removed) rmSync(new URL(f, dir));
console.log(`prune-originals: removed ${removed.length} full-size originals from dist/_astro`);
