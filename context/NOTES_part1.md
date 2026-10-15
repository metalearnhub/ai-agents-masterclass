# Botcake update, part 1 (Dijae video, recorded 14 Oct 2026): wallet + AI integration

Supersedes old docs: Botcake AI no longer needs your own OpenAI API key. It runs on the built-in "Botcake AI" model (OpenAI underneath, managed by Botcake), paid from a Pancake prepaid USD wallet.

## Flow (exact labels from screen)
1. Botcake top-right avatar > Profile (botcake.io/account) > tab "Prepaid account" > "+ Add prepaid account". (Tabs: Pricing & package | Prepaid account | Account settings.) Opens account.pancake.vn/wallets.
2. Pancake Account (account.pancake.vn/wallets): left menu Application / Top up / Subscriptions; "Balance by currency"; "Your accounts" table (Account name, Currency, Balance, Last transaction) + "+ Create account".
3. "Create account / Set up your prepaid account": "Account name *" (e.g. Botcake). Card: "Message via WhatsApp and use AI assistants. Pays in USD only." Covers: Message via WhatsApp Business; Use Pancake AI assistant; Use Botcake AI assistant. Buttons Cancel / "Create account". Toast "Account created".
4. "Top up" (Botcake • 0 USD): Currency (Account paid in USD); "Top-up amount *" dropdown $10, $20, $50, $100, $200, $500, $1,000...; "Card information *" > Add new card > Card number, Expiration date, CVC; right panel Total amount: Subtotal, Transaction fee $0, Amount received. "Next" -> card payment dialog. Return: wallet shows balance. Existing wallets have a "Top up" button per row; top-up form also shows "Auto top-up" toggle with a saved card.
   NOTE: transcript says "minimum $10,000" = misspoken; screen shows $10 as lowest option.
5. Botcake Settings > ACCOUNT > "Account Balance" (/settings/billing): "Balance $x", buttons "Reconnect", "Management" (opens Pancake wallet management). "Account Information": "Prepaid account" dropdown (pick wallet), "Auto top-up amount" ($10 in demo), "Auto top-up when balance is below" ($5 in demo).
6. Botcake Settings > SYSTEM > "Integrations" (/settings/connect): row "AI - Integrate AI to improve customer interaction" with pencil (edit) + "Connected". Modal "Configure AI integration - Choose your connection method with your AI": "+ Add new", columns AI Model | API key, row toggle + "Botcake AI" + trash. Toggle off = AI disabled for the whole account; on = enabled. Toast "Success / Action successful".
7. Left menu ADVANCE > "Botcake AI" (/agents): header "Botcake AI - Manage and set up your Agents. Each Agent can be used in multiple features". CATEGORY: Agent list, Information, Knowledge source, Statistics, General. "Search...", "+ Create new agent", DEFAULT AGENT, ALL AGENTS (cards "Ready to use"). Top bar toggle: "Default reply priority" <-> "AI priority".
- Sidebar usage: "Free message 4/500K", "Get Pro now".
- Home banner (time-limited): "Use AI. Get Cashback": $30+ spend 10%, $50+ 15%, $100+ 20%; cashback calculated every 30 days; campaign Sep 25 - Nov 25, 2026.

## Screenshots (out/)
bc-01 prepaid account tab; bc-02 create wallet (Use Botcake AI assistant); bc-03 top-up amount; bc-04 wallet list + Top up; bc-05 Account Balance (prepaid account + auto top-up); bc-06 Integrations AI row; bc-07 Botcake AI toggle; bc-08 Agent list (client agents blurred).
Blurred: email, Facebook ID, page ID (cropped URL bar), client agent names. Loom recorder overlay removed.

## Dijae's reasoning (transcript)
- Wallet first because you pay for tokens the AI uses to answer customers.
- One wallet works for both Pancake AI Assistant and Botcake AI Assistant.
- Use auto top-up so the AI never stops for lack of balance.
- Integration toggle is the account-wide kill switch; agents are managed separately.
