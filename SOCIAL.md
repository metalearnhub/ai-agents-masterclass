# Weekly Facebook post (PayMeGPT / MC connector)

- Page: "Dijae", pageId 1578607178925897 (platform facebook). Tool: mcp__MC__post_to_social_media with scheduledTime.
- Cadence: ONE post per week, every MONDAY 09:00 Asia/Manila. Order: blog posts OLDEST FIRST (`python3 tools/fbq.py next`), one per week, until the newest.
- Done on the MONDAY daily run: schedule the post for the FOLLOWING Monday 09:00 (+08:00), then `python3 tools/fbq.py mark <that date> <slug> "<info>"`. History: #1 what-is-an-ai-agent posted 2026-10-15; #2 turn-skills-into-ai-income scheduled Mon 2026-10-19 (post id 4836). The Mon 2026-10-19 run schedules #3 for Mon 2026-10-26.
- SOURCE OF POSTS: newsletter/queue.json (fed daily by `digest.py add`). Before picking, sync it with the live site: every <loc> in sitemap.xml that is a blog post and missing from the queue must be added (in publish order) so nothing is skipped. Only use a post whose URL loads live.
- NEVER RUN OUT / STOP RULE: if `fbq.py next` returns {"none":true}, do NOT create an image or post anything; just report "Facebook queue empty, nothing scheduled".
- VERIFY: after scheduling, call mcp__MC__list_scheduled_posts (platform facebook) and confirm the post is there with status "scheduled" and the right time. Report the post id. If it is missing, retry once, then report the failure.

## Image
- mcp__MC__generate_image, model gpt-image-2.5-flare, aspect 1:1. Same brand style as blog covers: clean flat vector, premium enterprise consulting feel, teal #007a66 + warm orange #c2410c on soft cream, generous empty space, rounded friendly objects that show the post's core idea (e.g. robot assistant, calendar, CRM card, chat bubbles, charts). NO text, letters, numbers or logos.
- Look at it (render_preview url), then re-host with mcp__Webcake__upload_images and use the statics.pancake.vn URL.

## Copy rules (max 300 characters INCLUDING the link)
- Line 1 = headline: short, scroll-stopping, calm and confident. A sharp contrast or reframe, not hype. No emojis, no ALL CAPS, no clickbait. Examples: "A chatbot answers. An agent acts." / "The tools come last."
- 1-2 short sentences: the insight from the post, framed for business owners and leaders. Enterprise/consultant tone; frontier expert voice; speaks from judgment, not tutorial.
- Simple CTA line + link: "The plain-English guide:" / "The full method:" / "Read the guide:" then the blog URL.
- Never mention: job titles, any private engagement or who it is with, clients' names, invented results or numbers. Expertise shows through the clarity of the idea, not claims.
- English only. No hashtags in the caption.
- Count characters with Python before posting.
