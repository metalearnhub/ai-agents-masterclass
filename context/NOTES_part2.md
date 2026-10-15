# Botcake update, part 2 (Dijae video): create your first Botcake AI agent

Supersedes old docs: the agent builder is now a full workspace (Instruction / Tools / Knowledge / AI response behavior tabs + live Preview), models are picked from a Botcake AI catalog (GPT and DeepSeek, billed from the wallet), and there is a built-in "Optimize instructions" tool and per-message cost readout.

## Botcake AI categories (left CATEGORY list at /agents)
- **Agent list**: DEFAULT AGENT + ALL AGENTS cards (title, description, "Ready to use"). "+ Create new agent". Top bar: "Default reply priority" <-> "AI priority".
- **Information** (/business_information): "Manage your personal information". Business information: Shop name, Phone number, Email, Address, Shop countries. Payment information: Bank, Branch, Account number, Account holder. Button "Update". Reusable by every agent ("Each Agent can be used in multiple features").
- **Knowledge source** (/knowledge): "Manage and update the information your AI relies on". Toggle "File instruction" | "Attachment", "Trash", "Find your files", "Folder (00)", "Config" (Google Drive), folder icon, "Upload".
  - Upload -> modal "Import data — Upload data from a file, or add a URL for the AI to search live by domain." Upload file: "Click or drag files to upload", Format: Docx, PDF, TXT, XLSX, MD, size 15MB. Or "Search and filter relevant web content by domain" + "Check URL". Warning: some sites block access with pop-ups, ads or anti-robot verification. Note: "Botcake only supports the Websearch feature for models Botcake AI". Cancel / Confirm.
  - Config -> modal "Settings — Configure data retrieval from Google Drive": tabs Choose file | Setting; "Select account" (Google account), "Select files", Current location "All file", Search, File type, sort; "My file"; "Select 0 files"; "Done".
  - Attachment tab = images (PNG etc.) the agent can send (demo: 7 PNGs); File instruction tab = TXT knowledge files + website entries.
- **Statistics**: not shown.
- **General** (/general_ai): tabs "General" | "MCP configuration".
  - Account Balance "Manage your expenses": Balance $x, Reconnect, Management, Top up.
  - Setting Default Reply: Select Default Agent (dropdown), Smart delay ("AI delay after customer reply", Immediate), Maximum length of a message ("Break down the AI messages into shorter segments", No limit), "AI automatically detects and recommends products" (dedicated GPT-5 mini model detects products from your Ads/Post; toggle). Info: "The model you selected for each AI Agent does not change and operates independently of this feature".
  - Permissions & Security: Audience (Everyone / Admins), "Restrict Botcake AI by countries" / Select countries.
  - Text & Speech Conversion: Select language (English (US)), "Automatically skip messages contain voice"; CONFIG SETTING: Speech-to-text toggle.
  - AI sync image search: "Sync products from POS to BotcakeAI", "Go to E-commerce" (on in demo).
  - Chat history: "Enable chat history" — "Allows AI to remember the last 50 messages to better understand context and respond more accurately"; "Clear chat" -> Clear.

## Create agent
1. Agent list > "+ Create new agent" -> modal "Add new agent — Guide your Agent according to your preferences": Enter name (demo "Botcake AI"), Description ("This is my first Ai Agent"), checkbox "Use as default Agent", button "Create new agent". Toast "Success / Agent created successfully".
2. Workspace (/agents/{id}): header agent name + model pill; tabs Instruction | Tools | Knowledge | AI response behavior; "Create your instruction"; buttons "AI enhancements" and "Detail" (dropdown); "Business information — Your detail business information" with gear (opens Config modal with Business information / Payment information, "Done"); instruction editor "Write, press "@" or "{" for insert picture or input field..." with 0/15,000 character counter and expand icon; footer "Don't know how to write Instructions? Reference template". Right: "Preview" ("What can I help you with?", "Enter your message..."), reset icon. Top: "Save".
3. Model pill -> "Select model" (group BOTCAKEAI): Botcake AI GPT-4o mini (Smart & Fast), GPT-4o (Smart), GPT-4.1 mini (Smart, selected default in demo), GPT-4.1, GPT-5, GPT-5-mini, DeepSeek V3.2 (Fast), DeepSeek V4 Flash (Fast), DeepSeek V4.1 Flash (Fast), DeepSeek V4 Pro (Smart).
   NOTE: Loom summary said default "GPT-4o mini"; screen shows GPT-4.1 mini selected.
4. "Config" presets: Creative, Balanced, Precise (transcript also says "easy to understand" = not on screen). Balanced demo values: Temperature 0.5, Top P 0.85, Presence Penalty 0.2, Frequency Penalty 0.3, Max Tokens 1000. Each has a (?) tooltip, e.g. Frequency Penalty "Reduce the possibility of AI repeating the same word too many times"; Max Tokens "Response length limit".
5. Instruction: expand -> "Instruction" modal; "Reference template" -> Templates #1–#6 with eye preview, right pane "Instruction" with copy icon (toast "Copy / Copy success"). Template #1 = Vietnamese-shop CS rep (Context / Objective / Customer Care Process / Sales Policy / Shipping / Forbidden questions...). Dijae replaced it with the blog's # ROLE / # GOAL / # BUSINESS FACTS / # PRODUCTS AND PRICES / # RULES / # HANDOFF structure (Bea, Glow Lab PH) — 1,917/15,000 chars.
6. Preview test: "Hi Bea! what can you do" -> reply greets user by first name. Under the reply: $ icon -> "Message cost": Input tokens 3,136, Output tokens 58, Estimated cost $0.0013; wand icon -> "Improve AI response".
7. "AI enhancements" -> modal "Optimize instructions — Optimize the structure of your instructions": left "Your instructions", right "Instructions after optimization" (re-optimize icon, copy icon), Cancel / Apply. After Apply the prompt is restructured into Role / Task sections, inserts {{user.first_name}}, 4,227/15,000 chars.

## Screenshots (out/)
bc-09 Information; bc-10 Knowledge source; bc-11 Import data; bc-12 Google Drive settings (email blurred); bc-13 General (balance, default agent, smart delay); bc-14 Chat history 50 + Clear; bc-15 Add new agent; bc-16 workspace overview; bc-17 model list (GPT + DeepSeek); bc-18 Config presets; bc-19 Reference template; bc-20 Preview test; bc-21 Optimize instructions (Taglish handoff line blurred); bc-22 Message cost + Improve AI response.
Blurred: client business name/phone/address, client file names, Google email. Loom overlay removed.

## Dijae's reasoning (transcript)
- Information is business-wide; you can create many agents on top of it.
- Knowledge source = external/training data the AI relies on; optional.
- Read the (?) pop-ups and the docs before touching sliders; presets set them for you.
- Start from a Reference template or the blog's structure, test in Preview, then optimize and re-optimize until it fits the business objective, then Apply and re-test.
- Watch cost per message (input/output tokens) and use Improve AI response to retrain answers.
