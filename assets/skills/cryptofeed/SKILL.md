---
name: cryptofeed
description: "Cryptofeed real-time crypto market data skill: WebSocket feeds, normalized tickers/trades/order books, NBBO, exchange subscriptions, authenticated channels, and backend streaming to Redis/Kafka/PostgreSQL."
---

# cryptofeed Skill

Use this skill to build Python market-data pipelines with Cryptofeed across exchanges, channels, callbacks, NBBO aggregation, and storage backends.

## When to Use This Skill

Trigger when any of these applies:
- Streaming real-time crypto market data from multiple exchanges.
- Subscribing to tickers, trades, L1/L2/L3 order books, candles, funding, liquidations, balances, fills, or order updates.
- Building NBBO, arbitrage monitors, market-data recorders, or backend writers.
- Debugging symbol/channel support, callback shape, reconnection behavior, or backend configuration.
- Comparing Cryptofeed with exchange-specific WebSocket clients.

## Not For / Boundaries

- Not a trading strategy engine, order execution system, or persistence database by itself.
- Authenticated channels require exchange credentials; never commit or print secrets.
- Exchange support, symbols, and channel names vary; confirm against the exchange class and `references/README.md`.
- Required inputs: exchange list, symbols, channels, callback/backend target, auth need, and failure mode.
- For historical backfills, pair this with REST or a storage system; Cryptofeed is WebSocket-first.

## Quick Reference

### Common Patterns

**Install Cryptofeed**
```bash
pip install cryptofeed
```

**Create a simple feed handler**
```python
from cryptofeed import FeedHandler
from cryptofeed.defines import TICKER
from cryptofeed.exchanges import Coinbase

def ticker(data, receipt_timestamp):
    print(data)

fh = FeedHandler()
fh.add_feed(Coinbase(symbols=["BTC-USD"], channels=[TICKER], callbacks={TICKER: ticker}))
fh.run()
```

**Subscribe to trades and L2 book**
```python
from cryptofeed.defines import TRADES, L2_BOOK
from cryptofeed.exchanges import Gemini

fh.add_feed(Gemini(
    symbols=["BTC-USD", "ETH-USD"],
    channels=[TRADES, L2_BOOK],
    callbacks={TRADES: trade_callback, L2_BOOK: book_callback},
))
```

**Build NBBO across exchanges**
```python
from cryptofeed.exchanges import Coinbase, Gemini, Kraken

fh.add_nbbo([Coinbase, Kraken, Gemini], ["BTC-USD"], nbbo_callback)
```

**Separate callback work from IO-heavy persistence**
```python
def trade_callback(data, receipt_timestamp):
    queue.put_nowait((data, receipt_timestamp))
```

**Check supported channel names**
```python
from cryptofeed.defines import L1_BOOK, L2_BOOK, L3_BOOK, TRADES, TICKER
```

## Examples

### Example 1: Single-Exchange Ticker Stream

- Input: exchange `Coinbase`, symbol `BTC-USD`, channel `TICKER`.
- Steps:
  1. Create `FeedHandler`.
  2. Add one exchange feed with a lightweight callback.
  3. Run the handler and observe normalized ticker objects.
- Expected output / acceptance: ticker updates print with timestamps and no callback-blocking persistence work.

### Example 2: NBBO Monitor

- Input: exchanges `Coinbase`, `Kraken`, `Gemini`, symbol `BTC-USD`.
- Steps:
  1. Define `nbbo_callback(symbol, bid, bid_size, ask, ask_size, bid_feed, ask_feed)`.
  2. Add NBBO with the exchange class list.
  3. Alert only when spread or venue changes cross configured thresholds.
- Expected output / acceptance: best bid/ask updates include source venues.

### Example 3: Backend Recorder

- Input: symbols, channels, and a storage backend such as Redis/Kafka/PostgreSQL.
- Steps:
  1. Confirm optional backend dependencies are installed.
  2. Configure the backend callback instead of writing inside a custom callback.
  3. Run a small symbol set before scaling to many exchanges.
- Expected output / acceptance: records arrive in the backend with normalized exchange and symbol fields.

## References

- `references/index.md`: navigation for the local Cryptofeed references.
- `references/README.md`: supported exchanges, basic usage, NBBO, channels, and backends.
- `references/other.md`: additional generated reference material.

## Maintenance

- Sources: local `references/` extracted from Cryptofeed documentation.
- Last updated: 2026-04-28
- Known limits: channel support is exchange-specific; always validate symbol naming and callback signatures against the installed version.
