# Botcake update, part 3 (Dijae video): test, train, tools, knowledge, response behavior, human handoff

## Train responses
- Preview test "Hi can you help me with my skin" -> agent follows the instruction steps.
- Wand icon under a reply ("Improve AI response") -> modal "Improved AI responses — Rewrite the response so Botcake AI can learn how to respond better next time". "Back to list", CUSTOMER QUESTION (0/400), AI RESPONSE (0/500), Cancel / Save. Saved items appear as a list (question + date) with "Add new". Toast "Success / Action successful".
- Demo: question "hello" -> response "Hi {name}! I'm Bea, your online AI sales assistant..." Save, refresh Preview (reset icon), send "hello" -> trained answer returned.

## Tools tab — "Integrate connection: Choose the connection method to integrate with your AI"
- BUILT-IN: Pancake POS ("Automation create order"), Pancake CRM ("CRM Lead Automation"). TOOLS: "No data" + "Add new". Search box.
- Pancake POS > "Automation create order": toggles "Auto-create order when information is available" (on), "Automatic Upsell/Cross-sell based on POS configuration", "Stop auto-creating orders when receiving negative reports on Pancake". Config: "Image sending method" (Send as single image / Send as image collection), "Import product" (Import all / No product selected). Toast "Setting saved successfully".
- Demo had no POS products, so "what are your products" -> agent says it has no list (honest limitation).

## Knowledge tab
- "Files knowledge (0)": "Uploaded files are stored in the knowledge base. For URL sources, the AI uses the Botcake AI [model] to search directly on the website each time it answers, so the information is always up to date." Empty state "You don't have any files yet".
- "Add files" -> modal "Add files knowledge — Add knowledge for your Agent": tabs File instructions | Link URL; Search; Upload; file list with checkboxes (pulls from the shared Knowledge source library); Select all; Cancel / "Add to instruction". After: "Files knowledge (1)".

## AI response behavior tab (switch: Auto follow-up | Special case)
- Auto follow-up toggle: "AI will automatically send follow-up messages if the customer has not replied". GENERAL CONFIGURATION: "Send follow-up messages automatically after" (30 minutes), "Number of messages" (3 messages). FOLLOW UP MESSAGE INSTRUCTIONS: "Create follow-up message" — Automatically with AI / Manually.
- Special case toggle: "AI automatically detects & handles special situations in the conversation as configured". "Add case" -> Case 1: "Skip AI message" toggle; "Select template": When the order is created successfully / When the order creation fails / When the customer sends a phone number. ADD ACTION -> "Add action" menu:
  - Bot Action: Add tag, Remove tag, Assign to Staff on Pancake, Start a Flow, Set User Field, Notify Admins.
  - AI action: Pause AI.
- "Assign to Staff on Pancake — Assign tasks to Pancake employees": Assign randomizer; Replace staff (on); Only assign to online staff; Only assign to available staff on Pancake (on; receive mode Available); Select staff (1/2 staffs); Cancel / Save.
- Pause AI: "Pause AI for a period of time" (1 Hours; Minutes/Hours) — "AI resumes replying automatically once the pause is over"; or "Pause AI until turned back on" — "AI only replies again when a staff member reactivates AI".
- Top "Save" -> toast "Setting saved successfully".

## Screenshots (out/)
bc-23 Improved AI responses; bc-24 Tools; bc-25 Pancake POS auto order; bc-26 Add files knowledge (file names blurred); bc-27 Auto follow-up; bc-28 Special case templates; bc-29 Add action menu; bc-30 Assign to Staff on Pancake; bc-31 completed case (assign + pause 1 hour).

## Dijae's reasoning
- Train with real customer phrases until output matches; the AI enhancements and Improve AI response are the two training loops.
- Connect Pancake POS so the agent finds products and creates orders automatically.
- Knowledge = extra instruction files for products/rules.
- Special case: after an order is created, assign to a human on Pancake and pause AI for an hour -> human in the loop.
