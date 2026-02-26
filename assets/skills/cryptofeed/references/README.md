# Cryptocurrency Exchange Feed Handler
[![License](https://img.shields.io/badge/license-XFree86-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
[![PyPi](https://img.shields.io/badge/PyPi-cryptofeed-brightgreen.svg)](https://pypi.python.org/pypi/cryptofeed)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/efa4e0d6e10b41d0b51454d08f7b33b1)](https://www.codacy.com/app/bmoscon/cryptofeed?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bmoscon/cryptofeed&amp;utm_campaign=Badge_Grade)

Handles multiple cryptocurrency exchange data feeds and returns normalized and standardized results to client registered callbacks for events like trades, book updates, ticker updates, etc. Utilizes websockets when possible, but can also poll data via REST endpoints if a websocket is not provided.

## Supported exchanges

* [AscendEX](https://ascendex.com/)
* [Bequant](https://bequant.io/)
* [Bitfinex](https://bitfinex.com)
* [bitFlyer](https://bitflyer.com/)
* [Bithumb](https://en.bithumb.com/)
* [Bitstamp](https://www.bitstamp.net/)
* [Blockchain.com](https://www.blockchain.com/)
* [Bybit](https://www.bybit.com/)
* [Binance](https://www.binance.com/en)
* [Binance Delivery](https://binance-docs.github.io/apidocs/delivery/en/)
* [Binance Futures](https://www.binance.com/en/futures)
* [Binance US](https://www.binance.us/en)
* [Bit.com](https://www.bit.com)
* [Bitget](https://www.bitget.com/)
* [BitMEX](https://www.bitmex.com/)
* [Coinbase](https://www.coinbase.com/)
* [Crypto.com](https://www.crypto.com)
* [Delta](https://www.delta.exchange/)
* [Deribit](https://www.deribit.com/)
* [dYdX](https://dydx.exchange/)
* [FMFW.io](https://www.fmfw.io/)
* [EXX](https://www.exx.com/)
* [Gate.io](https://www.gate.io/)
* [Gate.io Futures](https://www.gate.io/futures_center)
* [Gemini](https://gemini.com/)
* [HitBTC](https://hitbtc.com/)
* [Huobi](https://www.hbg.com/)
* [Huobi DM](https://www.huobi.com/en-us/markets/hb_dm/)
* Huobi Swap (Coin-M and USDT-M)
* [Independent Reserve](https://www.independentreserve.com/) 
* [Kraken](https://www.kraken.com/)
* [Kraken Futures](https://futures.kraken.com/)
* [KuCoin](https://www.kucoin.com/)
* [OKCoin](http://okcoin.com/)
* [OKX](https://www.okx.com/)
* [Phemex](https://phemex.com/)
* [Poloniex](https://www.poloniex.com/)
* [ProBit](https://www.probit.com/)
* [Upbit](https://sg.upbit.com/home)


## Basic Usage

Create a FeedHandler object and add subscriptions. For the various data channels that an exchange supports, you can supply callbacks for data events, or use provided backends (described below) to handle the data for you. Start the feed handler and you're done!

```python
from cryptofeed import FeedHandler
# not all imports shown for clarity

fh = FeedHandler()

# ticker, trade, and book are user defined functions that
# will be called when ticker, trade and book updates are received
ticker_cb = {TICKER: ticker}
trade_cb = {TRADES: trade}
gemini_cb = {TRADES: trade, L2_BOOK: book}


fh.add_feed(Coinbase(symbols=['BTC-USD'], channels=[TICKER], callbacks=ticker_cb))
fh.add_feed(Bitfinex(symbols=['BTC-USD'], channels=[TICKER], callbacks=ticker_cb))
fh.add_feed(Poloniex(symbols=['BTC-USDT'], channels=[TRADES], callbacks=trade_cb))
fh.add_feed(Gemini(symbols=['BTC-USD', 'ETH-USD'], channels=[TRADES, L2_BOOK], callbacks=gemini_cb))

fh.run()
```

Please see the [examples](https://github.com/bmoscon/cryptofeed/tree/master/examples) for more code samples and the [documentation](https://github.com/bmoscon/cryptofeed/blob/master/docs/README.md) for more information about the library usage.


For an example of a containerized application using cryptofeed to store data to a backend, please see [Cryptostore](https://github.com/bmoscon/cryptostore).


## National Best Bid/Offer (NBBO)

Cryptofeed also provides a synthetic [NBBO](examples/demo_nbbo.py) (National Best Bid/Offer) feed that aggregates the best bids and asks from the user specified feeds.

```python
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Gemini, Kraken


def nbbo_update(symbol, bid, bid_size, ask, ask_size, bid_feed, ask_feed):
    print(f'Pair: {symbol} Bid Price: {bid:.2f} Bid Size: {bid_size:.6f} Bid Feed: {bid_feed} Ask Price: {ask:.2f} Ask Size: {ask_size:.6f} Ask Feed: {ask_feed}')


def main():
    f = FeedHandler()
    f.add_nbbo([Coinbase, Kraken, Gemini], ['BTC-USD'], nbbo_update)
    f.run()
```

## Supported Channels

Cryptofeed supports the following channels from exchanges:

### Market Data Channels (Public)

* L1_BOOK - Top of book
* L2_BOOK - Price aggregated sizes. Some exchanges provide the entire depth, some provide a subset.
* L3_BOOK - Price aggregated orders. Like the L2 book, some exchanges may only provide partial depth.
* TRADES - Note this reports the taker's side, even for exchanges that report the maker side.
* TICKER
* FUNDING
* OPEN_INTEREST - Open interest data.
* LIQUIDATIONS
* INDEX
* CANDLES - Candlestick / K-Line data.

### Authenticated Data Channels

* ORDER_INFO - Order status updates
* TRANSACTIONS - Real-time updates on account deposits and withdrawals
* BALANCES - Updates on wallet funds
* FILLS - User's executed trades


## Backends

Cryptofeed supports `backend` callbacks that will write directly to storage or other interfaces.

Supported Backends:
* Redis (Streams and Sorted Sets)
* [Arctic](https://github.com/manahl/arctic)
* ZeroMQ
* UDP Sockets
* TCP Sockets
* Unix Domain Sockets
* [InfluxDB v2](https://github.com/influxdata/influxdb)
* MongoDB
* Kafka
* RabbitMQ
* PostgreSQL
* [QuasarDB](https://quasar.ai/)
* GCP Pub/Sub
* [QuestDB](https://questdb.io/)


## Installation

**Note:** cryptofeed requires Python 3.8+

Cryptofeed can be installed from PyPi. (It's recommended that you install in a virtual environment of your choosing).

    pip install cryptofeed

Cryptofeed has optional dependencies, depending on the backends used. You can install them individually, or all at once. To install Cryptofeed along with all its optional dependencies in one bundle:

    pip install cryptofeed[all]

If you wish to clone the repository and install from source, run this command from the root of the cloned repository.

    python setup.py install

Alternatively, you can install in 'edit' mode (also called development mode):

    python setup.py develop

See more discussion of package installation in [INSTALL.md](https://github.com/bmoscon/cryptofeed/blob/master/INSTALL.md).



## Rest API

Cryptofeed supports some REST interfaces for retrieving real-time and historical data, as well as order placement and account management. These are integrated into the exchange classes directly. You can view the supported methods by calling the `info()` method on any exchange. The methods for interacting with the exchange RET endpoints exist in two flavors, the synchronous methods (suffixed with `_sync`) as well as the asynchronous which can be utilized with asyncio. For more information see the [documentation](docs/rest.md).


## Future Work

There are a lot of planned features, new exchanges, etc planned! If you'd like to discuss ongoing development, please join the [discord](https://discord.gg/zaBYaGAYfR) or open a thread in the [discussions](https://github.com/bmoscon/cryptofeed/discussions) in GitHub.

## Contributing

Issues and PRs are welcomed!

Cryptofeed wouldn't be possible without the help of many [contributors](AUTHORS.md)! I owe them and all other contributors my thanks!

## Donations / Support

Support and donations are appreciated but not required. You can donate via [GitHub Sponsors](https://github.com/sponsors/bmoscon), or via the addresses below:

* Bitcoin: bc1qm0kxz8hqacaglku5fjhfe9a5hjnuyfwk02lsyr
* Ethereum: 0x690709FEe13eEce9E7852089BB2D53Ae5D073154
