# Issues found in current implementation vs. spec.md

Verified by running `npm run build` and reading every file under `src/`. Ordered by severity.

**Status: all issues below (1–5) have been fixed.** See the "Fix applied" note under each. Issue 6 remains open — it requires real photographs, which is a content task, not a code task.

---

## Critical

### 1. `npm run build` fails — TypeScript errors block the build

`astro check` (run as part of `npm run build`) reports:

```
src/components/NotesIndexList.astro:4:17 - error ts(7006): Parameter 'note' implicitly has an 'any' type.
src/components/WorkIndexList.astro:4:38 - error ts(7006): Parameter 'work' implicitly has an 'any' type.
```

Cause: neither component declares a `Props` interface for `Astro.props`, so under `astro/tsconfigs/strict` the `.map()` callback parameter is inferred as `any`.

**Fails spec.md §14 acceptance criteria: "`astro build` succeeds."**

Fix: add typed `Props` interfaces (e.g. `import type { CollectionEntry } from 'astro:content'; interface Props { notes: CollectionEntry<'notes'>[] }`) to both components.

**Fix applied.** Both components now import `CollectionEntry` and declare `Props`. `npm run build` reports 0 errors.

---

### 2. Home page never renders the works index

`src/pages/index.astro` only renders the site title, a tagline, and Notes/About links. `WorkIndexList.astro` exists and is correctly implemented (filters by status, sorts, renders title/year/nativeTitle/deck) but is **never imported or used anywhere**.

**Fails spec.md §3.1 ("Home page") and §14 acceptance criteria item 1** ("Renders only `published`/`ongoing` works, in `order` then `year` (desc) then `title` order").

Fix: in `index.astro`, fetch the `works` collection (filter `status !== 'hidden'`, sort by `order` asc → `year` desc → `title` asc per §6.1) and render `<WorkIndexList works={works} />` above or below the identity line, per §3.1 layout.

**Fix applied.** `index.astro` now fetches and sorts the `works` collection and renders `<WorkIndexList works={works} />`. Verified the empty-state path too: with the only current work (`almost-home`) set to `status: hidden`, the Home page correctly renders no list at all (per §3.1's empty state), rather than an empty `<ul>`.

---

### 3. Image pipeline is not implemented — `ResponsiveImage.astro` bypasses Astro's image optimization entirely

```astro
const images = import.meta.glob('/src/assets/works/**/*.{jpg,jpeg,png,webp,avif}', { eager: true, import: 'default' }) as Record<string, string>;
const asset = images[`/src/assets/works/${src}`];
...
<img src={asset} ... sizes={sizes[size]} />
```

This returns a raw Vite static-asset URL and renders a single `<img src>` with a `sizes` attribute but **no `srcset`** (so `sizes` does nothing), **no `width`/`height`** attributes, and **no format conversion**.

Consequences, all violating spec.md §9 (Image Pipeline):

- No AVIF/WebP generation — only whatever format the source file already is gets served (§9.2).
- No responsive width variants — full-resolution source image served to every viewport/DPR (§9.2).
- No aspect-ratio reservation → **no CLS prevention** (§9.3) — this was also an explicit top-level requirement in `requirement.md` §22/§23.
- Source master images would be served to visitors essentially unprocessed, which `requirement.md` §22 explicitly forbids ("These master files must not be directly served to visitors").

Fix: rewrite `ResponsiveImage.astro` to use Astro's built-in `astro:assets` (`getImage` or `<Picture>`), passing the width/format matrix from spec.md §9.2, so it emits real `<picture>` markup with AVIF/WebP/JPEG sources, correct `srcset`/`sizes`, and `width`/`height` from the source file's intrinsic dimensions.

**Fix applied.** `ResponsiveImage.astro` now imports images through `import.meta.glob` as real `ImageMetadata` objects (not raw URL strings) and renders them via Astro's `<Picture>` component with `formats={['avif', 'webp', 'jpeg']}`, the exact width matrix from §9.2, `quality={82}`, and the `sizes` strings from §9.2. It also clamps the requested widths to the source image's real intrinsic width so nothing is ever upscaled (§4.4/§9.2's "never upscale" rule).

Verified end-to-end with a temporary 2400×1600 placeholder photo and one `sequence` entry (then reverted): the build generated 16 real derivative files (AVIF/WebP/JPEG × 3 widths, correctly compressed — e.g. the AVIF variants were near 0 KB, WebP 1–6 KB, JPEG 2–22 KB, versus the 22 KB source), and the emitted markup was:

```html
<picture>
  <source srcset="...avif 760w, ...avif 1140w, ...avif 1520w" type="image/avif" sizes="(max-width: 767px) 72vw, min(72vw, 760px)">
  <source srcset="...webp 760w, ...webp 1140w, ...webp 1520w" type="image/webp" sizes="...">
  <source srcset="...jpeg 760w, ...jpeg 1140w, ...jpeg 1520w" type="image/jpeg" sizes="...">
  <img src="..." srcset="..." sizes="..." alt="..." loading="eager" fetchpriority="high" decoding="async" width="2400" height="1600">
</picture>
```

`width`/`height` are present (zero CLS per §9.3), and all three formats plus responsive widths are generated per §9.2.

---

### 4. Open Graph image points to a nonexistent file

`BaseLayout.astro` sets:

```astro
<meta property="og:image" content={new URL('/og-default.svg', Astro.site)} />
```

`public/` contains only `robots.txt` — `og-default.svg` does not exist, so every page's OG image is a broken link.

Fix: add a real `public/og-default.jpg` (or `.svg`) per spec.md §11, or remove the tag until one exists.

**Fix applied.** Generated a real `public/og-default.jpg` (1200×630, site background color + site name, via `sharp`) and updated `BaseLayout.astro`'s `og:image` tag to point at it. This is a functional placeholder, not final creative — replace with a designed OG image whenever one exists.

---

## Moderate

### 5. Typography spec not implemented — Inter / Noto Sans JP are never actually loaded

`tokens.css` declares:

```css
--font-latin: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif;
--font-cjk: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', 'Microsoft YaHei', sans-serif;
```

but there is no `@font-face` declaration, no self-hosted `.woff2` file, and no font `<link>` anywhere in the project. Both named fonts are unreachable, so every browser silently falls back to the system stack.

**Fails spec.md §4.2** (self-hosted Inter + subsetted Noto Sans JP with `font-display: swap`) **and §12** (preload the above-the-fold font weights).

Fix: self-host Inter (variable, woff2) and a subsetted Noto Sans JP under e.g. `public/fonts/`, add `@font-face` rules with `font-display: swap` to `global.css`, and add `<link rel="preload" as="font">` for the regular/medium Inter weights in `BaseLayout.astro`.

**Fix applied**, using the `@fontsource-variable/inter` and `@fontsource/noto-sans-jp` npm packages instead of hand-rolled font files — these ship self-hosted, pre-subsetted `woff2` files with `font-display: swap` already set, which is equivalent to the spec's intent without maintaining font binaries by hand. `global.css` now imports `@fontsource-variable/inter/standard.css` (upright, latin/cyrillic/greek/vietnamese subsets, weights 100–900) and `@fontsource/noto-sans-jp/400.css` + `/500.css`. `tokens.css`'s `--font-latin` now names `'Inter Variable'` (the family name the package registers) as the first choice. `BaseLayout.astro` preloads the latin `woff2` file for the above-the-fold weight via a Vite `?url` import. Verified in the build output: the `dist/_astro/` folder contains the real `inter-*.woff2` files and the rendered `<head>` includes the correct `<link rel="preload" as="font" type="font/woff2" href="/_astro/inter-latin-standard-normal.[hash].woff2" crossorigin>`.

---

## Not yet verifiable

### 6. The photography layout grammar has never been exercised with real content

`src/content/works/almost-home.md` is currently:

```yaml
status: hidden
sequence: []
```

An empty, hidden stub. This means the `Sequence`/`SequenceImage`/`SequencePair`/`SequenceBreak` components — the highest-risk part of the whole spec (implementation order step 4) — have never actually been rendered against real images, so issue #3 above has not yet surfaced visually but will as soon as real content is added.

Fix: once issue #3 is fixed, add at least one real image sequence (per spec.md §6.4 example) and visually verify every `size` × `align` combination and pair stacking behavior per spec.md §14 acceptance criteria.

**Still open.** The pipeline itself is now verified (see issue #3's fix note, tested with a temporary placeholder image and then reverted), but no real photographs have been added to `almost-home.md` yet, and `align`/pair-stacking have only been checked by reading the CSS, not visually in a browser. This needs the photographer's actual images before it can be closed — it's a content task, not a code task.

---

## Confirmed correct (no action needed)

- Design tokens (`tokens.css`) match spec.md §4 values exactly (color, type scale, spacing scale, image-width tokens, breakpoints).
- `status: hidden` works are correctly excluded from `getStaticPaths` in `src/pages/works/[slug].astro` — no route is generated.
- `SequenceImage.astro` correctly forces `large`/`full` images to always render centered regardless of authored `align`, and maps `gapAfter` to the correct spacing tokens.
- `SequencePair.astro` correctly stacks pairs below `768px`, uses `--space-2xs` between stacked images, and implements `ratio` via `flex-grow`.
- `SiteHeader.astro` / `SiteFooter.astro` match spec.md §2.2 (no sticky header, no hamburger menu, footer links omitted when env vars are unset).
- Notes index/entry pages (`src/pages/notes/*`) correctly wire up the `notes` collection with status filtering and sorting.
- `astro.config.mjs` has `trailingSlash: 'always'` and the sitemap integration configured.
