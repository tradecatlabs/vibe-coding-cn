# Polymarket - Getting Started

**Pages:** 8

---

## CLOB Introduction

**URL:** llms-txt#clob-introduction

**Contents:**
- System
- API
- Security
- Fees
  - Schedule
  - Overview
- Additional Resources

Source: https://docs.polymarket.com/developers/CLOB/introduction

Welcome to the Polymarket Order Book API! This documentation provides overviews, explanations, examples, and annotations to simplify interaction with the order book. The following sections detail the Polymarket Order Book and the API usage.

Polymarket's Order Book, or CLOB (Central Limit Order Book), is hybrid-decentralized. It includes an operator for off-chain matching/ordering, with settlement executed on-chain, non-custodially, via signed order messages.

The exchange uses a custom Exchange contract facilitating atomic swaps between binary Outcome Tokens (CTF ERC1155 assets and ERC20 PToken assets) and collateral assets (ERC20), following signed limit orders. Designed for binary markets, the contract enables complementary tokens to match across a unified order book.

Orders are EIP712-signed structured data. Matched orders have one maker and one or more takers, with price improvements benefiting the taker. The operator handles off-chain order management and submits matched trades to the blockchain for on-chain execution.

The Polymarket Order Book API enables market makers and traders to programmatically manage market orders. Orders of any amount can be created, listed, fetched, or read from the market order books. Data includes all available markets, market prices, and order history via REST and WebSocket endpoints.

Polymarket's Exchange contract has been audited by Chainsecurity ([View Audit](https://github.com/Polymarket/ctf-exchange/blob/main/audit/ChainSecurity_Polymarket_Exchange_audit.pdf)).

The operator's privileges are limited to order matching, non-censorship, and ensuring correct ordering. Operators can't set prices or execute unauthorized trades. Users can cancel orders on-chain independently if trust issues arise.

| Volume Level | Maker Fee Base Rate (bps) | Taker Fee Base Rate (bps) |
| ------------ | ------------------------- | ------------------------- |
| >0 USDC      | 0                         | 0                         |

Fees apply symmetrically in output assets (proceeds). This symmetry ensures fairness and market integrity. Fees are calculated differently depending on whether you are buying or selling:

* **Selling outcome tokens (base) for collateral (quote):**

$$
feeQuote = baseRate \times \min(price, 1 - price) \times size
$$

* **Buying outcome tokens (base) with collateral (quote):**

$$
feeBase = baseRate \times \min(price, 1 - price) \times \frac{size}{price}
$$

## Additional Resources

* [Exchange contract source code](https://github.com/Polymarket/ctf-exchange/tree/main/src)
* [Exchange contract documentation](https://github.com/Polymarket/ctf-exchange/blob/main/docs/Overview.md)

---

## API Rate Limits

**URL:** llms-txt#api-rate-limits

**Contents:**
- How Rate Limiting Works
- General Rate Limits
- Data API Rate Limits
- GAMMA API Rate Limits
- CLOB API Rate Limits
  - General CLOB Endpoints
  - CLOB Market Data
  - CLOB Ledger Endpoints
  - CLOB Markets & Pricing
  - CLOB Authentication

Source: https://docs.polymarket.com/quickstart/introduction/rate-limits

## How Rate Limiting Works

All rate limits are enforced using Cloudflare's throttling system. When you exceed the maximum configured rate for any endpoint, requests are throttled rather than immediately rejected. This means:

* **Throttling**: Requests over the limit are delayed/queued rather than dropped
* **Burst Allowances**: Some endpoints allow short bursts above the sustained rate
* **Time Windows**: Limits reset based on sliding time windows (e.g., per 10 seconds, per minute)

## General Rate Limits

| Endpoint              | Limit               | Notes                                              |
| --------------------- | ------------------- | -------------------------------------------------- |
| General Rate Limiting | 5000 requests / 10s | Throttle requests over the maximum configured rate |
| "OK" Endpoint         | 50 requests / 10s   | Throttle requests over the maximum configured rate |

## Data API Rate Limits

| Endpoint               | Limit                    | Notes                                              |
| ---------------------- | ------------------------ | -------------------------------------------------- |
| Data API (General)     | 200 requests / 10s       | Throttle requests over the maximum configured rate |
| Data API (Alternative) | 1200 requests / 1 minute | 10 minutes block on violation                      |
| Data API `/trades`     | 75 requests / 10s        | Throttle requests over the maximum configured rate |
| Data API "OK" Endpoint | 10 requests / 10s        | Throttle requests over the maximum configured rate |

## GAMMA API Rate Limits

| Endpoint                         | Limit              | Notes                                              |
| -------------------------------- | ------------------ | -------------------------------------------------- |
| GAMMA (General)                  | 750 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA Get Comments               | 100 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA `/events`                  | 100 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA `/markets`                 | 125 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA `/markets` /events listing | 100 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA Tags                       | 100 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA Search                     | 300 requests / 10s | Throttle requests over the maximum configured rate |

## CLOB API Rate Limits

### General CLOB Endpoints

| Endpoint                      | Limit               | Notes                                              |
| ----------------------------- | ------------------- | -------------------------------------------------- |
| CLOB (General)                | 5000 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB GET Balance Allowance    | 125 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB UPDATE Balance Allowance | 20 requests / 10s   | Throttle requests over the maximum configured rate |

| Endpoint          | Limit              | Notes                                              |
| ----------------- | ------------------ | -------------------------------------------------- |
| CLOB `/book`      | 200 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/books`     | 80 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB `/price`     | 200 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/prices`    | 80 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB `/midprice`  | 200 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/midprices` | 80 requests / 10s  | Throttle requests over the maximum configured rate |

### CLOB Ledger Endpoints

| Endpoint                                                    | Limit              | Notes                                              |
| ----------------------------------------------------------- | ------------------ | -------------------------------------------------- |
| CLOB Ledger (`/trades` `/orders` `/notifications` `/order`) | 300 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Ledger `/data/orders`                                  | 150 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Ledger `/data/trades`                                  | 150 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/notifications`                                       | 125 requests / 10s | Throttle requests over the maximum configured rate |

### CLOB Markets & Pricing

| Endpoint                | Limit              | Notes                                              |
| ----------------------- | ------------------ | -------------------------------------------------- |
| CLOB Price History      | 100 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Markets            | 250 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Market Tick Size   | 50 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB `markets/0x`       | 50 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB `/markets` listing | 100 requests / 10s | Throttle requests over the maximum configured rate |

### CLOB Authentication

| Endpoint      | Limit             | Notes                                              |
| ------------- | ----------------- | -------------------------------------------------- |
| CLOB API Keys | 50 requests / 10s | Throttle requests over the maximum configured rate |

### CLOB Trading Endpoints

| Endpoint                            | Limit                              | Notes                                                      |
| ----------------------------------- | ---------------------------------- | ---------------------------------------------------------- |
| CLOB POST `/order`                  | 2400 requests / 10s (240/s)        | BURST - Throttle requests over the maximum configured rate |
| CLOB POST `/order`                  | 24000 requests / 10 minutes (40/s) | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/order`                | 2400 requests / 10s (240/s)        | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/order`                | 24000 requests / 10 minutes (40/s) | Throttle requests over the maximum configured rate         |
| CLOB POST `/orders`                 | 800 requests / 10s (80/s)          | BURST - Throttle requests over the maximum configured rate |
| CLOB POST `/orders`                 | 12000 requests / 10 minutes (20/s) | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/orders`               | 800 requests / 10s (80/s)          | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/orders`               | 12000 requests / 10 minutes (20/s) | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/cancel-all`           | 200 requests / 10s (20/s)          | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-all`           | 3000 requests / 10 minutes (5/s)   | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/cancel-market-orders` | 800 requests / 10s (80/s)          | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-market-orders` | 12000 requests / 10 minutes (20/s) | Throttle requests over the maximum configured rate         |

## Other API Rate Limits

| Endpoint          | Limit                  | Notes                                              |
| ----------------- | ---------------------- | -------------------------------------------------- |
| RELAYER `/submit` | 15 requests / 1 minute | Throttle requests over the maximum configured rate |
| User PNL API      | 100 requests / 10s     | Throttle requests over the maximum configured rate |

---

## Glossary

**URL:** llms-txt#glossary

Source: https://docs.polymarket.com/quickstart/introduction/definitions

| Term                         | Definition                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Token**                    | A token represents a stake in a specific Yes/No outcome in a Market. The price of a token can fluctuate between $0 - $1 based on the market belief in the outcome. When a market resolves, the token associated with the correct prediction can be redeemed for \$1 USDC. This is also sometimes called an *Asset Id*                                             |
| **Market**                   | A single event outcome. Corresponds to a pair of CLOB token IDs(Yes/No), a market address, a question ID and a condition ID.                                                                                                                                                                                                                                      |
| **Event**                    | A collection of related markets grouped under a common topic or theme.                                                                                                                                                                                                                                                                                            |
| **SLUG**                     | A human readable identification for a market or event. Can be found in the URL of any Polymarket Market or Event. You can use this slug to find more detailed information about a market or event by using it as a parameter in the [Get Events](/developers/gamma-markets-api/get-events) or [Get Markets](/developers/gamma-markets-api/get-markets) endpoints. |
| **Negative Risk (negrisk)**  | A group of Markets(Event) in which only one Market can resolve as yes. For more detail see [Negrisk Details](https://docs.polymarket.com/developers/neg-risk/overview)                                                                                                                                                                                            |
| **Central Limit Order Book** | The off-chain order matching system. This is where you place resting orders and market orders are matched with existing orders before being sent on-chain.                                                                                                                                                                                                        |
| **Polygon Network**          | A scalable, multi-chain blockchain platform used by Polymarket to facilitate on-chain activities(contract creation, token transfers, etc)                                                                                                                                                                                                                         |

---

## WSS Quickstart

**URL:** llms-txt#wss-quickstart

**Contents:**
- Getting your API Keys
- Using those keys to connect to the Market or User Websocket

Source: https://docs.polymarket.com/quickstart/websocket/WSS-Quickstart

The following code samples and explanation will show you how to subsribe to the Marker and User channels of the Websocket.
You'll need your API keys to do this so we'll start with that.

## Getting your API Keys

## Using those keys to connect to the Market or User Websocket

<CodeGroup>
  
</CodeGroup>

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
</CodeGroup>

## Using those keys to connect to the Market or User Websocket

<CodeGroup>
```

---

## Does Polymarket have an API?

**URL:** llms-txt#does-polymarket-have-an-api?

Source: https://docs.polymarket.com/polymarket-learn/FAQ/does-polymarket-have-an-api

Getting data from Polymarket

Yes! Developers can find all the information they need for interacting with Polymarket. This includes [documentation on market discovery, resolution, trading etc.](/quickstart/introduction/main)

Whether you are an academic researcher a market maker or an indepedent developer, this documentation should provide you what you need to get started. All the code you find linked here and on our [GitHub](https://github.com/polymarket) is open source and free to use.

<Tip>
  If you have any questions please join our [Discord](https://discord.com/invite/polymarket) and direct your questions to the #devs channel.
</Tip>

---

## Developer Quickstart

**URL:** llms-txt#developer-quickstart

Source: https://docs.polymarket.com/quickstart/introduction/main

This section of the documentation will provide all the essential resources to help you perform basic trading actions on the Polymarket platform. If you're just getting started, you're in the right place.

Everything you need to start building with the Polymarket API is right here. Let’s get started.

[Not sure what to build next? Get inspired by checking out real examples from other developers using the API.](/quickstart/introduction/showcase)

---

## What is a Prediction Market?

**URL:** llms-txt#what-is-a-prediction-market?

**Contents:**
  - How it works
  - Making predictions
  - Free-market trading
  - Trust the markets

Source: https://docs.polymarket.com/polymarket-learn/FAQ/what-are-prediction-markets

How people collectively forecast the future.

A prediction market is a platform where people can bet on the outcome of future events. By buying and selling shares in the outcomes, participants collectively forecast the likelihood of events such as sports results, political elections, or entertainment awards.

Market Prices = Probabilities: The price of shares in a prediction market represents the current probability of an event happening. For example, if shares of an event are trading at 20 cents, it indicates a 20% chance of that event occurring.

### Making predictions

If you believe the actual probability of an event is higher than the market price suggests, you can buy shares. For instance, if you think a team has a better than 20% chance of winning, you would buy shares at 20 cents. If the event occurs, each share becomes worth \$1, yielding a profit.

### Free-market trading

You can buy or sell shares at any time before the event concludes, based on new information or changing circumstances. This flexibility allows the market prices to continuously reflect the most current and accurate probabilities.

### Trust the markets

Prediction markets provide unbiased and accurate probabilities in real time, cutting through the noise of human and media biases. Traditional sources often have their own incentives and slants, but prediction markets operate on the principle of "put your money where your mouth is." Here, participants are financially motivated to provide truthful insights, as their profits depend on the accuracy of their predictions.

In a prediction market, prices reflect the aggregated sentiment of all participants, weighing news, data, expert opinions, and culture to determine the true odds. Unlike media narratives, which can be swayed by various biases, prediction markets offer a transparent view of where people genuinely believe we're heading.

#### Why use prediction markets?

Prediction markets are often more accurate than traditional polls and expert predictions. The collective wisdom of diverse participants, each motivated by the potential for profit, leads to highly reliable forecasts. This makes prediction markets an excellent tool for gauging real-time probabilities of future events.

Polymarket, the world's largest prediction market, offers a user-friendly platform to bet on a wide range of topics, from sports to politics. By participating, you can profit from your knowledge while contributing to the accuracy of market predictions.

---

## What is Polymarket?

**URL:** llms-txt#what-is-polymarket?

**Contents:**
- Quick Overview
  - Understanding Prices
  - Making money on markets
  - How accurate are Polymarket odds?

Source: https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket

Polymarket is the world’s largest prediction market, allowing you to stay informed and profit from your knowledge by betting on future events across various topics.

Studies show prediction markets are often more accurate than pundits because they combine news, polls, and expert opinions into a single value that represents the market's view of an event's odds. Our markets reflect *accurate, unbiased, and real-time probabilities* for the events that matter most to you. Markets seek truth.

* On Polymarket, you can [buy and sell shares](making-your-first-trade) representing future event outcomes (i.e. "Will TikTok be banned in the U.S. this year?")

* Shares in event outcomes are [always priced](what-is-polymarket/#understanding-prices) between 0.00 and 1.00 [USDC](../FAQ/why-do-i-need-crypto/#why-usdc), and every pair of event outcomes (i.e. each pair of "YES" + "NO" shares) is fully collateralized by \$1.00 USDC.

* Shares are created when [opposing sides come to an agreement on odds](../trading/limit-orders), such that the sum of what each side is willing to pay is equal to \$1.00.

* The shares representing the *correct, final outcome* are paid out \$1.00 USDC each upon [market resolution](../markets/how-are-markets-resolved).

* Unlike sportsbooks, you are not betting against "the house" – the counterparty to each trade is another Polymarket user. As such:

* Shares can be sold before the event outcome is known\_ (i.e. to lock in profits or cut losses)

* *There is no "house" to ban you for winning too much.*

### Understanding Prices

Prices = Probabilities.

<VideoPlayer src="https://www.youtube.com/embed/v0CvPEYBzTI?si=9cirMPQ72orQzLyS" />

*Prices (odds) on Polymarket represent the current probability of an event occurring.* For example, in a market predicting whether the Miami Heat will win the 2025 NBA Finals, if YES shares are trading at 18 cents, it indicates a 18% chance of Miami winning.

These odds are determined by what price other Polymarket users are currently willing to buy & sell those shares at. Just how stock exchanges don't "set" the prices of stocks, Polymarket does not set prices / odds - they're a function of supply & demand.

[Learn more >](/docs/guides/trading/how-are-prices-calculated)

### Making money on markets

In the example above, if you believe Miami's chances of winning are higher than 18%, you would buy “Yes” shares at 18 cents each. If Miami wins, each “Yes” share would be worth \$1, resulting in an 82-cent profit per share. Conversely, any trader who owned “No” shares would see their investment become worthless once the game is over.

Since it's a market, you're not locked into your trade. You can sell your shares at any time at the current market price. As the news changes, the supply and demand for shares fluctuates, causing the share price to reflect the new odds for the event.

### How accurate are Polymarket odds?

Research shows prediction markets are often more accurate than experts, polls, and pundits. Traders aggregate news, polls, and expert opinions, making informed trades. Their economic incentives ensure market prices adjust to reflect true odds as more knowledgeable participants join.

This makes prediction markets the best source of real-time event probabilities. People use Polymarket for the most accurate odds, gaining the ability to make informed decisions about the future.

If you're an expert on a certain topic, Polymarket is your opportunity to profit from trading based on your knowledge, while improving the market's accuracy.

---
