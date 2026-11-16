# PayMeGPT (MC) -> Vercel + Supabase migration (Dijae, Nov 16 2026)

Decision: stop using PayMeGPT. Rebuild every project on Vercel (static/Next sites from GitHub repos) with Supabase (project qbubwemdvwflxvxwesrl, ap-south-1) as the database and API layer.
Nov 16 update: Dijae is permanently blocked from PayMeGPT, so nothing can be exported. Rebuild from GitHub + Supabase only; skip what only lived in PayMeGPT.
Dijae's answers (Nov 16, earlier): deploy by linking GitHub repos in Vercel; sign in to MC once so everything can be exported; scope = web apps + Supabase, landing pages, newsletter sending, and PM University (keep its passcode gate).

## Done
- [x] 37 PayMeGPT-hosted images (Facebook posters, content bank) mirrored to statics.pancake.vn; references rewritten in dijae-cv-landing posts.json, newsletter/queue.json, fb_pending.json. Map: migration/pmg_image_map.json.

- [x] Removed PayMeGPT runtime scripts and added vercel.json in dijae-cv-landing, drivefolio, dijae-dadula-ai-native-systems-architect-cv; ai-trainer-defense coach iframe replaced with a notice.
- [x] Newsletter signup rebuilt: Supabase tables nl_subscribers + nl_sends, edge function `nl` (subscribe POST, one-click unsubscribe ?u=token, welcome email through Zoho SMTP port 465 once secrets exist). grow.dijaedadula.com/newsletter (Webcake 9ff5ec38) now posts to it.

- [x] Vercel (account dijae0-8708, GitHub app installed on 4 repos only): ai-trainer-defense.vercel.app (+ /tasker/), drivefolio-wheat.vercel.app, dijae-cv-landing.vercel.app (+ /assets/content-bank/app.html), dijae-dadula-ai-native-systems-arch.vercel.app. Pushes to main auto-deploy.
- [x] Tasker sign-in: PayMeGPT email-code webhook removed; one-time device PIN (hashed in tk_config, 1-year session, locks after 10 wrong tries). Email codes via Zoho return automatically once secrets exist.

- [x] DNS (Namecheap, Nov 16): cv and drivefolio CNAMEs moved from GitHub Pages to Vercel; tasker.dijaedadula.com added (root redirects to /tasker/); duplicate _dmarc removed (kept rua=hello@). All three show Valid Configuration in Vercel.

## Supabase secrets to set (Dashboard > Edge Functions > Secrets), never in chat or git
ZOHO_SMTP_USER (mailbox login), ZOHO_SMTP_PASS (Zoho app-specific password), NL_FROM (hello@dijaedadula.com), optional ZOHO_SMTP_HOST (smtp.zoho.com, or smtppro.zoho.com for organization accounts).

## PayMeGPT dependencies found in GitHub repos
| Repo | Depends on | Replace with |
|---|---|---|
| dijae-cv-landing (content bank + CV) | /api/landing/context (page context XHR) | static, or Supabase edge function |
| dijae-dadula-ai-native-systems-architect-cv | /api/landing/context | static |
| drivefolio | /api/landing/context; data already in Supabase (df_* tables, edge functions) | static + Supabase |
| ai-trainer-defense (+ /tasker) | PayMeGPT coach agent embed (COACH_URL); tasker already on Supabase | Supabase edge function calling an LLM API |
| pm-university | PIN login (generate-pin / verify-pin), Google Sheet data via PayMeGPT sheet API, coach agent embed, /api/landing/context | Supabase table + PIN edge function + LLM edge function; passcode gate kept |

## Blocked until MC is signed in once (export list)
- Every landing page's HTML (list_landing_pages / get_landing_page), incl. grow.dijaedadula.com newsletter page and funnels.
- Contacts with tags (newsletter id 1532), form 947 submissions, other forms.
- Flows (welcome flow 7030), broadcasts/templates, automations, widgets/agents (prompts + knowledge).
- PM University sheet data (page 7953).
- Hands-off pages 7509/7510: export to a PRIVATE place only, never publish.

## Needs Dijae
1. Sign in to MC (connector card) for one export run.
2. In Vercel: Add New Project -> import each metalearnhub repo (static, no build command). Then point domains (drivefolio.dijaedadula.com, grow.dijaedadula.com, etc.) to Vercel.
3. Email sending provider for newsletter/welcome flow (proposed: Resend, sender hello@dijaedadula.com, needs DNS records; fix duplicate DMARC first).
4. Facebook/Instagram posting: MC was the Facebook page poster. Replacement: browser posting (Chrome extension) or a Meta app token in a Supabase edge function.

## Plan (order)
1. Export everything from MC into Supabase tables (pm_pages, contacts, forms, submissions, flows, broadcasts) and HTML into repos.
2. Rebuild pages as static sites per repo; swap PayMeGPT APIs for Supabase edge functions.
3. Newsletter: contacts table + send edge function (provider API) + scheduled jobs (pg_cron) for welcome flow, Friday digest, Tuesday story email.
4. Point domains to Vercel, test desktop/mobile, then retire MC.

- Content bank (dijae-cv-landing.vercel.app/assets/content-bank/app): passcode gate now served by the Supabase content-bank function (action unlock, hash in table cb_config). A correct passcode issues a device key; verifications sync from cb_state.
- Newsletter broadcasts: nl_broadcasts table + pg_cron job nl-broadcasts + edge function nl (run action). Tested Nov 16 with a test send.
- PM University: repo pm-university rebuilt for Vercel; passcode gate + progress sync via Supabase function pmu (tables pmu_rows, pmu_config, pmu_keys). Coach copies prompts for Claude/ChatGPT. Old progress data was not recoverable.
- AI Trainer Defense: coach button copies the report with debrief instructions and opens Claude/ChatGPT.
- Content bank: next-up post on top, posted posts grouped at the bottom.
- CRM backlog (low priority, Dijae Nov 16): email analytics per audience. Save the audience (tag, status, pipeline/stage) on each broadcast, show sent/failed/unsubscribed per audience on the dashboard and per email. Opens/clicks would need tracking pixels and redirect links.
- CRM Apps gallery (Nov 17): table crm_apps (30 apps seeded), visit beacon function hit -> app_hits (daily hashed visitor id, no IP stored), API function crm-apps. Tracked: crm, tasker, pm-university, content-bank, ai-trainer-defense, drivefolio, cv-landing, architect-cv. Not tracked yet: Webcake sites, jobs board.
