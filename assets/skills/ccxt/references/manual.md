# Ccxt - Manual

**Pages:** 2

---

## Search code, repositories, users, issues, pull requests...

**URL:** https://github.com/ccxt/ccxt/wiki/ccxt.pro.manual

**Contents:**
- Manual
- Exchanges
- Usage
- Prerequisites
- Streaming Specifics
  - Sub
  - Pub
  - unWatch
  - Incremental Data Structures
    - newUpdates mode

CCXT Pro is a free part of CCXT that adds support for WebSocket streaming: https://github.com/ccxt/ccxt/issues/15171

The CCXT Pro stack is built upon CCXT and extends the core CCXT classes, using:

The CCXT Pro heavily relies on the transpiler of CCXT for multilanguage support.

This is the list of exchanges in CCXT Pro with support for WebSockets APIs. This list will be updated with new exchanges on a regular basis.

Full list of exchanges available in CCXT via REST: Supported Cryptocurrency Exchange Markets.

The best way to understand CCXT Pro is to make sure you grasp the entire CCXT Manual and practice standard CCXT first. CCXT Pro borrows from CCXT. The two libraries share a lot of commonalities, including:

The CCXT Pro audience consists mostly of professional algorithmic traders and developers. In order to work efficiently with this library the user is required to be well-familiar with the concepts of streaming. One has to understand the underlying differences between connection-based streaming APIs (WebSocket, CCXT Pro) and request-response based APIs (REST, CCXT).

The general async-style flow for a CCXT application is as follows:

In CCXT Pro each public and private unified RESTful method having a fetch* prefix also has a corresponding stream-based counterpart method prefixed with watch*, as follows:

The Unified CCXT Pro Streaming API inherits CCXT usage patterns to make migration easier.

The general async-style flow for a CCXT Pro application (as opposed to a CCXT application above) is shown below:

That usage pattern is usually wrapped up into a core business-logic method called "a tick() function", since it reiterates a reaction to the incoming events (aka ticks). From the two examples above it is obvious that the generic usage pattern in CCXT Pro and CCXT is identical.

Many of the CCXT rules and concepts also apply to CCXT Pro:

Despite of the numerous commonalities, streaming-based APIs have their own specifics, because of their connection-based nature.

Having a connection-based interface implies connection-handling mechanisms. Connections are managed by CCXT Pro transparently to the user. Each exchange instance manages its own set of connections.

Upon your first call to any watch*() method the library will establish a connection to a specific stream/resource of the exchange and will maintain it. If the connection already exists – it is reused. The library will handle the subscription request/response messaging sequences as well as the authentication/signing if the requested stream is private.

The library will also watch the status of the uplink and will keep the connection alive. Upon a critical exception, a disconnect or a connection timeout/failure, the next iteration of the tick function will call the watch method that will trigger a reconnection. This way the library handles disconnections and reconnections for the user transparently. CCXT Pro applies the necessary rate-limiting and exponential backoff reconnection delays. All of that functionality is enabled by default and can be configured via exchange properties, as usual.

Most of the exchanges only have a single base URL for streaming APIs (usually, WebSocket, starting with ws:// or wss://). Some of them may have more than one URL for each stream, depending on the feed in question.

Exchanges' Streaming APIs can be classified into two different categories:

A sub interface usually allows to subscribe to a stream of data and listen for it. Most of exchanges that do support WebSockets will offer a sub type of API only. The sub type includes streaming public market data. Sometimes exchanges also allow subcribing to private user data. After the user subscribes to a data feed the channel effectively starts working one-way sending updates from the exchange towards the user continuously.

Commonly appearing types of public data streams:

Less common types of private user data streams:

A pub interface usually allows users to send data requests towards the server. This usually includes common user actions, like:

Some exchanges do not offer a pub WS API, they will offer sub WS API only. However, there are exchanges that have a complete Streaming API as well. In most cases a user cannot operate effectively having just the Streaming API. Exchanges will stream public market data sub, and the REST API is still needed for the pub part where missing.

Each watchX method establishes a subscription with a stream and will continuously get updates from the exchange. Even if you stop getting the return value from the watchX method, the stream will keep sending that, which is handled and stored in the background. To stop those background subscriptions, you should use unWatch method (eg. watchTrades -> unWatchTrades).

In many cases due to a unidirectional nature of the underlying data feeds, the application listening on the client-side has to keep a local snapshot of the data in memory and merge the updates received from the exchange server into the local snapshot. The updates coming from the exchange are also often called deltas, because in most cases those updates will contain just the changes between two states of the data and will not include the data that has not changed making it necessary to store the locally cached current state S of all relevant data objects.

All of that functionality is handled by CCXT Pro for the user. To work with CCXT Pro, the user does not have to track or manage subscriptions and related data. CCXT Pro will keep a cache of structures in memory to handle the underlying hassle.

Each incoming update says which parts of the data have changed and the receiving side "increments" local state S by merging the update on top of current state S and moves to next local state S'. In terms of CCXT Pro that is called "incremental state" and the structures involved in the process of storing and updating the cached state are called "incremental structures". CCXT Pro introduces several new base classes to handle the incremental state where necessary.

The incremental structures returned from the unified methods of CCXT Pro are often one of two types:

The unified methods returning arrays like watchOHLCV, watchTrades, watchMyTrades, watchOrders, are based on the caching layer. The user has to understand the inner workings of the caching layer to work with it efficiently.

The cache is a fixed-size deque aka array/list with two ends. The CCXT Pro library has a reasonable limit on the number of objects stored in memory. By default the caching array structures will store up to 1000 entries of each type (1000 most recent trades, 1000 most recent candles, 1000 most recent orders). The allowed maximum number can be configured by the user upon instantiation or later:

The cache limits have to be set prior to calling any watch-methods and cannot change during a program run.

When there is space left in the cache, new elements are simply appended to the end of it. If there's not enough room to fit a new element, the oldest element is deleted from the beginning of the cache to free some space. Thus, for example, the cache grows from 0 to 1000 most recent trades and then stays at 1000 most recent trades max, constantly renewing the stored data with each new update incoming from the exchange. It reminds a sliding frame window or a sliding door, that looks like shown below:

The user can configure the cache limits using the exchange.options as was shown above. Do not confuse the cache limits with the pagination limit.

Note, that the since and limit date-based pagination params have a different meaning and are always applied within the cached window! If the user specifies a since argument to the watchTrades() call, CCXT Pro will return all cached trades having timestamp >= since. If the user does not specify a since argument, CCXT pro will return cached trades from the beginning of the sliding window. If the user specifies a limit argument, the library will return up to limit candles starting from since or from the beginning of the cache. For that reason the user cannot paginate beyond the cached frame due to the WebSocket real-time specifics.

If you want to always get just the most recent trade, you should instantiate the exchange with the newUpdates flag set to true.

The newUpdates mode continues to utilize the sliding cache in the background, but the user will only be given the new updates. This is because some exchanges use incremental structures, so we need to keep a cache of objects as the exchange may only provide partial information such as status updates.

The result from the newUpdates mode will be one or more updates that have occurred since the last time exchange.watchMethod resolved. CCXT Pro can return one or more orders that were updated since the previous call. The result of calling exchange.watchOrders will look like shown below:

Deprecation Warning: in the future newUpdates: true will be the default mode and you will have to set newUpdates to false to get the sliding cache.

The imported CCXT Pro module wraps the CCXT inside itself – every exchange instantiated via CCXT Pro has all the CCXT methods as well as the additional functionality.

CCXT Pro is designed for async/await style syntax and relies heavily on async primitives such as promises and futures.

Creating a CCXT Pro exchange instance is pretty much identical to creating a CCXT exchange instance.

The Python implementation of CCXT Pro relies on builtin asyncio and Event Loop in particular. In Python it is possible to supply an asyncio's event loop instance in the constructor arguments as shown below (identical to ccxt.async support):

In PHP the async primitives are borrowed from ReactPHP. The PHP implementation of CCXT Pro relies on Promise and EventLoop in particular. In PHP the user is required to supply a ReactPHP's event loop instance in the constructor arguments as shown below:

Every CCXT Pro instance contains all properties of the underlying CCXT instance. Apart from the standard CCXT properties, the CCXT Pro instance includes the following:

The Unified CCXT Pro API encourages direct control flow for better codestyle, more readable and architecturally superior code compared to using EventEmitters and callbacks. The latter is considered an outdated approach nowadays since it requires inversion of control (people aren't used to inverted thinking).

CCXT Pro goes with the modern approach and it is designed for the async syntax. Under the hood, CCXT Pro will still have to use inverted control flow sometimes because of the dependencies and the WebSocket libs that can't do otherwise.

The same is true not only for JS/ES6 but also for Python 3 async code as well. In PHP the async primitives are borrowed from ReactPHP.

Modern async syntax allows you to combine and split the execution into parallel pathways and then merge them, group them, prioritize them, and what not. With promises one can easily convert from direct async-style control flow to inverted callback-style control flow, back and forth.

CCXT Pro supports two modes of tick function loops – the real-time mode and the throttling mode. Both of them are shown below in pseudocode:

In real-time mode CCXT Pro will return the result as soon as each new delta arrives from the exchange. The general logic of a unified call in a real-time loop is to await for the next delta and immediately return the unified result structure to the user, over and over again. This is useful when reaction time is critical, or has to be as fast as possible.

However, the real-time mode requires programming experience with async flows when it comes to synchronizing multiple parallel tick loops. Apart from that, the exchanges can stream a very large number of updates during periods of high activity or high volatility. Therefore the user developing a real-time algorithm has to make sure that the userland code is capable of consuming data that fast. Working in real-time mode may be more demanding for resources sometimes.

In throttling mode CCXT Pro will receive and manage the data in the background. The user is responsible for calling the results from time to time when necessary. The general logic of the throttling loop is to sleep for most of the time and wake up to check the results occasionally. This is usually done at some fixed frequency, or, "frame rate". The code inside a throttling loop is often easier to synchronize across multiple exchanges. The rationing of time spent in a throttled loop also helps reduce resource usage to a minimum. This is handy when your algorithm is heavy and you want to control the execution precisely to avoid running it too often.

The obvious downside of the throttling mode is being less reactive or responsive to updates. When a trading algorithm has to wait some number milliseconds before being executed – an update or two may arrive sooner than that time expires. In throttling mode the user will only check for those updates upon next wakeup (loop iteration), so the reaction lag may vary within some number of milliseconds over time.

The watchOrderBook's interface is identical to fetchOrderBook. It accepts three arguments:

In general, the exchanges can be divided in two categories:

If the exchange accepts a limiting argument, the limit argument is sent towards the exchange upon subscribing to the orderbook stream over a WebSocket connection. The exchange will then send only the specified amount of orders which helps reduce the traffic. Some exchanges may only accept certain values of limit, like 10, 25, 50, 100 and so on.

If the underlying exchange does not accept a limiting argument, the limiting is done on the client side.

The limit argument does not guarantee that the number of bids or asks will always be equal to limit. It designates the upper boundary or the maximum, so at some moment in time there may be less than limit bids or asks, but never more than limit bids or asks. This is the case when the exchange does not have enough orders on the orderbook, or when one of the top orders in the orderbook gets matched and removed from the orderbook, leaving less than limit entries on either bids side or asks side. The free space in the orderbook usually gets quickly filled with new data.

Similar to watchOrderBook but accepts an array of symbols so you can subscribe to multiple orderbooks in a single message.

Some exchanges allow different topics to listen to tickers (ie: bookTicker). You can set this in exchange.options['watchTicker']['name']

A very common misconception about WebSockets is that WS OHLCV streams can somehow speed up a trading strategy. If the purpose of your app is to implement OHLCV-trading or a speculative algorithmic strategy, consider the following carefully.

In general, there's two types of trading data used in the algorithms:

When developers say "real-time", that usually means pseudo real-time, or, put simply, "as fast and as close to real time as possible".

The 2nd-order data is always calculated from the 1st-order data. OHLCVs are calculated from aggregated trades. Tickers are calculated from trades and orderbooks.

Some exchanges do the calculation of OHLCVs (2nd order data) for you on the exchange side and send you updates over WS (Binance). Other exchanges don't really think that is necessary, for a reason.

Obviously, it takes time to calculate 2nd-order OHLCV candles from trades. Apart from that sending the calculated candle back to all connected users also takes time. Additional delays can happen during periods of high volatility if an exchange is traded very actively under high load.

There is no strict guarantee on how much time it will take from the exchange to calculate the 2nd order data and stream it to you over WS. The delays and lags on OHLCV candles can vary significantly from exchange to exchange. For example, an exchange can send an OHLCV update ~30 seconds after the actual closing of a corresponding period. Other exchanges may send the current OHLCV updates at a regular intervals (say, once every 100ms), while in reality trades can happen much more frequently.

Most people use WS to avoid any sorts of delays and have real-time data. So, in most cases it is much better to not wait for the exchange. Recalculating the 2nd order data from 1st order data on your own may be much faster and that can lower the unnecessary delays. Therefore it does not make much sense to use WS for watching just the OHLCV candles from the exchange. Developers would rather watch_trades() instead and recalculate the OHLCV candles using CCXT's built-in methods like build_ohlcvc().

That explains why some exchanges reasonably think that OHLCVs are not necessary in the WS context, cause users can calculate that information in the userland much faster having just a WS stream of realtime 1st-order trades.

If your application is not very time-critical, you can still subscribe to OHLCV streams, for charting purposes. If the underlying exchange.has['watchOHLCV'], you can watchOHLCV()/watch_ohlcv() as shown below:

Similar to watchOHLCV but allows multiple subscriptions of symbols and timeframes

Similar to watchTrades but allows subscribing to multiple symbols in a single call.

In most cases the authentication logic is borrowed from CCXT since the exchanges use the same keypairs and signing algorithms for REST APIs and WebSocket APIs. See API Keys Setup for more details.

watch all open positions and returns a list of position structure

If you want to have an access to raw incoming messages and use your custom handlers, you can override exchange's handleMessage/handle_message method, like:

B) by overriding the method:

In case of an error the CCXT Pro will throw a standard CCXT exception, see Error Handling for more details.

(If the page is not being rendered for you, you can refer to the mirror at https://docs.ccxt.com/)

**Examples:**

Example 1 (unknown):
```unknown
User

    +-------------------------------------------------------------+
    |                          CCXT Pro                           |
    +------------------------------+------------------------------+
    |            Public            .           Private            |
    +=============================================================+
    │                              .                              |
    │                  The Unified CCXT Pro API                   |
    |                              .                              |
    |     loadMarkets              .         watchBalance         |
    |     watchTicker              .         watchOrders          |
    |     watchTickers             .         watchMyTrades        |
    |     watchOrderBook           .         watchPositions       |
    |     watchOHLCV               .         createOrderWs        |
    |     watchStatus              .         editOrderWs          |
    |     watchTrades              .         cancelOrderWs        |
    │     watchOHLCVForSymbols     .         cancelOrdersWs       |
    │     watchTradesForSymbols    .         cancelAllOrdersWs    |
    │     watchOrderBookForSymbols .                              |
    │                              .                              |
    +=============================================================+
    │                          unWatch                            |
    │                   (to stop **watch** method)                |
    +=============================================================+
    │                              .                              |
    |            The Underlying Exchange-Specific APIs            |
    |         (Derived Classes And Their Implementations)         |
    │                              .                              |
    +=============================================================+
    │                              .                              |
    |                 CCXT Pro Base Exchange Class                |
    │                              .                              |
    +=============================================================+

    +-------------------------------------------------------------+
    |                                                             |
    |                            CCXT                             |
    |                                                             |
    +=============================================================+
```

Example 2 (unknown):
```unknown
past > ------------------ > time > - - - - - - - - > future


                           sliding frame
                           of 1000 most
                           recent trades
                        +-----------------+
                        |                 |
                        |===========+=====|
+----------------+------|           |     | - - - - - + - - - - - - - - + - - -
|                |      |           |     |           |                 |
0              1000     |         2000    |         3000              4000  ...
|                |      |           |     |           |                 |
+----------------+------|           |     | - - - - - + - - - - - - - - + - - -
                        |===========+=====|
                        |                 |
                        +---+---------+---+
                            |         |
                      since ^         ^ limit

                   date-based pagination arguments
                         are always applied
                       within the cached frame
```

---

## Search code, repositories, users, issues, pull requests...

**URL:** https://github.com/ccxt/ccxt/wiki/Manual

**Contents:**
- Overview
- Social
- Exchanges
- Instantiation
    - Javascript
    - Python
    - PHP
    - Javascript
    - Python
    - PHP

The ccxt library is a collection of available crypto exchanges or exchange classes. Each class implements the public and private API for a particular crypto exchange. All exchanges are derived from the base Exchange class and share a set of common methods. To access a particular exchange from ccxt library you need to create an instance of corresponding exchange class. Supported exchanges are updated frequently and new exchanges are added regularly.

The structure of the library can be outlined as follows:

Full public and private HTTP REST APIs for all exchanges are implemented. WebSocket implementations in JavaScript, PHP, Python are available in CCXT Pro, which is a professional addon to CCXT with support for WebSocket streams.

Besides making basic market and limit orders, some exchanges offer margin trading (leverage), various derivatives (like futures contracts and options) and also have dark pools, OTC (over-the-counter trading), merchant APIs and much more.

To connect to an exchange and start trading you need to instantiate an exchange class from ccxt library.

To get the full list of ids of supported exchanges programmatically:

An exchange can be instantiated like shown in the examples below:

The ccxt library in PHP uses builtin UTC/GMT time functions, therefore you are required to set date.timezone in your php.ini or call date_default_timezone_set() function before using the PHP version of the library. The recommended timezone setting is "UTC".

Major exchanges have the .features property available, where you can see what methods and functionalities are supported for each market-type (if any method is set to null/undefined it means method is "not supported" by the exchange)

this feature is currently a work in progress and might be incomplete, feel free to report any issues you find in it

Most of exchange properties as well as specific options can be overrided upon exchange class instantiation or afterwards, like shown below:

In all CCXT-supported languages, you can override instance methods during runtime:

Some exchanges also offer separate APIs for testing purposes that allows developers to trade virtual money for free and test out their ideas. Those APIs are called "testnets", "sandboxes" or "staging environments" (with virtual testing assets) as opposed to "mainnets" and "production environments" (with real assets). Most often a sandboxed API is a clone of a production API, so, it's literally the same API, except for the URL to the exchange server.

CCXT unifies that aspect and allows the user to switch to the exchange's sandbox (if supported by the underlying exchange). To switch to the sandbox one has to call the exchange.setSandboxMode (true) or exchange.set_sandbox_mode(true) immediately after creating the exchange before any other call!

Every exchange has a set of properties and methods, most of which you can override by passing an associative array of params to an exchange constructor. You can also make a subclass and override everything.

Here's an overview of generic exchange properties with values added for example:

Below is a detailed description of each of the base exchange properties:

id: Each exchange has a default id. The id is not used for anything, it's a string literal for user-land exchange instance identification purposes. You can have multiple links to the same exchange and differentiate them by ids. Default ids are all lowercase and correspond to exchange names.

name: This is a string literal containing the human-readable exchange name.

countries: An array of string literals of 2-symbol ISO country codes, where the exchange is operating from.

urls['api']: The single string literal base URL for API calls or an associative array of separate URLs for private and public APIs.

urls['www']: The main HTTP website URL.

urls['doc']: A single string URL link to original documentation for exchange API on their website or an array of links to docs.

version: A string literal containing version identifier for current exchange API. The ccxt library will append this version string to the API Base URL upon each request. You don't have to modify it, unless you are implementing a new exchange API. The version identifier is a usually a numeric string starting with a letter 'v' in some cases, like v1.1. Do not override it unless you are implementing your own new crypto exchange class.

api: An associative array containing a definition of all API endpoints exposed by a crypto exchange. The API definition is used by ccxt to automatically construct callable instance methods for each available endpoint.

has: This is an associative array of exchange capabilities (e.g fetchTickers, fetchOHLCV or CORS).

timeframes: An associative array of timeframes, supported by the fetchOHLCV method of the exchange. This is only populated when has['fetchOHLCV'] property is true.

timeout: A timeout in milliseconds for a request-response roundtrip (default timeout is 10000 ms = 10 seconds). If the response is not received in that time, the library will throw an RequestTimeout exception. You can leave the default timeout value or set it to a reasonable value. Hanging forever with no timeout is not your option, for sure. You don't have to override this option in general case.

rateLimit: A request rate limit in milliseconds. Specifies the required minimal delay between two consequent HTTP requests to the same exchange. The built-in rate-limiter is enabled by default and can be turned off by setting the enableRateLimit property to false.

enableRateLimit: A boolean (true/false) value that enables the built-in rate limiter and throttles consecutive requests. This setting is true (enabled) by default. The user is required to implement own rate limiting or leave the built-in rate limiter enabled to avoid being banned from the exchange.

userAgent: An object to set HTTP User-Agent header to. The ccxt library will set its User-Agent by default. Some exchanges may not like it. If you are having difficulties getting a reply from an exchange and want to turn User-Agent off or use the default one, set this value to false, undefined, or an empty string. The value of userAgent may be overrided by HTTP headers property below.

headers: An associative array of HTTP headers and their values. Default value is empty {}. All headers will be prepended to all requests. If the User-Agent header is set within headers, it will override whatever value is set in the userAgent property above.

verbose: A boolean flag indicating whether to log HTTP requests to stdout (verbose flag is false by default). Python people have an alternative way of DEBUG logging with a standard pythonic logger, which is enabled by adding these two lines to the beginning of their code:

returnResponseHeaders: If set to true, the HTTP response headers from the exchange will be included in the responseHeaders property inside the info field of the returned result for REST API calls. This can be useful for accessing metadata such as rate limit information or exchange-specific headers. By default, this is false and headers are not included in the response. Note: it's only supported when response is an object and not a list or string

markets: An associative array of markets indexed by common trading pairs or symbols. Markets should be loaded prior to accessing this property. Markets are unavailable until you call the loadMarkets() / load_markets() method on exchange instance.

symbols: A non-associative array (a list) of symbols available with an exchange, sorted in alphabetical order. These are the keys of the markets property. Symbols are loaded and reloaded from markets. This property is a convenient shorthand for all market keys.

currencies: An associative array (a dict) of currencies by codes (usually 3 or 4 letters) available with an exchange. Currencies are loaded and reloaded from markets.

markets_by_id: An associative array of arrays of markets indexed by exchange-specific ids. Typically a length one array unless there are multiple markets with the same marketId. Markets should be loaded prior to accessing this property.

apiKey: This is your public API key string literal. Most exchanges require API keys setup.

secret: Your private secret API key string literal. Most exchanges require this as well together with the apiKey.

password: A string literal with your password/phrase. Some exchanges require this parameter for trading, but most of them don't.

uid: A unique id of your account. This can be a string literal or a number. Some exchanges also require this for trading, but most of them don't.

requiredCredentials: A unified associative dictionary that shows which of the above API credentials are required for sending private API calls to the underlying exchange (an exchange may require a specific set of keys).

options: An exchange-specific associative dictionary containing special keys and options that are accepted by the underlying exchange and supported in CCXT.

precisionMode: The exchange decimal precision counting mode, read more about Precision And Limits

For proxies - proxyUrl, httpUrl, httpsUrl, socksProxy, wsProxy, wssProxy, wsSocksProxy : An url of specific proxy. Read details in Proxy section.

See this section on Overriding exchange properties.

has: An assoc-array containing flags for exchange capabilities, including the following:

The meaning of each flag showing availability of this or that method is:

For a complete list of all exchanges and their supported methods, please, refer to this example: https://github.com/ccxt/ccxt/blob/master/examples/js/exchange-capabilities.js

Exchanges usually impose what is called a rate limit. Exchanges will remember and track your user credentials and your IP address and will not allow you to query the API too frequently. They balance their load and control traffic congestion to protect API servers from (D)DoS and misuse.

WARNING: Stay under the rate limit to avoid ban!

Most exchanges allow up to 1 or 2 requests per second. Exchanges may temporarily restrict your access to their API or ban you for some period of time if you are too aggressive with your requests.

The exchange.rateLimit property is set to a safe default which is sub-optimal. Some exchanges may have varying rate limits for different endpoints. It is up to the user to tweak rateLimit according to application-specific purposes.

The CCXT library has a built-in experimental rate-limiter that will do the necessary throttling in background transparently to the user. WARNING: users are responsible for at least some type of rate-limiting: either by implementing a custom algorithm or by doing it with the built-in rate-limiter..

You can turn on/off the built-in rate-limiter with .enableRateLimit property, like so:

In case your calls hit a rate limit or get nonce errors, the ccxt library will throw an InvalidNonce exception, or, in some cases, one of the following types:

A later retry is usually enough to handle that.

The rate limiter is a property of the exchange instance, in other words, each exchange instance has its own rate limiter that is not aware of the other instances. In many cases the user should reuse the same exchange instance throughout the program. Do not use multiple instances of the same exchange with the same API keypair from the same IP address.

Reuse the exchange instance as much as possible as shown below:

Since the rate limiter belongs to the exchange instance, destroying the exchange instance will destroy the rate limiter as well. Among the most common pitfalls with the rate limiting is creating and dropping the exchange instance over and over again. If in your program you are creating and destroying the exchange instance (say, inside a function that is called multiple times), then you are effectively resetting the rate limiter over and over and that will eventually break the rate limits. If you are recreating the exchange instance every time instead of reusing it, CCXT will try to load the markets every time. Therefore, you will force-load the markets over and over as explained in the Loading Markets section. Abusing the markets endpoint will eventually break the rate limiter as well.

Do not break this rule unless you really understand the inner workings of the rate-limiter and you are 100% sure you know what you're doing. In order to stay safe always reuse the exchange instance throughout your functions and methods callchain like shown below:

Some exchanges are DDoS-protected by Cloudflare or Incapsula. Your IP can get temporarily blocked during periods of high load. Sometimes they even restrict whole countries and regions. In that case their servers usually return a page that states a HTTP 40x error or runs an AJAX test of your browser / captcha test and delays the reload of the page for several seconds. Then your browser/fingerprint is granted access temporarily and gets added to a whitelist or receives a HTTP cookie for further use.

The most common symptoms for a DDoS protection problem, rate-limiting problem or for a location-based filtering issue:

If you encounter DDoS protection errors and cannot reach a particular exchange then:

In asynchronous programming, CCXT allows you to schedule an unlimited number of requests. However, there is a default queue limit of 1,000 concurrent requests. If you attempt to enqueue more than this limit, you will encounter the error: "throttle queue is over maxCapacity".

In most cases, having such a large number of pending tasks indicates suboptimal design, as new requests will be delayed until the existing tasks complete.

That said, users who wish to bypass this restriction can increase the default maxCapacity during instantiation as shown below:

Each exchange is a place for trading some kinds of valuables. The exchanges may use differing terms to call them: "a currency", "an asset", "a coin", "a token", "stock", "commodity", "crypto", "fiat", etc. A place for trading one asset for another is usually called "a market", "a symbol", "a trading pair", "a contract", etc.

In terms of the ccxt library, every exchange offers multiple markets within itself. Each market is defined by two or more currencies. The set of markets differs from exchange to exchange opening possibilities for cross-exchange and cross-market arbitrage.

Each currency is an associative array (aka dictionary) with the following keys:

Each network is an associative array (aka dictionary) with the following keys:

Each market is an associative array (aka dictionary) with the following keys:

The active flag is typically used in currencies and markets. The exchanges might put a slightly different meaning into it. If a currency is inactive, most of the time all corresponding tickers, orderbooks and other related endpoints return empty responses, all zeroes, no data or outdated information. The user should check if the currency is active and reload markets periodically.

Note: the false value for the active property doesn't always guarantee that all of the possible features like trading, withdrawing or depositing are disabled on the exchange. Likewise, neither the true value guarantees that all those features are enabled on the exchange. Check the underlying exchanges' documentation and the code in CCXT for the exact meaning of the active flag for this or that exchange. This flag is not yet supported or implemented by all markets and may be missing.

WARNING! The information about the fee is experimental, unstable and may be partial or not available at all.

Do not confuse limits with precision! Precision has nothing to do with min limits. A precision of 0.01 does not necessarily mean that a minimum limit for market is 0.01. The opposite is also true: a min limit of 0.01 does not necessarily mean a precision is 0.01.

(market['precision']['amount'] == -1)

A negative precision might only theoretically happen if exchange's precisionMode is SIGNIFICANT_DIGIT or DECIMAL_PRECISION. It means that the amount should be an integer multiple of 10 (to the absolute power specified):

In case of -2 the acceptable values would be multiple of 100 (e.g. 100, 200, ... ), and so on.

Supported precision modes in exchange['precisionMode'] are:

The user is required to stay within all limits and precision! The values of the order should satisfy the following conditions:

The above values can be missing with some exchanges that don't provide info on limits from their API or don't have it implemented yet.

Each exchange has its own rounding, counting and padding modes.

Supported rounding modes are:

The decimal precision counting mode is available in the exchange.precisionMode property.

Supported padding modes are:

Most of the time the user does not have to take care of precision formatting, since CCXT will handle that for the user when the user places orders or sends withdrawal requests, if the user follows the rules as described on Precision And Limits. However, in some cases precision-formatting details may be important, so the following methods may be useful in the userland.

The exchange base class contains the decimalToPrecision method to help format values to the required decimal precision with support for different rounding, counting and padding modes.

For examples of how to use the decimalToPrecision to format strings and floats, please, see the following files:

Python WARNING! The decimal_to_precision method is susceptible to getcontext().prec!

For users' convenience CCXT base exchange class also implements the following methods:

Every exchange has its own precision settings, the above methods will help format those values according to exchange-specific precision rules, in a way that is portable and agnostic of the underlying exchange. In order to make that possible, markets and currencies have to be loaded prior to formatting any values.

Make sure to load the markets with exchange.loadMarkets() before calling these methods!

More practical examples that describe the behavior of exchange.precisionMode:

In most cases you are required to load the list of markets and trading symbols for a particular exchange prior to accessing other API methods. If you forget to load markets the ccxt library will do that automatically upon your first call to the unified API. It will send two HTTP requests, first for markets and then the second one for other data, sequentially. For that reason, your first call to a unified CCXT API method like fetchTicker, fetchBalance, etc will take more time, than the consequent calls, since it has to do more work loading the market information from the exchange API. See Notes On Rate Limiter for more details.

In order to load markets manually beforehand call the loadMarkets () / load_markets () method on an exchange instance. It returns an associative array of markets indexed by trading symbol. If you want more control over the execution of your logic, preloading markets by hand is recommended.

Apart from the market info, the loadMarkets() call will also load the currencies from the exchange and will cache the info in the .markets and the .currencies properties respectively.

The user can also bypass the cache and call unified methods for fetching that information from the exchange endpoints directly, fetchMarkets() and fetchCurrencies(), though using these methods is not recommended for end-users. The recommended way to preload markets is by calling the loadMarkets() unified method. However, new exchange integrations are required to implement these methods if the underlying exchange has the corresponding API endpoints.

To optimize memory usage and reduce redundant API calls, you can share market data between multiple instances of the same exchange. This is especially useful when creating multiple exchange instances or when you want to reuse market data that has already been loaded.

Benefits of Market Sharing:

Alternative Simple Assignment:

If you prefer direct property assignment, you can also share markets by directly assigning the markets property:

However, using the setMarketsFromExchange() method is recommended as it:

A currency code is a code of three to five letters, like BTC, ETH, USD, GBP, CNY, JPY, DOGE, RUB, ZEC, XRP, XMR, etc. Some exchanges have exotic currencies with longer codes.

A symbol is usually an uppercase string literal name of a pair of traded currencies with a slash in between. The first currency before the slash is usually called base currency, and the one after the slash is called quote currency. Examples of a symbol are: BTC/USD, DOGE/LTC, ETH/EUR, DASH/XRP, BTC/CNY, ZEC/XMR, ETH/JPY.

Market ids are used during the REST request-response process to reference trading pairs within exchanges. The set of market ids is unique per exchange and cannot be used across exchanges. For example, the BTC/USD pair/market may have different ids on various popular exchanges, like btcusd, BTCUSD, XBTUSD, btc/usd, 42 (numeric id), BTC/USD, Btc/Usd, tBTCUSD, XXBTZUSD. You don't need to remember or use market ids, they are there for internal HTTP request-response purposes inside exchange implementations.

The ccxt library abstracts uncommon market ids to symbols, standardized to a common format. Symbols aren't the same as market ids. Every market is referenced by a corresponding symbol. Symbols are common across exchanges which makes them suitable for arbitrage and many other things.

Sometimes the user might notice a symbol like 'XBTM18' or '.XRPUSDM20180101' or some other "exotic/rare symbols". The symbol is not required to have a slash or to be a pair of currencies. The string in the symbol really depends on the type of the market (whether it is a spot market or a futures market, a darkpool market or an expired market, etc). Attempting to parse the symbol string is highly discouraged, one should not rely on the symbol format, it is recommended to use market properties instead.

Market structures are indexed by symbols and ids. The base exchange class also has builtin methods for accessing markets by symbols. Most API methods require a symbol to be passed in their first argument. You are often required to specify a symbol when querying current prices, making orders, etc.

Most of the time users will be working with market symbols. You will get a standard userland exception if you access non-existent keys in these dicts.

There is a bit of term ambiguity across various exchanges that may cause confusion among newcoming traders. Some exchanges call markets as pairs, whereas other exchanges call symbols as products. In terms of the ccxt library, each exchange contains one or more trading markets. Each market has an id and a symbol. Most symbols are pairs of base currency and quote currency.

Exchanges → Markets → Symbols → Currencies

Historically various symbolic names have been used to designate same trading pairs. Some cryptocurrencies (like Dash) even changed their names more than once during their ongoing lifetime. For consistency across exchanges the ccxt library will perform the following known substitutions for symbols and currencies:

Each exchange has an associative array of substitutions for cryptocurrency symbolic codes in the exchange.commonCurrencies property, like:

where key represents actual name how exchange engine refers to that coin, and the value represents what you want to refer to it with through ccxt.

Sometimes the user may notice exotic symbol names with mixed-case words and spaces in the code. The logic behind having these names is explained by the rules for resolving conflicts in naming and currency-coding when one or more currencies have the same symbolic code with different exchanges:

Is it possible for symbols to change?

In short, yes, sometimes, but rarely. Symbolic mappings can be changed if that is absolutely required and cannot be avoided. However, all previous symbolic changes were related to resolving conflicts or forks. So far, there was no precedent of a market cap of one coin overtaking another coin with the same symbolic code in CCXT.

Can we rely on always listing the same crypto with the same symbol?

More or less ) First, this library is a work in progress, and it is trying to adapt to the everchanging reality, so there may be conflicts that we will fix by changing some mappings in the future. Ultimately, the license says "no warranties, use at your own risk". However, we don't change symbolic mappings randomly all over the place, because we understand the consequences and we'd want to rely on the library as well and we don't like to break the backward-compatibility at all.

If it so happens that a symbol of a major token is forked or has to be changed, then the control is still in the users' hands. The exchange.commonCurrencies property can be overrided upon initialization or later, just like any other exchange property. If a significant token is involved, we usually post instructions on how to retain the old behavior by adding a couple of lines to the constructor params.

It depends on which exchange you are using, but some of them have a reversed (inconsistent) pairing of base and quote. They actually have base and quote misplaced (switched/reversed sides). In that case you'll see a difference of parsed base and quote currency values with the unparsed info in the market substructure.

For those exchanges the ccxt will do a correction, switching and normalizing sides of base and quote currencies when parsing exchange replies. This logic is financially and terminologically correct. If you want less confusion, remember the following rule: base is always before the slash, quote is always after the slash in any symbol and with any market.

We currently load spot markets with the unified BASE/QUOTE symbol schema into the .markets mapping, indexed by symbol. This would cause a naming conflict for futures and other derivatives that have the same symbol as their spot market counterparts. To accomodate both types of markets in the .markets we require the symbols between 'future' and 'spot' markets to be distinct, as well as the symbols between 'linear' and 'inverse' contracts to be distinct.

Please, check this announcement: Unified contract naming conventions

CCXT supports the following types of derivative contracts:

A future market symbol consists of the underlying currency, the quoting currency, the settlement currency and an arbitrary identifier. Most often the identifier is the settlement date of the future contract in YYMMDD format:

The loadMarkets () / load_markets () is also a dirty method with a side effect of saving the array of markets on the exchange instance. You only need to call it once per exchange. All subsequent calls to the same method will return the locally saved (cached) array of markets.

When exchange markets are loaded, you can then access market information any time via the markets property. This property contains an associative array of markets indexed by symbol. If you need to force reload the list of markets after you have them loaded already, pass the reload = true flag to the same method again.

Each exchange offers a set of API methods. Each method of the API is called an endpoint. Endpoints are HTTP URLs for querying various types of information. All endpoints return JSON in response to client requests.

Usually, there is an endpoint for getting a list of markets from an exchange, an endpoint for retrieving an order book for a particular market, an endpoint for retrieving trade history, endpoints for placing and canceling orders, for money deposit and withdrawal, etc... Basically every kind of action you could perform within a particular exchange has a separate endpoint URL offered by the API.

Because the set of methods differs from exchange to exchange, the ccxt library implements the following:

The endpoint URLs are predefined in the api property for each exchange. You don't have to override it, unless you are implementing a new exchange API (at least you should know what you're doing).

Most of exchange-specific API methods are implicit, meaning that they aren't defined explicitly anywhere in code. The library implements a declarative approach for defining implicit (non-unified) exchanges' API methods.

Each method of the API usually has its own endpoint. The library defines all endpoints for each particular exchange in the .api property. Upon exchange construction an implicit magic method (aka partial function or closure) will be created inside defineRestApi()/define_rest_api() on the exchange instance for each endpoint from the list of .api endpoints. This is performed for all exchanges universally. Each generated method will be accessible in both camelCase and under_score notations.

The endpoints definition is a full list of ALL API URLs exposed by an exchange. This list gets converted to callable methods upon exchange instantiation. Each URL in the API endpoint list gets a corresponding callable method. This is done automatically for all exchanges, therefore the ccxt library supports all possible URLs offered by crypto exchanges.

Each implicit method gets a unique name which is constructed from the .api definition. For example, a private HTTPS PUT https://api.exchange.com/order/{id}/cancel endpoint will have a corresponding exchange method named .privatePutOrderIdCancel()/.private_put_order_id_cancel(). A public HTTPS GET https://api.exchange.com/market/ticker/{pair} endpoint would result in the corresponding method named .publicGetTickerPair()/.public_get_ticker_pair(), and so on.

An implicit method takes a dictionary of parameters, sends the request to the exchange and returns an exchange-specific JSON result from the API as is, unparsed. To pass a parameter, add it to the dictionary explicitly under a key equal to the parameter's name. For the examples above, this would look like .privatePutOrderIdCancel ({ id: '41987a2b-...' }) and .publicGetTickerPair ({ pair: 'BTC/USD' }).

The recommended way of working with exchanges is not using exchange-specific implicit methods but using the unified ccxt methods instead. The exchange-specific methods should be used as a fallback in cases when a corresponding unified method isn't available (yet).

To get a list of all available methods with an exchange instance, including implicit methods and unified methods you can simply do the following:

API URLs are often grouped into two sets of methods called a public API for market data and a private API for trading and account access. These groups of API methods are usually prefixed with a word 'public' or 'private'.

A public API is used to access market data and does not require any authentication whatsoever. Most exchanges provide market data openly to all (under their rate limit). With the ccxt library anyone can access market data out of the box without having to register with the exchanges and without setting up account keys and passwords.

Public APIs include the following:

The private API is mostly used for trading and for accessing account-specific private data, therefore it requires authentication. You have to get the private API keys from the exchanges. It often means registering with an exchange website and creating the API keys for your account. Most exchanges require personal information or identification. Some exchanges will only allow trading after completing the KYC verification. Private APIs allow the following:

Some exchanges offer the same logic under different names. For example, a public API is also often called market data, basic, market, mapi, api, price, etc... All of them mean a set of methods for accessing data available to public. A private API is also often called trading, trade, tapi, exchange, account, etc...

A few exchanges also expose a merchant API which allows you to create invoices and accept crypto and fiat payments from your clients. This kind of API is often called merchant, wallet, payment, ecapi (for e-commerce).

To get a list of all available methods with an exchange instance, you can simply do the following:

contract only and margin only

In the JavaScript version of CCXT all methods are asynchronous and return Promises that resolve with a decoded JSON object. In CCXT we use the modern async/await syntax to work with Promises. If you're not familiar with that syntax, you can read more about it here.

The ccxt library supports asynchronous concurrency mode in Python 3.5+ with async/await syntax. The asynchronous Python version uses pure asyncio with aiohttp. In async mode you have all the same properties and methods, but most methods are decorated with an async keyword. If you want to use async mode, you should link against the ccxt.async_support subpackage, like in the following example:

CCXT support PHP 8+ versions. The library has both synchronous and asynchronous versions. To use synchronous version, use \ccxt namespace (i.e. new ccxt\binance()) and to use asynchronous version, use \ccxt\async namespace (i.e. new ccxt\async\binance()). Asynchronous version uses ReactPHP library in the background. In async mode you have all the same properties and methods, but any networking API method should be decorated with the \React\Async\await keyword and your script should be in a ReactPHP wrapper:

See further examples in the examples/php directory; look for filenames that include the async word. Also, make sure you have installed the required dependencies using composer require recoil/recoil clue/buzz-react react/event-loop recoil/react react/http. Lastly, this article provides a good introduction to the methods used here. While syntactically the change is simple (i.e., just using a yield keyword before relevant methods), concurrency has significant implications for the overall design of your code.

All public and private API methods return raw decoded JSON objects in response from the exchanges, as is, untouched. The unified API returns JSON-decoded objects in a common format and structured uniformly across all exchanges.

The set of all possible API endpoints differs from exchange to exchange. Most of methods accept a single associative array (or a Python dict) of key-value parameters. The params are passed as follows:

The unified methods of exchanges might expect and will accept various params which affect their functionality, like:

An exchange will not accept the params from a different exchange, they're not interchangeable. The list of accepted parameters is defined by each specific exchange.

To find which parameters can be passed to a unified method:

For a full list of accepted method parameters for each exchange, please consult API docs.

An exchange method name is a concatenated string consisting of type (public or private), HTTP method (GET, POST, PUT, DELETE) and endpoint URL path like in the following examples:

The ccxt library supports both camelcase notation (preferred in JavaScript) and underscore notation (preferred in Python and PHP), therefore all methods can be called in either notation or coding style in any language. Both of these notations work in JavaScript, Python and PHP:

To get a list of all available methods with an exchange instance, you can simply do the following:

The unified ccxt API is a subset of methods common among the exchanges. It currently contains the following methods:

Note, that most of methods of the unified API accept an optional params argument. It is an associative array (a dictionary, empty by default) containing the params you want to override. The contents of params are exchange-specific, consult the exchanges' API documentation for supported fields and values. Use the params dictionary if you need to pass a custom setting or an optional parameter to your unified query.

Most of unified methods will return either a single object or a plain array (a list) of objects (trades, orders, transactions and so on). However, very few exchanges (if any at all) will return all orders, all trades, all ohlcv candles or all transactions at once. Most often their APIs limit output to a certain number of most recent objects. YOU CANNOT GET ALL OBJECTS SINCE THE BEGINNING OF TIME TO THE PRESENT MOMENT IN JUST ONE CALL. Practically, very few exchanges will tolerate or allow that.

To fetch historical orders or trades, the user will need to traverse the data in portions or "pages" of objects. Pagination often implies "fetching portions of data one by one" in a loop.

In most cases users are required to use at least some type of pagination in order to get the expected results consistently. If the user does not apply any pagination, most methods will return the exchanges' default, which may start from the beginning of history or may be a subset of most recent objects. The default behaviour (without pagination) is exchange-specific! The means of pagination are often used with the following methods in particular:

With methods returning lists of objects, exchanges may offer one or more types of pagination. CCXT unifies date-based pagination by default, with timestamps in milliseconds throughout the entire library.

Warning: this is an experimental feature and might produce unexpected/incorrect results in some instances.

Recently, CCXT introduced a way to paginate through several results automatically by just providing the paginate flag inside params, lifting this work from the userland. Most leading exchanges support it, and more will be added in the future, but the easiest way to check it is to look in the method's documentation and search for the pagination parameter. As always there are exceptions, and some endpoints might not provide a way to paginate either through a timestamp or a cursor, and in those cases, there's nothing CCXT can do about it.

Right now, we have three different ways of paginating:

The user cannot select the pagination method used, it will depend from implementation to implementation, considering the exchange API's features.

We can't perform an infinite amount of requests, and some of them might throw an error for different reasons, thus, we have some options that allow the user to control these variables and other pagination specificities.

All the options below, should be provided inside params, you can check the examples below

All unified timestamps throughout the CCXT library are integers in milliseconds unless explicitly stated otherwise.

Below is the set of methods for working with UTC dates and timestamps and for converting between them:

This is the type of pagination currently used throughout the CCXT Unified API. The user supplies a since timestamp in milliseconds (!) and a number to limit results. To traverse the objects of interest page by page, the user runs the following (below is pseudocode, it may require overriding some exchange-specific params, depending on the exchange in question):

The user supplies a from_id of the object, from where the query should continue returning results, and a number to limit results. This is the default with some exchanges, however, this type is not unified (yet). To paginate objects based on their ids, the user would run the following:

The user supplies a page number or an initial "cursor" value. The exchange returns a page of results and the next "cursor" value, to proceed from. Most of exchanges that implement this type of pagination will either return the next cursor within the response itself or will return the next cursor values within HTTP response headers.

See an example implementation here: https://github.com/ccxt/ccxt/blob/master/examples/py/coinbasepro-fetch-my-trades-pagination.py

Upon each iteration of the loop the user has to take the next cursor and put it into the overrided params for the next query (on the following iteration):

Exchanges expose information on open orders with bid (buy) and ask (sell) prices, volumes and other data. Usually there is a separate endpoint for querying current state (stack frame) of the order book for a particular market. An order book is also often called market depth. The order book information is used in the trading decision making process.

To get data on order books, you can use

The timestamp and datetime may be missing (undefined/None/null) if the exchange in question does not provide a corresponding value in the API response.

Prices and amounts are floats. The bids array is sorted by price in descending order. The best (highest) bid price is the first element and the worst (lowest) bid price is the last element. The asks array is sorted by price in ascending order. The best (lowest) ask price is the first element and the worst (highest) ask price is the last element. Bid/ask arrays can be empty if there are no corresponding orders in the order book of an exchange.

Exchanges may return the stack of orders in various levels of details for analysis. It is either in full detail containing each and every order, or it is aggregated having slightly less detail where orders are grouped and merged by price and volume. Having greater detail requires more traffic and bandwidth and is slower in general but gives a benefit of higher precision. Having less detail is usually faster, but may not be enough in some very specific cases.

Some exchanges accept a dictionary of extra parameters to the fetchOrderBook () / fetch_order_book () function. All extra params are exchange-specific (non-unified). You will need to consult exchanges docs if you want to override a particular param, like the depth of the order book. You can get a limited count of returned orders or a desired level of aggregation (aka market depth) by specifying an limit argument and exchange-specific extra params like so:

The levels of detail or levels of order book aggregation are often number-labelled like L1, L2, L3...

If you want to get an L2 order book, whatever the exchange returns, use the fetchL2OrderBook(symbol, limit, params) or fetch_l2_order_book(symbol, limit, params) unified method for that.

The limit argument does not guarantee that the number of bids or asks will always be equal to limit. It designates the upper boundary or the maximum, so at some moment in time there may be less than limit bids or asks. This is the case when the exchange does not have enough orders on the orderbook. However, if the underlying exchange API does not support a limit parameter for the orderbook endpoint at all, then the limit argument will be ignored. CCXT does not trim bids and asks if the exchange returns more than you request.

In order to get current best price (query market price) and calculate bidask spread take first elements from bid and ask, like so:

A price ticker contains statistics for a particular market/symbol for some period of time in recent past, usually last 24 hours. The methods for fetching tickers are described below.

Check the exchange.has['fetchTicker'] and exchange.has['fetchTickers'] properties of the exchange instance to determine if the exchange in question does support these methods.

Please, note, that calling fetchTickers () without a symbol is usually strictly rate-limited, an exchange may ban you if you poll that endpoint too frequently.

A ticker is a statistical calculation with the information calculated over the past 24 hours for a specific market.

The structure of a ticker is as follows:

All prices in ticker structure are in quote currency. Some fields in a returned ticker structure may be undefined/None/null.

Timestamp and datetime are both Universal Time Coordinated (UTC) in milliseconds.

Although some exchanges do mix-in orderbook's top bid/ask prices into their tickers (and some exchanges even serve top bid/ask volumes) you should not treat a ticker as a fetchOrderBook replacement. The main purpose of a ticker is to serve statistical data, as such, treat it as "live 24h OHLCV". It is known that exchanges discourage frequent fetchTicker requests by imposing stricter rate limits on these queries. If you need a unified way to access bids and asks you should use fetchL[123]OrderBook family instead.

To get historical prices and volumes use the unified fetchOHLCV method where available. To get historical mark, index, and premium index prices, add one of 'price': 'mark', 'price': 'index', 'price': 'premiumIndex' respectively to the params-overrides of fetchOHLCV. There are also convenience methods fetchMarkPriceOHLCV, fetchIndexPriceOHLCV, and fetchPremiumIndexOHLCV that obtain the mark, index and premiumIndex historical prices and volumes.

Methods for fetching tickers:

To get the individual ticker data from an exchange for a particular trading pair or a specific symbol – call the fetchTicker (symbol):

Some exchanges (not all of them) also support fetching all tickers at once. See their docs for details. You can fetch all tickers with a single call like so:

Fetching all tickers requires more traffic than fetching a single ticker. Also, note that some exchanges impose higher rate-limits on subsequent fetches of all tickers (see their docs on corresponding endpoints for details). The cost of the fetchTickers() call in terms of rate limit is often higher than average. If you only need one ticker, fetching by a particular symbol is faster as well. You probably want to fetch all tickers only if you really need all of them and, most likely, you don't want to fetchTickers more frequently than once in a minute or so.

Also, some exchanges may impose additional requirements on the fetchTickers() call, sometimes you can't fetch the tickers for all symbols because of the API limitations of the exchange in question. Some exchanges accept a list of symbols in HTTP URL query params, however, because URL length is limited, and in extreme cases exchanges can have thousands of markets – a list of all their symbols simply would not fit in the URL, so it has to be a limited subset of their symbols. Sometimes, there are other reasons for requiring a list of symbols, and there may be a limit on the number of symbols you can fetch at once, but whatever the limitation, please, blame the exchange. To pass the symbols of interest to the exchange, you can supply a list of strings as the first argument to fetchTickers:

Note that the list of symbols is not required in most cases, but you must add additional logic if you want to handle all possible limitations that might be imposed on the exchanges' side.

Like most methods of the Unified CCXT API, the last argument to fetchTickers is the params argument for overriding request parameters that are sent towards the exchange.

The structure of the returned value is as follows:

A general solution for fetching all tickers from all exchanges (even the ones that don't have a corresponding API endpoint) is on the way, this section will be updated soon.

Most exchanges have endpoints for fetching OHLCV data, but some of them don't. The exchange boolean (true/false) property named has['fetchOHLCV'] indicates whether the exchange supports candlestick data series or not.

To fetch OHLCV candles/bars from an exchange, ccxt has the fetchOHLCV method, which is declared in the following way:

You can call the unified fetchOHLCV / fetch_ohlcv method to get the list of OHLCV candles for a particular symbol like so:

To get the list of available timeframes for your exchange see the timeframes property. Note that it is only populated when has['fetchOHLCV'] is true as well.

The returned list of candles may have one or more missing periods, if the exchange did not have any trades for the specified timerange and symbol. To a user that would appear as gaps in a continuous list of candles. That is considered normal. If the exchange did not have any candles at that time, the CCXT library will show the results as returned from the exchange itself.

There's a limit on how far back in time your requests can go. Most of exchanges will not allow to query detailed candlestick history (like those for 1-minute and 5-minute timeframes) too far in the past. They usually keep a reasonable amount of most recent candles, like 1000 last candles for any timeframe is more than enough for most of needs. You can work around that limitation by continuously fetching (aka REST polling) latest OHLCVs and storing them in a CSV file or in a database.

Note that the info from the last (current) candle may be incomplete until the candle is closed (until the next candle starts).

Like with most other unified and implicit methods, the fetchOHLCV method accepts as its last argument an associative array (a dictionary) of extra params, which is used to override default values that are sent in requests to the exchanges. The contents of params are exchange-specific, consult the exchanges' API documentation for supported fields and values.

The since argument is an integer UTC timestamp in milliseconds (everywhere throughout the library with all unified methods).

If since is not specified the fetchOHLCV method will return the time range as is the default from the exchange itself. This is not a bug. Some exchanges will return candles from the beginning of time, others will return most recent candles only, the exchanges' default behaviour is expected. Thus, without specifying since the range of returned candles will be exchange-specific. One should pass the since argument to ensure getting precisely the history range needed.

Currently, the structure CCXT uses does not include the raw response from the exchange. However, users might be able to override the return value by doing:

Trading strategies require fresh up-to-date information for technical analysis, indicators and signals. Building a speculative trading strategy based on the OHLCV candles received from the exchange may have critical drawbacks. Developers should account for the details explained in this section to build successful bots.

First and foremost, when using CCXT you're talking to the exchanges directly. CCXT is not a server, nor a service, it's a software library. All data that you are getting with CCXT is received directly from the exchanges first-hand.

The exchanges usually provide two categories of public market data:

The primary first-order data is updated by the exchanges APIs in pseudo real time, or as close to real time as possible, as fast as possible. The second-order data requires time for the exchange to calculate it. For example, a ticker is nothing more than a rolling 24-hour statistical cut of orderbooks and trades. OHLCV candles and volumes are also calculated from first-order trades and represent fixed statistical cuts of specific periods. The volume traded within an hour is just a sum of traded volumes of the corresponding trades that happened within that hour.

Obviously, it takes some time for the exchange to collect the first-order data and calculate the secondary statistical data from it. That literally means that tickers and OHLCVs are always slower than orderbooks and trades. In other words, there is always some latency in the exchange API between the moment when a trade happens and the moment when a corresponding OHLCV candle is updated or published by the exchange API.

The latency (or how much time is needed by the exchange API for calculating the secondary data) depends on how fast the exchange engine is, so it is exchange-specific. Top exchange engines will usually return and update fresh last-minute OHLCV candles and tickers at a very fast rate. Some exchanges might do it in regular intervals like once a second or once in a few seconds. Slow exchange engines might take minutes to update the secondary statistical information, their APIs might return the current most recent OHLCV candle a few minutes late.

If your strategy depends on the fresh last-minute most recent data you don't want to build it based on tickers or OHLCVs received from the exchange. Tickers and exchanges' OHLCVs are only suitable for display purposes, or for simple trading strategies for hour-timeframes or day-timeframes that are less susceptible to latency.

Thankfully, the developers of time-critical trading strategies don't have to rely on secondary data from the exchanges and can calculate the OHLCVs and tickers in the userland. That may be faster and more efficient than waiting for the exchanges to update the info on their end. One can aggregate the public trade history by polling it frequently and calculate candles by walking over the list of trades - please take a look into "build-ohlcv-bars" file inside examples folder

Due to the differences in their internal implementations the exchanges may be faster to update their primary and secondary market data over WebSockets. The latency remains exchange-specific, cause the exchange engine still needs time to calculate the secondary data, regardless of whether you're polling it over the RESTful API with CCXT or getting updates via WebSockets with CCXT Pro. WebSockets can improve the networking latency, so a fast exchange will work even better, but adding the support for WS subscriptions will not make a slow exchange engine work much faster.

If you want to stay on top of the second-order data latency, then you will have to calculate it on your side and beat the exchange engine in speed of doing so. Depending on the needs of your application, it may be tricky, since you will need to handle redundancy, "data holes" in the history, exchange downtimes, and other aspects of data aggregation which is a whole universe in itself that is impossible to fully cover in this Manual.

As noted in above paragraph, users can build candles manually using buildOHLCV / build_ohlcv method. You can see an example file named "build-ohlcv-bars" inside examples folder. Notes:

The fetchOHLCV method shown above returns a list (a flat array) of OHLCV candles represented by the following structure:

The list of candles is returned sorted in ascending (historical/chronological) order, oldest candle first, most recent candle last.

To obtain historical Mark, Index Price and Premium Index candlesticks pass the 'price' params-override to fetchOHLCV. The 'price' parameter accepts one of the following values:

There are also convenience methods fetchMarkOHLCV, fetchIndexOHLCV and fetchPremiumIndexOHLCV

You can call the unified fetchTrades / fetch_trades method to get the list of most recent trades for a particular symbol. The fetchTrades method is declared in the following way:

For example, if you want to print recent trades for all symbols one by one sequentially (mind the rateLimit!) you would do it like so:

The fetchTrades method shown above returns an ordered list of trades (a flat array, sorted by timestamp in ascending order, oldest trade first, most recent trade last). A list of trades is represented by the trade structure.

Most exchanges return most of the above fields for each trade, though there are exchanges that don't return the type, the side, the trade id or the order id of the trade. Most of the time you are guaranteed to have the timestamp, the datetime, the symbol, the price and the amount of each trade.

The second optional argument since reduces the array by timestamp, the third limit argument reduces by number (count) of returned items.

If the user does not specify since, the fetchTrades method will return the default range of public trades from the exchange. The default set is exchange-specific, some exchanges will return trades starting from the date of listing a pair on the exchange, other exchanges will return a reduced set of trades (like, last 24 hours, last 100 trades, etc). If the user wants precise control over the timeframe, the user is responsible for specifying the since argument.

Most of unified methods will return either a single object or a plain array (a list) of objects (trades). However, very few exchanges (if any at all) will return all trades at once. Most often their APIs limit output to a certain number of most recent objects. YOU CANNOT GET ALL OBJECTS SINCE THE BEGINNING OF TIME TO THE PRESENT MOMENT IN JUST ONE CALL. Practically, very few exchanges will tolerate or allow that.

To fetch historical trades, the user will need to traverse the data in portions or "pages" of objects. Pagination often implies "fetching portions of data one by one" in a loop.

In most cases users are required to use at least some type of pagination in order to get the expected results consistently.

On the other hand, some exchanges don't support pagination for public trades at all. In general the exchanges will provide just the most recent trades.

The fetchTrades () / fetch_trades() method also accepts an optional params (assoc-key array/dict, empty by default) as its fourth argument. You can use it to pass extra params to method calls or to override a particular default value (where supported by the exchange). See the API docs for your exchange for more details.

The fetchTime() method (if available) returns the current integer timestamp in milliseconds from the exchange server.

The exchange status describes the latest known information on the availability of the exchange API. This information is either hardcoded into the exchange class or fetched live directly from the exchange API. The fetchStatus(params = {}) method can be used to get this information. The status returned by fetchStatus is one of:

The fetchStatus() method will return a status structure like shown below:

The possible values in the status field are:

When short trading or trading with leverage on a spot market, currency must be borrowed. Interest is accrued for the borrowed currency.

Data on the borrow rate for a currency can be retrieved using

The fetchBorrowRateHistory method retrieves a history of a currencies borrow interest rate at specific time slots

The fetchLeverageTiers() method can be used to obtain the maximum leverage for a market at varying position sizes. It can also be used to obtain the maintenance margin rate, and the max tradeable amount for a market when that information is not available from the market object

While you can obtain the absolute maximum leverage for a market by accessing market['limits']['leverage']['max'], for many contract markets, the maximum leverage will depend on the size of your position.

You can access those limits by using

In the example above:

Note for Huobi users: Huobi uses both leverage and amount to determine maintenance margin rates: https://www.huobi.com/support/en-us/detail/900000089903

Data on the current, most recent, and next funding rates can be obtained using the methods

Retrieve the current funding interval using the following methods:

Use the fetchOpenInterest method to get the current open interest for a symbol from the exchange. Use fetchOpenInterests to get the current open interest for multiple symbols

Use the fetchOpenInterestHistory method to get a history of open interest for a symbol from the exchange.

Note for OKX users: instead of a unified symbol okx.fetchOpenInterestHistory expects a unified currency code in the symbol argument (e.g. 'BTC').

Use the fetchVolatilityHistory method to get the volatility history for the code of an options underlying asset from the exchange.

Use the fetchUnderlyingAssets method to get the market id's of underlying assets for a contract market type from the exchange.

Use the fetchSettlementHistory method to get the public settlement history for a contract market from the exchange. Use fetchMySettlementHistory to get only your settlement history

margin and contract only

Use the fetchLiquidations method to get the public liquidations of a trading pair from the exchange. Use fetchMyLiquidations to get only your liquidation history

Use the fetchGreeks method to get the public greeks and implied volatility of an options trading pair from the exchange. Use fetchAllGreeks to get the greeks for all symbols or multiple symbols. The greeks measure how factors like the underlying assets price, time to expiration, volatility, and interest rates, affect the price of an options contract.

// for example fetchAllGreeks () // all symbols fetchAllGreeks ([ 'BTC/USD:BTC-240927-40000-C', 'ETH/USD:ETH-240927-4000-C' ]) // an array of specific symbols

Use the fetchOption method to get the public details of a single option contract from the exchange.

Use the fetchOptionChain method to get the public option chain data of an underlying currency from the exchange.

Use the fetchLongShortRatio method to fetch the current long short ratio of a symbol and use the fetchLongShortRatioHistory to fetch the history of long short ratios for a symbol.

In order to be able to access your user account, perform algorithmic trading by placing market and limit orders, query balances, deposit and withdraw funds and so on, you need to obtain your API keys for authentication from each exchange you want to trade with. They usually have it available on a separate tab or page within your user account settings. API keys are exchange-specific and cannnot be interchanged under any circumstances.

The exchanges' private APIs will usually allow the following types of interaction:

Authentication with all exchanges is handled automatically if provided with proper API keys. The process of authentication usually goes through the following pattern:

This process may differ from exchange to exchange. Some exchanges may want the signature in a different encoding, some of them vary in header and body param names and formats, but the general pattern is the same for all of them.

You should not share the same API keypair across multiple instances of an exchange running simultaneously, in separate scripts or in multiple threads. Using the same keypair from different instances simultaneously may cause all sorts of unexpected behaviour.

DO NOT REUSE API KEYS WITH DIFFERENT SOFTWARE! The other software will screw your nonce too high. If you get InvalidNonce errors – make sure to generate a fresh new keypair first and foremost.

The authentication is already handled for you, so you don't need to perform any of those steps manually unless you are implementing a new exchange class. The only thing you need for trading is the actual API key pair.

The API credentials usually include the following:

In order to create API keys find the API tab or button in your user settings on the exchange website. Then create your keys and copy-paste them to your config file. Your config file permissions should be set appropriately, unreadable to anyone except the owner.

Remember to keep your apiKey and secret key safe from unauthorized use, do not send or tell it to anybody. A leak of the secret key or a breach in security can cost you a fund loss.

For checking if the user has supplied all the required credentials the Exchange base class has a method called exchange.checkRequiredCredentials() or exchange.check_required_credentials(). Calling that method will throw an AuthenticationError, if some of the credentials are missing or empty. The Exchange base class also has property exchange.requiredCredentials that allows a user to see which credentials are required for this or that exchange, as shown below:

To set up an exchange for trading just assign the API credentials to an existing exchange instance or pass them to exchange constructor upon instantiation, like so:

Note that your private requests will fail with an exception or error if you don't set up your API credentials before you start trading. To avoid character escaping always write your credentials in single quotes, not double quotes ('VERY_GOOD', "VERY_BAD").

When you get errors like "Invalid API-key, IP, or permissions for action." or "API-key format invalid", then, most likely, the problem is not within ccxt, please avoid opening a new issue unless you ensure that:

Some exchanges required you to sign in prior to calling private methods, which can be done using the signIn method

The default nonce is defined by the underlying exchange. You can override it with a milliseconds-nonce if you want to make private requests more frequently than once per second! Most exchanges will throttle your requests if you hit their rate limits, read API docs for your exchange carefully!

In case you need to reset the nonce it is much easier to create another pair of keys for using with private APIs. Creating new keys and setting up a fresh unused keypair in your config is usually enough for that.

In some cases you are unable to create new keys due to lack of permissions or whatever. If that happens you can still override the nonce. Base market class has the following methods for convenience:

There are exchanges that confuse milliseconds with microseconds in their API docs, let's all forgive them for that, folks. You can use methods listed above to override the nonce value. If you need to use the same keypair from multiple instances simultaneously use closures or a common function to avoid nonce conflicts. In Javascript you can override the nonce by providing a nonce parameter to the exchange constructor or by setting it explicitly on exchange object:

In Python and PHP you can do the same by subclassing and overriding nonce function of a particular exchange class:

You can get all the accounts associated with a profile by using the fetchAccounts() method

The fetchAccounts() method will return a structure like shown below:

Types of account is one of the unified account types or subaccount

To query for balance and get the amount of funds available for trading or funds locked in orders, use the fetchBalance method:

The timestamp and datetime values may be undefined or missing if the underlying exchange does not provide them.

Some exchanges may not return full balance info. Many exchanges do not return balances for your empty or unused accounts. In that case some currencies may be missing in returned balance structure.

Most of the time you can query orders by an id or by a symbol, though not all exchanges offer a full and flexible set of endpoints for querying orders. Some exchanges might not have a method for fetching recently closed orders, the other can lack a method for getting an order by id, etc. The ccxt library will target those cases by making workarounds where possible.

The list of methods for querying orders consists of the following:

Note that the naming of those methods indicates if the method returns a single order or multiple orders (an array/list of orders). The fetchOrder() method requires a mandatory order id argument (a string). Some exchanges also require a symbol to fetch an order by id, where order ids can intersect with various trading pairs. Also, note that all other methods above return an array (a list) of orders. Most of them will require a symbol argument as well, however, some exchanges allow querying with a symbol unspecified (meaning all symbols).

The library will throw a NotSupported exception if a user calls a method that is not available from the exchange or is not implemented in ccxt.

To check if any of the above methods are available, look into the .has property of the exchange:

A typical structure of the .has property usually contains the following flags corresponding to order API methods for querying orders:

The meanings of boolean true and false are obvious. A string value of emulated means that particular method is missing in the exchange API and ccxt will workaround that where possible on the client-side.

The exchanges' order management APIs differ by design. The user has to understand the purpose of each specific method and how they're combined together into a complete order API:

The majority of the exchanges will have a way of fetching currently-open orders. Thus, the exchange.has['fetchOpenOrders']. If that method is not available, then most likely the exchange.has['fetchOrders'] that will provide a list of all orders. The exchange will return a list of open orders either from fetchOpenOrders() or from fetchOrders(). One of the two methods is usually available from any exchange.

Some exchanges will provide the order history, other exchanges will not. If the underlying exchange provides the order history, then the exchange.has['fetchClosedOrders'] or the exchange.has['fetchOrders']. If the underlying exchange does not provide the order history, then fetchClosedOrders() and fetchOrders() are not available. In the latter case, the user is required to build a local cache of orders and track the open orders using fetchOpenOrders() and fetchOrder() for order statuses and for marking them as closed locally in the userland (when they're not open anymore).

If the underlying exchange does not have methods for order history (fetchClosedOrders() and fetchOrders()), then it will provide fetchOpenOrders + the trade history with fetchMyTrades (see How Orders Are Related To Trades). That set of information is in many cases enough for tracking in a live-trading robot. If there's no order history – you have to track your live orders and restore historical info from open orders and historical trades.

In general, the underlying exchanges will usually provide one or more of the following types of historical data:

Any of the above three methods may be missing, but the exchanges APIs will usually provide at least one of the three methods.

If the underlying exchange does not provide historical orders, the CCXT library will not emulate the missing functionality – it has to be added on the user side where necessary.

Please, note, that a certain method may be missing either because the exchange does not have a corresponding API endpoint, or because CCXT has not implemented it yet (the library is also a work in progress). In the latter case, the missing method will be added as soon as possible.

All methods returning lists of trades and lists of orders, accept the second since argument and the third limit argument:

The second argument since reduces the array by timestamp, the third limit argument reduces by number (count) of returned items.

If the user does not specify since, the fetchTrades()/fetchOrders() methods will return the default set of results from the exchange. The default set is exchange-specific, some exchanges will return trades or recent orders starting from the date of listing a pair on the exchange, other exchanges will return a reduced set of trades or orders (like, last 24 hours, last 100 trades, first 100 orders, etc). If the user wants precise control over the timeframe, the user is responsible for specifying the since argument.

NOTE: not all exchanges provide means for filtering the lists of trades and orders by starting time, so, the support for since and limit is exchange-specific. However, most exchanges do provide at least some alternative for "pagination" and "scrolling" which can be overrided with extra params argument.

Some exchanges do not have a method for fetching closed orders or all orders. They will offer just the fetchOpenOrders() endpoint, and sometimes also a fetchOrder endpoint as well. Those exchanges don't have any methods for fetching the order history. To maintain the order history for those exchanges the user has to store a dictionary or a database of orders in the userland and update the orders in the database after calling methods like createOrder(), fetchOpenOrders(), cancelOrder(), cancelAllOrders().

To get the details of a particular order by its id, use the fetchOrder() / fetch_order() method. Some exchanges also require a symbol even when fetching a particular order by id.

The signature of the fetchOrder/fetch_order method is as follows:

Some exchanges don't have an endpoint for fetching an order by id, ccxt will emulate it where possible. For now it may still be missing here and there, as this is a work in progress.

You can pass custom overrided key-values in the additional params argument to supply a specific order type, or some other setting if needed.

Below are examples of using the fetchOrder method to get order info from an authenticated exchange instance:

Some exchanges don't have an endpoint for fetching all orders, ccxt will emulate it where possible. For now it may still be missing here and there, as this is a work in progress.

Do not confuse closed orders with trades aka fills ! An order can be closed (filled) with multiple opposing trades! So, a closed order is not the same as a trade. In general, the order does not have a fee at all, but each particular user trade does have fee, cost and other properties. However, many exchanges propagate those properties to the orders as well.

Some exchanges don't have an endpoint for fetching closed orders, ccxt will emulate it where possible. For now it may still be missing here and there, as this is a work in progress.

Most of methods returning orders within ccxt unified API will yield an order structure as described below:

The timeInForce field may be undefined/None/null if not specified by the exchange. The unification of timeInForce is a work in progress.

Possible values for thetimeInForce field:

There are different types of orders that a user can send to the exchange, regular orders eventually land in the orderbook of a corresponding symbol, others orders may be more advanced. Here is a list outlining various types of orders:

Placing an order always requires a symbol that the user has to specify (which market you want to trade).

To place an order use the createOrder method. You can use the id from the returned unified order structure to query the status and the state of the order later. If you need to place multiple orders simultaneously, you can check the availability of the createOrders method.

Some fields from the returned order structure may be undefined / None / null if that information is not returned from the exchange API's response. The user is guaranteed that the createOrder method will return a unified order structure that will contain at least the order id and the info (a raw response from the exchange "as is"):

This error happens when the exchange is expecting a natural number of contracts (1,2,3, etc) in the amount argument of createOrder. The market structure has a key called contractSize. Each contract is worth a certain amount of the base asset that is determined by the contractSize. The number of contracts multiplied by the contractSize is equal to the base amount. Base amount = (contracts * contractSize) so to derive the number of contracts you should enter in the amount argument you can solve for contracts: contracts = (Base amount / contractSize).

Here is an example of finding the contractSize:

Limit orders placed on the order book of the exchange for a price specified by the trader. They are fullfilled(closed) when there are no orders in the same market at a better price, and another trader creates a market order or an opposite order for a price that matches or exceeds the price of the limit order.

Limit orders may not be fully filled. This happens when the filling order is for a smaller amount than the amount specified by the limit order.

Market orders are executed immediately by fulfilling one of more already existing orders from the ask side of the exchanges order book. The orders that your market order fulfills are chosen from th top of the order book stack, meaning your market order is fulfilled at the best price available. When placing a market order you don't need to specify the price of the order, and if the price is specified, it will be ignored.

You are not guaranteed that the order will be executed for the price you observe prior to placing your order. There are multiple reasons for this, including:

price slippage a slight change of the price for the traded market while your order is being executed. Reasons for price slippage include, but are not limited to

unequivocal order sizes if a market order is for an amount that is larger than the size of the top order on the order book, then after the top order is filled, the market order will proceed to fill the next order in the order book, which means the market order is filled at multiple prices

Note, that some exchanges will not accept market orders (they allow limit orders only). In order to detect programmatically if the exchange in question does support market orders or not, you can use the .has['createMarketOrder'] exchange property:

In general, when placing a market buy or market sell order the user has to specify just the amount of the base currency to buy or sell. However, with some exchanges market buy orders implement a different approach to calculating the value of the order.

Suppose you're trading BTC/USD and the current market price for BTC is over 9000 USD. For a market buy or market sell you could specify an amount of 2 BTC and that would result in plus or minus 18000 USD (more or less ;)) on your account, depending on the side of the order.

With market buys some exchanges require the total cost of the order in the quote currency! The logic behind it is simple, instead of taking the amount of base currency to buy or sell some exchanges operate with "how much quote currency you want to spend on buying in total".

To place a market buy order with those exchanges you would not specify an amount of 2 BTC, instead you should somehow specify the total cost of the order, that is, 18000 USD in this example. The exchanges that treat market buy orders in this way have an exchange-specific option createMarketBuyOrderRequiresPrice that allows specifying the total cost of a market buy order in two ways.

The first is the default and if you specify the price along with the amount the total cost of the order would be calculated inside the lib from those two values with a simple multiplication (cost = amount * price). The resulting cost would be the amount in USD quote currency that will be spent on this particular market buy order.

The second alternative is useful in cases when the user wants to calculate and specify the resulting total cost of the order himself. That can be done by setting the createMarketBuyOrderRequiresPrice option to false to switch it off:

It is also possible to emulate a market order with a limit order.

WARNING this method can be risky due to high volatility, use it at your own risk and only use it when you know really well what you're doing!

Most of the time a market sell can be emulated with a limit sell at a very low price – the exchange will automatically make it a taker order for market price (the price that is currently in your best interest from the ones that are available in the order book). When the exchange detects that you're selling for a very low price it will automatically offer you the best buyer price available from the order book. That is effectively the same as placing a market sell order. Thus market orders can be emulated with limit orders (where missing).

The opposite is also true – a market buy can be emulated with a limit buy for a very high price. Most exchanges will again close your order for best available price, that is, the market price.

However, you should never rely on that entirely, ALWAYS test it with a small amount first! You can try that in their web interface first to verify the logic. You can sell the minimal amount at a specified limit price (an affordable amount to lose, just in case) and then check the actual filling price in trade history.

Limit price orders are also known as limit orders. Some exchanges accept limit orders only. Limit orders require a price (rate per unit) to be submitted with the order. The exchange will close limit orders if and only if market price reaches the desired level.

Coming from traditional trading, the term "Stop order" has been a bit ambigious, so instead of it, in CCXT we use term "Trigger" order. When symbol's price reaches your "trigger"("stop") price, the order is activated as market or limit order, depending which one you had chosen.

We have different classification of trigger orders:

Traditional "stop" order (which you might see across exchanges' websites) is now called "trigger" order across CCXT library. Implemented by adding a triggerPrice parameter. They are independent basic trigger orders that can open or close a position.

Typically, exchange automatically determines triggerPrice's direction (whether it is "above" or "below" current price), however, some exchanges require that you provide triggerDirection with either ascending or descending values:

Note, you can also add reduceOnly: true param to the trigger order (with a possible triggerDirection: 'ascending/descending' param), so it would act as "stop-loss" or "take-profit" order. However, for some exchanges we support "stop-loss" and "take-profit" trigger order types, which automatically involve reduceOnly and triggerDirection handling (see them below).

The same as Trigger Orders, but the direction matters. Implemented by specifying a stopLossPrice parameter (for the stop loss triggerPrice), and also automatically implemented triggerDirection on behalf of user, so instead of regular Trigger Order, you can use this as an alternative.

Suppose you entered a long position (you bought) at 1000 and want to protect yourself from losses from a possible price drop below 700. You would place a stop loss order with triggerPrice at 700. For that stop loss order either you would specify a limit price or it will be executed at market price.

Suppose you entered a short position (you sold) at 700 and want to protect yourself from losses from a possible price pump above 1300. You would place a stop loss order with triggerPrice at 1300. For that stop loss order either you would specify a limit price or it will be executed at market price.

Stop Loss orders are activated when the price of the underlying asset/contract:

The same as Stop Loss Orders, but the direction matters. Implemented by specifying a takeProfitPrice parameter (for the take profit triggerPrice).

Suppose you entered a long position (you bought) at 1000 and want to get your profits from a possible price pump above 1300. You would place a take profit order with triggerPrice at 1300. For that take profit order either you would specify a limit price or it will be executed at market price.

Suppose you entered a short position (you sold) at 700 and want to get your profits from a possible price drop below 600. You would place a take profit order with triggerPrice at 600. For that take profit order either you would specify a limit price or it will be executed at market price.

Take Profit orders are activated when the price of the underlying:

Take Profit / Stop Loss Orders which are tied to a position-opening primary order. Implemented by supplying a dictionary parameters for stopLoss and takeProfit describing each respectively.

For exchanges, where it is not possible to use attached SL &TP, after submitting an entry order, you can immediatelly submit another order (even though position might not be open yet) with triggerPrice and reduceOnly: true params, so it can still act as a stoploss order for your upcoming position (note, this approach might not work for some exchanges).

Trailing Orders trail behind an open position. Implemented by supplying float parameters for trailingPercent or trailingAmount.

Not supported by all exchanges.

Note: This is still under unification and is a work in progress

Some exchanges allow you to specify optional parameters for your order. You can pass your optional parameters and override your query with an associative array using the params argument to your unified API call. All custom params are exchange-specific, of course, and aren't interchangeable, do not expect those custom params for one exchange to work with another exchange.

The user can specify a custom clientOrderId field can be set upon placing orders with the params. Using the clientOrderId one can later distinguish between own orders. This is only available for the exchanges that do support clientOrderId at this time. For the exchanges that don't support it will either throw an error upon supplying the clientOrderId or will ignore it setting the clientOrderId to undefined/None/null.

If exchange supports feature for hedged orders, user can pass params['hedged'] = true in createOrder to open a hedged position instead of default one-way mode order. However, if exchange supports .has['setPositionMode'] then those exchanges might not support hedged param directly through createOrder, instead on such exchange you need to change the account-mode at first using setPositionMode() and then run createOrder (without hedged param) and it will place hedged order by default.

To edit an order, you can use the editOrder method

To cancel an existing order use

The cancelOrder() is usually used on open orders only. However, it may happen that your order gets executed (filled and closed) before your cancel-request comes in, so a cancel-request might hit an already-closed order.

A cancel-request might also throw a OperationFailed indicating that the order might or might not have been canceled successfully and whether you need to retry or not. Consecutive calls to cancelOrder() may hit an already canceled order as well.

As such, cancelOrder() can throw an OrderNotFound exception in these cases:

A trade is also often called a fill. Each trade is a result of order execution. Note, that orders and trades have a one-to-many relationship: an execution of one order may result in several trades. However, when one order matches another opposing order, the pair of two matching orders yields one trade. Thus, when an order matches multiple opposing orders, this yields multiple trades, one trade per each pair of matched orders.

To put it shortly, an order can contain one or more trades. Or, in other words, an order can be filled with one or more trades.

For example, an orderbook can have the following orders (whatever trading symbol or pair it is):

All specific numbers above aren't real, this is just to illustrate the way orders and trades are related in general.

A seller decides to place a sell limit order on the ask side for a price of 0.700 and an amount of 150.

As the price and amount of the incoming sell (ask) order cover more than one bid order (orders b and i), the following sequence of events usually happens within an exchange engine very quickly, but not immediately:

Order b is matched against the incoming sell because their prices intersect. Their volumes "mutually annihilate" each other, so, the bidder gets 100 for a price of 0.800. The seller (asker) will have their sell order partially filled by bid volume 100 for a price of 0.800. Note that for the filled part of the order the seller gets a better price than he asked for initially. He asked for 0.7 at least but got 0.8 instead which is even better for the seller. Most conventional exchanges fill orders for the best price available.

A trade is generated for the order b against the incoming sell order. That trade "fills" the entire order b and most of the sell order. One trade is generated per each pair of matched orders, whether the amount was filled completely or partially. In this example the seller amount (100) fills order b completely (closes the order b) and also fills the selling order partially (leaves it open in the orderbook).

Order b now has a status of closed and a filled volume of 100. It contains one trade against the selling order. The selling order has an open status and a filled volume of 100. It contains one trade against order b. Thus each order has just one fill-trade so far.

The incoming sell order has a filled amount of 100 and has yet to fill the remaining amount of 50 from its initial amount of 150 in total.

The intermediate state of the orderbook is now (order b is closed and is not in the orderbook anymore):

Order i is matched against the remaining part of incoming sell, because their prices intersect. The amount of buying order i which is 200 completely annihilates the remaining sell amount of 50. The order i is filled partially by 50, but the rest of its volume, namely the remaining amount of 150 will stay in the orderbook. The selling order, however, is fulfilled completely by this second match.

A trade is generated for the order i against the incoming sell order. That trade partially fills order i. And completes the filling of the sell order. Again, this is just one trade for a pair of matched orders.

Order i now has a status of open, a filled amount of 50, and a remaining amount of 150. It contains one filling trade against the selling order. The selling order has a closed status now and it has completely filled its total initial amount of 150. However, it contains two trades, the first against order b and the second against order i. Thus each order can have one or more filling trades, depending on how their volumes were matched by the exchange engine.

After the above sequence takes place, the updated orderbook will look like this.

Notice that the order b has disappeared, the selling order also isn't there. All closed and fully-filled orders disappear from the orderbook. The order i which was filled partially and still has a remaining volume and an open status, is still there.

Most of unified methods will return either a single object or a plain array (a list) of objects (trades). However, very few exchanges (if any at all) will return all trades at once. Most often their APIs limit output to a certain number of most recent objects. YOU CANNOT GET ALL OBJECTS SINCE THE BEGINNING OF TIME TO THE PRESENT MOMENT IN JUST ONE CALL. Practically, very few exchanges will tolerate or allow that.

As with all other unified methods for fetching historical data, the fetchMyTrades method accepts a since argument for date-based pagination. Just like with all other unified methods throughout the CCXT library, the since argument for fetchMyTrades must be an integer timestamp in milliseconds.

To fetch historical trades, the user will need to traverse the data in portions or "pages" of objects. Pagination often implies "fetching portions of data one by one" in a loop.

In many cases a symbol argument is required by the exchanges' APIs, therefore you have to loop over all symbols to get all your trades. If the symbol is missing and the exchange requires it then CCXT will throw an ArgumentsRequired exception to signal the requirement to the user. And then the symbol has to be specified. One of the approaches is to filter the relevant symbols from the list of all symbols by looking at non-zero balances as well as transactions (withdrawals and deposits). Also, the exchanges will have a limit on how far back in time you can go.

In most cases users are required to use at least some type of pagination in order to get the expected results consistently.

Returns ordered array [] of trades (most recent trade last).

Trades denote the exchange of one currency for another, unlike transactions, which denote a transfer of a given coin.

The ledger is simply the history of changes, actions done by the user or operations that altered the user's balance in any way, that is, the history of movements of all funds from/to all accounts of the user which includes

Data on ledger entries can be retrieved using

The type of the ledger entry is the type of the operation associated with it. If the amount comes due to a sell order, then it is associated with a corresponding trade type ledger entry, and the referenceId will contain associated trade id (if the exchange in question provides it). If the amount comes out due to a withdrawal, then is associated with a corresponding transaction.

The referenceId field holds the id of the corresponding event that was registered by adding a new item to the ledger.

The status field is there to support for exchanges that include pending and canceled changes in the ledger. The ledger naturally represents the actual changes that have taken place, therefore the status is 'ok' in most cases.

The ledger entry type can be associated with a regular trade or a funding transaction (deposit or withdrawal) or an internal transfer between two accounts of the same user. If the ledger entry is associated with an internal transfer, the account field will contain the id of the account that is being altered with the ledger entry in question. The referenceAccount field will contain the id of the opposite account the funds are transferred to/from, depending on the direction ('in' or 'out').

In order to deposit cryptocurrency funds to an exchange you must get an address from the exchange for the currency you want to deposit using fetchDepositAddress. You can then call the withdraw method with the specified currency and address.

To deposit fiat currency on an exchange you can use the deposit method with data retrieved from the fetchDepositMethodId method. this deposit feature is currently supported on coinbase only, feel free to report any issues you find

A transaction structure

fetchDepositMethodId ()

A deposit id structure

fetchDepositMethodIds ()

The deposit id structure returned from fetchDepositMethodId, fetchDepositMethodIds look like this:

Data on deposits made to an account can be retrieved using

The withdraw method can be used to withdraw funds from an account

Some exchanges require a manual approval of each withdrawal by means of 2FA (2-factor authentication). In order to approve your withdrawal you usually have to either click their secret link in your email inbox or enter a Google Authenticator code or an Authy code on their website to verify that withdrawal transaction was requested intentionally.

In some cases you can also use the withdrawal id to check withdrawal status later (whether it succeeded or not) and to submit 2FA confirmation codes, where this is supported by the exchange. See their docs for details.

Data on withdrawals made to an account can be retrieved using

It is also possible to pass the parameters as the fourth argument with or without a specified tag

The following aliases of network allow for withdrawing crypto on multiple chains

You may set the value of exchange.withdraw ('USDT', 100, 'TVJ1fwyJ1a8JbtUxZ8Km95sDFN9jhLxJ2D', { 'network': 'TRX' }) in order to withdraw USDT on the TRON chain, or 'BSC' to withdraw USDT on Binance Smart Chain. In the table above BSC and BEP20 are equivalent aliases, so it doesn't matter which one you use as they both will achieve the same effect.

Transactions denote a transfer of a given coin, unlike trades, which denote the exchange of one currency for another.

The address for depositing can be either an already existing address that was created previously with the exchange or it can be created upon request. In order to see which of the two methods are supported, check the exchange.has['fetchDepositAddress'] and exchange.has['createDepositAddress'] properties.

Some exchanges may also have a method for fetching multiple deposit addresses at once or all of them at once.

The address structures returned from fetchDepositAddress, fetchDepositAddresses, fetchDepositAddressesByNetwork and createDepositAddress look like this:

With certain currencies, like AEON, BTS, GXS, NXT, SBD, STEEM, STR, XEM, XLM, XMR, XRP, an additional argument tag is usually required by exchanges. Other currencies will have the tag set to undefined / None / null. The tag is a memo or a message or a payment id that is attached to a withdrawal transaction. The tag is mandatory for those currencies and it identifies the recipient user account.

Be careful when specifying the tag and the address. The tag is NOT an arbitrary user-defined string of your choice! You cannot send user messages and comments in the tag. The purpose of the tag field is to address your wallet properly, so it must be correct. You should only use the tag received from the exchange you're working with, otherwise your transaction might never arrive to its destination.

The network field is relatively new, it may be undefined / None / null or missing entirely in certain cases (with some exchanges), but will be added everywhere eventually. It is still in the process of unification.

The transfer method makes internal transfers of funds between accounts on the same exchange. This can include subaccounts or accounts of different types (spot, margin, future, ...). If an exchange is separated on CCXT into a spot and futures class (e.g. binanceusdm, kucoinfutures, ...), then the method transferIn may be available to transfer funds into the futures account, and the method transferOut may be available to transfer funds out of the futures account

fromAccount and toAccount can accept the exchange account id or one of the following unified values:

You can retrieve all the account types by selecting the keys from `exchange.options['accountsByType']

Some exchanges allow transfers to email addresses, phone numbers or to other users by user id.

This section of the Unified CCXT API is under development.

Fees are often grouped into two categories:

Because the fee structure can depend on the actual volume of currencies traded by the user, the fees can be account-specific. Methods to work with account-specific fees:

The fee methods will return a unified fee structure, which is often present with orders and trades as well. The fee structure is a common format for representing the fee info throughout the library. Fee structures are usually indexed by market or currency.

Because this is still a work in progress, some or all of methods and info described in this section may be missing with this or that exchange.

DO NOT use the .fees property of the exchange instance as most often it contains the predefined/hardcoded info. Actual fees should only be accessed from markets and currencies.

NOTE: Previously we used fetchTransactionFee(s) to fetch the transaction fees, which are now DEPRECATED and these functions have been replace by fetchDepositWithdrawFee(s)

You call fetchTradingFee / fetchTradingFees to fetch the trading fees, fetchDepositWithdrawFee / fetchDepositWithdrawFees to fetch the deposit & withdraw fees.

Orders, private trades, transactions and ledger entries may define the following info in their fee field:

Trading fees are properties of markets. Most often trading fees are loaded into the markets by the fetchMarkets call. Sometimes, however, the exchanges serve fees from different endpoints.

The calculateFee method can be used to precalculate trading fees that will be paid (use calculateFeeWithRate if you have a custom trading fee / tier, like VIP-X, instead of the default user fee) . WARNING! This method is experimental, unstable and may produce incorrect results in certain cases. You should only use it with caution. Actual fees may be different from the values returned from calculateFee, this is just for precalculation. Do not rely on precalculated values, because market conditions change frequently. It is difficult to know in advance whether your order will be a market taker or maker.

The calculateFee method will return a unified fee structure with precalculated fees for an order with specified params.

Accessing trading fee rates should be done via fetchTradingFees which is the recommended approach. If that method is not supported by exchange, then via the .markets property, like so:

The markets stored under the .markets property may contain additional fee related information:

WARNING! fee related information is experimental, unstable and may only be partial available or not at all.

Maker fees are paid when you provide liquidity to the exchange i.e. you market-make an order and someone else fills it. Maker fees are usually lower than taker fees. Similarly, taker fees are paid when you take liquidity from the exchange and fill someone else's order.

Fees can be negative, this is very common amongst derivative exchanges. A negative fee means the exchange will pay a rebate (reward) to the user for the trading.

Also, some exchanges might not specify fees as percentage of volume, check the percentage field of the market to be sure.

Some exchanges have an endpoint for fetching the trading fee schedule, this is mapped to the unified methods fetchTradingFees, and fetchTradingFee

Transaction fees are properties of currencies (account balance).

Accessing transaction fee rates should be done via the .currencies property. This aspect is not unified yet and is subject to change.

Some exchanges have an endpoint for fetching the transaction fee schedule, this is mapped to the unified methods

To trade with leverage in spot or margin markets, currency must be borrowed as a loan. This borrowed currency must be payed back with interest. To obtain the amount of interest that has accrued you can use the fetchBorrowInterest method

To borrow and repay currency as a margin loan use borrowCrossMargin, borrowIsolatedMargin, repayCrossMargin and repayIsolatedMargin.

margin and contract only

Note: through the manual we use term "collateral" which means current margin balance, but do not confuse it with "initial margin" or "maintenance margin":

For example, when you had opened an isolated position with 50$ initial margin and the position has unrealized profit of -15$, then your position's collateral will be 35$. However, if we take that Maintenance Margin requirement (to keep the position open) by exchange hints $25 for that position, then your collateral should not drop below it, otherwise the position will be liquidated.

To increase, reduce or set your margin balance (collateral) in an open leveraged position, use addMargin, reduceMargin and setMargin respectively. This is kind of like adjusting the amount of leverage you're using with a position that's already open.

Some scenarios to use these methods include

You can fetch the history of margin adjustments made using the methods above or automatically by the exchange using the following method

Updates the type of margin used to be either

Common reasons for why an exchange might have

Some exchange apis return an error response when a request is sent to set the margin mode to the mode that it is already set to (e.g. Sending a request to set the margin mode to cross for the market BTC/USDT:USDT when the account already has BTC/USDT:USDT set to use cross margin). CCXT doesn't see this as an error because the end result is what the user wanted, so the error is suppressed and the error result is returned as an object.

Some methods allow the usage of a marginMode parameter that can be set to either cross or isolated. This can be useful for specifying the marginMode directly within the methods params, for use with spot margin or contract markets. To specify a spot margin market, you need to use a unified spot symbol or set the market type to spot, while setting the marginMode parameter to cross or isolated.

Create a Spot Margin Order:

Use a unified spot symbol, while setting the marginMode parameter.

margin and contract only

The fetchMarginMode() method can be used to obtain the set margin mode for a market. The fetchMarginModes() method can be used to obtain the set margin mode for multiple markets at once.

You can access the set margin mode by using:

margin and contract only

margin and contract only

The fetchLeverage() method can be used to obtain the set leverage for a market. The fetchLeverages() method can be used to obtain the set leverage for multiple markets at once.

You can access the set leverage by using:

This can include futures with a set expiry date, perpetual swaps with funding payments, and inverse futures or swaps. Information about the positions can be served from different endpoints depending on the exchange. In the case that there are multiple endpoints serving different types of derivatives CCXT will default to just loading the "linear" (as oppose to the "inverse") contracts or the "swap" (as opposed to the "future") contracts.

To get information about positions currently held in contract markets, use

Positions allow you to borrow money from an exchange to go long or short on an market. Some exchanges require you to pay a funding fee to keep the position open.

When you go long on a position you are betting that the price will be higher in the future and that the price will never be less than the liquidationPrice.

As the price of the underlying index changes so does the unrealisedPnl and as a consequence the amount of collateral you have left in the position (since you can only close it at market price or worse). At some price you will have zero collateral left, this is called the "bust" or "zero" price. Beyond this point, if the price goes in the opposite direction far enough, the collateral of the position will drop below the maintenanceMargin. The maintenanceMargin acts as a safety buffer between your position and negative collateral, a scenario where the exchange incurs losses on your behalf. To protect itself the exchange will swiftly liquidate your position if and when this happens. Even if the price returns back above the liquidationPrice you will not get your money back since the exchange sold all the contracts you bought at market. In other words the maintenanceMargin is a hidden fee to borrow money.

It is recommended to use the maintenanceMargin and initialMargin instead of the maintenanceMarginPercentage and initialMarginPercentage since these tend to be more accurate. The maintenanceMargin might be calculated from other factors outside of the maintenanceMarginPercentage including the funding rate and taker fees, for example on kucoin.

An inverse contract will allow you to go long or short on BTC/USD by putting up BTC as collateral. Our API for inverse contracts is the same as for linear contracts. The amounts in an inverse contracts are quoted as if they were traded USD/BTC, however the price is still quoted terms of BTC/USD. The formula for the profit and loss of a inverse contract is (1/markPrice - 1/price) * contracts. The profit and loss and collateral will now be quoted in BTC, and the number of contracts are quoted in USD.

To quickly close open positions with a market order, use

margin and contract only

Method used for setting position mode:

Method used for fetching position mode:

It is the price at which the initialMargin + unrealized = collateral = maintenanceMargin. The price has gone in the opposite direction of your position to the point where the is only maintenanceMargin collateral left and if it goes any further the position will have negative collateral.

Perpetual swap (also known as perpetual future) contracts maintain a market price that mirrors the price of the asset they are based on because funding fees are exchanged between traders who hold positions in perpetual swap markets.

If the contract is being traded at a price that is higher than the price of the asset they represent, then traders in long positions pay a funding fee to traders in short positions at specific times of day, which encourages more traders to enter short positions prior to these times.

If the contract is being traded at a price that is lower than the price of the asset they represent, then traders in short positions pay a funding fee to traders in long positions at specific times of day, which encourages more traders to enter long positions prior to these times.

These fees are usually exchanged between traders with no commission going to the exchange

The fetchFundingHistory method can be used to retrieve an accounts history of funding fees paid or received

The fetchConvertQuote method can be used to retrieve a quote that can be used for a conversion trade. The quote usually needs to be used within a certain timeframe specified by the exchange for the convert trade to execute successfully.

The createConvertTrade method can be used to create a conversion trade order using the id retrieved from fetchConvertQuote. The quote usually needs to be used within a certain timeframe specified by the exchange for the convert trade to execute successfully.

The fetchConvertTrade method can be used to fetch a specific conversion trade using the trades id.

The fetchConvertTradeHistory method can be used to fetch the conversion history for a specified currency code.

In some specific cases you may want a proxy, when:

However, beware that each added intermediary might add some latency to requests.

Note for Go users: After setting any proxy property, you must call UpdateProxySettings() to apply the changes:

However be aware that each added intermediary might add some latency to requests.

CCXT supports the following proxy types (note, each of them also have callback support):

This property prepends an url to API requests. It might be useful for simple redirection or bypassing CORS browser restriction.

while 'YOUR_PROXY_URL' could be like (use the slash accordingly):

So requests will be made to i.e. https://cors-anywhere.herokuapp.com/https://exchange.xyz/api/endpoint. ( You can also have a small proxy script running on your device/webserver to use it in .proxyUrl - "sample-local-proxy-server" in examples folder). To customize the target url, you can also override urlEncoderForProxyUrl method of instance.

This approach works only for REST requests, but not for websocket connections. ((How to test if your proxy works))[#test-if-your-proxy-works]

To set a real http(s) proxy for your scripts, you need to have an access to a remote http or https proxy, so calls will be made directly to the target exchange, tunneled through your proxy server:

This approach only affects non-websocket requests of ccxt. To route CCXT's WebSockets connections through proxy, you need to specifically set wsProxy (or wssProxy) property, in addition to the httpProxy (or httpsProxy), so your script should be like:

So, both connections (HTTP & WS) would go through proxies. ((How to test if your proxy works))[#test-if-your-proxy-works]

You can also use socks proxy with the following format:

((How to test if your proxy works))[#test-if-your-proxy-works]

After setting any of the above listed proxy properties in your ccxt snippet, you can test whether it works by pinging some IP echoing websites - check a "proxy-usage" file in examples.

**Instead of setting a property, you can also use callbacks proxyUrlCallback, http(s)ProxyCallback, socksProxyCallback:

If you need for special cases, you can override userAgent property like:

Depending your programming language, you can set custom proxy agents.

CORS (known as Cross-Origin Resource Sharing) affects mostly browsers and is the cause of the well-know warning No 'Access-Control-Allow-Origin' header is present on the requested resource. It happens when a script (running in a browser) makes a request to a 3rd party domain (by default such requests are blocked, unless the target domain explicitly allows it). So, in such cases you will need to communicate with a "CORS" proxy, which would redirect requests (as opposed to direct browser-side request) to the target exchange. To set a CORS proxy, you can run sample-local-proxy-server-with-cors example file and in ccxt set the .proxyUrl property to route requests through cors/proxy server.

Some users might want to control how CCXT handles arithmetic operations. Even though it uses numeric types by default, users can switch to fixed-point math using string types. This can be done by:

The error handling with CCXT is done with the exception mechanism that is natively available with all languages.

To handle the errors you should add a try block around the call to a unified method and catch the exceptions like you would normally do with your language:

When dealing with HTTP requests, it's important to understand that requests might fail for various reasons. Common causes of these failures include the server being unavailable, network instability, or temporary server issues. To handle such scenarios gracefully, CCXT provide an option to automatically retry failed requests. You can set the value of maxRetriesOnFailure and maxRetriesOnFailureDelay to configure the number of retries and the delay between retries, example:

It's important to highlight that only server/network-related issues will be part of the retry mechanism; if the user gets an error due to InsufficientFunds or InvalidOrder, the request will not be repeated.

All exceptions are derived from the base BaseError exception, which, in its turn, is defined in the ccxt library like so:

The exception inheritance hierarchy lives in this file: https://github.com/ccxt/ccxt/blob/master/ts/src/base/errorHierarchy.ts , and visually can be outlined like shown below:

The BaseError class is a generic root error class for all sorts of errors, including accessibility and request/response mismatch. If you don't need to catch any specific subclass of exceptions, you can just use BaseError, where all exception types are being caught.

From BaseError derives two different families of errors: OperationFailed and ExchangeError (they also have their specific sub-types, as explained below).

An OperationFailed might happen when user sends correctly constructed & valid request to exchange, but a non-deterministic problem occurred:

Such exceptions are temporary and re-trying the request again might be enough. However, if the error still happens, then it may indicate some persistent problem with the exchange or with your connection.

OperationFailed has the following sub-types: RequestTimeout,DDoSProtection (includes sub-type RateLimitExceeded), ExchangeNotAvailable, InvalidNonce.

This exception is thrown in cases when cloud/hosting services (Cloudflare, Incapsula or etc..) limits requests from user/region/location or when the exchange API restricts user because of making abnormal requests. This exception also contains specific sub-type exception RateLimitExceeded, which directly means that user makes much frequent requests than tolerated by exchange API engine.

This exception is raised when the connection with the exchange fails or data is not fully received in a specified amount of time. This is controlled by the exchange's .timeout property. When a RequestTimeout is raised, the user doesn't know the outcome of a request (whether it was accepted by the exchange server or not).

Thus it's advised to handle this type of exception in the following manner:

This type of exception is thrown when the underlying exchange is unreachable. The ccxt library also throws this error if it detects any of the following keywords in response:

Raised when your nonce is less than the previous nonce used with your keypair, as described in the Authentication section. This type of exception is thrown in these cases (in order of precedence for checking):

In contrast to OperationFailed, the ExchangeError is mostly happening when the request is impossible to succeed (because of factors listed below), so even if you retry the same request hundreds of times, they will still fail, because the request is being made incorrectly.

Possible reasons for this exception:

ExchangeError has the following sub-type exceptions:

Users may occasionally encounter errors such as:

"Timestamp for this request is outside of the recvWindow." "Invalid request, please check your server timestamp or recv_window param." "Timestamp for this request was 1000ms ahead of the server's time."

These issues can arise for several reasons:

Your device’s system clock may not be properly synchronized with global time standards, leading to timestamp discrepancies. To resolve this, ensure your system clock is accurate to the millisecond. This should not be a one-time adjustment — configure your operating system to synchronize time periodically (e.g., every hour) to maintain accuracy.

If your device’s clock is correctly synchronized but network delays cause requests to take longer than the exchange’s accepted window (commonly around 5 seconds, though this varies by exchange), your request may be rejected.

If the issue persists, you can compare your local timestamp with the exchange’s server time to diagnose discrepancies:

If you continue to experience timestamp errors after verifying synchronization, you can modify certain exchange options to help mitigate the issue.

A) exchange.options['adjustForTimeDifference'] = True or increase window to eg. 10 seconds (only if an exchange supports it, search this keyword in target exchange file): B) exchange.options['recvWindow'] = 10000

For additional troubleshooting steps, community discussions, and related timestamp/recvWindow issues, refer to the following GitHub threads:

In case you experience any difficulty connecting to a particular exchange, do the following in order of precedence:

(If the page is not being rendered for you, you can refer to the mirror at https://docs.ccxt.com/)

**Examples:**

Example 1 (unknown):
```unknown
User
    +-------------------------------------------------------------+
    |                            CCXT                             |
    +------------------------------+------------------------------+
    |            Public            |           Private            |
    +=============================================================+
    │                              .                              |
    │                    The Unified CCXT API                     |
    │                              .                              |
    |       loadMarkets            .           fetchBalance       |
    |       fetchMarkets           .            createOrder       |
    |       fetchCurrencies        .            cancelOrder       |
    |       fetchTicker            .             fetchOrder       |
    |       fetchTickers           .            fetchOrders       |
    |       fetchOrderBook         .        fetchOpenOrders       |
    |       fetchOHLCV             .      fetchClosedOrders       |
    |       fetchStatus            .          fetchMyTrades       |
    |       fetchTrades            .                deposit       |
    |                              .               withdraw       |
    │                              .                              |
    +=============================================================+
    │                              .                              |
    |                     Custom Exchange API                     |
    |         (Derived Classes And Their Implicit Methods)        |
    │                              .                              |
    |       publicGet...           .          privateGet...       |
    |       publicPost...          .         privatePost...       |
    |                              .          privatePut...       |
    |                              .       privateDelete...       |
    |                              .                   sign       |
    │                              .                              |
    +=============================================================+
    │                              .                              |
    |                      Base Exchange Class                    |
    │                              .                              |
    +=============================================================+
```

Example 2 (unknown):
```unknown
ex = ccxt.binance({'options': {'maxRequestsQueue': 9999}})
```

Example 3 (unknown):
```unknown
market['limits']['amount']['min'] == 0.05 &&
market['precision']['amount'] == 0.0001 &&
market['precision']['price'] == 0.01
```

Example 4 (unknown):
```unknown
'commonCurrencies' : {
    'XBT': 'BTC',
    'OPTIMISM': 'OP',
    // ... etc
}
```

---
