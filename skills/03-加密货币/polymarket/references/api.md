# Polymarket - Api

**Pages:** 46

---

## Get sports metadata information

**URL:** llms-txt#get-sports-metadata-information

Source: https://docs.polymarket.com/api-reference/sports/get-sports-metadata-information

api-reference/gamma-openapi.json get /sports
Retrieves metadata for various sports including images, resolution sources, ordering preferences, tags, and series information. This endpoint provides comprehensive sport configuration data used throughout the platform.

---

## Get user activity

**URL:** llms-txt#get-user-activity

Source: https://docs.polymarket.com/api-reference/core/get-user-activity

api-reference/data-api-openapi.yaml get /activity
Returns on-chain activity for a user.

---

## Get comments by comment id

**URL:** llms-txt#get-comments-by-comment-id

Source: https://docs.polymarket.com/api-reference/comments/get-comments-by-comment-id

api-reference/gamma-openapi.json get /comments/{id}

---

## Get open interest

**URL:** llms-txt#get-open-interest

Source: https://docs.polymarket.com/api-reference/misc/get-open-interest

api-reference/data-api-openapi.yaml get /oi

---

## Get total value of a user's positions

**URL:** llms-txt#get-total-value-of-a-user's-positions

Source: https://docs.polymarket.com/api-reference/core/get-total-value-of-a-users-positions

api-reference/data-api-openapi.yaml get /value

---

## Get related tags (relationships) by tag id

**URL:** llms-txt#get-related-tags-(relationships)-by-tag-id

Source: https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-id

api-reference/gamma-openapi.json get /tags/{id}/related-tags

---

## List events

**URL:** llms-txt#list-events

Source: https://docs.polymarket.com/api-reference/events/list-events

api-reference/gamma-openapi.json get /events

---

## Get tag by id

**URL:** llms-txt#get-tag-by-id

Source: https://docs.polymarket.com/api-reference/tags/get-tag-by-id

api-reference/gamma-openapi.json get /tags/{id}

---

## Get market by id

**URL:** llms-txt#get-market-by-id

Source: https://docs.polymarket.com/api-reference/markets/get-market-by-id

api-reference/gamma-openapi.json get /markets/{id}

---

## WSS Authentication

**URL:** llms-txt#wss-authentication

Source: https://docs.polymarket.com/developers/CLOB/websocket/wss-auth

<Tip> Only connections to `user` channel require authentication. </Tip>

| Field      | Optional | Description                           |
| ---------- | -------- | ------------------------------------- |
| apikey     | yes      | Polygon account's CLOB api key        |
| secret     | yes      | Polygon account's CLOB api secret     |
| passphrase | yes      | Polygon account's CLOB api passphrase |

---

## Get tags related to a tag slug

**URL:** llms-txt#get-tags-related-to-a-tag-slug

Source: https://docs.polymarket.com/api-reference/tags/get-tags-related-to-a-tag-slug

api-reference/gamma-openapi.json get /tags/slug/{slug}/related-tags/tags

---

## Get related tags (relationships) by tag slug

**URL:** llms-txt#get-related-tags-(relationships)-by-tag-slug

Source: https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug

api-reference/gamma-openapi.json get /tags/slug/{slug}/related-tags

---

## Get total markets a user has traded

**URL:** llms-txt#get-total-markets-a-user-has-traded

Source: https://docs.polymarket.com/api-reference/misc/get-total-markets-a-user-has-traded

api-reference/data-api-openapi.yaml get /traded

---

## Get market by slug

**URL:** llms-txt#get-market-by-slug

Source: https://docs.polymarket.com/api-reference/markets/get-market-by-slug

api-reference/gamma-openapi.json get /markets/slug/{slug}

---

## List tags

**URL:** llms-txt#list-tags

Source: https://docs.polymarket.com/api-reference/tags/list-tags

api-reference/gamma-openapi.json get /tags

---

## Get market price

**URL:** llms-txt#get-market-price

Source: https://docs.polymarket.com/api-reference/pricing/get-market-price

api-reference/clob-subset-openapi.yaml get /price
Retrieves the market price for a specific token and side

---

## Next page of markets with tag filtering

**URL:** llms-txt#next-page-of-markets-with-tag-filtering

**Contents:**
- Best Practices
- Related Endpoints

curl "https://gamma-api.polymarket.com/markets?tag_id=100381&closed=false&limit=25&offset=25"
```

1. **For Individual Markets:** Always use the slug method for best performance
2. **For Category Browsing:** Use tag filtering to reduce API calls
3. **For Complete Market Discovery:** Use the events endpoint with pagination
4. **Always Include `closed=false`:** Unless you specifically need historical data
5. **Implement Rate Limiting:** Respect API limits for production applications

* [Get Markets](/developers/gamma-markets-api/get-markets) - Full markets endpoint documentation
* [Get Events](/developers/gamma-markets-api/get-events) - Full events endpoint documentation
* [Search Markets](/developers/gamma-markets-api/get-public-search) - Search functionality

---

## API Key Operations

**URL:** llms-txt#api-key-operations

**Contents:**
- Create API Key
- Derive API Key
- Get API Keys
- Delete API Key
- Access Status
- Get Closed Only Mode Status

<Tip>This endpoint requires an **L1 Header**.</Tip>

Create new API key credentials for a user.

<Tip>This endpoint requires an **L1 Header**. </Tip>

Derive an existing API key for an address and nonce.

<Tip>This endpoint requires an **L2 Header**. </Tip>

Retrieve all API keys associated with a Polygon address.

<Tip>This endpoint requires an **L2 Header**.</Tip>

Delete an API key used to authenticate a request.

Check the value of `cert_required` by signer address.

## Get Closed Only Mode Status

<Tip>This endpoint requires an **L2 Header**.</Tip>

Retrieve the closed-only mode flag status.

**Examples:**

Example 1 (unknown):
```unknown
***

## Derive API Key

<Tip>This endpoint requires an **L1 Header**. </Tip>

Derive an existing API key for an address and nonce.

**HTTP Request:**
```

Example 2 (unknown):
```unknown
***

## Get API Keys

<Tip>This endpoint requires an **L2 Header**. </Tip>

Retrieve all API keys associated with a Polygon address.

**HTTP Request:**
```

Example 3 (unknown):
```unknown
***

## Delete API Key

<Tip>This endpoint requires an **L2 Header**.</Tip>

Delete an API key used to authenticate a request.

**HTTP Request:**
```

Example 4 (unknown):
```unknown
***

## Access Status

Check the value of `cert_required` by signer address.

**HTTP Request:**
```

---

## List comments

**URL:** llms-txt#list-comments

Source: https://docs.polymarket.com/api-reference/comments/list-comments

api-reference/gamma-openapi.json get /comments

---

## Get trades for a user or markets

**URL:** llms-txt#get-trades-for-a-user-or-markets

Source: https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets

api-reference/data-api-openapi.yaml get /trades

---

## Get event tags

**URL:** llms-txt#get-event-tags

Source: https://docs.polymarket.com/api-reference/events/get-event-tags

api-reference/gamma-openapi.json get /events/{id}/tags

---

## Create and Place an Order

**URL:** llms-txt#create-and-place-an-order

**Contents:**
  - Request Payload Parameters
  - Order types
  - Response Format
  - Insert Error Messages
  - Insert Statuses

<Tip> This endpoint requires a L2 Header </Tip>

Create and place an order using the Polymarket CLOB API clients. All orders are represented as "limit" orders, but "market" orders are also supported. To place a market order, simply ensure your price is marketable against current resting limit orders, which are executed on input at the best price.

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

---

## Get series by id

**URL:** llms-txt#get-series-by-id

Source: https://docs.polymarket.com/api-reference/series/get-series-by-id

api-reference/gamma-openapi.json get /series/{id}

---

## List markets

**URL:** llms-txt#list-markets

Source: https://docs.polymarket.com/api-reference/markets/list-markets

api-reference/gamma-openapi.json get /markets

---

## Get bid-ask spreads

**URL:** llms-txt#get-bid-ask-spreads

Source: https://docs.polymarket.com/api-reference/spreads/get-bid-ask-spreads

api-reference/clob-subset-openapi.yaml post /spreads
Retrieves bid-ask spreads for multiple tokens

---

## List series

**URL:** llms-txt#list-series

Source: https://docs.polymarket.com/api-reference/series/list-series

api-reference/gamma-openapi.json get /series

---

## Search markets, events, and profiles

**URL:** llms-txt#search-markets,-events,-and-profiles

Source: https://docs.polymarket.com/api-reference/search/search-markets-events-and-profiles

api-reference/gamma-openapi.json get /public-search

---

## Get multiple order books summaries by request

**URL:** llms-txt#get-multiple-order-books-summaries-by-request

Source: https://docs.polymarket.com/api-reference/orderbook/get-multiple-order-books-summaries-by-request

api-reference/clob-subset-openapi.yaml post /books
Retrieves order book summaries for specified tokens via POST request

---

## Get multiple market prices

**URL:** llms-txt#get-multiple-market-prices

Source: https://docs.polymarket.com/api-reference/pricing/get-multiple-market-prices

api-reference/clob-subset-openapi.yaml get /prices
Retrieves market prices for multiple tokens and sides

---

## Get midpoint price

**URL:** llms-txt#get-midpoint-price

Source: https://docs.polymarket.com/api-reference/pricing/get-midpoint-price

api-reference/clob-subset-openapi.yaml get /midpoint
Retrieves the midpoint price for a specific token

---

## List teams

**URL:** llms-txt#list-teams

Source: https://docs.polymarket.com/api-reference/sports/list-teams

api-reference/gamma-openapi.json get /teams

---

## Get current positions for a user

**URL:** llms-txt#get-current-positions-for-a-user

Source: https://docs.polymarket.com/api-reference/core/get-current-positions-for-a-user

api-reference/data-api-openapi.yaml get /positions
Returns positions filtered by user and optional filters.

---

## Health check

**URL:** llms-txt#health-check

Source: https://docs.polymarket.com/api-reference/health/health-check

api-reference/data-api-openapi.yaml get /

---

## Get tags related to a tag id

**URL:** llms-txt#get-tags-related-to-a-tag-id

Source: https://docs.polymarket.com/api-reference/tags/get-tags-related-to-a-tag-id

api-reference/gamma-openapi.json get /tags/{id}/related-tags/tags

---

## Get multiple market prices by request

**URL:** llms-txt#get-multiple-market-prices-by-request

Source: https://docs.polymarket.com/api-reference/pricing/get-multiple-market-prices-by-request

api-reference/clob-subset-openapi.yaml post /prices
Retrieves market prices for specified tokens and sides via POST request

---

## Get market tags by id

**URL:** llms-txt#get-market-tags-by-id

Source: https://docs.polymarket.com/api-reference/markets/get-market-tags-by-id

api-reference/gamma-openapi.json get /markets/{id}/tags

---

## Get closed positions for a user

**URL:** llms-txt#get-closed-positions-for-a-user

Source: https://docs.polymarket.com/api-reference/core/get-closed-positions-for-a-user

api-reference/data-api-openapi.yaml get /closed-positions
Fetches closed positions for a user(address)

---

## Get event by slug

**URL:** llms-txt#get-event-by-slug

Source: https://docs.polymarket.com/api-reference/events/get-event-by-slug

api-reference/gamma-openapi.json get /events/slug/{slug}

---

## Get live volume for an event

**URL:** llms-txt#get-live-volume-for-an-event

Source: https://docs.polymarket.com/api-reference/misc/get-live-volume-for-an-event

api-reference/data-api-openapi.yaml get /live-volume

---

## Get tag by slug

**URL:** llms-txt#get-tag-by-slug

Source: https://docs.polymarket.com/api-reference/tags/get-tag-by-slug

api-reference/gamma-openapi.json get /tags/slug/{slug}

---

## Get comments by user address

**URL:** llms-txt#get-comments-by-user-address

Source: https://docs.polymarket.com/api-reference/comments/get-comments-by-user-address

api-reference/gamma-openapi.json get /comments/user_address/{user_address}

---

## Get order book summary

**URL:** llms-txt#get-order-book-summary

Source: https://docs.polymarket.com/api-reference/orderbook/get-order-book-summary

api-reference/clob-subset-openapi.yaml get /book
Retrieves the order book summary for a specific token

---

## Endpoint

**URL:** llms-txt#endpoint

[https://gamma-api.polymarket.com](https://gamma-api.polymarket.com)

---

## Get top holders for markets

**URL:** llms-txt#get-top-holders-for-markets

Source: https://docs.polymarket.com/api-reference/core/get-top-holders-for-markets

api-reference/data-api-openapi.yaml get /holders

---

## Get event by id

**URL:** llms-txt#get-event-by-id

Source: https://docs.polymarket.com/api-reference/events/get-event-by-id

api-reference/gamma-openapi.json get /events/{id}

---

## Get price history for a traded token

**URL:** llms-txt#get-price-history-for-a-traded-token

Source: https://docs.polymarket.com/api-reference/pricing/get-price-history-for-a-traded-token

api-reference/clob-subset-openapi.yaml get /prices-history
Fetches historical price data for a specified market token

---
