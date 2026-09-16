# Photography Website — Source of Truth

## 0. Purpose of this document

This document is the source material for producing a complete product / design / implementation specification for a personal photography website.

The next step in the workflow is:

```text
This document
    ↓
Claude
    ↓
Complete implementation spec
    ↓
Codex
    ↓
Implementation
```

Claude should **not merely summarize this document**.

Claude's task is to convert the intentions, constraints, creative identity, visual direction, content structure, and technical preferences below into a sufficiently concrete specification that another coding agent can implement without repeatedly asking design questions.

Where this document defines an intention rather than an exact implementation detail, Claude should make a considered decision that preserves the intention.

The final spec should remove implementation ambiguity while avoiding unnecessary product complexity.

---

# 1. Project

Create a personal photography website for Tei Koh.

The website exists primarily to present photographic work.

It is **not** primarily:

* a software engineer portfolio
* a commercial photographer portfolio
* a client acquisition website
* a social network
* an Instagram replacement
* a photography archive containing everything ever photographed
* a highly interactive digital-art website
* a showcase of frontend engineering techniques

The technology should remain quiet and subordinate to the photographs.

The site should feel intentionally designed, but it should not feel "designed at" the viewer.

---

# 2. Creative identity

The photographer does not want to position the work as conventional street photography or humanistic documentary photography.

Subjects themselves are not the central definition of the work.

The working method is closer to:

1. Encounter something that is not completely understood.
2. Stop because something in the scene produces attention or uncertainty.
3. Photograph it without necessarily knowing what it means.
4. Accumulate photographs over time.
5. Later discover relationships through sequencing, editing, comparison and writing.
6. Allow a body of work to emerge rather than deciding the theme first and photographing evidence for it.

The website should respect this process.

It should therefore **not force every photograph into an explicit concept, category or explanatory caption**.

The site should leave enough ambiguity for the photographs to remain photographs rather than illustrations of written ideas.

The website should also make sequencing important.

The order in which photographs appear is part of the work.

---

# 3. Desired atmosphere

The central design qualities are:

**quiet, modest, tactile, restrained, slightly imperfect, warm, serious, unforced and refined.**

A useful Japanese description would be:

> 質朴で、静かで、少し温度があり、丁寧だけど作り込みすぎていない。

The site should have quality without luxury signalling.

It should feel considered without feeling expensive.

It should feel contemporary without following obvious contemporary web-design trends.

The feeling should be closer to opening a small independently published photography book than entering a commercial photography agency website.

There should be room to breathe.

The photographs should never appear trapped inside a UI.

---

# 4. What "rustic / simple" means here

"Simple" does **not** mean unfinished.

"Rustic" does **not** mean deliberately retro.

Avoid superficial visual shortcuts such as:

* fake paper textures
* film sprocket graphics
* dust overlays
* fake contact sheets
* handwritten fonts
* distressed typography
* simulated analog-camera interfaces
* excessive beige
* nostalgia filters
* fake date stamps

The photographs are already made on film in many cases.

The interface does not need to perform "film photography."

The design should obtain its character through:

* typography
* proportion
* spacing
* rhythm
* image scale
* alignment
* page structure
* restrained material choices

rather than decorative effects.

---

# 5. Relationship between website and photography book

The conceptual model should be closer to a photography book than to an image gallery.

Important ideas:

* sequence matters
* blank space matters
* image size matters
* pairing two images can create meaning
* changing scale can create emphasis
* interruption can create rhythm
* text does not need to accompany every photograph
* not every screen needs content
* scrolling should feel like progressing through a work

Do not reproduce literal book spreads on screen.

Instead, translate photographic-book editing principles into web-native behaviour.

---

# 6. Overall visual direction

The design should be understated.

Preferred general direction:

* light background
* dark neutral typography
* substantial negative space
* very limited colour usage
* restrained typography
* no visible card UI around photographs
* no drop shadows unless there is an exceptional functional reason
* no rounded "app" containers
* no gradients
* no glossy effects
* no oversized design-system branding
* no visual gimmicks

Pure white is not required.

A slightly warm or neutral off-white may be preferable if it improves the photographic presentation.

However, the final colour values should be chosen carefully rather than mechanically using "cream = artistic."

Photographs must remain colour-neutral. The page colour must not visibly contaminate colour perception.

---

# 7. Typography

Typography should feel quiet and precise.

Avoid typography that loudly communicates:

* luxury
* fashion magazine
* startup
* brutalism
* retro
* Japanese traditionalism
* art-school experimentation

The typography should mostly disappear during viewing.

System fonts or restrained high-quality web fonts are acceptable.

Japanese and Latin typography must coexist naturally.

The site may contain English, Japanese and occasionally Chinese content.

Claude should specify:

* font stack
* fallback behaviour
* font sizes
* line heights
* letter spacing where necessary
* heading hierarchy
* caption / metadata styling
* text width
* mobile typography behaviour

Do not introduce many typefaces.

One family or a carefully selected Latin + Japanese combination is preferable.

---

# 8. Navigation philosophy

Navigation should be obvious enough that the viewer never feels trapped.

At the same time, it should not dominate the page.

Avoid:

* large persistent navigation bars
* hamburger menus on desktop
* animated menu systems
* sticky UI that continually occupies visual space
* complex category trees

The initial information architecture should remain small.

Working structure:

```text
Home
Works
Notes
About
```

If `Home` and `Works` are effectively the same thing, Claude may simplify the structure.

Do not preserve navigation items merely because conventional portfolio websites have them.

---

# 9. Home page

The homepage should establish identity quietly.

Do not use:

* a full-screen hero photograph
* marketing copy
* "Welcome to my portfolio"
* slideshows
* autoplay
* cinematic intro animations
* large personal portrait
* masonry gallery
* Instagram-like thumbnail grid as the dominant structure

A strong candidate is a restrained textual index of works.

Example conceptual structure:

```text
Tei Koh

Almost home
2026

Residents
2026

Photographs, 2026


Notes
About
```

This is illustrative, not mandatory.

Claude should decide the exact hierarchy and spacing.

The homepage may contain small photographic cues if that meaningfully improves the experience, but it should not become a conventional portfolio grid.

---

# 10. Works

`Works` contains edited photographic bodies of work.

Possible initial projects include:

* Almost home
* Residents / 住民
* Photographs, 2026
* future unnamed or unfinished bodies of work

Project names and final availability may change.

Therefore the architecture must make projects easy to add, remove, hide or reorder.

A project does not need to be "finished" in an institutional sense before appearing.

Some projects may represent an ongoing body of photographs.

---

# 11. Work page

This is the most important page type.

The viewer should primarily experience photographs through vertical scrolling.

The sequence is authored.

Do not provide a thumbnail navigator that encourages viewers to randomly skip around as the default viewing mode.

Do not automatically create a masonry layout.

Do not arrange photographs based on aspect ratio.

The project's sequence must come from content data.

Each photograph or grouping should allow editorial control over presentation.

At minimum, the system should support:

```text
single photograph

two-image pairing

small / medium / large image scale

left / centre / right positioning where appropriate

different vertical gaps

intentional larger pauses between sections
```

Claude may propose a cleaner underlying model if needed.

The important requirement is that **presentation should behave as an editing vocabulary**, not simply an array of images.

---

# 12. Image scale

Every image should not automatically occupy the maximum browser width.

A physically smaller photograph can feel different from a large photograph.

The system should support intentionally restrained image dimensions.

For example, the implementation might contain semantic sizes such as:

```text
small
medium
large
full
```

Do not interpret `small` merely as a lower-resolution image.

It means the photograph should occupy less visual space.

The final specification should define sensible maximum widths and responsive behaviour.

---

# 13. Image alignment

Desktop layouts may occasionally use asymmetrical positioning.

For example:

```text
        photograph

photograph

                    photograph
```

This should remain restrained.

The objective is not avant-garde layout for its own sake.

Alignment should create subtle rhythm and spatial relationships.

Most photographs may remain centred.

Claude should define a small set of predictable alignment rules rather than allowing arbitrary coordinates.

---

# 14. Image pairs

The system must support deliberate image pairs.

A pair is semantically different from two consecutive images.

Pairs may appear:

* side by side
* with equal sizes
* with intentionally unequal proportions if justified

The pairing must remain readable on smaller screens.

On mobile, the design may stack images where necessary, but should preserve the conceptual relationship between the two photographs.

Claude should explicitly define pair behaviour for desktop, tablet and mobile.

---

# 15. Vertical rhythm

Whitespace is an editorial tool.

There should be several semantic spacing levels.

For example:

```text
tight
normal
large
pause
```

Exact naming is flexible.

The largest spacing should create a perceptible interruption without looking like a rendering bug.

Spacing values should respond sensibly to viewport dimensions.

Do not simply use the same margin after every image.

---

# 16. Mobile experience

Mobile must not become an Instagram feed.

The sequence remains identical.

Relative scale should be preserved where practical.

A photograph intentionally presented small on desktop should not automatically become 100vw on mobile unless necessary.

Horizontal asymmetry can be reduced on narrow screens.

Pairs may stack.

Whitespace may be reduced but should still remain meaningful.

The experience should remain calm and deliberate rather than compressed into maximum information density.

---

# 17. Notes

The website should contain a lightweight `Notes` section.

Notes are not intended to become a conventional SEO blog.

Possible content includes:

* short observations
* photography-related notes
* fragments of writing
* notes about places
* work-in-progress thoughts
* longer essays occasionally
* text associated with photographic research

A note may have:

* title or no title
* date
* text
* optional images

The design should support short entries gracefully.

A three-sentence note should not look incomplete merely because blog templates expect long articles.

Avoid:

* reading-time badges
* social share buttons
* large author cards
* tags everywhere
* related-post recommendation engines
* comment sections

---

# 18. About

The About page should remain restrained.

Avoid generic artist-language such as:

> explores memory, identity, liminality, everyday life and the human condition

unless such language is later consciously written by the photographer.

Do not invent a conceptual framework for the work.

A short introduction is enough.

Possible information:

```text
Tei Koh
Based in Japan.

Photographs, writing, selected projects.

Instagram
Email
```

The exact copy is not final.

The structure should allow future addition of:

* exhibitions
* publications
* books
* selected projects

without requiring them today.

---

# 19. Metadata

Photography metadata should normally remain invisible.

Do not display:

* camera model
* lens
* aperture
* shutter speed
* film stock

unless explicitly entered for a particular project for editorial reasons.

The website is about photographs, not photographic equipment.

Project-level information may include:

* title
* year / year range
* optional short text
* optional location if artistically relevant

Individual photographs should not require captions.

---

# 20. Interaction

Default interaction should be extremely restrained.

Avoid:

* parallax
* scroll hijacking
* custom cursors
* draggable galleries
* hover distortion
* animated page transitions
* auto-scrolling
* zoom animations
* kinetic typography
* background audio
* unnecessary fade-ins

Normal browser scrolling is desirable.

Links should clearly behave like links.

Subtle hover states are acceptable.

Image enlargement / lightbox should **not automatically be included**.

If Claude believes enlargement materially improves the work, it must justify its use and define behaviour that does not break the authored sequence.

Default assumption: no lightbox.

---

# 21. Motion

Motion is not an important part of the visual identity.

Prefer either:

```text
no animation
```

or extremely subtle functional transitions.

Respect `prefers-reduced-motion`.

Never delay access to an image so that it can perform an entrance animation.

---

# 22. Image quality

Image rendering quality is important.

Original archive files may include high-resolution TIFF scans.

These master files must not be directly served to visitors.

The website should generate suitable web assets.

Preferred considerations:

* responsive images
* modern formats such as AVIF / WebP where appropriate
* JPEG fallback where useful
* several image widths
* correct aspect-ratio reservation to prevent layout shift
* lazy loading where appropriate
* eager loading for critical first images where appropriate
* colour fidelity
* removal of unnecessary EXIF metadata
* no visibly destructive compression

Claude should specify the image pipeline.

The implementation should not make image management unnecessarily elaborate.

---

# 23. Performance

The website should feel immediate despite containing photographs.

Priorities:

1. correct photographic rendering
2. low layout shift
3. sensible page weight
4. fast initial navigation
5. minimal unnecessary JavaScript

Performance should be achieved through appropriate static-site architecture and image optimization rather than by lowering image quality excessively.

---

# 24. Accessibility

The understated design must still be accessible.

Specify:

* keyboard navigation
* visible focus states
* semantic HTML
* meaningful heading structure
* sufficient contrast
* reduced motion support
* image alt strategy

Alt text deserves particular care.

Do not require invented interpretations of abstract photographs.

The specification should distinguish between:

* useful descriptive alt text
* intentionally decorative images
* cases where project context provides sufficient information

Do not mechanically expose filenames as alt text.

---

# 25. Technical direction

Preferred initial stack:

```text
Astro
TypeScript
CSS
Astro Content Collections or equivalent structured content
Static generation
```

Use JavaScript only where it produces meaningful functionality.

React is not required.

A backend is not required.

A database is not required.

Authentication is not required.

A CMS is not required for the initial version.

The content should be editable directly in the repository.

Possible deployment target:

```text
Cloudflare Pages
```

Other static hosts are acceptable if there is a concrete advantage.

Do not introduce AWS infrastructure merely because the photographer is familiar with AWS.

Infrastructure should remain proportional to the site.

---

# 26. Content model

The content model should allow the photographer to edit sequences without modifying presentation components.

A work should contain structured information broadly resembling:

```yaml
title:
slug:
year:
status:
description:

sequence:
  - type: image
    src:
    size:
    align:
    gapAfter:

  - type: pair
    images:
      - src:
      - src:
    size:
    gapAfter:
```

This is conceptual.

Claude should design the final schema.

The schema should:

* remain human-readable
* be convenient to edit manually
* prevent obviously invalid configurations
* support future extension
* avoid becoming a miniature page builder

Do not allow arbitrary CSS in content files.

The editing vocabulary should remain deliberately limited.

---

# 27. Project status

The content model should make it possible to represent:

```text
published
hidden / draft
ongoing
```

or an equivalent model.

This permits work-in-progress projects without exposing everything publicly.

---

# 28. Repository organisation

The final spec should define a clean repository structure.

Conceptually:

```text
src/
  components/
  layouts/
  pages/
  content/
  styles/

public/ or assets/
  images/
```

Claude should decide the exact Astro-appropriate organisation.

Avoid excessive component fragmentation.

A component should exist because it represents meaningful reusable behaviour, not merely because every HTML element should become a component.

---

# 29. CSS architecture

Use a small, understandable CSS architecture.

Avoid large UI frameworks.

Do not use Tailwind automatically.

If Claude chooses Tailwind, it must provide a meaningful reason why it improves this specific project.

Plain CSS / scoped Astro styles / CSS custom properties are strong candidates.

Design tokens should exist for meaningful recurring values such as:

```text
page width
text width
spacing rhythm
image widths
background
foreground
muted text
typographic scale
breakpoints
```

Do not create an enterprise-scale token system.

---

# 30. Breakpoints

Responsive behaviour should be based on where the photographic composition actually needs to change.

Do not blindly adopt framework-default breakpoints.

At minimum, Claude should define behaviour for:

```text
small mobile
large mobile / tablet
desktop
wide desktop
```

Exact CSS breakpoints can be fewer if fluid layout techniques make them unnecessary.

---

# 31. Wide displays

On very large monitors, photographs should not simply continue growing indefinitely.

Maximum photographic dimensions should preserve a viewing distance similar to looking at prints.

Large empty margins on wide displays are acceptable.

Whitespace is preferable to oversized photographs.

---

# 32. Dark mode

Dark mode is not required for v1.

Do not implement automatic dark mode merely because operating systems support it.

Photographic presentation requires predictable surroundings.

If dark mode is introduced in the future, it should be an intentional design decision.

---

# 33. Internationalization

A full i18n framework is not required initially.

The website may contain a mixture of:

```text
English
Japanese
Chinese
```

Content should support Unicode correctly.

Typography must handle these scripts gracefully.

Do not force every note or project description to exist in several translated versions.

---

# 34. SEO

Basic technical SEO is desirable.

Include:

* page titles
* descriptions where meaningful
* canonical URLs
* Open Graph metadata
* sitemap
* sensible semantic HTML

Do not distort content or visual hierarchy for SEO.

Do not generate keyword-heavy descriptions.

Search-engine optimization is subordinate to the photographic experience.

---

# 35. Social sharing

Open Graph images may be supported.

Do not add visible social-share buttons.

Instagram may appear as a simple external link.

The website should feel like an independent place rather than an extension of social media.

---

# 36. Privacy / analytics

Avoid invasive analytics.

For v1, analytics are optional.

If analytics are proposed, prefer privacy-respecting minimal analytics.

Do not introduce cookie banners unless technically or legally necessary for actual functionality being used.

---

# 37. Anti-goals

The final design should be rejected if it starts resembling any of the following:

### Commercial photography portfolio

Large hero photo, portfolio grid, client logos, "Let's work together."

### Instagram clone

Dense thumbnails, infinite visual feed, engagement-oriented presentation.

### Art-school web experiment

Unusual cursor, chaotic positioning, illegible typography, interaction puzzles.

### Luxury editorial website

Huge serif typography, excessive fashion-magazine styling, aggressive art direction.

### Developer portfolio

Visible technical gimmicks, animation demonstrations, framework branding.

### Analog-photography cosplay

Film borders, grain UI, date stamps, darkroom textures, camera-control metaphors.

### Generic minimalist portfolio

Everything centred, every photograph the same width, identical gaps, Helvetica + white background with no editorial rhythm.

The desired site is minimal, but **not generic**.

Its individuality should come from photographic sequencing and proportion.

---

# 38. Design decision principle

Whenever there is a choice between:

```text
showing more
```

and

```text
leaving more space
```

prefer leaving space unless showing more creates an important photographic relationship.

Whenever there is a choice between:

```text
adding interface
```

and

```text
allowing the browser to behave normally
```

prefer normal browser behaviour.

Whenever there is a choice between:

```text
making the site look artistic
```

and

```text
letting the photography create the artistic character
```

choose the photography.

---

# 39. First public version

Keep v1 deliberately small.

Minimum content:

```text
Home / Works index

One complete or reasonably developed photographic work
    initially likely Almost home

About

Notes
```

Support the underlying work-layout vocabulary from the beginning so additional projects do not require architectural redesign.

Do not delay publication because optional portfolio features are missing.

---

# 40. Future possibilities

Architecture may leave room for future additions such as:

* additional works
* exhibition information
* publications
* books
* bilingual project essays
* archival projects
* longer writing
* occasional embedded video
* custom domain email/contact information

These should not create implementation complexity in v1 unless the architecture would otherwise make them difficult later.

---

# 41. What Claude must produce

Using this document as the source of truth, create a **complete implementation-ready specification**.

The specification should be concrete enough to hand directly to Codex.

It should contain at least:

## Product definition

Explain the site purpose, scope and design philosophy succinctly.

## Information architecture

Define:

```text
routes
navigation
page hierarchy
URL structure
```

## Detailed page specifications

For every page type, specify:

```text
content
layout
desktop behaviour
mobile behaviour
interaction
empty / edge states
```

## Design system

Define actual values or clearly implementable formulas for:

```text
background
foreground
muted colours
typography
font stacks
font sizes
line heights
content widths
spacing scale
image widths
breakpoints
link states
focus states
```

Do not leave these as vague phrases such as "generous whitespace."

## Photography layout grammar

Define exactly how:

```text
single
pair
size
alignment
spacing
section breaks
```

work.

Include responsive rules.

## Content schema

Define TypeScript / Astro-compatible schemas for:

```text
works
notes
image sequences
metadata
draft state
```

Provide representative examples.

## Component architecture

Specify meaningful components and their responsibilities.

Avoid unnecessary abstraction.

## Repository structure

Provide the expected file / directory organisation.

## Image pipeline

Specify:

```text
source image expectations
generated formats
responsive widths
quality strategy
loading strategy
metadata handling
layout-shift prevention
```

## Accessibility

Define implementable accessibility requirements.

## SEO / metadata

Define the minimal technical implementation.

## Performance requirements

Provide reasonable measurable targets where useful.

Do not turn the project into a Lighthouse-score exercise.

## Acceptance criteria

For each major feature, provide concrete criteria Codex can use to judge whether the implementation is complete.

## Non-goals

Explicitly repeat important things Codex should **not** implement.

## Implementation order

Give a sensible sequence for Codex to build the application.

Prefer incremental checkpoints that result in a functioning site.

---

# 42. Instructions for specification quality

The resulting specification must avoid vague design language.

Bad:

> Images should have generous spacing.

Good:

> `normal`, `large`, and `pause` spacing use defined fluid values, with specified minimum and maximum values.

Bad:

> The website should be responsive.

Good:

> Define how each work-layout primitive transforms below each relevant viewport threshold.

Bad:

> Use elegant typography.

Good:

> Specify the font stack, weight, size, line-height and fallback behaviour for each textual role.

Codex should not need to invent the visual system while implementing.

At the same time, do not over-specify trivial HTML implementation details where normal semantic web conventions are sufficient.

---

# 43. Requirement priority

When resolving conflicts, use this priority order:

```text
1. integrity of photographic presentation
2. authored sequence and rhythm
3. visual restraint
4. readability and usability
5. image quality
6. performance
7. maintainability
8. implementation convenience
9. additional features
```

Do not sacrifice the first three merely to create a more conventional web application.

---

# 44. Final design character

The finished site should give approximately this impression:

> Someone has carefully arranged photographs and quietly left them here to be looked at.

Not:

> Someone built a beautiful photography website.

The distinction is important.

The website should have enough character that it does not feel like an off-the-shelf portfolio template, but the viewer should have difficulty pointing to a particular UI effect responsible for that character.

Most of the character should emerge from:

```text
photographs
sequence
scale
space
typography
editing
```

rather than decoration.
