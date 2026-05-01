# Real time data client

This client provides a wrapper to connect to the `real-time-data-streaming` `WebSocket` service.

## How to use it

Here is a quick example about how to connect to the service and start receiving messages (you can find more in the folder `examples/`):

```typescript
import { RealTimeDataClient } from "../src/client";
import { Message } from "../src/model";

const onMessage = (message: Message): void => {
    console.log(message.topic, message.type, message.payload);
};

const onConnect = (client: RealTimeDataClient): void => {
    // Subscribe to a topic
    client.subscribe({
        subscriptions: [
            {
                topic: "comments",
                type: "*", // "*"" can be used to connect to all the types of the topic
                filters: `{"parentEntityID":100,"parentEntityType":"Event"}`, // empty means no filter
            },
        ],
    });
};

new RealTimeDataClient({ onMessage, onConnect }).connect();
```

## How to subscribe and unsubscribe from messages

Once the connection is stablished and you have a `client: RealTimeDataClient` object, you can `subscribe` and `unsubscribe` to many messages streamings using the same connection.

### Subscribe

Subscribe to 'trades' messages from the topic 'activity' and to the all comments messages.

```typescript
client.subscribe({
    subscriptions: [
        {
            topic: "activity",
            type: "trades",
        },
    ],
});

client.subscribe({
    subscriptions: [
        {
            topic: "comments",
            type: "*", // "*"" can be used to connect to all the types of the topic
        },
    ],
});
```

### Unsubscribe

Unsubscribe from the new trades messages of the topic 'activity'. If 'activity' has more messages types and I used '\*' to connect to all of them, this will only unsubscribe from the type 'trades'.

```typescript
client.subscribe({
    subscriptions: [
        {
            topic: "activity",
            type: "trades",
        },
    ],
});
```

### Disconnect

The `client` object provides a method to disconnect from the `WebSocket` server:

```typescript
client.disconnect();
```

## Messages hierarchy

| Topic                     | Type               | Auth     | Filters (if it is empty the messages won't be filtered)         | Schema                              | Subscription Handler                                        |
| ------------------------- | ------------------ | -------- | --------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------- |
| `activity`                | `trades`           | -        | `{"event_slug":"string"}' OR '{"market_slug":"string"}`         | [`Trade`](#trade)                   |                                                             |
| `activity`                | `orders_matched`   | -        | `{"event_slug":"string"}' OR '{"market_slug":"string"}`         | [`Trade`](#trade)                   |                                                             |
| `comments`                | `comment_created`  | -        | `{"parentEntityID":number,"parentEntityType":"Event / Series"}` | [`Comment`](#comment)               |                                                             |
| `comments`                | `comment_removed`  | -        | `{"parentEntityID":number,"parentEntityType":"Event / Series"}` | [`Comment`](#comment)               |                                                             |
| `comments`                | `reaction_created` | -        | `{"parentEntityID":number,"parentEntityType":"Event / Series"}` | [`Reaction`](#reaction)             |                                                             |
| `comments`                | `reaction_removed` | -        | `{"parentEntityID":number,"parentEntityType":"Event / Series"}` | [`Reaction`](#reaction)             |                                                             |
| `rfq`                     | `request_created`  | -        | -                                                               | [`Request`](#request)               |                                                             |
| `rfq`                     | `request_edited`   | -        | -                                                               | [`Request`](#request)               |                                                             |
| `rfq`                     | `request_canceled` | -        | -                                                               | [`Request`](#request)               |                                                             |
| `rfq`                     | `request_expired`  | -        | -                                                               | [`Request`](#request)               |                                                             |
| `rfq`                     | `quote_created`    | -        | -                                                               | [`Quote`](#quote)                   |                                                             |
| `rfq`                     | `quote_edited`     | -        | -                                                               | [`Quote`](#quote)                   |                                                             |
| `rfq`                     | `quote_canceled`   | -        | -                                                               | [`Quote`](#quote)                   |                                                             |
| `rfq`                     | `quote_expired`    | -        | -                                                               | [`Quote`](#quote)                   |                                                             |
| `crypto_prices`           | `update`           | -        | `{"symbol":string}`                                             | [`CryptoPrice`](#cryptoprice)       | [`CryptoPriceHistorical`](#initial-data-dump-on-connection) |
| `crypto_prices_chainlink` | `update`           | -        | `{"symbol":string}`                                             | [`CryptoPrice`](#cryptoprice)       | [`CryptoPriceHistorical`](#initial-data-dump-on-connection) |
| `clob_user`               | `order`            | ClobAuth | -                                                               | [`Order`](#order)                   |                                                             |
| `clob_user`               | `trade`            | ClobAuth | -                                                               | [`Trade`](#trade-1)                 |                                                             |
| `clob_market`             | `price_change`     | -        | `["100","200",...]` (filters are mandatory on this one)         | [`PriceChanges`](#pricechanges)     |                                                             |
| `clob_market`             | `agg_orderbook`    | -        | `["100","200",...]`                                             | [`AggOrderbook`](#aggorderbook)     | [`AggOrderbook`](#aggorderbook)                             |
| `clob_market`             | `last_trade_price` | -        | `["100","200",...]`                                             | [`LastTradePrice`](#lasttradeprice) |                                                             |
| `clob_market`             | `tick_size_change` | -        | `["100","200",...]`                                             | [`TickSizeChange`](#ticksizechange) |                                                             |
| `clob_market`             | `market_created`   | -        | -                                                               | [`ClobMarket`](#clobmarket)         |                                                             |
| `clob_market`             | `market_resolved`  | -        | -                                                               | [`ClobMarket`](#clobmarket)         |                                                             |

## Auth

### ClobAuth

```typescript
/**
 * API key credentials for CLOB authentication.
 */
export interface ClobApiKeyCreds {
    /** API key used for authentication */
    key: string;

    /** API secret associated with the key */
    secret: string;

    /** Passphrase required for authentication */
    passphrase: string;
}
```

```typescript
client.subscribe({
    subscriptions: [
        {
            topic: "clob_user",
            type: "*",
            clob_auth: {
                key: "xxxxxx-xxxx-xxxxx-xxxx-xxxxxx",
                secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                passphrase: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            },
        },
    ],
});
```

## Message types

### Activity

#### Trade

| Name              | Type    | Description                                        |
| ----------------- | ------- | -------------------------------------------------- |
| `asset`           | string  | ERC1155 token ID of conditional token being traded |
| `bio`             | string  | Bio of the user of the trade                       |
| `conditionId`     | string  | Id of market which is also the CTF condition ID    |
| `eventSlug`       | string  | Slug of the event                                  |
| `icon`            | string  | URL to the market icon image                       |
| `name`            | string  | Name of the user of the trade                      |
| `outcome`         | string  | Human readable outcome of the market               |
| `outcomeIndex`    | integer | Index of the outcome                               |
| `price`           | float   | Price of the trade                                 |
| `profileImage`    | string  | URL to the user profile image                      |
| `proxyWallet`     | string  | Address of the user proxy wallet                   |
| `pseudonym`       | string  | Pseudonym of the user                              |
| `side`            | string  | Side of the trade (`BUY`/`SELL`)                   |
| `size`            | integer | Size of the trade                                  |
| `slug`            | string  | Slug of the market                                 |
| `timestamp`       | integer | Timestamp of the trade                             |
| `title`           | string  | Title of the event                                 |
| `transactionHash` | string  | Hash of the transaction                            |

### Comments

#### Comment

| Name               | Type   | Description                                 |
| ------------------ | ------ | ------------------------------------------- |
| `id`               | string | Unique identifier of comment                |
| `body`             | string | Content of the comment                      |
| `parentEntityType` | string | Type of the parent entity (Event or Series) |
| `parentEntityID`   | number | ID of the parent entity                     |
| `parentCommentID`  | string | ID of the parent comment                    |
| `userAddress`      | string | Address of the user                         |
| `replyAddress`     | string | Address of the reply user                   |
| `createdAt`        | string | Creation timestamp                          |
| `updatedAt`        | string | Last update timestamp                       |

#### Reaction

| Name           | Type   | Description                    |
| -------------- | ------ | ------------------------------ |
| `id`           | string | Unique identifier of reaction  |
| `commentID`    | number | ID of the comment              |
| `reactionType` | string | Type of the reaction           |
| `icon`         | string | Icon representing the reaction |
| `userAddress`  | string | Address of the user            |
| `createdAt`    | string | Creation timestamp             |

### RFQ

#### Request

| Name           | Type   | Description                                                     |
| -------------- | ------ | --------------------------------------------------------------- |
| `requestId`    | string | Unique identifier for the request                               |
| `proxyAddress` | string | User proxy address                                              |
| `market`       | string | Id of market which is also the CTF condition ID                 |
| `token`        | string | `ERC1155` token ID of conditional token being traded            |
| `complement`   | string | Complement `ERC1155` token ID of conditional token being traded |
| `state`        | string | Current state of the request                                    |
| `side`         | string | Indicates buy or sell side                                      |
| `sizeIn`       | number | Input size of the request                                       |
| `sizeOut`      | number | Output size of the request                                      |
| `price`        | number | Price from in/out sizes                                         |
| `expiry`       | number | Expiry timestamp (UNIX format)                                  |

#### Quote

| Name           | Type   | Description                                                     |
| -------------- | ------ | --------------------------------------------------------------- |
| `quoteId`      | string | Unique identifier for the quote                                 |
| `requestId`    | string | Associated request identifier                                   |
| `proxyAddress` | string | User proxy address                                              |
| `token`        | string | `ERC1155` token ID of conditional token being traded            |
| `state`        | string | Current state of the quote                                      |
| `side`         | string | Indicates buy or sell side                                      |
| `sizeIn`       | number | Input size of the quote                                         |
| `sizeOut`      | number | Output size of the quote                                        |
| `sizeOut`      | number | Output size of the request                                      |
| `condition`    | string | Id of market which is also the CTF condition ID                 |
| `complement`   | string | Complement `ERC1155` token ID of conditional token being traded |
| `expiry`       | number | Expiry timestamp (UNIX format)                                  |

### CryptoPrice

| Name        | Type   | Description                              |
| ----------- | ------ | ---------------------------------------- |
| `symbol`    | string | Symbol of the asset                      |
| `timestamp` | number | Timestamp in milliseconds for the update |
| `value`     | number | Value at the time of update              |

#### Filters

- `{"symbol":"btcusdt"}`
- `{"symbol":"ethusdt"}`
- `{"symbol":"xrpusdt"}`
- `{"symbol":"solusdt"}`

#### Initial data dump on connection

When the connection is stablished, if a `filter` is used, the server will dump an initial snapshoot of recent data

| Name   | Type   | Description                                                      |
| ------ | ------ | ---------------------------------------------------------------- |
| symbol | string | Symbol of the asset                                              |
| data   | array  | Array of price data objects, each containing timestamp and value |

### CLOB User

#### Order

| Name            | Type               | Description                                               |
| --------------- | ------------------ | --------------------------------------------------------- |
| `asset_id`      | string             | Order's `ERC1155` token ID of conditional token           |
| `created_at`    | string (timestamp) | Order's creation UNIX timestamp                           |
| `expiration`    | string (timestamp) | Order's expiration UNIX timestamp                         |
| `id`            | string             | Unique order hash identifier                              |
| `maker_address` | string             | Maker’s address (funder)                                  |
| `market`        | string             | Condition ID or market identifier                         |
| `order_type`    | string             | Type of order: `GTC`, `GTD`, `FOK`, `FAK`                 |
| `original_size` | string             | Original size of the order at placement                   |
| `outcome`       | string             | Order outcome: `YES` / `NO`                               |
| `owner`         | string             | UUID of the order owner                                   |
| `price`         | string             | Order price (e.g., in decimals like `0.5`)                |
| `side`          | string             | Side of the trade: `BUY` or `SELL`                        |
| `size_matched`  | string             | Amount of order that has been matched                     |
| `status`        | string             | Status of the order (e.g., `MATCHED`)                     |
| `type`          | string             | Type of update: `PLACEMENT`, `CANCELLATION`, `FILL`, etc. |

#### Trade

| Name               | Type               | Description                                                       |
| ------------------ | ------------------ | ----------------------------------------------------------------- |
| `asset_id`         | string             | `ERC1155` token ID of the conditional token involved in the trade |
| `fee_rate_bps`     | string             | Fee rate in basis points (bps)                                    |
| `id`               | string             | Unique identifier for the match record                            |
| `last_update`      | string (timestamp) | Last update timestamp (UNIX)                                      |
| `maker_address`    | string             | Maker’s address                                                   |
| `maker_orders`     | array              | List of maker orders (see nested schema below)                    |
| `market`           | string             | Condition ID or market identifier                                 |
| `match_time`       | string (timestamp) | Match execution timestamp (UNIX)                                  |
| `outcome`          | string             | Outcome of the market: `YES` / `NO`                               |
| `owner`            | string             | UUID of the taker (owner of the matched order)                    |
| `price`            | string             | Matched price (in decimal format, e.g., `0.5`)                    |
| `side`             | string             | Taker side of the trade: `BUY` or `SELL`                          |
| `size`             | string             | Total matched size                                                |
| `status`           | string             | Status of the match: e.g., `MINED`                                |
| `taker_order_id`   | string             | ID of the taker's order                                           |
| `transaction_hash` | string             | Transaction hash where the match was settled                      |

##### `maker_orders`

| Name             | Type   | Description                                                      |
| ---------------- | ------ | ---------------------------------------------------------------- |
| `asset_id`       | string | `ERC1155` token ID of the conditional token of the maker's order |
| `fee_rate_bps`   | string | Maker's fee rate in basis points                                 |
| `maker_address`  | string | Maker’s address                                                  |
| `matched_amount` | string | Amount matched from the maker's order                            |
| `order_id`       | string | ID of the maker's order                                          |
| `outcome`        | string | Outcome targeted by the maker's order (`YES` / `NO`)             |
| `owner`          | string | UUID of the maker                                                |
| `price`          | string | Order price                                                      |
| `side`           | string | Side of the maker: `BUY` or `SELL`                               |

### CLOB market

#### PriceChanges

| Name                | Type               | Description                                               |
| ------------------- | ------------------ | --------------------------------------------------------- |
| `m` (market)        | string             | Condition ID                                              |
| `pc` (price change) | array              | Price changes by book                                     |
| `t` (timestamp)     | string (timestamp) | Timestamp in milliseconds since epoch (UNIX time \* 1000) |

##### PriceChange

NOTE: Filters are mandatory for this topic/type. Example: `["100","200",...]` (collection of token ids)

| Name            | Type   | Description                                                     |
| --------------- | ------ | --------------------------------------------------------------- |
| `a` (asset_id)  | string | Asset identifier                                                |
| `h` (hash)      | string | Unique hash ID of the book snapshot                             |
| `p` (price)     | string | Price quoted (e.g., `0.5`)                                      |
| `s` (side)      | string | Side of the quote: `BUY` or `SELL`                              |
| `si` (size)     | string | Size or volume available at the quoted price (e.g., `0`, `100`) |
| `ba` (best_ask) | string | Best ask price                                                  |
| `bb` (best_bid) | string | Best bid price                                                  |

#### AggOrderbook

| Name             | Type               | Description                                                             |
| ---------------- | ------------------ | ----------------------------------------------------------------------- |
| `asks`           | array              | List of ask aggregated orders (sell side), each with `price` and `size` |
| `asset_id`       | string             | Asset Id identifier                                                     |
| `bids`           | array              | List of aggregated bid orders (buy side), each with `price` and `size`  |
| `hash`           | string             | Unique hash ID for this orderbook snapshot                              |
| `market`         | string             | Market or condition ID                                                  |
| `min_order_size` | string             | Minimum allowed order size                                              |
| `neg_risk`       | boolean            | NegRisk or not                                                          |
| `tick_size`      | string             | Minimum tick size                                                       |
| `timestamp`      | string (timestamp) | Timestamp in milliseconds since epoch (UNIX time \* 1000)               |

##### `asks`/`bids` scheema

| Name    | Type   | Description        |
| ------- | ------ | ------------------ |
| `price` | string | Price level        |
| `size`  | string | Size at that price |

##### Initial data dump on connection

When the connection is stablished, if a `filter` is used, the server will dump an initial snapshoot of recent data

#### LastTradePrice

| Name           | Type   | Description                        |
| -------------- | ------ | ---------------------------------- |
| `asset_id`     | string | Asset Id identifier                |
| `fee_rate_bps` | string | Fee rate in basis points (bps)     |
| `market`       | string | Market or condition ID             |
| `price`        | string | Trade price (e.g., `0.5`)          |
| `side`         | string | Side of the order: `BUY` or `SELL` |
| `size`         | string | Size of the trade                  |

#### TickSizeChange

| Name            | Type   | Description                          |
| --------------- | ------ | ------------------------------------ |
| `market`        | string | Market or condition ID               |
| `asset_id`      | string | Array of two `ERC1155` asset ID      |
| `old_tick_size` | string | Previous tick size before the change |
| `new_tick_size` | string | Updated tick size after the change   |

#### ClobMarket

| Name             | Type      | Description                                                        |
| ---------------- | --------- | ------------------------------------------------------------------ |
| `market`         | string    | Market or condition ID                                             |
| `asset_ids`      | [2]string | Array of two `ERC1155` asset ID identifiers associated with market |
| `min_order_size` | string    | Minimum size allowed for an order                                  |
| `tick_size`      | string    | Minimum allowable price increment                                  |
| `neg_risk`       | boolean   | Indicates if the market is negative risk                           |
