# LinkedIn system (content bank)

- Content bank: https://paymegpt.com/p/TE836bKrZ (PayMeGPT page 8185, passcode 1023). The PayMeGPT page is a small shell; the app UI is `metalearnhub/dijae-cv-landing/assets/content-bank/app.html` and the posts are `.../posts.json`. To change the UI or add posts, edit those files and push. Never edit the PayMeGPT page unless the shell itself must change.
- Two images per post: `image` (diagram, 1080x1350 PNG in the repo) and `art` (AI illustration, flat vector, teal #007a66 + orange #c2410c on cream, no text, generated with mcp__MC__generate_image gpt-image-2.5-flare 3:4, hosted on paymegpt.com). The page overlays `artTitle` + pillar + DIJAE DADULA on the art in the browser and downloads it as `artFile`.
- Two text versions per post (`post` and `post2`, optional `comment2`): same verified facts, different hook and angle, for reposting or recycling later. Verification is tracked per version (`p05` and `p05#2`); a post counts as Verified once either version is posted, and shows "1 of 2" until both are.
- Cadence: Tuesday and Thursday mornings Manila time. One hook line, short lines, one closing question, 3 hashtags, under 1,300 characters. Links only in the first comment.
- Every LinkedIn post points to a LIVE blog post in its first comment. Only link URLs listed in sitemap.xml.
- Confidentiality: zero-hit scan for micro1, labs, rubric, AI-trainer first-person lines before publishing.
- Stats must come from a primary source opened in the session. HBR 2011 speed-to-lead figures are paywalled: cite only its conclusion.

## Calendar

| # | Date | Pillar | Hook | Blog post (first comment) | Matching upcoming blog (autopilot) |
|---|---|---|---|---|---|
| 01 | 2026-10-15 | Development | An AI agent is software. Ship it like software. | /dont-automate-chaos |  |
| 02 | 2026-10-20 | Optimization | Change one thing. Then measure. | /how-to-test-an-ai-chatbot |  |
| 03 | 2026-10-22 | Review & audit | If an agent acted, you should be able to see why. | /what-is-an-ai-agent |  |
| 04 | 2026-10-27 | AI training, explained | "Training an AI" rarely means building a model from scratch. | (sources only) |  |
| 05 | 2026-10-29 | Lead response | The first reply wins more deals than the best reply. | /automate-lead-follow-up | Why Your Business Is Losing Customers in Messenger |
| 06 | 2026-11-03 | Cost control | Ask what your AI costs per resolved conversation. | /chatbot-roi-metrics | How Much Does an AI Chatbot Really Cost |
| 07 | 2026-11-05 | Human handoff | Customers don't hate AI. They hate being trapped by it. | /qualify-leads-messenger-automatically | When Should an AI Chatbot Hand Off to a Human? |
| 08 | 2026-11-10 | Instructions | Your AI agent is only as good as its instructions. | /ai-agent-instructions-template | How to Make Your Chatbot Sound Human |
| 09 | 2026-11-12 | Integrations · MCP | A chatbot answers. An agent acts. MCP is how it acts. | /what-is-mcp | Build an AI Agent That Uses Your Business Tools With MCP |
| 10 | 2026-11-17 | Process first | AI doesn't fix a broken process. It runs it faster. | /dont-automate-chaos |  |
| 11 | 2026-11-19 | Accountability | Your chatbot speaks for your business. Legally, too. | /how-to-test-an-ai-chatbot |  |
| 12 | 2026-11-24 | Pricing | Clients don't buy a chatbot. They buy what changes after it's live. | /price-ai-automation-services |  |
| 13 | 2026-11-26 | Client system | Get clients without living on social media. | /get-more-clients-with-ai | How to Turn Blog and Search Traffic Into Automated Chat Leads |
| 14 | 2026-12-01 | Assistive AI | Assist first. Automate second. | /what-is-an-ai-agent |  |

When an upcoming blog post goes live, swap or add its URL in that LinkedIn post's first comment (posts.json) before the LinkedIn date.

Status: #01 posted and verified 2026-10-15.
