# Community posting: FB group + Instagram (Dijae, Nov 14 2026)

Targets
- Facebook group "Chatbot Authority Philippines": https://www.facebook.com/groups/chatbotauthority (post as the page identity "Dijae", which the composer shows by default).
- Instagram @chatengrdijae: https://www.instagram.com/chatengrdijae/
- Source: the Dijae page posts (facebook.com/aidijae), in page order from the first brand post (Oct 15 2026) to the latest, then every new page post. Queue: tools/community/queue.json (`python3 tools/community/cq.py next group|ig`, `mark group|ig <slug> <url> <date>`, `sync` to append new page posts after each daily Facebook post). Apr-Sep 2026 page posts are excluded (Taglish and unverified figures); ask Dijae before adding any of them.

Cadence
- Instagram: one post every day, inside the daily 08:20 run, after the page post.
- FB group: TWO posts per week only (Tuesday and Saturday), so the group does not look automated. Never more than 2 in a rolling 7 days; check the `group` log in queue.json first.

How (browser: Claude in Chrome, Dijae's Windows Chrome; MC has no group or IG publishing for these accounts)
1. Image: `python3 tools/community/poster.py "<LABEL>" "<Headline\nline 2>" tools/community/img/<slug>.png <motif>` (motif: chat, ladder, funnel, gauge, shield, network). 1080x1350 dark theme, typographic, no AI art, so spelling is always exact. Upload with the file_upload tool from tools/community/img/ (files must be inside /home/claude/autopilot). Commit the image.
2. Group post: open the group, click "Write something...", type the text (use "→" lines, never "1." numbering: Facebook turns numbers into a broken list), end with "@everyone" and CLICK the "@everyone · Some members might receive notifications" suggestion so it becomes a real tag (it shows highlighted). Upload the image to the dialog's file input. Post. Then open the post and add 2-3 comments: (1) the blog link, (2) a practical hack, (3) a tutorial step or test tip. Value first, no hard selling.
3. Instagram: Create > Post, upload the image, Select crop > 4:5, Next, Next, caption (hook, 3-5 arrow lines, "Full guide on dijaedadula.com (link in bio).", 3-5 hashtags). Leave "Share to" Threads/Facebook OFF. Share. Then open the post and add 2 comments (hack + tip). No @everyone on IG.
4. Copy rules: English only, calm enterprise tone, a question that invites replies, no invented numbers or stories, confidentiality scan on all text (post and comments), AI-trainer career topics as general guides only, never any partner or job links.
5. Record: `cq.py mark ...` with the permalink, commit and push. Report both links.
6. If the browser is not connected or a step fails twice, skip the community post for that day, keep the queue unchanged and say so in the report.
