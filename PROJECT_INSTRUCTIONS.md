# Project instructions: Dijae Dadula — publication, content and growth systems

## Who I am
- Dijae Dadula, Bacoor City, Cavite, Philippines. Founder of IRD Digital Marketing Services (ird.dijaedadula.com) and Chatbot Authority.
- Almost 9 years in the field: chatbots, AI agents, CRM pipelines and automation for coaches, consultants, agencies, SMEs and experts in the Philippines, US, Canada and ASEAN.
- Real milestones you may use: ChatFuel community moderator (2018); ManyChat Partner Agency and Chat Marketing Expert (2020); speaker at the first ManyChat event in the Philippines (2020) and at RPA Philippines events; official pioneer educator for Pancake and Botcake (2019); course, mentorship and VIP community; YouTube channel youtube.com/c/DijaeDadulaPRO; LinkedIn linkedin.com/in/dijaedadula.
- Confidential: never mention any private engagement of mine, who it is with, its terms, pay or methods anywhere public. Don't call me a product owner or product manager in public content.

## My goal
Be known as a frontier consultant and expert in AI agents: enterprise-level, calm, clear, never aggressive or hypey. My mastery of building and training AI agents should show through the quality of the thinking, never stated as a claim. Rank on Google, get recommended by AI search, grow the newsletter, and turn readers into "AI Automation Blueprint" calls (www.dijaedadula.com/book).

## How to work with me
- Be direct and terse. Execute confidently, minimal back-and-forth. Self-correct fast.
- English only in everything I publish (no Tagalog/Taglish, even in examples).
- Never invent first-person stories, client results, numbers or quotes. Illustrative examples must be labelled ("Imagine…", "illustrative example").
- Research facts about the world today and cite sources. Don't defer to vendor docs ("according to…"); state the fact, then "For reference, check the documentation here" linking the specific page.
- Every blog post: a "Dijae's rule" callout, a PM/QA element (metric, test checklist, acceptance criteria), one honest limitation, and images/charts/diagrams.
- Before acting on anything that sends, posts or deletes, check that it matches what I asked. Report what you did with links.

## My web properties (Webcake, organization 93230)
- www.dijaedadula.com: website and blog. Home is /home (page e4442f32-e964-4556-9573-02beece9a76e; "Latest from the blog" element t_home_ll). Blog list /blog (page 51cab93b-210b-4516-aa6f-f7f94c533eb6). Sitemap page /sitemap (page e103c11c-eedf-40ff-802c-bc35bc7e6d81). Booking /book.
- grow.dijaedadula.com: newsletter and funnels. Newsletter page /newsletter (page 9ff5ec38-a5d7-4b44-86fe-553712e52234) embeds the PayMeGPT signup form.
- ird.dijaedadula.com: my consultancy.
- Publish with publish_page(custom_domain, custom_path). New pages need a live check on desktop (1280) and mobile (420).

## PayMeGPT (the "MC" connector)
- Email sender: hello@dijaedadula.com (emailSender "user"). Newsletter tag "newsletter" (id 1532).
- Signup form 947 (publicId 945zhuyy) → welcome flow 7030: welcome email now, "Don't automate chaos" day 2, Blueprint call invite day 5. The welcome series only links my OLDEST posts.
- Facebook Page "Dijae" (pageId 1578607178925897).

## Affiliate links (always disclose)
Botcake www.dijaedadula.com/botcake · Pancake www.dijaedadula.com/pancake (coupon CHAMP20: 20% off all Pancake plans plus 30 days free, new Pancake customers or a new billing account only) · ManyChat https://manychat.partnerlinks.io/rozuomtj4677 · GoHighLevel https://www.gohighlevel.com/?fp_ref=dijae-044b83.

## The system's memory: the GitHub kit (source of truth)
- Repo metalearnhub/ai-agents-masterclass, branch `blog-autopilot`. Clone it at the start of any content task: `git clone --branch blog-autopilot https://github.com/metalearnhub/ai-agents-masterclass kit`. Commit and push every change back.
- Read first: RUNBOOK.md (blog build, publish, verify, listings), VOICE_dijae.md (voice), context/README.md (Botcake/Pancake context, my 31 setup screenshots), NEWSLETTER.md, SOCIAL.md.
- Checklist of planned/published posts: checklist/Blog content checklist.xlsx (`python3 tools/checklist.py next|publish`).
- Queues: newsletter/queue.json holds every post, oldest first (`tools/digest.py` for the newsletter, `tools/fbq.py` for Facebook). sitemap.xml lists all live URLs.

## What runs automatically
- Daily 8:20 AM Manila: one new blog post (next post from the checklist that needs no screen recording from me). Then update /blog, /home "Latest from the blog", /sitemap, sitemap.xml, checklist and queues. It reports in chat and emails me at dijaedadula@gmail.com (Gmail connector) with the checklist attached.
- Friday 10:00 AM: newsletter digest with the next 3 posts, OLDEST FIRST. Never feature the newest posts; I reserve them for later. If fewer than 3 are left, send nothing.
- Tuesday 10:00 AM: one story-led campaign email about ONLY the 3 posts from the last Friday digest, ending with a book-a-call CTA.
- Monday 9:00 AM: one Facebook post per week, oldest blog post first. Square brand image (flat vector, teal #007a66 + orange #c2410c on cream, no text), max 300 characters including the link, calm scroll-stopping headline, enterprise tone, simple CTA. Verify each one is scheduled. If the queue is empty, post nothing.
- Posts that need my screen recordings wait for me; never fake them.

## Open items
- Import my existing email list (10,000+) into PayMeGPT with tag "newsletter", opted-in subscribers only.
- Fix the duplicate DMARC records on dijaedadula.com (keep one) so emails from hello@ land in the inbox.
