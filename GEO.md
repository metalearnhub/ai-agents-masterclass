# GEO: getting the site cited and recommended by AI assistants

Audit date: Nov 14, 2026. Read with RUNBOOK.md. Never promise rankings or recommendations.

## What the audit found
- robots.txt: `User-agent: * / Allow: /`. No AI crawler is blocked (OAI-SearchBot, GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot all fall under `*`). No `Sitemap:` line.
- /sitemap.xml and /llms.txt do not exist on the live domain: both URLs return the /home page. The sitemap.xml in this repo is not served. Fix needs a Webcake setting or support ticket; until then submit URLs by hand in Google Search Console and Bing Webmaster Tools.
- Domain root (/) serves the home page with canonical /home (checked live Nov 14). Any unknown URL also returns the home page with status 200 instead of a 404; the canonical tag limits the damage, but a real 404 page would be cleaner.
- Verified on the live server HTML (Nov 14, no JavaScript needed): /home has valid Person, ProfessionalService, WebSite and FAQPage JSON-LD, one h1 and six h2s; posts have their full text, headings and JSON-LD in the HTML, so AI crawlers can read them.
- Full survey of 46 posts (Nov 14): 42 already had BlogPosting + FAQPage + BreadcrumbList. what-is-an-ai-agent, dont-automate-chaos and turn-skills-into-ai-income had BlogPosting only. Fixed the same day: BreadcrumbList in html-box `h_bc01`, a visible four-question FAQ (text-blocks `t_fq00` to `t_fq4a` above Keep reading) and FAQPage in html-box `h_faq01`.
- Webcake gotcha: send patch_page calls one at a time. Two add-patches sent in parallel reported "Duplicate id" although they saved once, and the new elements were stored without defaults, which made publish fail on the build host ("Cannot convert undefined or null to object"). A second small patch_page update on the page re-saves it with defaults; then publish works. Never force a draft after such an error: re-read the page first.
- Search consoles (Nov 14): Google Search Console domain property is verified (52 indexed, 11 not indexed; the two submitted "sitemaps" are HTML pages and show errors). Bing Webmaster Tools site dijaedadula.com is verified by DNS and all 51 URLs were submitted by hand (quota 100 a day). After each new post: submit its URL in Bing URL Submission.
- https://dijaedadula.com (no www) shows a browser certificate error; only www works over HTTPS. Needs a fix at the domain or Webcake level.
- Analytics: the gtag snippet is in the server HTML of /home only, but Google Analytics and the Meta pixel load at runtime on posts through Webcake's global tracking (checked in a browser, Nov 14). Do not add a second tag.

## Standards for every new post (added Nov 14, 2026)
1. Answer first: the first paragraph answers the title question in 2-3 plain sentences that still make sense when quoted alone. Definitions use the "X is Y" form.
2. H2s phrased as the questions people ask an assistant. Sections of roughly 120-180 words, each understandable on its own.
3. Facts carry a number, a date and a linked source. No figure without a source opened in the same run.
4. At least one comparison table or numbered list where the topic allows it.
5. Name entities in full on first mention (product, company, place). "Dijae Dadula" appears in the byline and author schema, not forced into the body.
6. FAQ block in the exact h3/p shape so FAQPage schema is generated.
7. When a post is materially updated, change dateModified and show "Updated <date>" under the byline.

## Monthly check (first Monday)
Ask ChatGPT (search on), Perplexity, Google AI Mode, Copilot and Claude the prompts below. Log: mentioned yes/no, cited URL, which competitors appear. Keep the log in checklist/geo-log.csv.
- Who is Dijae Dadula?
- Best AI chatbot consultants in the Philippines
- Pancake vs Botcake vs ManyChat: which should I use?
- How do I set up Botcake AI with Pancake?
- What is an AI agent for a small business?
- How much does an AI chatbot cost in the Philippines?
- How do I qualify leads automatically in Messenger?

## Off-site (largest lever, needs Dijae)
AI answers lean on third-party mentions more than on a site's own pages. Priorities: Bing Webmaster Tools + Google Search Console verified, consistent name and one-line description on YouTube, LinkedIn, Threads and partner directories, guest posts or interviews on sites that already rank, and YouTube descriptions linking the matching blog post.
