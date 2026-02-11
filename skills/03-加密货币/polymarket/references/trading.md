# Polymarket - Trading

**Pages:** 26

---

## Place Single Order

**URL:** llms-txt#place-single-order

Source: https://docs.polymarket.com/developers/CLOB/orders/create-order

Detailed instructions for creating, placing, and managing orders using Polymarket's CLOB API.

---

## Cancel an single Order

**URL:** llms-txt#cancel-an-single-order

**Contents:**
  - Request Payload Parameters
  - Response Format

<Tip> This endpoint requires a L2 Header. </Tip>

`DELETE /<clob-endpoint>/order`

### Request Payload Parameters

| Name    | Required | Type   | Description           |
| ------- | -------- | ------ | --------------------- |
| orderID | yes      | string | ID of order to cancel |

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Onchain Order Info

**URL:** llms-txt#onchain-order-info

**Contents:**
- How do I interpret the OrderFilled onchain event?

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

---

## Cancel Orders(s)

**URL:** llms-txt#cancel-orders(s)

Source: https://docs.polymarket.com/developers/CLOB/orders/cancel-orders

Multiple endpoints to cancel a single order, multiple orders, all orders or all orders from a single market.

---

## Page 1: First 50 results (offset=0)

**URL:** llms-txt#page-1:-first-50-results-(offset=0)

curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=0"
bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Place Multiple Orders (Batching)

**URL:** llms-txt#place-multiple-orders-(batching)

**Contents:**
  - Request Payload Parameters
  - Order types
  - Response Format
  - Insert Error Messages
  - Insert Statuses

Source: https://docs.polymarket.com/developers/CLOB/orders/create-order-batch

Instructions for placing multiple orders(Batch)

<Tip> This endpoint requires a L2 Header </Tip>

Polymarket’s CLOB supports batch orders, allowing you to place up to `15` orders in a single request. Before using this feature, make sure you're comfortable placing a single order first. You can find the documentation for that [here.](/developers/CLOB/orders/create-order)

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

* **FOK**: A Fill-Or-Kill order is an market order to buy (in dollars) or sell (in shares) shares that must be executed immediately in its entirety; otherwise, the entire order will be cancelled.
* **FAK**: A Fill-And-Kill order is a market order to buy (in dollars) or sell (in shares) that will be executed immediately for as many shares as are available; any portion not filled at once is cancelled.
* **GTC**: A Good-Til-Cancelled order is a limit order that is active until it is fulfilled or cancelled.
* **GTD**: A Good-Til-Date order is a type of order that is active until its specified date (UTC seconds timestamp), unless it has already been fulfilled or cancelled. There is a security threshold of one minute. If the order needs to expire in 90 seconds the correct expiration value is: now + 1 minute + 30 seconds

| Name        | Type      | Description                                                                                                                        |
| ----------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| success     | boolean   | boolean indicating if server-side err (`success = false`) -> server-side error                                                     |
| errorMsg    | string    | error message in case of unsuccessful placement (in case `success = false`, e.g. `client-side error`, the reason is in `errorMsg`) |
| orderId     | string    | id of order                                                                                                                        |
| orderHashes | string\[] | hash of settlement transaction order was marketable and triggered a match                                                          |

### Insert Error Messages

If the `errorMsg` field of the response object from placement is not an empty string, the order was not able to be immediately placed. This might be because of a delay or because of a failure. If the `success` is not `true`, then there was an issue placing the order. The following `errorMessages` are possible:

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

When placing an order, a status field is included. The status field provides additional information regarding the order's state as a result of the placement. Possible values include:

| Status    | Description                                                  |
| --------- | ------------------------------------------------------------ |
| matched   | order placed and matched with an existing resting order      |
| live      | order placed and resting on the book                         |
| delayed   | order marketable, but subject to matching delay              |
| unmatched | order marketable, but failure delaying, placement successful |

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown

```

---

## null

**URL:** llms-txt#null

**Contents:**
- Subgraph Overview
- Source
- Hosted Version

Source: https://docs.polymarket.com/developers/subgraph/overview

Polymarket has written and open sourced a subgraph that provides, via a GraphQL query interface, useful aggregate calculations and event indexing for things like volume, user position, market and liquidity data. The subgraph updates in real time to be able to be mixed, and match core data from the primary Polymarket interface, providing positional data, activity history and more. The subgraph can be hosted by anyone but is also hosted and made publicly available by a 3rd party provider, Goldsky.

The Polymarket subgraph is entirely open source and can be found on the Polymarket Github.

**[Subgraph Github Repository](https://github.com/Polymarket/polymarket-subgraph)**

> Note: The available models/schemas can be found in the `schema.graphql` file.

The subgraphs are hosted on goldsky, each with an accompanying GraphQL playground:

* Orders subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn)

* Positions subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/positions-subgraph/0.0.7/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/positions-subgraph/0.0.7/gn)

* Activity subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/activity-subgraph/0.0.4/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/activity-subgraph/0.0.4/gn)

* Open Interest subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/oi-subgraph/0.0.6/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/oi-subgraph/0.0.6/gn)

* PNL subgraph: [https://api.goldsky.com/api/public/project\_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn](https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn)

---

## Get Order

**URL:** llms-txt#get-order

**Contents:**
  - Request Parameters
  - Response Format

Source: https://docs.polymarket.com/developers/CLOB/orders/get-order

Get information about an existing order

<Tip>This endpoint requires a L2 Header. </Tip>

Get single order by id.

`GET /<clob-endpoint>/data/order/<order_hash>`

### Request Parameters

| Name | Required | Type   | Description                          |
| ---- | -------- | ------ | ------------------------------------ |
| id   | no       | string | id of order to get information about |

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

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Page 2: Next 50 results (offset=50)

**URL:** llms-txt#page-2:-next-50-results-(offset=50)

curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=50"
bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Cancel ALL Orders

**URL:** llms-txt#cancel-all-orders

**Contents:**
  - Response Format

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel all open orders posted by a user.

`DELETE /<clob-endpoint>/cancel-all`

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Polymarket Changelog

**URL:** llms-txt#polymarket-changelog

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

---

## Splitting USDC

**URL:** llms-txt#splitting-usdc

Source: https://docs.polymarket.com/developers/CTF/split

At any time, after a condition has been prepared on the CTF contract (via `prepareCondition`), it is possible to "split" collateral into a full (position) set. In other words, one unit USDC can be split into 1 YES unit and 1 NO unit. If splitting from the collateral, the CTF contract will attempt to transfer `amount` collateral from the message sender to itself. If successful, `amount` stake will be minted in the split target positions. If any of the transfers, mints, or burns fail, the transaction will revert. The transaction will also revert if the given partition is trivial, invalid, or refers to more slots than the condition is prepared with. This operation happens via the `splitPosition()` function on the CTF contract with the following parameters:

* `collateralToken`: IERC20 - The address of the positions' backing collateral token.
* `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being split and the split target positions. Null in Polymarket case.
* `conditionId`: bytes32 - The ID of the condition to split on.
* `partition`: uint\[] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint). Each element's a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
* `amount` - The amount of collateral or stake to split. Also the number of full sets to receive.

---

## Merging Tokens

**URL:** llms-txt#merging-tokens

Source: https://docs.polymarket.com/developers/CTF/merge

In addition to splitting collateral for a full set, the inverse can also happen; a full set can be "merged" for collateral. This operation can again happen at any time after a condition has been prepared on the CTF contract. One unit of each position in a full set is burned in return for 1 collateral unit. This operation happens via the `mergePositions()` function on the CTF contract with the following parameters:

* `collateralToken`: IERC20 - The address of the positions' backing collateral token.
* `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being merged and the merge target positions. Null in Polymarket case.
* `conditionId`: bytes32 - The ID of the condition to merge on.
* `partition`: uint\[] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint). Each element's a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
* `amount` - The number of full sets to merge. Also the amount of collateral to receive.

---

## Your First Order

**URL:** llms-txt#your-first-order

Source: https://docs.polymarket.com/quickstart/orders/first-order

Placing your first order using one of our two Clients is relatively straightforward.

For Python: `pip install py-clob-client`.

For Typescript: `npm install polymarket/clob-client` & `npm install ethers`.

After installing one of those you will be able to run the below code. Take the time to fill in the constants at the top and ensure you're using the proper signature type based on your login method.
<Tip>Many additional examples for the Typescript and Python clients are available [here(TS)](https://github.com/Polymarket/clob-client/tree/main/examples) and [here(Python)](https://github.com/Polymarket/py-clob-client/tree/main/examples) .</Tip>

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

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Paginating through markets with tag filtering

**URL:** llms-txt#paginating-through-markets-with-tag-filtering

curl "https://gamma-api.polymarket.com/markets?tag_id=100381&closed=false&limit=25&offset=0"
bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Reedeeming Tokens

**URL:** llms-txt#reedeeming-tokens

Source: https://docs.polymarket.com/developers/CTF/redeem

Once a condition has had it's payouts reported (ie by the UMACTFAdapter calling `reportPayouts` on the CTF contract), users with shares in the winning outcome can redeem them for the underlying collateral. Specifically, users can call the `redeemPositions` function on the CTF contract which will burn all valuable conditional tokens in return for collateral according to the reported payout vector. This function has the following parameters:

* `collateralToken`: IERC20 - The address of the positions' backing collateral token.
* `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being redeemed. Null in Polymarket case.
* `indexSets`: uint\[] - The ID of the condition to redeem.
* `indexSets`: uint\[] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint). Each element's a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.

---

## Get Trades

**URL:** llms-txt#get-trades

**Contents:**
  - Request Parameters
  - Response Format

Source: https://docs.polymarket.com/developers/CLOB/trades/trades

<Tip> This endpoint requires a L2 Header. </Tip>

Get trades for the authenticated user based on the provided filters.

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

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Market Channel

**URL:** llms-txt#market-channel

**Contents:**
- Book Message
  - Structure
- price\_change Message
  - Structure
- tick\_size\_change Message
  - Structure
- last\_trade\_price Message

Source: https://docs.polymarket.com/developers/CLOB/websocket/market-channel

Public channel for updates related to market updates (level 2 price data).

`<wss-channel> market`

* First subscribed to a market
* When there is a trade that affects the book

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

## price\_change Message

<div style={{backgroundColor: '#fff3cd', border: '1px solid #ffeaa7', borderRadius: '4px', padding: '12px', marginBottom: '16px'}}>
  <strong>⚠️ Breaking Change Notice:</strong> The price\_change message schema will be updated on September 15, 2025 at 11 PM UTC. Please see the [migration guide](/developers/CLOB/websocket/market-channel-migration-guide) for details.
</div>

* A new order is placed
* An order is cancelled

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

## tick\_size\_change Message

* The minimum tick size of the market changes. This happens when the book's price reaches the limits: price > 0.96 or price \< 0.04

| Name            | Type   | Description                |
| --------------- | ------ | -------------------------- |
| event\_type     | string | "price\_change"            |
| asset\_id       | string | asset ID (token ID)        |
| market          | string | condition ID of market     |
| old\_tick\_size | string | previous minimum tick size |
| new\_tick\_size | string | current minimum tick size  |
| side            | string | buy/sell                   |
| timestamp       | string | time of event              |

## last\_trade\_price Message

* When a maker and taker order is matched creating a trade event.

**Examples:**

Example 1 (unknown):
```unknown
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
```

Example 2 (unknown):
```unknown
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
```

Example 3 (unknown):
```unknown
## last\_trade\_price Message

Emitted When:

* When a maker and taker order is matched creating a trade event.
```

---

## Cancel orders from market

**URL:** llms-txt#cancel-orders-from-market

**Contents:**
  - Request Payload Parameters
  - Response Format

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel orders from market.

`DELETE /<clob-endpoint>/cancel-market-orders`

### Request Payload Parameters

| Name      | Required | Type   | Description                |
| --------- | -------- | ------ | -------------------------- |
| market    | no       | string | condition id of the market |
| asset\_id | no       | string | id of the asset/token      |

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Page 3: Next 50 results (offset=100)

**URL:** llms-txt#page-3:-next-50-results-(offset=100)

curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=100"
bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Cancel Multiple Orders

**URL:** llms-txt#cancel-multiple-orders

**Contents:**
  - Request Payload Parameters
  - Response Format

<Tip> This endpoint requires a L2 Header. </Tip>

`DELETE /<clob-endpoint>/orders`

### Request Payload Parameters

| Name | Required | Type      | Description                 |
| ---- | -------- | --------- | --------------------------- |
| null | yes      | string\[] | IDs of the orders to cancel |

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

**Examples:**

Example 1 (unknown):
```unknown

```

---

## User Channel

**URL:** llms-txt#user-channel

**Contents:**
- Trade Message
  - Structure
- Order Message
  - Structure

Source: https://docs.polymarket.com/developers/CLOB/websocket/user-channel

Authenticated channel for updates related to user activities (orders, trades), filtered for authenticated user by apikey.

* when a market order is matched ("MATCHED")
* when a limit order for the user is included in a trade ("MATCHED")
* subsequent status changes for trade ("MINED", "CONFIRMED", "RETRYING", "FAILED")

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

* When an order is placed (PLACEMENT)
* When an order is updated (some of it is matched) (UPDATE)
* When an order is canceled (CANCELLATION)

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

**Examples:**

Example 1 (unknown):
```unknown
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
```

---

## Detail

**URL:** llms-txt#detail

1. **Market**
   1. Contains data related to a market that is traded on. Maps onto a pair of clob token ids, a market address, a question id and a condition id

2. **Event**
   1. Contains a set of markets
   2. Variants:
      1. Event with 1 market (i.e., resulting in an SMP)
      2. Event with 2 or more markets (i.e., resulting in an GMP)

---

## Get Active Orders

**URL:** llms-txt#get-active-orders

**Contents:**
  - Request Parameters
  - Response Format

Source: https://docs.polymarket.com/developers/CLOB/orders/get-active-order

<Tip> This endpoint requires a L2 Header. </Tip>

Get active order(s) for a specific market.

`GET /<clob-endpoint>/data/orders`

### Request Parameters

| Name      | Required | Type   | Description                          |
| --------- | -------- | ------ | ------------------------------------ |
| id        | no       | string | id of order to get information about |
| market    | no       | string | condition id of market               |
| asset\_id | no       | string | id of the asset/token                |

| Name | Type         | Description                                          |
| ---- | ------------ | ---------------------------------------------------- |
| null | OpenOrder\[] | list of open orders filtered by the query parameters |

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Check if some orders are scoring

**URL:** llms-txt#check-if-some-orders-are-scoring

**Contents:**
  - Request Parameters
  - Response Format

> This endpoint requires a L2 Header.

Returns to a dictionary with boolean value where it is indicated if an order is scoring or not.

`POST /<clob-endpoint>/orders-scoring`

### Request Parameters

| Name     | Required | Type      | Description                                |
| -------- | -------- | --------- | ------------------------------------------ |
| orderIds | yes      | string\[] | ids of the orders to get information about |

| Name | Type          | Description         |
| ---- | ------------- | ------------------- |
| null | OrdersScoring | orders scoring data |

An `OrdersScoring` object is a dictionary that indicates the order by if it score.

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Check Order Reward Scoring

**URL:** llms-txt#check-order-reward-scoring

**Contents:**
  - Request Parameters
  - Response Format

Source: https://docs.polymarket.com/developers/CLOB/orders/check-scoring

Check if an order is eligble or scoring for Rewards purposes

<Tip> This endpoint requires a L2 Header. </Tip>

Returns a boolean value where it is indicated if an order is scoring or not.

`GET /<clob-endpoint>/order-scoring?order_id={...}`

### Request Parameters

| Name    | Required | Type   | Description                          |
| ------- | -------- | ------ | ------------------------------------ |
| orderId | yes      | string | id of order to get information about |

| Name | Type          | Description        |
| ---- | ------------- | ------------------ |
| null | OrdersScoring | order scoring data |

An `OrdersScoring` object is of the form:

| Name    | Type    | Description                              |
| ------- | ------- | ---------------------------------------- |
| scoring | boolean | indicates if the order is scoring or not |

---
