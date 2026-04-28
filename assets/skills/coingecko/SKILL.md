---
name: coingecko
description: "CoinGecko API skill: cryptocurrency prices, market data, coin IDs, historical charts, trending search, onchain endpoints, API-key authentication, and rate-limit-aware request design."
---

# coingecko Skill

Use this skill to integrate CoinGecko market data into applications, agents, dashboards, and analysis pipelines with clear API-key and rate-limit handling.

## When to Use This Skill

Trigger when any of these applies:
- Querying token prices, market cap, volume, historical charts, trending coins, NFTs, categories, or exchange data from CoinGecko.
- Choosing Demo API vs Pro API root URLs and authentication headers.
- Designing rate-limit-aware polling, cache refresh, or price freshness checks.
- Building crypto dashboards, price alerts, analytics jobs, or market-data enrichers.
- Navigating CoinGecko MCP, REST, or onchain/GeckoTerminal reference material.

## Not For / Boundaries

- Not financial advice, token endorsement, trade execution, or market manipulation support.
- Do not expose API keys in query strings unless unavoidable; prefer headers and backend proxy insertion.
- Do not assume symbol uniqueness; resolve assets with CoinGecko coin IDs before price calls.
- Required inputs: plan type, root URL, API key availability, coin IDs/symbols/contracts, quote currencies, date range, and freshness requirements.
- CoinGecko endpoints and plan gates evolve; verify paid-only endpoints and rate limits in `references/` before production use.

## Quick Reference

### Common Patterns

**Demo API ping with header auth**
```bash
curl -X GET "https://api.coingecko.com/api/v3/ping" \
  -H "x-cg-demo-api-key: YOUR_API_KEY"
```

**Pro API ping with header auth**
```bash
curl -X GET "https://pro-api.coingecko.com/api/v3/ping" \
  -H "x-cg-pro-api-key: YOUR_API_KEY"
```

**Simple price for coin IDs**
```bash
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
```

**Include freshness fields in price response**
```bash
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true"
```

**Market list by market cap**
```bash
curl "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"
```

**Historical chart by coin ID**
```bash
curl "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"
```

**Trending search**
```bash
curl "https://api.coingecko.com/api/v3/search/trending"
```

**Onchain trending pools**
```bash
curl "https://api.coingecko.com/api/v3/onchain/networks/trending_pools"
```

## Examples

### Example 1: Price Widget

- Input: coin IDs `bitcoin,ethereum`, quote `usd`, refresh interval.
- Steps:
  1. Use `/simple/price` with `include_last_updated_at=true`.
  2. Cache responses according to product freshness needs and plan limits.
  3. Display stale-data warnings when `last_updated_at` is outside the allowed window.
- Expected output / acceptance: a small response with current prices and explicit freshness handling.

### Example 2: Market-Cap Dashboard

- Input: quote currency `usd`, `per_page=100`, page number.
- Steps:
  1. Query `/coins/markets`.
  2. Persist coin ID, symbol, name, price, market cap, and volume.
  3. Avoid treating symbols as primary keys because duplicates exist.
- Expected output / acceptance: stable dashboard rows keyed by CoinGecko ID.

### Example 3: Trending Research Batch

- Input: need trending coins, NFTs, and categories in the last 24 hours.
- Steps:
  1. Query `/search/trending`.
  2. Normalize returned entities by type.
  3. For coins that require prices, follow up with `/simple/price` using IDs.
- Expected output / acceptance: a typed trending list with price enrichment only where IDs are available.

## References

- `references/index.md`: navigation for local CoinGecko docs.
- `references/authentication.md`: Demo/Pro API keys, root URLs, and header names.
- `references/coins.md`: coin IDs, markets, charts, simple price, and trending search.
- `references/market_data.md`: NFT market data notes.
- `references/exchanges.md`: exchange endpoints.
- `references/trending.md`: onchain trending pool endpoints.
- `references/llms.md` and `references/llms-full.md`: LLM-oriented reference exports.

## Maintenance

- Sources: local `references/` extracted from CoinGecko documentation.
- Last updated: 2026-04-28
- Known limits: plan availability and rate limits are account-specific; verify against the active CoinGecko plan before shipping.
