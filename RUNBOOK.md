# Daily blog post runbook: www.dijaedadula.com

One run = write, publish and verify ONE new blog post for Dijae Dadula, then update the blog list, the /sitemap page, sitemap.xml and the content checklist. Work unattended: do not ask questions; make the reasonable call and note it in the final report.

## 0. Setup
```bash
git clone --branch blog-autopilot https://github.com/metalearnhub/ai-agents-masterclass kit && cd kit
(cd tools && npm install --no-audit --no-fund)   # playwright + fonts for height measurement (Chromium is preinstalled; do NOT run "playwright install")
python3 tools/checklist.py next
```
- If it prints `{"none":true}`: every post that needs no screen recording is done. Do NOT write anything. Report: "Queue empty: the remaining posts need Dijae's screen recordings (list them from the checklist)". Stop.
- Otherwise that row is today's post (Working title, Main search target, Funnel stage, Why it wins). Today's date = Asia/Manila date.
- Webcake tools (mcp__Webcake__*), PayMeGPT tools (mcp__MC__*) load through ToolSearch.

## 1. Fixed facts
- Webcake organization_id **93230**. Domain **www.dijaedadula.com**.
- Blog list page id `51cab93b-210b-4516-aa6f-f7f94c533eb6` (path `blog`). Sitemap page id `e103c11c-eedf-40ff-802c-bc35bc7e6d81` (path `sitemap`).
- Affiliate links (add `rel='sponsored nofollow'`): Botcake `https://www.dijaedadula.com/botcake`, Pancake `https://www.dijaedadula.com/pancake`, ManyChat `https://manychat.partnerlinks.io/rozuomtj4677`, GoHighLevel `https://www.gohighlevel.com/?fp_ref=dijae-044b83`.
- Pancake coupon **CHAMP20**: 20% off all Pancake plans plus 30 days free, for new Pancake customers or a new billing account only. Always state the condition.
- Booking CTA: `https://www.dijaedadula.com/book` ("Book a free AI Automation Blueprint call"). Newsletter: `https://grow.dijaedadula.com/newsletter`.
- Existing posts for internal links: every `<loc>` in `sitemap.xml`. Link 2-4 relevant ones in the body and 3 in "Keep reading".
- The validator warning "settings.bhet has a <style> with UNSCOPED selector(s) ... .dd-article" is a known false positive (all rules are scoped to the article wrapper). Ignore it.

## 2. Voice and content rules (read VOICE_dijae.md fully)
- **English only**. No Tagalog/Taglish anywhere, including sample customer messages.
- Senior authority, almost 9 years in the field. Plain, direct, practical. No hype.
- **Never invent first-person practices, numbers, client names or client stories.** Use recommendations ("I recommend", "My rule") and clearly labelled illustrative examples ("Every figure below is an illustrative example").
- Every post has: a `Dijae's rule` callout, a PM or QA element (success metric, test checklist, acceptance criteria or failure modes), and one sentence starting "An honest limitation:".
- Facts about the world (prices, rules, platform features, statistics) must be researched with WebSearch/WebFetch today and cited in References. If you cannot verify a number, leave it out.
- Vendor docs: never write "according to the documentation". State the fact, then "For reference, check the documentation <a href='SPECIFIC PAGE'>here</a>."
- Length 1,300-2,200 words. 5-8 H2 sections + FAQ (3-5 questions).

## 3. Write `posts/<slug>/article.html`
Read `context/README.md` first. On Fridays and Tuesdays also follow NEWSLETTER.md. On Mondays also follow SOCIAL.md. Copy the structure of `examples/c_src.html` (best reference) and `examples/a_src.html`, `examples/b_src.html`. Order:
1. `<div class="dd-article">` wrapper
2. `<!--COVER-->` (replaced by the cover image)
3. 2 intro paragraphs (problem, who it is for, what they will get)
4. `dd-tldr` box, `dd-toc` nav with anchor links
5. H2 sections with `id`s. Use the components: `dd-note` (with `<span class="dd-note-label">Dijae's rule</span>`), `dd-warn`, `dd-table-wrap` tables, `dd-code` copy blocks (`<div class="dd-code"><button class="dd-copy" type="button">Copy</button><pre><code>...</code></pre></div>`), numbered steps.
6. **At least 2 inline SVG figures** (diagram, chart, flow or comparison). Build them like `examples/svgs_examples.py` (viewBox width 640, classes svg-k/svg-t/svg-s/svg-o/svg-w/svg-ws, colors #007a66 teal, #5b9e90, #e8f4f1, #c2410c orange, #fff4ec, #f6f8fa background, `<title>` + `<desc>` for accessibility, unique ids per figure). Caption: `<figcaption><b>Figure N.</b> ...</figcaption>` (auto-numbered). Render each SVG to PNG with Playwright and LOOK at it: no overlapping or clipped text.
7. `<h2 id="faq">Frequently asked questions</h2>` then `<h3>Q</h3>\n<p>A</p>` pairs (this exact shape feeds the FAQ schema)
8. `dd-cta` box (affiliate links where relevant + booking link), `<h2>References</h2>` `<ol class="dd-refs">`, `<h2>Keep reading</h2>` `<ul class="dd-more">` ending with "See all posts on the blog".
Use normal double quotes in your HTML; the build converts everything to the quote-free format Webcake needs.

## 4. Cover image
- `mcp__MC__generate_image`, model `gpt-image-2.5-flare`, aspect 16:9. Style to match existing covers: clean flat vector illustration, teal (#007a66) and warm orange (#c2410c) accents on a soft cream background, friendly rounded objects (chat bubbles, robots, calendars, charts, price tags) that show the topic, NO text or letters in the image.
- Re-host with `mcp__Webcake__upload_images` (pass the generated https URL) and use the returned statics.pancake.vn URL. Look at the image (render_preview url) before using it.

## 5. `posts/<slug>/meta.json`
```json
{"slug":"kebab-case-slug","cat":"<one of: AI agents and workflows | CRM and automation that sells | Monetize your skills with AI | AI quality and evaluation | Your career in the AI era | Trends, tools and stories>",
 "short":"Breadcrumb name","h1":"Full title","dek":"One or two sentence subtitle",
 "seo":"SEO title under 65 chars | Dijae Dadula","desc":"Meta description 140-160 chars","kw":"comma, separated, keywords, Dijae Dadula",
 "cover":"https://statics.pancake.vn/...","cover_alt":"Describe the cover","date":"YYYY-MM-DD"}
```
Slug: short, keyword-first, not already in sitemap.xml.

## 6. Build and create
```bash
python3 tools/make_post.py posts/<slug>     # writes source.json + geometry.json, prints geometry
```
- `mcp__Webcake__create_page` with name `Blog Post - <short> (www /<slug>)`, organization_id 93230, dry_run false, source = contents of `posts/<slug>/source.json`. Save the page_id into `posts/<slug>/page.json`.
- `mcp__Webcake__publish_page` page_id, custom_domain `www.dijaedadula.com`, custom_path `<slug>`, dry_run false.

## 7. Verify live (mandatory)
- `render_preview` url `https://www.dijaedadula.com/<slug>?v=1` full_page true, width 1280, then width 420. Each result says where the JPG was saved.
- `python3 tools/gap.py <jpg> 1280` (and 420). Then `python3 tools/crop.py <jpg> bottom.png` and Read the PNG.
- Correct: the article ends (Keep reading list) and there is ~110-150px (desktop) / ~90-120px (mobile) of space before "Get one practical idea like this every week".
- Too much space: reduce. Overlap (article text running into the newsletter box): increase by the overlap plus 130. Patch with:
  `patch_page(page_id, dry_run=false, patches=[{"op":"update","id":"eb_2120","styles":{"desktop":{"height":DH},"mobile":{"height":MH}}},{"op":"update","id":"h_css2121","styles":{"desktop":{"top":eb_top_d+DH+47},"mobile":{"top":eb_top_m+MH+39}}},{"op":"update","id":"sec_2108","styles":{"desktop":{"height":eb_top_d+DH+57},"mobile":{"height":eb_top_m+MH+49}}}])`
  (eb_top values are in geometry.json), re-publish with the same domain and path, re-render with a new `?v=` and re-check. Max 3 rounds.
- Also look at the top of the page (H1, dek, byline, cover) and at least two figures.

## 8. Blog list, home page "Latest from the blog", sitemap, checklist
```bash
# get_page(51cab93b-...) -> the result file path (or save the JSON) then:
python3 tools/blog_patch.py <get_page_result.json> <slug> "<H1>" "<one-sentence blurb>"
# patch_page(blog id, patches=blog_patch.json contents, dry_run=false); publish_page(custom_domain www.dijaedadula.com, custom_path blog)
# get_page(e103c11c-...) then:
python3 tools/sitemap_patch.py <get_page_result.json> "<group>" <slug> "<short title>" "<short blurb>" <date>
# groups: "AI agents and chatbots" | "Sales and lead automation" | "Case studies" | "Careers and income in the AI era"
# patch_page(sitemap id, ...); publish_page(custom_path sitemap)
# get_page(e4442f32-e964-4556-9573-02beece9a76e) (/home, saved to a file) then:
python3 tools/home_patch.py <get_page_result_file> <slug> "<H1>"
# patch_page(home id, patches=home_patch.json contents, dry_run=false); publish_page(custom_domain www.dijaedadula.com, custom_path home)
python3 tools/checklist.py publish "<tab>" <#> https://www.dijaedadula.com/<slug> <date>
```

## 9. Save state (mandatory, or tomorrow's run repeats this post)
```bash
git add -A && git commit -m "Publish <slug>" && git push origin blog-autopilot
```
Do not commit node_modules (it is in .gitignore).

## 10. Report to Dijae (SendUserMessage, then final reply)
Short, English: post title + live URL, what visuals it has, any judgment calls, anything that failed. Send the updated `checklist/Blog content checklist.xlsx` and `sitemap.xml` with SendUserFile. If something blocked publishing, say exactly what and leave the checklist row as Planned.
