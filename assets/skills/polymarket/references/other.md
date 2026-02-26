# Polymarket - Other

**Pages:** 7

---

## Deployment and Additional Information

**URL:** llms-txt#deployment-and-additional-information

**Contents:**
- Deployment
- Resources

Source: https://docs.polymarket.com/developers/CTF/deployment-resources

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

* [On-Chain Code Samples](https://github.com/Polymarket/examples/tree/main/examples)
* [Polygon RPC List](https://chainlist.org/chain/137)
* [CTF Source Code](https://github.com/gnosis/conditional-tokens-contracts)
* [Audits](https://github.com/gnosis/conditional-tokens-contracts/tree/master/docs/audit)
* [Gist For positionId Calculation](https://gist.github.com/L-Kov/950bce141a9d1aa1ed3b1cfce6d30217)

---

## Gamma Structure

**URL:** llms-txt#gamma-structure

Source: https://docs.polymarket.com/developers/gamma-markets-api/gamma-structure

Gamma provides some organizational models. These include events, and markets. The most fundamental element is always markets and the other models simply provide additional organization.

---

## Real Time Data Socket

**URL:** llms-txt#real-time-data-socket

**Contents:**
- Overview
  - Connection Details
  - Authentication
  - Connection Management
- Available Subscription Types
- Message Structure
- Subscription Management
  - Subscribe to Topics
  - Unsubscribe from Topics
- Error Handling

Source: https://docs.polymarket.com/developers/RTDS/RTDS-overview

The Polymarket Real-Time Data Socket (RTDS) is a WebSocket-based streaming service that provides real-time updates for various Polymarket data streams. The service allows clients to subscribe to multiple data feeds simultaneously and receive live updates as events occur on the platform.

<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

### Connection Details

* **WebSocket URL**: `wss://ws-live-data.polymarket.com`
* **Protocol**: WebSocket
* **Data Format**: JSON

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

All messages received from the WebSocket follow this structure:

* `topic`: The subscription topic (e.g., "crypto\_prices", "comments", "activity")
* `type`: The message type/event (e.g., "update", "reaction\_created", "orders\_matched")
* `timestamp`: Unix timestamp in milliseconds
* `payload`: Event-specific data object

## Subscription Management

### Subscribe to Topics

To subscribe to data streams, send a JSON message with this structure:

### Unsubscribe from Topics

To unsubscribe from data streams, send a similar message with `"action": "unsubscribe"`.

* Connection errors will trigger automatic reconnection attempts
* Invalid subscription messages may result in connection closure
* Authentication failures will prevent successful subscription to protected topics

**Examples:**

Example 1 (unknown):
```unknown
* `topic`: The subscription topic (e.g., "crypto\_prices", "comments", "activity")
* `type`: The message type/event (e.g., "update", "reaction\_created", "orders\_matched")
* `timestamp`: Unix timestamp in milliseconds
* `payload`: Event-specific data object

## Subscription Management

### Subscribe to Topics

To subscribe to data streams, send a JSON message with this structure:
```

---

## RTDS Crypto Prices

**URL:** llms-txt#rtds-crypto-prices

**Contents:**
- Overview
- Binance Source (`crypto_prices`)
  - Subscription Details
  - Subscription Message
  - With Symbol Filter
- Chainlink Source (`crypto_prices_chainlink`)
  - Subscription Details
  - Subscription Message
  - With Symbol Filter
- Message Format

Source: https://docs.polymarket.com/developers/RTDS/RTDS-crypto-prices

<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

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

### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a filters parameter:

## Chainlink Source (`crypto_prices_chainlink`)

### Subscription Details

* **Topic**: `crypto_prices_chainlink`
* **Type**: `*` (all types)
* **Authentication**: Not required
* **Filters**: Optional (JSON object with symbol specification)
* **Symbol Format**: Slash-separated pairs (e.g., `eth/usd`, `btc/usd`)

### Subscription Message

### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a JSON filters parameter:

### Binance Source Message Format

When subscribed to Binance crypto prices (`crypto_prices`), you'll receive messages with the following structure:

### Chainlink Source Message Format

When subscribed to Chainlink crypto prices (`crypto_prices_chainlink`), you'll receive messages with the following structure:

| Field       | Type   | Description                                                                                                                                                |
| ----------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `symbol`    | string | Trading pair symbol<br />**Binance**: lowercase concatenated (e.g., "solusdt", "btcusdt")<br />**Chainlink**: slash-separated (e.g., "eth/usd", "btc/usd") |
| `timestamp` | number | Price timestamp in Unix milliseconds                                                                                                                       |
| `value`     | number | Current price value in the quote currency                                                                                                                  |

### Binance Source Examples

#### Solana Price Update (Binance)

#### Bitcoin Price Update (Binance)

### Chainlink Source Examples

#### Ethereum Price Update (Chainlink)

#### Bitcoin Price Update (Chainlink)

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

* Price updates are sent as market prices change
* The timestamp in the payload represents when the price was recorded
* The outer timestamp represents when the message was sent via WebSocket
* No authentication is required for crypto price data

**Examples:**

Example 1 (unknown):
```unknown
### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a filters parameter:
```

Example 2 (unknown):
```unknown
## Chainlink Source (`crypto_prices_chainlink`)

### Subscription Details

* **Topic**: `crypto_prices_chainlink`
* **Type**: `*` (all types)
* **Authentication**: Not required
* **Filters**: Optional (JSON object with symbol specification)
* **Symbol Format**: Slash-separated pairs (e.g., `eth/usd`, `btc/usd`)

### Subscription Message
```

Example 3 (unknown):
```unknown
### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a JSON filters parameter:
```

Example 4 (unknown):
```unknown
## Message Format

### Binance Source Message Format

When subscribed to Binance crypto prices (`crypto_prices`), you'll receive messages with the following structure:
```

---

## RTDS Comments

**URL:** llms-txt#rtds-comments

**Contents:**
- Overview
- Subscription Details
- Subscription Message
- Message Format
- Message Types
  - comment\_created
  - comment\_removed
  - reaction\_created
  - reaction\_removed
- Payload Fields

Source: https://docs.polymarket.com/developers/RTDS/RTDS-comments

<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

The comments subscription provides real-time updates for comment-related events on the Polymarket platform. This includes new comments being created, as well as other comment interactions like reactions and replies.

## Subscription Details

* **Topic**: `comments`
* **Type**: `comment_created` (and potentially other comment event types like `reaction_created`)
* **Authentication**: May require Gamma authentication for user-specific data
* **Filters**: Optional (can filter by specific comment IDs, users, or events)

## Subscription Message

When subscribed to comments, you'll receive messages with the following structure:

Triggered when a user creates a new comment on an event or in reply to another comment.

Triggered when a comment is removed or deleted.

### reaction\_created

Triggered when a user adds a reaction to an existing comment.

### reaction\_removed

Triggered when a reaction is removed from a comment.

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

### New Comment Created

### Reply to Existing Comment

Comments support nested threading:

* **Top-level comments**: `parentCommentID` is null or empty
* **Reply comments**: `parentCommentID` contains the ID of the parent comment
* All comments are associated with a `parentEntityID` and `parentEntityType`

* Real-time comment feed displays
* Discussion thread monitoring
* Community sentiment analysis

* Comments include `reactionCount` and `reportCount`
* Comment body contains the full text content

* The `createdAt` timestamp uses ISO 8601 format with timezone information
* The outer `timestamp` field represents when the WebSocket message was sent
* User profiles include both primary addresses and proxy wallet addresses

**Examples:**

Example 1 (unknown):
```unknown
## Message Format

When subscribed to comments, you'll receive messages with the following structure:
```

Example 2 (unknown):
```unknown
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
```

Example 3 (unknown):
```unknown
### Reply to Existing Comment
```

---

## UMA Optimistic Oracle Integration

**URL:** llms-txt#uma-optimistic-oracle-integration

**Contents:**
- Overview
- Clarifications
- Resolution Process
  - Actions
  - Possible Flows
- Deployed Addresses
  - v3.0
  - v2.0
  - v1.0
- Additional Resources

Polymarket leverages UMA's Optimistic Oracle (OO) to resolve arbitrary questions, permissionlessly. From [UMA's docs](https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work):

"UMA's Optimistic Oracle allows contracts to quickly request and receive data information ... The Optimistic Oracle acts as a generalized escalation game between contracts that initiate a price request and UMA's dispute resolution system known as the Data Verification Mechanism (DVM). Prices proposed by the Optimistic Oracle will not be sent to the DVM unless it is disputed. If a dispute is raised, a request is sent to the DVM. All contracts built on UMA use the DVM as a backstop to resolve disputes. Disputes sent to the DVM will be resolved within a few days -- after UMA tokenholders vote on what the correct outcome should have been."

To allow CTF markets to be resolved via the OO, Polymarket developed a custom adapter contract called `UmaCtfAdapter` that provides a way for the two contract systems to interface.

Recent versions (v2+) of the `UmaCtfAdapter` also include a bulletin board feature that allows market creators to issue "clarifications". Questions that allow updates will include the sentence in their ancillary data:

"Updates made by the question creator via the bulletin board on 0x6A5D0222186C0FceA7547534cC13c3CFd9b7b6A4F74 should be considered. In summary, clarifications that do not impact the question's intent should be considered."

Where the [transaction](https://polygonscan.com/tx/0xa14f01b115c4913624fc3f508f960f4dea252758e73c28f5f07f8e19d7bca066) reference outlining what outlining should be considered.

## Resolution Process

* **Initiate** - Binary CTF markets are initialized via the `UmaCtfAdapter`'s `initialize()` function. This stores the question parameters on the contract, prepares the CTF and requests a price for a question from the OO. It returns a `questionID` that is also used to reference on the `UmaCtfAdapter`. The caller provides:
  1. `ancillaryData` - data used to resolve a question (i.e the question + clarifications)
  2. `rewardToken` - ERC20 token address used for payment of rewards and fees
  3. `reward` - Reward amount offered to a successful proposer. The caller must have set allowance so that the contract can pull this reward in.
  4. `proposalBond` - Bond required to be posted by OO proposers/disputers. If 0, the default OO bond is used.
  5. `liveness` - UMA liveness period in seconds. If 0, the default liveness period is used.

* **Propose Price** - Anyone can then propose a price to the question on the OO. To do this they must post the `proposalBond`. The liveness period begins after a price is proposed.

* **Dispute** - Anyone that disagrees with the proposed price has the opportunity to dispute the price by posting a counter bond via the OO, this proposed will now be escalated to the DVM for a voter-wide vote.

When the first proposed price is disputed for a `questionID` on the adapter, a callback is made and posted as the reward for this new proposal. This means a second `questionID`, making a new `questionID` to the OO (the reward is returned before the callback is made and posted as the reward for this new proposal). This allows for a second round of resolution, and correspondingly a second dispute is required for it to go to the DVM. The thinking behind this is to doubles the cost of a potential griefing vector (two disputes are required just one) and also allows far-fetched (incorrect) first price proposals to not delay the resolution. As such there are two possible flows:

* **Initialize (CTFAdapter) -> Propose (OO) -> Resolve (CTFAdapter)**
* **Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) -> Resolve (CTFAdaptor)**
* **Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) -> Challenge (CtfAdapter) -> Resolve (CTFAdaptor)**

## Deployed Addresses

| Network         | Address                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Polygon Mainnet | [0x2F5e3684cb1F318ec51b00Edba38d79Ac2c0aA9d](https://polygonscan.com/address/0x2F5e3684cb1F318ec51b00Edba38d79Ac2c0aA9d) |

| Network         | Address                                                                                                                     |
| --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Polygon Mainnet | [0x6A9D0222186C0FceA7547534cC13c3CFd9b7b6A4F74](https://polygonscan.com/address/0x6A9D222616C90FcA5754cd1333cFD9b7fb6a4F74) |

| Network         | Address                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Polygon Mainnet | [0xC8B122858a4EF82C2d4eE2E6A276C719e692995130](https://polygonscan.com/address/0xCB1822859cEF82Cd2Eb4E6276C7916e692995130) |

## Additional Resources

* [Audit](https://github.com/Polymarket/uma-ctf-adapter/blob/main/audit/Polymarket_UMA_Optimistic_Oracle_Adapter_Audit.pdf)
* [Source Code](https://github.com/Polymarket/uma-ctf-adapter)
* [UMA Documentation](https://docs.uma.xyz/)
* [UMA Oracle Portal](https://oracle.uma.xyz/)

---

## Resolution

**URL:** llms-txt#resolution

Source: https://docs.polymarket.com/developers/resolution/UMA

---
