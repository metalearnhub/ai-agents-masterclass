# Pancake + Botcake combined playbook (source: official docs exports, Oct 2026)

Sources: botcake_all_pages_1.docx, pancake_all_pages.docx (docs.pancake.biz). English UI labels verified from official screenshots (render_preview).

## Who does what
| Layer | Tool | Role |
|---|---|---|
| Channels | Messenger, Instagram, WhatsApp, TikTok, Zalo, Viber, Telegram, Line, Chat Plugin | Botcake supports 9 platforms |
| Automation brain | Botcake | Flows, Keywords, Default reply, Welcome, Main menu, Ice breaker, Sequences, Rules, Comments, Broadcasts, Growth tools |
| AI that REPLIES | Botcake AI | Agents w/ instructions, file library, auto-orders to Pancake POS, CRM capture, AI block in flows |
| Human inbox | Pancake | Unified inbox, tags, round robin assignment, quick replies, CRM, POS orders, stats |
| AI that SUGGESTS | Pancake AI Assistant | Reply suggestions (3), AI quick replies (/), sentiment, QA scoring. Does NOT send. "If you want AI to reply automatically, use Botcake AI" |
| Orders | Pancake POS | Products sync into Botcake; auto-order from Botcake AI or flows |
| CRM | Pancake CRM (paid add-on, 14-day trial) | Botcake custom fields / webform / AI info capture map to CRM fields |

## Glue settings (exact paths)
- Botcake: Settings → Customer tags (Tag Configuration): "Sync Tag from Pancake to Botcake in real-time", "Sync Pancake Tag from Botcake to Pancake in real-time", "Automatically tag customers when they message the Fanpage for the first time". Tags: create in Pancake → sync to Botcake; attach/remove sequences per tag.
- Pancake: Settings → General → 3. Ecosystem Synchronization: 3.1 "Display [Botcake Reply] notification when Botcake sends an automated response"; 3.2 Real-time Botcake Tag Synchronization; 3.3 Automatically Create Orders in POS (when message contains phone number).
- Botcake: Settings → General → "Conversation Status on Pancake When the Bot Responds": actions on fail/success + time for bot to pause while staff is replying. Bot reply failed options: Mark Bot reply failed / Mark unread / Add or remove Pancake tag automatically when Botcake is failed.
- Botcake Custom Field: Settings → Custom Field → + New Custom Field: Attribute Name, Data Type, CRM Field (only if Page connected to Pancake CRM), Description. AI responses saved to custom fields = String only.
- Botcake Webform: Settings → Webform → Add new; component Settings tab: User field / CRM fields.
- Botcake AI info capture: Agent → Information Management: "Data description for AI collection" + "CRM Field" + enable card + Save (max 10 fields). Requires BotcakeAI active, an Agent, Page uses Pancake CRM.
- POS order status → Botcake sequence: Pancake POS → Settings → Facebook → Order Status Notifications → "+" → Use Botcake → select page, attach sequence, tag customer.
- Meta conversation control: Page → Settings → Advanced Messaging → app Botcake/Pancake v2 → Edit → enable "Take control" permission (both apps). Last app to send owns the thread; any app message pauses Meta Business Agent (BizAI) 7 days. Enable permission BEFORE passing control to BizAI.
- Handover Protocol: don't use if only Botcake/Pancake; misconfig breaks tools, input, buttons, sequences, rules, keywords (#10 error).
- 7-day window (Pancake, testing; Meta enabling ~90% from Sep 21 2026): CTM/CTD/CTWA ad leads; Botcake flows run full 7 days; Broadcast beta option.

## Botcake AI exact UI (EN)
- Connect key: Settings → Integrations → AI → "Connect" → "Add new" → Open AI → Insert API Key → "Connect". (Also CakeAI being integrated; Pancake wallet.)
- Botcake AI page (left menu Advanced → Botcake AI): header "Default Message Priority / AI Priority" toggle; Message-Sending Configuration (→ Smart Delay). Panels: Agent List, File Library (folders, 1 level), AI Settings (default agent, Speech-to-Text, delete AI history), AI Statistics. General → MCP Configuration tab → Add New.
- Setup flow (official diagram): Start → Create AI Agent → AI response configuration → Save → Test AI → Select default agent → Finish.
- Agent page: "AI configuration" with tabs "Instruction" | "Product manage"; model dropdown (e.g. GPT-4.1 mini); right "Preview" chat ("BotcakeAI may make a mistake. Check important info.").
- Model panel: Select model, Config: Templates; Temperature (ex 0.5), Top P (0.85), Presence Penalty (0.2), Frequency Penalty (0.3), Max Tokens (1000). Max message length setting: min 200 chars, max ~1000–1200 (split only if >min+100).
- Models listed: GPT-5 / 5 Mini / 5 Nano (reasoning), GPT-4.1 / 4.1 mini (speed), GPT-4o/4o mini legacy.
- Instruction editor: "Create your instruction", Detail | Quick toggle, placeholder 'Write, press "@" or "{" for insert picture or input field...', limit 0/10,000, icons emoji / { } input fields / attachment, link "Don't know how to write Instructions? Reference template".
- Quick setup sections: Sample Responses, Business Policies, Business Overview, Response Behavior (older doc also: Auto-create Order on Pancake POS, Product, Instructions Library).
- Product manage tab: Automation → "Auto-create order when information is available" [Phone number][Product][Address]; "Stop auto-creating orders when receiving negative reports on Pancake"; Config → "Image sending method" (Send as single image / Send as image collection); "Import product" (Import all). Below: "Auto follow-up" toggle → "Send follow-up messages automatically after" (e.g. 5 minutes, max 60) + "Number of messages" (e.g. 3, max 5). "Add files instruction" → Add.
- Files: older spec .DOCX/.TXT, max 10 files, 2MB each; overview says images, DOCX, PDFs. File search chunks ~200–300 tokens: short headed sections, keyword-rich headings, bullets not tables, repeat product names.
- Product images without POS: host image publicly, paste direct link in Instruction.
- AI block in Flow: "Customer's question content" (Input question; use input field e.g. custom field from User Input), "Agent" (default tagged), "More settings": Additional instruction / Enter priority product for consultation (max 3) / Skip AI message / Display 'typing' while waiting for a response; "Save Response to a Custom Field"; outcomes "AI responded successfully → Continue to another step", "AI response failed → Continue to another step", "Special case → Add customer's intent" (manual or templates: Order Success, Order Failed, customer shares phone).
- Loop pattern: Flow: User Input (save to custom field "Chat GPT") → AI block (question = that field) → success → loop back to input; special case "talk to consultant" → message "Please wait a moment 😊…" → assign human.
- JSON API block: GET/POST/DELETE, headers, params, body, Save Response to Custom Field via JSON Path, "Send" to test; ~30s timeout; prefix fields api_/gpt_.
- Botcake MCP (Jul 2026): 49 tools. Pancake MCP: https://mcp.pancake.biz/mcp (31 endpoints, 5 webhook events).
- Aug 28 2026: AI uses comment+post context for comment-originated inbox; read CRM variables in any flow; AI settings edit history; AI pulls POS promotions/gifts into orders.

## Botcake core (EN labels)
- Automation → Main Menu (max 20 items, flat), Ice Breaker (+ Settings → Enable Start button), Welcome Message, Default Reply (cycle), Keywords (12 match types; first keyword in list wins), Sequences (attach via tags or Rules), Rules (When this happens / Additional Actions; any number of times or once per person).
- Keyword match types: Content is / contains / contains and does not contain / contains all / contains all and does not contain / starts with / contains…and contains / Sticker / Image / Video / Customer rate / Contains POS products.
- Comments: General (auto reply + auto inbox; template must include {{user_full_name}} or spin syntax), specific post, keyword; 20 comments/min cap.
- Messages: Text 640 chars, max 3 buttons; images 25MB; collection ≤10 elements; Delay; Input (Text/Email/Phone; Skip) → Custom Field.
- Meta 24h rule; tags POST_PURCHASE_UPDATE, CONFIRMED_EVENT_UPDATE, ACCOUNT_UPDATE; Marketing Messages (paid, opt-in, 1 per 12h, F-caps); Utility messages (free, no promo, Meta approval).
- Fees: 500,000 free messages/page/month (since Nov 2 2024), top-up packages.
- Roles: Admin, Editor, Live Chat Agent, Viewer.

## Pancake key (EN labels)
- AI Assistant: Settings → AI Assistant; AI Model (Economy / Mid / Pro); Dataset (20–200 past conversations + files); Payment (USD prepaid wallet); groups AI conversation assist (Reply suggestions tab, Sentiment detection tab) and AI quality monitoring (≤25 criteria, ≤4 critical, weights 1–10). Free: Suggest frequently bought products. Tab cycles, Enter sends, ⭐ to add conversations to training.
- Round robin: Even Distribution / Online Only / Prioritize Online; ratios; shift scheduling; unread caps.
- Quick replies: / + shortcut, variables #{FULL_NAME} #{STAFF_NAME} #{PAGE_NAME} #{STAFF_DETAILS}.
- Pancake CRM paid add-on, 14-day trial.
