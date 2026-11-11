# Blog styles: three variants of one brand (Dijae, Nov 1 2026)

Every post uses ONE of three styles. They share the brand (Inter, teal #007a66, orange #c2410c, the Webcake post template, SEO set, Dijae's rule, a PM/QA element, one honest limitation, FAQ with schema, references, CTA box, Keep reading). They differ in **how the post is written and organized, which components it uses, how the diagrams are drawn, and how the cover looks**.

## Rotation
- Run `python3 tools/style_next.py` before writing. It rotates A → B → C → A from the most recent post's `meta.json` "style".
- Put `"style": "A" | "B" | "C"` in `meta.json`. `make_post.py` checks the wrapper class, adds the style CSS to the page head and numbers the captions.
- Only swap the order if the topic clearly cannot work in that style (say why in the report). Never use the same style two days in a row.
- Samples to copy from: `examples/style_a_sample.html`, `examples/style_b_sample.html`, `examples/style_c_sample.html` (plus `examples/c_src.html` for a full A post).

## Dark theme for all graphics (Dijae, Nov 11 2026; applies to blog covers, blog diagrams, Facebook posters and LinkedIn content bank images)
- Mostly black and grey: matte dark gradient background from near-black `#0a0b0c` into graphite grey `#1f2224` (neutral, no blue or teal tint). Flat matte finish: no gloss, glow, shine, neon or texture noise.
- Accents are green only: `#3fbfa6` (strokes, marks) and `#4fd1b5` (labels, the one highlight). Use green sparingly as the accent; the rest is black, grey and white. No orange.
- Text is white (`#ffffff`) in heavy weights: headlines Inter 900 (Black), labels 800-900, body/secondary text 600 in light grey `#b5b9bd`. No thin or regular-weight text in graphics.
- Image prompts must say: "matte black-to-graphite-grey gradient background, flat matte finish, no gloss, no glow, mostly black and grey with green (#3fbfa6) accents only, no orange".
- Blog SVG diagrams: add `class="dk"` to the `<svg>`, a `<linearGradient>` background (`#1f2224` to `#0a0b0c`, unique id) on the base rect, boxes `#17191b` with `#3a3f43` strokes, the highlighted box `#10302a` with a 2px `#3fbfa6` stroke, gridlines `#2a2e31`, arrows `#8a8f94`, text `font-weight` 800+. The `dk` CSS (template/live_src.json, tools/style.css) makes svg-t/svg-num/svg-w white 800, svg-k/svg-ax green 900, svg-s light grey 600. Style C sketches: dot grid `#2a2e31`, dashed paths `#3fbfa6`, highlighter `#3fbfa6` at opacity 0.3.
- Posts published before Nov 11 2026 keep their light graphics unless Dijae asks to convert them.

## Style A: Field Guide (the original)
- **For**: how-to and setup topics, step-by-step builds.
- **Voice**: senior practitioner teaching a method. "Here is how to do it."
- **Wrapper**: `<div class="dd-article">`
- **Order**: problem intro (2 paragraphs) → `dd-tldr` "What you will get" → `dd-toc` → numbered H2 sections ("1. ...") → FAQ → CTA → References → Keep reading.
- **Components**: `dd-note` (Dijae's rule, blue), `dd-warn`, tables, `dd-code` copy blocks, numbered steps.
- **Diagrams**: process boxes and arrows on a dark matte gradient card (see Dark theme), grey outlines, green for the risky or final step, uppercase `svg-k` title. Caption: `<b>Figure N.</b>`.
- **Cover**: clean flat vector illustration, friendly rounded objects (chat bubbles, robots, calendars, charts), mostly black and grey objects with green accents on a matte black-to-graphite gradient background, flat matte finish, no gloss or glow, no text.

## Style B: Executive Brief
- **For**: decisions, comparisons, costs, strategy, metrics, anything a manager signs off.
- **Voice**: consultant briefing a decision-maker. Short, declarative, numbers first. No warm-up paragraphs.
- **Wrapper**: `<div class="dd-article dd-b">`
- **Order**:
  1. `dd-brief` dark panel "The 60-second brief": 3 numbered key points + one `dd-decision` line ("Decision: ...").
  2. `dd-tiles`: 3 key-figure tiles. Only sourced numbers or structural counts ("6 stages", "5 checks"). Never invented statistics.
  3. `dd-toc` (optional), then sections as **Moves**: `<p class="dd-kicker">Move 01 · Diagnose</p>` followed by an H2 that states the action ("Set the timing before the words"). The H2 still carries an `id`.
  4. Each Move opens with a `dd-move` 3-card row: What / Why it matters / Do this, then supporting text, tables and exhibits.
  5. `dd-bottom` "Dijae's rule" as a bold bottom-line statement (orange bar).
  6. `dd-check` decision checklist table (empty checkbox column) as the PM/QA element, plus a success metric.
  7. FAQ → CTA → References → Keep reading.
- **Diagrams (Exhibits)**: data style on a dark matte gradient card (see Dark theme). Gridlines `#2e3a42`, light grey `#8b98a3` axes, uppercase axis labels (`svg-ax`), bold value labels (`svg-num`), grey marks with one green highlight. Use timelines, bar charts, 2x2 matrices, scorecards, waterfalls. First text line inside the SVG: `EXHIBIT · <WHAT IT SHOWS>`. Caption: `<b>Exhibit N.</b>` + the takeaway in one sentence. Draw to scale: every label names a real value on the axis.
- **Tables**: dark header row (automatic).
- **Cover**: clean isometric flat illustration on a matte black-to-graphite gradient background, grey structures with green accents, flat matte finish, no gloss or glow: dashboards, stacked blocks, a pipeline of tiles, a control panel. Precise, corporate, generous whitespace, no text.

## Style C: Story Explainer (Q&A)
- **For**: concepts, beginner topics, myths, "what is / should I" questions. Written so AI search and Google can lift answers.
- **Voice**: a calm expert explaining to a smart friend. Warm, concrete, plain English.
- **Wrapper**: `<div class="dd-article dd-c">`
- **Order**:
  1. `dd-scene` "Picture this · illustrative": a short scenario. Always labelled illustrative; never a real client.
  2. `dd-plain`: one-sentence plain-English definition with the key phrase in `<mark>`.
  3. `dd-words`: 3-5 glossary chips (`<span><b>Term</b> meaning</span>`).
  4. H2s written as the questions people ask ("How often should you follow up with a lead?"), each followed by `<p class="dd-short"><b>Short answer:</b> ...</p>`, then the detail.
  5. `dd-myth` Myth / Reality pair (one or two per post).
  6. `dd-sticky` sticky note for "Dijae's rule".
  7. "What can you set up today?" as `<ol class="dd-try">` (big outlined numerals). Include the PM/QA element as a short "How you will know it works" list or table.
  8. FAQ → CTA → References → Keep reading.
- **Diagrams (Sketches)**: notebook look on a dark matte gradient card with a dot-grid `<pattern>` (`#2b363d`), dashed teal paths (`stroke-dasharray="8 7"`, round caps, 2.5-3px), hollow circles for stops, rounded speech bubbles, an orange highlighter rectangle (`#ffd8bf`, opacity 0.7) behind one key phrase, handwritten notes with class `svg-hand` (Caveat font, loaded automatically). Use journeys, before/after, cause-and-effect, simple maps. Caption: `<b>Sketch N.</b>`.
- **Cover**: layered paper-cut editorial illustration on matte black and graphite paper layers with a few green paper accents with soft shadows, no gloss, a small scene that tells the post's story. No text.

## All styles
- Unique SVG ids per figure (prefix with the style letter and figure number, e.g. `sb1a`).
- Render every SVG with `tools/svgr.py` (or Playwright) and look at it: no clipped or overlapping text.
- Run the confidentiality scan exactly as before. English only. No invented stories, numbers or quotes.
- Mobile: B and C grids stack to one column under 560px automatically.
