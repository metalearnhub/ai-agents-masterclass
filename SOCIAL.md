# Facebook posts (PayMeGPT / MC connector) — rules from Dijae, Oct 29 2026

- Page: "Dijae", pageId 1578607178925897 (platform facebook). Tool: mcp__MC__post_to_social_media (post now, or scheduledTime ISO with +08:00).
- PayMeGPT has no built-in "new blog post -> Facebook" trigger, so the DAILY blog run does this itself.

## What runs every day (inside the daily 08:20 blog run) — OLDEST FIRST, newest posts are the buffer
1. ONE POST PER DAY, AT THE SAME TIME AS THE BLOG RUN: right after the day's blog is published, post the OLDEST blog not yet on Facebook (`python3 tools/fbq.py next`) to the page immediately (no scheduledTime). Never jump to the newest post: new blogs join the end of the queue and wait their turn. Mark it: `python3 tools/fbq.py mark <date> <slug> "posted with the daily run" <postUrl> <imageUrl>`. If `next` returns {"none":true}, post nothing.
2. LINKS: `python3 tools/fbq.py pending` lists scheduled entries without a Facebook link. Call mcp__MC__list_scheduled_posts (platform facebook, includeAll true); for each published one, build the link from postId (`1578607178925897_<N>` -> `https://www.facebook.com/1579937777474981/posts/<N>`) and run `fbq.py seturl <slug> <url>`.
3. CONTENT BANK: mirror every Facebook entry into `metalearnhub/dijae-cv-landing/assets/content-bank/posts.json` under "facebook" (slug, blogTitle, blogUrl, message, image, alt, when, fbUrl). The app (Facebook tab) shows the post, image and "View on Facebook" link; LinkedIn cards for the same blog show "Also on Facebook". Commit and push that repo.
4. Never post a blog twice: before posting, check `fbq.py done <slug>` AND the live page (`list_scheduled_posts` source "page") for the blog URL. Posts Dijae made by hand count as done.
5. VERIFY: immediate posts return a postUrl; scheduled ones must appear in list_scheduled_posts with status "scheduled". Report both.
- History: the Monday-only weekly rule was retired Oct 29 2026. Post 5182 (ai-chatbot-for-small-business, Mon Nov 2 09:00) and post 5248 (automate-lead-follow-up, Thu Oct 29 18:00) stay as scheduled. data-privacy-act-chatbots-philippines went out early on Oct 29 (before the oldest-first rule was confirmed) and counts as done.

## Image: always the "creative" (2nd) style from the content bank
- Portrait 3:4, soft cream background #f3ece0. Top-left: small letter-spaced teal (#007a66) uppercase pillar label, then a large bold dark Inter-style headline (2-3 lines). Lower two-thirds: flat vector illustration in teal #007a66 + warm orange #c2410c showing the post's idea. Bottom-left: white rounded pill "DIJAE DADULA". No other text.
- mcp__MC__generate_image, model gpt-image-2.5-flare, aspect 3:4, prompt spells the label and headline exactly ("reading exactly ..."). Use the content bank's artTitle/pillar when a LinkedIn post exists for the same blog.
- ALWAYS look at it (render_preview url, width 800) and check spelling, word spacing and layout. Regenerate if anything is off. Use the paymegpt.com image URL directly in the post.

## Copy rules (max 300 characters INCLUDING the link)
- Line 1 = headline: short, scroll-stopping, calm and confident. A sharp contrast or reframe, not hype. No emojis, no ALL CAPS, no clickbait.
- 1-2 short sentences: the insight from the post, for business owners and leaders. Enterprise/consultant tone.
- Simple CTA line + link: "The plain-English guide:" / "The full method:" / "Read the guide:" then the blog URL.
- Never mention: job titles, any private engagement or who it is with, clients' names, invented results or numbers.
- English only. No hashtags in the caption. Count characters with Python before posting.

## Public-content rules
Follow CONFIDENTIALITY.md. Run the private zero-hit scan on every caption before posting or scheduling. AI-trainer career posts are framed as general career guides; never add the job-roles link to Facebook.
