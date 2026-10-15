# Newsletter runbook (PayMeGPT / MC connector)

- Sender: hello@dijaedadula.com (emailSender "user"). Audience: tag **newsletter** (tag id 1532). Always target `tagIds: [1532]`.
- Signup form: PayMeGPT form 947 (publicId 945zhuyy), embedded on grow.dijaedadula.com/newsletter (Webcake page 9ff5ec38-a5d7-4b44-86fe-553712e52234, element pmg_form). Each signup is tagged and runs flow 7030 "Newsletter Welcome Series" (welcome now, day 2 "Don't automate chaos", day 5 Blueprint call invite).
- Voice: same as VOICE_dijae.md. English only, authority, no invented stories, numbers or client results. Short paragraphs, mobile-friendly, one clear CTA.
- Every email ends with the footer below (PayMeGPT broadcasts also add their own unsubscribe link).

## Friday (every week): Blog digest
- Run on Friday's daily run, after the day's post is published.
- Content: the 3 newest posts (from sitemap.xml lastmod / the checklist Publish date). For each: title (linked), 2 sentences on the problem it solves and one takeaway, "Read the guide" link.
- Subject pattern: "3 new guides: <short hook from the strongest post>".
- create_broadcast(channel email, name "Digest YYYY-MM-DD", subject, htmlContent, tagIds [1532], emailSender "user") then send_broadcast(channel email, broadcastId, scheduledAt "YYYY-MM-DDT10:00:00", timezone "Asia/Manila").
- Save a copy in newsletter/YYYY-MM-DD-digest.html and log it in newsletter/log.md.

## Tuesday (every week): Story / campaign email
- Built on Tuesday's daily run. Theme = the most useful idea from the previous Friday's 3 posts.
- Shape: hook (a common problem business owners face) -> the insight from the posts, stated with authority -> one practical step they can do this week -> CTA to book a free AI Automation Blueprint call (https://www.dijaedadula.com/book) for their business, or to learn (link the relevant post).
- Story-led is allowed ONLY with real facts Dijae stated (VOICE_dijae.md, profile) or clearly hypothetical "Imagine a clinic that..." scenarios. Never invent a client story.
- Subject: curiosity + benefit, under 50 characters. Schedule for 10:00 Asia/Manila the same day.

## Footer (append to every email)
<hr style="border:none;border-top:1px solid #e3e8ee;margin:24px 0 12px 0"><p style="font-size:12px;color:#888">You are receiving this because you subscribed to Dijae Dadula's newsletter at dijaedadula.com. IRD Digital Marketing Services, Bacoor City, Cavite, Philippines.</p>

## Report
Mention the scheduled email (subject, send time, broadcast id) in the daily report and email to Dijae.
