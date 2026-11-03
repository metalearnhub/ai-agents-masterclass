# Meta Messenger messaging rules: verified facts (checked Nov 3 2026)

Use these in any post about Messenger follow-ups, broadcasts or bots. Re-check the changelog before each use.

- Standard messaging window: 24 hours after the user's last message; up to 7 days when the user's first message follows a Click-to-Messenger / Click-to-Direct ad. Promotional content is allowed inside the window.
  Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages
- Message tags: CONFIRMED_EVENT_UPDATE, ACCOUNT_UPDATE, POST_PURCHASE_UPDATE retired; since April 27 2026 requests fail with error code 100 (changelog entry March 27 2026). HUMAN_AGENT is the only remaining tag: a person replies manually within 7 days, no promotional content.
  Source: https://developers.secure.facebook.com/documentation/business-messaging/messenger-platform/changelog
- Utility messages: pre-approved templates for orders, account updates and appointments; no marketing content; Meta's replacement for the retired tags. Open beta from July 29 2025 (US, Vietnam, Thailand, Philippines per PPC Land). Images since Sept 29 2025; named parameters since March 6 2026. Whether they can be sent outside the window is not stated on Meta's send-messages page: do not claim it.
- Marketing Message API for Messenger: launched July 1 2025; opt-in required; paid campaigns billed through an ad account with per-recipient-country pricing; frequency caps enforced since April 10 2026.
  Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/changelog
- Older Recurring Notifications (also called Marketing Messages in chatbot tools): third-party sources say region-limited (EU, UK, Japan, South Korea, Australia). Treat as unverified.
- Sponsored messages: paid, to people who messaged the Page before, labelled "Sponsored", must follow ad policies, not on Instagram.
- Automated disclosure: where the law requires (California, Germany named), automated chats must disclose at the start of a conversation, after a long gap and when moving from a human back to automation; Meta recommends it everywhere.
  Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/policy
- Quick replies: up to 13 per message, 20-character titles, disappear after tap / next message.
  Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/quick-replies
- Posts already updated with these rules: facebook-messenger-missed-messages, stop-bogus-cod-orders, ai-chatbot-human-handoff, chatbot-conversation-design. Link to them instead of re-explaining.
