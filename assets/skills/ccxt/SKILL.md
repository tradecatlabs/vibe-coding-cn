---
name: ccxt
description: "CCXT crypto exchange API skill: unified market data, order books, balances, order creation, sandbox mode, rate limits, verbose debugging, and exchange capability checks for JavaScript/Python/PHP trading automation."
---

# ccxt Skill

Use this skill to implement or debug CCXT integrations against cryptocurrency exchanges while keeping exchange-specific behavior explicit and testable.

## When to Use This Skill

Trigger when any of these applies:
- Fetching tickers, order books, trades, OHLCV, balances, markets, or exchange metadata through CCXT.
- Creating, cancelling, or inspecting orders with the unified CCXT API.
- Checking exchange capabilities with `exchange.has`, `exchange.features`, `loadMarkets()`, or market metadata.
- Handling sandbox/testnet mode, rate limits, authentication, precision, contract size, or market-buy cost semantics.
- Producing minimal reproducible debug reports with verbose HTTP request/response output.

## Not For / Boundaries

- Not financial advice, strategy validation, custody guidance, or a guarantee that an exchange supports a specific feature.
- Never run live orders before sandbox or dry-run validation; call `set_sandbox_mode(True)` immediately after exchange construction when supported.
- Do not log, commit, or paste API keys, secrets, passphrases, cookies, or private wallet information.
- Required inputs: language/runtime, exchange id, market symbol, operation type, sandbox/live mode, auth status, and exact error/verbose output.
- Exchange APIs change independently; verify feature support against `exchange.has`, `exchange.features`, and the relevant reference file before production use.

## Quick Reference

### Common Patterns

**Install CCXT for Python**
```bash
pip install ccxt
```

**Create an exchange with built-in rate limiting**
```python
import ccxt

exchange = ccxt.binance({"enableRateLimit": True})
```

**Enable sandbox mode before any other call**
```python
exchange = ccxt.binance({"apiKey": "KEY", "secret": "SECRET"})
exchange.set_sandbox_mode(True)
```

**Load and inspect markets**
```python
markets = exchange.load_markets()
market = exchange.market("BTC/USDT")
```

**Fetch one ticker instead of all tickers**
```python
ticker = exchange.fetch_ticker("BTC/USDT")
```

**Fetch an order book for bid/ask work**
```python
book = exchange.fetch_order_book("BTC/USDT", limit=20)
best_bid = book["bids"][0] if book["bids"] else None
best_ask = book["asks"][0] if book["asks"] else None
```

**Check capability before using an endpoint**
```python
if exchange.has.get("fetchOHLCV"):
    candles = exchange.fetch_ohlcv("BTC/USDT", timeframe="1m", limit=100)
```

**Create a reduce-only order when supported by the exchange**
```python
params = {"reduceOnly": True}
order = exchange.create_order("BTC/USDT:USDT", "limit", "sell", 1, 70000, params)
```

**Debug with verbose request/response output**
```python
exchange.verbose = True
exchange.fetch_balance()
```

**Use async support in Python**
```python
import ccxt.async_support as ccxt

exchange = ccxt.binance({"enableRateLimit": True})
try:
    await exchange.load_markets()
finally:
    await exchange.close()
```

## Examples

### Example 1: Market Data Collector

- Input: exchange `binance`, symbol `BTC/USDT`, timeframe `1m`.
- Steps:
  1. Instantiate with `enableRateLimit=True`.
  2. Call `load_markets()` once and verify `exchange.has["fetchOHLCV"]`.
  3. Fetch candles and persist timestamp, open, high, low, close, volume.
- Expected output / acceptance: one normalized candle batch and no repeated `load_markets()` calls inside the polling loop.

### Example 2: Sandbox Order Flow

- Input: exchange with sandbox support, symbol, side, amount, price.
- Steps:
  1. Create the exchange with credentials and immediately call sandbox mode.
  2. Load markets and inspect precision/limits for the symbol.
  3. Place a tiny limit order, fetch it by id, then cancel it.
- Expected output / acceptance: order lifecycle succeeds in sandbox and no live order endpoint is touched.

### Example 3: Debug a Failing Exchange Call

- Input: an exception from `create_order()` or `fetch_balance()`.
- Steps:
  1. Reduce code to a 5-20 line reproduction including exchange construction.
  2. Set `exchange.verbose = True` immediately before the failing call.
  3. Capture language version, CCXT version, exchange id, symbol, method, request, response, and full stack trace.
- Expected output / acceptance: a reproducible report without secrets and with enough evidence to distinguish CCXT misuse from exchange API failure.

## References

- `references/index.md`: navigation for the CCXT reference set.
- `references/manual.md`: unified API, markets, rate limits, orders, sandbox, and debugging.
- `references/faq.md`: common trading/order pitfalls and issue-reporting requirements.
- `references/exchanges.md`: exchange support and capability notes.
- `references/pro.md`: CCXT Pro and WebSocket-oriented material.
- `references/cli.md`: CCXT CLI usage.
- `references/specification.md`: generated API/spec material.

## Maintenance

- Sources: local `references/` extracted from CCXT documentation.
- Last updated: 2026-04-28
- Known limits: exchange-specific parameters and capabilities must be verified per exchange; examples intentionally avoid live credentials.
