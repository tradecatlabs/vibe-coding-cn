# Get comments by comment id
Source: https://docs.polymarket.com/api-reference/comments/get-comments-by-comment-id

api-reference/gamma-openapi.json get /comments/{id}



# Get comments by user address
Source: https://docs.polymarket.com/api-reference/comments/get-comments-by-user-address

api-reference/gamma-openapi.json get /comments/user_address/{user_address}



# List comments
Source: https://docs.polymarket.com/api-reference/comments/list-comments

api-reference/gamma-openapi.json get /comments



# Get closed positions for a user
Source: https://docs.polymarket.com/api-reference/core/get-closed-positions-for-a-user

api-reference/data-api-openapi.yaml get /closed-positions
Fetches closed positions for a user(address)



# Get current positions for a user
Source: https://docs.polymarket.com/api-reference/core/get-current-positions-for-a-user

api-reference/data-api-openapi.yaml get /positions
Returns positions filtered by user and optional filters.



# Get top holders for markets
Source: https://docs.polymarket.com/api-reference/core/get-top-holders-for-markets

api-reference/data-api-openapi.yaml get /holders



# Get total value of a user's positions
Source: https://docs.polymarket.com/api-reference/core/get-total-value-of-a-users-positions

api-reference/data-api-openapi.yaml get /value



# Get trades for a user or markets
Source: https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets

api-reference/data-api-openapi.yaml get /trades



# Get user activity
Source: https://docs.polymarket.com/api-reference/core/get-user-activity

api-reference/data-api-openapi.yaml get /activity
Returns on-chain activity for a user.



# Get event by id
Source: https://docs.polymarket.com/api-reference/events/get-event-by-id

api-reference/gamma-openapi.json get /events/{id}



# Get event by slug
Source: https://docs.polymarket.com/api-reference/events/get-event-by-slug

api-reference/gamma-openapi.json get /events/slug/{slug}



# Get event tags
Source: https://docs.polymarket.com/api-reference/events/get-event-tags

api-reference/gamma-openapi.json get /events/{id}/tags



# List events
Source: https://docs.polymarket.com/api-reference/events/list-events

api-reference/gamma-openapi.json get /events



# Health check
Source: https://docs.polymarket.com/api-reference/health/health-check

api-reference/data-api-openapi.yaml get /



# Get market by id
Source: https://docs.polymarket.com/api-reference/markets/get-market-by-id

api-reference/gamma-openapi.json get /markets/{id}



# Get market by slug
Source: https://docs.polymarket.com/api-reference/markets/get-market-by-slug

api-reference/gamma-openapi.json get /markets/slug/{slug}



# Get market tags by id
Source: https://docs.polymarket.com/api-reference/markets/get-market-tags-by-id

api-reference/gamma-openapi.json get /markets/{id}/tags



# List markets
Source: https://docs.polymarket.com/api-reference/markets/list-markets

api-reference/gamma-openapi.json get /markets



# Get live volume for an event
Source: https://docs.polymarket.com/api-reference/misc/get-live-volume-for-an-event

api-reference/data-api-openapi.yaml get /live-volume



# Get open interest
Source: https://docs.polymarket.com/api-reference/misc/get-open-interest

api-reference/data-api-openapi.yaml get /oi



# Get total markets a user has traded
Source: https://docs.polymarket.com/api-reference/misc/get-total-markets-a-user-has-traded

api-reference/data-api-openapi.yaml get /traded



# Get multiple order books summaries by request
Source: https://docs.polymarket.com/api-reference/orderbook/get-multiple-order-books-summaries-by-request

api-reference/clob-subset-openapi.yaml post /books
Retrieves order book summaries for specified tokens via POST request



# Get order book summary
Source: https://docs.polymarket.com/api-reference/orderbook/get-order-book-summary

api-reference/clob-subset-openapi.yaml get /book
Retrieves the order book summary for a specific token



# Get market price
Source: https://docs.polymarket.com/api-reference/pricing/get-market-price

api-reference/clob-subset-openapi.yaml get /price
Retrieves the market price for a specific token and side



# Get midpoint price
Source: https://docs.polymarket.com/api-reference/pricing/get-midpoint-price

api-reference/clob-subset-openapi.yaml get /midpoint
Retrieves the midpoint price for a specific token



# Get multiple market prices
Source: https://docs.polymarket.com/api-reference/pricing/get-multiple-market-prices

api-reference/clob-subset-openapi.yaml get /prices
Retrieves market prices for multiple tokens and sides



# Get multiple market prices by request
Source: https://docs.polymarket.com/api-reference/pricing/get-multiple-market-prices-by-request

api-reference/clob-subset-openapi.yaml post /prices
Retrieves market prices for specified tokens and sides via POST request



# Get price history for a traded token
Source: https://docs.polymarket.com/api-reference/pricing/get-price-history-for-a-traded-token

api-reference/clob-subset-openapi.yaml get /prices-history
Fetches historical price data for a specified market token



# Search markets, events, and profiles
Source: https://docs.polymarket.com/api-reference/search/search-markets-events-and-profiles

api-reference/gamma-openapi.json get /public-search



# Get series by id
Source: https://docs.polymarket.com/api-reference/series/get-series-by-id

api-reference/gamma-openapi.json get /series/{id}



# List series
Source: https://docs.polymarket.com/api-reference/series/list-series

api-reference/gamma-openapi.json get /series



# Get sports metadata information
Source: https://docs.polymarket.com/api-reference/sports/get-sports-metadata-information

api-reference/gamma-openapi.json get /sports
Retrieves metadata for various sports including images, resolution sources, ordering preferences, tags, and series information. This endpoint provides comprehensive sport configuration data used throughout the platform.



# List teams
Source: https://docs.polymarket.com/api-reference/sports/list-teams

api-reference/gamma-openapi.json get /teams



# Get bid-ask spreads
Source: https://docs.polymarket.com/api-reference/spreads/get-bid-ask-spreads

api-reference/clob-subset-openapi.yaml post /spreads
Retrieves bid-ask spreads for multiple tokens



# Get related tags (relationships) by tag id
Source: https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-id

api-reference/gamma-openapi.json get /tags/{id}/related-tags



# Get related tags (relationships) by tag slug
Source: https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug

api-reference/gamma-openapi.json get /tags/slug/{slug}/related-tags



# Get tag by id
Source: https://docs.polymarket.com/api-reference/tags/get-tag-by-id

api-reference/gamma-openapi.json get /tags/{id}



# Get tag by slug
Source: https://docs.polymarket.com/api-reference/tags/get-tag-by-slug

api-reference/gamma-openapi.json get /tags/slug/{slug}



# Get tags related to a tag id
Source: https://docs.polymarket.com/api-reference/tags/get-tags-related-to-a-tag-id

api-reference/gamma-openapi.json get /tags/{id}/related-tags/tags



# Get tags related to a tag slug
Source: https://docs.polymarket.com/api-reference/tags/get-tags-related-to-a-tag-slug

api-reference/gamma-openapi.json get /tags/slug/{slug}/related-tags/tags



# List tags
Source: https://docs.polymarket.com/api-reference/tags/list-tags

api-reference/gamma-openapi.json get /tags



# Polymarket Changelog
Source: https://docs.polymarket.com/changelog/changelog

Welcome to the Polymarket Changelog. Here you will find any important changes to Polymarket, including but not limited to CLOB, API, UI and Mobile Applications.

<Update label="Sept 24, 2025" description="Polymarket Real-Time Data Socket (RTDS) official release">
  * **Crypto Price Feeds**: Access real-time cryptocurrency prices from two sources (Binance & Chainlink)
  * **Comment Streaming**: Real-time updates for comment events including new comments, replies, and reactions
  * **Dynamic Subscriptions**: Add, remove, and modify subscriptions without reconnecting
  * **TypeScript Client**: Official TypeScript client available at [real-time-data-client](https://github.com/Polymarket/real-time-data-client)
    For complete documentation, see [RTDS Overview](/developers/RTDS/RTDS-overview).
</Update>

<Update label="September 15, 2025" description="WSS price_change event update">
  * There has been a significant change to the structure of the price change message. This update will be applied at 11PM UTC September 15, 2025. We apologize for the short notice
    * Please see the [migration guide](/developers/CLOB/websocket/market-channel-migration-guide) for details.
</Update>

<Update label="August 26, 2025" description="Updated /trades and /activity endpoints">
  * Reduced maximum values for query parameters on Data-API /trades and /activity:
    * `limit`: 500
    * `offset`: 1,000
</Update>

<Update label="August 21, 2025" description="Batch Orders Increase">
  * The batch orders limit has been increased from from 5 -> 15. Read more about the batch orders functionality [here](/developers/CLOB/orders/create-order-batch).
</Update>

<Update label="July 23, 2025" description="Get Book(s) update">
  * We’re adding new fields to the `get-book` and `get-books` CLOB endpoints to include key market metadata that previously required separate queries.
    * `min_order_size`
      * type: string
      * description: Minimum allowed order size.
    * `neg_risk`
      * type: boolean
      * description: Boolean indicating whether the market is neg\_risk.
    * `tick_size`
      * type: string
      * description: Minimum allowed order size.
</Update>

<Update label="June 3, 2025" description="New Batch Orders Endpoint">
  * We’re excited to roll out a highly requested feature: **order batching**. With this new endpoint, users can now submit up to five trades in a single request. To help you get started, we’ve included sample code demonstrating how to use it. Please see [Place Multiple Orders (Batching)](/developers/CLOB/orders/create-order-batch) for more details.
</Update>

<Update label="June 3, 2025" description="Change to /data/trades">
  * We're adding a new `side` field to the `MakerOrder` portion of the trade object. This field will indicate whether the maker order is a `buy` or `sell`, helping to clarify trade events where the maker side was previously ambiguous. For more details, refer to the MakerOrder object on the [Get Trades](/developers/CLOB/trades/trades) page.
</Update>

<Update label="May 28, 2025" description="Websocket Changes">
  * The 100 token subscription limit has been removed for the Markets channel. You can now subscribe to as many token IDs as needed for your use case.
  * New Subscribe Field `initial_dump`
    * Optional field to indicate whether you want to receive the initial order book state when subscribing to a token or list of tokens.
    * `default: true`
</Update>

<Update label="May 28, 2025" description="New FAK Order Type">
  We’re excited to introduce a new order type soon to be available to all users: Fill and Kill (FAK). FAK orders behave similarly to the well-known Fill or Kil(FOK) orders, but with a key difference:

  * FAK will fill as many shares as possible immediately at your specified price, and any remaining unfilled portion will be canceled.
  * Unlike FOK, which requires the entire order to fill instantly or be canceled, FAK is more flexible and aims to capture partial fills if possible.
</Update>

<Update label="May 15, 2025" description="Increased API Rate Limits">
  All API users will enjoy increased rate limits for the CLOB endpoints.

  * CLOB - /books (website) (300req - 10s / Throttle requests over the maximum configured rate)
  * CLOB - /books (50 req - 10s / Throttle requests over the maximum configured rate)
  * CLOB - /price (100req - 10s / Throttle requests over the maximum configured rate)
  * CLOB markets/0x (50req / 10s - Throttle requests over the maximum configured rate)
  * CLOB POST /order - 500 every 10s (50/s) - (BURST) - Throttle requests over the maximum configured rateed
  * CLOB POST /order - 3000 every 10 minutes (5/s) - Throttle requests over the maximum configured rate
  * CLOB DELETE /order - 500 every 10s (50/s) - (BURST) - Throttle requests over the maximum configured rate
  * DELETE /order - 3000 every 10 minutes (5/s) - Throttle requests over the maximum configured rate
</Update>


# null
Source: https://docs.polymarket.com/developers/CLOB/authentication



There are two levels of authentication to be considered when using Polymarket’s CLOB.\
All signing can be handled directly by the client libraries.
<Tip>This is information for advanced users who are NOT using our [Python](https://github.com/Polymarket/py-clob-client) or [Typescript](https://github.com/Polymarket/clob-client) Clients. Our provided clients handle signing and authentication for you.</Tip>

## L1: Private Key Authentication

The highest level of authentication is via an account’s Polygon private key.\
The private key remains in control of a user’s funds and all trading is non-custodial.\
The operator **never** has control over users’ funds.

Private key authentication is required for:

* Placing an order (for signing the order)
* Creating or revoking API keys

### L1 Header

| Header           | Required? | Description            |
| ---------------- | --------- | ---------------------- |
| `POLY_ADDRESS`   | yes       | Polygon address        |
| `POLY_SIGNATURE` | yes       | CLOB EIP 712 signature |
| `POLY_TIMESTAMP` | yes       | Current UNIX timestamp |
| `POLY_NONCE`     | yes       | Nonce. Default 0       |

The `POLY_SIGNATURE` is generated by signing the following EIP-712 struct.

Implementations exist in:

* [Typescript](https://github.com/Polymarket/clob-client/blob/main/src/signing/eip712.ts)
* [Python](https://github.com/Polymarket/py-clob-client/blob/main/py_clob_client/signing/eip712.py)

### Signing Example

<CodeGroup>
  ```python Python theme={null}
  domain = {
      "name": "ClobAuthDomain",
      "version": "1",
      "chainId": chainId,  # Polygon Chain ID 137
  }

  types = {
      "ClobAuth": [
          {"name": "address", "type": "address"},
          {"name": "timestamp", "type": "string"},
          {"name": "nonce", "type": "uint256"},
          {"name": "message", "type": "string"},
      ]
  }

  value = {
      "address": signingAddress,  # The signing address
      "timestamp": ts,            # The CLOB API server timestamp
      "nonce": nonce,             # The nonce used
      "message": "This message attests that I control the given wallet",
  }

  sig = await signer._signTypedData(domain, types, value)
  ```

  ```typescript Typescript theme={null}
  const domain = {
      name: "ClobAuthDomain",
      version: "1",
      chainId: chainId, // Polygon Chain ID 137
  };

  const types = {
      ClobAuth: [
          { name: "address", type: "address" },
          { name: "timestamp", type: "string" },
          { name: "nonce", type: "uint256" },
          { name: "message", type: "string" },
      ],
  };

  const value = {
      address: signingAddress, // The Signing address
      timestamp: ts,            // The CLOB API server timestamp
      nonce: nonce,             // The nonce used
      message: "This message attests that I control the given wallet", // Static message
  };

  const sig = await signer._signTypedData(domain, types, value);
  ```
</CodeGroup>

***

## L2: API Key Authentication

The next level of authentication consists of the API key, secret, and passphrase.\
These are used solely to authenticate API requests made to Polymarket’s CLOB, such as posting/canceling orders or retrieving an account’s orders and fills.

When a user on-boards via:

```bash  theme={null}
POST /auth/api-key
```

the server uses the signature as a seed to deterministically generate credentials.\
An API credential includes:

* `key`: UUID identifying the credentials
* `secret`: Secret string used to generate HMACs (not sent with requests)
* `passphrase`: Secret string sent with each request, used to encrypt/decrypt the secret (never stored)

All private endpoints require an API key signature (`L2 Header`).

### L2 Header

| Header            | Required? | Description                   |
| ----------------- | --------- | ----------------------------- |
| `POLY_ADDRESS`    | yes       | Polygon address               |
| `POLY_SIGNATURE`  | yes       | HMAC signature for request    |
| `POLY_TIMESTAMP`  | yes       | Current UNIX timestamp        |
| `POLY_API_KEY`    | yes       | Polymarket API key            |
| `POLY_PASSPHRASE` | yes       | Polymarket API key passphrase |

***

# API Key Operations

## Create API Key

<Tip>This endpoint requires an **L1 Header**.</Tip>

Create new API key credentials for a user.

**HTTP Request:**

```bash  theme={null}
POST {clob-endpoint}/auth/api-key
```

***

## Derive API Key

<Tip>This endpoint requires an **L1 Header**. </Tip>

Derive an existing API key for an address and nonce.

**HTTP Request:**

```bash  theme={null}
GET {clob-endpoint}/auth/derive-api-key
```

***

## Get API Keys

<Tip>This endpoint requires an **L2 Header**. </Tip>

Retrieve all API keys associated with a Polygon address.

**HTTP Request:**

```bash  theme={null}
GET {clob-endpoint}/auth/api-keys
```

***

## Delete API Key

<Tip>This endpoint requires an **L2 Header**.</Tip>

Delete an API key used to authenticate a request.

**HTTP Request:**

```bash  theme={null}
DELETE {clob-endpoint}/auth/api-key
```

***

## Access Status

Check the value of `cert_required` by signer address.

**HTTP Request:**

```bash  theme={null}
GET {clob-endpoint}/auth/access-status
```

***

## Get Closed Only Mode Status

<Tip>This endpoint requires an **L2 Header**.</Tip>

Retrieve the closed-only mode flag status.

**HTTP Request:**

```bash  theme={null}
GET {clob-endpoint}/auth/ban-status/closed-only
```


# null
Source: https://docs.polymarket.com/developers/CLOB/clients



Polymarket has implemented reference clients that allow programmatic use of the API below:

* [clob-client](https://github.com/Polymarket/clob-client) (Typescript)
* [py-clob-client](https://github.com/Polymarket/py-clob-client) (Python)

<CodeGroup>
  ```python python_initialization theme={null}
  pip install py-clob-client

  from py_clob_client.client import ClobClient

  host: str = ""
  key: str = ""
  chain_id: int = 137

  ### Initialization of a client that trades directly from an EOA
  client = ClobClient(host, key=key, chain_id=chain_id)

  ### Initialization of a client using a Polymarket Proxy associated with an Email/Magic account
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

  ```

  ```javascript typescript_initialization theme={null}
  //npm install @polymarket/clob-client
  //npm install ethers
  //Client initialization example and dumping API Keys

  import { ApiKeyCreds, ClobClient} from "@polymarket/clob-client";
  import { Wallet } from "@ethersproject/wallet";

  const host = 'https://clob.polymarket.com';
  const funder = '';//This is your Polymarket Profile Address, where you send UDSC to. 
  const signer = new Wallet(""); //This is your Private Key. If using email login export from https://reveal.magic.link/polymarket otherwise export from your Web3 Application

  //In general don't create a new API key, always derive or createOrDerive
  const creds = new ClobClient(host, 137, signer).createOrDeriveApiKey();

  //0: EOA
  //1: Magic/Email Login
  //2: Metamask
  const signatureType = 1; 
    
  (async () => {
      const clobClient = new ClobClient(host, 137, signer, await creds, signatureType, funder);
  })


  ```
</CodeGroup>

***

## Order Utils

Polymarket has implemented utility libraries to programmatically sign and generate orders:

* [clob-order-utils](https://github.com/Polymarket/clob-order-utils) (Typescript)
* [python-order-utils](https://github.com/Polymarket/python-order-utils) (Python)
* [go-order-utils](https://github.com/Polymarket/go-order-utils) (Golang)


# null
Source: https://docs.polymarket.com/developers/CLOB/endpoints



### REST

Used for all CLOB REST endpoints, denoted `{clob-endpoint}`.

[https://clob.polymarket.com/](https://clob.polymarket.com/)

### Data-API

An additional endpoint that delivers user data, holdings, and other on-chain activities.
[https://data-api.polymarket.com/](https://data-api.polymarket.com/)

### WebSocket

Used for all CLOB WSS endpoints, denoted `{wss-channel}`.

[wss://ws-subscriptions-clob.polymarket.com/ws/](wss://ws-subscriptions-clob.polymarket.com/ws/)

### Real Time Data Socket (RTDS)

Used for real-time data streaming including crypto prices and comments, denoted `{rtds-endpoint}`.

[wss://ws-live-data.polymarket.com](wss://ws-live-data.polymarket.com)


# CLOB Introduction
Source: https://docs.polymarket.com/developers/CLOB/introduction



Welcome to the Polymarket Order Book API! This documentation provides overviews, explanations, examples, and annotations to simplify interaction with the order book. The following sections detail the Polymarket Order Book and the API usage.

## System

Polymarket's Order Book, or CLOB (Central Limit Order Book), is hybrid-decentralized. It includes an operator for off-chain matching/ordering, with settlement executed on-chain, non-custodially, via signed order messages.

The exchange uses a custom Exchange contract facilitating atomic swaps between binary Outcome Tokens (CTF ERC1155 assets and ERC20 PToken assets) and collateral assets (ERC20), following signed limit orders. Designed for binary markets, the contract enables complementary tokens to match across a unified order book.

Orders are EIP712-signed structured data. Matched orders have one maker and one or more takers, with price improvements benefiting the taker. The operator handles off-chain order management and submits matched trades to the blockchain for on-chain execution.

## API

The Polymarket Order Book API enables market makers and traders to programmatically manage market orders. Orders of any amount can be created, listed, fetched, or read from the market order books. Data includes all available markets, market prices, and order history via REST and WebSocket endpoints.

## Security

Polymarket's Exchange contract has been audited by Chainsecurity ([View Audit](https://github.com/Polymarket/ctf-exchange/blob/main/audit/ChainSecurity_Polymarket_Exchange_audit.pdf)).

The operator's privileges are limited to order matching, non-censorship, and ensuring correct ordering. Operators can't set prices or execute unauthorized trades. Users can cancel orders on-chain independently if trust issues arise.

## Fees

### Schedule

> Subject to change

| Volume Level | Maker Fee Base Rate (bps) | Taker Fee Base Rate (bps) |
| ------------ | ------------------------- | ------------------------- |
| >0 USDC      | 0                         | 0                         |

### Overview

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


# Cancel Orders(s)
Source: https://docs.polymarket.com/developers/CLOB/orders/cancel-orders

Multiple endpoints to cancel a single order, multiple orders, all orders or all orders from a single market.

# Cancel an single Order

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel an order.

**HTTP REQUEST**

`DELETE /<clob-endpoint>/order`

### Request Payload Parameters

| Name    | Required | Type   | Description           |
| ------- | -------- | ------ | --------------------- |
| orderID | yes      | string | ID of order to cancel |

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel(order_id="0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88")
  print(resp)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    // Send it to the server
    const resp = await clobClient.cancelOrder({
      orderID:
        "0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88",
    });
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</CodeGroup>

# Cancel Multiple Orders

<Tip> This endpoint requires a L2 Header. </Tip>

**HTTP REQUEST**

`DELETE /<clob-endpoint>/orders`

### Request Payload Parameters

| Name | Required | Type      | Description                 |
| ---- | -------- | --------- | --------------------------- |
| null | yes      | string\[] | IDs of the orders to cancel |

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel_orders(["0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88", "0xaaaa..."])
  print(resp)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    // Send it to the server
    const resp = await clobClient.cancelOrders([
      "0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88",
      "0xaaaa...",
    ]);
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</CodeGroup>

# Cancel ALL Orders

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel all open orders posted by a user.

**HTTP REQUEST**

`DELETE /<clob-endpoint>/cancel-all`

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel_all()
  print(resp)
  print("Done!")
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const resp = await clobClient.cancelAll();
    console.log(resp);
    console.log(`Done!`);
  }

  main();
  ```
</CodeGroup>

# Cancel orders from market

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel orders from market.

**HTTP REQUEST**

`DELETE /<clob-endpoint>/cancel-market-orders`

### Request Payload Parameters

| Name      | Required | Type   | Description                |
| --------- | -------- | ------ | -------------------------- |
| market    | no       | string | condition id of the market |
| asset\_id | no       | string | id of the asset/token      |

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel_market_orders(market="0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af", asset_id="52114319501245915516055106046884209969926127482827954674443846427813813222426")
  print(resp)

  ```

  ```javascript Typescript theme={null}
  async function main() {
    // Send it to the server
    const resp = await clobClient.cancelMarketOrders({
      market:
        "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
      asset_id:
        "52114319501245915516055106046884209969926127482827954674443846427813813222426",
    });
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</CodeGroup>


# Check Order Reward Scoring
Source: https://docs.polymarket.com/developers/CLOB/orders/check-scoring

Check if an order is eligble or scoring for Rewards purposes

<Tip> This endpoint requires a L2 Header. </Tip>

Returns a boolean value where it is indicated if an order is scoring or not.

**HTTP REQUEST**

`GET /<clob-endpoint>/order-scoring?order_id={...}`

### Request Parameters

| Name    | Required | Type   | Description                          |
| ------- | -------- | ------ | ------------------------------------ |
| orderId | yes      | string | id of order to get information about |

### Response Format

| Name | Type          | Description        |
| ---- | ------------- | ------------------ |
| null | OrdersScoring | order scoring data |

An `OrdersScoring` object is of the form:

| Name    | Type    | Description                              |
| ------- | ------- | ---------------------------------------- |
| scoring | boolean | indicates if the order is scoring or not |

# Check if some orders are scoring

> This endpoint requires a L2 Header.

Returns to a dictionary with boolean value where it is indicated if an order is scoring or not.

**HTTP REQUEST**

`POST /<clob-endpoint>/orders-scoring`

### Request Parameters

| Name     | Required | Type      | Description                                |
| -------- | -------- | --------- | ------------------------------------------ |
| orderIds | yes      | string\[] | ids of the orders to get information about |

### Response Format

| Name | Type          | Description         |
| ---- | ------------- | ------------------- |
| null | OrdersScoring | orders scoring data |

An `OrdersScoring` object is a dictionary that indicates the order by if it score.

<RequestExample>
  ```python Python theme={null}
  scoring = client.is_order_scoring(
      OrderScoringParams(
          orderId="0x..."
      )
  )
  print(scoring)

  scoring = client.are_orders_scoring(
      OrdersScoringParams(
          orderIds=["0x..."]
      )
  )
  print(scoring)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const scoring = await clobClient.isOrderScoring({
      orderId: "0x...",
    });
    console.log(scoring);
  }

  main();

  async function main() {
    const scoring = await clobClient.areOrdersScoring({
      orderIds: ["0x..."],
    });
    console.log(scoring);
  }

  main();

  ```
</RequestExample>


# Place Single Order
Source: https://docs.polymarket.com/developers/CLOB/orders/create-order

Detailed instructions for creating, placing, and managing orders using Polymarket's CLOB API.

# Create and Place an Order

<Tip> This endpoint requires a L2 Header </Tip>

Create and place an order using the Polymarket CLOB API clients. All orders are represented as "limit" orders, but "market" orders are also supported. To place a market order, simply ensure your price is marketable against current resting limit orders, which are executed on input at the best price.

**HTTP REQUEST**

`POST /<clob-endpoint>/order`

### Request Payload Parameters

| Name      | Required | Type   | Description                      |
| --------- | -------- | ------ | -------------------------------- |
| order     | yes      | Order  | signed object                    |
| owner     | yes      | string | api key of order owner           |
| orderType | yes      | string | order type ("FOK", "GTC", "GTD") |

An `order` object is the form:

| Name          | Required | Type    | Description                                        |
| ------------- | -------- | ------- | -------------------------------------------------- |
| salt          | yes      | integer | random salt used to create unique order            |
| maker         | yes      | string  | maker address (funder)                             |
| signer        | yes      | string  | signing address                                    |
| taker         | yes      | string  | taker address (operator)                           |
| tokenId       | yes      | string  | ERC1155 token ID of conditional token being traded |
| makerAmount   | yes      | string  | maximum amount maker is willing to spend           |
| takerAmount   | yes      | string  | minimum amount taker will pay the maker in return  |
| expiration    | yes      | string  | unix expiration timestamp                          |
| nonce         | yes      | string  | maker's exchange nonce of the order is associated  |
| feeRateBps    | yes      | string  | fee rate basis points as required by the operator  |
| side          | yes      | string  | buy or sell enum index                             |
| signatureType | yes      | integer | signature type enum index                          |
| signature     | yes      | string  | hex encoded signature                              |

### Order types

* **FOK**: A Fill-Or-Kill order is an market order to buy (in dollars) or sell (in shares) shares that must be executed immediately in its entirety; otherwise, the entire order will be cancelled.
* **FAK**: A Fill-And-Kill order is a market order to buy (in dollars) or sell (in shares) that will be executed immediately for as many shares as are available; any portion not filled at once is cancelled.
* **GTC**: A Good-Til-Cancelled order is a limit order that is active until it is fulfilled or cancelled.
* **GTD**: A Good-Til-Date order is a type of order that is active until its specified date (UTC seconds timestamp), unless it has already been fulfilled or cancelled. There is a security threshold of one minute. If the order needs to expire in 90 seconds the correct expiration value is: now + 1 minute + 30 seconds

### Response Format

| Name        | Type      | Description                                                                                                                        |
| ----------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| success     | boolean   | boolean indicating if server-side err (`success = false`) -> server-side error                                                     |
| errorMsg    | string    | error message in case of unsuccessful placement (in case `success = false`, e.g. `client-side error`, the reason is in `errorMsg`) |
| orderId     | string    | id of order                                                                                                                        |
| orderHashes | string\[] | hash of settlement transaction order was marketable and triggered a match                                                          |

### Insert Error Messages

If the `errorMsg` field of the response object from placement is not an empty string, the order was not able to be immediately placed. This might be because of a delay or because of a failure. If the `success` is not `true`, then there was an issue placing the order. The following `errorMessages` are possible:

#### Error

| Error                                | Success | Message                                                                                 | Description                                                           |
| ------------------------------------ | ------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| INVALID\_ORDER\_MIN\_TICK\_SIZE      | yes     | order is invalid. Price breaks minimum tick size rules                                  | order price isn't accurate to correct tick sizing                     |
| INVALID\_ORDER\_MIN\_SIZE            | yes     | order is invalid. Size lower than the minimum                                           | order size must meet min size threshold requirement                   |
| INVALID\_ORDER\_DUPLICATED           | yes     | order is invalid. Duplicated. Same order has already been placed, can't be placed again |                                                                       |
| INVALID\_ORDER\_NOT\_ENOUGH\_BALANCE | yes     | not enough balance / allowance                                                          | funder address doesn't have sufficient balance or allowance for order |
| INVALID\_ORDER\_EXPIRATION           | yes     | invalid expiration                                                                      | expiration field expresses a time before now                          |
| INVALID\_ORDER\_ERROR                | yes     | could not insert order                                                                  | system error while inserting order                                    |
| EXECUTION\_ERROR                     | yes     | could not run the execution                                                             | system error while attempting to execute trade                        |
| ORDER\_DELAYED                       | no      | order match delayed due to market conditions                                            | order placement delayed                                               |
| DELAYING\_ORDER\_ERROR               | yes     | error delaying the order                                                                | system error while delaying order                                     |
| FOK\_ORDER\_NOT\_FILLED\_ERROR       | yes     | order couldn't be fully filled, FOK orders are fully filled/killed                      | FOK order not fully filled so can't be placed                         |
| MARKET\_NOT\_READY                   | no      | the market is not yet ready to process new orders                                       | system not accepting orders for market yet                            |

### Insert Statuses

When placing an order, a status field is included. The status field provides additional information regarding the order's state as a result of the placement. Possible values include:

#### Status

| Status    | Description                                                  |
| --------- | ------------------------------------------------------------ |
| matched   | order placed and matched with an existing resting order      |
| live      | order placed and resting on the book                         |
| delayed   | order marketable, but subject to matching delay              |
| unmatched | order marketable, but failure delaying, placement successful |

<RequestExample>
  ```python Python theme={null}
  from py_clob_client.client import ClobClient
  from py_clob_client.clob_types import OrderArgs, OrderType
  from py_clob_client.order_builder.constants import BUY

  host: str = "https://clob.polymarket.com"
  key: str = "" #This is your Private Key. Export from reveal.polymarket.com or from your Web3 Application
  chain_id: int = 137 #No need to adjust this
  POLYMARKET_PROXY_ADDRESS: str = '' #This is the address you deposit/send USDC to to FUND your Polymarket account.

  #Select from the following 3 initialization options to matches your login method, and remove any unused lines so only one client is initialized.


  ### Initialization of a client using a Polymarket Proxy associated with an Email/Magic account. If you login with your email use this example.
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client that trades directly from an EOA. 
  client = ClobClient(host, key=key, chain_id=chain_id)

  ## Create and sign a limit order buying 100 YES tokens for 0.50c each
  #Refer to the Markets API documentation to locate a tokenID: https://docs.polymarket.com/developers/gamma-markets-api/get-markets

  client.set_api_creds(client.create_or_derive_api_creds()) 

  order_args = OrderArgs(
      price=0.01,
      size=5.0,
      side=BUY,
      token_id="", #Token ID you want to purchase goes here. 
  )
  signed_order = client.create_order(order_args)

  ## GTC(Good-Till-Cancelled) Order
  resp = client.post_order(signed_order, OrderType.GTC)
  print(resp)
  ```

  ```javascript typescript theme={null}
  // GTC Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a buy order for 100 YES for 0.50c
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563
    const order = await clobClient.createOrder({
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      price: 0.5,
      side: Side.BUY,
      size: 100,
      feeRateBps: 0,
      nonce: 1,
    });
    console.log("Created Order", order);

    // Send it to the server

    // GTC Order
    const resp = await clobClient.postOrder(order, OrderType.GTC);
    console.log(resp);
  }

  main();
  // GTD Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a buy order for 100 YES for 0.50c that expires in 1 minute
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563

    // There is a 1 minute of security threshold for the expiration field.
    // If we need the order to expire in 30 seconds the correct expiration value is:
    // now + 1 miute + 30 seconds
    const oneMinute = 60 * 1000;
    const seconds = 30 * 1000;
    const expiration = parseInt(
      ((new Date().getTime() + oneMinute + seconds) / 1000).toString()
    );

    const order = await clobClient.createOrder({
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      price: 0.5,
      side: Side.BUY,
      size: 100,
      feeRateBps: 0,
      nonce: 1,
      // There is a 1 minute of security threshold for the expiration field.
      // If we need the order to expire in 30 seconds the correct expiration value is:
      // now + 1 miute + 30 seconds
      expiration: expiration,
    });
    console.log("Created Order", order);

    // Send it to the server

    // GTD Order
    const resp = await clobClient.postOrder(order, OrderType.GTD);
    console.log(resp);
  }

  main();
  // FOK BUY Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a market buy order for $100
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563

    const marketOrder = await clobClient.createMarketOrder({
      side: Side.BUY,
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      amount: 100, // $$$
      feeRateBps: 0,
      nonce: 0,
      price: 0.5,
    });
    console.log("Created Order", order);

    // Send it to the server
    // FOK Order
    const resp = await clobClient.postOrder(order, OrderType.FOK);
    console.log(resp);
  }

  main();
  // FOK SELL Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a market sell order for 100 shares
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563

    const marketOrder = await clobClient.createMarketOrder({
      side: Side.SELL,
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      amount: 100, // shares
      feeRateBps: 0,
      nonce: 0,
      price: 0.5,
    });
    console.log("Created Order", order);

    // Send it to the server
    // FOK Order
    const resp = await clobClient.postOrder(order, OrderType.FOK);
    console.log(resp);
  }

  main();
  ```
</RequestExample>


# Place Multiple Orders (Batching)
Source: https://docs.polymarket.com/developers/CLOB/orders/create-order-batch

Instructions for placing multiple orders(Batch)

<Tip> This endpoint requires a L2 Header </Tip>

Polymarket’s CLOB supports batch orders, allowing you to place up to `15` orders in a single request. Before using this feature, make sure you're comfortable placing a single order first. You can find the documentation for that [here.](/developers/CLOB/orders/create-order)

**HTTP REQUEST**

`POST /<clob-endpoint>/orders`

### Request Payload Parameters

| Name      | Required | Type          | Description                                                      |
| --------- | -------- | ------------- | ---------------------------------------------------------------- |
| PostOrder | yes      | PostOrders\[] | list of signed order objects (Signed Order + Order Type + Owner) |

A `PostOrder` object is the form:

| Name      | Required | Type   | Description                                         |
| --------- | -------- | ------ | --------------------------------------------------- |
| order     | yes      | order  | See below table for details on crafting this object |
| orderType | yes      | string | order type ("FOK", "GTC", "GTD", "FAK")             |
| owner     | yes      | string | api key of order owner                              |

An `order` object is the form:

| Name          | Required | Type    | Description                                        |
| ------------- | -------- | ------- | -------------------------------------------------- |
| salt          | yes      | integer | random salt used to create unique order            |
| maker         | yes      | string  | maker address (funder)                             |
| signer        | yes      | string  | signing address                                    |
| taker         | yes      | string  | taker address (operator)                           |
| tokenId       | yes      | string  | ERC1155 token ID of conditional token being traded |
| makerAmount   | yes      | string  | maximum amount maker is willing to spend           |
| takerAmount   | yes      | string  | minimum amount taker will pay the maker in return  |
| expiration    | yes      | string  | unix expiration timestamp                          |
| nonce         | yes      | string  | maker's exchange nonce of the order is associated  |
| feeRateBps    | yes      | string  | fee rate basis points as required by the operator  |
| side          | yes      | string  | buy or sell enum index                             |
| signatureType | yes      | integer | signature type enum index                          |
| signature     | yes      | string  | hex encoded signature                              |

### Order types

* **FOK**: A Fill-Or-Kill order is an market order to buy (in dollars) or sell (in shares) shares that must be executed immediately in its entirety; otherwise, the entire order will be cancelled.
* **FAK**: A Fill-And-Kill order is a market order to buy (in dollars) or sell (in shares) that will be executed immediately for as many shares as are available; any portion not filled at once is cancelled.
* **GTC**: A Good-Til-Cancelled order is a limit order that is active until it is fulfilled or cancelled.
* **GTD**: A Good-Til-Date order is a type of order that is active until its specified date (UTC seconds timestamp), unless it has already been fulfilled or cancelled. There is a security threshold of one minute. If the order needs to expire in 90 seconds the correct expiration value is: now + 1 minute + 30 seconds

### Response Format

| Name        | Type      | Description                                                                                                                        |
| ----------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| success     | boolean   | boolean indicating if server-side err (`success = false`) -> server-side error                                                     |
| errorMsg    | string    | error message in case of unsuccessful placement (in case `success = false`, e.g. `client-side error`, the reason is in `errorMsg`) |
| orderId     | string    | id of order                                                                                                                        |
| orderHashes | string\[] | hash of settlement transaction order was marketable and triggered a match                                                          |

### Insert Error Messages

If the `errorMsg` field of the response object from placement is not an empty string, the order was not able to be immediately placed. This might be because of a delay or because of a failure. If the `success` is not `true`, then there was an issue placing the order. The following `errorMessages` are possible:

#### Error

| Error                                | Success | Message                                                                                 | Description                                                           |
| ------------------------------------ | ------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| INVALID\_ORDER\_MIN\_TICK\_SIZE      | yes     | order is invalid. Price breaks minimum tick size rules                                  | order price isn't accurate to correct tick sizing                     |
| INVALID\_ORDER\_MIN\_SIZE            | yes     | order is invalid. Size lower than the minimum                                           | order size must meet min size threshold requirement                   |
| INVALID\_ORDER\_DUPLICATED           | yes     | order is invalid. Duplicated. Same order has already been placed, can't be placed again |                                                                       |
| INVALID\_ORDER\_NOT\_ENOUGH\_BALANCE | yes     | not enough balance / allowance                                                          | funder address doesn't have sufficient balance or allowance for order |
| INVALID\_ORDER\_EXPIRATION           | yes     | invalid expiration                                                                      | expiration field expresses a time before now                          |
| INVALID\_ORDER\_ERROR                | yes     | could not insert order                                                                  | system error while inserting order                                    |
| EXECUTION\_ERROR                     | yes     | could not run the execution                                                             | system error while attempting to execute trade                        |
| ORDER\_DELAYED                       | no      | order match delayed due to market conditions                                            | order placement delayed                                               |
| DELAYING\_ORDER\_ERROR               | yes     | error delaying the order                                                                | system error while delaying order                                     |
| FOK\_ORDER\_NOT\_FILLED\_ERROR       | yes     | order couldn't be fully filled, FOK orders are fully filled/killed                      | FOK order not fully filled so can't be placed                         |
| MARKET\_NOT\_READY                   | no      | the market is not yet ready to process new orders                                       | system not accepting orders for market yet                            |

### Insert Statuses

When placing an order, a status field is included. The status field provides additional information regarding the order's state as a result of the placement. Possible values include:

#### Status

| Status    | Description                                                  |
| --------- | ------------------------------------------------------------ |
| matched   | order placed and matched with an existing resting order      |
| live      | order placed and resting on the book                         |
| delayed   | order marketable, but subject to matching delay              |
| unmatched | order marketable, but failure delaying, placement successful |

<RequestExample>
  ```python Python theme={null}
  from py_clob_client.client import ClobClient
  from py_clob_client.clob_types import OrderArgs, OrderType, PostOrdersArgs
  from py_clob_client.order_builder.constants import BUY


  host: str = "https://clob.polymarket.com"
  key: str = "" ##This is your Private Key. Export from https://reveal.magic.link/polymarket or from your Web3 Application
  chain_id: int = 137 #No need to adjust this
  POLYMARKET_PROXY_ADDRESS: str = '' #This is the address listed below your profile picture when using the Polymarket site.

  #Select from the following 3 initialization options to matches your login method, and remove any unused lines so only one client is initialized.


  ### Initialization of a client using a Polymarket Proxy associated with an Email/Magic account. If you login with your email use this example.
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client that trades directly from an EOA. 
  client = ClobClient(host, key=key, chain_id=chain_id)

  ## Create and sign a limit order buying 100 YES tokens for 0.50c each
  #Refer to the Markets API documentation to locate a tokenID: https://docs.polymarket.com/developers/gamma-markets-api/get-markets

  client.set_api_creds(client.create_or_derive_api_creds()) 

  resp = client.post_orders([
      PostOrdersArgs(
          # Create and sign a limit order buying 100 YES tokens for 0.50 each
          order=client.create_order(OrderArgs(
              price=0.01,
              size=5,
              side=BUY,
              token_id="88613172803544318200496156596909968959424174365708473463931555296257475886634",
          )),
          orderType=OrderType.GTC,  # Good 'Til Cancelled
      ),
      PostOrdersArgs(
          # Create and sign a limit order selling 200 NO tokens for 0.25 each
          order=client.create_order(OrderArgs(
              price=0.01,
              size=5,
              side=BUY,
              token_id="93025177978745967226369398316375153283719303181694312089956059680730874301533",
          )),
          orderType=OrderType.GTC,  # Good 'Til Cancelled
      )
  ])
  print(resp)
  print("Done!")
  ```

  ```javascript typescript theme={null}
  import { ethers } from "ethers";
  import { config as dotenvConfig } from "dotenv";
  import { resolve } from "path";
  import { ApiKeyCreds, Chain, ClobClient, OrderType, PostOrdersArgs, Side } from "../src";

  dotenvConfig({ path: resolve(__dirname, "../.env") });

  async function main() {
      const wallet = new ethers.Wallet(`${process.env.PK}`);
      const chainId = parseInt(`${process.env.CHAIN_ID || Chain.AMOY}`) as Chain;
      console.log(`Address: ${await wallet.getAddress()}, chainId: ${chainId}`);

      const host = process.env.CLOB_API_URL || "https://clob.polymarket.com";
      const creds: ApiKeyCreds = {
          key: `${process.env.CLOB_API_KEY}`,
          secret: `${process.env.CLOB_SECRET}`,
          passphrase: `${process.env.CLOB_PASS_PHRASE}`,
      };
      const clobClient = new ClobClient(host, chainId, wallet, creds);

      await clobClient.cancelAll();

      const YES = "71321045679252212594626385532706912750332728571942532289631379312455583992563";
      const orders: PostOrdersArgs[] = [
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.4,
                  side: Side.BUY,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.45,
                  side: Side.BUY,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.55,
                  side: Side.SELL,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.6,
                  side: Side.SELL,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
      ];

      // Send it to the server
      const resp = await clobClient.postOrders(orders);
      console.log(resp);
  }

  main();
  ```

  ```REQUEST Example Payload theme={null}
  [
      {'order': {'salt': 660377097, 'maker': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'signer': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'taker': '0x0000000000000000000000000000000000000000', 'tokenId': '88613172803544318200496156596909968959424174365708473463931555296257475886634', 'makerAmount': '50000', 'takerAmount': '5000000', 'expiration': '0', 'nonce': '0', 'feeRateBps': '0', 'side': 'BUY', 'signatureType': 0, 'signature': '0xccb8d1298d698ebc0859e6a26044c848ac4a4b0e20a391a4574e42b9c9bf237e5fa09fc00743e3e2d2f8e909a21d60f276ce083cc35c6661410b892f5bcbe2291c'}, 'owner': 'PRIVATEKEY', 'orderType': 'GTC'}, 
      {'order': {'salt': 1207111323, 'maker': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'signer': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'taker': '0x0000000000000000000000000000000000000000', 'tokenId': '93025177978745967226369398316375153283719303181694312089956059680730874301533', 'makerAmount': '50000', 'takerAmount': '5000000', 'expiration': '0', 'nonce': '0', 'feeRateBps': '0', 'side': 'BUY', 'signatureType': 0, 'signature': '0x0feca28666283824c27d7bead0bc441dde6df20dd71ef5ff7c84d3d1d5bf8aa4296fa382769dc11a92abe05b6f731d6c32556e9b4fb29e6eb50131af23a9ac941c'}, 'owner': 'PRIVATEKEY', 'orderType': 'GTC'}
  ]

  ```
</RequestExample>


# Get Active Orders
Source: https://docs.polymarket.com/developers/CLOB/orders/get-active-order



<Tip> This endpoint requires a L2 Header. </Tip>

Get active order(s) for a specific market.

**HTTP REQUEST**

`GET /<clob-endpoint>/data/orders`

### Request Parameters

| Name      | Required | Type   | Description                          |
| --------- | -------- | ------ | ------------------------------------ |
| id        | no       | string | id of order to get information about |
| market    | no       | string | condition id of market               |
| asset\_id | no       | string | id of the asset/token                |

### Response Format

| Name | Type         | Description                                          |
| ---- | ------------ | ---------------------------------------------------- |
| null | OpenOrder\[] | list of open orders filtered by the query parameters |

<RequestExample>
  ```python Python theme={null}
  from py_clob_client.clob_types import OpenOrderParams

  resp = client.get_orders(
      OpenOrderParams(
          market="0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
      )
  )
  print(resp)
  print("Done!")
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const resp = await clobClient.getOpenOrders({
      market:
        "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
    });
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</RequestExample>


# Get Order
Source: https://docs.polymarket.com/developers/CLOB/orders/get-order

Get information about an existing order

<Tip>This endpoint requires a L2 Header. </Tip>

Get single order by id.

**HTTP REQUEST**

`GET /<clob-endpoint>/data/order/<order_hash>`

### Request Parameters

| Name | Required | Type   | Description                          |
| ---- | -------- | ------ | ------------------------------------ |
| id   | no       | string | id of order to get information about |

### Response Format

| Name  | Type      | Description        |
| ----- | --------- | ------------------ |
| order | OpenOrder | order if it exists |

An `OpenOrder` object is of the form:

| Name              | Type      | Description                                                    |
| ----------------- | --------- | -------------------------------------------------------------- |
| associate\_trades | string\[] | any Trade id the order has been partially included in          |
| id                | string    | order id                                                       |
| status            | string    | order current status                                           |
| market            | string    | market id (condition id)                                       |
| original\_size    | string    | original order size at placement                               |
| outcome           | string    | human readable outcome the order is for                        |
| maker\_address    | string    | maker address (funder)                                         |
| owner             | string    | api key                                                        |
| price             | string    | price                                                          |
| side              | string    | buy or sell                                                    |
| size\_matched     | string    | size of order that has been matched/filled                     |
| asset\_id         | string    | token id                                                       |
| expiration        | string    | unix timestamp when the order expired, 0 if it does not expire |
| type              | string    | order type (GTC, FOK, GTD)                                     |
| created\_at       | string    | unix timestamp when the order was created                      |

<RequestExample>
  ```python Python theme={null}
  order = clob_client.get_order("0xb816482a5187a3d3db49cbaf6fe3ddf24f53e6c712b5a4bf5e01d0ec7b11dabc")
  print(order)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const order = await clobClient.getOrder(
      "0xb816482a5187a3d3db49cbaf6fe3ddf24f53e6c712b5a4bf5e01d0ec7b11dabc"
    );
    console.log(order);
  }

  main();

  ```
</RequestExample>


# Onchain Order Info
Source: https://docs.polymarket.com/developers/CLOB/orders/onchain-order-info



## How do I interpret the OrderFilled onchain event?

Given an OrderFilled event:

* `orderHash`: a unique hash for the Order being filled
* `maker`: the user generating the order and the source of funds for the order
* `taker`: the user filling the order OR the Exchange contract if the order fills multiple limit orders
* `makerAssetId`: id of the asset that is given out. If 0, indicates that the Order is a BUY, giving USDC in exchange for Outcome tokens. Else, indicates that the Order is a SELL, giving Outcome tokens in exchange for USDC.
* `takerAssetId`: id of the asset that is received. If 0, indicates that the Order is a SELL, receiving USDC in exchange for Outcome tokens. Else, indicates that the Order is a BUY, receiving Outcome tokens in exchange for USDC.
* `makerAmountFilled`: the amount of the asset that is given out.
* `takerAmountFilled`: the amount of the asset that is received.
* `fee`: the fees paid by the order maker


# Orders Overview
Source: https://docs.polymarket.com/developers/CLOB/orders/orders

Detailed instructions for creating, placing, and managing orders using Polymarket's CLOB API.

All orders are expressed as limit orders (can be marketable). The underlying order primitive must be in the form expected and executable by the on-chain binary limit order protocol contract. Preparing such an order is quite involved (structuring, hashing, signing), thus Polymarket suggests using the open source typescript, python and golang libraries.

## Allowances

To place an order, allowances must be set by the funder address for the specified `maker` asset for the Exchange contract. When buying, this means the funder must have set a USDC allowance greater than or equal to the spending amount. When selling, the funder must have set an allowance for the conditional token that is greater than or equal to the selling amount. This allows the Exchange contract to execute settlement according to the signed order instructions created by a user and matched by the operator.

## Signature Types

Polymarket’s CLOB supports 3 signature types. Orders must identify what signature type they use. The available typescript and python clients abstract the complexity of signing and preparing orders with the following signature types by allowing a funder address and signer type to be specified on initialization. The supported signature types are:

| Type               | ID | Description                                                                                |
| ------------------ | -- | ------------------------------------------------------------------------------------------ |
| EOA                | 0  | EIP712 signature signed by an EOA                                                          |
| POLY\_PROXY        | 1  | EIP712 signatures signed by a signer associated with funding Polymarket proxy wallet       |
| POLY\_GNOSIS\_SAFE | 2  | EIP712 signatures signed by a signer associated with funding Polymarket gnosis safe wallet |

## Validity Checks

Orders are continually monitored to make sure they remain valid. Specifically, this includes continually tracking underlying balances, allowances and on-chain order cancellations. Any maker that is caught intentionally abusing these checks (which are essentially real time) will be blacklisted.

Additionally, there are rails on order placement in a market. Specifically, you can only place orders that sum to less than or equal to your available balance for each market. For example if you have 500 USDC in your funding wallet, you can place one order to buy 1000 YES in marketA @ \$.50, then any additional buy orders to that market will be rejected since your entire balance is reserved for the first (and only) buy order. More explicitly the max size you can place for an order is:

$$
\text{maxOrderSize} = \text{underlyingAssetBalance} - \sum(\text{orderSize} - \text{orderFillAmount})
$$


# null
Source: https://docs.polymarket.com/developers/CLOB/status



Check the status of the Polymarket Order Book:

[Status Page](https://status-clob.polymarket.com/)


# Get Trades
Source: https://docs.polymarket.com/developers/CLOB/trades/trades



<Tip> This endpoint requires a L2 Header. </Tip>

Get trades for the authenticated user based on the provided filters.

**HTTP REQUEST**

`GET /<clob-endpoint>/data/trades`

### Request Parameters

| Name   | Required | Type   | Description                                                                                         |
| ------ | -------- | ------ | --------------------------------------------------------------------------------------------------- |
| id     | no       | string | id of trade to fetch                                                                                |
| taker  | no       | string | address to get trades for where it is included as a taker                                           |
| maker  | no       | string | address to get trades for where it is included as a maker                                           |
| market | no       | string | market for which to get the trades (condition ID)                                                   |
| before | no       | string | unix timestamp representing the cutoff up to which trades that happened before then can be included |
| after  | no       | string | unix timestamp representing the cutoff for which trades that happened after can be included         |

### Response Format

| Name | Type     | Description                                 |
| ---- | -------- | ------------------------------------------- |
| null | Trade\[] | list of trades filtered by query parameters |

A `Trade` object is of the form:

| Name              | Type          | Description                                                                  |
| ----------------- | ------------- | ---------------------------------------------------------------------------- |
| id                | string        | trade id                                                                     |
| taker\_order\_id  | string        | hash of taker order (market order) that catalyzed the trade                  |
| market            | string        | market id (condition id)                                                     |
| asset\_id         | string        | asset id (token id) of taker order (market order)                            |
| side              | string        | buy or sell                                                                  |
| size              | string        | size                                                                         |
| fee\_rate\_bps    | string        | the fees paid for the taker order expressed in basic points                  |
| price             | string        | limit price of taker order                                                   |
| status            | string        | trade status (see above)                                                     |
| match\_time       | string        | time at which the trade was matched                                          |
| last\_update      | string        | timestamp of last status update                                              |
| outcome           | string        | human readable outcome of the trade                                          |
| maker\_address    | string        | funder address of the taker of the trade                                     |
| owner             | string        | api key of taker of the trade                                                |
| transaction\_hash | string        | hash of the transaction where the trade was executed                         |
| bucket\_index     | integer       | index of bucket for trade in case trade is executed in multiple transactions |
| maker\_orders     | MakerOrder\[] | list of the maker trades the taker trade was filled against                  |
| type              | string        | side of the trade: TAKER or MAKER                                            |

A `MakerOrder` object is of the form:

| Name            | Type   | Description                                                 |
| --------------- | ------ | ----------------------------------------------------------- |
| order\_id       | string | id of maker order                                           |
| maker\_address  | string | maker address of the order                                  |
| owner           | string | api key of the owner of the order                           |
| matched\_amount | string | size of maker order consumed with this trade                |
| fee\_rate\_bps  | string | the fees paid for the taker order expressed in basic points |
| price           | string | price of maker order                                        |
| asset\_id       | string | token/asset id                                              |
| outcome         | string | human readable outcome of the maker order                   |
| side            | string | the side of the maker order. Can be `buy` or `sell`         |

<RequestExample>
  ```python Python theme={null}
  from py_clob_client.clob_types import TradeParams

  resp = client.get_trades(
      TradeParams(
          maker_address=client.get_address(),
          market="0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
      ),
  )
  print(resp)
  print("Done!")
  ```

  ```typescript Typescript theme={null}
  async function main() {
    const trades = await clobClient.getTrades({
      market:
        "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
      maker_address: await wallet.getAddress(),
    });
    console.log(`trades: `);
    console.log(trades);
  }

  main();
  ```
</RequestExample>


# Trades Overview
Source: https://docs.polymarket.com/developers/CLOB/trades/trades-overview



## Overview

All historical trades can be fetched via the Polymarket CLOB REST API. A trade is initiated by a "taker" who creates a marketable limit order. This limit order can be matched against one or more resting limit orders on the associated book. A trade can be in various states as described below. Note: in some cases (due to gas limitations) the execution of a "trade" must be broken into multiple transactions which case separate trade entities will be returned. To associate trade entities, there is a bucket\_index field and a match\_time field. Trades that have been broken into multiple trade objects can be reconciled by combining trade objects with the same market\_order\_id, match\_time and incrementing bucket\_index's into a top level "trade" client side.

## Statuses

| Status    | Terminal? | Description                                                                                                                                               |
| --------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MATCHED   | no        | trade has been matched and sent to the executor service by the operator, the executor service submits the trade as a transaction to the Exchange contract |
| MINED     | no        | trade is observed to be mined into the chain, no finality threshold established                                                                           |
| CONFIRMED | yes       | trade has achieved strong probabilistic finality and was successful                                                                                       |
| RETRYING  | no        | trade transaction has failed (revert or reorg) and is being retried/resubmitted by the operator                                                           |
| FAILED    | yes       | trade has failed and is not being retried                                                                                                                 |


# Market Channel
Source: https://docs.polymarket.com/developers/CLOB/websocket/market-channel



Public channel for updates related to market updates (level 2 price data).

**SUBSCRIBE**

`<wss-channel> market`

## Book Message

Emitted When:

* First subscribed to a market
* When there is a trade that affects the book

### Structure

| Name        | Type            | Description                                                                 |
| ----------- | --------------- | --------------------------------------------------------------------------- |
| event\_type | string          | "book"                                                                      |
| asset\_id   | string          | asset ID (token ID)                                                         |
| market      | string          | condition ID of market                                                      |
| timestamp   | string          | unix timestamp the current book generation in milliseconds (1/1,000 second) |
| hash        | string          | hash summary of the orderbook content                                       |
| buys        | OrderSummary\[] | list of type (size, price) aggregate book levels for buys                   |
| sells       | OrderSummary\[] | list of type (size, price) aggregate book levels for sells                  |

Where a `OrderSummary` object is of the form:

| Name  | Type   | Description                        |
| ----- | ------ | ---------------------------------- |
| price | string | size available at that price level |
| size  | string | price of the orderbook level       |

```json Response theme={null}
{
  "event_type": "book",
  "asset_id": "65818619657568813474341868652308942079804919287380422192892211131408793125422",
  "market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
  "bids": [
    { "price": ".48", "size": "30" },
    { "price": ".49", "size": "20" },
    { "price": ".50", "size": "15" }
  ],
  "asks": [
    { "price": ".52", "size": "25" },
    { "price": ".53", "size": "60" },
    { "price": ".54", "size": "10" }
  ],
  "timestamp": "123456789000",
  "hash": "0x0...."
}
```

## price\_change Message

<div style={{backgroundColor: '#fff3cd', border: '1px solid #ffeaa7', borderRadius: '4px', padding: '12px', marginBottom: '16px'}}>
  <strong>⚠️ Breaking Change Notice:</strong> The price\_change message schema will be updated on September 15, 2025 at 11 PM UTC. Please see the [migration guide](/developers/CLOB/websocket/market-channel-migration-guide) for details.
</div>

Emitted When:

* A new order is placed
* An order is cancelled

### Structure

| Name           | Type           | Description                    |
| -------------- | -------------- | ------------------------------ |
| event\_type    | string         | "price\_change"                |
| market         | string         | condition ID of market         |
| price\_changes | PriceChange\[] | array of price change objects  |
| timestamp      | string         | unix timestamp in milliseconds |

Where a `PriceChange` object is of the form:

| Name      | Type   | Description                        |
| --------- | ------ | ---------------------------------- |
| asset\_id | string | asset ID (token ID)                |
| price     | string | price level affected               |
| size      | string | new aggregate size for price level |
| side      | string | "BUY" or "SELL"                    |
| hash      | string | hash of the order                  |
| best\_bid | string | current best bid price             |
| best\_ask | string | current best ask price             |

```json Response theme={null}
{
    "market": "0x5f65177b394277fd294cd75650044e32ba009a95022d88a0c1d565897d72f8f1",
    "price_changes": [
        {
            "asset_id": "71321045679252212594626385532706912750332728571942532289631379312455583992563",
            "price": "0.5",
            "size": "200",
            "side": "BUY",
            "hash": "56621a121a47ed9333273e21c83b660cff37ae50",
            "best_bid": "0.5",
            "best_ask": "1"
        },
        {
            "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
            "price": "0.5",
            "size": "200",
            "side": "SELL",
            "hash": "1895759e4df7a796bf4f1c5a5950b748306923e2",
            "best_bid": "0",
            "best_ask": "0.5"
        }
    ],
    "timestamp": "1757908892351",
    "event_type": "price_change"
}
```

## tick\_size\_change Message

Emitted When:

* The minimum tick size of the market changes. This happens when the book's price reaches the limits: price > 0.96 or price \< 0.04

### Structure

| Name            | Type   | Description                |
| --------------- | ------ | -------------------------- |
| event\_type     | string | "price\_change"            |
| asset\_id       | string | asset ID (token ID)        |
| market          | string | condition ID of market     |
| old\_tick\_size | string | previous minimum tick size |
| new\_tick\_size | string | current minimum tick size  |
| side            | string | buy/sell                   |
| timestamp       | string | time of event              |

```json Response theme={null}
{
"event_type": "tick_size_change",
"asset_id": "65818619657568813474341868652308942079804919287380422192892211131408793125422",\
"market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
"old_tick_size": "0.01",
"new_tick_size": "0.001",
"timestamp": "100000000"
}
```

## last\_trade\_price Message

Emitted When:

* When a maker and taker order is matched creating a trade event.

```json Response theme={null}
{
"asset_id":"114122071509644379678018727908709560226618148003371446110114509806601493071694",
"event_type":"last_trade_price",
"fee_rate_bps":"0",
"market":"0x6a67b9d828d53862160e470329ffea5246f338ecfffdf2cab45211ec578b0347",
"price":"0.456",
"side":"BUY",
"size":"219.217767",
"timestamp":"1750428146322"
}
```


# User Channel
Source: https://docs.polymarket.com/developers/CLOB/websocket/user-channel



Authenticated channel for updates related to user activities (orders, trades), filtered for authenticated user by apikey.

**SUBSCRIBE**

`<wss-channel> user`

## Trade Message

Emitted when:

* when a market order is matched ("MATCHED")
* when a limit order for the user is included in a trade ("MATCHED")
* subsequent status changes for trade ("MINED", "CONFIRMED", "RETRYING", "FAILED")

### Structure

| Name             | Type          | Description                                 |
| ---------------- | ------------- | ------------------------------------------- |
| asset\_id        | string        | asset id (token ID) of order (market order) |
| event\_type      | string        | "trade"                                     |
| id               | string        | trade id                                    |
| last\_update     | string        | time of last update to trade                |
| maker\_orders    | MakerOrder\[] | array of maker order details                |
| market           | string        | market identifier (condition ID)            |
| matchtime        | string        | time trade was matched                      |
| outcome          | string        | outcome                                     |
| owner            | string        | api key of event owner                      |
| price            | string        | price                                       |
| side             | string        | BUY/SELL                                    |
| size             | string        | size                                        |
| status           | string        | trade status                                |
| taker\_order\_id | string        | id of taker order                           |
| timestamp        | string        | time of event                               |
| trade\_owner     | string        | api key of trade owner                      |
| type             | string        | "TRADE"                                     |

Where a `MakerOrder` object is of the form:

| Name            | Type   | Description                            |
| --------------- | ------ | -------------------------------------- |
| asset\_id       | string | asset of the maker order               |
| matched\_amount | string | amount of maker order matched in trade |
| order\_id       | string | maker order ID                         |
| outcome         | string | outcome                                |
| owner           | string | owner of maker order                   |
| price           | string | price of maker order                   |

```json Response theme={null}
{
  "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
  "event_type": "trade",
  "id": "28c4d2eb-bbea-40e7-a9f0-b2fdb56b2c2e",
  "last_update": "1672290701",
  "maker_orders": [
    {
      "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
      "matched_amount": "10",
      "order_id": "0xff354cd7ca7539dfa9c28d90943ab5779a4eac34b9b37a757d7b32bdfb11790b",
      "outcome": "YES",
      "owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
      "price": "0.57"
    }
  ],
  "market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
  "matchtime": "1672290701",
  "outcome": "YES",
  "owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "price": "0.57",
  "side": "BUY",
  "size": "10",
  "status": "MATCHED",
  "taker_order_id": "0x06bc63e346ed4ceddce9efd6b3af37c8f8f440c92fe7da6b2d0f9e4ccbc50c42",
  "timestamp": "1672290701",
  "trade_owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "type": "TRADE"
}
```

## Order Message

Emitted when:

* When an order is placed (PLACEMENT)
* When an order is updated (some of it is matched) (UPDATE)
* When an order is canceled (CANCELLATION)

### Structure

| Name              | Type      | Description                                                         |
| ----------------- | --------- | ------------------------------------------------------------------- |
| asset\_id         | string    | asset ID (token ID) of order                                        |
| associate\_trades | string\[] | array of ids referencing trades that the order has been included in |
| event\_type       | string    | "order"                                                             |
| id                | string    | order id                                                            |
| market            | string    | condition ID of market                                              |
| order\_owner      | string    | owner of order                                                      |
| original\_size    | string    | original order size                                                 |
| outcome           | string    | outcome                                                             |
| owner             | string    | owner of orders                                                     |
| price             | string    | price of order                                                      |
| side              | string    | BUY/SELL                                                            |
| size\_matched     | string    | size of order that has been matched                                 |
| timestamp         | string    | time of event                                                       |
| type              | string    | PLACEMENT/UPDATE/CANCELLATION                                       |

```json Response theme={null}
{
  "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
  "associate_trades": null,
  "event_type": "order",
  "id": "0xff354cd7ca7539dfa9c28d90943ab5779a4eac34b9b37a757d7b32bdfb11790b",
  "market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
  "order_owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "original_size": "10",
  "outcome": "YES",
  "owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "price": "0.57",
  "side": "SELL",
  "size_matched": "0",
  "timestamp": "1672290687",
  "type": "PLACEMENT"
}
```


# WSS Authentication
Source: https://docs.polymarket.com/developers/CLOB/websocket/wss-auth



<Tip> Only connections to `user` channel require authentication. </Tip>

| Field      | Optional | Description                           |
| ---------- | -------- | ------------------------------------- |
| apikey     | yes      | Polygon account's CLOB api key        |
| secret     | yes      | Polygon account's CLOB api secret     |
| passphrase | yes      | Polygon account's CLOB api passphrase |


# WSS Overview
Source: https://docs.polymarket.com/developers/CLOB/websocket/wss-overview

Overview and general information about the Polymarket Websocket

## Overview

The Polymarket CLOB API provides websocket (wss) channels through which clients can get pushed updates. These endpoints allow clients to maintain almost real-time views of their orders, their trades and markets in general. There are two available channels `user` and `market`.

## Subscription

To subscribe send a message including the following authentication and intent information upon opening the connection.

| Field       | Type      | Description                                                                 |
| ----------- | --------- | --------------------------------------------------------------------------- |
| auth        | Auth      | see next page for auth information                                          |
| markets     | string\[] | array of markets (condition IDs) to receive events for (for `user` channel) |
| assets\_ids | string\[] | array of asset ids (token IDs) to receive events for (for `market` channel) |
| type        | string    | id of channel to subscribe to (USER or MARKET)                              |

Where the `auth` field is of type `Auth` which has the form described in the WSS Authentication section below.


# Deployment and Additional Information
Source: https://docs.polymarket.com/developers/CTF/deployment-resources



## Deployment

The CTF contract is deployed (and verified) at the following addresses:

| Network         | Deployed Address                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Polygon Mainnet | [0x4D97DCd97eC945f40cF65F87097ACe5EA0476045](https://polygonscan.com/address/0x4D97DCd97eC945f40cF65F87097ACe5EA0476045) |
| Polygon Mainnet | [0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E](https://polygonscan.com/address/0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E) |

Polymarket provides code samples in both Python and TypeScript for interacting
with our smart chain contracts. You will need an RPC endpoint to access the
blockchain, and you'll be responsible for paying gas fees when executing these
RPC/function calls. Please ensure you're using the correct example for your wallet
type (Safe Wallet vs Proxy Wallet) when implementing.

## Resources

* [On-Chain Code Samples](https://github.com/Polymarket/examples/tree/main/examples)
* [Polygon RPC List](https://chainlist.org/chain/137)
* [CTF Source Code](https://github.com/gnosis/conditional-tokens-contracts)
* [Audits](https://github.com/gnosis/conditional-tokens-contracts/tree/master/docs/audit)
* [Gist For positionId Calculation](https://gist.github.com/L-Kov/950bce141a9d1aa1ed3b1cfce6d30217)


# Merging Tokens
Source: https://docs.polymarket.com/developers/CTF/merge



In addition to splitting collateral for a full set, the inverse can also happen; a full set can be "merged" for collateral. This operation can again happen at any time after a condition has been prepared on the CTF contract. One unit of each position in a full set is burned in return for 1 collateral unit. This operation happens via the `mergePositions()` function on the CTF contract with the following parameters:

* `collateralToken`: IERC20 - The address of the positions' backing collateral token.
* `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being merged and the merge target positions. Null in Polymarket case.
* `conditionId`: bytes32 - The ID of the condition to merge on.
* `partition`: uint\[] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint). Each element's a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
* `amount` - The number of full sets to merge. Also the amount of collateral to receive.


# Overview
Source: https://docs.polymarket.com/developers/CTF/overview



All outcomes on Polymarket are tokenized on the Polygon network. Specifically, Polymarket outcomes shares are binary outcomes (ie "YES" and "NO") using Gnosis' Conditional Token Framework (CTF). They are distinct ERC1155 tokens related to a parent condition and backed by the same collateral. More technically, the binary outcome tokens are referred to as "positionIds" in Gnosis's documentation. "PositionIds" are derived from a collateral token and distinct "collectionIds". "CollectionIds" are derived from a "parentCollectionId", (always bytes32(0) in our case) a "conditionId", and a unique "indexSet".

The "indexSet" is a 256 bit array denoting which outcome slots are in an outcome collection; it MUST be a nonempty proper subset of a condition's outcome slots. In the binary case, which we are interested in, there are two "indexSets", one for the first outcome and one for the second. The first outcome's "indexSet" is 0b01 = 1 and the second's is 0b10 = 2. The parent "conditionId" (shared by both "collectionIds" and therefore "positionIds") is derived from a "questionId" (a hash of the UMA ancillary data), an "oracle" (the UMA adapter V2), and an "outcomeSlotCount" (always 2 in the binary case). The steps for calculating the ERC1155 token ids (positionIds) is as follows:

1. Get the conditionId
   1. Function:
      1. `getConditionId(oracle, questionId, outcomeSlotCount)`
   2. Inputs:
      1. `oracle`: address - UMA adapter V2
      2. `questionId`: bytes32 - hash of the UMA ancillary data
      3. `outcomeSlotCount`: uint - 2 for binary markets

2. Get the two collectionIds
   1. Function:
      1. `getCollectionId(parentCollectionId, conditionId, indexSet)`
   2. Inputs:
      1. `parentCollectionId`: bytes32 - bytes32(0)
      2. `conditionId`: bytes32 - the conditionId derived from (1)
      3. `indexSet`: uint - 1 (0b01) for the first and 2 (0b10) for the second.

3. Get the two positionIds
   1. Function:
      1. `getPositionId(collateralToken, collectionId)`
   2. Inputs:
      1. `collateralToken`: IERC20 - address of ERC20 token collateral (USDC)
      2. `collectionId`: bytes32 - the two collectionIds derived from (3)

Leveraging the relations above, specifically "conditionIds" -> "positionIds" the Gnosis CTF contract allows for "splitting" and "merging" full outcome sets. We explore these actions and provide code examples below.


# Reedeeming Tokens
Source: https://docs.polymarket.com/developers/CTF/redeem



Once a condition has had it's payouts reported (ie by the UMACTFAdapter calling `reportPayouts` on the CTF contract), users with shares in the winning outcome can redeem them for the underlying collateral. Specifically, users can call the `redeemPositions` function on the CTF contract which will burn all valuable conditional tokens in return for collateral according to the reported payout vector. This function has the following parameters:

* `collateralToken`: IERC20 - The address of the positions' backing collateral token.
* `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being redeemed. Null in Polymarket case.
* `indexSets`: uint\[] - The ID of the condition to redeem.
* `indexSets`: uint\[] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint). Each element's a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.


# Splitting USDC
Source: https://docs.polymarket.com/developers/CTF/split



At any time, after a condition has been prepared on the CTF contract (via `prepareCondition`), it is possible to "split" collateral into a full (position) set. In other words, one unit USDC can be split into 1 YES unit and 1 NO unit. If splitting from the collateral, the CTF contract will attempt to transfer `amount` collateral from the message sender to itself. If successful, `amount` stake will be minted in the split target positions. If any of the transfers, mints, or burns fail, the transaction will revert. The transaction will also revert if the given partition is trivial, invalid, or refers to more slots than the condition is prepared with. This operation happens via the `splitPosition()` function on the CTF contract with the following parameters:

* `collateralToken`: IERC20 - The address of the positions' backing collateral token.
* `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being split and the split target positions. Null in Polymarket case.
* `conditionId`: bytes32 - The ID of the condition to split on.
* `partition`: uint\[] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint). Each element's a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
* `amount` - The amount of collateral or stake to split. Also the number of full sets to receive.


# RTDS Comments
Source: https://docs.polymarket.com/developers/RTDS/RTDS-comments



<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

## Overview

The comments subscription provides real-time updates for comment-related events on the Polymarket platform. This includes new comments being created, as well as other comment interactions like reactions and replies.

## Subscription Details

* **Topic**: `comments`
* **Type**: `comment_created` (and potentially other comment event types like `reaction_created`)
* **Authentication**: May require Gamma authentication for user-specific data
* **Filters**: Optional (can filter by specific comment IDs, users, or events)

## Subscription Message

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "comments", 
      "type": "comment_created"
    }
  ]
}
```

## Message Format

When subscribed to comments, you'll receive messages with the following structure:

```json  theme={null}
{
  "topic": "comments",
  "type": "comment_created",
  "timestamp": 1753454975808,
  "payload": {
    "body": "do you know what the term encircle means? it means to surround from all sides, Russia has present on only 1 side, that's the opposite of an encirclement",
    "createdAt": "2025-07-25T14:49:35.801298Z",
    "id": "1763355",
    "parentCommentID": "1763325",
    "parentEntityID": 18396,
    "parentEntityType": "Event",
    "profile": {
      "baseAddress": "0xce533188d53a16ed580fd5121dedf166d3482677",
      "displayUsernamePublic": true,
      "name": "salted.caramel",
      "proxyWallet": "0x4ca749dcfa93c87e5ee23e2d21ff4422c7a4c1ee",
      "pseudonym": "Adored-Disparity"
    },
    "reactionCount": 0,
    "replyAddress": "0x0bda5d16f76cd1d3485bcc7a44bc6fa7db004cdd",
    "reportCount": 0,
    "userAddress": "0xce533188d53a16ed580fd5121dedf166d3482677"
  }
}
```

## Message Types

### comment\_created

Triggered when a user creates a new comment on an event or in reply to another comment.

### comment\_removed

Triggered when a comment is removed or deleted.

### reaction\_created

Triggered when a user adds a reaction to an existing comment.

### reaction\_removed

Triggered when a reaction is removed from a comment.

## Payload Fields

| Field              | Type   | Description                                                               |
| ------------------ | ------ | ------------------------------------------------------------------------- |
| `body`             | string | The text content of the comment                                           |
| `createdAt`        | string | ISO 8601 timestamp when the comment was created                           |
| `id`               | string | Unique identifier for this comment                                        |
| `parentCommentID`  | string | ID of the parent comment if this is a reply (null for top-level comments) |
| `parentEntityID`   | number | ID of the parent entity (event, market, etc.)                             |
| `parentEntityType` | string | Type of parent entity (e.g., "Event", "Market")                           |
| `profile`          | object | Profile information of the user who created the comment                   |
| `reactionCount`    | number | Current number of reactions on this comment                               |
| `replyAddress`     | string | Polygon address for replies (may be different from userAddress)           |
| `reportCount`      | number | Current number of reports on this comment                                 |
| `userAddress`      | string | Polygon address of the user who created the comment                       |

### Profile Object Fields

| Field                   | Type    | Description                                       |
| ----------------------- | ------- | ------------------------------------------------- |
| `baseAddress`           | string  | User profile address                              |
| `displayUsernamePublic` | boolean | Whether the username should be displayed publicly |
| `name`                  | string  | User's display name                               |
| `proxyWallet`           | string  | Proxy wallet address used for transactions        |
| `pseudonym`             | string  | Generated pseudonym for the user                  |

## Parent Entity Types

The following parent entity types are supported:

* `Event` - Comments on prediction events
* `Market` - Comments on specific markets
* Additional entity types may be available

## Example Messages

### New Comment Created

```json  theme={null}
{
  "topic": "comments",
  "type": "comment_created",
  "timestamp": 1753454975808,
  "payload": {
    "body": "do you know what the term encircle means? it means to surround from all sides, Russia has present on only 1 side, that's the opposite of an encirclement",
    "createdAt": "2025-07-25T14:49:35.801298Z",
    "id": "1763355",
    "parentCommentID": "1763325",
    "parentEntityID": 18396,
    "parentEntityType": "Event",
    "profile": {
      "baseAddress": "0xce533188d53a16ed580fd5121dedf166d3482677",
      "displayUsernamePublic": true,
      "name": "salted.caramel",
      "proxyWallet": "0x4ca749dcfa93c87e5ee23e2d21ff4422c7a4c1ee",
      "pseudonym": "Adored-Disparity"
    },
    "reactionCount": 0,
    "replyAddress": "0x0bda5d16f76cd1d3485bcc7a44bc6fa7db004cdd",
    "reportCount": 0,
    "userAddress": "0xce533188d53a16ed580fd5121dedf166d3482677"
  }
}
```

### Reply to Existing Comment

```json  theme={null}
{
  "topic": "comments",
  "type": "comment_created",
  "timestamp": 1753454985123,
  "payload": {
    "body": "That's a good point about the definition of encirclement.",
    "createdAt": "2025-07-25T14:49:45.120000Z",
    "id": "1763356",
    "parentCommentID": "1763355",
    "parentEntityID": 18396,
    "parentEntityType": "Event",
    "profile": {
      "baseAddress": "0x1234567890abcdef1234567890abcdef12345678",
      "displayUsernamePublic": true,
      "name": "trader",
      "proxyWallet": "0x9876543210fedcba9876543210fedcba98765432",
      "pseudonym": "Bright-Analysis"
    },
    "reactionCount": 0,
    "replyAddress": "0x0bda5d16f76cd1d3485bcc7a44bc6fa7db004cdd",
    "reportCount": 0,
    "userAddress": "0x1234567890abcdef1234567890abcdef12345678"
  }
}
```

## Comment Hierarchy

Comments support nested threading:

* **Top-level comments**: `parentCommentID` is null or empty
* **Reply comments**: `parentCommentID` contains the ID of the parent comment
* All comments are associated with a `parentEntityID` and `parentEntityType`

## Use Cases

* Real-time comment feed displays
* Discussion thread monitoring
* Community sentiment analysis

## Content

* Comments include `reactionCount` and `reportCount`
* Comment body contains the full text content

## Notes

* The `createdAt` timestamp uses ISO 8601 format with timezone information
* The outer `timestamp` field represents when the WebSocket message was sent
* User profiles include both primary addresses and proxy wallet addresses


# RTDS Crypto Prices
Source: https://docs.polymarket.com/developers/RTDS/RTDS-crypto-prices



<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

## Overview

The crypto prices subscription provides real-time updates for cryptocurrency price data from two different sources:

* **Binance Source** (`crypto_prices`): Real-time price data from Binance exchange
* **Chainlink Source** (`crypto_prices_chainlink`): Price data from Chainlink oracle networks

Both streams deliver current market prices for various cryptocurrency trading pairs, but use different symbol formats and subscription structures.

## Binance Source (`crypto_prices`)

### Subscription Details

* **Topic**: `crypto_prices`
* **Type**: `update`
* **Authentication**: Not required
* **Filters**: Optional (specific symbols can be filtered)
* **Symbol Format**: Lowercase concatenated pairs (e.g., `solusdt`, `btcusdt`)

### Subscription Message

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices",
      "type": "update"
    }
  ]
}
```

### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a filters parameter:

```json  theme={null}
{
  "action": "subscribe", 
  "subscriptions": [
    {
      "topic": "crypto_prices",
      "type": "update",
      "filters": "solusdt,btcusdt,ethusdt"
    }
  ]
}
```

## Chainlink Source (`crypto_prices_chainlink`)

### Subscription Details

* **Topic**: `crypto_prices_chainlink`
* **Type**: `*` (all types)
* **Authentication**: Not required
* **Filters**: Optional (JSON object with symbol specification)
* **Symbol Format**: Slash-separated pairs (e.g., `eth/usd`, `btc/usd`)

### Subscription Message

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices_chainlink",
      "type": "*",
      "filters": ""
    }
  ]
}
```

### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a JSON filters parameter:

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices_chainlink",
      "type": "*",
      "filters": "{\"symbol\":\"eth/usd\"}"
    }
  ]
}
```

## Message Format

### Binance Source Message Format

When subscribed to Binance crypto prices (`crypto_prices`), you'll receive messages with the following structure:

```json  theme={null}
{
  "topic": "crypto_prices",
  "type": "update", 
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "solusdt",
    "timestamp": 1753314064213,
    "value": 189.55
  }
}
```

### Chainlink Source Message Format

When subscribed to Chainlink crypto prices (`crypto_prices_chainlink`), you'll receive messages with the following structure:

```json  theme={null}
{
  "topic": "crypto_prices_chainlink",
  "type": "update", 
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "eth/usd",
    "timestamp": 1753314064213,
    "value": 3456.78
  }
}
```

## Payload Fields

| Field       | Type   | Description                                                                                                                                                |
| ----------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `symbol`    | string | Trading pair symbol<br />**Binance**: lowercase concatenated (e.g., "solusdt", "btcusdt")<br />**Chainlink**: slash-separated (e.g., "eth/usd", "btc/usd") |
| `timestamp` | number | Price timestamp in Unix milliseconds                                                                                                                       |
| `value`     | number | Current price value in the quote currency                                                                                                                  |

## Example Messages

### Binance Source Examples

#### Solana Price Update (Binance)

```json  theme={null}
{
  "topic": "crypto_prices",
  "type": "update",
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "solusdt", 
    "timestamp": 1753314064213,
    "value": 189.55
  }
}
```

#### Bitcoin Price Update (Binance)

```json  theme={null}
{
  "topic": "crypto_prices",
  "type": "update", 
  "timestamp": 1753314088421,
  "payload": {
    "symbol": "btcusdt",
    "timestamp": 1753314088395,
    "value": 67234.50
  }
}
```

### Chainlink Source Examples

#### Ethereum Price Update (Chainlink)

```json  theme={null}
{
  "topic": "crypto_prices_chainlink",
  "type": "update",
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "eth/usd", 
    "timestamp": 1753314064213,
    "value": 3456.78
  }
}
```

#### Bitcoin Price Update (Chainlink)

```json  theme={null}
{
  "topic": "crypto_prices_chainlink",
  "type": "update", 
  "timestamp": 1753314088421,
  "payload": {
    "symbol": "btc/usd",
    "timestamp": 1753314088395,
    "value": 67234.50
  }
}
```

## Supported Symbols

### Binance Source Symbols

The Binance source supports various cryptocurrency trading pairs using lowercase concatenated format:

* `btcusdt` - Bitcoin to USDT
* `ethusdt` - Ethereum to USDT
* `solusdt` - Solana to USDT
* `xrpusdt` - XRP to USDT

### Chainlink Source Symbols

The Chainlink source supports cryptocurrency trading pairs using slash-separated format:

* `btc/usd` - Bitcoin to USD
* `eth/usd` - Ethereum to USD
* `sol/usd` - Solana to USD
* `xrp/usd` - XRP to USD

## Notes

### General

* Price updates are sent as market prices change
* The timestamp in the payload represents when the price was recorded
* The outer timestamp represents when the message was sent via WebSocket
* No authentication is required for crypto price data


# Real Time Data Socket
Source: https://docs.polymarket.com/developers/RTDS/RTDS-overview



## Overview

The Polymarket Real-Time Data Socket (RTDS) is a WebSocket-based streaming service that provides real-time updates for various Polymarket data streams. The service allows clients to subscribe to multiple data feeds simultaneously and receive live updates as events occur on the platform.

<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

### Connection Details

* **WebSocket URL**: `wss://ws-live-data.polymarket.com`
* **Protocol**: WebSocket
* **Data Format**: JSON

### Authentication

The RTDS supports two types of authentication depending on the subscription type:

1. **CLOB Authentication**: Required for certain trading-related subscriptions
   * `key`: API key
   * `secret`: API secret
   * `passphrase`: API passphrase

2. **Gamma Authentication**: Required for user-specific data
   * `address`: User wallet address

### Connection Management

The WebSocket connection supports:

* **Dynamic Subscriptions**: Without disconnecting from the socket users can add, remove and modify topics and filters they are subscribed to.
* **Ping/Pong**: You should send PING messages (every 5 seconds ideally) to maintain connection

## Available Subscription Types

<Note>Although this connection technically supports additional activity and subscription types, they are not fully supported at this time. Users are free to use them but there may be some unexpected behavior.</Note>

The RTDS currently supports the following subscription types:

1. **[Crypto Prices](/developers/RTDS/RTDS-crypto-prices)** - Real-time cryptocurrency price updates
2. **[Comments](/developers/RTDS/RTDS-comments)** - Comment-related events including reactions

## Message Structure

All messages received from the WebSocket follow this structure:

```json  theme={null}
{
  "topic": "string",
  "type": "string", 
  "timestamp": "number",
  "payload": "object"
}
```

* `topic`: The subscription topic (e.g., "crypto\_prices", "comments", "activity")
* `type`: The message type/event (e.g., "update", "reaction\_created", "orders\_matched")
* `timestamp`: Unix timestamp in milliseconds
* `payload`: Event-specific data object

## Subscription Management

### Subscribe to Topics

To subscribe to data streams, send a JSON message with this structure:

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "topic_name",
      "type": "message_type",
      "filters": "optional_filter_string",
      "clob_auth": {
        "key": "api_key",
        "secret": "api_secret", 
        "passphrase": "api_passphrase"
      },
      "gamma_auth": {
        "address": "wallet_address"
      }
    }
  ]
}
```

### Unsubscribe from Topics

To unsubscribe from data streams, send a similar message with `"action": "unsubscribe"`.

## Error Handling

* Connection errors will trigger automatic reconnection attempts
* Invalid subscription messages may result in connection closure
* Authentication failures will prevent successful subscription to protected topics


# How to Fetch Markets
Source: https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide



<Tip>Both the getEvents and getMarkets are paginated. See [pagination section](#pagination) for details.</Tip>
This guide covers the three recommended approaches for fetching market data from the Gamma API, each optimized for different use cases.

## Overview

There are three main strategies for retrieving market data:

1. **By Slug** - Best for fetching specific individual markets or events
2. **By Tags** - Ideal for filtering markets by category or sport
3. **Via Events Endpoint** - Most efficient for retrieving all active markets

***

## 1. Fetch by Slug

**Use Case:** When you need to retrieve a specific market or event that you already know about.

Individual markets and events are best fetched using their unique slug identifier. The slug can be found directly in the Polymarket frontend URL.

### How to Extract the Slug

From any Polymarket URL, the slug is the path segment after `/event/` or `/market/`:

```
https://polymarket.com/event/fed-decision-in-october?tid=1758818660485
                            ↑
                  Slug: fed-decision-in-october
```

### API Endpoints

**For Events:** [GET /events/slug/{slug}](/api-reference/events/list-events)

**For Markets:** [GET /markets/slug/{slug}](/api-reference/markets/list-markets)

### Examples

```bash  theme={null}
curl "https://gamma-api.polymarket.com/events/slug/fed-decision-in-october"
```

***

## 2. Fetch by Tags

**Use Case:** When you want to filter markets by category, sport, or topic.

Tags provide a powerful way to categorize and filter markets. You can discover available tags and then use them to filter your market requests.

### Discover Available Tags

**General Tags:** [GET /tags](/api-reference/tags/list-tags)

**Sports Tags & Metadata:** [GET /sports](/api-reference/sports/get-sports-metadata-information)

The `/sports` endpoint returns comprehensive metadata for sports including tag IDs, images, resolution sources, and series information.

### Using Tags in Market Requests

Once you have tag IDs, you can use them with the `tag_id` parameter in both markets and events endpoints.

**Markets with Tags:** [GET /markets](/api-reference/markets/list-markets)

**Events with Tags:** [GET /events](/api-reference/events/list-events)

```bash  theme={null}
curl "https://gamma-api.polymarket.com/events?tag_id=100381&limit=1&closed=false"

```

### Additional Tag Filtering

You can also:

* Use `related_tags=true` to include related tag markets
* Exclude specific tags with `exclude_tag_id`

***

## 3. Fetch All Active Markets

**Use Case:** When you need to retrieve all available active markets, typically for broader analysis or market discovery.

The most efficient approach is to use the `/events` endpoint and work backwards, as events contain their associated markets.

**Events Endpoint:** [GET /events](/api-reference/events/list-events)

**Markets Endpoint:** [GET /markets](/api-reference/markets/list-markets)

### Key Parameters

* `order=id` - Order by event ID
* `ascending=false` - Get newest events first
* `closed=false` - Only active markets
* `limit` - Control response size
* `offset` - For pagination

### Examples

```bash  theme={null}
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=100"
```

This approach gives you all active markets ordered from newest to oldest, allowing you to systematically process all available trading opportunities.

### Pagination

For large datasets, use pagination with `limit` and `offset` parameters:

* `limit=50` - Return 50 results per page
* `offset=0` - Start from the beginning (increment by limit for subsequent pages)

**Pagination Examples:**

```bash  theme={null}
# Page 1: First 50 results (offset=0)
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=0"
```

```bash  theme={null}
# Page 2: Next 50 results (offset=50)
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=50"
```

```bash  theme={null}
# Page 3: Next 50 results (offset=100)
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=100"
```

```bash  theme={null}
# Paginating through markets with tag filtering
curl "https://gamma-api.polymarket.com/markets?tag_id=100381&closed=false&limit=25&offset=0"
```

```bash  theme={null}
# Next page of markets with tag filtering
curl "https://gamma-api.polymarket.com/markets?tag_id=100381&closed=false&limit=25&offset=25"
```

***

## Best Practices

1. **For Individual Markets:** Always use the slug method for best performance
2. **For Category Browsing:** Use tag filtering to reduce API calls
3. **For Complete Market Discovery:** Use the events endpoint with pagination
4. **Always Include `closed=false`:** Unless you specifically need historical data
5. **Implement Rate Limiting:** Respect API limits for production applications

## Related Endpoints

* [Get Markets](/developers/gamma-markets-api/get-markets) - Full markets endpoint documentation
* [Get Events](/developers/gamma-markets-api/get-events) - Full events endpoint documentation
* [Search Markets](/developers/gamma-markets-api/get-public-search) - Search functionality


# Gamma Structure
Source: https://docs.polymarket.com/developers/gamma-markets-api/gamma-structure



Gamma provides some organizational models. These include events, and markets. The most fundamental element is always markets and the other models simply provide additional organization.

# Detail

1. **Market**
   1. Contains data related to a market that is traded on. Maps onto a pair of clob token ids, a market address, a question id and a condition id

2. **Event**
   1. Contains a set of markets
   2. Variants:
      1. Event with 1 market (i.e., resulting in an SMP)
      2. Event with 2 or more markets (i.e., resulting in an GMP)

# Example

* **\[Event]** Where will Barron Trump attend College?
  * **\[Market]** Will Barron attend Georgetown?
  * **\[Market]** Will Barron attend NYU?
  * **\[Market]** Will Barron attend UPenn?
  * **\[Market]** Will Barron attend Harvard?
  * **\[Market]** Will Barron attend another college?


# null
Source: https://docs.polymarket.com/developers/gamma-markets-api/overview



All market data necessary for market resolution is available on-chain (ie ancillaryData in UMA 00 request), but Polymarket also provides a hosted service, Gamma, that indexes this data and provides additional market metadata (ie categorization, indexed volume, etc). This service is made available through a REST API. For public users, this resource read only and can be used to fetch useful information about markets for things like non-profit research projects, alternative trading interfaces, automated trading systems etc.

# Endpoint

[https://gamma-api.polymarket.com](https://gamma-api.polymarket.com)


# Overview
Source: https://docs.polymarket.com/developers/neg-risk/overview



Certain events which meet the criteria of being "winner-take-all" may be deployed as **"negative risk"** events/markets. The Gamma API includes a boolean field on events, `negRisk`, which indicates whether the event is negative risk.

Negative risk allows for increased capital efficiency by relating all markets within events via a convert action. More explicitly, a NO share in any market can be converted into 1 YES share in all other markets. Converts can be exercised via the [Negative Adapter](https://polygonscan.com/address/0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296). You can read more about negative risk [here](https://github.com/Polymarket/neg-risk-ctf-adapter).

***

## Augmented Negative Risk

There is a known issue with the negative risk architecture which is that the outcome universe must be complete before conversions are made or otherwise conversion will “cost” something. In most cases, the outcome universe can be made complete by deploying all the named outcomes and then an “other” option. But in some cases this is undesirable as new outcomes can come out of nowhere and you'd rather them be directly named versus grouped together in an “other”.

To fix this, some markets use a system of **"augmented negative risk"**, where named outcomes, a collection of unnamed outcomes, and an *other* is deployed. When a new outcome needs to be added, an unnamed outcome can be clarified to be the new outcome via the bulletin board. This means the “other” in the case of augmented negative risk can effectively change definitions (outcomes can be taken out of it).

As such, trading should only happen on the named outcomes, and the other outcomes should be ignored until they are named or until resolution occurs. The Polymarket UI will not show unnamed outcomes.

If a market becomes resolvable and the correct outcome is not named (originally or via placeholder clarification), it should resolve to the *“other”* outcome. An event can be considered “augmented negative risk” when `enableNegRisk` is true **AND** `negRiskAugmented` is true.

The naming conventions are as follows:

### Original Outcomes

* Outcome A
* Outcome B
* ...

### Placeholder Outcomes

* Person A -> can be clarified to a named outcome
* Person B -> can be clarified to a named outcome
* ...

### Explicit Other

* Other -> not meant to be traded as the definition of this changes as placeholder outcomes are clarified to named outcomes


# null
Source: https://docs.polymarket.com/developers/proxy-wallet



## Overview

When a user first uses Polymarket.com to trade they are prompted to create a wallet. When they do this, a 1 of 1 multisig is deployed to Polygon which is controlled/owned by the accessing EOA (either MetaMask wallet or MagicLink wallet). This proxy wallet is where all the user's positions (ERC1155) and USDC (ERC20) are held.

Using proxy wallets allows Polymarket to provide an improved UX where multi-step transactions can be executed atomically and transactions can be relayed by relayers on the gas station network. If you are a developer looking to programmatically access positions you accumulated via the Polymarket.com interface, you can either continue using the smart contract wallet by executing transactions through it from the owner account, or you can transfer these assets to a new address using the owner account.

***

## Deployments

Each user has their own proxy wallet (and thus proxy wallet address) but the factories are available at the following deployed addresses on the **Polygon network**:

| **Address**                                                                                                              | **Details**                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [0xaacfeea03eb1561c4e67d661e40682bd20e3541b](https://polygonscan.com/address/0xaacfeea03eb1561c4e67d661e40682bd20e3541b) | **Gnosis safe factory** – Gnosis safes are used for all MetaMask users                            |
| [0xaB45c54AB0c941a2F231C04C3f49182e1A254052](https://polygonscan.com/address/0xaB45c54AB0c941a2F231C04C3f49182e1A254052) | **Polymarket proxy factory** – Polymarket custom proxy contracts are used for all MagicLink users |


# Resolution
Source: https://docs.polymarket.com/developers/resolution/UMA



# UMA Optimistic Oracle Integration

## Overview

Polymarket leverages UMA's Optimistic Oracle (OO) to resolve arbitrary questions, permissionlessly. From [UMA's docs](https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work):

"UMA's Optimistic Oracle allows contracts to quickly request and receive data information ... The Optimistic Oracle acts as a generalized escalation game between contracts that initiate a price request and UMA's dispute resolution system known as the Data Verification Mechanism (DVM). Prices proposed by the Optimistic Oracle will not be sent to the DVM unless it is disputed. If a dispute is raised, a request is sent to the DVM. All contracts built on UMA use the DVM as a backstop to resolve disputes. Disputes sent to the DVM will be resolved within a few days -- after UMA tokenholders vote on what the correct outcome should have been."

To allow CTF markets to be resolved via the OO, Polymarket developed a custom adapter contract called `UmaCtfAdapter` that provides a way for the two contract systems to interface.

## Clarifications

Recent versions (v2+) of the `UmaCtfAdapter` also include a bulletin board feature that allows market creators to issue "clarifications". Questions that allow updates will include the sentence in their ancillary data:

"Updates made by the question creator via the bulletin board on 0x6A5D0222186C0FceA7547534cC13c3CFd9b7b6A4F74 should be considered. In summary, clarifications that do not impact the question's intent should be considered."

Where the [transaction](https://polygonscan.com/tx/0xa14f01b115c4913624fc3f508f960f4dea252758e73c28f5f07f8e19d7bca066) reference outlining what outlining should be considered.

## Resolution Process

### Actions

* **Initiate** - Binary CTF markets are initialized via the `UmaCtfAdapter`'s `initialize()` function. This stores the question parameters on the contract, prepares the CTF and requests a price for a question from the OO. It returns a `questionID` that is also used to reference on the `UmaCtfAdapter`. The caller provides:
  1. `ancillaryData` - data used to resolve a question (i.e the question + clarifications)
  2. `rewardToken` - ERC20 token address used for payment of rewards and fees
  3. `reward` - Reward amount offered to a successful proposer. The caller must have set allowance so that the contract can pull this reward in.
  4. `proposalBond` - Bond required to be posted by OO proposers/disputers. If 0, the default OO bond is used.
  5. `liveness` - UMA liveness period in seconds. If 0, the default liveness period is used.

* **Propose Price** - Anyone can then propose a price to the question on the OO. To do this they must post the `proposalBond`. The liveness period begins after a price is proposed.

* **Dispute** - Anyone that disagrees with the proposed price has the opportunity to dispute the price by posting a counter bond via the OO, this proposed will now be escalated to the DVM for a voter-wide vote.

### Possible Flows

When the first proposed price is disputed for a `questionID` on the adapter, a callback is made and posted as the reward for this new proposal. This means a second `questionID`, making a new `questionID` to the OO (the reward is returned before the callback is made and posted as the reward for this new proposal). This allows for a second round of resolution, and correspondingly a second dispute is required for it to go to the DVM. The thinking behind this is to doubles the cost of a potential griefing vector (two disputes are required just one) and also allows far-fetched (incorrect) first price proposals to not delay the resolution. As such there are two possible flows:

* **Initialize (CTFAdapter) -> Propose (OO) -> Resolve (CTFAdapter)**
* **Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) -> Resolve (CTFAdaptor)**
* **Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) -> Challenge (CtfAdapter) -> Resolve (CTFAdaptor)**

## Deployed Addresses

### v3.0

| Network         | Address                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Polygon Mainnet | [0x2F5e3684cb1F318ec51b00Edba38d79Ac2c0aA9d](https://polygonscan.com/address/0x2F5e3684cb1F318ec51b00Edba38d79Ac2c0aA9d) |

### v2.0

| Network         | Address                                                                                                                     |
| --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Polygon Mainnet | [0x6A9D0222186C0FceA7547534cC13c3CFd9b7b6A4F74](https://polygonscan.com/address/0x6A9D222616C90FcA5754cd1333cFD9b7fb6a4F74) |

### v1.0

| Network         | Address                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Polygon Mainnet | [0xC8B122858a4EF82C2d4eE2E6A276C719e692995130](https://polygonscan.com/address/0xCB1822859cEF82Cd2Eb4E6276C7916e692995130) |

## Additional Resources

* [Audit](https://github.com/Polymarket/uma-ctf-adapter/blob/main/audit/Polymarket_UMA_Optimistic_Oracle_Adapter_Audit.pdf)
* [Source Code](https://github.com/Polymarket/uma-ctf-adapter)
* [UMA Documentation](https://docs.uma.xyz/)
* [UMA Oracle Portal](https://oracle.uma.xyz/)


# Liquidity Rewards
Source: https://docs.polymarket.com/developers/rewards/overview

Polymarket provides incentives aimed at catalyzing the supply and demand side of the marketplace. Specifically there is a public liquidity rewards program as well as one-off public pnl/volume competitions.

## Overview

By posting resting limit orders, liquidity providers (makers) are automatically eligible for Polymarket's incentive program. The overall goal of this program is to catalyze a healthy, liquid marketplace. We can further define this as creating incentives that:

* Catalyze liquidity across all markets
* Encourage liquidity throughout a market's entire lifecycle
* Motivate passive, balanced quoting tight to a market's mid-point
* Encourages trading activity
* Discourages blatantly exploitative behaviors

This program is heavily inspired by dYdX's liquidity provider rewards which you can read more about [here](https://www.dydx.foundation/blog/liquidity-provider-rewards). In fact, the incentive methodology is essentially a copy of dYdX's successful methodology but with some adjustments including specific adaptations for binary contract markets with distinct books, no staking mechanic a slightly modified order utility-relative depth function and reward amounts isolated per market. Rewards are distributed directly to the maker's addresses daily at midnight UTC.

## Methodology

Polymarket liquidity providers will be rewarded based on a formula that rewards participation in markets (complementary consideration!), boosts two-sided depth (single-sided orders still score), and spread (vs. mid-market, adjusted for the size cutoff!). Each market still configure a max spread and min size cutoff within which orders are considered the average of rewards earned is determined by the relative share of each participant's Q<sub>n</sub> in market m.

| Variable       | Description                                                      |
| -------------- | ---------------------------------------------------------------- |
| \$             | order position scoring function                                  |
| v              | max spread from midpoint (in cents)                              |
| s              | spread from size-cutoff-adjusted midpoint                        |
| b              | in-game multiplier                                               |
| m              | market                                                           |
| m'             | market complement (i.e NO if m = YES)                            |
| n              | trader index                                                     |
| u              | sample index                                                     |
| c              | scaling factor (currently 3.0 on all markets)                    |
| Q<sub>ne</sub> | point total for book one for a sample                            |
| Q<sub>no</sub> | point total for book two for a sample                            |
| Spread%        | distance from midpoint (bps or relative) for order n in market m |
| BidSize        | share-denominated quantity of bid                                |
| AskSize        | share-denominated quantity of ask                                |

## Equations

**Equation 1:**

$S(v,s)= (\frac{v-s}{v})^2 \cdot b$

**Equation 2:**

$Q_{one}= S(v,Spread_{m_1}) \cdot BidSize_{m_1} + S(v,Spread_{m_2}) \cdot BidSize_{m_2} + \dots $
$ + S(v, Spread_{m^\prime_1}) \cdot AskSize_{m^\prime_1} + S(v, Spread_{m^\prime_2}) \cdot AskSize_{m^\prime_2}$

**Equation 3:**

$Q_{two}= S(v,Spread_{m_1}) \cdot AskSize_{m_1} + S(v,Spread_{m_2}) \cdot AskSize_{m_2} + \dots $
$ + S(v, Spread_{m^\prime_1}) \cdot BidSize_{m^\prime_1} + S(v, Spread_{m^\prime_2}) \cdot BidSize_{m^\prime_2}$

**Equation 4:**

**Equation 4a:**

If midpoint is in range \[0.10,0.90] allow single sided liq to score:

$Q_{\min} = \max(\min({Q_{one}, Q_{two}}), \max(Q_{one}/c, Q_{two}/c))$

**Equation 4b:**

If midpoint is in either range \[0,0.10) or (.90,1.0] require liq to be double sided to score:

$Q_{\min} = \min({Q_{one}, Q_{two}})$

**Equation 5:**

$Q_{normal} = \frac{Q_{min}}{\sum_{n=1}^{N}{(Q_{min})_n}}$

**Equation 6:**

$Q_{epoch} = \sum_{u=1}^{10,080}{(Q_{normal})_u}$

**Equation 7:**

$Q_{final}=\frac{Q_{epoch}}{\sum_{n=1}^{N}{(Q_{epoch})_n}}$

## Steps

1. Quadratic scoring rule for an order based on position between the adjusted midpoint and the minimum qualifying spread

2. Calculate first market side score. Assume a trader has the following open orders:

   * 100Q bid on m @0.49 (adjusted midpoint is 0.50 then spread of this order is 0.01 or 1c)
   * 200Q bid on m @0.48
   * 100Q ask on m' @0.51

   and assume an adjusted market midpoint of 0.50 and maxSpread config of 3c for both m and m'. Then the trader's score is:

   $$
   Q_{ne} = \left( \frac{(3-1)}{3} \right)^2 \cdot 100 + \left( \frac{(3-2)}{3} \right)^2 \cdot 200 + \left( \frac{(3-1)}{3} \right)^2 \cdot 100
   $$

   $Q_{ne}$ is calculated every minute using random sampling

3. Calculate second market side score. Assume a trader has the following open orders:

   * 100Q bid on m @0.485
   * 100Q bid on m' @0.48
   * 200Q ask on m' @0.505

   and assume an adjusted market midpoint of 0.50 and maxSpread config of 3c for both m and m'. Then the trader's score is:

   $$
   Q_{no} = \left( \frac{(3-1.5)}{3} \right)^2 \cdot 100 + \left( \frac{(3-2)}{3} \right)^2 \cdot 100 + \left( \frac{(3-.5)}{3} \right)^2 \cdot 200
   $$

   $Q_{no}$ is calculated every minute using random sampling

4. Boosts 2-sided liquidity by taking the minimum of $Q_{ne}$ and $Q_{no}$, and rewards 1-side liquidity at a reduced rate (divided by c)

   Calculated every minute

5. $Q_{normal}$ is the $Q_{min}$ of a market maker divided by the sum of all the $Q_{min}$ of other market makers in a given sample

6. $Q_{epoch}$ is the sum of all $Q_{normal}$ for a trader in a given epoch

7. $Q_{final}$ normalizes $Q_{epoch}$ by dividing it by the sum of all other market maker's $Q_{epoch}$ in a given epoch this value is multiplied by the rewards available for the market to get a trader's reward

<Tip>Both min\_incentive\_size and max\_incentive\_spread can be fetched alongside full market objects via both the CLOB API and Markets API. Reward allocations for an epoch can be fetched via the Markets API. </Tip>


# null
Source: https://docs.polymarket.com/developers/subgraph/overview



## Subgraph Overview

Polymarket has written and open sourced a subgraph that provides, via a GraphQL query interface, useful aggregate calculations and event indexing for things like volume, user position, market and liquidity data. The subgraph updates in real time to be able to be mixed, and match core data from the primary Polymarket interface, providing positional data, activity history and more. The subgraph can be hosted by anyone but is also hosted and made publicly available by a 3rd party provider, Goldsky.

## Source

The Polymarket subgraph is entirely open source and can be found on the Polymarket Github.

**[Subgraph Github Repository](https://github.com/Polymarket/polymarket-subgraph)**

> Note: The available models/schemas can be found in the `schema.graphql` file.

## Hosted Version

The subgraphs are hosted on goldsky, each with an accompanying GraphQL playground:

* Orders subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn)

* Positions subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/positions-subgraph/0.0.7/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/positions-subgraph/0.0.7/gn)

* Activity subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/activity-subgraph/0.0.4/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/activity-subgraph/0.0.4/gn)

* Open Interest subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/oi-subgraph/0.0.6/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/oi-subgraph/0.0.6/gn)

* PNL subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn)


# Does Polymarket have an API?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/does-polymarket-have-an-api

Getting data from Polymarket

Yes! Developers can find all the information they need for interacting with Polymarket. This includes [documentation on market discovery, resolution, trading etc.](/quickstart/introduction/main)

Whether you are an academic researcher a market maker or an indepedent developer, this documentation should provide you what you need to get started. All the code you find linked here and on our [GitHub](https://github.com/polymarket) is open source and free to use.

<Tip>
  If you have any questions please join our [Discord](https://discord.com/invite/polymarket) and direct your questions to the #devs channel.
</Tip>


# How To Use Embeds
Source: https://docs.polymarket.com/polymarket-learn/FAQ/embeds

Adding market embeds to your Substack or website.

Polymarket allows you to embed a live-updating widget displaying the latest odds for markets in many places around the web.

### Web

Navigate to the individual market you want to embed and click the embed (\< >) link.

Select light or dark mode, and copy the auto-generated code
Paste the code into your code editor or CMS and publish as normal

### Twitter / X

Navigate to any Polymarket market
Copy the URL from your browser
Paste the URL into the compose window

### Substack

<Note>The embeds feature currently supports single markets only (eg “USA to Win Most Gold Medals”, not “Most Gold Medals at Paris Olympics’) </Note>

To embed a market, navigate on Polymarket.com to the single market you want to embed and click “copy link.”

Navigate to your Substack editor and paste the link directly into the body of your newsletter. The editor will recognize the market and convert it to a widget that automatically refreshes with the latest odds.


# How Do I Export My Key?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/how-to-export-private-key

Exporting your private key on Magic.Link

Exporting your private key gives you direct control and security over your funds. This process is applicable if you’ve signed up via email.

<Warning>
  **DO NOT** share your private key with other parties, platforms, or people. We will never ask for your private key.
</Warning>

1. Access the Export Link while signed into Polymarket: [https://reveal.magic.link/polymarket](https://reveal.magic.link/polymarket)

2. Sign-in on Magic.Link

3. Export Private Key. Once revealed, you should securely store the private key displayed, where others can’t access it.

4. Log out of Magic.Link


# Is My Money Safe?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/is-my-money-safe

Yes. Polymarket is non-custodial, so you're in control of your funds.

#### Non-custodial, you’re in control

Polymarket recognizes the importance of a trustworthy environment for managing your funds. To ensure this, Polymarket uses non-custodial wallets, meaning we never take possession of your USDC. This approach gives you full control over your assets, providing protection against potential security threats like hacks, misuse, and unauthorized transactions.

### Your keys = your funds

A private key acts like a highly secure password, essential for managing and moving your assets without restrictions. You can export your private key at any time, ensuring sole access to your funds. Learn how to export your private key [here](../FAQ/how-to-export-private-key/).

### Keep your private keys private.

**Do not share your private key with others**. While Polymarket provides the infrastructure, the security of your assets depends on how securely you handle your private key and passwords. Losing your private key or passwords can result in losing access to your funds. It's crucial to store this information in a safe and secure environment.

### Our Commitment

Polymarket aims to give you peace of mind, knowing that your assets are safe and fully under your control at all times. We encourage you to take necessary precautions to secure your digital assets effectively. The ability to manage your private key means you are not reliant on Polymarket to secure your assets; you have the control to ensure your financial security.


# Is Polymarket The House?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/is-polymarket-the-house

No, Polymarket is not the house. All trades happen peer-to-peer (p2p).

## Polymarket is different in three ways:

### 1. Traders interact directly with each other, not with Polymarket.

Polymarket is a marketplace comprised of traders on both sides of any given market. This means you're always trading with other users, not against a centralized entity or "house." Prices on Polymarket are determined by supply and demand. As traders buy and sell shares in outcomes, prices fluctuate to reflect the collective sentiment and knowledge of market participants.

### 2. Polymarket does not charge trading fees.

Unlike bookmakers or wagering operations, Polymarket does not charge deposit/withdrawal fees, or any type of trading fees. This means that Polymarket does not stand to benefit from the outcome of any market or usage of any trader.

### 3. Transact at any time.

Polymarket enables you to sell your position at any time before the market resolves, provided there is a willing buyer of your shares. This offers flexibility and allows you to manage your risk and lock in profits or cut losses as you see fit.

In essence, Polymarket empowers you to trade based on your own knowledge and research, without going up against a "house" with potentially unfair advantages.


# Polymarket vs. Polling
Source: https://docs.polymarket.com/polymarket-learn/FAQ/polling

How is Polymarket better than traditional / legacy polling?

While legacy polls capture a snapshot of opinion at a specific moment, they are often outdated by the time they're published—sometimes lagging by several days. In contrast, Polymarket reflects real-time sentiment as events unfold, offering continuous updates and a more dynamic understanding of public opinion.

Studies show that prediction markets like Polymarket tend to outperform traditional pollsters because participants are financially incentivized to be correct. This creates more thoughtful, data-driven predictions. Research by James Surowiecki, author of The Wisdom of Crowds, has highlighted how markets like these can be more accurate than polls due to the "collective intelligence" of diverse participants. Additionally, the Iowa Electronic Markets, an academic research project at the University of Iowa, has consistently demonstrated the superior accuracy of prediction markets like Polymarket over traditional polling in predicting political outcomes.

Polymarket provides a constantly updating picture of public sentiment, offering a degree of accuracy and timeliness that traditional pollsters, who typically report data that is days old, simply cannot match.


# Recover Missing Deposit
Source: https://docs.polymarket.com/polymarket-learn/FAQ/recover-missing-deposit

If you deposited the wrong cryptocurrency on Ethereum or Polygon, use these tools to recover those funds.

### Recover on Ethereum

<Note>Use this tool if you deposited the wrong token on Ethereum.</Note>

1. Go to [https://recovery.polymarket.com/](https://recovery.polymarket.com/) and sign in with your Polymarket account or connect the wallet you use on Polymarket.

2. Select the asset you incorrectly deposited.

3. You’ll then see the asset balance displayed, and will have the ability to recover those funds to your specified wallet.

### Recover on Polygon

<Note>Use this tool if you deposited the wrong token on Polygon.</Note>

1. Go to [https://matic-recovery.polymarket.com/](https://matic-recovery.polymarket.com/) and sign in with your Polymarket account or connect the wallet you use on Polymarket.

2. Select the asset you incorrectly deposited.

3. You’ll then see the asset balance displayed, and will have the ability to recover those funds to your specified wallet.


# Can I Sell Early?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/sell-early



**Yes, you can sell or close your position early.**

You may sell shares at any point before the market is resolved by either placing a market order to sell shares at the prevailing bid price in the orderbook, or by placing a limit order for how many shares you wish to sell and at what price.

The limit order will only be executed if/when there is a willing buyer for your shares at the price you set.


# How Do I Contact Support?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/support

Polymarket offers technical support through our website chat feature, and through Discord.

To contact support through our website:

* Navigate to [Polymarket](https://polymarket.com).

* Click the blue chat icon in the bottom right and start your chat session.

For technical support on Discord:

* Join the [Polymarket Discord server](https://discord.gg/polymarket)

* Navigate to the Support sidebar and click #open-a-ticket. This will open a private conversation with a Polymarket team member.

<Warning>
  Be aware of numerous scams and malicious links. Polymarket team members will never DM you first or ask for private keys or personal information. Polymarket team members are identified in blue font on Discord.
</Warning>


# Does Polymarket Have a Token?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/wen-token



**Polymarket does not have a token.**

All trading and liquidity rewards are in USDC, a USD-pegged stablecoin.

Polymarket has not announced plans for any airdrop or token generation event. Be wary of scams claiming airdrops, giveaways, etc.

If in doubt, refer to official Polymarket communication channels:

* Web: [https://polymarket.com](https://polymarket.com)
* Twitter / X: [https://x.com/polymarket](https://x.com/polymarket)
* Discord: [https://discord.gg/polymarket](https://discord.gg/polymarket)


# What is a Prediction Market?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/what-are-prediction-markets

How people collectively forecast the future.

A prediction market is a platform where people can bet on the outcome of future events. By buying and selling shares in the outcomes, participants collectively forecast the likelihood of events such as sports results, political elections, or entertainment awards.

### How it works

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


# Why Crypto?
Source: https://docs.polymarket.com/polymarket-learn/FAQ/why-do-i-need-crypto

Why Polymarket uses crypto and blockchain technology to create the world’s largest Prediction market.

Polymarket operates on Polygon, a proof-of-stake layer two blockchain built on [Ethereum](https://ethereum.org). All transactions are denominated in USDC, a US-dollar pegged stablecoin.

This architecture offers several advantages over traditional prediction markets:

## Why USDC?

### Stable Value

Polymarket denominates trades in USDC, which is pegged 1:1 to the US Dollar. This shields you from the volatility associated with other cryptocurrencies and offers a stable medium for trading.

### Regulated Reserves

USDC operates in adherence to regulatory standards and is backed by reserved assets.

### Transparency

Blockchain technology facilitates transparency, as all transactions are recorded publicly.

### Global Reach

Research has shown that wide availability of prediction markets increases their accuracy. Using decentralized blockchain technology removes the need for a central authority in trading, which fosters fairness and open participation around the globe.


# Deposit with Coinbase
Source: https://docs.polymarket.com/polymarket-learn/deposits/coinbase

How to buy and deposit USDC to your Polymarket account using Coinbase.

## Buying USDC

**How to buy and deposit USDC to your Polymarket account using Coinbase.**

Depositing directly to Polymarket from Coinbase is simple and easy. If you need help creating a Coinbase account, see their [guide on Coinbase.com](https://help.coinbase.com/en/coinbase/getting-started)

<iframe width="560" height="315" src="https://www.youtube.com/embed/IlDLdqT8RjU?si=v8iHe20FNqob_Cgr" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

<Steps>
  <Steps.Step>
    Login to <ExternalLink href="https://coinbase.com">Coinbase</ExternalLink>, and click "**Transfer**"
  </Steps.Step>

  <Steps.Step>
    Select "Deposit Cash" > "Deposit USDC"
  </Steps.Step>

  <Steps.Step>
    Enter the amount you wish to deposit, and connect a payment method under "**Transfer from**"
  </Steps.Step>

  <Steps.Step>
    Click **Preview**, review the Order Preview, then click **Deposit cash now**.
  </Steps.Step>

  <Steps.Step>
    You'll see a **“Your deposit is pending”** screen. You'll receive a confirmation email from Coinbase when your USDC purchase is successful.
  </Steps.Step>
</Steps>

If something went wrong along the way, we recommend reaching to Coinbase support.

## Transfering to Polymarket

<VideoPlayer src="https://www.youtube.com/embed/O6HaKdE9d80?si=NwuCGTzcilUhVQwg" />

<Steps>
  <Steps.Step>
    Copy your Polymarket USDC (Polygon) wallet address, as shown in your <ExternalLink href="https://polymarket.com/wallet">Polymarket wallet</ExternalLink>.

    *Ensure you have copied your address for the Polygon network, as depicted below*

    <Frame>
      <ExternalLink href="https://polymarket.com/wallet">
        <img className="hidden h-32 dark:block" src="https://polymarket-upload.s3.us-east-2.amazonaws.com/PolygonAddress-dark.png" />
      </ExternalLink>
    </Frame>
  </Steps.Step>

  <Steps.Step>
    Login to <ExternalLink href="https://coinbase.com">Coinbase</ExternalLink>, and select "Transfer" > "Send Crypto"
  </Steps.Step>

  <Steps.Step>
    Select USDC as the sending asset (note: you may have to search for it), and enter the amount you wish to send (deposit) to Polymarket.
  </Steps.Step>

  <Steps.Step>
    Under **To**, enter your Polymarket deposit address you copied from your <ExternalLink href="https://polymarket.com/wallet">Polymarket wallet</ExternalLink>.
  </Steps.Step>

  <Steps.Step>
    Under **Network**, select Polygon.
  </Steps.Step>

  <Steps.Step>
    Click **Send Now**. Your deposit will be available to trade on Polymarket in a few minutes!
  </Steps.Step>

  <Steps.Step>
    Back on the Polymarket <ExternalLink href="https://polymarket.com/wallet">deposit page</ExternalLink>, click **"Confirm pending deposit"**.
  </Steps.Step>
</Steps>


# How to Withdraw
Source: https://docs.polymarket.com/polymarket-learn/deposits/how-to-withdraw

How to withdraw your cash balance from Polymarket.

Withdrawing from Polymarket is simple, instant, and free.

<Steps>
  <Steps.Step>
    Go to the Polymarket funds page and click on the **Withdraw** button.
  </Steps.Step>

  <Steps.Step>
    Enter the USDC address you wish to withdraw to. Make sure the address
    supports USDC on the Polygon network. Then, enter the amount you want to
    withdraw.
  </Steps.Step>

  <Steps.Step>
    Click **Withdraw**. Your funds will be transferred instantly.
  </Steps.Step>
</Steps>

<iframe width="560" height="315" src="https://www.youtube.com/embed/fAXn0LCPTgA?si=JsYilGM3h0jSNBZa" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

<Note>
  Note: When withdrawing USDC.e (bridged USDC) is swapped through the [Uniswap v3 pool](https://polygonscan.com/address/0xd36ec33c8bed5a9f7b6630855f1533455b98a418)
  for USDC (native) (the UI enforces less than 10bp difference in output
  amount). At times, this pool may be exhausted and for extremely large deposits
  there might not be enough liquidity. If you are having withdraw issues, try
  breaking your withdraw into smaller amounts or waiting for the pool to be
  rebalanced. Additionally, you can select to withdraw USDC.e directly which
  does not require any Uniswap liquidity; just be aware that some exchanges no
  longer allow USDC.e to be deposited directly.
</Note>


# Large Cross Chain Deposits
Source: https://docs.polymarket.com/polymarket-learn/deposits/large-cross-chain-deposits



**For deposits over \$50,000 we recommended to use bridges and ensure minimal fee's (slippage).**

## Recommended Bridges

* [DeBridge](https://app.debridge.finance/?inputChain=1\&outputChain=137\&inputCurrency=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48\&outputCurrency=0x3c499c542cef5e3811e1192ce70d8cc03d5c3359\&dlnMode=simple)
* [Across](https://app.across.to/bridge?)
* [Portal](https://portalbridge.com/)

For large deposits (>\$50,000) originating from a chain other than Polygon, we recommend using one of the aforementioned bridges. Ensure you bridge to your Polymarket USDC (Polygon) [deposit address](https://polymarket.com/wallet) (screenshot below). Please be mindful of potential slippage during the transaction.

<Warning>
  Polymarket is not affiliated with, responsible for, or makes any guarantees regarding any third-party bridge. Users are advised to review the Terms of Use or other relevant documentation for third-party bridges.
</Warning>

## Important Notes

You can deposit USDC or USDC.e to your Polymarket Polygon wallet.

If you deposit USDC (native), you will be prompted to "activate funds," which will swap this to USDC.e via the lowest fee Uniswap pool, ensuring slippage of less than 10 basis points (bps).

If you encounter any issues with the deposit process, please reach out to us on Discord for assistance.


# Deposit Using Your Card
Source: https://docs.polymarket.com/polymarket-learn/deposits/moonpay

Use MoonPay to deposit cash using your Visa, Mastercard, or bank account.

**Use MoonPay to deposit cash using your Visa, Mastercard, or bank account.**

Access MoonPay by clicking "Buy USDC" on the [Deposit Page](https://polymarket.com/wallet)

Check out [MoonPay's guide](https://support.moonpay.com/customers/docs/how-to-buy-cryptocurrency-with-moonpay) for further instructions.


# Deposit by Transfering Crypto
Source: https://docs.polymarket.com/polymarket-learn/deposits/supported-tokens

Learn what Tokens and Chains are supported for deposit.

## **How do I use Transfer Crypto?**

The feature was designed to be one of the simplest ways to transfer your tokens into a dApp.

<img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.comxd.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=b0bfcc917f51f03c422947be7abcc5fc" alt="polymarket.comxd.png" title="polymarket.comxd.png" className="mx-auto" style={{ width:"62%" }} data-og-width="760" width="760" data-og-height="1146" height="1146" data-path="images/polymarket.comxd.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.comxd.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=0558e8b116d4e7f8698f3ad49ebed3f1 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.comxd.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=610193ec185ccf3697a6fb153084cb9c 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.comxd.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=9c0375436b39cb88b23a68ff1660743f 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.comxd.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=218f394193340e8cb1dc63b996fac84d 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.comxd.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=7d11259b246b32b7214213a1f106a1fc 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.comxd.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=aa6adbb43af08d1f6e1a23e7556796a1 2500w" />

1. **Click on the Deposit button** and **select Transfer Crypto** as a source option
2. **Select which supported token and chain** your assets are on from the dropdown
   * Depending on your combination, this **may update the deposit address**
   * Only send **supported token-chain combinations**
     * Sending non-supported tokens may cause an irrecoverable loss
3. **Scan the QR code or copy the deposit address** and paste as the recipient in the withdrawal/transfer page of your exchange/wallet
   * This is where you'll specify how much crypto you're transferring
   * You **must send more than the minimum deposit** amount or the funds will not process
   * Always ensure to **double check the pasted address** versus that is shown on the widget to protect against clickjacking attempts
   * You can click on the **collapsible section at the bottom of the widget** for estimated price impact, slippage, delivery time, and our help guide
4. **Withdraw/transfer the tokens** from your exchange/wallet and wait until they're reflected on the dApp
   * You will receive notifications on the Fun widget as your withdraw/transfer processes and completes as shown below

<img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio1.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=43ea11c20e25e45584d3ab0f1c1f0b4c" alt="polymarket.com_portfolio 1.png" title="polymarket.com_portfolio 1.png" className="mx-auto" style={{ width:"78%" }} data-og-width="760" width="760" data-og-height="500" height="500" data-path="images/polymarket.com_portfolio1.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio1.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=c44d0ee9b9f51028693595529bfe1060 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio1.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=0de5f6543688d0429d04b7d60e15731f 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio1.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=812b954f39f91b932c546669b1fdae47 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio1.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=2587143a31ecc3f58f94a13c064fd05b 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio1.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=f09d6918697d145638c21d70bf66161f 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio1.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=dabc2b27d7408a0b606d07cbdcaefb93 2500w" />

<img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio2.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=91e6dfeb4bb5cdada8d9b62fef23f487" alt="polymarket.com_portfolio 2.png" title="polymarket.com_portfolio 2.png" className="mx-auto" style={{ width:"78%" }} data-og-width="760" width="760" data-og-height="499" height="499" data-path="images/polymarket.com_portfolio2.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio2.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=c5e94f023a2679e0d84e43ff61f5fcf4 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio2.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=8ded25ed35ceb8493e4469bce4b21740 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio2.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=bee694bf666c5d86b5d7aaede5798a48 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio2.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=17c84cae3c2fbd48e21a48c6e6f84634 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio2.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=e2d39c595a4b5a896c55e7cd71c871c9 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/polymarket.com_portfolio2.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=7696037ce611263ce4eb1be7bd4ba60e 2500w" />

## **What can I transfer?**

Transfer Crypto is compatible with a range of supported tokens and chains:

|            | **Ethereum** | **Polygon** | **Base** | **Arbitrum** | **Solana** |
| :--------- | :----------- | :---------- | :------- | :----------- | :--------- |
| **USDC**   | ✅            | ✅           | ✅        | ✅            | ✅          |
| **USDC.e** |              | ✅           |          |              |            |
| **USDT**   | ✅            | ✅           | ✅        | ✅            |            |
| **DAI**    | ✅            | ✅           | ✅        | ✅            |            |
| **ETH**    | ✅            |             | ✅        | ✅            |            |
| **WETH**   | ✅            | ✅           | ✅        | ✅            |            |
| **MATIC**  | ✅            | ✅           |          |              |            |
| **POL**    | ✅            | ✅           |          |              |            |
| **SOL**    |              |             |          |              | ✅          |
| **CBBTC**  | ✅            |             | ✅        |              |            |
| **ARB**    |              |             |          | ✅            |            |

## Need help with your deposit?

Please contact us using the live chat button on the bottom right on [**Polymarket.com**](http://Polymarket.com)\*\* or email us on [support@polymarket.com](mailto:support@polymarket.com)\*\*

<img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/imagee.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=e862c32062cd7b8a7198714241c162dd" alt="imagee.png" data-og-width="2556" width="2556" data-og-height="1304" height="1304" data-path="images/imagee.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/imagee.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=ec7b40dddf3c4de102b2106fe30934aa 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/imagee.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=ca51d6f87f78779815cfaf89422725af 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/imagee.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=cc2bf6d79868b05369f3133bd0ab7a57 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/imagee.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=b7a40ad1f76cd5d90875291ff948a4f0 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/imagee.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=ad31b6cbe24eb83e124df4e9f3cc78f7 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/images/imagee.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=9be6c9c4bd2f170b92d33e7bac08dbc4 2500w" />


# Deposit USDC on Ethereum
Source: https://docs.polymarket.com/polymarket-learn/deposits/usdc-on-eth

How to deposit USDC on the Ethereum Network to your Polymarket account.

<iframe width="560" height="315" src="https://www.youtube.com/embed/igx1J2ugFIg?si=gOBDPFnXZTLoRLGM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

Depositing USDC on the Ethereum network to Polymarket will automatically bridge your funds to the Polygon network.

<Steps>
  <Steps.Step>
    On the Polymarket deposit page, under “Other Methods,” click **USDC (ETH)**.
  </Steps.Step>

  <Steps.Step>
    Copy your unique USDC (ETH) deposit address.

    <Frame>
      <img className="hidden h-32 dark:block" src="https://polymarket-upload.s3.us-east-2.amazonaws.com/EthAddress-dark.png" />
    </Frame>
  </Steps.Step>

  <Steps.Step>
    Send your USDC to the address you just copied on the Ethereum network. This feature is typically called “send” or “withdraw” on most exchanges and wallets.

    <Note>
      Ensure you are sending USDC to your Polymarket Ethereum deposit address on
      Ethereum network to avoid any issues.
    </Note>
  </Steps.Step>

  <Steps.Step>
    Once your deposit is detected, a countdown timer will begin.
  </Steps.Step>

  <Steps.Step>
    You will see "Deposit Complete" when your funds are ready to trade.

    <Tip>
      If your countdown timer resets more than once, or if you encounter any issues,
      please reach out to support on
      [Discord](https://discord.com/invite/polymarket)
    </Tip>
  </Steps.Step>
</Steps>


# How to Deposit
Source: https://docs.polymarket.com/polymarket-learn/get-started/how-to-deposit

How to add cash to your balance on Polymarket.

## Depositing funds on Polymarket

This guide will walk you through the deposit process for Polymarket, covering popular methods and step-by-step instructions for buying and depositing USDC.

<Note>
  Need Help? For assistance, reach out to us on [Discord](https://discord.gg/polymarket).
</Note>

## About USDC and Polygon

Polymarket uses [USDC (USD Coin)](https://circle.com/en/usdc), a federally regulated "stable coin" backed by the US dollar.

Polymarket utilizes USDC on the Polygon network for transactions. By using USDC on Polygon, Polymarket ensures fast and reliable transactions, enhancing the overall user experience.

### How to purchase and deposit USDC

<iframe width="560" height="315" src="https://www.youtube.com/embed/IlDLdqT8RjU?si=2f0ze0d-SQznVP_N" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

USDC is available on most major exchanges, including Coinbase.

If your exchange supports sending or withdrawing to Polygon, we recommend this option for faster and fee-free transactions. Alternatively, you can deposit USDC via the Ethereum network.

### Deposit with crypto exchanges

For detailed instructions, check out our guides for purchasing and depositing USDC using popular exchanges:

* [Deposit from Coinbase](../deposits/coinbase) (recommended)

<Note>
  If you decide to use an exchange to purchase and send (deposit) USDC to your Polygon deposit address, please ensure you're sending on Polygon Network. If you're unsure, please reach out to support on [Discord](https://discord.com/invite/polymarket).
</Note>

### Deposit with Visa or Mastercard

MoonPay enables you to buy USDC (on Polygon) using your Visa, Mastercard, and select bank cards. Please be aware that payment options and transaction limits may vary depending on your region. [How to use MoonPay](../deposits/moonpay/).

### Depositing on Etheruem and Polygon

You can send USDC with your wallet on Ethereum or USDC.e on Polygon to your respective deposit addresses found on the Deposit page. [Learn more](../deposits/usdc-on-eth/).


# How to Sign-Up
Source: https://docs.polymarket.com/polymarket-learn/get-started/how-to-signup

How to create a Polymarket account.

<Tip>
  Need Help?
  We're available to guide you through the sign-up process on [Discord](https://discord.gg/polymarket)
</Tip>

### Email or Google Sign-Up

Signing up for Polymarket with your email address or Google account is quick, simple, and secure.

<Steps>
  <Steps.Step>
    Click **Sign Up** on the top right of the Polymarket homepage.
  </Steps.Step>

  <Steps.Step>
    Enter your email address and click **continue**.

    *You can also use your Google account to sign in and follow the same procedure.*
  </Steps.Step>

  <Steps.Step>
    **Copy the security code** provided by Magic.
  </Steps.Step>

  <Steps.Step>
    You’ll receive an email with the subject “Log in to Polymarket”. Open the email, and click the **Log in to Polymarket** button.

    In the new window, enter or **paste the security code** from the previous step.

    <Note>Note: This page will be hosted on auth.magic.link.</Note>

    You'll see a Login Complete message. Return to your original Polymarket window.
  </Steps.Step>

  <Steps.Step>
    Back on Polymarket, you'll be signed in. Choose your display name, agree to the terms of service, opt into email updates, and get started trading.
  </Steps.Step>
</Steps>

### Crypto Wallet Sign-Up

Polymarket supports most crypto wallets, including MetaMask, Coinbase Wallet, and others via WalletConnect.

<Steps>
  <Steps.Step>
    Click Sign Up on the Polymarket homepage.
  </Steps.Step>

  <Steps.Step>
    Choose your preferred wallet and follow the prompts to connect it to Polymarket. Ensure you are connected to the Polygon Network, your wallet may prompt you to switch networks.
  </Steps.Step>

  <Steps.Step>
    Sign the transaction prompt(s) on your wallet app or extension.
  </Steps.Step>

  <Steps.Step>
    You're signed in! Choose your display name, agree to the terms of service, opt into email updates, and start trading.
  </Steps.Step>
</Steps>

<Note>
  If you have MetaMask or Coinbase Wallet browser extensions installed but wish to connect using their mobile apps, you'll need to disable the extensions in your browser settings and reload Polymarket.
</Note>


# Making Your First Trade
Source: https://docs.polymarket.com/polymarket-learn/get-started/making-your-first-trade

How to buy shares.

Once you've [signed up](../get-started/how-to-signup) and [deposited funds](../get-started/how-to-deposit), you're ready to start trading on Polymarket. Here's a step-by-step guide to get you started.

## Video guide

<iframe width="560" height="315" src="https://www.youtube.com/embed/1lFgkHLqo28?si=i7e61-roRsOVeRMW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

## Walkthrough

Before trading, you'll have to visit the [markets page](https://polymarket.com/markets) to see all available markets. Use the search, sort, and filter tools to narrow down your options and find a market that interests you.
screen shot.

<Steps>
  <Steps.Step>
    ### Choose a Market

    Locate the 'buy' modal, on the right side of the screen. Click the outcome you want to buy (usually Yes or No), then enter the dollar amount you wish to invest.
  </Steps.Step>

  <Steps.Step>
    ### Buy Shares

    Click **Buy** and confirm the transaction in your wallet. Once your trade goes through, you'll receive a notification confirming its success.

    <Tip>Congrats, you're officially a Polymarket trader!</Tip>
  </Steps.Step>

  <Steps.Step>
    ### Share your trade

    You'll also see a bet slip to share on social media. We love sending \$\$\$ to traders who post their trades on Twitter and tag us!
  </Steps.Step>
</Steps>

Simple, right? If you think you've got the hang of it, it's time to learn about more advanced trading and order types. [Limit Orders](../trading/limit-orders/).


# What is Polymarket?
Source: https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket



Polymarket is the world’s largest prediction market, allowing you to stay informed and profit from your knowledge by betting on future events across various topics.

Studies show prediction markets are often more accurate than pundits because they combine news, polls, and expert opinions into a single value that represents the market's view of an event's odds. Our markets reflect *accurate, unbiased, and real-time probabilities* for the events that matter most to you. Markets seek truth.

## Quick Overview

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


# How Are Markets Disputed?
Source: https://docs.polymarket.com/polymarket-learn/markets/dispute



**Anyone can dispute a proposed market resolution if they feel it was proposed in error.**

Once a market is proposed for resolution it goes into a challenge period of 2 hours.

If no one challenges the proposal the resolution is deemed valid and the proposer receives their bond back plus the reward.

During the 2-hour challenge period, anyone may dispute the proposal on the [UMA dapp](https://oracle.uma.xyz/) by posting a challenge bond of the same amount as the proposer bond (usually \$750).

This begins the debate period of 24-48 hours (votes happen every other day and there will always be at least 24 hours for discussion). Anyone wishing to contribute evidence to the discussion can do so in the Uma Discord server in the #evidence-rationale and #voting-discussion channels.

After the debate period, Uma token holders vote (this process takes approximately 48 hours) and one of four outcomes happens:

## Outcomes

### Proposer wins

Proposer receives their bond back plus half the disputer’s bond as a bounty. Disputer loses their bond.

### Disputer wins

Disputer receives their bond back plus half the proposer’s bond as a bounty. Proposer loses their bond.

### Too Early

This outcome is for proposals for which the underlying event has not yet happened. Eg the result of a sports match that is still ongoing. Disputer receives their bond back plus half the proposer’s bond as a bounty. Proposer loses their bond.

### Unknown/50-50

This (rarely used) outcome is for events where none of the other options are appropriate. In this case the market price resolves to 50 yes and 50 no. Disputer receives their bond back plus half the proposer’s bond as a bounty. Proposer loses their bond.


# How Are Markets Clarified?
Source: https://docs.polymarket.com/polymarket-learn/markets/how-are-markets-clarified

How are markets on Polymarket clarified?

## Overview

* Markets are resolved according to the rules set forth on the market page.

* The rules specify the resolution source, the market end date, and they outline how the market should resolve in various edge-cases.

* The market title describes the market, but the rules define how it should be resolved.

<Important>It is important to read the rules before trading in a market. </Important>

<Frame>
  <img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/market-rules.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=22ee2dab424287bd8ffe4ee8017dff4e" data-og-width="1684" width="1684" data-og-height="1278" height="1278" data-path="polymarket-learn/markets/market-rules.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/market-rules.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=a18e693ed0ef40b937a20c2f016b9285 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/market-rules.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=55f60bb6f0fc6e73dbc79f4ddb89a48b 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/market-rules.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=fd54012529a854f0eaff03c2b8622923 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/market-rules.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=cee1310e052ddc361c2c5f05cb5af08d 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/market-rules.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=ddcac99c3515d39e8803420fe47c6263 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/market-rules.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=d78bcb523db705fe43cf95a9db20b1e0 2500w" />
</Frame>

***

## Clarifications

In rare cases, circumstances occur that were not foreseen at a market’s creation and it becomes necessary to clarify rules after trading has begun. In these cases Polymarket may issue an “Additional context” update to the rules.

<Tip>If you believe a clarification is necessary for a market, the best place to request a clarification is in the [Polymarket Discord](https://discord.com/invite/polymarket) **#market-review** channel.</Tip>

<Frame caption="An example clarification in the market on what Trump would say during Hannity Town Hall. ">
  <img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/additional-context.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=c541cfe17203de08a547da32d0995804" data-og-width="940" width="940" data-og-height="482" height="482" data-path="polymarket-learn/markets/additional-context.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/additional-context.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=189aff574aa25f6cc33a2aada719e7ee 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/additional-context.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=cc34b7c65289a0481c23d4f082410684 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/additional-context.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=251fd8aff678b616583d1997ce2bcfcf 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/additional-context.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=1b11238c8c08383cae76cee0b2747f73 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/additional-context.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=358861be6c10816b76e5dd56e3c446d1 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/markets/additional-context.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=1b556681e45977ceefadecd562a61360 2500w" />
</Frame>


# How Are Markets Created?
Source: https://docs.polymarket.com/polymarket-learn/markets/how-are-markets-created

Markets are created by the markets team with input from users and the community.

## Can I create my own market?

While users cannot directly create their own markets, they are encouraged to suggest ideas for new markets. In choosing which markets to list, Polymarket considers the following factors:

<Steps>
  <Steps.Step>
    Is there enough demand for trading in the market to produce an accurate probability? Polymarket targets \$X in trading volume as a minimum.
  </Steps.Step>

  <Steps.Step>
    Is there social good or news value in understanding the probability generated by the market?
  </Steps.Step>

  <Steps.Step>
    Can the market be resolved clearly?
  </Steps.Step>

  <Steps.Step>
    Is there a credible information source for market resolution?

    *For example, a country’s elections commission can be specified as the official resolution source for an election.*
  </Steps.Step>

  <Steps.Step>
    Can the market be resolved in a definitive time frame?
  </Steps.Step>
</Steps>

### Submit your market proposal

To give your proposal the best chance of being listed, include as much information as possible, such as:

* What is the market title?
* What is the [resolution source](../markets/how-are-markets-resolved)?
* Evidence of demand for trading that market

The best ways to propose a new market are:

* On [Discord](https://discord.com/invite/polymarket) in the **#market-suggestion** channel
* On Twitter / X by tagging [@polymarket](https://twitter.com/intent/tweet?text=I+have+an+idea+for+a+new+market+@polymarket)


# How Are Prediction Markets Resolved?
Source: https://docs.polymarket.com/polymarket-learn/markets/how-are-markets-resolved

Markets are resolved by the UMA Optimistic Oracle, a smart-contract based optimistic oracle.

## Overview

* When the result of a market becomes clear, the market can be “resolved,” or permanently finalized.

* Markets are resolved according to the market's pre-defined rules, which can be found under market's the order book.

* When a market is resolved, holders of winning shares receive \$1 per share, losing shares become worthless, and trading of shares is no longer possible.

* To resolve a market, an outcome must first be “proposed,” which involves putting up a bond in USDC.e which will be forfeited if the proposal is unsuccessful.

* If the proposal is validated as accurate, the proposer will receive a reward for your proposal.

<Warning>
  If you propose a market too early, or are unsuccessful in your proposal, you will lose all of your \$750 bond. Do not propose a resolution unless you understand the process and are confident in your view.
</Warning>

### To propose a market resolution

<Steps>
  <Steps.Step>
    Navigate to the market you want to propose and click Resolution > Propose Resolution.

    <Note>You will be taken to the corresponding UMA oracle page for the market, which shows the bond required and reward for successful proposal.</Note>
  </Steps.Step>

  <Steps.Step>
    Ensure that you have enough USDC.e in your wallet on Polygon to supply the bond (usually \$750)
  </Steps.Step>

  <Steps.Step>
    Select the outcome you would like to propose from the drop-down menu.
  </Steps.Step>

  <Steps.Step>
    Connect your wallet and submit the transaction. It will now enter the UMA Oracle’s verification queue.
  </Steps.Step>
</Steps>

Once in the verification process, UMA will review the transaction to ensure it was proposed correctly. If approved, you will receive your bond amount back in your wallet plus the reward. If not approved, it will enter Uma’s dispute resolution process, which is described in detail here.

### To dispute a proposed resolution

Once a market is proposed for resolution it goes into a challenge period of 2 hours.

If you do not agree with a proposed resolution, you can [dispute the outcome](../markets/dispute).


# Trading Fees
Source: https://docs.polymarket.com/polymarket-learn/trading/fees



**Polymarket does not charge any type of fee.**

There are no fees to deposit or withdraw USDC, although intermediaries such as Coinbase, MoonPay, etc may charge transaction fees.

There are no fees to trade shares in any market.


# Holding Rewards
Source: https://docs.polymarket.com/polymarket-learn/trading/holding-rewards



## What are we doing?

To keep long-term pricing accurate, we're paying 4.00% annualized Holding Reward based on your total position value in certain polymarkets. We anticipate rolling out a new reward and oracle-resolution system later this year — at which point there will be a simple 1-click migration.

## Reward Rate and Conditions

The current rate is set at 4.00% and applies to all eligible positions. This rate is variable and subject to change at Polymarket's discretion. We also reserve the right to introduce limits to the total amount of rewards paid out at any time. This iteration of rewards is funded through the Polymarket Treasury.

Your total position value is randomly sampled once each hour, and the reward is distributed daily. Your rewards are calculated based on the total position value of your eligible positions at the time of evaluation.

### **Total Position Value Computation**

For each eligible polymarket, we calculate the eligible position in the following way:

**Position Valuation**:

* Based on your current "Yes" and "No" shares and the most recent mid-price for each outcome.

### **Example**

If you hold at time of sample:

* 30,000 “Yes” shares at a price of **\$0.53**
* 10,000 “No” shares at a price of **\$0.45**

**Total Position Value** =

→ `(30000 × 0.53) + (10000 × 0.45)`

→ `$15,900 + $4,500 = $20,400`

**Hourly Holding Reward Calculation** (based on 4.00% Annual Reward):

→ `$20400 × (0.04 / 365 / 24) ≈ $.09315068493`

## Eligible Events:

* [Presidential Election Winner 2028](https://polymarket.com/event/presidential-election-winner-2028)
* [Republican Presidential Nominee 2028](https://polymarket.com/event/republican-presidential-nominee-2028)
* [Democratic Presidential Nominee 2028](https://polymarket.com/event/democratic-presidential-nominee-2028)
* [Which party wins 2028 US Presidential Election?](https://polymarket.com/event/which-party-wins-2028-us-presidential-election)
* [Balance of Power: 2026 Midterms](https://polymarket.com/event/balance-of-power-2026-midterms)
* [Which party will win the Senate in 2026?](https://polymarket.com/event/which-party-will-win-the-senate-in-2026)
* [Which party will win the House in 2026?](https://polymarket.com/event/which-party-will-win-the-house-in-2026)
* [Erdoğan out before 2027?](https://polymarket.com/event/erdoan-out-before-2027)
* [Zelenskyy out as Ukraine president before 2027?](https://polymarket.com/event/zelenskyy-out-as-ukraine-president-before-2027)
* [Netanyahu out before 2027?](https://polymarket.com/event/netanyahu-out-before-2027)
* [Xi Jinping out before 2027?](https://polymarket.com/event/xi-jinping-out-before-2027)
* [Putin out as President of Russia before 2027?](https://polymarket.com/event/putin-out-before-2027)
* [Russia x Ukraine ceasefire before 2027?](https://polymarket.com/event/russia-x-ukraine-ceasefire-before-2027)


# How Are Prices Calculated?
Source: https://docs.polymarket.com/polymarket-learn/trading/how-are-prices-calculated

The prices probabilities displayed on Polymarket are the midpoint of the bid-ask spread in the orderbook.

## Initial Price

* When a market is created, there are initially zero shares and no pre-defined prices or odds.

* Market makers (a fancy term for traders placing limit orders) interested in buying YES or NO shares can place [Limit Orders](../trading/limit-orders) at the price they're willing to pay

* When offers for the YES and NO side equal \$1.00, the order is "matched" and that \$1.00 is converted into 1 YES and 1 NO share, each going to their respective buyers.

For example, if you place a limit order at \$0.60 for YES, that order is matched when someone places a NO order at \$0.40. *This becomes the initial market price.*

<Important>Polymarket is not a "bookie" and does not set prices / odds. Prices are set by what Polymarket users are currently willling to buy/sell shares at. All trades are peer-to-peer.</Important>

## Future Price

The prices displayed on Polymarket are the midpoint of the bid-ask spread in the orderbook — unless that spread is over \$0.10, in which case the last traded price is used.

Like the stock market, prices on Polymarket are a function of realtime supply & demand.

<VideoPlayer src="https://www.youtube.com/embed/v0CvPEYBzTI?si=9cirMPQ72orQzLyS" />

### Prices = Probabilities

In the market below, the probability of 37% is the midpoint between the 34¢ bid and 40¢ ask. If the bid-ask spread is wider than 10¢, the probability is shown as the last traded price.

<Frame>
  <img className="block w-full h-auto dark:hidden" style={{ maxWidth: '100%', height: 'auto' }} noZoom src="https://polymarket-upload.s3.us-east-2.amazonaws.com/how_are_prices_calculated.png" />
</Frame>

<Note>You may not be able to buy shares at the displayed probability / price because there is a bid-ask spread. In the above example, a trader wanting to buy shares would pay 40¢ for up to 4,200 shares, after which the price would rise to 43¢.</Note>


# Limit Orders
Source: https://docs.polymarket.com/polymarket-learn/trading/limit-orders

What are limit orders and how to make them.

## Video guide

<iframe width="560" height="315" src="https://www.youtube.com/embed/_WfpoVGqzbw?si=yvuXC5i08Eik-PnR" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

## What are Limit Orders?

Limit orders are open orders (pending trades) that only execute when the market trades at your desired price.

For example, if the highest you’re willing to pay for a share of Trump “Yes” in the 2024 Republican Nomination is 72c, but the current market price is 73c, you could create a limit order at 72c and wait until someone is willing to sell Yes shares at your desired price.

<Note>
  It’s not necessary for the entire order to execute at once. Limit orders can ‘partially fill’ as individual traders fill parts of your order.
</Note>

<Steps>
  <Steps.Step>
    In the buy modal, select **limit** in the order type dropdown.
  </Steps.Step>

  <Steps.Step>
    Enter the price you are willing to buy (or sell, if you’ve selected to sell) shares at.
  </Steps.Step>

  <Steps.Step>
    Enter the number of shares you want to buy or sell at that price.

    *Optional: Set an expiration date for your limit order. This means that if the order does not execute at your desired price within this timeframe, it will be canceled.*
  </Steps.Step>

  <Steps.Step>
    Click **Buy** and confirm the transaction in your wallet.

    <Note>
      Your limited orders that have yet to be filled are called "Open Orders".
    </Note>
  </Steps.Step>

  <Steps.Step>
    You'll see a **“Your deposit is pending”** screen. You'll receive a confirmation email from Coinbase when your USDC purchase is successful.
  </Steps.Step>
</Steps>

## Managing limit orders

When you have an open order, you'll find it displayed just below the Order Book on the market's page.

If you have open orders across multiple markets, you can easily manage and monitor them all from the [Portfolio page](https://polymarket.com/portfolio?tab=Open+orders).

<Tip>
  Specifically for sports markets, any outstanding limit orders are automatically cancelled once the game begins, clearing the entire order book at the official start time. Be aware, game start times can shift so it’s important to always monitor your orders closely in case they are not cleared due to game changes or other circumstances. 
</Tip>

<Tip>
  Additionally, sports markets include a 3-second delay on the placement of marketable orders.
</Tip>

## Canceling limit orders

When you have an open order, you'll find it displayed just below the Order Book on the market's page.

To cancel the order, you can simply click the red **x** button alongside the order.

<iframe width="560" height="315" src="https://www.youtube.com/embed/KuA2UdUfZls?si=RUpuzqB9lbBB2pl9" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

If you have open orders across multiple markets, you can easily manage and monitor them all from the [Portfolio page](https://polymarket.com/portfolio?tab=Open+orders).

Nice! You can officially call yourself an advanced trader.

<Tip>
  If some of this still isn’t making sense, feel free to reach out to us on [Discord](https://discord.com/invite/polymarket). We’re happy to help get you up to speed.
</Tip>


# Liquidity Rewards
Source: https://docs.polymarket.com/polymarket-learn/trading/liquidity-rewards

Learn how to earn rewards merely by placing trades on Polymarket

With Polymarket's Liquidity Rewards Program, you can earn money by placing limit orders that help keep the market active and balanced.

## Overview

* The closer your orders are to the market's average price, the more you earn.

* The reward amount depends on how helpful your orders are in terms of size and pricing compared to others.

* The more competitive your limit orders, the more you can make.

* You get paid daily based on how much your orders add to the market, and can use our [Rewards page](https://polymarket.com/rewards) to check your current earnings for the day, which markets have rewards in place, as well as how much.

* The minimum reward payout is \$1; amounts below this will not be paid.

<Frame>
  <img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-earnings.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=ebcb693900b79d2c23356b0f087b5941" data-og-width="2000" width="2000" data-og-height="767" height="767" data-path="polymarket-learn/media/liquidity-rewards-earnings.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-earnings.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=9db6070985119ba1a50a442567f0aa60 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-earnings.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=0751971d6bdbf37e5b6199c75667b7df 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-earnings.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=f202b8060f23a9dfe979a984f6ff7dc2 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-earnings.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=85fca21bad31dda8a833de3c0ec3ffbf 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-earnings.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=a1ac5afea3e04a8223d135159792cfbc 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-earnings.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=85b91f7804be348fcea35ccc7981ae6e 2500w" />
</Frame>

Simply put, the more you help the market by placing good orders, the more rewards you earn!

## Seeing Rewards in the Order Book

### Viewing Rewards

The total rewards, max spread, and minimum shares required to earn rewards vary by market. You can view the rewards for a given market in its Order Book.

* On the Polymarket order book, you can hover over the Rewards text to see the amount of rewards available in total on each market.

* The blue highlighted lines correspond to the max spread — meaning the farthest distance your limit order can be from the midpoint of the market to earn rewards.

* In the example below, because the max spread is 3c, every order within 3c of the midpoint is eligible for rewards. If the midpoint is \< \$0.10, you need to have orders on both sides to qualify.

<Frame>
  <img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-market.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=12202bc1af31cdc1935ee816ca00f308" data-og-width="2000" width="2000" data-og-height="1367" height="1367" data-path="polymarket-learn/media/liquidity-rewards-market.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-market.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=b065f81168d3d5f9541857471a041427 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-market.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=35755273beea782b1bb20c11288afb74 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-market.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=75f37d73214985f85bdb5c98351a4654 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-market.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=7b14257457d28ae5209200328093439d 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-market.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=58d5ff89f7f9efe900bdb9602de7b9b1 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/liquidity-rewards-market.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=fa5269ee4ff8c40974c69024a89c2e90 2500w" />
</Frame>

### Earning Rewards

When your orders are earning rewards you’ll see a blue highlight around the clock icon, as shown below:

<Frame>
  <img src="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/earning-liquidity-rewards.png?fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=1a0c05e93f37c95c66b4ad67ff66c320" data-og-width="2000" width="2000" data-og-height="1631" height="1631" data-path="polymarket-learn/media/earning-liquidity-rewards.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/earning-liquidity-rewards.png?w=280&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=f8423304aac914fefae7361fc2d2c17e 280w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/earning-liquidity-rewards.png?w=560&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=69ee175aab44d11b54ca22e02769c7e7 560w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/earning-liquidity-rewards.png?w=840&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=53a591eb0724fcc6d1bc60ff57d54a4c 840w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/earning-liquidity-rewards.png?w=1100&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=c1360cc0a9aadafee148df76e446dc39 1100w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/earning-liquidity-rewards.png?w=1650&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=8c078f355b61a3d8bd09a62ff246fbad 1650w, https://mintcdn.com/polymarket-292d1b1b/YUHnSq4JdekVofRY/polymarket-learn/media/earning-liquidity-rewards.png?w=2500&fit=max&auto=format&n=YUHnSq4JdekVofRY&q=85&s=4cdcf0dc79ea6e6e28dcce1cbf08657e 2500w" />
</Frame>

## Learn more

Rewards are paid out automatically every day at \~midnight UTC. Your history on your portfolio page will reflect rewards paid to your address.

To read more about the specific calculations and formulas that determine rewards, visit our  [Rewards Documentation](/developers/rewards/overview).


# Market Orders
Source: https://docs.polymarket.com/polymarket-learn/trading/market-orders

How to buy shares.

# Market Orders

Once you've [signed up](../get-started/how-to-signup) and [deposited funds](../get-started/how-to-deposit), you're ready to start trading on Polymarket. Here's a step-by-step guide to get you started.

## Video Walkthrough

<iframe width="560" height="315" src="https://www.youtube.com/embed/1lFgkHLqo28?si=i7e61-roRsOVeRMW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

## Placing a Market Order

\_Before trading, you'll want to visit the [markets page](https://polymarket.com/markets) to find a market that interests you.

<Steps>
  <Steps.Step>
    ### [Choose a market](https://polymarket.com/markets)

    Locate the 'buy' modal, on the right side of the screen. Click the outcome you want to buy (usually Yes or No), then enter the dollar amount you wish to invest.
  </Steps.Step>

  <Steps.Step>
    ### Buy shares

    Click **Buy** and confirm the transaction in your wallet. Once your trade goes through, you'll receive a notification confirming its success.

    <Tip>Congrats, you're officially a Polymarket trader!</Tip>
  </Steps.Step>

  <Steps.Step>
    ### Share your bet slip

    You'll also see a bet slip to share on social media. We love sending \$\$\$ to traders who post their trades on Twitter and tag us!
  </Steps.Step>
</Steps>

Simple, right? If you think you've got the hang of it, it's time to learn about more advanced trading and order types. [Limit Orders](../trading/limit-orders/).


# Does Polymarket Have Trading Limits?
Source: https://docs.polymarket.com/polymarket-learn/trading/no-limits



By design, the Polymarket orderbook **does not** have trading size limits. It matches willing buyers and sellers of any amount.

However, there is no guarantee that it will be possible to transact a desired amount of shares without impacting the price significantly, or at all if there are no willing counterparties. Before trading in any market, especially in large size, it is valuable to look at the orderbook to understand depth of liquidity, ie how many buyers or sellers are in the market and their desired trade size and price.


# Using the Order Book
Source: https://docs.polymarket.com/polymarket-learn/trading/using-the-orderbook

Understanding the Order Book will help you become an advanced trader.

In the Getting Started tutorial on [Making your First Trade](../get-started/making-your-first-trade/), we learned about market orders.

In a market order, your trade executes instantly at the current market price.

But what if you think the market price is too high and want to set a specific price that you would be willing to accept? These are called [Limit Orders](../trading/limit-orders/).

## Viewing the Order Book

The order book is a list of every open order to buy or sell shares in a particular market.

<Frame>
  <img className="block w-full h-auto dark:hidden" style={{ maxWidth: '100%', height: 'auto' }} noZoom src="https://polymarket-upload.s3.us-east-2.amazonaws.com/Orderbook-light.png" />
</Frame>

In this market, **“Presidential Election Winner 2024”**, we are viewing the order book for Trump <span style={{ backgroundColor: '#E5F8E6', color: '#27AE60', padding: '2px 4px', borderRadius: '4px' }}>Yes</span> shares.

The green side represents the <span style={{ backgroundColor: '#E5F8E6', color: '#27AE60', padding: '2px 4px', borderRadius: '4px' }}>Bids</span>: the highest price traders are willing to pay to buy Trump <span style={{ backgroundColor: '#E5F8E6', color: '#27AE60', padding: '2px 4px', borderRadius: '4px' }}>Yes</span>
shares.

The red side represents the <span style={{ backgroundColor: '#FEEEE5', color: '#F55A00', padding: '2px 4px', borderRadius: '4px' }}>Asks</span>: the lowest price traders are willing to accept to sell Trump <span style={{ backgroundColor: '#E5F8E6', color: '#27AE60', padding: '2px 4px', borderRadius: '4px' }}>Yes</span> shares.

<Tip>
  Notice that there is a 0.3c gap between the highest bid and the lowest ask price. This is referred to as the spread.
</Tip>

## Managing open orders

When you have an open order, you'll find it displayed just below the Order Book on the market's page.

If you have open orders across multiple markets, you can easily manage and monitor them all from the [Portfolio page](https://polymarket.com/portfolio?tab=Open+orders).

## Canceling open orders

When you have an open order, you'll find it displayed just below the Order Book on the market's page.

To cancel the order, you can simply click the red **x** button alongside the order.

<iframe width="560" height="315" src="https://www.youtube.com/embed/KuA2UdUfZls?si=RUpuzqB9lbBB2pl9" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

If you have open orders across multiple markets, you can easily manage and monitor them all from the [Portfolio page](https://polymarket.com/portfolio?tab=Open+orders).

Nice! You can officially call yourself an advanced trader.

<Tip>
  If some of this still isn’t making sense, feel free to reach out to us on [Discord](https://discord.com/invite/polymarket). We’re happy to help get you up to speed.
</Tip>


# Glossary
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


# Developer Quickstart
Source: https://docs.polymarket.com/quickstart/introduction/main



This section of the documentation will provide all the essential resources to help you perform basic trading actions on the Polymarket platform. If you're just getting started, you're in the right place.

Everything you need to start building with the Polymarket API is right here. Let’s get started.

[Not sure what to build next? Get inspired by checking out real examples from other developers using the API.](/quickstart/introduction/showcase)


# API Rate Limits
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

### CLOB Market Data

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


# Your First Order
Source: https://docs.polymarket.com/quickstart/orders/first-order



Placing your first order using one of our two Clients is relatively straightforward.

For Python: `pip install py-clob-client`.

For Typescript: `npm install polymarket/clob-client` & `npm install ethers`.

After installing one of those you will be able to run the below code. Take the time to fill in the constants at the top and ensure you're using the proper signature type based on your login method.
<Tip>Many additional examples for the Typescript and Python clients are available [here(TS)](https://github.com/Polymarket/clob-client/tree/main/examples) and [here(Python)](https://github.com/Polymarket/py-clob-client/tree/main/examples) .</Tip>

<CodeGroup>
  ```python Python First Trade [expandable] theme={null}
  from py_clob_client.client import ClobClient
  from py_clob_client.clob_types import OrderArgs, OrderType
  from py_clob_client.order_builder.constants import BUY

  host: str = "https://clob.polymarket.com"
  key: str = "" #This is your Private Key. Export from https://reveal.magic.link/polymarket or from your Web3 Extension
  chain_id: int = 137 #No need to adjust this
  POLYMARKET_PROXY_ADDRESS: str = '' #This is the address listed below your profile picture when using the Polymarket site.

  #Select from the following 3 initialization options to match your login method, and remove any unused lines so only one client is initialized.


  ### Initialization of a client using a Polymarket Proxy associated with an Email/Magic account. If you login with your email use this example.
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client that trades directly from an EOA. (If you don't know what this means, you're not using it)
  client = ClobClient(host, key=key, chain_id=chain_id)

  ## Create and sign a limit order buying 5 tokens for 0.010c each
  #Refer to the API documentation to locate a tokenID: https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide

  client.set_api_creds(client.create_or_derive_api_creds()) 

  order_args = OrderArgs(
      price=0.01,
      size=5.0,
      side=BUY,
      token_id="", #Token ID you want to purchase goes here. Example token: 114304586861386186441621124384163963092522056897081085884483958561365015034812 ( Xi Jinping out in 2025, YES side )
  )
  signed_order = client.create_order(order_args)

  ## GTC(Good-Till-Cancelled) Order
  resp = client.post_order(signed_order, OrderType.GTC)
  print(resp)

  ```

  ```typescript Typescript First Trade theme={null}
  //npm install @polymarket/clob-client
  //npm install ethers
  //Client initialization example and dumping API Keys

  import { ApiKeyCreds, ClobClient, OrderType, Side, } from "@polymarket/clob-client";
  import { Wallet } from "@ethersproject/wallet";

  const host = 'https://clob.polymarket.com';
  const funder = ''; //This is the address listed below your profile picture when using the Polymarket site.
  const signer = new Wallet(""); //This is your Private Key. If using email login export from https://reveal.magic.link/polymarket otherwise export from your Web3 Application


  //In general don't create a new API key, always derive or createOrDerive
  const creds = new ClobClient(host, 137, signer).createOrDeriveApiKey();

  //1: Magic/Email Login
  //2: Browser Wallet(Metamask, Coinbase Wallet, etc)
  //0: EOA (If you don't know what this is you're not using it)

  const signatureType = 1; 
    (async () => {
      const clobClient = new ClobClient(host, 137, signer, await creds, signatureType, funder);
      const resp2 = await clobClient.createAndPostOrder(
          {
              tokenID: "", //Use https://docs.polymarket.com/developers/gamma-markets-api/get-markets to grab a sample token
              price: 0.01,
              side: Side.BUY,
              size: 5,
              feeRateBps: 0,
          },
          { tickSize: "0.001",negRisk: false }, //You'll need to adjust these based on the market. Get the tickSize and negRisk T/F from the get-markets above
          //Refer to the API documentation to locate a tokenID: https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide
          //Example token: 114304586861386186441621124384163963092522056897081085884483958561365015034812 ( Xi Jinping out in 2025, YES side )
          //{ tickSize: "0.001",negRisk: true },

          OrderType.GTC, 
      );
      console.log(resp2)
    })();
  ```
</CodeGroup>

#### In addition to detailed comments in the code snippet, here are some more tips to help you get started.

* See the Python example for details on the proper way to initialize a Py-Clob-Client depending on your wallet type. Three exhaustive examples are given. If using a MetaMask wallet or EOA please see the resources [here](https://github.com/Polymarket/py-clob-client?tab=readme-ov-file), for instructions on setting allowances.
* When buying into a market you purchase a "Token" that token represents either a Yes or No outcome of the event. To easily get required token pairs for a given event we have provided an interactive endpoint [here](/developers/gamma-markets-api/get-markets).
* Common pitfalls:
  * Negrisk Markets require an additional flag in the OrderArgs `negrisk=False `
  * `invalid signature` error, likely due to one of the following.
    * Incorrect Funder and or Private Key
    * Incorrect NegRisk flag in your order arguments
  * `not enough balance / allowance`.
    * Not enough USDC to perform the trade. See the formula at the bottom of [this](/developers/CLOB/orders/orders) page for details.
    * If using Metamask / WEB3 wallet go [here](https://github.com/Polymarket/py-clob-client?tab=readme-ov-file), for instructions on setting allowances.


# WSS Quickstart
Source: https://docs.polymarket.com/quickstart/websocket/WSS-Quickstart



The following code samples and explanation will show you how to subsribe to the Marker and User channels of the Websocket.
You'll need your API keys to do this so we'll start with that.

## Getting your API Keys

<CodeGroup>
  ```python DeriveAPIKeys-Python [expandable] theme={null}
  from py_clob_client.client import ClobClient

  host: str = "https://clob.polymarket.com"
  key: str = "" #This is your Private Key. If using email login export from https://reveal.magic.link/polymarket otherwise export from your Web3 Application
  chain_id: int = 137 #No need to adjust this
  POLYMARKET_PROXY_ADDRESS: str = '' #This is the address you deposit/send USDC to to FUND your Polymarket account.

  #Select from the following 3 initialization options to matches your login method, and remove any unused lines so only one client is initialized.

  ### Initialization of a client using a Polymarket Proxy associated with an Email/Magic account. If you login with your email use this example.
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client that trades directly from an EOA. 
  client = ClobClient(host, key=key, chain_id=chain_id)

  print( client.derive_api_key() )

  ```

  ```javascript DeriveAPIKeys-TS [expandable] theme={null}
  //npm install @polymarket/clob-client
  //npm install ethers
  //Client initialization example and dumping API Keys
  import {ClobClient, ApiKeyCreds } from "@polymarket/clob-client";
  import { Wallet } from "@ethersproject/wallet";

  const host = 'https://clob.polymarket.com';
  const signer = new Wallet("YourPrivateKey"); //This is your Private Key. If using email login export from https://reveal.magic.link/polymarket otherwise export from your Web3 Application

  // Initialize the clob client
  // NOTE: the signer must be approved on the CTFExchange contract
  const clobClient = new ClobClient(host, 137, signer);

  (async () => {
    const apiKey = await clobClient.deriveApiKey();
    console.log(apiKey);
  })();
  ```
</CodeGroup>

## Using those keys to connect to the Market or User Websocket

<CodeGroup>
  ```python WSS-Connection [expandable] theme={null}
  from websocket import WebSocketApp
  import json
  import time
  import threading

  MARKET_CHANNEL = "market"
  USER_CHANNEL = "user"


  class WebSocketOrderBook:
      def __init__(self, channel_type, url, data, auth, message_callback, verbose):
          self.channel_type = channel_type
          self.url = url
          self.data = data
          self.auth = auth
          self.message_callback = message_callback
          self.verbose = verbose
          furl = url + "/ws/" + channel_type
          self.ws = WebSocketApp(
              furl,
              on_message=self.on_message,
              on_error=self.on_error,
              on_close=self.on_close,
              on_open=self.on_open,
          )
          self.orderbooks = {}

      def on_message(self, ws, message):
          print(message)
          pass

      def on_error(self, ws, error):
          print("Error: ", error)
          exit(1)

      def on_close(self, ws, close_status_code, close_msg):
          print("closing")
          exit(0)

      def on_open(self, ws):
          if self.channel_type == MARKET_CHANNEL:
              ws.send(json.dumps({"assets_ids": self.data, "type": MARKET_CHANNEL}))
          elif self.channel_type == USER_CHANNEL and self.auth:
              ws.send(
                  json.dumps(
                      {"markets": self.data, "type": USER_CHANNEL, "auth": self.auth}
                  )
              )
          else:
              exit(1)

          thr = threading.Thread(target=self.ping, args=(ws,))
          thr.start()

      def ping(self, ws):
          while True:
              ws.send("PING")
              time.sleep(10)

      def run(self):
          self.ws.run_forever()


  if __name__ == "__main__":
      url = "wss://ws-subscriptions-clob.polymarket.com"
      #Complete these by exporting them from your initialized client. 
      api_key = ""
      api_secret = ""
      api_passphrase = ""

      asset_ids = [
          "109681959945973300464568698402968596289258214226684818748321941747028805721376",
      ]
      condition_ids = [] # no really need to filter by this one

      auth = {"apiKey": api_key, "secret": api_secret, "passphrase": api_passphrase}

      market_connection = WebSocketOrderBook(
          MARKET_CHANNEL, url, asset_ids, auth, None, True
      )
      user_connection = WebSocketOrderBook(
          USER_CHANNEL, url, condition_ids, auth, None, True
      )

      market_connection.run()
      # user_connection.run()
  ```
</CodeGroup>


