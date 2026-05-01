---
name: telegram-dev
description: "Telegram development skill: Bot API, Mini Apps/Web Apps, webhooks, long polling, inline/reply keyboards, payments, initData validation, TDLib/MTProto, message formatting, and deployment troubleshooting."
---

# telegram-dev Skill

Use this skill to build Telegram bots, Mini Apps, and client integrations with explicit security boundaries around tokens, webhooks, and user data.

## When to Use This Skill

Trigger when any of these applies:
- Creating or debugging a Telegram Bot with Bot API methods, long polling, webhooks, commands, messages, media, files, or payments.
- Building Telegram Mini Apps/Web Apps with `window.Telegram.WebApp`, buttons, theme params, storage, sensors, or `initData` validation.
- Implementing inline keyboards, reply keyboards, callback queries, command menus, or dynamic aligned message views.
- Working with TDLib/MTProto client development or API ID/hash based integrations.
- Troubleshooting webhook TLS/port issues, bot token errors, callback handling, formatting, or deployment.

## Not For / Boundaries

- Not for spam, unauthorized scraping, account abuse, or bypassing Telegram platform rules.
- Never commit or print bot tokens, API hash, API ID plus phone session data, payment secrets, or user private data.
- Webhook examples require HTTPS and public reachability; local-only servers need a tunnel or local Bot API server setup.
- Required inputs: Bot vs Mini App vs TDLib scope, language/framework, token/auth status, update payload, deployment URL, and exact error.
- Telegram APIs evolve; verify current method parameters and limits in official docs when precision matters.

## Quick Reference

### Common Patterns

**Bot API endpoint shape**
```text
https://api.telegram.org/bot<TOKEN>/<METHOD_NAME>
```

**Send a message**
```python
import requests

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={"chat_id": chat_id, "text": "Hello"},
    timeout=10,
)
```

**Long polling**
```python
updates = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
    params={"offset": offset, "timeout": 30},
    timeout=35,
).json()
```

**Set a webhook**
```python
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": "https://example.com/webhook"},
    timeout=10,
)
```

**Inline keyboard**
```python
reply_markup = {
    "inline_keyboard": [[
        {"text": "Open", "url": "https://example.com"},
        {"text": "Action", "callback_data": "action:1"},
    ]]
}
```

**Answer a callback query**
```python
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
    json={"callback_query_id": callback_query_id, "text": "OK"},
)
```

**Initialize a Mini App**
```javascript
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();
```

**Send Mini App data back to the bot**
```javascript
tg.sendData(JSON.stringify({ action: "submit" }));
```

**Validate Mini App initData server-side**
```text
Parse initData -> remove hash -> sort key=value pairs -> HMAC with WebAppData-derived secret -> compare hash.
```

## Examples

### Example 1: Echo Bot with Long Polling

- Input: bot token and a private test chat.
- Steps:
  1. Call `getUpdates` with an offset.
  2. Extract `message.chat.id` and `message.text`.
  3. Reply with `sendMessage` and advance offset.
- Expected output / acceptance: each user message gets one reply and old updates are not processed repeatedly.

### Example 2: Webhook Deployment

- Input: HTTPS URL `https://example.com/webhook`.
- Steps:
  1. Deploy an endpoint that accepts POST JSON updates.
  2. Call `setWebhook` with the public URL.
  3. Use `getWebhookInfo` to verify status and last error.
- Expected output / acceptance: Telegram delivers updates to the endpoint and webhook info has no current delivery error.

### Example 3: Mini App Button Flow

- Input: web app URL and bot chat.
- Steps:
  1. Send a reply or inline keyboard button with `web_app.url`.
  2. In the Mini App, call `ready()` and validate `initData` on the backend.
  3. Send final data with `sendData` or a backend API call.
- Expected output / acceptance: Mini App opens inside Telegram, backend authenticates the user, and bot receives structured data.

## References

- `references/index.md`: Telegram ecosystem navigation and official links.
- `references/Telegram_Bot_按钮和键盘实现模板.md`: button and keyboard implementation templates.
- `references/动态视图对齐实现文档.md`: aligned data display and dynamic message formatting.

## Maintenance

- Sources: local Telegram reference files plus official links listed in `references/index.md`.
- Last updated: 2026-04-28
- Known limits: API methods, limits, and Mini App capabilities are version-sensitive; verify against official Telegram docs for production releases.
