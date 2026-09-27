# nicolastei.com — Typography + Fullscreen Navigation Redesign

## Purpose

Redesign nicolastei.com with stronger homepage typography and a global fullscreen menu while preserving the site's photographic presentation and existing responsive behavior.

This is an implementation plan for the existing Astro site. It is not a request to rebuild the site or reorganize the repository.

Reference direction: jooyongseong.com. Use only the idea of strong typography and fullscreen navigation, not a pixel-for-pixel copy.

## Final design direction

- Keep the homepage completely image-free.
- Keep Works directly visible on the homepage. Do not hide Works behind the menu.
- Replace the visible upper-right `Notes / About` navigation with a text button labelled `Menu`.
- The fullscreen menu becomes the global site directory and contains all Works, Notes, and About.
- Increase homepage project-title typography substantially.
- Keep the fullscreen menu denser and more functional than the homepage.
- Preserve the restrained visual language: no decorative effects, hero image, hover thumbnails, or theatrical transitions.
- Continue to prioritize photography on individual project pages.
- Audit the current implementation before changing it. Existing behavior is the baseline, but typography, homepage spacing, header proportions, and menu layout may change intentionally.

## Known implementation baseline

The source audit must still be completed before implementation, but the current repository already establishes these facts:

- The site is Astro without a client UI framework.
- `BaseLayout.astro` renders the global header, main content, and footer.
- All public pages currently pass through `BaseLayout.astro`.
- Works metadata is stored in the `works` Astro content collection under `src/content/works/`.
- The homepage already reads and sorts that collection.
- Current responsive thresholds are approximately:
  - `420px`: narrow index rows stack vertically.
  - `767/768px`: primary mobile/tablet layout boundary.
  - `1080px`: desktop work-image sizing and alignment changes.
- The CSS tokens name `768px` and `1080px`, but current media queries use literal values.
- Work pages do **not** currently implement CSS scroll snap.
- Most work pages use document scrolling with viewport-height frames based on a pinned `--svh-unit`.
- `Inhabitant Portraits` uses a click-through image gallery with an internal active slide.
- The homepage index currently has a `34rem` maximum width, which is likely too narrow for the new large title treatment.

Do not describe the existing work-page behavior as scroll snap in implementation notes or QA results.

---

## Phase 0 — Mandatory audit and regression baseline

Do not change production code until the audit and baseline capture are complete.

### 0.1 Inspect the source

Inspect and record:

- `src/layouts/BaseLayout.astro`
- `src/components/SiteHeader.astro`
- `src/components/SiteFooter.astro`
- `src/pages/index.astro`
- `src/components/WorkIndexList.astro`
- `src/layouts/WorkLayout.astro`
- `src/components/Sequence.astro`
- `src/components/SequenceImage.astro`
- `src/components/SequencePair.astro`
- `src/components/WorkImageGallery.astro`
- Notes and About pages/layouts
- `src/styles/tokens.css`
- `src/styles/global.css`
- works content schema and entries

Inventory:

- all media queries and their actual behavior
- `clamp()`, `vw`, `vh`, `svh`, and `dvh` usage
- fixed, sticky, absolute, and relative positioning
- z-index layers
- overflow and scrolling ownership
- the pinned mobile viewport-height JavaScript
- shared horizontal page padding
- typography tokens and page-specific scales
- image width and max-height rules
- footer/contact links
- visible focus treatment

Do not perform unrelated cleanup during this work.

### 0.2 Record the responsive system

Create a short audit note in the final implementation summary using this structure:

```text
Base:
- header positioning:
- horizontal padding:
- homepage index width/type:
- project image sizing:
- scrolling behavior:

420px rule:
- changes:

767/768px boundary:
- changes:

1080px rule:
- changes:
```

Reuse `420`, `768`, and `1080` unless the redesigned content demonstrates a real need for an additional breakpoint. QA viewport sizes are not mandatory CSS breakpoints.

### 0.3 Capture the visual baseline

Capture the current site after fonts and initial images have loaded:

- homepage at `390 × 844`
- homepage at `1440 × 900`
- one representative sequence-based project at both sizes
- `Inhabitant Portraits` at both sizes
- Notes mobile
- About mobile

Use Playwright if it is added intentionally as a development/QA dependency. Otherwise use the local dev server and browser screenshots, and document that the comparison was manual. Do not claim automated visual comparison when no screenshot tooling exists.

Record the active `Inhabitant Portraits` slide used in the baseline.

### 0.4 Classify current behavior

Classify audited rules as:

- **Preserve** — project sequencing, image presentation, existing responsive behavior that already works, Notes/About content layout, footer behavior.
- **Modify** — homepage index width, homepage title typography and spacing, header navigation, global menu behavior.
- **Remove** — only rules made obsolete by this redesign.

---

## Phase 1 — Information architecture

The homepage remains the Works index.

Intended hierarchy:

1. Works/project titles
2. Photography after entering a project
3. Nicolas Tei
4. Global navigation controls, Notes, and About

The homepage should feel like a photobook contents/opening page rather than a conventional portfolio landing page.

Do not add a homepage hero, slideshow, background image, or hover-preview image.

---

## Phase 2 — Works data architecture

Use the existing `works` Astro content collection as the single source of truth for:

- project title
- native title where applicable
- route slug/URL
- status
- order
- deck where applicable

Homepage and fullscreen menu must not maintain separate hardcoded project arrays.

The existing homepage sorting behavior must remain consistent in both locations. A small shared helper such as `getVisibleWorks()` is acceptable if it removes duplicated querying/filtering/sorting logic. Do not reorganize the content system.

---

## Phase 3 — Header redesign

Change the visible global header from:

```text
Nicolas Tei                              Notes   About
```

to:

```text
Nicolas Tei                                      Menu
```

Requirements:

- Keep `Nicolas Tei` linked to `/`.
- Use the word `Menu`, not a hamburger icon.
- Use a real `<button type="button">` for Menu/Close.
- Change its visible label to `Close` while open.
- Remove visible Notes/About links from the closed header.
- Do not add a closed-header Works link; the homepage already is the Works index.
- Preserve the current header's in-flow positioning model unless the audit finds a concrete reason to change it.
- Use the same navigation semantics across homepage, projects, Notes, and About; positioning may continue to follow the page's existing layout context.
- Do not introduce an opaque fixed strip over photographs.

Initial control semantics:

```html
<button type="button" aria-expanded="false" aria-controls="site-menu">
  Menu
</button>
```

The closed header must retain useful touch target sizing and visible keyboard focus.

---

## Phase 4 — Homepage typography

Project titles become the homepage's principal visual content.

### 4.1 Homepage-specific layout

The current shared index width is approximately `34rem`. Do not globally enlarge `--width-index`, because other indexes may depend on it.

Create a homepage/Works-specific width or layout rule where needed. Keep it aligned to the site's existing horizontal grid and padding.

Do not turn project entries into cards, bordered rows, panels, or tiles. Use typography and whitespace only.

Do not add a large `WORKS` label unless visual testing demonstrates a genuine need.

### 4.2 Type scale and wrapping

- Increase homepage project titles substantially relative to the current body-size treatment.
- Derive the final scale from the existing fluid token system.
- A homepage-specific `clamp()` token is acceptable.
- Do not replace unrelated global typography tokens.
- Use natural wrapping with no truncation, ellipsis, or forced `white-space: nowrap`.
- Do not shrink titles excessively just to keep them on one line.
- Keep line-height compact enough to feel intentional without creating collisions.

Primary stress-test title:

`Staring at the Skin of the World Until It Peels Off.`

Test it at `320`, `375`, `390`, `430`, `768`, `1024`, `1280`, and `1440` CSS pixels.

### 4.3 Secondary metadata

- Keep `nativeTitle` only if it remains clearly subordinate and does not disrupt the title-led rhythm.
- Hide `deck` on the redesigned homepage if retaining it weakens the photobook-contents hierarchy.
- This choice must be applied consistently and documented; do not accidentally remove the underlying content data.
- Menu entries should use project titles only unless a secondary label proves necessary for disambiguation.

### 4.4 Interaction

Desktop hover may use only:

- a modest opacity/color change; or
- a very small positional shift.

Avoid image previews, cursor-following images, text scrambling, distortion, and large underline animations.

Keyboard focus must remain clearly visible.

---

## Phase 5 — Fullscreen global menu

The menu is a global directory, not a device for hiding Notes/About and not a duplicate homepage.

Desktop conceptual structure:

```text
Nicolas Tei                                      Close

Works                         How Much Silence Can a Space Hold?
Notes                         Staring at the Skin of the World Until It Peels Off.
About                         The Room Was Not Dark.
                              Inhabitant Portraits
```

Mobile conceptual structure:

```text
Nicolas Tei                           Close

Works
Notes
About

Projects

How Much Silence Can a Space Hold?
Staring at the Skin of the World Until It Peels Off.
The Room Was Not Dark.
Inhabitant Portraits
```

Principles:

- Homepage project titles are expressive and large.
- Menu project titles are smaller, denser, and navigational.
- Notes and About are visible within the first menu viewport at normal mobile heights where practical.
- On mobile, expose Works/Notes/About before the project index.
- Do not force all content into one viewport; allow the menu to scroll.
- Use actual titles, ordering, and existing routes.
- Do not rename routes.

Visual treatment:

- use the existing background, foreground color, and font family
- retain left alignment
- use clear hierarchy and generous but functional whitespace
- no colored panel, gradient, blur/glass, card, thumbnail, icon, photograph, or decorative cursor

Use `100vh` as a fallback and `100dvh` where supported. Respect existing safe-area behavior; the repository already uses `env(safe-area-inset-bottom)` for scroll hints. Apply top/bottom safe-area padding to the overlay only where it is useful.

---

## Phase 6 — Menu implementation and accessibility

Implement the overlay without adding React, Vue, Svelte, an animation library, or a heavy focus-management dependency.

Typical overlay positioning may use:

```css
position: fixed;
inset: 0;
```

but its z-index must be established relative to the existing header and fixed scroll hint.

### 6.1 DOM and visibility

- Keep the menu outside any subtree that becomes `inert`.
- When open, make background `main` and footer content inert and unavailable to assistive technology.
- Do not set `inert` on the whole body or on an ancestor containing the Close control.
- Use the `hidden` attribute or an equivalent robust hidden state when closed; do not leave an invisible interactive overlay in the accessibility tree.
- Use a labelled navigation region. If dialog semantics are used, implement `role="dialog"` and `aria-modal="true"` consistently rather than mixing partial dialog behavior.
- Apply `aria-current="page"` to the current destination where appropriate.

### 6.2 Required interaction

- Menu opens the overlay.
- Visible control label changes to Close.
- Close closes the overlay.
- Escape closes the overlay.
- Following a destination works normally and does not leave stale open state.
- Background content cannot scroll while open.
- Menu content can scroll when taller than its viewport.
- Opening moves focus predictably to Close or the first menu navigation item.
- Tab and Shift+Tab remain within the open menu.
- Closing via Close or Escape returns focus to the Menu button.
- When route navigation occurs, normal browser navigation may take precedence over focus restoration.
- `aria-expanded` always reflects state.

### 6.3 No-JavaScript reachability

Notes, About, and Works must remain reachable if the interaction script fails or JavaScript is unavailable.

Prefer server-rendering the menu links in the HTML and using JavaScript only to enhance open/close behavior. If the closed overlay cannot safely expose those links without JavaScript, provide a simple `<noscript>` navigation fallback.

### 6.4 Scroll locking and restoration

The current site scrolls the document/window. Do not add overflow ownership to `.sequence`, `.work-frame`, or the gallery.

When opening:

1. Record `window.scrollY`.
2. Lock the background without visually jumping the document.
3. Preserve the document width to avoid horizontal layout shift.

When closing:

1. Remove the lock.
2. Restore the exact recorded window position after fixed positioning is removed.
3. Confirm that opening/closing did not cause the pinned `--svh-unit` logic to change unexpectedly.

The overlay should use its own `overflow-y: auto` and may use `overscroll-behavior: contain`.

On sequence-based work pages, opening/closing must preserve the same document position and visible photograph. On `Inhabitant Portraits`, it must preserve the current `.is-active` slide.

---

## Phase 7 — Responsive behavior

Start with the existing `420`, `768`, and `1080` boundaries. Add a breakpoint only when the content produces a demonstrated layout failure.

Mobile goals:

```text
Nicolas Tei                         Menu

How Much Silence
Can a Space Hold?

Staring at the Skin
of the World Until
It Peels Off.

The Room Was
Not Dark.

Inhabitant Portraits
```

Requirements:

- no hamburger icon
- no truncation or horizontal overflow
- natural multi-line project titles
- useful touch targets
- tighter spacing than desktop where necessary
- a menu scale clearly smaller than the homepage title scale
- menu content may extend beyond one viewport
- portrait and landscape behavior remains usable

---

## Phase 8 — Notes, About, footer, and project pages

Do not redesign Notes or About content. Only change their access through global navigation and any unavoidable shared-header styling.

Preserve:

- content and URLs
- article/body typography
- responsive content width and spacing
- footer copyright, Instagram, and email behavior

Preserve project presentation unless compatibility with the menu strictly requires a change:

- image order and files
- dimensions and responsive source behavior
- desktop image sizing
- mobile viewport-frame behavior
- sequence gaps, captions, and project text
- pinned `--svh-unit` behavior
- loading strategy
- project URLs
- `Inhabitant Portraits` click-to-advance behavior and active slide

Do not introduce scroll snap as part of this redesign.

---

## Phase 9 — Motion and performance

Keep motion nearly invisible:

- a short opacity transition is sufficient
- optional very small vertical movement is acceptable
- do not stagger menu items or animate individual letters
- no parallax, page-transition sequence, or photograph animation

Respect `prefers-reduced-motion: reduce` by removing non-essential transitions.

Performance requirements:

- homepage remains image-free
- do not preload project images for hover behavior
- do not add an animation library
- do not add a framework runtime for menu state
- avoid typography/font layout shift
- preserve or improve current build output

---

## Phase 10 — QA and regression comparison

### 10.1 Required before/after screenshots

Compare the same viewport sizes and loaded states:

- homepage — `390 × 844`
- homepage — `1440 × 900`
- fullscreen menu — `390 × 844`
- fullscreen menu — `1440 × 900`
- representative sequence project — `390 × 844`
- representative sequence project — `1440 × 900`
- `Inhabitant Portraits` with a known active slide
- Notes mobile
- About mobile

Review:

- intentional title wrapping
- balanced first-viewport weight
- header scale and alignment
- clear visual difference between menu and homepage
- immediate Notes/About discoverability
- calm rather than merely oversized composition
- continued dominance of photography inside Works

### 10.2 Viewport matrix

QA viewports, not mandatory breakpoints:

- `320 × 568`
- `375 × 812`
- `390 × 844`
- `430 × 932`
- `768 × 1024`
- `1024 × 768`
- `1280 × 800`
- `1440 × 900`

At relevant sizes verify:

- header alignment and touch targets
- no horizontal overflow
- title wrapping and spacing
- menu open/close/Escape
- menu scrolling and overscroll behavior
- exact background scroll restoration
- Tab and Shift+Tab behavior
- focus return
- hidden/inert background behavior
- current-page indication
- Notes/About visibility
- sequence image layout and document scrolling
- `--svh-unit` stability on touch layouts
- unchanged `Inhabitant Portraits` active slide
- portrait and landscape behavior

### 10.3 Checks

Run:

```sh
npm run check
npm run build
```

Also test with JavaScript disabled or intentionally blocked to confirm that Works, Notes, and About remain reachable.

Document whether visual QA was automated with Playwright or performed manually in a browser.

---

## Implementation order

- [ ] Audit the current responsive implementation and record actual rules.
- [ ] Capture the current visual and behavioral baseline.
- [ ] Confirm the content collection as the Works source of truth and share sorting logic where useful.
- [ ] Add a homepage-specific index width and larger title scale.
- [ ] Resolve native-title/deck presentation and verify the longest-title wrapping.
- [ ] Replace visible Notes/About header links with the Menu button.
- [ ] Server-render the global fullscreen menu from the Works collection.
- [ ] Make the menu visually denser than the homepage.
- [ ] Add open/close, Escape, focus trap, inert background, and current-page behavior.
- [ ] Add robust document scroll locking and exact restoration.
- [ ] Add no-JavaScript navigation fallback.
- [ ] Tune responsive spacing using existing breakpoints first.
- [ ] Test mobile viewport and safe-area behavior.
- [ ] Re-test sequence frames, image sizing, pinned viewport units, and click-through gallery state.
- [ ] Run check and production build.
- [ ] Complete same-size before/after visual comparison.
- [ ] Remove any unnecessary CSS, animation, or JavaScript introduced during implementation.

---

## Acceptance criteria

### Homepage

- [ ] remains completely image-free
- [ ] Works remain directly accessible without opening Menu
- [ ] project titles are noticeably larger and visually dominant
- [ ] homepage uses an intentional page-specific width rather than globally widening all indexes
- [ ] longest title wraps naturally at all QA widths
- [ ] no truncation or horizontal overflow
- [ ] native-title/deck treatment is deliberate and consistent
- [ ] all project links and ordering remain correct

### Header

- [ ] left side contains Nicolas Tei linked to `/`
- [ ] right side contains a real Menu button
- [ ] old visible Notes/About links are removed
- [ ] Menu changes to Close while open
- [ ] `aria-expanded` and `aria-controls` are correct
- [ ] positioning remains compatible with existing page layouts

### Fullscreen menu

- [ ] contains all visible Works from the content collection
- [ ] contains Notes and About
- [ ] works globally across homepage, projects, Notes, and About
- [ ] is visually distinct from and denser than the homepage
- [ ] exposes Notes/About promptly on mobile
- [ ] fills the dynamic viewport appropriately
- [ ] scrolls internally when needed
- [ ] Escape and Close work
- [ ] background content is inert and cannot scroll
- [ ] closing restores the exact document position
- [ ] sequence-page visible position is preserved
- [ ] click-through gallery active slide is preserved
- [ ] focus enters predictably, remains trapped, and returns on close
- [ ] current-page state is exposed accessibly
- [ ] hidden menu is not interactive or present in the accessibility tree
- [ ] reduced-motion preference is respected
- [ ] core destinations remain reachable without JavaScript

### Responsive and regression

- [ ] existing `420`, `768`, and `1080` behavior is reused unless a documented content need requires more
- [ ] project image sizing and order are preserved
- [ ] document/viewport-frame scrolling remains intact
- [ ] no scroll snap is introduced
- [ ] pinned mobile viewport-height behavior remains intact
- [ ] `Inhabitant Portraits` behavior remains intact
- [ ] Notes and About layouts are preserved
- [ ] footer/contact/social links are preserved
- [ ] project URLs and routing are unchanged
- [ ] `npm run check` passes
- [ ] `npm run build` passes
- [ ] before/after visual comparison is completed and its method is documented

---

## Explicit non-goals

Do not implement:

- homepage hero imagery
- hover project thumbnails
- hamburger icons
- intro/splash screens
- Works hidden behind Menu
- a homepage containing only Nicolas Tei/Menu
- scroll snap
- parallax or cursor effects
- background video
- gradients, glass effects, cards, or decorative UI
- large transition sequences
- unnecessary font replacement
- project-gallery redesign
- arbitrary breakpoint replacement
- unrelated refactors
- a client framework or animation dependency solely for the menu
