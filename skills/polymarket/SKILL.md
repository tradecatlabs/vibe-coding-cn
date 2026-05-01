---
name: polymarket
description: "Polymarket prediction-market skill: REST/API research, CLOB market data, trading integration boundaries, WebSocket real-time data client, subscriptions, filters, authentication, and LLM-oriented market monitoring."
---

# polymarket Skill

Use this skill to build Polymarket research, monitoring, market-data, and integration workflows while keeping trading/authentication risks explicit.

## When to Use This Skill

Trigger when any of these applies:
- Querying Polymarket markets, events, prices, trades, comments, RFQ, or CLOB data.
- Building prediction-market monitors, dashboards, alerts, or LLM market-analysis tools.
- Using the `@polymarket/real-time-data-client` WebSocket client.
- Subscribing to activity, comments, RFQ, crypto price, `clob_market`, or authenticated `clob_user` topics.
- Debugging subscription filters, authentication payloads, reconnect handling, or message processing.

## Not For / Boundaries

- Not financial advice, market-making advice, or a guarantee of trading profitability.
- Do not expose CLOB API keys, secrets, passphrases, wallet keys, or private signing material.
- Private user streams and trading actions require explicit authentication and security review.
- Required inputs: market/event slug or CLOB market id, topic/type, auth need, filter payload, runtime, and expected output.
- For live trading, verify API terms, regional restrictions, auth scheme, and risk controls before implementation.

## Quick Reference

### Common Patterns

**Install the real-time data client**
```bash
npm install @polymarket/real-time-data-client
```

**Subscribe to live trades**
```typescript
import { RealTimeDataClient } from "@polymarket/real-time-data-client";

const client = new RealTimeDataClient({
  onMessage: (message) => console.log(message.topic, message.type, message.payload),
  onConnect: (c) => c.subscribe({
    subscriptions: [{ topic: "activity", type: "trades" }],
  }),
});

client.connect();
```

**Filter activity to one market slug**
```typescript
client.subscribe({
  subscriptions: [{
    topic: "activity",
    type: "trades",
    filters: "{\"market_slug\":\"btc-above-100k-2024\"}",
  }],
});
```

**Subscribe to CLOB market price changes**
```typescript
client.subscribe({
  subscriptions: [{
    topic: "clob_market",
    type: "price_change",
    filters: "[\"100\",\"101\",\"102\"]",
  }],
});
```

**Subscribe to comments for an event**
```typescript
client.subscribe({
  subscriptions: [{
    topic: "comments",
    type: "*",
    filters: "{\"parentEntityID\":12345,\"parentEntityType\":\"Event\"}",
  }],
});
```

**Authenticate a user stream**
```typescript
client.subscribe({
  subscriptions: [{
    topic: "clob_user",
    type: "*",
    clob_auth: {
      key: "YOUR_API_KEY",
      secret: "YOUR_API_SECRET",
      passphrase: "YOUR_PASSPHRASE",
    },
  }],
});
```

## Examples

### Example 1: Public Trade Monitor

- Input: market slug and alert threshold.
- Steps:
  1. Subscribe to `activity/trades` with a `market_slug` filter.
  2. Normalize messages into timestamp, market, side, price, size.
  3. Alert only when trade size or price movement crosses the configured threshold.
- Expected output / acceptance: real-time public trade stream with no private authentication material.

### Example 2: CLOB Price Dashboard

- Input: CLOB market IDs.
- Steps:
  1. Subscribe to `clob_market/price_change` with a JSON array filter.
  2. Update an in-memory view keyed by market id.
  3. Persist snapshots at a controlled interval rather than every message if volume is high.
- Expected output / acceptance: dashboard shows latest market prices and handles reconnects idempotently.

### Example 3: Authenticated User Order Feed

- Input: CLOB API credentials stored in a secret manager.
- Steps:
  1. Load credentials at runtime without logging them.
  2. Subscribe to `clob_user` order/trade events.
  3. Validate message schema and write audit logs without secrets.
- Expected output / acceptance: private user updates are received and secrets never appear in source control or logs.

## References

- `references/index.md`: navigation for local Polymarket references.
- `references/api.md`: platform API documentation.
- `references/getting_started.md`: onboarding and setup notes.
- `references/trading.md`: trading and market operations.
- `references/realtime-client.md`: WebSocket real-time data client.
- `references/README.md`: platform overview.
- `references/llms.md` and `references/llms-full.md`: LLM integration material.

## Maintenance

- Sources: local `references/` extracted from Polymarket platform and real-time client documentation.
- Last updated: 2026-04-28
- Known limits: API auth, market availability, and regional/legal constraints must be verified outside this skill before live trading.
