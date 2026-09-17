# Photography Website — Implementation Specification

Source: `requirement.md`. This document translates that source of truth into a concrete, implementation-ready specification for Codex. Where the source document expressed an intention without a concrete value, a decision has been made below and is stated as fact, not as a suggestion.

Priority order governing every decision and every future tradeoff Codex must make:

1. Integrity of photographic presentation
2. Authored sequence and rhythm
3. Visual restraint
4. Readability and usability
5. Image quality
6. Performance
7. Maintainability
8. Implementation convenience
9. Additional features

---

## 1. Product Definition

A personal photography website for Nicolas Tei, structured like a small independently published photo-book rather than a portfolio product. It exists to present sequences of photographs with authored scale, pairing, alignment and rhythm — not to sell services, not to replicate a social feed, and not to demonstrate frontend craft.

The site is statically generated, has no backend, no database, no CMS, no auth, and no client-side framework runtime beyond what the browser gives for free (native scroll, native links, `<img>`/`<picture>`). Almost all visual character comes from typography, spacing, image scale and sequencing — not from decoration, animation, or UI chrome.

Non-goals are enumerated in full in §17.

### 1.1 Why Astro, not React/Next.js

Astro is a static-site framework built around shipping zero JavaScript by default: every `.astro` component renders to plain HTML/CSS at build time, and Astro's Content Collections give schema-validated (Zod) Markdown/MDX content out of the box — a good fit for this site's Markdown-authored works and notes (§6).

React (or Next.js) is not required here because:

- Nothing on this site needs client-side state or interactivity — no lightbox, no animation, no forms (§13 Non-Goals). React's value is managing interactive state; there is none to manage.
- The source document explicitly says "React is not required" and "use JavaScript only where it produces meaningful functionality" (requirement.md §25/§23).
- Shipping a React runtime would add bundle size and build complexity with no corresponding feature benefit, working against the requirement priority order's ranking of restraint and performance above implementation convenience.

If a genuinely interactive widget is needed later, Astro's islands architecture allows a single React (or other framework) component to be hydrated in isolation via `client:visible`/`client:load` without adopting a framework for the rest of the site — this does not need to be decided now.

---

## 2. Information Architecture

### 2.1 Routes

```
/                       Home (index of works + entry points to Found/Notes/About)
/works/[slug]/          Individual work page (e.g. /works/almost-home/)
/found/                 Found index (list of found-photograph pieces)
/found/[slug]/          Individual found piece (same sequence grammar as a work)
/notes/                 Notes index
/notes/[slug]/          Individual note
/about/                 About page
/sitemap-index.xml      Generated sitemap
```

There is no separate `/works/` index route distinct from Home. Home *is* the works index (see §3 — `Works` and `Home` are merged per the source document's explicit permission to simplify when they overlap).

`Found` is deliberately **not** merged into Home/works the same way: it is a distinct content collection (§6.1a) with its own index route and its own header nav entry, because found/appropriated photographs are conceptually different from authored works (not made by the photographer) and the photographer wants them kept in a visibly separate section rather than interleaved in the main work index.

### 2.2 Navigation

Global navigation, present in a `<header>` on every page, minimal and non-sticky by default:

```
Nicolas Tei     Found   Notes   About
```

- "Nicolas Tei" (site title) links to `/`, set at `--font-size-index`, weight 500 — the one place in the header with any visual weight.
- `Found`, `Notes` and `About` are plain text links, right- or right-of-title aligned, set at `--font-size-small` in `--color-muted` (not `--color-fg`), brightening to `--color-fg` on hover/focus. This deliberately makes the header read as quiet utility chrome rather than competing with a page's own content — most visibly on Home, where the work index (in full `--color-fg`) is the page's real navigational moment (§3.1).
- Each nav link (including the site title) sets `aria-current="page"` when it matches (or, for `Found`/`Notes`, prefixes) the current path — a small accessibility affordance not in the original source document, added because it's essentially free and helps screen-reader/keyboard users confirm where they are without changing the visual design (no visual style is defined for `aria-current` beyond the default browser/AT behavior).
- A hairline `border-bottom: 1px solid var(--color-border)` under the header (mirrored by a `border-top` above the footer) frames the page content — a restrained structural device, not a decorative box.
- No hamburger menu at any breakpoint. At the narrowest viewport the header wraps to two lines if needed (title on line 1, links on line 2) rather than collapsing into a menu.
- The header is `position: static` (scrolls away with content). It does not re-appear as a sticky bar. This is a deliberate rejection of "persistent UI occupying visual space" (source §8, §20).
- Within a work page, there is no secondary in-page navigation, no progress indicator, and no thumbnail rail. The only way to leave a work is the browser back action or the header links.
- A minimal footer appears at the bottom of every page: a `© {current year} Nicolas Tei. All rights reserved.` copyright line (year computed at build time, not hardcoded per year), followed by Instagram link and email link — in `--color-muted`, brightening to `--color-fg` on hover/focus for the links (the copyright text itself is not a link and never brightens). It does **not** repeat the site name as a heading — the header already shows it (and Home's own `<h1>` shows it again as its title-page moment); the copyright line is a legal notice, not a redundant name repetition, so this is not a violation of that rule. Instagram/email URLs are hardcoded directly in `SiteFooter.astro` (not environment variables — deliberately simple for a single-maintainer site with no per-environment variation). The footer always renders (the copyright line alone is sufficient content); Instagram/email links within it are still individually omitted if not set. No sitemap-style footer link farm.

### 2.3 URL structure rules

- Slugs are lowercase, hyphenated, ASCII (e.g. `almost-home`, `residents`).
- Work and note slugs are permanent; do not reuse a slug for different content once published.
- Trailing slash on all content routes (Astro default `trailingSlash: 'always'`).

---

## 3. Page Specifications

### 3.1 Home (`/`)

**Content**

A quiet textual index, in authored order (not auto-sorted by date), of all `published` and `ongoing` works. Structure:

```
Almost home                          2026
Residents                      2026 · 住民
Photographs                          2026
```

Home does **not** display the site name as a visible heading, and does not repeat `Notes`/`About` either — both are earlier drafts of this spec that were removed as redundant:

- The site name already appears once, visibly, in the header (§2.2) on every page including Home — the photographer wants their name on-page only there and on About, not a third time as a Home title. Home's `<h1>` still exists for document structure but is visually hidden (§10 Accessibility) — its text is a plain structural label, not the name.
- `Notes` and `About` links already exist in that same persistent header on every page, so a second copy at the bottom of Home would duplicate them rather than add information.

- Each work title is a link to its work page. Year sits at the trailing edge of the same line, in `--color-muted` (desktop); stacks beneath the title only if it doesn't fit on mobile (see mobile behaviour below).
- A work's native-script subtitle (e.g. 住民 for Residents), if present in frontmatter, is shown after the year on the same muted line, separated by " · ".
- Hidden/draft works are excluded entirely from this list (not shown greyed-out, not shown with a "coming soon" label — see §16 Project status).
- No thumbnails, no hover-preview images, no descriptions on this index by default. A work MAY optionally carry a one-line `deck` (short description) in frontmatter; if present, it renders as a small muted line beneath the title, wrapped to the text column width. Most works will omit it.

**Desktop layout**

- Single column, left-aligned, sitting inside the standard text column (`--width-text`, see §7.6), vertically centered-ish in the viewport but not forced — content starts at a fixed top offset (`--space-xl`) from the top of the viewport, not vertically centered with flexbox (avoids awkward reflow / avoids look of a "landing hero").
- No image on the homepage in v1. The source document permits small photographic cues "if it meaningfully improves the experience" — the deliberate choice here is to omit them for v1 to keep the page unambiguous and fast to build; this can be revisited later without architecture changes (a single optional `coverImage` field can be added to the work schema later, see §10.7 extension note).

**Mobile behaviour**

- Same structure, single column. Year moves to a second line under the title only if the title + year cannot fit on one line at `--font-size-body`; implement this with plain flex-wrap, not a JS breakpoint check.
- Top offset reduces to `--space-lg`.

**Interaction**

- Standard link hover/focus states (§7.8). No hover-triggered previews. No animation on load.

**Empty / edge states**

- If zero works are published (all draft/hidden), the works list section is omitted entirely and only the identity line remains (the header's Notes/About links are still present, as on every page). Never render an empty list, an empty heading, or a "no works yet" message.

---

### 3.2 Work page (`/works/[slug]/`)

This is the primary page type and the one that must be built most carefully; see §8 for the full photography layout grammar it renders.

**Content**

- Work title (native script subtitle inline or beneath, if present).
- Year or year range.
- Optional short description (`description` field), rendered once, near the top, in the text column width — never repeated per image.
- The authored `sequence`: an ordered list of blocks (`image`, `pair`, `break`) rendered top to bottom exactly in the order authored. See §9 (content schema) and §8 (layout grammar).
- No per-image captions by default (source §19). A block MAY carry an optional `caption`, rendered as small muted text directly beneath that specific image/pair only when explicitly authored — never auto-generated from filename.

**Desktop behaviour**

- Vertical scroll is the only navigation mechanic.
- Each block renders per its own `size`, `align`, and `gapAfter` — see §8.
- Images reserve their aspect ratio (via explicit `width`/`height` on the generated `<img>`, or CSS `aspect-ratio` from stored metadata) so nothing shifts on load.
- First 1–2 images in the sequence load eagerly (`loading="eager"`, `fetchpriority="high"` on the very first); everything after loads `loading="lazy"`.

**Mobile behaviour**

- Same sequence, same order. `align` values collapse toward center (see §8.3). `pair` blocks stack vertically (see §8.4) unless viewport is wide enough (≥ tablet breakpoint) to keep them side by side. `size` values scale down proportionally but a `small` image never becomes edge-to-edge — see §7 image width table.

**Interaction**

- No lightbox by default (source §20 explicit default). No zoom. No swipe gallery. Standalone `<img>` in normal document flow.
- No scroll-triggered animation of any kind. Images are simply present when scrolled to.

**Empty / edge states**

- A work with an empty `sequence` (e.g. announced but not yet populated) still renders title/year/description; the sequence area is simply absent. This supports "ongoing" works that exist as a placeholder entry before photographs are added — but note such a work should generally be `status: hidden` until it has at least one image, per §16.
- A work `status: hidden` is not built into a route at all in production (see §16), so there is no "this page doesn't exist" state to design for a hidden work — it simply isn't generated.

---

### 3.3 Notes index (`/notes/`)

**Content**

A reverse-chronological plain list of notes: title (or, if untitled, a truncated first line / the date alone acts as the link label), date, nothing else. No excerpts, no reading time, no tags, no pagination controls beyond simple "older" if the list ever gets long (see below).

```
2026-03-02   On the weight of a print
2026-02-14   —
2026-01-30   Two photographs of the same door
```

- An untitled note (`title` omitted) shows an em dash or the note's date-only as the link label — never a slug, never "Untitled".
- If the number of notes exceeds ~40, paginate with simple prev/next text links at the bottom (`Older`) rather than infinite scroll or numbered pages. This is an intentionally cheap mechanism, acceptable because Notes is not the primary content type.

**Desktop / mobile**

- Single column, same text width as Home. Date in `--color-muted`, monospaced-adjacent tabular alignment via CSS `font-variant-numeric: tabular-nums`, not literal `<table>`.

**Interaction / empty state**

- If there are zero notes, the Notes index still exists but the page shows only the page heading and no list (not a "coming soon" message). `/notes/` should not 404 even with zero entries.

---

### 3.4 Note (`/notes/[slug]/`)

**Content**

- Optional title.
- Date.
- Body text (Markdown/MDX), which may be as short as one sentence.
- Optional images, embedded inline in the body at the author's chosen point, rendered at `medium` size by default (a note is not a photographic work — it does not need the full layout grammar of §8, just an optional single image or two, block-centered).

**Layout**

- Body copy constrained to `--width-text` (see §7.6), left-aligned, using the body type scale (§7.4).
- A short (one- to three-sentence) note must not display awkwardly — no minimum height, no forced "read more," no card border. It simply ends where the text ends, followed by normal spacing to the footer or the "back to notes" implicit navigation (browser back / header link).

**Interaction / empty / edge states**

- No comments, no share buttons, no related-notes block, no author card (source §17 explicit).

---

### 3.5 About (`/about/`)

**Content** (structure, not final copy):

```
Nicolas Tei
Based in Japan.

[short intro paragraph — optional, plain text]

Instagram
Email
```

**Layout**

- Same text column width as Notes body. Left-aligned static content, no photograph required.
- The schema (§6.3) must allow later, low-effort addition of an `Exhibitions`, `Publications`, or `Selected projects` block as further paragraphs/lists in the same page without restructuring — implement About as a single Markdown/MDX content file (not fully hardcoded in a template) precisely so this is a content edit, not a code change.

**Interaction / empty / edge states**

- None beyond standard link states. If Instagram/email are not yet set, omit those lines rather than showing empty links.

---

### 3.6 Found index (`/found/`) and Found piece (`/found/[slug]/`)

Added after v1: a section for photographs the photographer found or was given rather than made themselves (old prints, someone else's negatives, images "found" in the colloquial photo-book sense) — distinct enough in authorship/intent from `works` that it gets its own content collection and route tree instead of being folded into the works index.

**`/found/` index — content and layout**

- Structurally identical to Home's work index (§3.1): a plain list of `title`, `year` (trailing edge, `--color-muted`), optional `nativeTitle` after the year, optional one-line `deck` beneath the title. `status: hidden` entries are excluded entirely.
- Unlike Home, this index has a visible `<h1>Found</h1>` (Home's own `<h1>` is visually hidden per §10 — Found's is not, since nothing else on this page needs to be the visual anchor the way Home's index does).
- Sort order: `order` ascending, then `year` descending, then `title` alphabetical — same rule as Home (§6.1).
- Empty state: if zero found pieces are published, the index still renders (heading only), same non-404 rule as Notes (§3.3).

**`/found/[slug]/` piece — content and layout**

- Renders with the exact same photography layout grammar as a work page (§5): `sequence` of `image`/`pair`/`break` blocks, same size/align/gapAfter vocabulary, same no-lightbox/no-animation interaction rules (§3.2).
- Title, optional `nativeTitle`, year, optional `description` render the same way as a work page's intro block.
- The one schema difference from `works` is an optional `provenance` field (§6.1a) — a short plain-text line (e.g. "Found in a secondhand shop, Ōsaka, 2025.") rendered as a second muted line beneath the description, in the same `.meta` treatment as the year line. This is the one place the site records how an image came to the photographer rather than what it depicts — deliberately kept to plain text, not a structured citation format.
- Assets live under `src/assets/found/[slug]/` (parallel to `src/assets/works/[slug]/`, §8), kept in a separate top-level asset folder so found-photograph masters are never intermixed with the photographer's own authored work in the repo.

---

## 4. Design System

### 4.1 Color

Dark is the site's only theme — no light variant, no toggle, no `prefers-color-scheme` handling. This is a deliberate choice (revising an earlier draft of this spec that considered a toggle): one considered palette, not a switch.

```css
:root {
  --color-bg:     #1B1917;  /* warm near-black, not pure #000 — avoids OLED-crush around photographs */
  --color-fg:     #EDEAE3;  /* warm off-white, not pure #FFF — avoids glare */
  --color-muted:  #8C867B;  /* muted warm grey for metadata/secondary text — verified ≥4.5:1 on --color-bg */
  --color-border: #33302B;  /* hairline rules only, used sparingly (e.g. footer separator) */
  --color-link:   #EDEAE3;  /* links are the same colour as body text, underlined — no blue */
  --color-focus:  #EDEAE3;  /* focus ring colour */
}
```

Rationale for concrete values: the warmth is a very slight, deliberately subtle shift off neutral gray (not a "cream," "sepia," or blue-black tone) so it reads as considered rather than mechanically "artistic" or "techy." The background is verified to keep image colour perception neutral (low saturation, no visible colour cast), and `--color-muted` is verified to clear WCAG AA's 4.5:1 contrast ratio against `--color-bg` — re-verify if either hex value is ever adjusted.

### 4.2 Typography

**Font stacks**

```css
--font-latin: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif;
--font-cjk:   'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', 'Microsoft YaHei', sans-serif;
--font-body:  var(--font-latin), var(--font-cjk);
```

- One typographic family in spirit: a single quiet, low-personality grotesk sans (Inter) for Latin text, paired with Noto Sans JP for Japanese/Chinese glyphs, since no single font covers both scripts well. Both are neutral, similar in weight/x-height, and neither carries a strong stylistic signature — this satisfies source §7's "one family or a carefully selected Latin + Japanese combination."
- Self-host Inter (variable font, woff2) and subset Noto Sans JP to reduce weight (see §11 performance) — do not load full Noto Sans JP (~15MB before subsetting) unless subsetting is set up.
- No serif, no display face, no second "accent" typeface anywhere in the system.
- Font weights used: 400 (body/regular), 500 (titles, nav — a single medium weight for emphasis). Do not introduce 600/700/800 weights; emphasis is achieved via size and spacing, not boldness.

**Type scale** (fluid, `clamp()`-based, so it needs no discrete breakpoint switches):

```css
--font-size-body:     clamp(1.05rem, 1rem + 0.25vw, 1.15rem);    /* 16.8–18.4px */
--font-size-small:    clamp(0.85rem, 0.83rem + 0.1vw, 0.9rem);   /* 13.6–14.4px, metadata/dates/captions */
--font-size-title:    clamp(1.4rem, 1.2rem + 1.1vw, 2.05rem);    /* work/page titles */
--font-size-index:    clamp(1.15rem, 1.08rem + 0.45vw, 1.35rem); /* home index work titles, site title */

--line-height-body:   1.65;
--line-height-title:  1.3;
--line-height-small:  1.5;

--letter-spacing-title: -0.01em;  /* h1/site-title only — a hair tighter at larger sizes */
--letter-spacing-caps: 0.02em;  /* used only if any all-caps label is ever introduced; none exist in v1 */
```

**Heading hierarchy**

- `h1`: page/work title — one per page, uses `--font-size-title`, weight 500.
- `h2`: used only for section breaks inside long Notes/About content, not inside work pages (work pages have no headings inside the sequence — headings would fight the photographs).
- No `h3`+ needed in v1 content.

**Caption / metadata styling**

- Year, dates, muted secondary lines: `--font-size-small`, `--color-muted`, `line-height: var(--line-height-small)`, `font-variant-numeric: tabular-nums` for dates.
- Image captions (when authored): `--font-size-small`, `--color-muted`, `margin-top: var(--space-2xs)` (see §4.3), max-width equal to the image's own rendered width (caption never wider than the photograph it describes).

**Text width**

```css
--width-text: 38rem;     /* ~608px at 16px root — body copy, About, Notes */
--width-index: 34rem;    /* Home / Notes index column */
--width-content: 1400px; /* outer bound for work-page image column, see §7.6 */
```

**Mobile typography behaviour**

- Root font-size stays at browser default (16px); the `clamp()` values above already flatten to their lower bound below ~420px viewport width, so no separate mobile override rules are needed.
- `--width-text` becomes `100% - (2 × var(--space-sm))` below the tablet breakpoint (i.e., fluid, bounded by the viewport minus side padding, not a fixed rem value that could overflow).

### 4.3 Spacing scale

Fluid tokens, all `clamp()`-based so they respond to viewport without discrete breakpoint jumps, per source §15/§30:

```css
--space-3xs: clamp(0.25rem, 0.2rem + 0.2vw, 0.375rem);   /* 4–6px */
--space-2xs: clamp(0.5rem,  0.45rem + 0.3vw, 0.75rem);   /* 8–12px */
--space-xs:  clamp(0.75rem, 0.6rem + 0.6vw, 1rem);        /* 12–16px */
--space-sm:  clamp(1rem,    0.8rem + 1vw, 1.5rem);        /* 16–24px */
--space-md:  clamp(1.5rem,  1rem + 2vw, 2.5rem);          /* 24–40px */
--space-lg:  clamp(3rem,    2rem + 4vw, 5rem);            /* 48–80px */
--space-xl:  clamp(5rem,    3rem + 8vw, 8.75rem);         /* 80–140px */
--space-pause: clamp(8.75rem, 6rem + 10vw, 15rem);        /* 140–240px */
```

Semantic mapping used by the layout grammar (§8):

| Semantic gap | Token |
|---|---|
| `tight` | `--space-sm` |
| `normal` | `--space-lg` |
| `large` | `--space-xl` |
| `pause` | `--space-pause` |

Default `gapAfter` when unspecified on a sequence block: `normal`.

### 4.4 Image width tokens

Semantic sizes map to a **max-width as a fraction of `--width-content`**, capped in absolute pixels so images never grow unboundedly on very wide monitors (source §31):

```css
--image-small-max:  min(52vw, 480px);
--image-medium-max: min(72vw, 760px);
--image-large-max:  min(92vw, 1040px);
--image-full-max:   min(96vw, 1280px);
```

- These are *max-widths*; actual rendered width is `min(max-width, intrinsic-width)` — a small-resolution source image never gets upscaled past its native size.
- All four sizes are always centered within `--width-content` by default; `align` (§8.3) offsets `small`/`medium` images only, per the alignment rules below.
- At mobile widths (< tablet breakpoint), every size token's `vw` component naturally shrinks the image, but `small` still remains visibly smaller than `medium`/`large` (never force `small` to become the full viewport width — source §16 explicit constraint). Minimum enforced: `small` is capped at `80vw` on mobile via a breakpoint override, not `100vw`.

### 4.5 Breakpoints

```css
--bp-small-mobile: 420px;
--bp-tablet:       768px;
--bp-desktop:      1080px;
--bp-wide:         1440px;
```

Used only where the photographic composition genuinely needs to change (pair stacking, alignment collapsing, side padding) — not for a generic 12-column grid system that doesn't exist in this design.

### 4.6 Links, hover, focus (see also §12)

Two link contexts, two treatments — both share the same ink color (`--color-link`) and never change hue on hover/visited (source §6, §20: subtle hover states acceptable, no hover distortion):

**Standalone links** (nav, footer, index-list titles — a link that is the only text in its row/element, not embedded in a sentence):

```css
a { color: var(--color-link); text-decoration: none; }
a:hover, a:focus-visible { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.2em; }
a:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
```

No permanent underline: each of these links is already unambiguous from its position (one link per list row, per nav item), so a hover/focus-only underline is sufficient affordance without the visual clutter of underlining every navigational element on the page.

**Inline (prose) links** — inside About/Notes body text, where a link sits next to plain text of the same color and needs a permanent, position-independent cue to read as a link:

```css
.prose a { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.2em; }
.prose a:hover { text-decoration-thickness: 1.5px; }
```

---

## 5. Photography Layout Grammar

This is the core editorial vocabulary. It is deliberately small: three block types, three sizes, four alignments, four gap levels. Codex must not add block types beyond what's here without a content-model reason (source §26: "avoid becoming a miniature page builder").

### 5.1 Block types

**`image`** — a single photograph.

```yaml
type: image
src: string          # required, path relative to the work's asset folder
size: small | medium | large | full     # default: large
align: left | center | right            # default: center
gapAfter: tight | normal | large | pause  # default: normal
caption: string      # optional
alt: string          # required unless decorative: true (see §12.4)
decorative: boolean  # optional, default false
```

**`pair`** — two photographs presented as a single deliberate unit.

```yaml
type: pair
images:
  - src: string
    alt: string
    decorative: boolean   # optional
  - src: string
    alt: string
    decorative: boolean   # optional
size: small | medium | large           # default: medium (a pair does not support `full` — two full-width images side by side would exceed the intent of "full")
ratio: equal | left-heavy | right-heavy  # default: equal
gapAfter: tight | normal | large | pause  # default: normal
caption: string       # optional, applies to the pair as a whole
```

**`break`** — an explicit structural pause with no image, for sections that need a beat larger than any single `gapAfter` value, or to separate named sub-sections within one long work.

```yaml
type: break
size: large | pause     # default: pause
```

### 5.2 Sizing rules

- `size` on `image` maps directly to the width tokens in §4.4.
- `size` on `pair` sets the **combined** width envelope (§5.4) — each individual image within the pair is narrower than that envelope, not equal to it.
- There is no per-image arbitrary pixel width in content data. This is intentional: it prevents content authors (or Codex, generating content) from silently reintroducing arbitrary layout, keeping the vocabulary closed per source §11/§26.

### 5.3 Alignment rules (desktop / ≥ `--bp-desktop`)

Alignment only applies to `small` and `medium` single images (a `large`/`full` image is wide enough that meaningful left/right offset would look accidental rather than deliberate, so those two sizes always render `center` regardless of the authored `align` value — this is an enforced rule, not a convention, and should be implemented as a clamp in the component, not left to content discipline).

| `align` | Behaviour (small/medium only) |
|---|---|
| `center` (default) | Centered within `--width-content` |
| `left` | Flush to the left edge of `--width-content`, i.e. `margin-inline-start: 0`, `margin-inline-end: auto` |
| `right` | Flush to the right edge, mirrored |

Below `--bp-desktop`, all `align` values collapse to `center` (source §16: "horizontal asymmetry can be reduced on narrow screens"). Implement as a single media-query override, not a separate mobile field in content.

### 5.4 Pair behaviour

**Desktop (≥ `--bp-tablet`):**

- Two images side by side in a single flex row, centered within `--width-content`, separated by a fixed inter-image gap of `--space-sm`.
- `ratio: equal` → both images `flex: 1 1 0`, same rendered height (width adjusts per aspect ratio — implementation detail: set both to the same CSS `height` via `object-fit: contain`-free approach is wrong for photography; instead constrain by equal `flex-basis` width and let each image keep its own aspect ratio, which is the correct book-editing behavior — do NOT crop images to force equal heights).
- `ratio: left-heavy` → left image `flex: 1.4`, right image `flex: 1`. `right-heavy` is the mirror.
- The combined pair width envelope is the `size` token from §4.4 applied to the *row*, i.e. `max-width: var(--image-{size}-max)` on the flex container, centered.

**Tablet (< `--bp-tablet`, i.e. large mobile/tablet band) and small mobile:**

- Pair stacks vertically. The conceptual relationship is preserved by: (a) a smaller vertical gap between the two stacked images than a normal `gapAfter` would use — always `--space-2xs` between the two images of a stacked pair, regardless of the pair's own `gapAfter` (which still applies *after* the whole pair, before the next block); (b) both images share the same rendered width in the stacked state (`width: 100%` of the mobile image column, per the pair's `size` token), so they visually read as one unit rather than two independent images with standard spacing between them.
- `ratio` is ignored when stacked (both images render at equal width — a heavier/lighter *height* relationship along one shared row doesn't translate to a stacked layout).

### 5.5 Section breaks (`break` blocks and `gapAfter: pause`)

- A `break` block renders as pure vertical space — no rule, no icon, no text — sized per `--space-large` or `--space-pause`.
- The difference between a `break` block and simply setting `gapAfter: pause` on the preceding image: `gapAfter: pause` puts an intentional pause *after* a specific image; a standalone `break` block is used when the pause itself is the semantic marker of a new section rather than being attached to the preceding image. Both are supported because they read differently in the content file and give the photographer(/content author) two distinct editorial gestures.

### 5.6 Sequence-level rules

- The `sequence` array is rendered in array order with no re-sorting, no aspect-ratio-based auto-layout, no masonry. This is non-negotiable per source §11.
- The first block's `gapAfter`-equivalent *before* it (i.e., space between title/description block and the first sequence item) is fixed at `--space-lg`, not authored per work.
- The space after the last sequence block, before the footer, is fixed at `--space-xl`, not authored per work.

---

## 6. Content Schema

Astro Content Collections, defined in `src/content/config.ts`.

### 6.1 `works` collection

```typescript
import { defineCollection, z, reference } from 'astro:content';

const sequenceImage = z.object({
  type: z.literal('image'),
  src: z.string(),
  size: z.enum(['small', 'medium', 'large', 'full']).default('large'),
  align: z.enum(['left', 'center', 'right']).default('center'),
  gapAfter: z.enum(['tight', 'normal', 'large', 'pause']).default('normal'),
  caption: z.string().optional(),
  alt: z.string().optional(),
  decorative: z.boolean().default(false),
}).refine(
  (v) => v.decorative || (v.alt && v.alt.length > 0),
  { message: 'alt is required unless decorative: true' }
);

const pairImage = z.object({
  src: z.string(),
  alt: z.string().optional(),
  decorative: z.boolean().default(false),
}).refine(
  (v) => v.decorative || (v.alt && v.alt.length > 0),
  { message: 'alt is required unless decorative: true' }
);

const sequencePair = z.object({
  type: z.literal('pair'),
  images: z.tuple([pairImage, pairImage]),
  size: z.enum(['small', 'medium', 'large']).default('medium'),
  ratio: z.enum(['equal', 'left-heavy', 'right-heavy']).default('equal'),
  gapAfter: z.enum(['tight', 'normal', 'large', 'pause']).default('normal'),
  caption: z.string().optional(),
});

const sequenceBreak = z.object({
  type: z.literal('break'),
  size: z.enum(['large', 'pause']).default('pause'),
});

const sequenceBlock = z.discriminatedUnion('type', [
  sequenceImage,
  sequencePair,
  sequenceBreak,
]);

export const works = defineCollection({
  type: 'content', // frontmatter + optional Markdown body for `description`
  schema: z.object({
    title: z.string(),
    nativeTitle: z.string().optional(),   // e.g. "住民" for Residents
    routeSlug: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/),
    year: z.string(),                     // "2026" or "2024–2026"
    status: z.enum(['published', 'hidden', 'ongoing']).default('hidden'),
    order: z.number().default(0),         // manual ordering on the Home index
    deck: z.string().max(140).optional(), // one-line description shown on Home index
    description: z.string().optional(),   // longer intro shown on the work page itself
    location: z.string().optional(),
    sequence: z.array(sequenceBlock).default([]),
  }),
});
```

Notes:

- `status: hidden` works are excluded from `getStaticPaths` in production builds (see §16) — not merely CSS-hidden.
- `status: ongoing` behaves like `published` (it *is* built and listed) but the Home index may optionally suffix it with a small muted "ongoing" label — this is the one place a status word may appear in the UI, and it must render as plain muted text, never a badge/pill/chip.
- `order` is ascending; ties fall back to `year` descending, then `title` alphabetical. In practice the photographer sets `order` explicitly for every published work so this is deterministic and intentional, not incidental.
- The frontmatter field is named `routeSlug`, not `slug` (renamed during implementation to avoid any ambiguity with Astro's own file-based `entry.slug`, which this project does not use for routing). It is redundant with the file-based slug in Astro content collections but is kept explicit to decouple the URL from the filename (so a work's file can be renamed without changing its live URL) — code uses the frontmatter `routeSlug` field for routing, never `entry.slug`. This same rename applies to `notes` (§6.2) and `found` (§6.1a).

### 6.1a `found` collection

A separate collection for found/appropriated photographs (§3.6) — deliberately not folded into `works`, since these pieces are not authored by the photographer and the site keeps that distinction visible via a separate section rather than a shared list with a status flag.

```typescript
export const found = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    nativeTitle: z.string().optional(),
    routeSlug: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/),
    year: z.string(),
    status: z.enum(['published', 'hidden', 'ongoing']).default('hidden'),
    order: z.number().default(0),
    deck: z.string().max(140).optional(),
    description: z.string().optional(),
    provenance: z.string().optional(),   // e.g. "Found in a secondhand shop, Ōsaka, 2025." — see §3.6
    sequence: z.array(sequenceBlock).default([]),
  }),
});
```

Notes:

- Reuses the exact same `sequenceBlock` union as `works` (§6.1) — `found` pieces are laid out with the identical `image`/`pair`/`break` grammar (§5), so no separate layout vocabulary was introduced for this collection.
- The only field `found` has that `works` doesn't is `provenance`; the only field `works` has that `found` doesn't is `location`. Everything else (including the `status`/`order`/sort behavior) is identical to §6.1's notes above.
- Assets for this collection live under `src/assets/found/[slug]/`, resolved the same way as `src/assets/works/[slug]/` (§8) but from a separate top-level folder, keyed by an explicit `collection: 'works' | 'found'` prop threaded through `Sequence.astro` → `SequenceImage.astro`/`SequencePair.astro` → `ResponsiveImage.astro`, so the same image-resolution code serves both collections instead of being duplicated per collection.

### 6.2 `notes` collection

```typescript
export const notes = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string().optional(),
    date: z.date(),
    routeSlug: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/),
    status: z.enum(['published', 'hidden']).default('published'),
  }),
});
```

Body (Markdown/MDX) contains the note text and any inline images using standard Markdown image syntax; inline images in note bodies default to `medium` size, centered, via a small MDX component override (§10.4) — content authors do not need to hand-write layout grammar for a one-off note image.

### 6.3 `about` collection

Implemented as an explicit single-entry collection (`src/content/about/index.md`, entry id `index`), not left schema-less:

```typescript
export const about = defineCollection({
  type: 'content',
  schema: z.object({ title: z.string().default('About') }),
});
```

`title` defaults to `'About'` so the frontmatter can omit it entirely for the common case; the page reads it via `getEntry('about', 'index')`, not a hardcoded string, so the `<h1>` text stays a content edit rather than a template change if it's ever renamed. Body is prose Markdown — no further schema complexity.

### 6.4 Representative example — `src/content/works/almost-home.md`

```yaml
---
title: Almost home
routeSlug: almost-home
year: "2026"
status: published
order: 1
deck: Photographs made along a route walked too many times to still be a route.
sequence:
  - type: image
    src: "01.jpg"
    size: large
    align: center
    gapAfter: normal
    alt: "A narrow street at dusk, a single lit window above a shuttered shop."

  - type: pair
    images:
      - src: "02.jpg"
        alt: "A folded tarpaulin on a stack of crates."
      - src: "03.jpg"
        alt: "A cat asleep on the same crates, days later."
    size: medium
    ratio: equal
    gapAfter: large

  - type: break
    size: pause

  - type: image
    src: "04.jpg"
    size: small
    align: right
    gapAfter: tight
    alt: "A hand-painted sign, partially peeled, on a metal shutter."

  - type: image
    src: "05.jpg"
    size: full
    gapAfter: pause
    alt: "A wide view of a car park at night, sodium lights overexposed."
---

A body of photographs made walking the same three kilometres between 2024 and 2026.
```

---

## 7. Component Architecture

Astro components, `.astro` files, minimal client-side JS (ideally zero — no `client:*` hydration directives anywhere in v1; the only JavaScript on the site, if any, is a tiny inline script for `prefers-reduced-motion`-aware behaviour, which is unnecessary if no animation exists at all).

```
src/components/
  SiteHeader.astro        Global nav (title + Found/Notes/About links, aria-current on the active one)
  SiteFooter.astro        Copyright line, Instagram/email links, minimal
  WorkIndexList.astro     Renders the Home page's list of works (title, year, deck)
  FoundIndexList.astro    Renders the Found index list (title, year, deck) — same shape as WorkIndexList,
                           kept as a separate component rather than a shared/parameterized one (§7 note below)
  NotesIndexList.astro    Renders the Notes index list (date, title)
  Sequence.astro          Iterates a `sequence` array, dispatches per block type; takes a `collection`
                           prop ('works' | 'found', default 'works') threaded down to ResponsiveImage
                           so the same grammar/components serve both collections
  SequenceImage.astro     Renders a single `image` block (uses ResponsiveImage)
  SequencePair.astro      Renders a `pair` block (two ResponsiveImage instances + flex/stack logic)
  SequenceBreak.astro     Renders a `break` block (pure spacing div)
  ResponsiveImage.astro   Wraps Astro's <Image>/<Picture>, applies size-token max-width,
                           handles alt/decorative logic, reserves aspect ratio; resolves its `src`
                           against `src/assets/{collection}/**` via the `collection` prop
```

Component responsibilities are kept to exactly what's listed — no generic `<Card>`, `<Container>`, `<Section>`, or `<Grid>` components exist, because the design has no card/grid concept (source §6, §28: avoid fragmenting every HTML element into a component).

`WorkIndexList.astro`/`FoundIndexList.astro` were implemented as two separate components rather than one generic `IndexList` taking a collection prop — the two lists are identical in markup today, but keeping them separate leaves room for the Found index to diverge later (e.g. showing `provenance`) without threading conditional branches through a shared component. Revisit only if a third identical list appears.

`Sequence.astro` responsibility: given `sequence: SequenceBlock[]` and a `collection`, render each block via a conditional on `type`, passing `gapAfter` down as a CSS custom property (`style={`--gap-after: var(--space-${gapMap[block.gapAfter]})`}`) consumed by a shared `margin-block-end` rule, and forwarding `workSlug`/`collection` to each block component so it can resolve its own image paths — this keeps spacing and asset-resolution logic in one place rather than duplicated per block component.

`ResponsiveImage.astro` responsibility: the single point where Astro's built-in image optimization (`astro:assets`) is invoked, producing the responsive `srcset`/`sizes` and `width`/`height` attributes from the source file's real dimensions (see §10). It accepts `size` (small/medium/large/full), translates it into both the CSS max-width token and an appropriate `sizes` attribute, and accepts `collection` ('works' | 'found') to select which top-level asset folder its `import.meta.glob` resolves `src` against.

---

## 8. Repository Structure

```
/
├─ astro.config.mjs
├─ package.json
├─ tsconfig.json
├─ src/
│  ├─ components/            (§7)
│  ├─ layouts/
│  │  ├─ BaseLayout.astro    <head>, header, footer, SEO tags
│  │  ├─ WorkLayout.astro    BaseLayout + work-page-specific title/description block
│  │  └─ FoundLayout.astro   BaseLayout + found-piece title/description/provenance block (§3.6)
│  ├─ pages/
│  │  ├─ index.astro                 → /
│  │  ├─ works/[slug].astro          → /works/[slug]/
│  │  ├─ found/index.astro           → /found/
│  │  ├─ found/[slug].astro          → /found/[slug]/
│  │  ├─ notes/index.astro           → /notes/
│  │  ├─ notes/[slug].astro          → /notes/[slug]/
│  │  ├─ about.astro                 → /about/
│  │  └─ rss.xml.ts                  (optional, cheap to add — Notes only)
│  ├─ content/
│  │  ├─ config.ts           (§6 schemas)
│  │  ├─ works/
│  │  │  ├─ almost-home.md
│  │  │  ├─ residents.md
│  │  │  └─ photographs-2026.md
│  │  ├─ found/
│  │  │  └─ *.md
│  │  ├─ notes/
│  │  │  └─ *.md
│  │  └─ about/
│  │     └─ index.md
│  └─ styles/
│     ├─ tokens.css          (§4: color, type, spacing, breakpoints, image widths)
│     └─ global.css          (reset, base element styles, link/focus states)
├─ src/assets/
│  ├─ works/
│  │  ├─ almost-home/
│  │  │  ├─ 01.jpg   (source masters, see §10 — NOT served directly)
│  │  │  └─ ...
│  │  ├─ residents/
│  │  └─ photographs-2026/
│  └─ found/
│     └─ [slug]/      (one folder per found piece, same convention as works/[slug]/)
└─ public/
   ├─ favicon.svg
   └─ og-default.jpg
```

- Source images live under `src/assets/works/[slug]/` or `src/assets/found/[slug]/` (not `public/`) specifically so Astro's build-time image pipeline (`astro:assets`) processes every reference — anything placed in `public/` bypasses optimization entirely and must never be used for photographic content.
- `sequence[].src` in frontmatter is a filename relative to that entry's asset folder; `ResponsiveImage.astro` resolves it via a single Vite `import.meta.glob` over `src/assets/{works,found}/**/*.{jpg,jpeg,png}` keyed by relative path, then looks up `` `/src/assets/${collection}/${src}` `` — one glob shared across both collections, rather than requiring a static `import` statement per image in a `.astro` file (which doesn't scale to dozens of photographs per work) or a separate glob per collection.

---

## 9. Image Pipeline

### 9.1 Source expectations

- Archive masters (TIFF or high-res JPEG) are never committed to the web repository. Only web-ready derivatives that Astro will further process are committed under `src/assets/works/[slug]/` or `src/assets/found/[slug]/`.
- Accepted input format for the pipeline: high-quality JPEG (quality ≥ 90 at source) or PNG, sRGB color profile embedded or convertible to sRGB at ingestion. Do not commit TIFFs into the repo (they bloat the git history and are unnecessary for a static site build).
- Ingestion step (manual or scripted, outside the site build): from a TIFF master, export an sRGB JPEG at the image's true pixel dimensions (do not pre-downscale below what `full` size could ever need at the widest supported viewport × device-pixel-ratio — practically, ~2560px on the long edge is a sufficient ceiling given `--image-full-max` tops out at 1280 CSS px and accounting for 2x DPR).

### 9.2 Generated formats and widths

Using Astro's built-in `astro:assets` (Sharp-based) image service:

- Formats generated per source image: **AVIF**, **WebP**, **JPEG** (fallback), via `<Picture>` with `<source>` elements in that preference order.
- Responsive widths generated per size token (only the widths actually needed for that token's max CSS width, at 1x/2x):

| size token | widths generated (px) |
|---|---|
| `small` | 480, 960 |
| `medium` | 760, 1140, 1520 |
| `large` | 1040, 1560, 2080 |
| `full` | 1280, 1920, 2560 |

- `sizes` attribute on each `<Picture>` mirrors the CSS max-width formula from §4.4 (e.g. for `medium`: `sizes="(max-width: 767px) 90vw, min(72vw, 760px)"`).
- JPEG quality: 82. AVIF/WebP quality: Sharp defaults (auto) tuned for perceptual quality, verified visually on 2–3 representative images before locking the pipeline config — do not accept default compression blindly if banding/artifacts are visible on smooth tonal gradients (a real risk for film-scan skies).

### 9.3 Aspect ratio / layout shift

- Astro's `<Image>`/`<Picture>` output includes `width`/`height` attributes automatically from the source file's real dimensions — this is sufficient to reserve aspect ratio with zero extra config, as long as CSS never overrides both dimensions with a fixed pixel box (only `max-width` is set; height is `auto`).

### 9.4 Loading strategy

- The first sequence block's image(s) on a work page: `loading="eager"`, and the very first only also gets `fetchpriority="high"`.
- All subsequent images: `loading="lazy"`.
- Home and Notes pages carry no photographs in v1, so this mainly applies to work pages.

### 9.5 Metadata handling

- Sharp's default processing strips EXIF on output by default when re-encoding — verify this remains true in the chosen Astro image config, or explicitly strip EXIF (camera/lens/GPS) from generated derivatives. Do not deliberately preserve or expose EXIF to the front end (source §19 — equipment metadata is invisible by design, and GPS EXIF in particular must never leak from a photograph even if the project doesn't display a location).
- Color profile: convert to sRGB at ingestion (§9.1); do not rely on the browser to interpret an embedded ProPhoto/Adobe RGB profile correctly across all devices.

---

## 10. Accessibility

- **Keyboard navigation**: every interactive element (nav links, footer links, in-body links) is a real `<a>`; no `<div onclick>` pseudo-links anywhere. Tab order follows visual/DOM order (no `tabindex` overrides).
- **Focus states**: `:focus-visible` outline per §4.6 on every link; never remove focus outlines without replacement.
- **Semantic HTML**: `<header>`, `<nav>` (for the header link group), `<main>`, `<footer>`; one `<h1>` per page; work titles are `<h1>` on their own page and plain link text (not headings) in the Home index list, since the index itself has its own single `<h1>` ("Nicolas Tei" or a visually-hidden "Works" label — see below).
- **Heading structure**: Home page `<h1>` is present for correct document structure but visually hidden (`.sr-only`, standard clip-based hidden pattern — not `display: none`, which some screen readers also skip) — the site name already appears once, visibly, in the header on every page, and the photographer's name should appear on-page only in the header nav and on About (not a third time on Home); the hidden `<h1>` text is a plain structural label ("Works"), not the name. Work page `<h1>` = work title. Notes index `<h1>` = "Notes". About `<h1>` = "About" (the name itself appears in the page's own body copy, not the heading).
- **Contrast**: `--color-fg` on `--color-bg` computes to a contrast ratio well above WCAG AA (>15:1) for body text. `--color-muted` on `--color-bg` clears **4.5:1** (~4.85:1) for any text below `--font-size-small` used as real content (dates, deck lines) — re-verify and do not ship muted text that fails AA if either hex value changes.
- **Reduced motion**: since v1 ships with no animation at all, there is technically nothing to gate — but if any transition is added later (e.g. a hover underline transition), wrap it in `@media (prefers-reduced-motion: no-preference)`.
- **Alt text strategy** (source §24 — this needs explicit rules, not vibes):
  - Every `image`/`pair` image block requires either a real `alt` string or an explicit `decorative: true` flag (enforced by the Zod schema in §6.1 — a build-time validation error if neither is present).
  - Alt text should describe what is concretely visible (subject, composition, light) in plain, unromanticized language — not an interpretation of meaning, and never invented symbolism. Example: `"A folded tarpaulin on a stack of crates."` — not `"A meditation on impermanence."`
  - Filenames must never be used as alt text (enforced by review, not automatable — Codex should flag any `alt` value that looks like a filename pattern, e.g. matches `/^(img|dsc|_[a-z0-9]+)?[-_ ]?\d{2,6}(\.\w+)?$/i`, as a lint warning during content build, not a hard error).
  - `decorative: true` should be used sparingly — realistically only for a texture-like or non-subject-bearing frame within a `pair` where the paired alt text on the other image already carries the meaning; it is not a shortcut for "author didn't write alt text."

---

## 11. SEO / Metadata

- `BaseLayout.astro` sets, per page: `<title>`, `<meta name="description">` (from `deck`/`description` where present, else a short static fallback per page type — never keyword-stuffed), canonical `<link rel="canonical">`, Open Graph (`og:title`, `og:description`, `og:image`, `og:type`).
- `og:image`: a static `public/og-default.jpg` site-wide default is sufficient for v1; per-work OG images (e.g. the work's first sequence image, re-rendered at OG dimensions 1200×630) are a reasonable low-effort future enhancement, not required for v1.
- `sitemap-index.xml` via `@astrojs/sitemap` integration, excluding any `status: hidden` work/note routes (they aren't built, so this is automatic).
- `robots.txt` present, allowing all, pointing at the sitemap.
- No structured data (JSON-LD) required in v1 — would add complexity disproportionate to the site's goals.

---

## 12. Performance

Targets (indicative, not a Lighthouse-chasing exercise per source §23):

- Lighthouse Performance ≥ 90 on a representative work page on throttled mobile, achieved naturally by static HTML + optimized images + zero JS hydration, not by special-casing.
- Cumulative Layout Shift ≈ 0, verified by the aspect-ratio reservation in §9.3.
- No render-blocking web font FOIT beyond a brief, acceptable flash — use `font-display: swap` on the self-hosted Inter/Noto Sans JP `@font-face` declarations; preload the Inter regular/medium woff2 files (the ones used above the fold) via `<link rel="preload" as="font" ...>` in `BaseLayout.astro`.
- Total JS shipped to the browser in v1: effectively 0 KB of custom application JS. Astro ships zero JS by default for purely static `.astro` components with no `client:*` directive — preserve this.
- Image weight: rely on the format/width matrix in §9.2 rather than a page-weight budget number, since a photography site's legitimate weight is dominated by images the viewer came to see.

---

## 13. Non-Goals (repeated explicitly per source §41)

Codex must **not** implement any of the following, even if they seem like natural additions:

- A lightbox / image enlargement modal.
- Any masonry or aspect-ratio-driven auto-layout.
- A thumbnail navigator/rail for jumping around within a work.
- Parallax, scroll-hijacking, scroll-triggered fade/slide-in animations, kinetic typography, custom cursors, draggable galleries, autoplay of anything.
- A sticky/persistent header or any UI chrome that stays fixed while scrolling.
- A hamburger menu at any breakpoint.
- Card UI, drop shadows, rounded "app" containers, gradients, glossy effects around photographs.
- Camera/lens/aperture/shutter/film-stock metadata display, unless a specific project explicitly opts in via a future schema extension (none exist in v1).
- Tags, related-content recommendations, comments, reading-time badges, social share buttons, author cards.
- A light theme or a theme toggle of any kind — the site ships dark only (§4.1), and does not follow OS `prefers-color-scheme`.
- A CMS, database, authentication, or server backend of any kind.
- Full i18n / translated content duplication requirements — content is whatever language it's authored in; no `[lang]` routing tree in v1.
- Cookie banners or invasive analytics (no analytics at all in v1 unless the user separately requests a specific privacy-respecting tool later).
- Fake film/analog UI affectations: paper texture, sprockets, dust overlays, contact sheets, handwritten fonts, distressed type, date-stamp graphics.

---

## 14. Acceptance Criteria

**Home**
- [ ] Renders only `published`/`ongoing` works, in `order` then `year` (desc) then `title` order.
- [ ] Zero layout for hidden works anywhere in output HTML (view-source contains no reference to hidden work titles/slugs).
- [ ] No image requests fire from the Home page in v1.

**Work page**
- [ ] Sequence renders in exact authored array order.
- [ ] Every `image`/`pair` block without `decorative: true` has non-empty `alt`; build fails otherwise (Zod refine).
- [ ] `size`/`align`/`gapAfter` produce the exact CSS custom-property/max-width values specified in §4.4/§4.3/§5.3, verified by inspecting computed styles in a browser for at least one instance of each size × align combination.
- [ ] `large`/`full` images always render centered regardless of authored `align`.
- [ ] A `pair` block stacks below `--bp-tablet` with the two images at equal width and `--space-2xs` between them.
- [ ] No CLS: forcing a slow network throttle, scrolling through a work page produces no visible image-load reflow.
- [ ] `status: hidden` work produces no route in `astro build` output (`dist/works/[slug]/` absent).

**Found**
- [ ] Renders only `published`/`ongoing` found pieces, same sort rule as Home (`order` then `year` desc then `title`).
- [ ] `status: hidden` found piece produces no route in `astro build` output (`dist/found/[slug]/` absent), same as a hidden work.
- [ ] A found piece's sequence renders with the identical size/align/gapAfter/pair rules as a work page — no visual or behavioral divergence beyond the optional `provenance` line.
- [ ] `/found/` still renders (heading only) with zero published entries — never a 404, never a "coming soon" message.

**Notes**
- [ ] A note with only a date and one sentence of body text renders without visual "emptiness" artifacts (no forced min-height, no broken card).
- [ ] Notes index paginates only once entries exceed ~40, and never before.

**About**
- [ ] Content is editable by modifying `src/content/about/index.md` alone, no component/template change required for a copy edit.

**Global**
- [ ] No `client:*` directive appears anywhere in the codebase for v1.
- [ ] `prefers-reduced-motion` has nothing to override because no motion exists — confirmed by grep for `animation`/`transition` in CSS returning only the link-underline-thickness hover rule (§4.6), which is not motion-sensitive (instant, not animated).
- [ ] Lighthouse a11y score ≥ 95 on Home, a work page, and a note.
- [ ] `astro build` succeeds with `@astrojs/sitemap` producing a sitemap that excludes hidden content.
- [ ] Keyboard-only pass: every link on every page type is reachable and visibly focused via Tab, in logical order.
- [ ] Every page loads dark regardless of the visitor's OS `prefers-color-scheme` setting — there is no light variant and no toggle anywhere in the UI.

---

## 15. Implementation Order

Each checkpoint should leave the site in a working, deployable state.

1. **Scaffold**: `astro init` (minimal template), TypeScript config, `astro.config.mjs` with `@astrojs/sitemap`, `trailingSlash: 'always'`. Add `tokens.css`/`global.css` with the full §4 token set even before any page consumes all of them.
2. **Base layout & nav**: `BaseLayout.astro`, `SiteHeader.astro`, `SiteFooter.astro`. A placeholder Home page proves the header/footer/token system end to end.
3. **Content schema**: `src/content/config.ts` per §6, with one real `works` entry (Almost home) and its images placed under `src/assets/works/almost-home/`.
4. **Photography layout grammar**: `Sequence.astro`, `SequenceImage.astro`, `SequencePair.astro`, `SequenceBreak.astro`, `ResponsiveImage.astro`, wired to render the one real work end to end at `/works/almost-home/`. This is the highest-risk, most important checkpoint — validate every size/align/pair/gap combination visually before moving on.
5. **Home index**: `WorkIndexList.astro` rendering the real work(s) per §3.1, hooked up to the `works` collection with status filtering and ordering.
6. **Notes**: `notes` collection, index page, individual note page, at least one real note.
7. **About**: static content page from Markdown.
8. **Image pipeline hardening**: confirm AVIF/WebP/JPEG output, correct `sizes`, EXIF stripped, aspect ratio reserved — audit network tab and computed styles against §9/§4.4.
9. **SEO pass**: titles, descriptions, OG tags, sitemap, robots.txt.
10. **Accessibility pass**: heading structure, focus states, contrast check on `--color-muted`, alt-text lint check, full keyboard pass.
11. **Second and third works** (Residents, Photographs 2026) added purely as content — no component changes should be required; if any are needed, that's a signal the grammar in step 4 was under-specified and should be revisited before adding more content.
12. **Deploy**: Cloudflare Pages (or equivalent static host), verify production build matches dev in image quality and hidden-content exclusion.
13. **Found section** (added after v1, §3.6/§6.1a): `found` collection, `FoundLayout.astro`, `FoundIndexList.astro`, `/found/` + `/found/[slug]/` routes, `src/assets/found/`, header nav entry. Reused `Sequence.astro`/`SequenceImage.astro`/`SequencePair.astro`/`ResponsiveImage.astro` unchanged in logic except for the added `collection` prop — confirming step 4's layout grammar was in fact reusable across collections, per the caution in step 11.
