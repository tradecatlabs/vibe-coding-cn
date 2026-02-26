---
name: cryptofeed
description: Cryptofeed - Real-time cryptocurrency market data feeds from 40+ exchanges. WebSocket streaming, normalized data, order books, trades, tickers. Python library for algorithmic trading and market data analysis.
---

# Cryptofeed Skill

Comprehensive assistance with Cryptofeed development - a Python library for handling cryptocurrency exchange data feeds with normalized and standardized results.

## When to Use This Skill

This skill should be triggered when:
- Working with real-time cryptocurrency market data
- Implementing WebSocket streaming from crypto exchanges
- Building algorithmic trading systems
- Processing order book updates, trades, or ticker data
- Connecting to 40+ cryptocurrency exchanges
- Using normalized exchange APIs
- Implementing market data backends (Redis, MongoDB, Kafka, etc.)

## Quick Reference

### Installation

```python
# Basic installation
pip install cryptofeed

# With all optional backends
pip install cryptofeed[all]
```

### Basic Usage Pattern

```python
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Bitfinex
from cryptofeed.defines import TICKER, TRADES, L2_BOOK

# Define callbacks
def ticker_callback(data):
    print(f"Ticker: {data}")

def trade_callback(data):
    print(f"Trade: {data}")

# Create feed handler
fh = FeedHandler()

# Add exchange feeds
fh.add_feed(Coinbase(
    symbols=['BTC-USD'],
    channels=[TICKER],
    callbacks={TICKER: ticker_callback}
))

fh.add_feed(Bitfinex(
    symbols=['BTC-USD'],
    channels=[TRADES],
    callbacks={TRADES: trade_callback}
))

# Start receiving data
fh.run()
```

### National Best Bid/Offer (NBBO)

```python
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Gemini, Kraken

def nbbo_update(symbol, bid, bid_size, ask, ask_size, bid_feed, ask_feed):
    print(f'Pair: {symbol} Bid: {bid:.2f} ({bid_size:.6f}) from {bid_feed}')
    print(f'Ask: {ask:.2f} ({ask_size:.6f}) from {ask_feed}')

f = FeedHandler()
f.add_nbbo([Coinbase, Kraken, Gemini], ['BTC-USD'], nbbo_update)
f.run()
```

## Supported Exchanges (40+)

### Major Exchanges
- **Binance** (Spot, Futures, Delivery, US)
- **Coinbase**, **Kraken** (Spot, Futures), **Bitfinex**
- **Gemini**, **OKX**, **Bybit**
- **Huobi** (Spot, DM, Swap), **Gate.io** (Spot, Futures)
- **KuCoin**, **Deribit**, **BitMEX**, **dYdX**

### Additional Exchanges
AscendEX, Bequant, bitFlyer, Bithumb, Bitstamp, Blockchain.com, Bit.com, Bitget, Crypto.com, Delta, EXX, FMFW.io, HitBTC, Independent Reserve, OKCoin, Phemex, Poloniex, ProBit, Upbit

## Supported Data Channels

### Market Data (Public)
- **L1_BOOK** - Top of order book
- **L2_BOOK** - Price aggregated sizes
- **L3_BOOK** - Price aggregated orders
- **TRADES** - Executed trades (taker side)
- **TICKER** - Price ticker updates
- **FUNDING** - Funding rate data
- **OPEN_INTEREST** - Open interest statistics
- **LIQUIDATIONS** - Liquidation events
- **INDEX** - Index price data
- **CANDLES** - Candlestick/K-line data

### Authenticated Channels (Private)
- **ORDER_INFO** - Order status updates
- **TRANSACTIONS** - Deposits and withdrawals
- **BALANCES** - Wallet balance updates
- **FILLS** - User's executed trades

## Supported Backends

Write data directly to storage:

- **Redis** (Streams and Sorted Sets)
- **Arctic** - Time-series database
- **ZeroMQ**, **InfluxDB v2**, **MongoDB**
- **Kafka**, **RabbitMQ**, **PostgreSQL**
- **QuasarDB**, **GCP Pub/Sub**, **QuestDB**
- **UDP/TCP/Unix Sockets**

## Key Features

### Real-time Data Normalization
Cryptofeed normalizes data across all exchanges, providing consistent:
- Symbol formatting
- Timestamp handling
- Data structures
- Channel names

### WebSocket + REST Fallback
- Primarily uses WebSockets for real-time data
- Falls back to REST polling when WebSocket unavailable
- Automatic reconnection handling

### NBBO Aggregation
Create synthetic National Best Bid/Offer feeds by aggregating data across multiple exchanges to find arbitrage opportunities.

### Backend Integration
Direct data writing to various storage systems without custom integration code.

## Requirements

- **Python**: 3.8 or higher
- **Installation**: Via pip or from source
- **Optional Dependencies**: Install backends as needed

## Common Use Cases

### Multi-Exchange Price Monitoring
```python
fh = FeedHandler()
fh.add_feed(Binance(symbols=['BTC-USDT'], channels=[TICKER], callbacks=ticker_cb))
fh.add_feed(Coinbase(symbols=['BTC-USD'], channels=[TICKER], callbacks=ticker_cb))
fh.add_feed(Kraken(symbols=['BTC-USD'], channels=[TICKER], callbacks=ticker_cb))
fh.run()
```

### Order Book Depth Analysis
```python
def book_callback(book, receipt_timestamp):
    print(f"Bids: {len(book.book.bids)} | Asks: {len(book.book.asks)}")

fh.add_feed(Coinbase(
    symbols=['BTC-USD'],
    channels=[L2_BOOK],
    callbacks={L2_BOOK: book_callback}
))
```

### Trade Flow Analysis
```python
def trade_callback(trade, receipt_timestamp):
    print(f"{trade.exchange} - {trade.symbol}: {trade.side} {trade.amount} @ {trade.price}")

fh.add_feed(Binance(
    symbols=['BTC-USDT', 'ETH-USDT'],
    channels=[TRADES],
    callbacks={TRADES: trade_callback}
))
```

## Reference Files

This skill includes documentation in `references/`:

- **getting_started.md** - Installation and basic usage
- **README.md** - Complete overview and examples

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with basic FeedHandler setup and single exchange connections before adding multiple feeds.

### For Advanced Users
Explore NBBO feeds, authenticated channels, and backend integrations for production systems.

### For Code Examples
See the quick reference section above and the reference files for complete working examples.

## Resources

- **Repository**: https://github.com/bmoscon/cryptofeed
- **PyPI**: https://pypi.python.org/pypi/cryptofeed
- **Examples**: https://github.com/bmoscon/cryptofeed/tree/master/examples
- **Documentation**: https://github.com/bmoscon/cryptofeed/blob/master/docs/README.md
- **Discord**: https://discord.gg/zaBYaGAYfR
- **Related**: Cryptostore (containerized data storage)

## Notes

- Requires Python 3.8+
- WebSocket-first approach with REST fallback
- Normalized data across all exchanges
- Active development and community support
- 40+ supported exchanges and growing
