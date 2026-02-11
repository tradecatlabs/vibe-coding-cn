# Changelog
Source: https://docs.coingecko.com/changelog

Product updates and announcements

export const GreenSeparator = () => (
  <div style={{
    height: '4px',
    background: 'linear-gradient(to right, transparent, #4BCC00, transparent)',
    margin: '20px 0 60px 0',
    border: 'none'
  }} />
);

<Update label="October 2025">
  ## Websocket is now supported for Self-serve API subscribers

  🗓️ **October 23, 2025**

  ### CoinGecko Websocket (Beta) is now available for [paid plan](https://www.coingecko.com/en/api/pricing) customers (Analyst plan & above)!

  For Analyst, Lite, Pro, and Pro+ self-serve customers, you are now eligible to access the following Websocket features, and stream real-time data by utilising your monthly API plan credits:

  * Max connections: 10 concurrent socket connections
  * Max subscriptions: 100 token or pool data subscription per channel, per socket
  * Channel Access: [all 4 channels](https://docs.coingecko.com/websocket#channel-%26-data-support)
  * Credit charge: **0.1** credit per response returned, deducting from monthly API plan credits

  Please visit [Websocket](https://docs.coingecko.com/websocket) for full details, and test out Websocket data streaming. We will gradually improve the Websocket and expand the feature limits. Please share your feedback and suggestion via this [**survey form**](https://forms.gle/gNE1Txc9FCV55s7ZA), or email soonaik\@coingecko\[dot]com .

  ### Notice: Temporary Disruption on MagicEden data for NFT Endpoints

  Due to recent updates to MagicEden's API, we are updating our integration. During this period, endpoints for NFT data may be temporarily unavailable or return incomplete information.

  <GreenSeparator />

  ## More Bonding Curve Support and New Ascending Sort for Megafilter

  🗓️ **October 4, 2025**

  ### Now supported Bonding Curve (non-graduated) Data for More Endpoints

  We've added support for bonding curve (e.g. launchpad graduation from PumpFun) data across multiple token endpoints:

  * [Token Data by Token Address](/reference/token-data-contract-address) — `/onchain/networks/{network}/tokens/{address}`
  * [Tokens Data by Token Addresses](/reference/tokens-data-contract-addresses) — `/onchain/networks/{network}/tokens/multi/{addresses}`
  * [Token Info by Token Address](/reference/token-info-contract-address) — `/onchain/networks/{network}/tokens/{address}/info`
  * [Pool Tokens Info by Pool Address](/reference/pool-token-info-contract-address) — `/onchain/networks/{network}/pools/{pool_address}/info`

  ```json JSON theme={null}
  "launchpad_details": {
    "graduation_percentage": 2.16,
    "completed": false,
    "completed_at": null,
    "migrated_destination_pool_address": null
  }
  ```

  ### Megafilter: Ascending Sort Order for Price Change %

  The [Megafilter for Pools](/reference/pools-megafilter) endpoint now supports ascending sorting for price change percentage:

  * `m5_price_change_percentage_asc`
  * `h1_price_change_percentage_asc`
  * `h6_price_change_percentage_asc`
  * `h24_price_change_percentage_asc`

  ### Token OHLCV Endpoint Fix to respect Specified Token Address

  We've fixed an issue where the [Token OHLCV chart by Token Address](/reference/token-ohlcv-token-address) endpoint returned data for the base token of the top pool instead of the requested token. It will now always return data for the specified token address.
</Update>

<Update label="September 2025">
  ## SDK Gains Public Treasury Coverage, MCP Adds Exchanges, NFTs, and ISO Support

  🗓️ **September 25, 2025**

  ### Expanded SDK Coverage for Public Treasuries

  We're broadening our SDK coverage to make treasury-level insights more powerful and easier to access. Check out what's new below (with functions from [our TypeScript SDK](https://github.com/coingecko/coingecko-typescript))

  * [`publicTreasury.getCoinID(coinID, { ...params })`](https://github.com/coingecko/coingecko-typescript/blob/main/api.md#publictreasury) \
    to query public companies & governments' cryptocurrency holdings by Coin ID
  * [`publicTreasury.getEntityID(entityID)`](https://github.com/coingecko/coingecko-typescript/blob/main/api.md#publictreasury) \
    to query public companies & governments' cryptocurrency holdings by Entity ID
  * [`entities.getList({ ...params })`](https://github.com/coingecko/coingecko-typescript/blob/main/api.md#entities) \
    to query all the supported entities on CoinGecko with entities ID, name, symbol, and country

  ### New MCP Tools: Exchanges, NFTs & Multi-Address Queries

  We're also surfacing new tools through the MCP to give developers a richer, faster way to query exchanges, NFTs, and onchain activity.

  * New tools:
    * Exchange coverage with [/exchanges/list](reference/exchanges-list), [/exchanges/](reference/exchanges-id), [/exchanges//tickers](reference/exchanges-id-tickers), and [/exchanges//volume\_chart/range](reference/exchanges-id-volume-chart-range)
    * NFT markets with [/nfts/markets](reference/nfts-markets)
    * Multi-address queries with [/onchain/networks//pools/multi/](reference/pools-addresses) and [/onchain/networks//tokens/multi/](reference/tokens-data-contract-addresses)
  * Retired tools:
    * We've removed endpoints such as [/coins/list](reference/coins-list), [/onchain/networks/trending\_pools](reference/trending-pools-network), and single-address pool/token queries in favor of more scalable multi-address endpoints

  ### Friendlier Time-related MCP Queries with ISO Support

  Time-based queries just got easier. MCP tools now accept **ISO date strings** (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`) alongside UNIX timestamps.

  For example, when using the [Coin Historical Chart Data within Time Range](reference/coins-id-market-chart-range) tool, you can now pass ISO date strings directly instead of converting them into UNIX timestamps for your LLM tools.

  **CoinGecko API Team**

  <GreenSeparator />

  ## New Crypto Treasury Endpoints and Improvements

  🗓️ **September 19, 2025**

  1. [Crypto Treasury Holdings by Coin ID](https://docs.coingecko.com/reference/companies-public-treasury) endpoint now supports governments and more coins data as seen on [https://www.coingecko.com/en/treasuries/bitcoin](https://www.coingecko.com/en/treasuries/bitcoin)
  2. **New endpoints:**
     1. [Crypto Treasury Holdings by Entity ID](https://docs.coingecko.com/reference/public-treasury-entity)
     2. [Entities List (ID Map)](https://docs.coingecko.com/reference/entities-list)
  3. [Derivatives Exchange Data by ID](https://docs.coingecko.com/reference/derivatives-exchanges-id) endpoint now supports `coin_id` and `target_coin_id` to identify coins of ticker pairs.

     ```json JSON theme={null}
     "tickers": [
       {
         "symbol": "ASTERUSDT",
         "base": "ASTER",
         "target": "USDT",
         "coin_id": "aster-2",  👈 NEW
         "target_coin_id": "tether"  👈 NEW
       }
     ]
     ```

  <GreenSeparator />

  ## Multiple Improvements: Bonding Curve Data, Pooled Token Balance, and More.

  🗓️ **September 12, 2025**

  ### 🚀 Now Supporting Bonding Curve Data

  Bonding curve data (launchpad graduation) is now supported for the followiing endpoints:

  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  * [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)

  **Payload example:**

  ```json  theme={null}
  "launchpad_details": {
    "graduation_percentage": 100,
    "completed": true,
    "completed_at": "2024-04-08T16:52:35Z",
    "migrated_destination_pool_address": "5wNu5QhdpRGrL37ffcd6TMMqZugQgxwafgz477rShtHy"  
  }
  ```

  More endpoints to support bonding curve data soon.

  ### 🚀 Now Supporting Pooled Token Balance Data

  The following endpoints now support additional pool token balance data by flagging this parameter `include_composition=true` :

  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  * [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)
  * [Token Data by Token Address](https://docs.coingecko.com/reference/token-data-contract-address) (requires `include=top_pools` parameter to be flagged together)
  * [Tokens Data by Token Addresses](https://docs.coingecko.com/reference/tokens-data-contract-addresses) (requires `include=top_pools` parameter to be flagged together)

  **Payload example:**

  ```json  theme={null}
  "base_token_balance": "11700.98",
  "base_token_liquidity_usd": "29630000",
  "quote_token_balance": "66384614.21",
  "quote_token_liquidity_usd": "66330000",  
  ```

  ### 🚀 Other improvements

  1. [Onchain Megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint now supports more `sort` options:
     * `m5_price_change_percentage_desc`
     * `h1_price_change_percentage_desc`
     * `h6_price_change_percentage_desc`
     * `fdv_usd_asc`
     * `fdv_usd_desc`
     * `reserve_in_usd_asc`
     * `reserve_in_usd_desc`
  2. [Top Gainers & Losers](https://docs.coingecko.com/reference/coins-top-gainers-losers) endpoint now supports additional price change percentage data by flagging `price_change_percentage` parameter. The available options are: `1h,24h,7d,14d,30d,60d,200d,1y`.
     * Payload example:

       ```json  theme={null}
       "usd_1y_change": 21740.8866287307,
       "usd_1h_change": -0.279590756868549,
       "usd_24h_change": 3.13876587906131,
       "usd_7d_change": -9.67782096261206,
       "usd_14d_change": -3.39755498745517,
       "usd_30d_change": -13.7768698159765,
       "usd_60d_change": 29.9096824213076,
       "usd_200d_change": 2282.33681679488
       ```
  3. [Exchange Tickers by ID](https://docs.coingecko.com/reference/exchanges-id-tickers) endpoint now supports to sort tickers based on market cap, by flagging the `order` parameter.
     * Available options: `market_cap_desc`, `market_cap_asc`
</Update>

<Update label="August 2025">
  ## Improved Update Frequency for selected Pro-API On-chain Endpoints

  🗓️ **August 18, 2025**

  \[Changes below are applicable to all [paid plan subscribers](https://www.coingecko.com/en/api/pricing).]

  Dear CoinGecko API paid plan subscribers,

  We're excited to announce an improvement to our API, aimed at providing you with even faster access to real-time data! Starting **02:00 UTC, September 2, 2025**, the edge cache duration for the following endpoints will be reduced from \*\*30s \*\*to **10s**, allowing you to retrieve updated data more frequently.

  | Endpoints                                                                                                    | Effective Date & Time                   | Current Update Frequency | New Update Frequency |
  | :----------------------------------------------------------------------------------------------------------- | :-------------------------------------- | :----------------------- | :------------------- |
  | [Token Price by Token Addresses](https://docs.coingecko.com/reference/onchain-simple-price)                  | Tuesday, 02:00 UTC, September 2, 2025   | 30s                      | 10s                  |
  | [Token Data by Token Address](https://docs.coingecko.com/reference/token-data-contract-address)              | Tuesday, 02:00 UTC, September 2, 2025   | 30s                      | 10s                  |
  | [Tokens Data by Token Addresses](https://docs.coingecko.com/reference/tokens-data-contract-addresses)        | Tuesday, 02:00 UTC, September 2, 2025   | 30s                      | 10s                  |
  | [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)                      | Wednesday, 02:00 UTC, September 3, 2025 | 30s                      | 10s                  |
  | [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)                | Wednesday, 02:00 UTC, September 3, 2025 | 30s                      | 10s                  |
  | [Pool OHLCV chart by Pool Address](https://docs.coingecko.com/reference/pool-ohlcv-contract-address)         | Thursday, 02:00 UTC, September 4, 2025  | 30s                      | 10s                  |
  | [Token OHLCV chart by Token Address](https://docs.coingecko.com/reference/token-ohlcv-token-address)         | Thursday, 02:00 UTC, September 4, 2025  | 30s                      | 10s                  |
  | [Past 24 Hour Trades by Pool Address](https://docs.coingecko.com/reference/pool-trades-contract-address)     | Thursday, 02:00 UTC, September 4, 2025  | 30s                      | 10s                  |
  | [Past 24 Hour Trades by Token Address](https://docs.coingecko.com/reference/token-trades-contract-address#/) | Thursday, 02:00 UTC, September 4, 2025  | 30s                      | 10s                  |

  #### **What This Means for You:**

  * **Fresher Data, Quicker**: With a reduced cache time, you'll now have the option to access more up-to-date data, closer to real-time!
  * **No Extra Credits for Cached Data**: If your request hits the cache (now updated every 10 seconds for endpoints above), there will be no additional credits charged - just like before.

  **Things to Keep in Mind:**

  * If your request hits our origin server instead of the cache to retrieve the latest data, there may be additional credits used.
  * To balance cost and real-time data needs, we recommend reviewing your request frequency. For those who prefer to obtain data without extra credits, consider keeping your request interval at 30 seconds or more to align with the new cache duration.

  We're committed to continuously improving your experience and ensuring you get the data you need, as efficiently as possible. If you have any questions or need assistance, feel free to reach out to [soonaik@coingecko.com](mailto:soonaik@coingecko.com) .

  **CoinGecko API Team**

  <GreenSeparator />

  ## Now Supported: Launchpad Data (Pump.fun & More), Granular OHLCV, and Honeypot Info

  🗓️ **August 05, 2025**

  We're excited to announce a major update to our on-chain API endpoints! This release introduces support for popular token launchpads, adds high-frequency OHLCV data, and enhances our honeypot detection capabilities to give you deeper and more timely on-chain insights.

  ### 🚀 Now Supporting Launchpad Data (Pump.fun & More!)

  In addition to the 1,600+ DEXes already integrated with GeckoTerminal.com, you can now track token data from popular launchpad platforms directly through the CoinGecko API. More launchpads will be supported soon!

  **New Supported Launchpads:**

  | Launchpad                                                                                       | network id (API) | dex id (API)      |
  | :---------------------------------------------------------------------------------------------- | :--------------- | :---------------- |
  | [Meteora DBC](https://www.geckoterminal.com/solana/meteora-dbc/pools)                           | solana           | meteora-dbc       |
  | [Pump.fun](https://www.geckoterminal.com/solana/pump-fun/pools)                                 | solana           | pump-fun          |
  | [Raydium Launchpad](https://www.geckoterminal.com/solana/raydium-launchlab/pools) (LetsBonkFun) | solana           | raydium-launchlab |
  | [Boop.fun](https://www.geckoterminal.com/solana/boop-fun/pools)                                 | solana           | boop-fun          |
  | [Virtuals (Base)](https://www.geckoterminal.com/base/virtuals-base/pools)                       | base             | virtuals-base     |

  **Improved endpoints to track launchpad data:**

  * [Token Data by Token Address](https://docs.coingecko.com/reference/token-data-contract-address)
  * [Tokens Data by Token Addresses](https://docs.coingecko.com/reference/tokens-data-contract-addresses)
  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  * [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)

  More launchpad-specific data will be supported soon for the endpoints above!

  **Tips:** use [megafilter endpoint](https://docs.coingecko.com/reference/pools-megafilter) to retrieve latest launchpad data, by flagging `sort=pool_created_at_desc`

  **Request example** (Get latest pools on Pump.fun):

  ```curl  theme={null}
  https://pro-api.coingecko.com/api/v3/onchain/pools/megafilter?page=1&networks=solana&dexes=pump-fun&sort=pool_created_at_desc&x_cg_pro_api_key=YOUR_KEY
  ```

  ### \[Pro-API Exclusive] More Granular OHLCV Data

  On-chain OHLCV endpoints now support higher frequency intervals, down to 1-second granularity.

  | Timeframe | Aggregate (Before) | Aggregate (New) |
  | :-------- | :----------------- | :-------------- |
  | day       | 1                  | 1               |
  | hour      | 1, 4, 12           | 1, 4, 12        |
  | minute    | 1, 5, 15           | 1, 5, 15        |
  | second    | n/a                | 1, 15, 30       |

  **Improved Endpoints:**

  * [Pool OHLCV chart by Pool Address](https://docs.coingecko.com/reference/pool-ohlcv-contract-address)
  * [Token OHLCV chart by Token Address](https://docs.coingecko.com/reference/token-ohlcv-token-address)

  **New interval supported:**

  * 1s
  * 15s
  * 30s

  **Example Request (Get the last 100 1-second intervals for a pool on Ethereum):**

  ```curl  theme={null}
  https://pro-api.coingecko.com/api/v3/onchain/networks/eth/pools/0x06da0fd433c1a5d7a4faa01111c044910a184553/ohlcv/second?aggregate=1&limit=100&include_empty_intervals=false&x_cg_pro_api_key=YOUR_KEY
  ```

  ### 🍯 Enhanced Honeypot Information

  We've expanded our honeypot detection features to provide more comprehensive risk assessment. You can now check if a token is a potential honeypot using the main info endpoints.

  **Improved Endpoints:**

  * [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  * [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)

  **Example Payload:**

  ```json  theme={null}
  {
   "mint_authority": null,
   "freeze_authority": null,
   "is_honeypot": true  // possible values: true / false / unknown
  }
  ```

  ### \[Pro-API Exclusive] New Filtering Option in Megafilter

  Previously, the[Pools Megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint could only show tokens confirmed as ***not*** a honeypot (`checks=no_honeypot`). Now, you can also include tokens where the honeypot status is 'unknown'.

  * To use this, set `include_unknown_honeypot_tokens=true`.
  * Important: This parameter only takes effect when `checks=no_honeypot` is also specified in the request.

  **Example Request (Get trending pools that are not confirmed honeypots, including those with an unknown status):**

  ```curl  theme={null}
  https://pro-api.coingecko.com/api/v3/onchain/pools/megafilter?page=1&sort=h6_trending&checks=no_honeypot&include_unknown_honeypot_tokens=true&x_cg_pro_api_key=YOUR_KEY
  ```

  ### 📈 Expanded Pool Data

  **Endpoint**: [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)

  By adding `include=pool` to your request on the pool tokens endpoint, you can now retrieve additional context about the pool itself.

  * Base and quote token address
  * Sentiment vote percentage (positive and negative)
  * Community suspicious reports count

  **Payload Example**:

  ```json  theme={null}
    "included": [
      {
        "id": "eth_0x06da0fd433c1a5d7a4faa01111c044910a184553",
        "type": "pool",
        "attributes": {
          "base_token_address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
          "quote_token_address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
          "sentiment_vote_positive_percentage": 100,
          "sentiment_vote_negative_percentage": 0,
          "community_sus_report": 0
        }
      }
    ]
  ```
</Update>

<Update label="June 2025">
  ## SOL Currency Is Now Supported for CoinGecko Endpoints

  🗓️ **June 19, 2025**

  We're excited to announce that you can now obtain real-time and historical price & market data for tokens listed on CoinGecko.com, with the option to return data value in **SOL** (Solana) currency.

  Note: for dates prior to May 2025, 'SOL' historical data is limited to hourly and daily granularity

  #### **Improved endpoints:**

  * [Coin Price by IDs](https://docs.coingecko.com/reference/simple-price)
  * [Coin Price by Token Addresses](https://docs.coingecko.com/reference/simple-token-price)
  * [Supported Currencies List](https://docs.coingecko.com/reference/simple-supported-currencies)
  * [Top Gainers & Losers](https://docs.coingecko.com/reference/coins-top-gainers-losers)
  * [Coins List with Market Data](https://docs.coingecko.com/reference/coins-markets)
  * [Coin Data by ID](https://docs.coingecko.com/reference/coins-id)
  * [Coin Historical Data by ID](https://docs.coingecko.com/reference/coins-id-history)
  * [Coin Historical Chart Data by ID](https://docs.coingecko.com/reference/coins-id-market-chart)
  * [Coin Historical Chart Data within Time Range by ID](https://docs.coingecko.com/reference/coins-id-market-chart-range)
  * [Coin OHLC Chart by ID](https://docs.coingecko.com/reference/coins-id-ohlc)
  * [Coin OHLC Chart within Time Range by ID](https://docs.coingecko.com/reference/coins-id-ohlc-range)
  * [Coin Data by Token Address](https://docs.coingecko.com/reference/coins-contract-address)
  * [Coin Historical Chart Data by Token Address](https://docs.coingecko.com/reference/contract-address-market-chart)
  * [Coin Historical Chart Data within Time Range by Token Address](https://docs.coingecko.com/reference/contract-address-market-chart-range)
  * [Trending Search List](https://docs.coingecko.com/reference/trending-search)
  * [Crypto Global Market Data](https://docs.coingecko.com/reference/crypto-global)

  **Example**: price of Bitcoin in Solana, using [Coin Price by IDs](https://docs.coingecko.com/reference/simple-price) endpoint.

  ```json  theme={null}
  {
    "bitcoin": {
      "sol": 720.21
    }
  }
  ```

  **Example:** historical daily price, market cap and volume of Trump in Solana, using [Coin Historical Chart Data by ID](https://docs.coingecko.com/reference/coins-id-market-chart) endpoint.

  ```json  theme={null}
  {
    "prices": [
      [
        1750118400000,
        0.0640701365814472
      ],
      [
        1750204800000,
        0.0644263929356261
      ],
      [
        1750291200000,
        0.0639713357587322
      ],
      [
        1750326151000,
        0.06415963364804504
      ]
    ],
    "market_caps": [
      [
        1750118400000,
        12843589.584485611
      ],
      [
        1750204800000,
        12882547.839086628
      ],
      [
        1750291200000,
        12793790.726102708
      ],
      [
        1750326151000,
        12826247.390733324
      ]
    ],
    "total_volumes": [
      [
        1750118400000,
        2425793.780846796
      ],
      [
        1750204800000,
        2055697.9106767387
      ],
      [
        1750291200000,
        1871087.4334618242
      ],
      [
        1750326151000,
        2008278.189223005
      ]
    ]
  }
  ```

  <GreenSeparator />

  ## New Endpoints & Improvements: Historical Token Holders Chart, OHLCV by Token Address, Multi-pool Token Data Support

  🗓️ **June 09, 2025**

  ### \[Pro-API Exclusive] New Endpoint  - Historical Token Holders Chart by Token Address

  This new endpoint allows you to get the historical token holders chart based on the provided token contract address on a network.

  * Supported chains include: Solana, EVM (Ethereum, Polygon, BNB, Arbitrum, Optimism, Base), Sui, TON, and Ronin.

  Check it out now: [Historical Token Holders Chart by Token Address](https://docs.coingecko.com/reference/token-holders-chart-token-address)

  ### \[Pro-API Exclusive] New Endpoint  - Token OHLCV chart by Token Address

  This endpoint allows you to get the OHLCV chart (Open, High, Low, Close, Volume) of a token based on the provided token address on a network.

  * This endpoint will return OHLCV data of the most liquid pool of the specified token. You may use this endpoint Top Pools by Token Address to check the top pools of a token.

  Check it out now: [Token OHLCV chart by Token Address](https://docs.coingecko.com/reference/token-ohlcv-token-address#/)

  ### Improved Endpoints - Support Multi-pool Token Data

  Previously, we only surfaced 1 quote token for pools with more than 2 tokens.  With this new improvements, for pools that have 2 or more tokens:

  * Extra quote tokens being listed under a new key `relationships.quote_tokens`
  * If `include=quote_token` is flagged, the extra quote tokens will be also listed under `included`

  ```json  theme={null}
      "relationships": {  
        "base_token": {
          "data": {
            "id": "eth_0x40d16fc0246ad3160ccc09b8d0d3a2cd28ae6c2f",
            "type": "token"
          }
        },
        "quote_token": {
          "data": {
            "id": "eth_0x8353157092ed8be69a9df8f95af097bbf33cb2af",
            "type": "token"
          }
        },
        "quote_tokens": {
          "data": [
            {
              "id": "eth_0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
              "type": "token"
            },
            {
              "id": "eth_0xdac17f958d2ee523a2206206994597c13d831ec7",
              "type": "token"
            }
  ```

  This improvement is applicable to all onchain pool endpoints that support `relationships.quote_token`, including but not limited to:

  * [Top Pools by Token Address](https://docs.coingecko.com/reference/top-pools-contract-address#/)
  * [Search Pools](https://docs.coingecko.com/reference/search-pools#/)
  * [Megafilter for Pools](https://docs.coingecko.com/reference/pools-megafilter#/)
  * [Trending Pools List](https://docs.coingecko.com/reference/trending-pools-list#/)
  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address#/)
  * [Top Pools by Network](https://docs.coingecko.com/reference/top-pools-network#/)
  * [New Pools List](https://docs.coingecko.com/reference/latest-pools-list#/)
</Update>

<Update label="May 2025">
  ## Upcoming Change Notice: Removal of normalized\_volume\_btc Data

  🗓️ **May 30, 2025**

  **`Notice: Upcoming Change to CoinGecko API Endpoints - Removal ofnormalized_volume_btc Data`**

  **Effective Date: 16 June 2025**

  **Affected Endpoints:**

  * [Exchange Data by ID](https://docs.coingecko.com/reference/exchanges-id)
  * [Exchanges List with Data](https://docs.coingecko.com/reference/exchanges#/)

  **Details of the Change:**

  Please be advised that the `normalized_volume_btc` data point will be removed from the above-listed API endpoints, effective 16 June 2025. This change is being implemented due to significant recent change to a 3rd party data source provider, which have fundamentally altered how this specific data can be accessed.

  Example of Affected Data Structure:

  ```json  theme={null}
    {
      "trade_volume_24h_btc_normalized": 47765.5886637453
    },
  ```

  After the effective date, the `trade_volume_24h_btc_normalized` field will no longer be present in the API responses for these endpoints.

  **Action Required:**

  If your applications or integrations currently rely on the `trade_volume_24h_btc_normalized` data from these CoinGecko API endpoints, please make the necessary adjustments to your code before 16 June 2025 to avoid potential errors or data discrepancies.

  <GreenSeparator />

  ## New Endpoint & Improvements: On-Chain Trades, Net Buy Volume, and More

  🗓️ **May 29, 2025**

  ### \[Pro-API Exclusive] New Endpoint  - On-chain Trades by Token Address

  Previously, the [Past 24 Hour Trades by Pool Address](https://docs.coingecko.com/reference/pool-trades-contract-address) endpoint allows you to retrieve the last 300 trades of a specific pool only.

  With this new endpoint [Past 24 Hour Trades by Token Address](https://docs.coingecko.com/reference/token-trades-contract-address), you can now retrieve the last 300 trades **across different pools**, based on the provided **token contract address** on a network.

  ### Improved Endpoints - Support Net Buy Volume Data

  The following endpoints now support more volume breakdown data:

  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  * [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses#/)

  By flagging `include_volume_breakdown=true` , you can surface the following data:

  * net\_buy\_volume\_usd
  * buy\_volume\_usd
  * sell\_volume\_usd

  Sample Response:

  ```json JSON theme={null}
  {
    "data": {
      "id": "eth_0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
      "type": "pool",
      "attributes": {
        ...
        },
        "net_buy_volume_usd": {
          "m5":  "-40796.577553965",
          "m15": "-69765.771189161",
          "m30": "-88014.095440243",
          "h1":   "0.000000000000",
          "h6":   "1884879.921855301",
          "h24":  "17555422.243003801"
        },
        "buy_volume_usd": {
          "m5":  "30597.433165473",
          "m15": "139531.542378324",
          "m30": "396063.429481099",
          "h1":  "969922.728762430",
          "h6":  "10366839.570204150",
          "h24": "52666266.729011402"
        },
        "sell_volume_usd": {
          "m5":  "71394.010719438",
          "m15": "209297.313567485",
          "m30": "484077.524921342",
          "h1":  "969922.728762430",
          "h6":  "8481959.648348849",
          "h24": "35110844.486007601"
        },
  ```

  ### Improved Endpoint - On-Chain OHLCV endpoint

  [Pool OHLCV chart by Pool Address](https://docs.coingecko.com/reference/pool-ohlcv-contract-address) endpoint now supports to include empty intervals by flagging `include_empty_intervals=true` .

  * By default, specific timeframe intervals (e.g. minutely) with no recorded swaps are excluded (or **skipped**) from the response.
  * This new parameter option provides the flexibility to get **padded** data, when there's no trade data.

  Sample Response:

  ```json  theme={null}
  {
    "data": {
      "id": "81da0682-1c4f-445a-9bed-9b5454004df5",
      "type": "ohlcv_request_response",
      "attributes": {
        "ohlcv_list": [
          [
            1744712700,
            0.000212149802253853,
            0.000212173305907688,
            0.000212149802253853,
            0.000212173305907688,
            46.48164903882
          ],
          [
            1744712400,
            0.000212149802253853,  👈 O — Follow previous Close value
            0.000212149802253853,  👈 H — Follow previous Close value
            0.000212149802253853,  👈 L — Follow previous Close value
            0.000212149802253853,  👈 C — Follow previous Close value
            0.0  👈 V — Set to zero
          ],
          [
            1744712100,
            0.000210532522666822,
            0.000212149802253853,
            0.000210532522666822,
            0.000212149802253853,  👈 Previous Close value
            46.4765
          ],
  ...
  }
  ```

  ### Improved Endpoints - Support Large Images

  The following endpoints now support more size options for coin logo image:

  * [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  * [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-addres)

  Sample Response:

  ```json  theme={null}
    "data": {
      "id": "eth_0xdac17f958d2ee523a2206206994597c13d831ec7",
      "type": "token",
      "attributes": {
  ...
        "image_url": "https://assets.coingecko.com/coins/images/325/small/Tether.png?1696501661",
        "image": {
          "thumb": "https://assets.coingecko.com/coins/images/325/thumb/Tether.png?1696501661",
          "small": "https://assets.coingecko.com/coins/images/325/small/Tether.png?1696501661",
          "large": "https://assets.coingecko.com/coins/images/325/large/Tether.png?1696501661"
        },
  ```

  ### Improved Endpoints - Support Normalized Supply Data

  The following endpoints now support `normalized_total_supply`:

  * [Token Data by Token Address](https://docs.coingecko.com/reference/token-data-contract-address)
  * [Tokens Data by Token Addresses](https://docs.coingecko.com/reference/tokens-data-contract-addresses)

  Sample Response:

  ```json  theme={null}
        "decimals": 6,
        "total_supply": "49999156520373530.0",
        "normalized_total_supply": "49999156520.37353",
  ```

  ### Improved Endpoints - Support Pool 'Name' and 'Fee' Data

  The following endpoints now support `pool_name` and `pool_fee`:

  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  * [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)

  Sample Response:

  ```json  theme={null}
          "name": "WETH / USDC 0.05%",
          "pool_name": "WETH / USDC",
          "pool_fee_percentage": "0.05",
  ```

  ### Improved Endpoints - Support Symbols of DEX Pairs

  The following endpoints now allow to flag `dex_pair_format=symbol` to return DEX pair symbols instead of contract address.

  * [Coin Data by ID](https://docs.coingecko.com/reference/coins-id)
  * [Coin Tickers by ID](https://docs.coingecko.com/reference/coins-id-tickers)
  * [Exchange Tickers by ID](https://docs.coingecko.com/reference/exchanges-id-tickers)
  * [Exchange Data by ID](https://docs.coingecko.com/reference/exchanges-id)

  Sample Response:

  ```json  theme={null}
  // before
  {
        "base": "0X8FC8F8269EBCA376D046CE292DC7EAC40C8D358A",
        "target": "0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48",
        "market": {
          "name": "Uniswap V2 (Ethereum)",
          "identifier": "uniswap_v2",
  ...
  }

  // now when "dex_pair_format=symbol" is flagged
  {
        "base": "DFI",
        "target": "USDC",
        "market": {
          "name": "Uniswap V2 (Ethereum)",
          "identifier": "uniswap_v2",
  ...
  }
  ```
</Update>

<Update label="April 2025">
  ## New Endpoint & Improvements: On-Chain Trending Data, Enhanced Trending Search, and Improved Token Lookup

  🗓️ **April 25, 2025**

  ### \[Pro-API Exclusive] New Endpoint  - On-chain Trending Search Data

  With this new endpoint [Trending Search Pools](https://docs.coingecko.com/reference/trending-search-pools), you can now retrieve the on-chain trending search pools and tokens data, as seen on GeckoTerminal.com .

  By default, this endpoint returns the top 4 trending pools data, you may specify the `pools` parameter to retrieve up to top 10 pools data.

  Tips: you may flag `include=base_token` to retrieve the trending tokens data.

  Note:  this exclusive endpoint is available for our API [paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above).

  ### \[Pro-API Exclusive] Improved Endpoint - Trending Search List

  [Paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above) can now use [Trending Search List](https://docs.coingecko.com/reference/trending-search) endpoint and flag `show_max` parameter to retrieve more trending coins, NFTs and coin categories on CoinGecko.com.

  | Trending Data   | Public API (Demo plan) | Paid API (Analyst plan & above) |
  | :-------------- | :--------------------- | :------------------------------ |
  | Coins           | 15                     | 30                              |
  | NFTs            | 7                      | 10                              |
  | Coin Categories | 6                      | 10                              |

  ### Improved Endpoints - Support Token Lookup by Symbol and Name

  The following endpoints now support token lookup by symbol and name, in addition to the existing API ID support:

  * [Coin Price by IDs and Symbols](https://docs.coingecko.com/reference/simple-price)
  * [Coins List with Market Data](https://docs.coingecko.com/reference/coins-markets)

  Previously, these endpoints only supported token lookup by \[API IDs]\([https://docs.coingecko.com/docs/1-get-data-by-id-or-address#/methods-to-query-price--market-data-of-coins](https://docs.coingecko.com/docs/1-get-data-by-id-or-address#/methods-to-query-price--market-data-of-coins\)).  This enhancement streamlines token data retrieval and eliminates the need for manual coin ID mapping.

  Example Mapping:

  | API Ids  | Symbol | Name    |
  | :------- | :----- | :------ |
  | bitcoin  | btc    | Bitcoin |
  | tether   | usdt   | Tether  |
  | usd-coin | usdc   | USDC    |

  Lookup Priority: When multiple lookup parameters are provided, the system applies the following priority order: id (highest) > name > symbol (lowest).

  **`Filtering by Symbol withinclude_tokens`**

  The `include_tokens`parameter has been added to provide flexibility when filtering by symbol:

  * `include_tokens=top` : Returns only the top market cap token for the specified symbol.
  * `include_tokens=all`: Returns all tokens that share the specified symbol.

  Example Request & Data:

  | Request Example                                                                               | Token Data Returned                                                                                              | Remarks                                                                                                                                                                                          |
  | :-------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | pro-api.coingecko.com/api/v3/coins/markets?vs\_currency=usd\&symbols=btc\&include\_tokens=top | 1. Bitcoin                                                                                                       | When symbols and 'include\_tokens=**top**' is specified, only the top market cap tokens will be returned.                                                                                        |
  | pro-api.coingecko.com/api/v3/coins/markets?vs\_currency=usd\&symbols=btc\&include\_tokens=all | 1. Bitcoin<br />2. Osmosis allBTC<br />3. atcat<br />4. Meld Bridged BTC (Meld)<br />5. BlackrockTradingCurrency | When symbols and 'include\_tokens=**all**' is specified, all the coins that share the same symbol will be returned.<br /><br />All the 5 coins stated in the example have the same symbol 'btc'. |

  ### /coins/markets Endpoint Improvement

  We've enhanced the`/coins/markets` endpoint [Coins List with Market Data](https://docs.coingecko.com/reference/coins-markets), by including 'total' and 'per-page' values in the Response Headers.

  This addition to the Response Headers enables developers to identify the total number of active coins on coingecko.com and specify the required pagination to retrieve all available data.

  ```Text Response Header (Example) theme={null}
  per-page: 250
  total:16989
  ```

  <GreenSeparator />

  ## Upcoming Change Notice: Removal of twitter\_followers Data

  🗓️ **April 25, 2025**

  **`Notice: Upcoming Change to CoinGecko API Endpoints - Removal oftwitter_followers Data`**

  **Effective Date: 15 May 2025**

  **Affected Endpoints:**

  * [Coin Data by ID](https://docs.coingecko.com/reference/coins-id)
  * [Coin Data by Token Address](https://docs.coingecko.com/reference/coins-contract-address)
  * [Coin Historical Data by ID](https://docs.coingecko.com/reference/coins-id-history)

  **Details of the Change:**

  Please be advised that the `twitter_followers` data point within the `community_data` object will be removed from the above-listed API endpoints, effective 15 May 2025. This change is being implemented due to significant recent changes to the X (formerly Twitter) API, which have fundamentally altered how this specific data can be accessed.

  Example of Affected Data Structure:

  ```json  theme={null}
  "community_data": {  
    "twitter_followers": 7694251,
    // ... other community data points ...
  }
  ```

  After the effective date, the `twitter_followers` field will no longer be present in the API responses for these endpoints.

  **Action Required:**

  If your applications or integrations currently rely on the `twitter_followers` data from these CoinGecko API endpoints, please make the necessary adjustments to your code before 15 May 2025 to avoid potential errors or data discrepancies.

  **`Important Note Regarding Previously Storedtwitter_followers Data:`**

  Please be aware that if you have previously stored `twitter_followers` data obtained from the CoinGecko API and archived it within your own systems, you are solely responsible for its continued use and any implications thereof.

  We appreciate your understanding as we adapt to changes in third-party platforms to maintain the stability and reliability of our API. If you have any questions or require further clarification, please do not hesitate to contact our support team.
</Update>

<Update label="March 2025">
  ## New Endpoint & Multiple Improvements: On-Chain Top Token Holder Address, Security Data, Historical Supply.

  🗓️ **March 28, 2025**

  ### \[Pro-API Exclusive] New Endpoint  - Top Token Holder Address Data

  You can now access the top 50 token holder address data for tokens, as seen on GeckoTerminal.com.

  By default, this endpoint returns the top 10 holders data, you can also specify the `holders` parameter to retrieve up to top 50 holders data.

  **Network supported:**

  * EVM: Ethereum, Polygon, BNB, Arbitrum, Optimism, Base
  * Solana
  * Sui
  * TON
  * Ronin

  👉 Visit the endpoint reference page - [Top Token Holders by Token Address](https://docs.coingecko.com/reference/top-token-holders-token-address) to learn more and try it out now!

  **Note:**  this exclusive endpoint is available for our API [paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above).

  * The holders data is currently in **Beta**, with ongoing improvements to data quality, coverage, and update frequency.
  * For Solana tokens, the maximum number of retrievable top holders data is 40 instead of 50.

  **Tips:** You may also use the following endpoints to retrieve **token holders count** and **top holders distribution percentage data**:

  * [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  * [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)

  ### Historical Supply endpoints - Support for Inactive Coins

  You may now access historical total and circulating supply data of inactive coins using the following endpoints. To check for list of inactive coins, you may use [Coin List (ID Map)](https://docs.coingecko.com/reference/coins-list) endpoint and flag `status=inactive`.

  Note: these endpoints below are exclusive for [Enterprise plan](https://www.coingecko.com/en/api/pricing) customers only.

  **Improved endpoints:**

  * [Circulating Supply Chart by ID](https://docs.coingecko.com/reference/coins-id-circulating-supply-chart)
  * [Circulating Supply Chart within Time Range by ID](https://docs.coingecko.com/reference/coins-id-circulating-supply-chart-range)
  * [Total Supply Chart by ID](https://docs.coingecko.com/reference/coins-id-total-supply-chart)
  * [Total Supply Chart within time range by ID](https://docs.coingecko.com/reference/coins-id-total-supply-chart-range)

  ### Onchain Pool Data endpoints - Locked Liquidity

  Now support **`locked_liquidity_percentage`** data.

  **Improved endpoints:**

  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  * [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)

  ```json  theme={null}
  {
    "data": [
      {
        "id": "eth_0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
        "type": "pool",
        "attributes": {
          "base_token_price_usd": "3653.12491645176",
          "base_token_price_native_currency": "1.0",
  ..
          "volume_usd": {
            "m5": "868581.7348314",
            "h1": "16798158.0138526",
            "h6": "164054610.850188",
            "h24": "536545444.904535"
          },
          "reserve_in_usd": "163988541.3812",
          "locked_liquidity_percentage": "99.82"
        },
  ```

  ### Onchain Token Info endpoints - GT Score, Mint Authority, Freeze Authority

  The following Token Info endpoints now provide more security related information:

  * **GeckoTerminal Score Details** - Learn more about GT Score [here](https://support.coingecko.com/hc/en-us/articles/38381394237593-What-is-GT-Score-How-is-GT-Score-calculated).
    * **Pool** - Combination of pool signals such as honeypot risk, buy/sell tax, proxy contract, liquidity amount, and whether the liquidity is locked.
    * **Transaction** - Total number of transactions and trading volume in the last 24 hours.
    * **Creation** - Age of the pool since creation. The longer, the better it is for the score.
    * **Info** - Submitted social info and metadata to the token.
    * **Holders** - Distribution of tokens among unique addresses.
  * **Mint Authority**
  * **Freeze Authority**

  **Improved endpoints:**

  * [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  * [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)

  ```json  theme={null}
          "gt_score": 92.6605504587156,    
          "gt_score_details": {
            "pool": 0,
            "transaction": 32.2,
            "creation": 0,
            "info": 0,
            "holders": 0
          }
          "mint_authority": "no",   
          "freeze_authority": "no" 
  ```

  ### Onchain Simple Token Price endpoint - Market Cap to FDV Fallback

  The [Onchain Simple Token Price](https://docs.coingecko.com/reference/onchain-simple-price) endpoint now supports fallback option for Market Cap to return FDV value, when the Market Cap value is not available.

  Notes:

  * If the token's market cap is not verified by the CoinGecko team, the onchain endpoints will return **null** for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.

  If you require the Market Cap key (`market_cap_usd`) to return FDV value (as seen on GeckoTerminal.com) when Market Cap data is unavailable, please specify this parameter `marketcap_fdv_fallback=true`.

  <GreenSeparator />

  ## Update Frequency Improvements for selected Pro-API endpoints (March 2025)

  🗓️ **March 14, 2025**

  \[Changes below are applicable to Analyst/Lite/Pro/Enterprise [plan subscribers](https://www.coingecko.com/en/api/pricing) only.]

  Dear CoinGecko API paid plan subscribers,

  We're excited to announce an improvement to our API, aimed at providing you with even faster access to real-time data! Starting **02:00 UTC, March 25, 2025**, the edge cache duration for the following endpoints will be reduced from 60s to 30s, allowing you to retrieve updated data more frequently.

  1. Effective from 02:00 UTC, March 25, 2025:
     1. [Trending Pools List](https://docs.coingecko.com/reference/trending-pools-list)
     2. [Trending Pools by Network](https://docs.coingecko.com/reference/trending-pools-network)
     3. [Top Pools by Network](https://docs.coingecko.com/reference/top-pools-network)
     4. [Top Pools by Dex](https://docs.coingecko.com/reference/top-pools-dex)
  2. Effective from 02:00 UTC, March 26, 2025:
     1. [New Pools by Network](https://docs.coingecko.com/reference/latest-pools-network)
     2. [New Pools List](https://docs.coingecko.com/reference/latest-pools-list)
     3. [ Megafilter for Pools](https://docs.coingecko.com/reference/pools-megafilter)
     4. [Search Pools](https://docs.coingecko.com/reference/search-pools)
  3. Effective from 02:00 UTC, March 27, 2025:
     1. [Top Pools by Token Address](https://docs.coingecko.com/reference/top-pools-contract-address)
     2. [Most Recently Updated Tokens List](https://docs.coingecko.com/reference/tokens-info-recent-updated)
     3. [Pools by Category ID](https://docs.coingecko.com/reference/pools-category)

  **What This Means for You:**

  * **Fresher Data, Quicker**: With a reduced cache time, you'll now have the option to access more up-to-date data, closer to real-time!
  * **No Extra Credits for Cached Data**: If your request hits the cache (now updated every 30 seconds for endpoints above), there will be no additional credits charged—just like before.

  **Things to Keep in Mind:**

  * If your request hits our origin server instead of the cache to retrieve the latest data, there may be additional credits used.
  * To balance cost and real-time data needs, we recommend reviewing your request frequency. For those who prefer to obtain data without extra credits, consider keeping your request interval at 60 seconds or more to align with the new cache duration.

  We're committed to continuously improving your experience and ensuring you get the data you need, as efficiently as possible. If you have any questions or need assistance, feel free to reach out to [soonaik@coingecko.com](mailto:soonaik@coingecko.com) .

  **CoinGecko API Team**

  <GreenSeparator />

  ## Multiple Improvement: Holders data, Pool Stats, Simple Token Price

  🗓️ **March 14, 2025**

  ### Onchain Token Info endpoints - Holders data

  Now support the following holder data **(Beta)**:

  * holders count
  * top holders distribution percentage

  **Improved endpoints:**

  * [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  * [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)

  ```json  theme={null}
      "holders": {
        "count": 1432761,
        "distribution_percentage": {
          "top_10": "1.3019",
          "11_20": "0.1024",
          "21_40": "0.095",
          "rest": "98.5007"
        },
        "last_updated": "2025-03-06T01:21:18Z"
  ```

  ### Onchain Pool Data endpoints - More Data Support

  Now support the following data:

  * `price_change_percentage`: m15, m30
  * `volume_usd`: m15, m30
  * `transactions`: h6

  **Improved endpoints:**

  * [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  * [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)

  ```json  theme={null}
          "price_change_percentage": {
            "m5": "0.06",
            "m15": "0.06",
            "m30": "0.89",
            "h1": "-4.31",
            "h6": "-1.02",
            "h24": "3.32"
          },
          "transactions": {
            "m5": {
              "buys": 0,
              "sells": 2,
              "buyers": 0,
              "sellers": 2
            },
            "m15": {
              "buys": 0,
              "sells": 2,
              "buyers": 0,
              "sellers": 2
            },
            "m30": {
              "buys": 0,
              "sells": 3,
              "buyers": 0,
              "sellers": 3
            },
            "h1": {
              "buys": 1,
              "sells": 23,
              "buyers": 1,
              "sellers": 7
            },
            "h6": {
              "buys": 60,
              "sells": 38,
              "buyers": 23,
              "sellers": 18
            },
            "h24": {
              "buys": 206,
              "sells": 138,
              "buyers": 96,
              "sellers": 77
            }
          },
          "volume_usd": {
            "m5": "130.5119858698",
            "m15": "130.5119858698",
            "m30": "177.109036156",
            "h1": "4942.2463835639",
            "h6": "28362.2127269542",
            "h24": "112426.585893123"
          }
  ```

  ### Onchain Simple Token Price endpoint - Liquidity & Price Change Percentage data

  Now supports the following optional parameter to return more data.

  * `include_24hr_price_change` (24hr price change percentage)
  * `include_total_reverse_in_usd` (token liquidity data - total liquidity portion attributable to a specific token across all available pools)

  **Improved Endpoint:**

  * [Token Price by Token Addresses](https://docs.coingecko.com/reference/onchain-simple-price)

  ```json  theme={null}
  {
    "data": {
      "id": "e58258f7-8368-4968-bbe1-b5343540cd71",
      "type": "simple_token_price",
      "attributes": {
        "token_prices": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "1.00276143983565",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "3175.22870146126"
        },
        "market_cap_usd": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "25000000000",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "500000000000"
        },
        "h24_volume_usd": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "50000000",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "10000000000"
        },
        "h24_price_change_percentage": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "-0.15",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "1.15"
        },
        "total_reserve_in_usd": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "417994486.4342195821530162288",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "417994486.4342195821530162288" 
      }
    }
  }
  ```
</Update>

<Update label="February 2025">
  ## New Megafilter Endpoint,  200+ Chains Supported: Hyperliquid, Abstract, Berachain & MOAR!

  🗓️ **February 27, 2025**

  Powered by GeckoTerminal, the CoinGecko API now supports on-chain data across **200+ blockchain networks**, including the latest additions: Hyperliquid, HyperEVM, Abstract, Berachain, Story, Monad, Unichain, and Soneium.

  While we offer the widest on-chain data coverage, we understand that you may have specific needs when slicing and dicing data for your use case. That's why we're introducing Megafilter, an exclusive endpoint available for our API paid plan subscribers (Analyst plan & above).

  ### 🔥 What's Megafilter?

  This new endpoint provides unmatched flexibility, allowing you to query and filter data exactly the way you want.

  🔗 Docs: [Megafilter for Pools](https://docs.coingecko.com/reference/pools-megafilter)

  ### 👀 What Can You Do?

  With the /megafilter endpoint, you can slice and dice on-chain data your way across:

  * 200+ blockchain networks, 1,400+ dexes, 6M+ pools, and 5M+ tokens
  * Advanced filtering options based on liquidity, FDV, volume, transactions, buy/sell trends, and time range
  * Custom sorting, including trending pools (5m), newest pools, or liquidity growth
  * Fraud detection filters: Exclude honeypots, check GT Score, verify CG listings, and track social metrics

  Here's some quick examples:

  * Track fresh pools on Uniswap V4 & Aerodrome with liquidity above \$1,000
  * Discover trending DEX pools across Solana, Base, and other chains with a high GT Score.
  * Filter out risky pools with built-in honeypot protection & fraud checks
  * Customize data retrieval based on your strategy: time-based, volume-based, or trend-driven

  ### Try it out now!

  🚀 API Docs: [Megafilter for Pools](https://docs.coingecko.com/reference/pools-megafilter)\
  🔗 Live Filtering on [GeckoTerminal](https://www.geckoterminal.com/)

  <GreenSeparator />

  ## Update Frequency Improvements for selected Pro-API endpoints

  🗓️ **February 14, 2025**

  \[Changes below are applicable to Analyst/Lite/Pro/Enterprise [plan subscribers](https://www.coingecko.com/en/api/pricing) only.]

  Dear CoinGecko API paid plan subscribers,

  We're excited to announce an improvement to our API, aimed at providing you with even faster access to real-time data! Starting **02:00 UTC, February 24, 2025**, the edge cache duration for the following endpoints will be reduced to 30s, allowing you to retrieve updated data more frequently.

  | Endpoints                                                                                                 | Effective Date & Time                                            | Current Update Frequency | New Update Frequency |
  | :-------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- | :----------------------- | :------------------- |
  | Onchain [/networks/../tokens/](https://docs.coingecko.com/reference/token-data-contract-address)          | 02:00 UTC, February 24, 2025                                     | 60s                      | 30s                  |
  | Onchain [/networks/../tokens/multi/](https://docs.coingecko.com/reference/tokens-data-contract-addresses) | 06:00 UTC, February 24, 2025                                     | 60s                      | 30s                  |
  | Onchain [/networks/../pools/../ohlcv](https://docs.coingecko.com/reference/pool-ohlcv-contract-address)   | 02:00 UTC, February 25, 2025 - Enterprise plan subscribers only  | 60s                      | 30s                  |
  | Onchain [/networks/../pools/../ohlcv](https://docs.coingecko.com/reference/pool-ohlcv-contract-address)   | 02:00 UTC, February 26, 2025 - Analyst/Lite/Pro plan subscribers | 60s                      | 30s                  |

  **What This Means for You:**

  * **Fresher Data, Quicker**: With a reduced cache time, you'll now have the option to access more up-to-date data, closer to real-time!
  * **No Extra Credits for Cached Data**: If your request hits the cache (now updated every 30 seconds for endpoints above), there will be no additional credits charged—just like before.

  **Things to Keep in Mind:**

  * If your request hits our origin server instead of the cache to retrieve the latest data, there may be additional credits used.
  * To balance cost and real-time data needs, we recommend reviewing your request frequency. For those who prefer to obtain data without extra credits, consider keeping your request interval at 60 seconds or more to align with the new cache duration.

  We're committed to continuously improving your experience and ensuring you get the data you need, as efficiently as possible. If you have any questions or need assistance, feel free to reach out to [soonaik@coingecko.com](mailto:soonaik@coingecko.com) .

  **CoinGecko API Team**

  <GreenSeparator />

  ## Enhanced Onchain Metadata, Increased Max Address Limit for Multi Endpoints, Improved Exchange Tickers Sorting

  🗓️ **February 09, 2025**

  ### Onchain Metadata: Improved Coverage

  **Previously:** Payload may return 'missing.png' for `image_url` for tokens that do not have image data.

  **Now:** Coverage of metadata (images, websites, description, socials) is now improved for tokens on Solana, Ton, Base, and Sui networks. For tokens that do not contain image data, 'null' value will be returned for `image_url`.

  **Improved endpoints with image data:**

  1. [Trending Pools List](https://docs.coingecko.com/reference/trending-pools-list)
  2. [Trending Pools by Network](https://docs.coingecko.com/reference/trending-pools-network)
  3. [Specific Pool Data by Pool Address](https://docs.coingecko.com/reference/pool-address)
  4. [Multiple Pools Data by Pool Addresses](https://docs.coingecko.com/reference/pools-addresses)
  5. [Top Pools by Network](https://docs.coingecko.com/reference/top-pools-network)
  6. [Top Pools by Dex](https://docs.coingecko.com/reference/top-pools-dex)
  7. [New Pools by Network](https://docs.coingecko.com/reference/latest-pools-network)
  8. [New Pools List](https://docs.coingecko.com/reference/latest-pools-list)
  9. [Search Pools](https://docs.coingecko.com/reference/search-pools)
  10. [Top Pools by Token Address](https://docs.coingecko.com/reference/top-pools-contract-address)
  11. [Token Data by Token Address](https://docs.coingecko.com/reference/token-data-contract-address)
  12. [Tokens Data by Token Addresses](https://docs.coingecko.com/reference/tokens-data-contract-addresses)
  13. [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  14. [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)
  15. [Most Recently Updated Tokens List](https://docs.coingecko.com/reference/tokens-info-recent-updated)

  **Improved endpoints with metadata (images, websites, description, socials):**

  1. [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  2. [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)
  3. [Most Recently Updated Tokens List](https://docs.coingecko.com/reference/tokens-info-recent-updated)

  Note: Metadata may be sourced on-chain and is not vetted by the CoinGecko team. If you wish to get metadata reviewed by CoinGecko team, you may use the following endpoints:

  * [Coin Data by ID](https://docs.coingecko.com/reference/coins-id)
  * [Coin Data by Token Address](https://docs.coingecko.com/reference/coins-contract-address)

  ### Improved Max Address Limit for onchain /multi endpoints

  **Previously:** Onchain /multi endpoints support up to 30 token or pool contract addresses per request.

  **Now:** Onchain /multi endpoints support up to 50 token or pool contract addresses per request.

  **Improved endpoints:**

  1. [Tokens Data by Token Addresses](https://docs.coingecko.com/reference/tokens-data-contract-addresses)
  2. [Multiple Pools Data by Pool Addresses ](https://docs.coingecko.com/reference/pools-addresses)

  Note: this new max address input limit is exclusive for paid plan subscribers (Analyst plan & above) only.

  ### Improved Data Consistency for Exchange Tickers by ID

  For [Exchange Tickers by ID](https://docs.coingecko.com/reference/exchanges-id-tickers) endpoint, the order is sorted by **trust\_score\_desc** by default.

  * Sometimes duplicate or missing data may occur due to paginated cached response, especially when a ticker's rank changes between 2 paginated requests, e.g. it might shift from Page 2 to Page 1, vice versa.
  * We've added a new `order` option: **base\_target**, which will sort the tickers by **base** symbol, then **target** symbol, in lexicographical order, i.e. `0->9`, then `a->Z`.

  Example:  flagging ?order=base\_target

  ```
  pro-api.coingecko.com/api/v3/exchanges/binance/tickers?order=base_target
  ```

  This sorting method ensures stable pagination, reducing issues where cached responses may cause duplicate or missing tickers across pages.
</Update>

<Update label="January 2025">
  ## Multiple Improvements: Onchain Pools Page Limit, Trades Token Filter

  🗓️ **January 27, 2025**

  ### Onchain Pools Data: Supports more than 10 pages of data

  **Previously:** There was a limitation of a maximum of 10 pages for accessing pools data in the related endpoints.

  **Now:** All paid plan subscribers (Analyst & above) can access more than 10 pages of pools data for the endpoints below.

  **Improved Endpoints:**

  1. [Search Pools](https://docs.coingecko.com/reference/search-pools)
  2. [Top Pools by Token Address](https://docs.coingecko.com/reference/top-pools-contract-address)
  3. [Trending Pools List](https://docs.coingecko.com/reference/trending-pools-list)
  4. [Trending Pools by Network](https://docs.coingecko.com/reference/trending-pools-network)
  5. [New Pools by Network](https://docs.coingecko.com/reference/latest-pools-network)
  6. [New Pools List](https://docs.coingecko.com/reference/latest-pools-list)
  7. [Top Pools by Network](https://docs.coingecko.com/reference/top-pools-network)
  8. [Top Pools by Dex](https://docs.coingecko.com/reference/top-pools-dex)

  ### Onchain Trades: Added Token Filter

  **Endpoint:** [Past 24 Hour Trades by Pool Address](https://docs.coingecko.com/reference/pool-trades-contract-address)

  **Previously:** There was no way to filter trades data by base or quote token.

  **Now**: A new optional parameter has been added to allow filtering by base or quote token of a pool.

  * Parameter: `token`
  * Value options:
    * `base`
    * `quote`
    * `{token_address}`

  **Example**:

  ```json Example theme={null}
  ?token=base // get the trades data of base token
  ?token=quote // get the trades data of quote token
  ?token=8FqXr6dw5NHA2TtwFeDz6q9p7y9uWyoEdZmpXqqUpump // get the trades data of specific token based on address
  ```

  <GreenSeparator />

  ## Multiple Improvements: Onchain Token Price, NFT Market Cap

  🗓️ **January 24, 2025**

  ### Onchain Simple Token Price: Added Market Cap and 24h Volume Data

  **Endpoint:** [Token Price by Token Addresses](https://docs.coingecko.com/reference/onchain-simple-price)

  * You can now flag `include_market_cap=true` and `include_24hr_vol=true` to retrieve market cap and 24h trading volume data. e.g.

  ```json json theme={null}
  {
    "data": {
      "id": "e1979db1-5c3e-4ba8-b103-cb0258af4a7c",
      "type": "simple_token_price",
      "attributes": {
        "token_prices": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "0.999365729816931",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "3399.24368371279"
        },
        "market_cap_usd": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "51963214441.24363",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "10005535878.50094"
        },
        "h24_volume_usd": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "2095689865.85327",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "2544539948.02599"
        }
      }
    }
  }
  ```

  ### NFT Data: Added 'Market Cap Rank'

  You can now obtain the `market_cap_rank` data of NFT collections via the following endpoints:

  * [NFTs Collection Data by ID](https://docs.coingecko.com/reference/nfts-id)
  * [NFTs Collection Data by Contract Address](https://docs.coingecko.com/reference/nfts-contract-address)

  ```json example theme={null}

    "market_cap_rank": 75,

  ```

  <GreenSeparator />

  ## Removal of Unsupported Categories

  🗓️ **January 23, 2025**

  ### Upcoming Removal of Unsupported Categories from CoinGecko and CoinGecko API

  #### Summary

  We are announcing the removal of certain categories from CoinGecko and CoinGecko API. These categories will no longer be supported across all API endpoints starting **February 12, 2025**.

  | No | Category Name          | Category ID         |
  | :- | :--------------------- | :------------------ |
  | 1  | US Election 2020       | us-election-2020    |
  | 2  | Governance             | governance          |
  | 3  | Cryptocurrency         | cryptocurrency      |
  | 4  | Technology and Science | technology-science  |
  | 5  | Presale Meme           | presale-meme-coins  |
  | 6  | Business Platform      | business-platform   |
  | 7  | Number                 | number              |
  | 8  | Structured Product     | structured-products |
  | 9  | Investment             | investment          |
  | 10 | Niftex Shards          | niftex-shards       |
  | 11 | Ethereum POW IOU       | ethereum-pow-iou    |
  | 12 | Mirrored Assets        | mirrored-assets     |
  | 13 | Remittance             | remittance          |
  | 14 | Protocol               | protocol            |
  | 15 | Unicly Ecosystem       | utokens             |
  | 16 | Finance and Banking    | finance-banking     |
  | 17 | Eth 2.0 Staking        | eth-2-0-staking     |

  #### Reason for Removal

  Many of these categories no longer have associated coins. Some categories are outdated and no longer relevant in the crypto space. The changes align with updated category topology standards to maintain data accuracy and relevance.

  #### Impact

  API responses for the `/coins/markets` [endpoint](https://docs.coingecko.com/reference/coins-markets) will no longer support data of the categories above. Any requests specifying these categories will return an error.

  #### Action Required

  Ensure applications using the `/coins/markets` [endpoint](https://docs.coingecko.com/reference/coins-markets) are not querying these removed categories. Please update any code or documentation referencing these categories to prevent errors.

  <GreenSeparator />

  ## Extended Historical Data for Onchain OHLCV Endpoint

  🗓️ **January 15, 2025**

  ### What's New?

  We've improved the [Pool OHLCV Chart by Pool Address](https://docs.coingecko.com/reference/pool-ohlcv-contract-address) endpoint to provide access to a much broader range of historical data.

  #### Key Updates

  * **Previous Behavior:** Users could only query data for the past 6 months from today.
  * **New Behavior**: Users can now access data from September 2021 to the present, depending on the pool's tracking start date on GeckoTerminal.
  * Each API request is **limited to a 6-month date range**, but users can query older data by using the before\_timestamp parameter.

  Note: access to data beyond the past 6 months is only available to [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above).

  #### Action Required

  No changes are required for existing integrations. However, users who need data beyond the past 6 months should adjust their queries to use the `before_timestamp` parameter to fetch additional data.

  <GreenSeparator />

  ## Update to Total Supply of POW Coins

  🗓️ **January 15, 2025**

  #### What's Changing?

  We are updating the definition of Total Supply for PoW (Proof-of-Work) coins to reflect the actual number of mined coins rather than the maximum supply. This change ensures consistency and accuracy in representing the supply data.

  #### Key Updates

  * **Previous Behavior:**
    * Total Supply: Displayed as the maximum possible supply (e.g., Bitcoin: 21,000,000).
  * **New Behavior:**
    * Total Supply: Now reflects the actual number of mined coins.\
      For example: Bitcoin: \~19,500,000 (as of January 2025).

  This update will also affect historical Total Supply data for consistency. This change applies to all affected PoW coins, including Bitcoin, Bitcoin Cash, Litecoin, Ethereum Classic, and more.

  #### Affected endpoints that contain "total\_supply" data:

  * **Current Data**
    * [Coin Data by ID](https://docs.coingecko.com/reference/coins-id)
    * [Coins List with Market Data](https://docs.coingecko.com/reference/coins-markets)
  * **Historical Darta**
    * [Total Supply Chart by ID](https://docs.coingecko.com/reference/coins-id-total-supply-chart)
    * [Total Supply chart within time range by ID](https://docs.coingecko.com/reference/coins-id-total-supply-chart-range)

  #### Timeline:

  **Bitcoin:** Updated on Jan 14, 2025

  **Other PoW Coins**: Scheduled for Jan 22, 2025

  * [Bitcoin Cash](https://www.coingecko.com/en/coins/bitcoin-cash)
  * [Litecoin](https://www.coingecko.com/en/coins/litecoin)
  * [Ethereum Classic](https://www.coingecko.com/en/coins/ethereum-classic)
  * [Bitcoin SV](https://www.coingecko.com/en/coins/bitcoin-sv)
  * [Zcash](https://www.coingecko.com/en/coins/zcash)
  * [eCash](https://www.coingecko.com/en/coins/ecash)
  * [Dash](https://www.coingecko.com/en/coins/dash)
  * [Verus Coin](https://www.coingecko.com/en/coins/verus-coin)
  * [Ravencoin](https://www.coingecko.com/en/coins/ravencoin)
  * [Kadena](https://www.coingecko.com/en/coins/kadena)
  * [Decred](https://www.coingecko.com/en/coins/decred)
  * [Flux (Zelcash)](https://www.coingecko.com/en/coins/flux-zelcash)
  * [DigiByte](https://www.coingecko.com/en/coins/digibyte)
  * [Quantum Resistant Ledger](https://www.coingecko.com/en/coins/quantum-resistant-ledger)
  * [Komodo](https://www.coingecko.com/en/coins/komodo)
  * [Groestlcoin](https://www.coingecko.com/en/coins/groestlcoin)
  * [Firo](https://www.coingecko.com/en/coins/firo)
  * [Litecoin Cash](https://www.coingecko.com/en/coins/litecoin-cash)
  * [LuckyCoin](https://www.coingecko.com/en/coins/luckycoin)
  * [Enecuum](https://www.coingecko.com/en/coins/enecuum)
  * [Wownero](https://www.coingecko.com/en/coins/wownero)
  * [Radiant](https://www.coingecko.com/en/coins/radiant)
  * [Tidecoin](https://www.coingecko.com/en/coins/tidecoin)
  * [Handshake](https://www.coingecko.com/en/coins/handshake)
  * [Neoxa](https://www.coingecko.com/en/coins/neoxa)
  * [Vertcoin](https://www.coingecko.com/en/coins/vertcoin)
  * [Feathercoin](https://www.coingecko.com/en/coins/feathercoin)
  * [Bitcore](https://www.coingecko.com/en/coins/bitcore)
  * [Phoenixcoin](https://www.coingecko.com/en/coins/phoenixcoin)
  * [BitcoinZ](https://www.coingecko.com/en/coins/bitcoinz)
  * [Hush](https://www.coingecko.com/en/coins/hush)
  * [DigitalNote](https://www.coingecko.com/en/coins/digitalnote)
  * [EquityPay](https://www.coingecko.com/en/coins/equitypay)
  * [Evadore](https://www.coingecko.com/en/coins/evadore)
  * [Swap](https://www.coingecko.com/en/coins/swap)
  * [DeVault](https://www.coingecko.com/en/coins/devault)
  * [AXE](https://www.coingecko.com/en/coins/axe)
  * [Iridium](https://www.coingecko.com/en/coins/iridium)
  * [X-Cash](https://www.coingecko.com/en/coins/x-cash)
  * [Bolivarcoin](https://www.coingecko.com/en/coins/bolivarcoin)
  * [uPlexa](https://www.coingecko.com/en/coins/uplexa)
  * [WorldCoin (WDC)](https://www.coingecko.com/en/coins/worldcoin-wdc)

  <GreenSeparator />

  ## Improved Update Frequency for selected Pro-API endpoints

  🗓️ **January 13, 2025**

  \[Changes below are applicable to Analyst/Lite/Pro/Enterprise [plan subscribers](https://www.coingecko.com/en/api/pricing) only.]

  The edge cache duration for the following endpoints are now reduced to 20-30s, allowing you to retrieve updated data more frequently.

  | Endpoints                                                                                                 | Previous Update Frequency | Current Update Frequency |
  | :-------------------------------------------------------------------------------------------------------- | :------------------------ | :----------------------- |
  | CoinGecko [/simple/price](https://docs.coingecko.com/reference/simple-price)                              | 30s                       | 20s                      |
  | CoinGecko [/simple/token\_price](https://docs.coingecko.com/reference/simple-token-price)                 | 30s                       | 20s                      |
  | Onchain [/simple/networks/../token\_price](https://docs.coingecko.com/reference/onchain-simple-price)     | 60s                       | 30s                      |
  | Onchain [/networks/../pools/../trades](https://docs.coingecko.com/reference/pool-trades-contract-address) | 60s                       | 30s                      |
  | Onchain [/networks/../pools/..](https://docs.coingecko.com/reference/pool-address)                        | 60s                       | 30s                      |
  | Onchain [/networks/../pools/multi/..](https://docs.coingecko.com/reference/pools-addresses)               | 60s                       | 30s                      |

  **What This Means for You:**

  * **Fresher Data, Quicker**: With a reduced cache time, you'll now have the option to access more up-to-date data, closer to real-time!
  * **No Extra Credits for Cached Data**: If your request hits the cache (now updated every 20-30 seconds for endpoints above), there will be no additional credits charged—just like before.

  **Things to Keep in Mind:**

  * If your request hits our origin server instead of the cache to retrieve the latest data, there may be additional credits used.
  * To balance cost and real-time data needs, we recommend reviewing your request frequency. For those who prefer fresher data without extra credits, consider keeping your request interval at 30 seconds or more to align with the new cache duration.

  We're committed to continuously improving your experience and ensuring you get the data you need, as efficiently as possible. If you have any questions or need assistance, feel free to reach out to [soonaik@coingecko.com](mailto:soonaik@coingecko.com) .

  **CoinGecko API Team**

  <GreenSeparator />

  ## Improved 5-minutely data for Historical Chart Data endpoints

  🗓️ **January 09, 2025**

  For the following 4 historical chart endpoints, the data of the *last 48 hours from now* is no longer excluded.

  * [Coin Historical Chart Data by ID](https://docs.coingecko.com/reference/coins-id-market-chart)
  * [Coin Historical Chart Data within Time Range by ID](https://docs.coingecko.com/reference/coins-id-market-chart-range)
  * [Coin Historical Chart Data by Token Address](https://docs.coingecko.com/reference/contract-address-market-chart)
  * [Coin Historical Chart Data within Time Range by Token Address](https://docs.coingecko.com/reference/contract-address-market-chart-range)

  **Note:** The **5-minutely** and **hourly** interval params are exclusively available to Enterprise plan subscribers, bypassing auto-granularity:

  * `interval=5m`: 5-minutely historical data, supports up to any 10 days date range per request.
  * `interval=hourly`: hourly historical data, supports up to any 100 days date range per request.
  * **Data availability:**
    * `interval=5m`: Available from 9 February 2018 onwards
    * `interval=hourly`: Available from 30 Jan 2018 onwards

  For non-Enterprise plan subscribers who would like to get hourly data, please leave the `interval` params empty for auto granularity:

  * 1 day from current time = 5-minutely data
  * 1 day from any time (except current time) = hourly data
  * 2 - 90 days from any time = hourly data
  * above 90 days from any time = daily data (00:00 UTC)
</Update>

<Update label="December 2024">
  ## Added: Onchain Categories Data, CG data improvements

  🗓️ **December 24, 2024**

  ### NEW: Onchain Categories : Get Categories on GeckoTerminal.com

  This new [Categories List](https://docs.coingecko.com/reference/categories-list) endpoint allows you to query all the categories supported on GeckoTerminal.com such as 'Pump Fun' and 'Animal'.

  * This endpoint is exclusively available for [Analyst/Lite/Pro/Enterprise plan](https://www.coingecko.com/en/api/pricing) subscribers only.

  ### NEW: Onchain Catergory Pools: Get Pools of a specific Category

  This new [Pools by Category ID](https://docs.coingecko.com/reference/pools-category) endpoint allows you to query all the pools of a specific category on GeckoTerminal.com.

  * This endpoint is exclusively available for [Analyst/Lite/Pro/Enterprise plan](https://www.coingecko.com/en/api/pricing) subscribers only.
  * You can also obtain tokens of a specific category, by flagging `include=base_token`

  ### Onchain Token Info: Added Categories Data

  You can now obtain the categories of a token via the following endpoints:

  1. [Token Info by Token Address](https://docs.coingecko.com/reference/token-info-contract-address)
  2. [Pool Tokens Info by Pool Address](https://docs.coingecko.com/reference/pool-token-info-contract-address)

  Payload example:

  ```yaml json theme={null}
    "categories": [
      "Doge",
      "Baby",
      "Animal"
    ],
    "gt_category_ids": [
      "doge",
      "baby",
      "animal"
  ```

  ### Onchain New Pools Data: Bug Fixed

  Previously, this [/networks/new\_pools](https://docs.coingecko.com/reference/latest-pools-network) endpoint omitted new pools that are created within the last 24 hours.

  It now returns all newly created pools in the last 48 hours.

  ### CoinGecko Exchange Data: Added support of inactive exchange id

  You now query the the list of id of delisted exchanges with [Exchanges List (ID Map)](https://docs.coingecko.com/reference/exchanges-list) endpoint, by flagging `status=inactive `

  Payload example:

  ```yaml json theme={null}
    {
      "id": "ftx",
      "name": "FTX (Derivatives)"
    },
    {
      "id": "ftx_spot",
      "name": "FTX"
    },
    {
      "id": "ftx_tr",
      "name": "FTX TR"
    },
    {
      "id": "ftx_us",
      "name": "FTX.US"
    },
  ```

  **Tips**: you may query to get historical volume delisted exchanges for via the following endpoints:

  * [Exchange Volume Chart by ID](https://docs.coingecko.com/reference/exchanges-id-volume-chart)
  * [Exchange Volume Chart within Time Range by ID](https://docs.coingecko.com/reference/exchanges-id-volume-chart-range)

  ### CoinGecko Historical Chart Data: Faster Last UTC Day (00:00) Data Update

  For [Coin Historical Chart Data by ID](https://docs.coingecko.com/reference/coins-id-market-chart) endpoint, the last completed UTC day (00:00) data is now available **10 minutes after midnight** on the next UTC day (00:10).

  Previously, the last completed UTC day (00:00) was only made available **35 minutes** after midnight.

  <GreenSeparator />

  ## \[Updated: Q4 2024] CoinGecko Asset Issuance Standardisation Initiative Updates

  🗓️ **December 17, 2024**

  As part of our commitment to improving data quality and enhancing the consistency of asset information, we are rolling out an asset standardization initiative at CoinGecko.

  **What is asset standardization?**\
  Standardization involves refining how we classify and display assets. By systematically organizing asset listings into more precise categories - such as native, bridged, or wrapped tokens each following specific naming conventions, we aim to eliminate confusion and enhance data reliability.

  **What changes should I expect?**\
  The most notable change is that non-native token contracts previously grouped under native asset listings will now be assigned their own distinct pages.

  For example, a bridged version of USDT that might have been aggregated under the original, native USDT page, will now be featured on a dedicated page specifically for that bridged variant.

  Additionally, there may be varying levels of changes in various aggregated data points of the standardized assets, including trading volume, supply, market cap rankings, etc., due to misplaced contracts being transitioned away from the original page to accurately reflect their true metrics.

  **Focus for Q3 2024** **\[Completed ✅]**

  * [Wrapped Bitcoin (WBTC)](https://www.coingecko.com/en/coins/wrapped-bitcoin)
  * [Wrapped Ethereum (WETH)](https://www.coingecko.com/en/coins/weth)
  * [Dai (DAI)](https://www.coingecko.com/en/coins/dai)

  \*\*For full list of FAQs and updated infomation, please refer [here](https://support.coingecko.com/hc/en-us/articles/35555248857497-CoinGecko-Asset-Issuance-Standardisation-Initiative-Updates-and-FAQ)

  ### What's New in Q4 2024? 👈

  Building on Q3's achievements, we're expanding the scope of Standardization to include four additional Coins this quarter, selected based on their significance and impact on the DeFi ecosystem.

  * [Frax (FRAX)](https://www.coingecko.com/en/coins/frax)
  * [Wrapped AVAX (WAVAX)](https://www.coingecko.com/en/coins/wrapped-avax)
  * [Wrapped BNB (WBNB)](https://www.coingecko.com/en/coins/wbnb)
  * [Wrapped stETH (wstETH)](https://www.coingecko.com/en/coins/wrapped-steth)

  ### Tips and FAQs for API users

  #### **1. How does this affect my current API setup?**

  The following CoinGecko API endpoints will be impacted, with full details tracked in [this spreadsheet](https://docs.google.com/spreadsheets/d/15FyY1gvUi20LdnlJRly-pXvm5ATNbFbSy06VoI1vVs4/edit?usp=sharing). We encourage you to make the necessary adjustments and enable edit notifications on the Google Sheets, to receive real-time updates when non-native token contracts have been successfully standardized.

  **Simple**

  * /simple/price
  * /simple/token\_price/id

  **Coins**

  * /coins/markets
  * /coins/id
  * /coins/id/tickers
  * /coins/id/history
  * /coins/id/market\_chart
  * /coins/id/market\_chart/range
  * /coins/id/ohlc
  * /coins/id/ohlc/range
  * /coins/id/circulating\_supply\_chart
  * /coins/id/circulating\_supply\_chart/range
  * /coins/id/total\_supply\_chart
  * /coins/id/total\_supply\_chart/range

  **Contract**

  * /coins/id/contract/contract\_address
  * /coins/id/contract/contract\_address/market\_chart
  * /coins/id/contract/contract\_address/market\_chart/range

  **Exchange**

  * /exchanges/id/tickers
  * /exchanges/id/volume\_chart
  * /exchanges/id/volume\_chart/range

  #### **2. Do I have to make changes to my API?**

  **No changes are necessary** if you do not need data for non-native token contracts that will be separated away from the native tokens.

  #### **3. What will happen to the coins that are separated into a new coin page?**

  Historical data for new non-native or bridged assets will only be available from the date of asset page creation (i.e. stnadardized). To access historical data prior to the asset standardization, we recommend retrieving data from the original native assets.

  #### **4. How do I identify the list of coins that will be separated?**

  For a finalised list of token contracts and API IDs that have been separated from its native asset page and listed individually, please refer to this [Google Sheets](https://docs.google.com/spreadsheets/d/15FyY1gvUi20LdnlJRly-pXvm5ATNbFbSy06VoI1vVs4/edit?usp=sharing)

  You may also identify the list of bridged coins via API: you may also use [/categories/list endpoint](/reference/coins-categories-list) to look for bridged categories such as:

  1. bridged-usdc
  2. bridged-wbtc
  3. bridged-weth

  Then you may use [/coins/market endpoint](/reference/coins-markets) to retrieve the list of coins

  <GreenSeparator />

  ## Enhancing Your Access to Even Fresher Data!

  🗓️ **December 16, 2024**

  \[Changes below are applicable to Analyst/Lite/Pro/Enterprise [plan subscribers](https://www.coingecko.com/en/api/pricing) only.]

  **Dear CoinGecko API paid plan subscribers,**

  We're excited to announce an improvement to our API, aimed at providing you with even faster access to real-time data! Starting **02:00 UTC, January 13, 2025**, the edge cache duration for the following endpoints will be reduced to 20-30s, allowing you to retrieve updated data more frequently.

  | Endpoints                                                                                                 | Current Update Frequency | New Update Frequency |
  | :-------------------------------------------------------------------------------------------------------- | :----------------------- | :------------------- |
  | CoinGecko [/simple/price](https://docs.coingecko.com/reference/simple-price)                              | 30s                      | 20s                  |
  | CoinGecko [/simple/token\_price](https://docs.coingecko.com/reference/simple-token-price)                 | 30s                      | 20s                  |
  | Onchain [/simple/networks/../token\_price](https://docs.coingecko.com/reference/onchain-simple-price)     | 60s                      | 30s                  |
  | Onchain [/networks/../pools/../trades](https://docs.coingecko.com/reference/pool-trades-contract-address) | 60s                      | 30s                  |
  | Onchain [/networks/../pools/..](https://docs.coingecko.com/reference/pool-address)                        | 60s                      | 30s                  |
  | Onchain [/networks/../pools/multi/..](https://docs.coingecko.com/reference/pools-addresses)               | 60s                      | 30s                  |

  **What This Means for You:**

  * **Fresher Data, Quicker**: With a reduced cache time, you'll now have the option to access more up-to-date data, closer to real-time!
  * **No Extra Credits for Cached Data**: If your request hits the cache (now updated every 20-30 seconds for endpoints above), there will be no additional credits charged—just like before.

  **Things to Keep in Mind:**

  * If your request hits our origin server instead of the cache to retrieve the latest data, there may be additional credits used.
  * To balance cost and real-time data needs, we recommend reviewing your request frequency. For those who prefer fresher data without extra credits, consider keeping your request interval at 30 seconds or more to align with the new cache duration.

  We're committed to continuously improving your experience and ensuring you get the data you need, as efficiently as possible. If you have any questions or need assistance, feel free to reach out to [soonaik@coingecko.com](mailto:soonaik@coingecko.com) .

  **CoinGecko API Team**

  <GreenSeparator />

  ## Multiple Improvements: Onchain Trending Pools, CG New Currencies Support, Snapshot, Exchange Info

  🗓️ **December 15, 2024**

  ### Onchain Trending Pools: Added Support to Filter by Duration

  You can now query trending pools with the following endpoints, and filter them by different duration: 5m, 1h, 6h, 24h, using `duration` parameter. e.g. `duration=5m`

  * [Trending Pools List](https://docs.coingecko.com/reference/trending-pools-list): query all the trending pools across all networks on GeckoTerminal
  * [Trending Pools by Network](https://docs.coingecko.com/reference/trending-pools-network): query the trending pools based on the provided network

  ### CG Coin Prices: Added Support for New Fiat Currencies

  You can now query coin prices in the 13 new currencies for the following 3 endpoints:

  * [Coin Price by IDs](https://docs.coingecko.com/reference/simple-price): query latest price in selected currencies, by coin id
  * [Coin Price by Token Addresses](https://docs.coingecko.com/reference/simple-token-price): query latest price in selected currencies, by token address
  * [BTC-to-Currency Exchange Rates](https://docs.coingecko.com/reference/exchange-rates): query BTC exchange rates with other currencies

  **New supported currencies:**

  1. Colombia | COP
  2. Kenya | KES
  3. Romania | RON
  4. Dominican Republic | DOP
  5. Costa Rica | CRC
  6. Honduras | HNL
  7. Zambia | ZMW
  8. El Salvador | SVC
  9. Bosnia and Herzegovina | BAM
  10. Peru | PEN
  11. Guatemala | GTQ
  12. Lebanon | LBP
  13. Armenian Dram | AMD

  ### CG Coin Info: Included Snapshot URL

  [Coin Data by ID](https://docs.coingecko.com/reference/coins-id) now includes Snapshot link, e.g.

  ```asp json theme={null}
  "snapshot_url": "https://snapshot.org/#/lido-snapshot.eth",
  ```

  ### CG Exchange Info: Included Number of Coins and Pairs

  [https://docs.coingecko.com/reference/exchanges-id](https://docs.coingecko.com/reference/exchanges-id) now includes "coins" and "pairs", e.g.

  ```asp json theme={null}
   "coins": 384,
   "pairs": 1281,
  ```
</Update>

<Update label="October 2024">
  ## Multiple Improvements: Onchain Simple Price, Onchain Recently Updated Info, NFT Collection Data

  🗓️ **October 09, 2024**

  ### Onchain: Simple Price - Increased Token Address Limit from 30 to 100

  [Token Price by Token Addresses](/reference/onchain-simple-price) now allows to input up to 100 contract addresses, instead of 30.

  * You may now retrieve data of up to 100 token prices of a specific network, in one single request.
  * Available exclusively to Pro API paid plan subscribers.

  ### Onchain: Recently Updated Info - Added Filter by Network

  [Most Recently Updated Token List](/reference/tokens-info-recent-updated) now allows to filter by blockchain network, by flagging the `network` parameter. e.g. `network=eth`.

  * You can use the `network` parameter to retrieve the 100 most recently updated token info of a specific network.
  * View list of supported network via [Supported Networks List](https://docs.coingecko.com/reference/networks-list) endpoint.

  ### NFT Collection Data  - Included Banner Image

  [NFTs Collection Data by ID](/reference/nfts-id) now provides banner image of a NFT collection.

  View banner image [example](https://coin-images.coingecko.com/nft_contracts/images/38/pudgy-penguins-banner.png?1708416126) on: [https://www.coingecko.com/en/nft/pudgy-penguins](https://www.coingecko.com/en/nft/pudgy-penguins)

  ```json  theme={null}
  {
    "symbol": "PPG",
    "image": {
      "small": "https://coin-images.coingecko.com/nft_contracts/images/38/small/da64989d9762c8a61b3c65917edfdf97.png?1707287183"
    },
    "banner_image": "https://coin-images.coingecko.com/nft_contracts/images/38/pudgy-penguins-banner.png?1708416126",
  ..
  ```
</Update>

<Update label="September 2024">
  ## Multiple Improvements: Global Market Chart, Asset Platforms, Coin Categories, Historical Supply Chart

  🗓️ **September 26, 2024**

  ### Global Market Chart - Improved Daily Data Update

  Previously, for [Global Market Cap Chart Data endpoint](https://docs.coingecko.com/reference/global-market-cap-chart) , the daily data is returned at 23:00 UTC. We've made improvement to return daily data at 00:00 UTC.

  The last completed UTC day (00:00) is available 5 minutes after midnight on the next UTC day (00:05). The cache will **always expire at 00:05 UTC**. If you wish to get the latest daily data (00:00 UTC), you can make request at 00:05 UTC or later.

  ### Asset Platforms - Included Images of Blockchain Network Logos

  [Asset Platforms List (ID Map)](/reference/asset-platforms-list) now provides the logos of blockchain networks.

  For example:

  ```json  theme={null}
      "image": {
        "thumb": "https://coin-images.coingecko.com/asset_platforms/images/93/thumb/AN_logomark.png?1706606703",
        "small": "https://coin-images.coingecko.com/asset_platforms/images/93/small/AN_logomark.png?1706606703",
        "large": "https://coin-images.coingecko.com/asset_platforms/images/93/large/AN_logomark.png?1706606703"
      }
  ```

  ### Coins Categories - Included Ids of Top 3 Coins

  [Coins Categories List with Market Data](/reference/coins-categories) now provides coins id of the top 3 coins of a category.

  For example:

  ```json  theme={null}
  "top_3_coins_id": [
    "bitcoin",
    "ethereum",
    "binancecoin"
  ],
  ```

  ### Circulating Supply Chart and Total Supply Chart - Fixed '0' data issue

  For the following **Enterprise-plan** exclusive endpoints below, there was a bug that returned wrong '0' value in the payload. This is fixed and will no longer return wrong '0' value in the payload.

  1. [👑 Circulating Supply Chart by ID](https://docs.coingecko.com/reference/coins-id-circulating-supply-chart)
  2. [👑 Circulating Supply chart within Time Range by ID](https://docs.coingecko.com/reference/coins-id-circulating-supply-chart-range)
  3. [👑 Total Supply Chart by ID](https://docs.coingecko.com/reference/coins-id-total-supply-chart)
  4. [👑 Total Supply Chart within time range by ID](https://docs.coingecko.com/reference/coins-id-total-supply-chart-range)

  <GreenSeparator />

  ## Improvement of update frequency for OHLC endpoints

  🗓️ **September 04, 2024**

  The cache & update frequency of the following endpoints have been improved from every 30 minutes to every 15 minutes:

  * [/coins//ohlc](/reference/coins-id-ohlc)
  * [/coins//ohlc/range](/reference/coins-id-ohlc-range)
</Update>

<Update label="August 2024">
  ## Included new fields - NFT data

  🗓️ **August 18, 2024**

  We've added  'user\_favorites\_count', and 'ath' (all-time-high) related data to the following NFT endpoints:

  * [/nfts/](/reference/nfts-id)
  * [/nfts//contract/](/reference/nfts-contract-address)

  **Example of responses:**

  ```json  theme={null}
  {
    "user_favorites_count": 3660,
    "ath": {
      "native_currency": 22.9,
      "usd": 67535
    },
    "ath_change_percentage": {
      "native_currency": -59.825327510917,
      "usd": -64.3396788440525
    },
    "ath_date": {
      "native_currency": "2024-02-17T09:25:05.056Z",
      "usd": "2024-02-29T11:45:08.150Z"
  }
  ```
</Update>

<Update label="May 2024">
  ## Introduced /coins/id/ohlc/range endpoint

  🗓️ **May 10, 2024**

  We've introduced a new endpoint [/coins//ohlc/range](/reference/coins-id-ohlc-range).

  This endpoint allows you to get the OHLC chart (Open, High, Low, Close) of a coin within a range of timestamp based on particular coin id.

  Please note that this endpoint is available exclusively for **paid plan subscribers only**.

  <GreenSeparator />

  ## Added interval hourly params to /coins/id/ohlc

  🗓️ **May 04, 2024**

  We've expanded functionality to include support for the `interval=hourly` parameter within the [/coins//ohlc](/reference/coins-id-ohlc) endpoint.

  Users can use this parameter to retrieve OHLC (Open/High/Low/Close) data on a hourly interval for up to 90 days of the date range.

  Example of endpoint request:

  `https://pro-api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=1&interval=hourly&x_cg_pro_api_key=YOUR_API_KEY`
</Update>

<Update label="April 2024">
  ## Added support for inactive coins in /coins/list and historical data endpoints

  🗓️ **April 30, 2024**

  We've now enhanced the [/coins/list](/reference/coins-list) endpoint to include inactive coins

  * You may access the inactive coins by specifying `status=inactive` in your query
  * Example of endpoint request:\
    `https://pro-api.coingecko.com/api/v3/coins/list?include_platform=false&status=inactive&x_cg_pro_api_key=YOUR_API_KEY`

  Additionally, historical data for inactive coins can be queried using their IDs in the following endpoints:

  * [/coins//history](/reference/coins-id-history)
  * [/coins//market\_chart](/reference/coins-id-market-chart)
  * [/coins//market\_chart/range](/reference/coins-id-market-chart-range)
  * [/coins//contract//market\_chart](/reference/contract-address-market-chart)
  * [/coins//contract//market\_chart/range](/reference/contract-address-market-chart-range)

  Please note that these features are available exclusively for **paid plan subscribers only**
</Update>

<Update label="March 2024">
  ## Introduced /key endpoint

  🗓️ **March 27, 2024**

  We've introduced a new endpoint [/key](/reference/api-usage) for conveniently monitoring your account's API usage, including rate limits and remaining credits.

  **Example of responses**:

  ```json  theme={null}
  {
    "plan": "Other",
    "rate_limit_request_per_minute": 1000,
    "monthly_call_credit": 1000000,
    "current_total_monthly_calls": 307,
    "current_remaining_monthly_calls": 999693
  }
  ```
</Update>

<Update label="February 2024">
  ## Multiple Improvements (Onchain/GT)

  🗓️ **February 28, 2024**

  * image\_url is now returned in the token response for pools and tokens endpoints:

    Example of responses:

    ```json JSON theme={null}
     "data": {
        "id": "eth_0xdac17f958d2ee523a2206206994597c13d831ec7",
        "type": "token",
        "attributes": {
          "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
          "name": "Tether USD",
          "symbol": "USDT",
          "image_url": "https://assets.coingecko.com/coins/images/325/small/Tether.png?1696501661", 👈
          ......
          "market_cap_usd": "100719721661.467"
        },
        "relationships": {}
    }
    ```
  * We've added sorting parameters such as order= `h24_volume_usd_desc` and order=` h24_tx_count_desc` for /pools endpoints
  * The 'token' parameter within the [/ohlcv ](/reference/pool-ohlcv-contract-address) endpoint can now accept a token address, provided it exists in the queried pool, to return OHLCV data\
    Example of endpoint request (**token=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2**):\
    `https://pro-api.coingecko.com/api/v3/onchain/networks/eth/pools/0x06da0fd433c1a5d7a4faa01111c044910a184553/ohlcv/day?token=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&x_cg_pro_api_key=YOUR_API_KEY`
  * [/ohlcv ](/reference/pool-ohlcv-contract-address) endpoint now includes the base and target token metadata in the response\
    Example of responses:

    ```json JSON theme={null}
    {
      "data": {
        "id": "46303eb4-fba1-44f3-a3c8-c542e4cd5d1a",
        "type": "ohlcv_request_response",
        "attributes": {
          "ohlcv_list": []
        }
      },
      "meta": {
        "base": {
          "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
          "name": "Tether USD",
          "symbol": "USDT",
          "coingecko_coin_id": "tether"
        },
        "quote": {
          "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
          "name": "Wrapped Ether",
          "symbol": "WETH",
          "coingecko_coin_id": "weth"
        }
      }
    }
    ```

  <GreenSeparator />

  ## Introduced /networks/network/trending\_pools endpoint (Onchain/GT)

  🗓️ **February 19, 2024**

  Trending Pools endpoint, [/networks//trending\_pools](/reference/trending-pools-network) is now available to fetch a list of pools that are trending as seen on GeckoTerminal based on web visits and on-chain activities.

  <GreenSeparator />

  ## Introduced /search/pools endpoint (Onchain/GT)

  🗓️ **February 19, 2024**

  Added new endpoint to search for pools /search/pools based on keywords passed into query.
</Update>

<Update label="January 2024">
  ## Included new field for /coins/id endpoint

  🗓️ **January 18, 2024**

  We've included a new field "whitepaper" under "links" section for [/coins/](/reference/coins-id) endpoint

  **Example of responses:**

  ```json  theme={null}
  {
    "id": "bitcoin",
    ......
    "links": {
      "homepage": [],
      "whitepaper": "https://bitcoin.org/bitcoin.pdf", 👈
      "blockchain_site": [],
      "official_forum_url": [],
      "chat_url": [],
      "announcement_url": [],
      "twitter_screen_name": "bitcoin",
      "facebook_username": "bitcoins",
      "bitcointalk_thread_identifier": null,
      "telegram_channel_identifier": "",
      "subreddit_url": "https://www.reddit.com/r/Bitcoin/",
      "repos_url": {}
    },
    .......
  }
  ```
</Update>

<Update label="December 2023">
  ## Deprecated response fields for /coins/id

  🗓️ **December 13, 2023**

  The following data is now deprecated for [/coins/](/reference/coins-id) endpoint:

  * coingecko\_rank
  * coingecko\_score
  * developer\_score
  * community\_score
  * liquidity\_score
  * public\_interest\_score
  * public\_interest\_stats
  * alexa\_rank
  * bing\_matches

  <GreenSeparator />

  ## Introduced new historical total supply endpoints

  🗓️ **December 12, 2023**

  We've introduced Historical Total Supply data to Enterprise plan subscribers via these 2 exclusive endpoints:

  * [/coins//total\_supply\_chart](/reference/coins-id-total-supply-chart) : get historical total supply of a coin, by number of days away from now.
  * [/coins//total\_supply\_chart/range](/reference/coins-id-total-supply-chart-range) : get historical total supply of a coin, within a range of timestamp.

  <GreenSeparator />

  ## Included more trending coins

  🗓️ **December 07, 2023**

  We've expanded the capabilities of the [/search/trending](/reference/trending-search) endpoint.

  It now supports up to 15 trending coins, a significant increase from the previous limit of 7.

  <GreenSeparator />

  ## Improvement on pool data (Onchain/GT)

  🗓️ **December 03, 2023**

  Pool data now returns transaction stats for the last 1 hour. Unique buyers and sellers in the last 1 hour and 24 hours are now returned in the response
</Update>

<Update label="November 2023">
  ## Multiple Improvements

  🗓️ **November 21, 2023**

  The web\_slug data is now available in the following endpoints.

  * [/coins/](/reference/coins-id)
  * [/coins//contract/](/reference/coins-contract-address)

  This addition allows users to accurately link to a CoinGecko coin page using [www.coingecko.com/en/](http://www.coingecko.com/en/\{web_slug}).

  **Example of responses:**

  ```Text JSON theme={null}
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "web_slug": "bitcoin", 👈
    ......
    "tickers": [...]
  }
  ```

  For the [/asset\_platforms](/reference/asset-platforms-list) endpoint, we've introduced the native\_coin\_id data. This enables users to obtain the coin ID of different blockchain networks or asset platforms that may not have a contract address to look up

  **Example of responses:**

  ```Text JSON theme={null}
  {
    "id": "polygon-pos",
    "chain_identifier": 137,
    "name": "Polygon POS",
    "shortname": "MATIC", 
    "native_coin_id": "matic-network" 👈
  },
  ```

  <GreenSeparator />

  ## Introduced /simple/networks/network/token\_price/addresses endpoint (Onchain/GT)

  🗓️ **November 10, 2023**

  Inspired by CoinGecko API most popular endpoint, we have launched the [/simple/networks//token\_price/](/reference/onchain-simple-price), simple endpoint. Simply pass in addresses of any tokens on supported blockchain and get price data for it

  <GreenSeparator />

  ## Introduced /networks/network/pools/pool\_address/trades endpoint (Onchain/GT)

  🗓️ **November 08, 2023**

  You can now get the latest 300 trades in the past 24 hours of a given pool from this endpoint [/networks//pools//trades](/reference/pool-trades-contract-address). You may optionally filter by trade size as well. You can now build your own telegram bot alert!
</Update>

<Update label="October 2023">
  ## Introduced new endpoints (Onchain/GT)

  🗓️ **October 23, 2023**

  You can now fetch token information such as name, image, social links, and description via these endpoints:

  * To fetch information of tokens inside a pool, use [/networks//pools//info](/reference/pool-token-info-contract-address)
  * To fetch information of a specific token use [/networks//tokens//info](/reference/token-info-contract-address)
  * If you like to get token information of the most recently updated tokens, use [/tokens/info\_recently\_updated](/reference/tokens-info-recent-updated)
</Update>

<Update label="September 2023">
  ## Included new fields (Onchain/GT)

  🗓️ **September 11, 2023**

  Pool response data now returns price in the base and quote token of the pool base\_token\_price\_quote\_token and quote\_token\_price\_base\_token for your convenience without the need to do additional calculation to derive these values

  <GreenSeparator />

  ## Introduced new endpoints (Onchain/GT)

  🗓️ **September 06, 2023**

  Added new endpoints to allow querying multiple pools and tokens in a single API call. /networks/network/pools/multi/addresses and /networks/network/tokens/multi/addresses
</Update>

<Update label="June 2023">
  ## Included new fields (Onchain/GT)

  🗓️ **June 23, 2023**

  * More data added to the Pool response such as FDV, market cap (from CoinGecko if available), price change percentage, volume, number of buy/sell transactions
  * More data added when querying for token such as FDV, volume, market cap, and the top 3 pools

  <GreenSeparator />

  ## Introduced precision params for other endpoints

  🗓️ **June 15, 2023**

  The uses of 'precision' parameter allows to specify price data in full or 0-18 decimals, and previously was only made available for [/simple/price](/reference/simple-price) and [/simple/token\_price/](/reference/simple-token-price) endpoints.

  This parameter is now supported for more endpoints as listed below:

  * [/coins/markets](/reference/coins-markets)
  * [/coins/market\_chart](/reference/coins-id-market-chart)
  * [/coins/market\_chart/range](/reference/coins-id-market-chart)
  * [/coins//contract//market\_chart](/reference/contract-address-market-chart)
  * [/coins//contract//market\_chart/range](/reference/contract-address-market-chart-range)
  * [/coins//ohlc](/reference/coins-id-ohlc)

  <GreenSeparator />

  ## Multiple Improvements

  🗓️ **June 01, 2023**

  We've made enhancements to the /search/trending and /coins/asset\_platform\_id/contract/contract\_address endpoints:

  * Top 5 trending NFT data (based on high trading volume in the last 24 hours) is now included in the [/search/trending](/reference/trending-search) endpoint
  * Near Protocol contract address (e.g. wrap.near) is now supported for [/coins//contract/ ](/reference/coins-contract-address) endpoint
</Update>

<Update label="May 2023">
  ## Multiple Improvements (Onchain/GT)

  🗓️ **May 28, 2023**

  * Token metadata such as name, symbol, and CoinGecko ID are now returned in the responses for pools endpoints. Users will need to pass in this attribute include=base\_token, quote\_token
  * CoinGecko asset platform ID added to the response for [/networks](/reference/networks-list) endpoint

  <GreenSeparator />

  ## Added interval daily params to /coins/id/ohlc

  🗓️ **May 22, 2023**

  The [/coins//ohlc](/reference/coins-id-ohlc) endpoint now supports the "interval=daily" parameter for Paid Plan Subscribers

  Users can use this parameter to retrieve OHLC (Open/High/Low/Close) data on a daily interval for up to 180 days of date range.
</Update>

<Update label="April 2023">
  ## Included new fields

  🗓️ **April 26, 2023**

  We've added  'watchlist\_portfolio\_users' field to [/coins/](/reference/coins-id) endpoint responses.

  This refers to number of users who added the coin into a watchlist or portfolio.

  **Example of responses:**

  ```json JSON theme={null}
  {
  "id": "bitcoin",
  ......
  "watchlist_portfolio_users": 1449601, 👈
  "market_cap_rank": 1,
  ......
  "tickers": []
  }
  ```

  <GreenSeparator />

  ## Increased Rate Limit (Onchain/GT)

  🗓️ **April 19, 2023**

  We've increased the rate limit of Public Plan from 10 calls per minute to 30 calls per minute

  <GreenSeparator />

  ## Multiple Improvements (Onchain/GT)

  🗓️ **April 18, 2023**

  * base\_token\_native\_currency and quote\_token\_native\_currency added to the pools endpoint response. This allows you to obtain price in the network's native currency in addition to in USD
  * reserve\_in\_usd added to the pools endpoint response. This returns the total liquidity/reserve of the pool in USD
  * pool\_created\_at added to the pools endpoint response

  Example of responses for [/networks//pools/](/reference/pool-address) :

  ```json  theme={null}
  {
  "data": {
      "id": "eth_0xeb2eae8a9912a09cb0f13bfafd5ad56cd263bb3f",
      "type": "pool",
      "attributes": {
      "base_token_price_usd": "0.0000186523882966482",
      "base_token_price_native_currency": "0.00000000647822280242372", 👈
      "quote_token_price_usd": "2881.71870575097",
      "quote_token_price_native_currency": "1.0", 👈
      "base_token_price_quote_token": "0.000000006478222802",
      "quote_token_price_base_token": "154363323",
      "address": "0xeb2eae8a9912a09cb0f13bfafd5ad56cd263bb3f",
      "name": "DGX-1 / WETH",
      "pool_created_at": "2024-02-18T08:10:59Z", 👈
      "fdv_usd": "784687",
      "market_cap_usd": null,
      "price_change_percentage": {
      "h1": "34.67",
      "h24": "8406.81"
      },
      "transactions": {},
      "volume_usd": {},
      "reserve_in_usd": "110214.6247" 👈
      },
      "relationships": {}
      }
  }
  ```

  * [/networks//new\_pools](/reference/latest-pools-network) endpoint added to query new pools discovered for a network
  * [/networks/new\_pools](/reference/latest-pools-list) endpoint added to query new pools discovered across all networks

  <GreenSeparator />

  ## Included new fields

  🗓️ **April 03, 2023**

  We've added "symbol" field to these NFT endpoints responses:

  * [/nfts/markets](/reference/nfts-markets)
  * [/nfts/ ](/reference/nfts-id)
  * [/nfts//contract/](/reference/nfts-contract-address)

  **Example of responses:**

  ```Text JSON theme={null}
  {
  	"id": "pudgy-penguins",
    "contract_address": "0xBd3531dA5CF5857e7CfAA92426877b022e612cf8",
    "asset_platform_id": "ethereum",
    "name": "Pudgy Penguins",
    "symbol": "PPG", 👈
    ....
  },
  ```
</Update>

<Update label="March 2023">
  ## Included new fields

  🗓️ **March 27, 2023**

  We've added "links" field (e.g. homepage, twitter, discord) to these NFT endpoints responses:

  * [/nfts/](/reference/nfts-id)
  * [/nfts//contract/](/reference/nfts-contract-address)

  **Example of responses:**

  ```json  theme={null}
  {
    "id": "pudgy-penguins",
    "contract_address": "0xBd3531dA5CF5857e7CfAA92426877b022e612cf8",
    .......
    "links": {
      "homepage": "https://www.pudgypenguins.com/", 👈
      "twitter": "https://twitter.com/pudgypenguins",👈
      "discord": "https://discord.gg/pudgypenguins" 👈
    },
  	.......
  }
  ```

  <GreenSeparator />

  ## Introduced /coins/top\_gainer\_losers endpoint

  🗓️ **March 23, 2023**

  We've added [/coins/top\_gainers\_losers](/reference/coins-top-gainers-losers) endpoint exclusively for Paid Plan Subscribers.

  Users can now get the top 30 coins with largest price gain and loss by a specific time duration with this endpoint.

  <GreenSeparator />

  ## Improved OHLCV endpoint (Onchain/GT)

  🗓️ **March 23, 2023**

  [/networks//pools//ohlcv/](/reference/pool-ohlcv-contract-address) now returns more granularity `day,` `hour`, `minute` and multiple aggregates
</Update>

<Update label="February 2023">
  ## Multiple Improvements

  🗓️ **February 23, 2023**

  We've made some updates to the /coins/categories and /simple/token\_price/id endpoints:

  * Market cap and volume data for 'ecosystem' categories in the [/coins/categories](/reference/coins-categories) endpoint will now return 'null' until further notice. The CoinGecko team is actively working on improvements to provide more accurate data. If you have any feedback or suggestions, please reach out via [api@coingecko.com](mailto:api@coingecko.com).
  * Previously, the [/simple/token\_price/](/reference/simple-token-price) endpoint was unable to return data for some Solana coins. This issue has been resolved, and users can now expect accurate data for Solana coins from this endpoint.

  <GreenSeparator />

  ## Introduced /exchange/id/volume\_chart/range endpoint

  🗓️ **February 15, 2023**

  We've introduced the [/exchange//volume\_chart/range](/reference/exchanges-id-volume-chart-range) endpoint for Paid Plan Subscribers.

  This exclusive feature allows users to query full historical volume data of an exchange.
</Update>

<Update label="January 2023">
  ## Introduced /coins/list/new endpoint

  🗓️ **January 09, 2023**

  We've introduced the [/coins/list/new](/reference/coins-list-new) endpoint for Paid Plan Subscribers.

  This exclusive feature allows users to query the latest 200 coins on CoinGecko.
</Update>


# 1. Get data by ID or Address
Source: https://docs.coingecko.com/docs/1-get-data-by-id-or-address



## Methods to query price & market data of coins

### a. Coin ID

Using [/simple/price](/reference/simple-price) endpoint as example:

* `https://pro-api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&x_cg_pro_api_key=YOUR_API_KEY`

* The provided endpoint URL includes parameters such as `ids=bitcoin` and `vs_currencies=usd`, indicating that the intention to retrieve the current price of Bitcoin in US Dollars.

**How to obtain Coin ID aka API ID?** There are 3 options:

* Use [/coins/list](/reference/coins-list) endpoint, example of responses:

  <CodeGroup>
    ```json JSON theme={null}
    [
      ......
      {
      "id": "bitcoin", 👈
      "symbol": "btc",
      "name": "Bitcoin"
      },
      ......
    ]
    ```
  </CodeGroup>

* View the full list of coins with API ID, symbol and name using this [Google Sheet](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).

* Look for the "API ID“ by visiting the info section of a coin page on CoinGecko:

  <Frame>
    <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/7bf604e-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=ca1093ad1577a2160c53ee6ea3c9de8c" data-og-width="2122" width="2122" data-og-height="1256" height="1256" data-path="images/docs/7bf604e-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/7bf604e-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=58b6818eb39f1cc1cb13bfb1b827e9ef 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/7bf604e-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=debd856f53bd0349a94586da15246140 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/7bf604e-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=4995bc412246ed062435c7700fce33b0 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/7bf604e-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=54503566448e1f70bfd6e3938ff18830 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/7bf604e-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=45f0c1afb1803886ff058fe7682a3a2a 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/7bf604e-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=f3d3d13f19af39c3c2918e06f9552bd6 2500w" />
  </Frame>

### b. Contract Address

Other than using Coin ID, you may also query price & market data of a coin using contract address, using [/simple/token\_price/\{id](/reference/simple-token-price)} endpoint as example:

* `https://pro-api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&vs_currencies=usd&x_cg_pro_api_key=YOUR_API_KEY`

There are 3 parameters values required to apply for this endpoint:

* `id`: `Ethereum` (Asset Platform ID)
* `contract_addresses`: `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` (Contract Address)
* `vs_currencies`: `usd` (Target Currencies)

**How to obtain Coins/Tokens Contract Address**

* Use [/coins/list](/reference/coins-list) endpoint (`include_platform=true`), example of responses:
  <CodeGroup>
    ```json JSON theme={null}
    [
      ......
    	{
        "id": "1inch",
        "symbol": "1inch",
        "name": "1inch",
        "platforms": {
          "ethereum": "0x111111111117dc0aa78b770fa6a738034120c302",
          "avalanche": "0xd501281565bf7789224523144fe5d98e8b28f267",
          "binance-smart-chain": "0x111111111117dc0aa78b770fa6a738034120c302",
          "near-protocol": "111111111117dc0aa78b770fa6a738034120c302.factory.bridge.near",
          "energi": "0xdda6205dc3f47e5280eb726613b27374eee9d130",
          "harmony-shard-0": "0x58f1b044d8308812881a1433d9bbeff99975e70c",
          "polygon-pos": "0x9c2c5fd7b07e95ee044ddeba0e97a665f142394f"
          }
       },
      ......
    ]
    ```
  </CodeGroup>
* Look for the "Contract“ by visiting the info section of a coin page on CoinGecko.

<Note>
  ### Notes

  * Not all coins will have a contract address listed on the CoinGecko site.
  * If an address is not shown on the CoinGecko page, you will not be able to query the coin by its contract address via the API.
  * The contract addresses are curated by the CoinGecko team, if you find out any missing contract address, feel free to [share](https://support.coingecko.com/hc/en-us/requests/new) with us to review.
</Note>

<Frame>
  <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/576675c-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=d16b2cfd819ece1c689f6595081edcad" data-og-width="2096" width="2096" data-og-height="1484" height="1484" data-path="images/docs/576675c-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/576675c-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=2e16c3e076d1cd3f43af7fb949d2382a 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/576675c-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=e46ee9cc8a1f9be560c3ea1940695a02 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/576675c-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=c19faccaebd60eeeb79e8305ca20c609 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/576675c-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=68ad652fdbc4fc6739daaf8f0121a548 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/576675c-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=330f42772de72f72af2759e0c417db30 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/576675c-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=d9a988b003d06757a4f9886a9e047d58 2500w" />
</Frame>

* Get the token contract address from project website, white-paper, documentation, or block explorer site:

  * [Uniswap Documentation](https://docs.uniswap.org/protocol/concepts/governance/overview#uni-address)
  * [Block Explorer (Etherscan)](https://etherscan.io/token/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984)

## Specify target currency to return

In the 2 examples above, both queries for Coin ID and Contract Address contain `vs_currencies=usd`. Most of the CoinGecko API endpoints will require you to specify the currency.

CoinGecko API data supports all major fiat currencies and some famous crypto currencies like the following:

| Type           | Currency     | vs\_currencies (Param value) |
| -------------- | ------------ | ---------------------------- |
| Fiat           | US Dollar    | `usd`                        |
| Fiat           | Japanese Yen | `jpy`                        |
| Fiat           | Euro         | `eur`                        |
| Cryptocurrency | Bitcoin      | `btc`                        |
| Cryptocurrency | Ether        | `eth`                        |
| Cryptocurrency | Binance Coin | `bnb`                        |

For full list of supported currencies, please go to [/simple/supported\_vs\_currencies](/reference/simple-supported-currencies) endpoint

## Other way to obtain coin prices & market data

Using [/coins/market ](/reference/coins-markets) endpoint as example to query prices and market data of coins in bulk

* `https://pro-api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&x_cg_pro_api_key=YOUR_API_KEY`

There are 4 parameters values applied for this endpoint:

* `vs_currency`: `usd`
* `order`: `market_cap_desc` — The endpoint response will be sorted in descending order, from the coins with the largest market cap to those with the smallest.
* `per_page`: `100` — The results of coins per page are set at 100 in this case (maximum is 250).
* `page`: `1` — The page number of the results is determined by the parameter `per_page`. In the case of `per_page=100` and `page=2`, the responses will include coins ranked 101 to 200 on CoinGecko, sorted by market cap, as per the specified endpoint.


# 10-mins Tutorial Guide
Source: https://docs.coingecko.com/docs/10-mins-tutorial-guide

New to CoinGecko API? Fret not. Whether you're a programmer or someone with zero coding experience, we've got you covered!

If you are not a developer and prefer to learn only specific tutorials on Google Sheet/Excel, feel free to check [👶 Tutorials (Beginner-friendly)](/docs/tutorials-beginner-friendly)

| Tutorial Steps                                                    | Description                                                                                      |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [1. Get data by ID or Address](/docs/1-get-data-by-id-or-address) | Learn how to use different endpoints by obtaining Coin ID and token's contract address at first. |
| [2. Get Historical Data](/docs/2-get-historical-data)             | Learn how to get historical data of a coin by using different historical endpoints.              |
| [3. Get Exchanges & NFT Data](/docs/3-get-exchanges-nft-data)     | Learn how to query exchanges and NFT data by accessing different endpoints.                      |
| [4. Get On-chain Data](/docs/4-get-on-chain-data)                 | Learn how to use `/onchain` GT endpoints to query onchain data.                                  |


# 2. Get Historical Data
Source: https://docs.coingecko.com/docs/2-get-historical-data



<Check>
  ### **Tips**

  * Most of the historical data are returned and queried using UNIX Timestamp.
    * If you are not familiar with UNIX Timestamp, you may use tool like [epochconverter.com](https://www.epochconverter.com/) to convert between UNIX Timestamp and human readable date.
  * You may use either coin ID or contract address to get the historical data.
</Check>

There are five different endpoints to get historical data of a coin:

| Endpoint                                                                                                         | Description                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [/coins/\{id}/history](/reference/coins-id-history)                                                              | Get the historical data (price, market cap, 24hrs volume, etc.) at a given date for a coin based on a particular coin ID.                                |
| [/coins/\{id}/market\_chart](/reference/coins-id-market-chart)                                                   | Get the historical chart data of a coin including time in UNIX, price, market cap and 24hrs volume based on particular coin ID.                          |
| [/coins/\{id}/market\_chart/range](/reference/coins-id-market-chart-range)                                       | Get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hrs volume based on particular coin ID.     |
| [/coins/\{id}/contract/\{contract\_address}/market\_chart](/reference/contract-address-market-chart)             | Get the historical chart data of a coin including time in UNIX, price, market cap and 24hrs volume based on token contract address.                      |
| [/coins/\{id}/contract/\{contract\_address}/market\_chart/range](/reference/contract-address-market-chart-range) | Get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hrs volume based on token contract address. |

<Note>
  ### **Notes**

  The data granularity (interval) for [/market\_chart](/reference/coins-id-market-chart) and [/market\_chart/range](/reference/coins-id-market-chart-range) endpoints is automatic and based on the date range:

  * 1 day from current time = 5-minutely data
  * 1 day from anytime (except from current time) = hourly data
  * 2-90 days from current time or anytime = hourly data
  * above 90 days from current time or anytime = daily data (00:00 UTC)
</Note>


# 3. Get Exchanges & NFT Data
Source: https://docs.coingecko.com/docs/3-get-exchanges-nft-data



You can get Exchange and NFT data just like how you get the coins data:

1. Get the ID (exchange or NFT) from `/list` endpoint.
2. Use the ID to query latest or historical market data

| Type                   | Coins                                                          | NFTs                                                         | Exchanges                                                              | Derivatives                                                            |
| ---------------------- | -------------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Get Full List with IDs | [/coins/list](/reference/coins-list)                           | [/nfts/list](/reference/nfts-list)                           | [/exchanges/list](/reference/exchanges-list)                           | [/derivatives/exchanges/list](/reference/derivatives-exchanges-list)   |
| Get latest market data | [/coins/\{id}](/reference/coins-id)                            | [/nfts/\{id}](/reference/nfts-id)                            | [/exchanges/\{id}](/reference/exchanges-id)                            | [/derivatives/exchanges/\{id}](/reference/derivatives-exchanges-id)    |
| Get Historical Data    | [/coins/\{id}/market\_chart](/reference/coins-id-market-chart) | [/nfts/\{id}/market\_chart](/reference/nfts-id-market-chart) | [/exchanges/\{id}/volume\_chart](/reference/exchanges-id-volume-chart) | [/exchanges/\{id}/volume\_chart](/reference/exchanges-id-volume-chart) |


# 4. Get On-chain Data
Source: https://docs.coingecko.com/docs/4-get-on-chain-data



Here are some of the important parameters to take note while using Onchain DEX API Endpoints:

* Blockchain Networks
* DEXs
* Pool Contract Address
* Token Contract Address

## Blockchain Networks

<Note>
  ### Notes

  * Please do not use CoinGecko Asset Platform ID as the Network ID in Onchain DEX API Endpoints (CoinGecko Asset Platform ID ≠ GT Network ID)

  * Example:

    * Asset Platform on CoinGecko: `ethereum`
    * Onchain Network ID: `eth`
</Note>

**How to obtain Network ID?**

* Use [/onchain/networks](/reference/networks-list) endpoint, example of response:

  <CodeGroup>
    ```json JSON theme={null}
    {
      "data": [
        {
          "id": "eth",  👈 Network ID
          "type": "network",
          "attributes": {
            "name": "Ethereum",
            "coingecko_asset_platform_id": "ethereum" 👈 CoinGecko Asset Platform ID
          }
        },
       ......
      ]
    }
    ```
  </CodeGroup>

* Go to [GeckoTerminal](https://www.geckoterminal.com/)

  1. Select or search for a blockchain network.

  2. Copy the slug from the URL:

  <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/5b9a903-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=3d58e3708238e2c869afeb50f36ba74a" alt="" data-og-width="3024" width="3024" data-og-height="1964" height="1964" data-path="images/docs/5b9a903-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/5b9a903-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=4989c53c98cdf6a3b7e313e6a9804ab0 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/5b9a903-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=d969711a6080bed61c7ea74574f8c9c4 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/5b9a903-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=00c5bc4b0bddd4b5c2a1db9feccf6cb9 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/5b9a903-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=fae4d183cc2e8adffa335e7fd646f7d0 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/5b9a903-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=557a46ebb5da439b2f10be9d31b78618 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/5b9a903-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=c2a5d9ec2a1c59d2479ee38eb887b103 2500w" />

## DEXs

Some of the pools endpoints require you to provide DEX ID along with Network ID to query the pools on a particular DEX (Decentralized Exchange).

Using [/onchain/networks/\{network}/dexes/\{dex}/pools](/reference/top-pools-dex) as example:

* `https://pro-api.coingecko.com/api/v3/onchain/networks/eth/dexes/uniswap_v3/pools?x_cg_pro_api_key=YOUR_API_KEY`

There are 2 parameter values required to apply for this endpoint:

* `network`: `eth` (network ID)
* `dex`: `uniswap_v3` (DEX ID)

**How to obtain DEX ID?**

* Use [/onchain/networks/\{network}/dexes](/reference/dexes-list) endpoint, example of response:

  <CodeGroup>
    ```json JSON theme={null}
    {
      "data": [
        {
          "id": "uniswap_v2", 👈 DEX ID
          "type": "dex",
          "attributes": {
            "name": "Uniswap V2"
          }
        },
      ......
      ]
    }
    ```
  </CodeGroup>

* Go to [GeckoTerminal](https://www.geckoterminal.com/)

  1. Select or search for a blockchain network.

  2. Choose the DEX from the DEXs List on the top (e.g. Uniswap V3).

  3. Copy the slug from the URL:

  <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/f68325c-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=58ed481ea98687173a3cbf9493c73669" alt="" data-og-width="3024" width="3024" data-og-height="1964" height="1964" data-path="images/docs/f68325c-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/f68325c-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=c65139982268e19bca411599181dc636 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/f68325c-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=643f58b710957517ea5bf1f44719c865 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/f68325c-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=caf2849ed3d33c014ad8f9ebeb4e5335 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/f68325c-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=053455ede8148791a44e985dfaf9b7ca 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/f68325c-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=174ed6ec00474abb69e58b1955992896 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/f68325c-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=ece2e33e95afc4a26ce9632aee91ab09 2500w" />

## Methods to query Onchain Data

### a. Pool Contract Address

Most of the time, you will need a pool contract address along with Network ID to query the onchain data, especially when using the Pools Endpoints.

Using [/onchain/networks/\{network}/pools/\{address}](/reference/pool-address) as example:

* `https://pro-api.coingecko.com/api/v3/onchain/networks/eth/pools/0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc?x_cg_pro_api_key=YOUR_API_KEY`

There are 2 parameter values required to apply for this endpoint:

* `network`: `eth` (network ID)
* `address`: `0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc` (pool contract address)

**How to obtain the pool contract address? (e.g.`WETH/USDC`)**

* Look for the contract address section of pool page on [GeckoTerminal](https://www.geckoterminal.com/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640):

  <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/741fbc7-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=a80b0dafe3d5db5a527e02ea18fcc2ad" alt="" data-og-width="3023" width="3023" data-og-height="1708" height="1708" data-path="images/docs/741fbc7-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/741fbc7-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=aa93c1116c1d08b205703db5012bab40 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/741fbc7-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=3a880e5a52baccf4ba59ebccbe403e0e 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/741fbc7-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=3ce6dab28d3f89568ebcb90c06c5b476 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/741fbc7-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=94b5901e74822c87037922b50b6c4502 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/741fbc7-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=363a6b4dae6ba819ca437b307847bfca 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/741fbc7-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=094ec22716e968240e77cf49c8a85670 2500w" />

* Get the pool contract address from the project website, white-paper, documentation, or block explorer site:

  * [Block Explorer (Etherscan)](https://etherscan.io/address/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640)
  * [DEX (Uniswap)](https://info.uniswap.org/#/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640)

### b. Token Contract Address

Apart from the pool contract address, you also have the option to query onchain data by using the token contract address, using [/onchain/networks/\{network}/tokens/\{token\_address}/pools](/reference/top-pools-contract-address) as example:

* `https://pro-api.coingecko.com/api/v3/onchain/networks/eth/tokens/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48/pools?x_cg_pro_api_key=YOUR_API_KEY`

There are 2 parameter values required to apply for this endpoint:

* `network`: `eth` (network ID)
* `address`: `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` (token contract address)

**How to obtain tokens contract address (e.g. UNI):**

* Look for the contract address section of pool page on GeckoTerminal:

  <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/56f6c15-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=f889558b4ea90de11cb582a6b7de0abc" alt="" data-og-width="3023" width="3023" data-og-height="1714" height="1714" data-path="images/docs/56f6c15-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/56f6c15-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=9ce75c1292f0d566078dda3943b1fe7e 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/56f6c15-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=4516e149c14a8bdac49d99f6e4915363 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/56f6c15-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=d630847a7ee3c65560f8ebb5ad44ad38 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/56f6c15-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=7509e70029974a1eab8c270e88190071 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/56f6c15-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=598fa1be5c51ab303f7c53b707ea1424 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/56f6c15-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=1f47293f6b9d8bddb811001f3ff1f65e 2500w" />

* Get the token contract address from the project website, white-paper, documentation, or block explorer site. For example:

  * [Uniswap Documentation](https://docs.uniswap.org/protocol/concepts/governance/overview#uni-address)
  * [DEX (Uniswap)](https://info.uniswap.org/#/tokens/tokens/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984)
  * [Block Explorer (Etherscan)](https://etherscan.io/token/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984)


# AI Prompts
Source: https://docs.coingecko.com/docs/ai-prompts

CoinGecko API AI prompt library

Accelerate your development with CoinGecko's curated AI prompts. These prompts are designed to guide AI-powered coding assistants in correctly implementing our official API SDKs (libraries), helping you spend less time debugging and more time building.

## How to Use Our Prompts

Integrating these prompts into your workflow is simple. Copy the entire markdown prompt for your chosen language and provide it as context to your AI assistant.

1. For **Chat Interfaces (Claude, ChatGPT, etc.)**: Paste the prompt at the beginning of your conversation before asking the AI to write code.
2. For **Cursor IDE**: Add the prompt to your project's `Rules` to enforce the guidelines across all AI interactions.
3. For **GitHub Copilot**: Save the prompt to a file (e.g. `coingecko_rules.md`) and reference it in your chat with `@workspace #coingecko_rules.md`.

## Available Prompts

Select the prompt that matches your project's tech stack.

* 🐍 **[Python](/docs/python-ai-prompts)**: A complete guide for implementing the CoinGecko API using our official [coingecko-sdk](https://pypi.org/project/coingecko-sdk/).
* 🟦 **[TypeScript](/docs/typescript-ai-prompts#/)**: The definitive prompt for integrating the CoinGecko API with our official [@coingecko/coingecko-typescript](https://www.npmjs.com/package/@coingecko/coingecko-typescript) package.

## Best Practices

To get the most out of our AI prompts, keep these tips in mind:

* **Be Specific**: After providing the main prompt, give the AI a clear, specific task (e.g. "Write a function to fetch the price of Bitcoin and Ethereum in EUR").
* **Customize**: Feel free to modify the prompts to fit your project's unique requirements or coding standards.
* **Version Control**: Store your customized prompts in your repository to ensure your entire team benefits from consistent AI-generated code.
* **Always Review**: Treat AI-generated code as a starting point. Always review it for security, performance, and correctness.


# API Status
Source: https://docs.coingecko.com/docs/api-status

CoinGecko's API status page provides information on the current status and incident history of CoinGecko API (Public & Pro)

<Check>
  ### **Tips**

  * You can view our live updates, and subscribe to updates via Email, Slack and Discord.
  * Instead of subscribing to all updates, you may click on 'Select services' to subscribe to either Public or Pro API updates.
</Check>

<img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/73a827b-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=5fefdb6ae9202da2644d922ccf79356f" alt="" data-og-width="1840" width="1840" data-og-height="1528" height="1528" data-path="images/reference/73a827b-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/73a827b-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=7403db5955420bec7d169d0a4dcac3d1 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/73a827b-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=8c74b607d2e47dc3581f21c3de9c1ba3 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/73a827b-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=c0daaedaca6d6d3f721eb672c676554f 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/73a827b-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=76e79ef68e3a410718a9d12e6bd4bf3c 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/73a827b-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=444dda0811606f4c6deffbaddd3d3450 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/73a827b-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=5e2b0d20dad6ec97b912b05fe235c9a6 2500w" />

* CoinGecko API Status — [https://status.coingecko.com](https://status.coingecko.com)
* Incident & Maintenance History — [https://status.coingecko.com/incidents](https://status.coingecko.com/incidents)
* Uptime Calendar — [https://status.coingecko.com/incidents/uptime-calendar](https://status.coingecko.com/incidents/uptime-calendar)


# Best Practices
Source: https://docs.coingecko.com/docs/best-practices

Wonder how to use different endpoints together? This is the perfect place for you

## User Journey for CoinGecko API Endpoints

<img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/60fecdf-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=509cde2f1085a0102c86f391db0837b1" alt="" data-og-width="1328" width="1328" data-og-height="710" height="710" data-path="images/docs/60fecdf-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/60fecdf-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=5ea5fec3760a2bfb5c33277e3511479f 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/60fecdf-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=5f926c131c7bb67afb13f89d3ec5e942 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/60fecdf-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=574e6d149e5fa962e8f7a3bfe0f5371b 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/60fecdf-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=7a78b8790c86a92040eabf432a6cd64b 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/60fecdf-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=885633eb663ed8e54827a45a74e67ab8 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/60fecdf-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=f3051a393bcc6c0ff6a3dee44ec89ac7 2500w" />

### "Discovery/Navigational Endpoints"

**Examples:**

* [/coins/list](/reference/coins-list) — can be used to query all the supported coins on CoinGecko with names, symbols and coin IDs that can be used in other endpoints.
* [/search/trending](/reference/trending-search) — can be used to query trending search coins, categories and NFTs on CoinGecko.

### "Supporting Endpoints"

**Examples:**

* [/simple/supported\_vs\_currencies](/reference/simple-supported-currencies) — can be used to query the list of currencies for other endpoints that include parameters like `vs_currencies`, allowing to obtain the corresponding data for those currencies.
* [/asset\_platforms](/reference/asset-platforms-list) — can be used to query the list of asset platforms for other endpoints that contain parameters like `id` or `ids` (asset platforms), allowing the retrieval of corresponding data for these asset platforms.

### "Data Endpoints"

**Examples:**

* [/simple/price](/reference/simple-price) — can be used to query the prices of coins using the unique coin IDs that can be obtained from the "Discovery/Navigational Endpoints" mentioned above.
* [/coins/\{id}](/reference/coins-id) — can be used to query the coin data using the unique coin IDs that can be obtained from the "Discovery/Navigational Endpoints" mentioned above.

## User Journey for Onchain DEX API Endpoints (GeckoTerminal data)

<img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/fc38fa8-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=011c5c6d5cb8ff880eb957e528c57891" alt="" data-og-width="1328" width="1328" data-og-height="544" height="544" data-path="images/docs/fc38fa8-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/fc38fa8-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=5ec52efdba31f801866c7c7bd041eafd 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/fc38fa8-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=fd4e8526d2c0eb8347aa54eca4ed4289 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/fc38fa8-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=6f2af440ec46cd89576b60c00f532ea1 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/fc38fa8-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=c8e9cb77c67cf34a1cbb3ad7d99dbe84 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/fc38fa8-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=5e7bcc911db7af9296a5782886417ddf 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/docs/fc38fa8-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=62e234622a2ec45e8575c14c0532c6f4 2500w" />

### "Discovery/Navigational Endpoints"

**Examples:**

* [/onchain/trending\_pools](/reference/trending-pools-list) - can be used to query trending pools across all networks on GeckoTerminal.
* [/onchain/search/pools](/reference/search-pools) - can be used to search for any pools on GeckoTerminal.

### "Supporting Endpoints"

**Examples:**

* [/onchain/networks-list](/reference/networks-list) - can be used to query all the supported networks on GeckoTerminal.
* [/onchain/networks/\{network}/dexes](/reference/dexes-list) - can be used to query all the supported decentralized exchanges (DEXs/`dexes`) on GeckoTerminal based on network id that can be obtained from the endpoint mentioned above.

### "Data Endpoints"

**Examples:**

* [/onchain/simple/networks/\{network}/token\_price/\{addresses}](/reference/onchain-simple-price) - can be used to query any token price using the token address and network id that can be obtained from the "Discovery/Navigational Endpoints" and "Supporting Endpoints" mentioned above.
* [/onchain/networks/\{network}/pools/\{address}](/reference/pool-address) - can be used to query the data of a specific pool based on the pool address and network id that can be obtained from the "Discovery/Navigational Endpoints" and "Supporting Endpoints" mentioned above.


# Building with AI
Source: https://docs.coingecko.com/docs/building-with-ai

Quick tips to empower your AI applications with CoinGecko API, and leverage our AI capabilities to help you build better and easier.

CoinGecko provides a powerful suite of AI-native tools to help you integrate real-time, historical, and onchain market data into your applications. Whether you're building a sophisticated trading bot, a market analysis tool, or a simple portfolio tracker, our AI toolkit is here to accelerate your development.

## Using `llms.txt`

To help AI models interact with CoinGecko data effectively, we provide an `llms.txt` file at [/llms-full.txt](/llms-full.txt). This file gives models context on how to best query our API, ensuring more accurate and efficient data retrieval. We recommend utilizing this in your integrations of MCP and AI applications.

## CoinGecko MCP Server

The **MCP (Model-Context-Protocol)** Server is your gateway for connecting AI agents and large language models, like Claude and Gemini, directly to CoinGecko's live data streams. It's ideal for building conversational applications that can perform complex, real-time crypto analysis and answer user queries with up-to-the-minute information. Learn how to connect your AI agent by checking out [CoinGecko MCP Server](/docs/mcp-server)

## Tools for Your Workflow

We've integrated AI assistance directly into our documentation to help you find answers and ship faster.

1. Use the **'Copy page'** button to copy endpoint-specific markdown prompts. You can take these prompts to your favorite LLM chat interface to explore use cases or generate boilerplate code.
2. Stuck on a problem? Click the **'AI Support'** button anywhere in our docs to chat with our AI Assistant. It's trained to resolve your inquiries instantly.

<Frame>
  <img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/e9b8e85-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=d50f10a06097c241df55c3ab5b809d84" data-og-width="2006" width="2006" data-og-height="1364" height="1364" data-path="images/docs/e9b8e85-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/e9b8e85-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=cb8143580ee2990c66855af7ec934061 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/e9b8e85-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=c47b12a514d650c26024442ddb64d4f9 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/e9b8e85-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=199af9b08dc0bdfae67226399b4409de 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/e9b8e85-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=b44f67afc911a4bbacb227726e9823cb 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/e9b8e85-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=93c5c92256523702b423fc0547a3a833 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/e9b8e85-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=a95711c3e148ec09d808029d05006564 2500w" />
</Frame>


# Clients
Source: https://docs.coingecko.com/docs/clients

Explore client resources, including official Swagger JSON and unofficial Python wrapper

## API Swagger JSON (OAS)

<a href="https://github.com/coingecko/coingecko-api-oas" target="_blank" rel="noopener noreferrer">
  <Frame>
    <img src="https://mintcdn.com/coingecko/HbbqJRkzM8wbxbUM/images/docs/51c3a7e-image.png?fit=max&auto=format&n=HbbqJRkzM8wbxbUM&q=85&s=89a0e23044b6440703a9949f2d111a72" noZoom data-og-width="1404" width="1404" data-og-height="552" height="552" data-path="images/docs/51c3a7e-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/HbbqJRkzM8wbxbUM/images/docs/51c3a7e-image.png?w=280&fit=max&auto=format&n=HbbqJRkzM8wbxbUM&q=85&s=f790f47b07cb2309a9d8a4ccd644957a 280w, https://mintcdn.com/coingecko/HbbqJRkzM8wbxbUM/images/docs/51c3a7e-image.png?w=560&fit=max&auto=format&n=HbbqJRkzM8wbxbUM&q=85&s=dbff0485155760cc1ba8771bda4323c4 560w, https://mintcdn.com/coingecko/HbbqJRkzM8wbxbUM/images/docs/51c3a7e-image.png?w=840&fit=max&auto=format&n=HbbqJRkzM8wbxbUM&q=85&s=bc7acc8a93d983a1a7850777347ce5f0 840w, https://mintcdn.com/coingecko/HbbqJRkzM8wbxbUM/images/docs/51c3a7e-image.png?w=1100&fit=max&auto=format&n=HbbqJRkzM8wbxbUM&q=85&s=d15a8bd2ddd52e934cc9a07200431b12 1100w, https://mintcdn.com/coingecko/HbbqJRkzM8wbxbUM/images/docs/51c3a7e-image.png?w=1650&fit=max&auto=format&n=HbbqJRkzM8wbxbUM&q=85&s=0b03fab442b9e8129bda1ab9f10c4f12 1650w, https://mintcdn.com/coingecko/HbbqJRkzM8wbxbUM/images/docs/51c3a7e-image.png?w=2500&fit=max&auto=format&n=HbbqJRkzM8wbxbUM&q=85&s=70bb4883d506a864c3f6a2cb09914c97 2500w" />
  </Frame>
</a>

* [CoinGecko Pro OAS](https://docs.coingecko.com/reference/endpoint-overview)
  * CoinGecko Pro API — [coingecko-pro.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/coingecko-pro.json)
  * GeckoTerminal Onchain API (Pro) — [onchain-pro.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/onchain-pro.json)

* [CoinGecko Public/Demo OAS](https://docs.coingecko.com/v3.0.1/reference/endpoint-overview)
  * CoinGecko Public/Demo API — [coingecko-demo.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/coingecko-demo.json)
  * GeckoTerminal Onchain API (Demo) — [onchain-demo.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/onchain-demo.json)

***

## Official CoinGecko API SDK

Here are the official API SDKs maintained by us.

* [🐍 coingecko-python (Python)](https://github.com/coingecko/coingecko-python)
* [🟦 coingecko-typescript (Typescript)](https://github.com/coingecko/coingecko-python)

Want us to support your favorite programming language? Let us know [here](https://forms.gle/JJLH3SXiL2eJaGzBA)!

**Not a developer?** Fred not, check our no-code tutorial for beginners here: [Tutorials (Beginner-friendly)](/docs/tutorials-beginner-friendly)


# Common Errors & Rate Limit
Source: https://docs.coingecko.com/docs/common-errors-rate-limit



## Common Errors

The server responds to a user’s request by issuing status codes when the request is made to the server. Kindly refer to the table below to further understand the status codes when indicating the success or failure of an API call.

| Status Codes                  | Description                                                                                                                                                                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `400` (Bad Request)           | This is due to an invalid request and the server could not process the user's request                                                                                                                                                                         |
| `401` (Unauthorized)          | This is due to the lack of valid authentication credentials for the requested resource by the user                                                                                                                                                            |
| `403` (Forbidden)             | This is likely indicating that your access is blocked by our server, and we're unable to authorize your request                                                                                                                                               |
| `408` (Timeout)               | This error indicates that our server did not receive your complete request within our allowed time frame. This is usually caused by a slow network connection on your end or network latency. Please check your connection and try sending the request again. |
| `429` (Too many requests)     | This is likely indicating that the rate limit has reached. The user should reduce the number of calls made, or consider scaling their service plan that has much higher rate limits and call credits                                                          |
| `500` (Internal Server Error) | This is a generic error response indicating that the server has encountered an unexpected issue that prevented it from fulfilling the request                                                                                                                 |
| `503` (Service Unavailable)   | The service is currently unavailable. Please check the API status and updates on [https://status.coingecko.com](https://status.coingecko.com)                                                                                                                 |
| `1020` (Access Denied)        | This is due to violation of CDN firewall rule                                                                                                                                                                                                                 |
| `10005`                       | You may not have access to this endpoint. e.g. 'This request is limited Pro API subscribers'. You may wanna subscribe to a paid plan [here](https://www.coingecko.com/en/api/pricing)                                                                         |
| `10002` (Missing API Key)     | API Key Missing. Please make sure you're using the right authentication method.<br />For Pro API, ensure you pass in `x_cg_pro_api_key` parameter with a Pro Key.<br />For Demo API, ensure you pass in `x_cg_demo_api_key` parameter with a Demo Key.        |
| `10010` (Invalid API Key)     | You have provided incorrect API key credentials. If you are using Pro API key, please change your root URL from `api.coingecko.com` to `pro-api.coingecko.com`                                                                                                |
| `10011` (Invalid API Key)     | You have provided incorrect API key credentials. If you are using Demo API key, please change your root URL from `pro-api.coingecko.com` to `api.coingecko.com`                                                                                               |
| CORS error                    | Occurs when the server doesn't return the CORS headers required. You may learn more and attempt the recommended solutions [here](https://www.bannerbear.com/blog/what-is-a-cors-error-and-how-to-fix-it-3-ways/#how-to-fix-a-cors-error)                      |

## Rate Limit

<Note>
  ### **Notes**

  * If you're using the Public API with Google Sheet and got hit with error, this is due to the IP sharing among Google Sheet users, and we have no control over this.
  * If you need reliable performance, please **register for a demo account** or **subscribe to a paid plan** that comes with dedicated infra (API key) to prevent rate limit issues.
  * For more details, please go to the page [here](https://www.coingecko.com/en/api/pricing).
</Note>

* For Public API user (Demo plan), the rate limit is \~30 calls per minutes and it varies depending on the traffic size.
* If you're Pro API user (any paid plan), the rate limit is depending on the paid plan that you're subscribed to.
* Regardless of the HTTP status code returned (including `4xx` and `5xx` errors), all API requests will count towards your **minute rate limit**.


# Common Use Cases
Source: https://docs.coingecko.com/docs/common-use-cases

Discover the common use cases of CoinGecko API by our users

## 1. Get Coins Logo Images

* Use [/coins/id](/reference/coins-id) endpoint.

  * This endpoint can be used to query other coin's metadata like: links, categories, contract address, community, description in different languages and many more.
  * Coin descriptions may include newline characters represented as `\r\n` (escape sequences), which may require processing for proper formatting.

* Use [Token Info by Token Address](/reference/token-info-contract-address) endpoint to get metadata of tokens listed on GeckoTerminal.com.

## 2. Best Endpoint for Latest Crypto Price

* Use [/simple/price](/reference/simple-price) endpoint.
* This endpoint can be used to query other market data like market cap, 24-hour trading volume and 24-hour price change percentage.

## 3. Get All Trading Pairs (Tickers) of a Coin

* Use [/coins/id/tickers](/reference/coins-id-tickers) endpoint.

## 4. Get Trading Pairs of Specific Coins from a Specific Exchange

* Use[ /coins/id/tickers](/reference/coins-id-tickers) endpoint by supplying specific exchange ID.

## 5. Building Telegram Bot for Latest Coin Listings

* Use [/coins/list/new](/reference/coins-list-new) endpoint.

## 6. Get List of Coins Under Specific Category

* For CoinGecko [categories](https://www.coingecko.com/en/categories), use [/coins/markets](/reference/coins-markets) endpoint by supplying specific category.
* For GeckoTerminal [categories](https://www.geckoterminal.com/category), use [Pools by Category ID](/reference/pools-category) endpoint by supplying specific category.

## 7. Identify DEX Decentralized Exchanges

* Use [/exchanges/list](/reference/exchanges-list) endpoint to get full list of exchanges with ID on CoinGecko.

* Use [/exchanges/id](/reference/exchanges-id) to find out whether the exchange is centralized or decentralized.

* Example of responses (using Uniswap V3 as example) :

  Since Uniswap is a DEX, therefore it shows `"centralized": false`

  <CodeGroup>
    ```json JSON theme={null}
    {
      "name": "Uniswap V3 (Ethereum)",
      ......
      "centralized": false, 👈
      ......
      "tickers": [],
      "status_updates": []
    }
    ```
  </CodeGroup>

## 8. Get Bitcoin Dominance Data (BTC.D)

* Use [/global ](/reference/crypto-global)endpoint.

* Example of responses:

  <CodeGroup>
    ```json JSON theme={null}
    {
      "data": {
        "active_cryptocurrencies": 12414,
        ......
        "market_cap_percentage": { 👈
          "btc": 47.82057011844006,👈
          "eth": 16.943340351591583,
          ......
        },
        "market_cap_change_percentage_24h_usd": -5.032104325648996,
        "updated_at": 1706002730
      }
    }
    ```
  </CodeGroup>

## 9. Get Market Cap or Dominance of a Specific Ecosystem

* Use [/coins/categories](/reference/coins-categories).
* The endpoint also returns the 24-hour percentage change, offering insights into the traction of different categories or ecosystems.

## 10. Get Token Lists of a Specific Blockchain Network

* Use [/token\_lists/asset\_platforms\_id/all.json](/reference/token-lists) endpoint.
* Supply asset platform id to the endpoint.

## 11. Get 7-Day Sparkline Price Data of a Coin

* Use [/coins/id](/reference/coins-id) or [/coins/markets](/reference/coins-markets) endpoints by flagging `sparkline = true`.

## 12. Get Link to Individual CoinGecko Coin Page

* Use [/coins/list](/reference/coins-list) endpoint to get the coin **`{ID}`**.
  * Supply API ID in this URL path format: `www.coingecko.com/en/coins/{ID}`
* If you wish to the obtain the URL slug of a specific CoinGecko Coin Page, e.g. `www.coingecko.com/en/coins/{web_slug}` you may use [/coin/id](/reference/coins-id) endpoint and obtain the **`{web_slug}`** value.

## 13. Check Coin Status and Stale Price Updates

* Active: use [/coins/list](/reference/coins-list) endpoint, only active coins will be shown by default. You may also flag **`status=inactive`** to get a list of inactive coins.
* Price Stale: use [/simple/price](/reference/simple-price) endpoint, flag `include_last_updated_at=true` to check latest update time.

## 14. Get Real-Time and Historical Exchange of BTC in USD

* Current exchange rate: use [/exchange\_rates](/reference/exchange-rates) endpoint.
* Historical exchange rate: use [/coins/id/history](/reference/coins-id-history) or [/coins/id/market\_chart](/reference/coins-id-market-chart) endpoints.

## 15. Get Watchlist Portfolio Data of a Coin

* Use [/coins/id](/reference/coins-id) endpoint by supplying coin ID.

* Example of responses:

  <CodeGroup>
    ```json JSON theme={null}
    {
      "id": "bitcoin",
      ......
      "watchlist_portfolio_users": 1487932, 👈
      "market_cap_rank": 1,
      ......
    }
    ```
  </CodeGroup>

## 16. Get Historical Data for Inactive Coins

**Note**: This is available for paid plan subscribers only.

* Use [/coins/list](/reference/coins-list) endpoint, specifying the status param as `inactive`.

* Example of endpoint request: `https://pro-api.coingecko.com/api/v3/coins/list?include_platform=false&status=inactive&x_cg_pro_api_key=YOUR_API_KEY`

* Retrieve the coin's ID from the endpoint mentioned above and use it to access historical data via the following endpoints:

  * [/coins/id/history](/reference/coins-id-history)
  * [/coins/id/market\_chart](/reference/coins-id-market-chart)
  * [/coins/id/market\_chart/range](/reference/coins-id-market-chart-range)
  * [/coins/id/contract/contract\_address/market\_chart](/reference/contract-address-market-chart)
  * [/coins/id/contract/contract\_address/market\_chart/range](/reference/contract-address-market-chart-range)

## 17. Get TVL (Total Value Locked) data of a Coin

* Use [/coins/id](/reference/coins-id) endpoint by supplying coin ID.

* Example of responses:

  <CodeGroup>
    ```json JSON theme={null}
    "total_value_locked":
    {
        "btc": 72324,
        "usd": 4591842314
    }
    ```
  </CodeGroup>

## 18. Query Search for Coins, Categories, NFTs, Exchanges, and Pools

We have 2 Search endpoints:

* [/search](/reference/search-data) endpoint allows you to search for coins, categories, exchanges (markets), and NFTs listed on CoinGecko.com. You may query by name or symbol.
* [/search-pools](/reference/search-pools) endpoint allows you to search for pools listed on GeckoTerminal.com. You may query by pool contract address, token contract address, or token symbol.

## 19. Get List of Blockchain Networks supported on CoinGecko and GeckoTerminal.

CoinGecko and GeckoTerminal support different sets of blockchain networks. You can use the following endpoints to find the list of supported networks and their respective IDs:

* CoinGecko: [/asset-platforms-list](/reference/asset-platforms-list)
* GeckoTerminal ([onchain endpoints](/reference/endpoint-overview#-onchain-dex-endpoints-geckoterminal)): [/networks-list](/reference/networks-list)

## 20. Get Native Coin of a Blockchain Network (Asset Platform)

You may use the [/asset-platforms-list](/reference/asset-platforms-list) endpoint to obtain the native coin ID of all networks (asset platforms) listed on [www.coingecko.com](http://www.coingecko.com.).

## 21. Get Liquidity data of a Liquidity Pool or Token

There are multiple onchain endpoints that provide the liquidity data (`reserve_in_usd`) of a pool, for example: [Specific Pool Data by Pool Address](/reference/pool-address). You may also get liquidity data (`total_reserve_in_usd`) of a token, using endpoints like: [Token Data by Token Address](/reference/token-data-contract-address).

Note: `reserve_in_usd` (pool) represents the total liquidity of all tokens within a specific pool, whereas `total_reserve_in_usd` (token) refers to the total liquidity portion attributable to a specific token across all available pools.

## 22. Get list of onchain DEX pools based on specific criteria

* Use [/pools/megafilter](/reference/pools-megafilter) to retrieve data for onchain DEX pools that match a given set of filters.

* Example of use cases:

  * Custom filtering: Combine multiple params — like liquidity thresholds, FDV ranges, 24-hour volume, and more — to extract the precise datasets you need.
  * Risk and Quality checks: Apply fraud filters to weed out risky projects.

* For more details on examples and available filters, refer to:

  * [Changelog — New Megafilter Endpoint](/changelog#february-2025)
  * [Live Filtering on GeckoTerminal](https://www.geckoterminal.com/)

## 23. Get List of Trending Coins

* Use the following endpoints to get trending coins and pools:

  * [Trending Search List](/reference/trending-search/) — Trending Coins, NFTs, Categories on CoinGecko.com, based on user searches.
  * [Trending Search Pools](/reference/trending-search-pools/) — Trending Pools and Tokens on GeckoTerminal.com, based on user searches.

* Other useful endpoints:

  * [Top Gainers & Losers](/reference/coins-top-gainers-losers) on CoinGecko.com, by specific time duration.
  * [Trending Pools List](/reference/trending-pools-list) and [Trending Pools by Network](/reference/trending-pools-network) on GeckoTerminal.com, by specific time duration.

## 24. Get Security Info of Tokens

* By using [Token Info by Token Address](/reference/token-info-contract-address) endpoint, you can obtain the following security related data:

  * GeckoTerminal Score (Pool, Transaction, Creation, Info, Holders)
  * Holders count and distribution percentage
  * Mint and Freeze Authority

## 25. Get Latest Token/Pool Data from Launchpad

* Use [megafilter](/reference/pools-megafilter) endpoint to retrieve latest launchpad data, by flagging `sort=pool_created_at_desc`. Learn more on [changelog](/changelog#now-supported%3A-launchpad-data-pump-fun-%26-more-%2C-granular-ohlcv%2C-and-honeypot-info).
* **Request example (Get latest pools on Pump.fun)**:

<CodeGroup>
  ```bash Bash theme={null}
  https://pro-api.coingecko.com/api/v3/onchain/pools/megafilter?page=1&networks=solana&dexes=pump-fun&sort=pool_created_at_desc&x_cg_pro_api_key=YOUR_API_KEY
  ```
</CodeGroup>

<br />

⚡️ Need Real-time Data Streams? Try [WebSocket API](https://docs.coingecko.com/websocket)

<a href="/websocket">
  <Frame>
    <img src="https://mintcdn.com/coingecko/Vs362t2sI6OcYG2J/images/wss-banner-3.png?fit=max&auto=format&n=Vs362t2sI6OcYG2J&q=85&s=0100cf5563559f9abaa820953d7b51d1" noZoom data-og-width="2400" width="2400" data-og-height="470" height="470" data-path="images/wss-banner-3.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/Vs362t2sI6OcYG2J/images/wss-banner-3.png?w=280&fit=max&auto=format&n=Vs362t2sI6OcYG2J&q=85&s=7af476c453eac401449894b2082e1e51 280w, https://mintcdn.com/coingecko/Vs362t2sI6OcYG2J/images/wss-banner-3.png?w=560&fit=max&auto=format&n=Vs362t2sI6OcYG2J&q=85&s=24e14a72713ad27eab213dbd12095087 560w, https://mintcdn.com/coingecko/Vs362t2sI6OcYG2J/images/wss-banner-3.png?w=840&fit=max&auto=format&n=Vs362t2sI6OcYG2J&q=85&s=55c681e36c2e8a23b6560b650ddc76b7 840w, https://mintcdn.com/coingecko/Vs362t2sI6OcYG2J/images/wss-banner-3.png?w=1100&fit=max&auto=format&n=Vs362t2sI6OcYG2J&q=85&s=c57736ebd1362301406aa43788b31f92 1100w, https://mintcdn.com/coingecko/Vs362t2sI6OcYG2J/images/wss-banner-3.png?w=1650&fit=max&auto=format&n=Vs362t2sI6OcYG2J&q=85&s=02e2f731fde9f613e7c701ad78ac898f 1650w, https://mintcdn.com/coingecko/Vs362t2sI6OcYG2J/images/wss-banner-3.png?w=2500&fit=max&auto=format&n=Vs362t2sI6OcYG2J&q=85&s=66df269e8b922a799737ec64b66268d1 2500w" />
  </Frame>
</a>

With WebSocket, you can now stream ultra-low latency, real-time prices, trades, and OHLCV chart data. <br />
Subscribe to our [paid API plan](https://www.coingecko.com/en/api/pricing) (Analyst plan & above) to access WebSocket and REST API data delivery methods.


# Endpoint Showcase
Source: https://docs.coingecko.com/docs/endpoint-showcase

Discover how CoinGecko API is used at CoinGecko.com and GeckoTerminal.com

## CoinGecko

### [Home Page](https://www.coingecko.com)

<img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/5efbe42-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=d63633d56cc7a4d3c7d71a931a7112d8" alt="" data-og-width="2200" width="2200" data-og-height="1528" height="1528" data-path="images/docs/5efbe42-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/5efbe42-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=094bb211db972bea7d8b66716f5eed3a 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/5efbe42-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=da211f3d8c1aec265d53891dc8f43ed6 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/5efbe42-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=fc59610f652ef640696568679b90b723 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/5efbe42-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=4d8905af936b5a34968b6dad1c59f7c5 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/5efbe42-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=1679ab4c405a2ad10f8037bf0e830a0d 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/5efbe42-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=299d7edb9949e51d03a2c357eb0ce127 2500w" />

1. [/global](/reference/crypto-global) — Display global crypto data such as number of active cryptocurrencies, exchanges and etc.
2. [/search/trending](/reference/trending-search) — Display trending search coins, NFTs and categories.
3. [/coins/top\_gainers\_losers](/reference/coins-top-gainers-losers) — Display the largest gainers in 24hr.
4. [/coins/categories](/reference/coins-categories) — Display all the categories list.
5. [/coins/markets](/reference/coins-markets) — Display all the supported coins with market related data.

### [Coin Page](https://www.coingecko.com/en/coins/bitcoin)

<img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/2f71923-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=4f3f1e9c241ac3c7fb3c6fdfec6f516d" alt="" data-og-width="2104" width="2104" data-og-height="1492" height="1492" data-path="images/docs/2f71923-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/2f71923-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=9a71372f238cd241108306680d5a2a46 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/2f71923-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=cad968f1b3cf92f47091e006897bd9c8 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/2f71923-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=0977ba4c9e4fd44e025685bd4527bfbe 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/2f71923-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=a7bdbd1e213ad62e8763ad00177567e7 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/2f71923-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=602e29d2123e3681f7f7eca248348f6c 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/2f71923-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=1931234bdbbc82514affdaf503710e38 2500w" />

1. [/coins/\{id} ](/reference/coins-id)— Display all the coin data including name, price, market related data, website, explorers and etc.
2. [/simple/price](/reference/simple-price) — Display data such as latest coin price, market cap and 24hr trading volume.
3. * [/coins/\{id}/history](/reference/coins-id-history) — Display the historical price data.
   * [/coins/\{id}/market\_chart](/reference/coins-id-market-chart) — Display the historical data in line chart.
   * [/coins/\{id}/ohlc](/reference/coins-id-ohlc) — Display the historical data in candlestick chart.

### [Exchanges Page](https://www.coingecko.com/en/exchanges/hyperliquid-spot)

<img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/9e12298-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=8306154da0e21d2b902eadda23cb7dfc" alt="" data-og-width="2128" width="2128" data-og-height="1394" height="1394" data-path="images/docs/9e12298-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/9e12298-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=cad9ee450cbc127562e5bc65d922339a 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/9e12298-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=03edf7a33acb4c998656ce6b1007e6ad 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/9e12298-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=ba853e66f1bed4efcf8a6a1bf0ad5c6f 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/9e12298-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=ab46e891e1c84ca00961a549e27e9434 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/9e12298-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=b741c73166b49da858f7a9de5e9dda45 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/9e12298-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=063b3126d0c4236464345bb4cf9c38d0 2500w" />

1. [/exchanges/\{id}](/reference/exchanges-id) — Display the exchange information such as name, type, market related data such as trading volume and etc.
2. [/exchanges/\{id}/volume\_chart](/reference/exchanges-id-volume-chart) — Display the historical volume chart data.
3. [/exchanges/\{id}/tickers](/reference/exchanges-id-tickers) — Display the exchange's tickers.

### [NFTs Page](https://www.coingecko.com/en/nft/pudgy-penguins)

<img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/cda9241-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=666f359cbc3e65fef656e351617f2b9f" alt="" data-og-width="1845" width="1845" data-og-height="1867" height="1867" data-path="images/docs/cda9241-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/cda9241-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=885542d09a7346a1a7000df7cd2a4452 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/cda9241-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=16419d75014aab231cda6c6d7596a1da 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/cda9241-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=1df3f1689b943b7a3f53d7e6099b0897 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/cda9241-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=5aa83a631e8e6960cbe416b7d4375fbd 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/cda9241-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=e037c284ec52bb4f9c9c666c8501d99d 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/cda9241-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=c27add5b7c705a2034414567ab1693de 2500w" />

1. [/nfts/\{id}](/reference/nfts-id) — Display NFT data such as name, contract address, website, market related data such as floor price, market cap, volume and etc.
2. [/nfts/\{id}/market\_chart](/reference/nfts-id-market-chart) — Display the historical market data in chart.
3. [/nfts/\{id}](/reference/nfts-id) — Display the description of the NFT collection.
4. [/nfts/\{id}/tickers](/reference/nfts-id-tickers) — Display the tickers of the NFT collection on different NFT marketplace.

## GeckoTerminal

### [Home Page](https://www.geckoterminal.com/)

<img src="https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/8d5ac53-image.png?fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=006779468e238af7cb515c3b90d478b7" alt="" data-og-width="3023" width="3023" data-og-height="1881" height="1881" data-path="images/docs/8d5ac53-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/8d5ac53-image.png?w=280&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=1e64c2a847217aeb6a1524ba665d0bb7 280w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/8d5ac53-image.png?w=560&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=98994fc84ed994e69ef12ea133093092 560w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/8d5ac53-image.png?w=840&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=e1f9614a1227137104e693480cb739cb 840w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/8d5ac53-image.png?w=1100&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=de8a324c611cc5b2557a1d130224346a 1100w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/8d5ac53-image.png?w=1650&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=d94dee12678b5c879f5e6ebafe107d4a 1650w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/8d5ac53-image.png?w=2500&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=96c61ccae7576b9f486e28459ca4e963 2500w" />

1. [/onchain/search/pools ](/reference/search-pools)— Allow users to search for pools on GeckoTerminal.
2. [/onchain/networks](/reference/networks-list) — Display a list of supported networks on GeckoTerminal.
3. [/onchain/networks/trending\_pools](/reference/trending-pools-list) — Display a list of trending pools across all networks on GeckoTerminal.
4. [/onchain/networks/new\_pools](/reference/latest-pools-list) — Display all the latest pools across all networks on GeckoTerminal.
5. [/onchain/categories](/reference/categories-list) — Display all the onchain categories on GeckoTerminal.

### [Chain Page](https://www.geckoterminal.com/eth/pools)

<img src="https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/7b49f3e-image.png?fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=26f7cdd8a92a237ac6358be830d42c55" alt="" data-og-width="3023" width="3023" data-og-height="1883" height="1883" data-path="images/docs/7b49f3e-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/7b49f3e-image.png?w=280&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=46918d142183d419c4d2ddb6852c2b9e 280w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/7b49f3e-image.png?w=560&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=2b60fc1e44832b2df0b0fa39e01cc6dc 560w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/7b49f3e-image.png?w=840&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=9ce014411117fb3907620cca658c4b81 840w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/7b49f3e-image.png?w=1100&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=4e1b0fb9ea89441c506fe7cd66007e91 1100w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/7b49f3e-image.png?w=1650&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=bc062efdc17e4506c6d1fa9c203e524f 1650w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/7b49f3e-image.png?w=2500&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=ee169d02c1f17780b97daf3ee9e34189 2500w" />

1. [/onchain/networks/\{network}/dexes](/reference/dexes-list) — Display all the supported dex on a network on GeckoTerminal.
2. [/onchain/networks/\{network}/trending\_pools](/reference/trending-pools-network) — Display a list of trending pools on a network on GeckoTerminal.
3. [/onchain/networks/\{network}/new\_pools](/reference/latest-pools-network) — Display a list of new pools on a network on GeckoTerminal.
4. [/onchain/networks/\{network}/pools](/reference/top-pools-network) — Display all the top pools on a network on GeckoTerminal.
5. [/onchain/categories/\{category\_id}/pools](/reference/pools-category) — Display all the pools under a specific onchain category on GeckoTerminal.

### [Pool Page](https://www.geckoterminal.com/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640)

<img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/43e04c2-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=dedf21f04c9bbf11fbf376f83b101969" alt="" data-og-width="3023" width="3023" data-og-height="1887" height="1887" data-path="images/docs/43e04c2-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/43e04c2-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=6e355b30d2a491ccf540d269d631721c 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/43e04c2-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=2088b61a6ae8a189a4249db17fd75928 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/43e04c2-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=ced214f96c8c869eca7627410782dc7a 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/43e04c2-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=722d09f605c5a0eabeda3e194f6bd51c 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/43e04c2-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=4d921a31f241b78515f25be7a698a6ff 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/43e04c2-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=1f522f2b1fbc4e1cf96c5e4bf7cb3f44 2500w" />

1. * [/onchain/networks/\{network}/pools/\{address}](/reference/pool-address) — Display pool data such as price, transactions, volume and etc.
   * [/onchain/networks/\{network}/pools/\{pool\_address}/info](/reference/pool-token-info-contract-address) — Display pool information such as name, symbol, image URL, description and etc.
2. [/onchain/networks/\{network}/pools/\{pool\_address}/ohlcv/\{timeframe}](/reference/pool-ohlcv-contract-address) — Display the OHLCV chart of the pool.
3. [/onchain/networks/\{network}/pools/\{pool\_address}/trades](/reference/pool-trades-contract-address) — Display the trades of the pool in the past 24 hours.

### [Categories Page](https://www.geckoterminal.com/category)

<img src="https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/cd8f5e-image.png?fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=912a6001736c59cf4fcdbf7bdce05814" alt="" data-og-width="3023" width="3023" data-og-height="1887" height="1887" data-path="images/docs/cd8f5e-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/cd8f5e-image.png?w=280&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=c97b53b79138f3e1e2f909e8e563c7fe 280w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/cd8f5e-image.png?w=560&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=84aedbbff60dc6f80fa478d0f389c31c 560w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/cd8f5e-image.png?w=840&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=80ff73fe40ba9b98c15894752d42a981 840w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/cd8f5e-image.png?w=1100&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=331705cce03b7b5aea56d00bc22a294d 1100w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/cd8f5e-image.png?w=1650&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=28fe2d9a7552ce2477be4c616b7f4fad 1650w, https://mintcdn.com/coingecko/Jrf60GKLjFfVX1SS/images/docs/cd8f5e-image.png?w=2500&fit=max&auto=format&n=Jrf60GKLjFfVX1SS&q=85&s=b7750c4ae2c4de27b6b6bedb41c8af96 2500w" />

1. [/onchain/categories](/reference/categories-list) — Display list of onchain categories with market data.
2. [/onchain/categories/\{id}/pools](/reference/pools-category) — Display list of pools with market data of a specific onchain category.


# CoinGecko MCP Server (Beta)
Source: https://docs.coingecko.com/docs/mcp-server

MCP Server for Crypto Price & Market Data. MCP (Model Context Protocol) is an open standard that allows Large Language Model (LLM) and other AI agents to securely and intelligently interact with external data sources and tools.

<img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/63500e3-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=02ca3c105f2e635a6f2c7d055295f0d0" alt="" data-og-width="1200" width="1200" data-og-height="628" height="628" data-path="images/reference/63500e3-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/63500e3-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=1720600784a5461c52e10e227df80b7c 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/63500e3-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=293707f46e3f25f53958009a55744b3b 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/63500e3-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=f4ace3ad35e9091f9e89a9d24dd1f169 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/63500e3-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c904edee1f977ba97e1e659498da6daa 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/63500e3-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=cad8e9cba2ce58e6142c92359fefa25a 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/63500e3-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=a7b36813341277fed347efe5b18b7967 2500w" />

<Warning>
  ### Welcome to the CoinGecko MCP Server!

  **CoinGecko MCP Server is currently in Beta.** We're constantly improving, and your feedback is crucial. Please share any thoughts or suggestions via [this feedback form](https://docs.google.com/forms/d/e/1FAIpQLSf06DOBauiZ8XS6NwWXUUwhFluH7jKHOAa3y4VsrkyGbLKyfA/viewform).
</Warning>

# 📕 Overview

The official CoinGecko MCP Server is now live, making CoinGecko data readily available to your AI models and applications. With the CoinGecko MCP, you can empower your agents to:

* **Access real-time market data**: Get aggregated prices, market cap, and trading volume for over 15k+ coins on CoinGecko, integrated across 1,000+ exchanges.
* **Dive into onchain analytics**: Query onchain DEX price and liquidity data for more than 8M tokens across 200+ networks via GeckoTerminal.
* **Discover market trends**: Instantly find trending coins, new token listings, top gainers/losers, and popular NFT collections.
* **Retrieve rich metadata**: Pull essential details like project descriptions, logos, social links, contract addresses, security info, and more.
* **Analyze historical performance**: Access historical price, market data, and OHLCV for any cryptocurrency.
* **Explore crypto categories**: Effortlessly list coins within specific sectors like Meme, DeFi, Layer 1, AI agent, and more.

<Frame caption="MCP Demo with Claude Desktop">
  <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/8c45171-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=a17e15d1b672940226da961086b986ed" data-og-width="2930" width="2930" data-og-height="1882" height="1882" data-path="images/reference/8c45171-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/8c45171-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c026d75329f72ee001fafea1c6d35659 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/8c45171-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=e90eb94aa0cd98f9409042706e598703 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/8c45171-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=fd02d8b78f1e6b325e29b59795d1f84f 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/8c45171-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=2ef4c5580ce4de3f5caae91b4c9be11d 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/8c45171-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c9efb0e238afbfe0a3d7bf54ede0c3c1 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/8c45171-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=2b8f2e6b387cd3c9f9c229a31c1efe12 2500w" />
</Frame>

# 🔥 Getting Started

Connecting your AI to CoinGecko is simple. We offer several MCP server options to fit your needs, from keyless access for testing to authenticated connections for production applications.

Most MCP-compatible clients, like Claude Desktop, Gemini CLI, and Cursor, can be configured using a simple JSON file (e.g., `claude_desktop_config.json`)

<Note>
  ### Prerequisites

  * Make sure your device has `node` installed. You can download it from [nodejs.org/download](https://nodejs.org/en/download)
</Note>

## Which MCP Server Should You Use?

Here's a breakdown of the available options to help you choose the right one:

| MCP Server Type                 | Best For                                                                                                                                                                                                                                | Endpoints                                | Status      | Setup Details                                                                 |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ----------- | ----------------------------------------------------------------------------- |
| Remote Server (Public, Keyless) | - First-time users, quick tests, and basic queries<br />- Connect instantly without any registration<br />- Subject to shared rate limits, not for heavy use                                                                            | Primary: `/mcp`<br />Alternative: `/sse` | Public Beta | [mcp.api.coingecko.com](https://mcp.api.coingecko.com/)                       |
| Remote Server (Authenticated)   | - Scalable apps, AI agent integrations<br />- Unlocks 76+ tools available under your Demo/Pro plan<br />- Higher, reliable rate limits with 24/7 uptime. Get your API key [here](https://www.coingecko.com/en/api/pricing)              | Primary: `/mcp`<br />Alternative: `/sse` | Public Beta | [mcp.pro-api.coingecko.com](https://mcp.pro-api.coingecko.com/)               |
| Local Server                    | - Ideal for local development, desktop AI apps<br />- Build/test your AI app even without an active internet connection<br />- Demo/Pro API key to access more tools. Get your API key [here](https://www.coingecko.com/en/api/pricing) | Local server instance                    | Beta        | [npmjs/coingecko-mcp](https://www.npmjs.com/package/@coingecko/coingecko-mcp) |

## 🔗 Endpoint Options

Each remote server offers two connection methods to ensure compatibility with various MCP clients:

### Primary Endpoint (HTTP Streaming)

* **Public Server**: `https://mcp.api.coingecko.com/mcp`
* **Pro Server**: `https://mcp.pro-api.coingecko.com/mcp`
* Uses HTTP streaming protocol for real-time data transfer.
* Recommended for most modern MCP clients.

### Alternative Endpoint (SSE — Server-Sent Events)

* **Public Server**: `https://mcp.api.coingecko.com/sse`
* **Pro Server**: `https://mcp.pro-api.coingecko.com/sse`
* Uses Server-Sent Events for compatibility.
* Use this if you encounter connection issues with the primary endpoint.

<Note>
  Most clients work with either endpoint. The configuration examples below use the SSE endpoint by default for maximum compatibility.
</Note>

## Remote Server (Public, Keyless)

The easiest way to get started. Just add the following to your client's `mcp_config.json` file.

<Note>
  ### Client-Specific Config

  The file name and location depend on your client. Find your config file here: [modelcontextprotocol.io/quickstart](https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server)
</Note>

Add the following configuration to your `mcp_config.json`:

<CodeGroup>
  ```json JSON theme={null}
  {
    "mcpServers": {
      "coingecko_mcp": {
        "command": "npx",
        "args": [
          "mcp-remote",
          "https://mcp.api.coingecko.com/mcp"
        ]
      }
    }
  }
  ```
</CodeGroup>

Here's a quick 2-minute tutorial for setting up the public server with Claude Desktop:

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/PDYJvtKok0E" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

## Remote Server (Authenticated)

To access more tools and higher rate limits, use your CoinGecko API key with our hosted "Bring Your Own Key" (BYOK) server. Get your API key [here](https://www.coingecko.com/en/api/pricing)

### Step 1: Add the configuration

Add the following configuration to your `mcp_config.json`:

<CodeGroup>
  ```json JSON theme={null}
  {
    "mcpServers": {
      "coingecko_mcp": {
        "command": "npx",
        "args": [
          "mcp-remote",
          "https://mcp.pro-api.coingecko.com/mcp"
        ]
      }
    }
  }
  ```
</CodeGroup>

### Step 2: Authorize your MCP access

After adding the config, the first time your client tries to use the CoinGecko MCP, a new browser tab will open, redirecting you to our authentication page:

<img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/0fd54e7-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c40d3876ad3b12c0c3177231e8642bf7" alt="" data-og-width="1627" width="1627" data-og-height="1611" height="1611" data-path="images/reference/0fd54e7-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/0fd54e7-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=b44038862f84320e55096acf29d704ab 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/0fd54e7-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=d7518c452993e3c2191de720716fc28a 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/0fd54e7-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=f4e361fa7c96759e52cf23b245e44bfc 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/0fd54e7-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=41d3e848470a50259a8aabd2f11f879d 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/0fd54e7-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=4767ab92447bc5ba7a7f1ed2994945ea 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/0fd54e7-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=686d5177b5697a4561eae0f10f157694 2500w" />

* Simply paste in your CoinGecko API key, and authorize to link your key to the MCP session.

  ✨ Don't have an API key yet? Upgrade to Pro today! Read more [here](https://www.coingecko.com/en/api/pricing).

* You can also toggle between dynamic/static tools here. Learn more about [Dynamic Tools](#dynamic-vs-static-tools).

## Local Server (API Key Required)

For local development and maximum control, run the MCP server directly on your machine. This method offers the rate limits based on your API plan.

<CodeGroup>
  ```json JSON theme={null}
  {
    "mcpServers": {
      "coingecko_mcp_local": {
        "command": "npx",
        "args": [
          "-y",
          "@coingecko/coingecko-mcp"
        ],
        "env": {
          "COINGECKO_PRO_API_KEY": "YOUR_PRO_API_KEY",
          "COINGECKO_ENVIRONMENT": "pro"
        }
      }
    }
  }
  ```
</CodeGroup>

✨ Don't have an API key yet? Get your free Demo key or upgrade to Pro! Read more [here](https://www.coingecko.com/en/api/pricing).

* Configure the `env` based on your API key tier:

  * Pro API access:
    <CodeGroup>
      ```json JSON theme={null}
      ...
            "env": {
              "COINGECKO_PRO_API_KEY": "YOUR_PRO_API_KEY",
              "COINGECKO_ENVIRONMENT": "pro"
            }
      ...
      ```
    </CodeGroup>
  * Demo API access:
    <CodeGroup>
      ```json JSON theme={null}
      ...
            "env": {
              "COINGECKO_DEMO_API_KEY": "YOUR_DEMO_API_KEY",
              "COINGECKO_ENVIRONMENT": "demo"
            }
      ...
      ```
    </CodeGroup>

# 🚀 Connecting with Claude

Connecting CoinGecko MCP to Claude is straightforward. The method varies slightly depending on your Claude plan.

## For Claude Free Users (via Claude Desktop)

You **must use the Claude Desktop app** and modify the configuration file.

1. **Locate`claude_desktop_config.json`**: Follow the instructions [here](https://modelcontextprotocol.io/quickstart/user) to find the file on your system.
2. **Add a server config**: Copy and paste one of the server configs above that matches your use case.
3. **Restart Claude Desktop**: Close and reopen the app for the changes to take effect.

## For Claude Pro Users

<Check>
  ### Tips

  You can also follow the same steps as the Free users by modifying the `claude_desktop_config.json` file.
</Check>

1. In Claude ([claude.ai](https://claude.ai/) or the Desktop app), click on 'Add connectors' in your chat.

   <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/5cd6a58-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=73013011cc734857c113270206f71e7b" alt="" data-og-width="1606" width="1606" data-og-height="1122" height="1122" data-path="images/reference/5cd6a58-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/5cd6a58-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=e6833e4c3da93dedaec0f9ee341c0ea7 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/5cd6a58-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=f3176360bc6ddb6195743bcd82cd80ed 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/5cd6a58-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=900afa23a6af477b66b2fc58d1108a14 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/5cd6a58-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=2a6dbc4be6a8d688e0d037c7ee1ec418 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/5cd6a58-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=75dbaec8d5e3d998870e7e07f77b0c51 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/5cd6a58-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c27022d416fe6df622e6f0ac386fea0a 2500w" />

2. Click on 'Add custom connector'

   <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/1459ea5-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=63c2c7bc4254c52ba263b9617aae51bd" alt="" data-og-width="1843" width="1843" data-og-height="988" height="988" data-path="images/reference/1459ea5-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/1459ea5-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=488051a2a6574be78e62eebf533b7ba9 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/1459ea5-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=0a2dc2058e55364193572e1c5a9162a8 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/1459ea5-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=85d55bb6a7cd9c4ae2b02abce971c344 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/1459ea5-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c04b37491fcfc8454d43ccc56dc2cde4 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/1459ea5-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=6386434cc86f48afd82a283e676ad6f9 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/1459ea5-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=ab805d6c5f0c8745b99a2497eed3074d 2500w" />

3. Remote MCP server URL:

   * Keyless access: `https://mcp.api.coingecko.com/mcp`
   * Authenticated access (BYOK): `https://mcp.pro-api.coingecko.com/mcp`

   <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/b465d51-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=075452b45aa6696f046084f5a23d610b" alt="" data-og-width="1146" width="1146" data-og-height="899" height="899" data-path="images/reference/b465d51-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/b465d51-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=ac7d12f41f9375d1b13e6ddee2d2617c 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/b465d51-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=145c9550a2097b66c3aea388d63f8489 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/b465d51-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=b2c2f85d97c0c320e83045c31dbcfd51 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/b465d51-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=0914181d22bbe3d687c452b6be3649f2 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/b465d51-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=5c7df15af6e89de35ebf07bb186c6332 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/b465d51-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=43c552ceb2c3604b16b2018e3dca319c 2500w" />

4. Click on 'Add', and you're ready to go!

# 🚀 Connecting with ChatGPT

OpenAI ChatGPT have just launched an MCP connector, but requires [developer mode](https://platform.openai.com/docs/guides/developer-mode) toggle turned on.

1. Open your profile > Connectors > Advanced Settings > Toggle Developer Mode On

2. In the Connectors modal, choose "Create" and enter the CoinGecko MCP server info

   <Frame>
     <img
       src="https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-1.png?fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=19b9da2451dbb287b3e14bbd1bb1d6c4"
       style={{
      width: "400px", height: "auto"
    }}
       data-og-width="921"
       width="921"
       data-og-height="1330"
       height="1330"
       data-path="images/reference/mcp-open-ai-chatgpt-1.png"
       data-optimize="true"
       data-opv="3"
       srcset="https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-1.png?w=280&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=1e0e27aefe9eed409e50802d46ccbd96 280w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-1.png?w=560&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=4fa547e688348c71af6bd7a65018a06b 560w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-1.png?w=840&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=b58a95c0d11926961008038c5c150a2c 840w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-1.png?w=1100&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=d9a04921b35edb6034fe498ce69e06c2 1100w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-1.png?w=1650&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=043bd546e1eadb1d7b20b1cdc44fe5d5 1650w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-1.png?w=2500&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=deb9413356da4ff107766f1c483d14b8 2500w"
     />
   </Frame>

3. Before prompting, choose "+" > More > Developer Mode > CoinGecko MCP tool must be turned on

   <Frame>
     <img
       src="https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-2.png?fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=2dbce0217b55c42f75bcf72b1840261c"
       style={{
      width: "500px", height: "auto"
    }}
       data-og-width="1604"
       width="1604"
       data-og-height="404"
       height="404"
       data-path="images/reference/mcp-open-ai-chatgpt-2.png"
       data-optimize="true"
       data-opv="3"
       srcset="https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-2.png?w=280&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=1164c4b43b3973808b53e78219db4544 280w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-2.png?w=560&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=57565551346ddc2479ec396c5f03a5ad 560w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-2.png?w=840&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=9ffd706dd65fc5d64cae76ed5c44c6db 840w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-2.png?w=1100&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=20e6b62405c7069c6c58d6523a98854b 1100w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-2.png?w=1650&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=963d3992d6e0d46cfbbc56bd4179c099 1650w, https://mintcdn.com/coingecko/-YWykcjHRtoo7cBr/images/reference/mcp-open-ai-chatgpt-2.png?w=2500&fit=max&auto=format&n=-YWykcjHRtoo7cBr&q=85&s=2eabd675061763732754fc304f7e48e9 2500w"
     />
   </Frame>

# 💡 Example Prompts

Tap into the full potential of CoinGecko data — use these prompts to kickstart your next AI build.

### Simple Queries

> * What is the current price of Bitcoin in USD?
> * What is the market cap of Ethereum?
> * What are the top 3 trending coins on CoinGecko right now?
> * What are the top AI coins on GeckoTerminal now?
> * What is the floor price of the Pudgy Penguins NFT collection?

### Advanced Queries

> * Show me the current top 10 cryptocurrencies by market cap. Include their price, 24h change, and total volume. Display this in an interactive table.
>
>   <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/9ef35ab-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=76c2d6cbda125a20f3d2d4ee8bd5b840" alt="" data-og-width="2915" width="2915" data-og-height="1884" height="1884" data-path="images/reference/9ef35ab-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/9ef35ab-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c48640c27703887235b99f419b09ba12 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/9ef35ab-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=0ae223b5ab2812b2dc516ebea4bad63b 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/9ef35ab-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=50da86d6358bd614574590fec55e69f7 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/9ef35ab-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=948e0ca92b980bbfe5ba2afb76b3f34f 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/9ef35ab-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=9762d7eda6e8d5516b4fdb6f551a0003 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/9ef35ab-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=48de11fa6a230658b33645bf771fbabc 2500w" />
>
> * Generate a 30-day price chart for Ethereum (ETH) against USD, showing both price and trading volume.
>
>   <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/249fc22-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=b92c7f7e4c503e7d5b1e285f0901c850" alt="" data-og-width="2904" width="2904" data-og-height="1886" height="1886" data-path="images/reference/249fc22-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/249fc22-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=c3ac5ca1c3f030e3030df10fe6598321 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/249fc22-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=99ba5dee1419b3f6d4a9500554643c7f 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/249fc22-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=d255006760aa0d4c5c625ea1d610cf9c 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/249fc22-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=a959c53fc30a7ace129534b45d25a8cd 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/249fc22-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=0429bc6d59230e2290787c0f7c4ddefb 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/249fc22-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=ab3786ea42c1add908c744ca57da4090 2500w" />

### Creative and Fun Ideas

> * Create a quiz to tell me which cryptocurrency I am based on my personality.
>
>   <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/fb09018-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=9849ef5a53aedccf2ac0c9bc39ee5953" alt="" data-og-width="2909" width="2909" data-og-height="1887" height="1887" data-path="images/reference/fb09018-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/fb09018-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=0b256fa8214e83fd391836a3edaeca2f 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/fb09018-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=2d6d0b3bc94f5913bfee1b6096067e1b 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/fb09018-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=6c9ab464d9d3cb1c4b6e2b033182997d 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/fb09018-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=7af07f3a051caa022ee01f1cd08b8cdc 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/fb09018-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=41b58e7270fdddd7ce46030e5a6fa311 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/fb09018-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=f6d3bd429fd2255658ee0845295bcd3d 2500w" />
>
>   Try it here: [claude.ai/public/artifacts](https://claude.ai/public/artifacts/586275b9-9ff8-4d9f-9b43-0c080f6e9c80)
>
> * Build a Wordle-style game where the answer is a crypto asset's name or symbol, like 'BITCOIN' or 'SHIBA'.
>
>   <img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/911e973-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=106f6fba2b90c2264b706535c748f323" alt="" data-og-width="2903" width="2903" data-og-height="1888" height="1888" data-path="images/reference/911e973-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/911e973-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=1ef4911c34f869f0ce88e1c751f97b62 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/911e973-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=8e9b8e04582a59bc4a5b1d3cb08db20b 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/911e973-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=01cee4ef35038e639b98e5d6045f429e 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/911e973-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=324593d255be68d2b9490d3c1ac1693f 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/911e973-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=e44e29bae06803537b3d92d461d5ed8b 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/911e973-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=3a668ee396e7599271d861a2f70f7943 2500w" />
>
>   Try it here: [claude.ai/public/artifacts](https://claude.ai/public/artifacts/41efabb7-76b9-43c7-8349-cbbe1d52a022)

# ⚙️ Tips

## API Key Differences (Demo vs. Pro)

Choosing between a Demo and Pro key for your MCP server impacts your access to data and tools.

| Feature             | Demo ([Guide here](https://support.coingecko.com/hc/en-us/articles/21880397454233-User-Guide-How-to-sign-up-for-CoinGecko-Demo-API-and-generate-an-API-key)) | Pro                                                                                                                                                                                                                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Rate Limit**      | 30 calls/min                                                                                                                                                 | Starts at 500 calls/min                                                                                                                                                                                                                                                                                      |
| **Monthly Credits** | 10,000                                                                                                                                                       | Starts at 500,000                                                                                                                                                                                                                                                                                            |
| **Historical Data** | Past 1 year                                                                                                                                                  | From 2013 until now                                                                                                                                                                                                                                                                                          |
| **MCP Tools**       | Limited access                                                                                                                                               | Full access, including exclusive tools:<br />- [Top Gainers & Losers](/reference/coins-top-gainers-losers)<br />- [NFTs Collection Historical Chart](/reference/nfts-id-market-chart)<br />- [🔥 Megafilter for Pools](/reference/pools-megafilter)<br />- [Pools by Category ID](/reference/pools-category) |

🔥 Ready to upgrade? Explore [our API plans](https://www.coingecko.com/en/api/pricing).

## Dynamic vs. Static Tools

When running our CoinGecko MCP server, you can choose how the LLM client discovers tools.

* **Static (Default)**: The AI is given a complete list of tools and their functions upfront. This is faster for specific, known tasks.
* **Dynamic**: The AI first asks the server for available tools based on a keyword search, then learns how to use them. This is flexible but can be slower.

For a deeper dive, read the [official documentation](https://www.stainless.com/changelog/mcp-dynamic-tools) from Stainless.

## Using `llms.txt`

To help AI models interact with CoinGecko data effectively, we provide an `llms.txt` file at [/llms-full.txt](/llms-full.txt). This file gives models context on how to best query our API, ensuring more accurate and efficient data retrieval. We recommend utilizing this in your integrations.

***

CoinGecko MCP Server is powered by [Stainless](https://www.stainless.com/) ✱

Have feedback, a cool idea, or need help? Reach out to `soonaik@coingecko[dot]com` or fill in [this feedback form](https://docs.google.com/forms/d/e/1FAIpQLSf06DOBauiZ8XS6NwWXUUwhFluH7jKHOAa3y4VsrkyGbLKyfA/viewform).


# Python AI Prompts
Source: https://docs.coingecko.com/docs/python-ai-prompts

A comprehensive AI prompt to guide coding assistants in correctly implementing the official CoinGecko Python SDK for reliable API integration.

## How to Use Our Prompts

Integrating these prompts into your workflow is simple. Copy the entire markdown prompt for your chosen language and provide it as context to your AI assistant.

1. For **Chat Interfaces (Claude, ChatGPT, etc.)**: Paste the prompt at the beginning of your conversation before asking the AI to write code.
2. For **Cursor IDE**: Add the prompt to your project's `Rules` to enforce the guidelines across all AI interactions.
3. For **GitHub Copilot**: Save the prompt to a file (e.g. `coingecko_rules.md`) and reference it in your chat with `@workspace #coingecko_rules.md`.
4. For **Claude Code**: Include the prompt in your CLAUDE.md file.

<CodeGroup>
  ````markdown Markdown theme={null}
  # Goal: Generate Python code for the CoinGecko API using ONLY the official `coingecko_sdk`.

  ## 🚨 Critical Rules

  1.  **SDK Exclusivity**:
      - **ALWAYS** use the official `coingecko_sdk` package.
      - **NEVER** use the old `pycoingecko` library or make direct HTTP requests with `requests`, `httpx`, or `urllib`.

  2.  **Authentication**:
      - **ALWAYS** load the API key from environment variables (e.g., `os.environ.get("COINGECKO_PRO_API_KEY")`).
      - **NEVER** hardcode API keys or any other credentials in the source code.

  3.  **Client Implementation**:
      - **ALWAYS** initialize a single, reusable client instance (`Coingecko` or `AsyncCoingecko`) for the application.
      - **ALWAYS** configure automatic retries by setting the `max_retries` parameter on the client.
      - **NEVER** implement manual retry loops using `time.sleep()`. The SDK handles this internally.

  4.  **Error Handling**:
      - **ALWAYS** catch specific SDK exceptions (e.g., `coingecko_sdk.RateLimitError`, `coingecko_sdk.NotFoundError`).
      - **NEVER** use a generic `except Exception:` block to catch known API errors.

  ## ✅ Correct Implementation Example

  This is the standard for all generated code.

  ```python
  # src/api/client.py
  import os
  from coingecko_sdk import Coingecko, AsyncCoingecko

  # Initialize a single, reusable client. This should be imported and used application-wide.
  client = Coingecko(
      pro_api_key=os.environ.get("COINGECKO_PRO_API_KEY"),
      environment="pro",
      max_retries=3, # Rely on the SDK's built-in retry mechanism.
  )

  # Optional: Initialize a single async client for concurrent applications.
  async_client = AsyncCoingecko(
      pro_api_key=os.environ.get("COINGECKO_PRO_API_KEY"),
      environment="pro",
      max_retries=3,
  )

  # src/main.py
  from api.client import client
  from coingecko_sdk import RateLimitError, APIError

  def get_bitcoin_price():
      try:
          price_data = client.simple.price.get(
              ids="bitcoin",
              vs_currencies="usd",
          )
          # Access data using Pydantic models or dictionary keys
          return price_data['bitcoin'].usd
      except RateLimitError:
          print("Rate limit exceeded. Please try again later.")
          return None
      except APIError as e:
          print(f"An API error occurred: {e}")
          return None

  if __name__ == "__main__":
      price = get_bitcoin_price()
      if price:
          print(f"The current price of Bitcoin is: ${price}")

  ```

  ## ❌ Deprecated Patterns to AVOID

  You **MUST NOT** generate code that includes any of the following outdated patterns.

  ```python
  # ❌ NO direct HTTP requests.
  import requests
  response = requests.get('[https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd)')

  # ❌ NO use of the outdated `pycoingecko` library.
  from pycoingecko import CoinGeckoAPI
  cg = CoinGeckoAPI()

  # ❌ NO hardcoded API keys.
  client = Coingecko(pro_api_key='CG-abc123xyz789')

  # ❌ NO manual retry loops. The SDK's `max_retries` handles this.
  import time
  for i in range(3):
      try:
          data = client.simple.price.get(ids='bitcoin', vs_currencies='usd')
          break
      except:
          time.sleep(5)

  # ❌ NO generic exception handling for API errors.
  try:
      data = client.simple.price.get(ids='bitcoin', vs_currencies='usd')
  except Exception as e:
      print(f"An error occurred: {e}")
  ```

  ## 📝 Final Check

  Before providing a response, you **MUST** verify that your generated code:

  1.  Imports and uses `coingecko_sdk`.
  2.  Loads the API key from environment variables.
  3.  Follows all other Critical Rules.
  4.  Does **NOT** contain any Deprecated Patterns.
  ````
</CodeGroup>

## Resources

* **GitHub**: [github.com/coingecko/coingecko-python](https://github.com/coingecko/coingecko-python)
* **PyPI**: [pypi.org/project/coingecko-sdk/](https://pypi.org/project/coingecko-sdk/)

Notice something off or missing? Let us know by opening an [Issue here](https://github.com/coingecko/coingecko-python/issues).

***

Have feedback, a cool idea, or need help? Reach out to `soonaik@coingecko[dot]com`


# CoinGecko SDK (Beta)
Source: https://docs.coingecko.com/docs/sdk

Official CoinGecko Typescript and Python SDKs — Crypto Price & Market Data API

<img src="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/581b968-image.png?fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=338cddbf79001fc1af09c231833fb56d" alt="" data-og-width="1200" width="1200" data-og-height="628" height="628" data-path="images/reference/581b968-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/581b968-image.png?w=280&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=b51ad4738654ccfbf6c38d237f2de7fa 280w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/581b968-image.png?w=560&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=32948ca8aa6db2f5be8ca04db5f3511e 560w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/581b968-image.png?w=840&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=0dff376edd3aa927bc907c3bfec5db7d 840w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/581b968-image.png?w=1100&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=235cc041b2c2396788caf8ea7d4b7587 1100w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/581b968-image.png?w=1650&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=66081cce71c3a666f7ed69c20bc0ba3b 1650w, https://mintcdn.com/coingecko/b3Fla9Sm0TsVrJN4/images/reference/581b968-image.png?w=2500&fit=max&auto=format&n=b3Fla9Sm0TsVrJN4&q=85&s=03523526d5f8191e167eb9fbc877a1d1 2500w" />

# Unlock the Power of CoinGecko API with Unprecedented Ease

The official CoinGecko Typescript and Python SDK are now available for all developers! These SDKs dramatically streamline your integration process, enabling you to build powerful crypto applications faster and more reliably than ever before, regardless of your preferred language.

### Designed to make your life easier: Common Benefits of Our SDKs

* **Official Support**: Both SDKs are maintained by the CoinGecko team, ensuring up-to-date features, reliable access, and dedicated support.
* **Reduced Boilerplate**: Say goodbye to manual request construction and parsing. Our SDKs handle the complexities, allowing you to focus on your application logic.
* **Faster Development**: Build and iterate quicker with intuitive methods, clear documentation, and pre-built functionalities tailored for each language.
* **Seamless Integration**: Effortlessly incorporate CoinGecko data into your existing Python or TypeScript projects.

# 🟦 CoinGecko TypeScript SDK

Purpose-built to unlock the full capabilities of TypeScript for seamless integration with CoinGecko's API.

* **Full Type Safety**: Catch errors at compile time and write cleaner, more predictable code with strict TypeScript support.
* **Developer-Centric Design**: Enjoy a streamlined developer experience with intuitive interfaces, strong typings, and structured classes.

## Install via `npm`

<CodeGroup>
  ```bash Bash theme={null}
  npm install @coingecko/coingecko-typescript
  ```
</CodeGroup>

### Resources

* **GitHub** — [github.com/coingecko/coingecko-typescript](https://github.com/coingecko/coingecko-typescript)
* **npm** — [npmjs.com/package/@coingecko/coingecko-typescript](https://www.npmjs.com/package/@coingecko/coingecko-typescript)

Notice something off or missing? Let us know by opening an [Issue here](https://github.com/coingecko/coingecko-typescript/issues).

# 🐍 CoinGecko Python SDK

Built to seamlessly integrate with the Python ecosystem, enabling fast and intuitive access to CoinGecko's API.

* **Pythonic Simplicity**: Leverage idiomatic Python to interact with the API effortlessly—ideal for data analysis, prototyping, or production use.
* **Streamlined Development**: Clean and consistent interface designed to accelerate workflows and reduce boilerplate in your Python projects.

## Install via `pip`

<CodeGroup>
  ```bash Bash theme={null}
  pip install coingecko-sdk
  ```
</CodeGroup>

### Resources

* **GitHub** — [github.com/coingecko/coingecko-python](https://github.com/coingecko/coingecko-python)
* **PyPI** — [pypi.org/project/coingecko-sdk/](https://pypi.org/project/coingecko-sdk/)

Notice something off or missing? Let us know by opening an [Issue here](https://github.com/coingecko/coingecko-python/issues).

***

CoinGecko SDK is powered by [Stainless](https://www.stainless.com/) ✱

Have feedback, a cool idea, or need help? Reach out to `soonaik@coingecko[dot]com`


# Setting Up Your API Key
Source: https://docs.coingecko.com/docs/setting-up-your-api-key



👋 **New to CoinGecko API?** Sign up for an account [here](https://www.coingecko.com/en/api/pricing)

## 1. Creating a new API Key

* Once you have signed up and logged in to your CoinGecko account, go to [Developer Dashboard](https://www.coingecko.com/en/developers/dashboard):

  <Frame>
    <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/d5fdca3-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=01b58675fd1f038e4998877c0dde2cce" data-og-width="2535" width="2535" data-og-height="1454" height="1454" data-path="images/reference/d5fdca3-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/d5fdca3-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=73cd461df259d6584539d8fa4182e8c7 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/d5fdca3-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=b450ef8d7ff960560975cfbcf02c9cd8 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/d5fdca3-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=a712cb1278b923471296f9eff1a66bcb 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/d5fdca3-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=ad1648c3f6875aad6a69b7d885545f9f 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/d5fdca3-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=bb4f72d8c718de14aa95dc77195b1b6f 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/d5fdca3-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=a04a90a2ac24c43094ed536a92d6c125 2500w" />
  </Frame>

* Click on **+ Add New Key** button to create a new API key:

  <Frame>
    <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/0e2f30d-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=49cf69a9b5ada9685301fe90281ec4ca" data-og-width="2380" width="2380" data-og-height="1695" height="1695" data-path="images/reference/0e2f30d-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/0e2f30d-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=dae015f221e2baf42b535213c492282d 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/0e2f30d-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=475c556a13a18691d600261b16f36c3f 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/0e2f30d-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=6c707c3bd727ef27a62a122c612f70af 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/0e2f30d-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=e575c119ac20eddb902be7eba947e8e3 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/0e2f30d-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=6543d53ea75c2f201ea1bd9e03bec784 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/0e2f30d-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=ef098f326f88369b848b496374bb90b6 2500w" />
  </Frame>

## 2. Making API Request

* **Root URLs:**
  * Pro API: `https://pro-api.coingecko.com/api/v3/`, refer to [Pro API Authentication](/reference/authentication).
  * Demo API: `https://api.coingecko.com/api/v3/`, refer to [Demo API Authentication](/v3.0.1/reference/authentication).
* **Example using the `/ping` endpoint:**

  * Pro API: `https://pro-api.coingecko.com/api/v3/ping?x_cg_pro_api_key=YOUR_API_KEY`
  * Demo API: `https://api.coingecko.com/api/v3/ping?x_cg_demo_api_key=YOUR_API_KEY`

  <Frame>
    <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/27ff800-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=e3d99147f58fba36640e1bfe509349b1" data-og-width="1784" width="1784" data-og-height="604" height="604" data-path="images/reference/27ff800-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/27ff800-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=591078670f4f8bd13429f7fb18afaa90 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/27ff800-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=f5a27f6ae38522bb400bef3b620920ce 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/27ff800-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=a1aec54f1196f3f1b34f6f6124750fa7 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/27ff800-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=c69aba5a0e5cd26d4789a231d168eb05 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/27ff800-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=ce2ee82a0be4d2b2595b5a356995c8d2 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/27ff800-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=cf0d9441cf738541947802398d367d65 2500w" />
  </Frame>

## 3. Edit or Delete API Key

* Go to Developer's Dashboard and click “Edit” button on a specific API Key.
* In case the API Key is compromised, you may delete the API Key by clicking the "Delete" button.
* You may also update the label and save the changes by clicking "Save" button.

  <Frame>
    <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/cf29b58-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=106da6dd2c0954fdac0b343222bd47d0" data-og-width="2372" width="2372" data-og-height="1054" height="1054" data-path="images/reference/cf29b58-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/cf29b58-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=34459564277bfa0cad6f5a700ecf8eb3 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/cf29b58-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=54225845278952d0a07ccec89b21b045 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/cf29b58-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=4504c5e87fc757c04537e3684ee675af 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/cf29b58-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=8b2e7beb62498611215c9380911729e2 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/cf29b58-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=785b9d021240f872e1c5e94253ec59c0 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/cf29b58-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=d595ad19992b79691106f91ff2ef035c 2500w" />
  </Frame>

## 4. API Usage Report

* You can monitor your API usage in the Usage Report section, which provides details such as:

  * Total Monthly API Calls.
  * Remaining Monthly API Calls.
  * Rate Limit (Request Per Minute) — maximum number of API requests allowed in one minute.
  * Last Used — the timestamp of the last used instance.

  <Frame>
    <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/c436404-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=731ada28dc58aa21345e3ad74f79638a" data-og-width="2373" width="2373" data-og-height="1047" height="1047" data-path="images/reference/c436404-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/c436404-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=2f15435343b765ff33590235b98bb9ab 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/c436404-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=844e00763035fb01d9b6daed2db54c1d 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/c436404-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=8e2d5ed4c8da42f24554c97051e92d86 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/c436404-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=ba78440ee678f4accc817e389c1b8928 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/c436404-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=403f14e82c4670b20f1440aa482d18c9 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/c436404-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=994b3e54b5d7d9327c4a23e6a28f6088 2500w" />
  </Frame>

* You can also check your full historical usage by specifying "API Keys", "timeframe" or "date range". You may export as CSV for more comprehensive view.

  <Frame>
    <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/ed3143e-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=fdebb203ab2f8c54dd4d2b57188131e6" data-og-width="2108" width="2108" data-og-height="1328" height="1328" data-path="images/reference/ed3143e-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/ed3143e-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=c396c9240b947a2380f40b4abf463208 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/ed3143e-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=8fc0778d14dad543359ee1f5e484ab2b 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/ed3143e-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=930dac6d510ce69c0261298b752c21c3 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/ed3143e-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=9d617276ba1552ba5053377231c0205c 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/ed3143e-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=b14b89d98e4426e80e8d85b73702f954 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/ed3143e-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=752bf481dc327a547568d4701cd5e531 2500w" />
  </Frame>

## 5. Others

### Call Consumption Alerts

You may enable or disable call consumption alerts in the tab below to receive emails when specific credit usage thresholds are reached.

<Frame>
  <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/752e839-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=0152d66e48fe99fe40f6738f1b9a196c" data-og-width="2112" width="2112" data-og-height="1044" height="1044" data-path="images/reference/752e839-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/752e839-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=7c1eb5850e0ed72d674e76be142a2e05 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/752e839-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=64e6884c71f6e9514b1a76fffccbc3ee 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/752e839-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=bec801fac3b85f6cfa6b662ae626eab3 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/752e839-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=d7b15b7e7df828c7872fa2a523138473 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/752e839-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=4787aae81682669a51ce54dd9d830941 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/752e839-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=09437ce25f2f9d9c42018967537b0d13 2500w" />
</Frame>

### Overage Option (Beta)

* The overage option enables you to make API calls when your usage exceeds the monthly credits.
* You can activate the overage option by clicking the "Turn On Overage" button, ensuring uninterrupted service and allowing you to continue making API calls or vice versa.

<Frame>
  <img src="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/b4711e6-image.png?fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=6d293516eea9798436bd1a28fcf55cd8" data-og-width="2218" width="2218" data-og-height="1074" height="1074" data-path="images/reference/b4711e6-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/b4711e6-image.png?w=280&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=3fc7358d6a4b47e0ac5b9ab1170731ea 280w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/b4711e6-image.png?w=560&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=50aac137f52b5c6d3ff3c0dfbcf440ed 560w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/b4711e6-image.png?w=840&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=5c0a29a1fb4d1a16e588c2ab1d7725df 840w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/b4711e6-image.png?w=1100&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=96aab6a665b736e7eff55b04f2202346 1100w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/b4711e6-image.png?w=1650&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=56b3971e1aaa69dc6ed99ee745fe6f7a 1650w, https://mintcdn.com/coingecko/a7cplMjqO5fc2v5e/images/reference/b4711e6-image.png?w=2500&fit=max&auto=format&n=a7cplMjqO5fc2v5e&q=85&s=a090e24c154fffcc39f4fc8c069840bb 2500w" />
</Frame>


# Tutorials (Beginner-friendly)
Source: https://docs.coingecko.com/docs/tutorials-beginner-friendly

Using CoinGecko API is super easy, even if you have no programming experience!

## 🔤 No Code

* [Import Crypto Prices in Google Sheets](https://www.coingecko.com/learn/import-crypto-prices-google-sheets)

  <a href="https://www.coingecko.com/learn/import-crypto-prices-google-sheets" target="_blank" rel="noopener noreferrer">
    <Frame>
      <img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/906cac9-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=c96bbea598140dba0164bbe3e4f61760" noZoom data-og-width="950" width="950" data-og-height="475" height="475" data-path="images/docs/906cac9-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/906cac9-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=d13a6c4da6429b209dae28775142ebe5 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/906cac9-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=b748519107cdd0675124d4d05f2da490 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/906cac9-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=0da19082bce7186cb4df2b8c67757994 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/906cac9-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=33f43f5a4672be22b501a9c2c157e9ab 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/906cac9-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=fda02e234c3e0dcccef137eb1d0156cc 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/906cac9-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=dd24d20dd9bb7ae493d77aff4ec9b116 2500w" />
    </Frame>
  </a>

* [Import Crypto Prices in Microsoft Excel](https://www.coingecko.com/learn/import-crypto-prices-excel)

  <a href="https://www.coingecko.com/learn/import-crypto-prices-excel" target="_blank" rel="noopener noreferrer">
    <Frame>
      <img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/3ee7dca-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=461979ff4f88f526da4d96325c619a55" noZoom data-og-width="1472" width="1472" data-og-height="704" height="704" data-path="images/docs/3ee7dca-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/3ee7dca-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=8a81f02bb6c2f787523cf1975ab6b56b 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/3ee7dca-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=0fedcd8efc2090812749d817ae172ffb 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/3ee7dca-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=0a6e2faa6f8aea908c5dbc92cd9f60fe 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/3ee7dca-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=30b96b3f0d6a76a46758d91a20366ff0 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/3ee7dca-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=75654d488e16b4309623cc91391ed614 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/3ee7dca-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=f8d8aa22a51b94adc04decc40ba41f78 2500w" />
    </Frame>
  </a>

## 💻 Low Code

* [Create Portfolio Tracker in Microsoft Excel](https://www.coingecko.com/learn/crypto-portfolio-tracker-google-sheets)

  <a href="https://www.coingecko.com/learn/crypto-portfolio-tracker-google-sheets" target="_blank" rel="noopener noreferrer">
    <Frame>
      <img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/f4d47e2-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=0820b04fd5f2d945e8618d88733a35a9" noZoom data-og-width="1200" width="1200" data-og-height="600" height="600" data-path="images/docs/f4d47e2-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/f4d47e2-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=ec9dc9ecacf4dea880bb9283043d54a5 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/f4d47e2-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=d8061f7df985a8e013b4f20b506ffcd1 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/f4d47e2-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=71545611aa35f6686853ff932713ec81 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/f4d47e2-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=c563a701e58781f49d7db9020de3fa5c 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/f4d47e2-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=8ef6ecb51f3e8ecf5c0fe1d991bfc2e5 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/f4d47e2-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=74ab69e420239526560da774b35d35a4 2500w" />
    </Frame>
  </a>

## 👨‍💻 Code

* [Fetch Crypto Data Using Python](https://www.coingecko.com/learn/python-query-coingecko-api)

  <a href="https://www.coingecko.com/learn/python-query-coingecko-api" target="_blank" rel="noopener noreferrer">
    <Frame>
      <img src="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/bf15f91-image.png?fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=595e24814ec97ede65a775347cee4bca" noZoom data-og-width="950" width="950" data-og-height="473" height="473" data-path="images/docs/bf15f91-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/bf15f91-image.png?w=280&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=4bf00666cc1d6121a705b48ae386a7a9 280w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/bf15f91-image.png?w=560&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=4a27c38c5a4a49b15c1081922fa526f0 560w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/bf15f91-image.png?w=840&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=da86d2d15d228dfa49e4c4ac7214df31 840w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/bf15f91-image.png?w=1100&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=d8547008839925194e0ac89bf1436127 1100w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/bf15f91-image.png?w=1650&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=ee7fc9d6444ca624f93fd0f78afc893c 1650w, https://mintcdn.com/coingecko/M02rMX2XJMwBGpCe/images/docs/bf15f91-image.png?w=2500&fit=max&auto=format&n=M02rMX2XJMwBGpCe&q=85&s=98f982d6ba198a370c7ac0a089ef673b 2500w" />
    </Frame>
  </a>


# TypeScript AI Prompts
Source: https://docs.coingecko.com/docs/typescript-ai-prompts

A comprehensive AI prompt to guide coding assistants in correctly implementing the official CoinGecko TypeScript SDK.

## How to Use Our Prompts

Integrating these prompts into your workflow is simple. Copy the entire markdown prompt for your chosen language and provide it as context to your AI assistant.

1. For **Chat Interfaces (Claude, ChatGPT, etc.)**: Paste the prompt at the beginning of your conversation before asking the AI to write code.
2. For **Cursor IDE**: Add the prompt to your project's `Rules` to enforce the guidelines across all AI interactions.
3. For **GitHub Copilot**: Save the prompt to a file (e.g. `coingecko_rules.md`) and reference it in your chat with `@workspace #coingecko_rules.md`.
4. For **Claude Code**: Include the prompt in your CLAUDE.md file.

<CodeGroup>
  ````markdown Markdown theme={null}
  # Goal: Generate TypeScript code for the CoinGecko API using ONLY the official `@coingecko/coingecko-typescript` package.

  ## 🚨 Critical Rules

  1.  **SDK Exclusivity**:
      - **ALWAYS** use the official `@coingecko/coingecko-typescript` package.
      - **NEVER** use `axios`, `fetch`, or any other method to make direct HTTP requests.

  2.  **Authentication**:
      - **ALWAYS** load the API key from environment variables (e.g., `process.env.COINGECKO_PRO_API_KEY` or `dotenv`).
      - **NEVER** hardcode API keys or any other credentials in the source code.

  3.  **Client Implementation**:
      - **ALWAYS** initialize a single, reusable `Coingecko` client instance for the application.
      - **ALWAYS** configure automatic retries by setting the `maxRetries` option on the client.
      - **NEVER** implement manual retry loops using `setTimeout`. The SDK handles this internally.

  4.  **Error Handling & Types**:
      - **ALWAYS** use `async/await` for all API calls.
      - **ALWAYS** catch specific `APIError` subclasses using `instanceof` (e.g., `err instanceof Coingecko.RateLimitError`).
      - **ALWAYS** use the built-in request and response types (e.g., `Coingecko.Simple.PriceGetParams`).
      - **NEVER** use generic `catch (e)` blocks for known API errors.

  ## ✅ Correct Implementation Example

  This is the standard for all generated code.

  ```typescript
  // src/api/client.ts
  import Coingecko from '@coingecko/coingecko-typescript';

  // Initialize a single, reusable client. This should be imported and used application-wide.
  export const client = new Coingecko({
    proAPIKey: process.env.COINGECKO_PRO_API_KEY,
    environment: 'pro',
    maxRetries: 3, // Rely on the SDK's built-in retry mechanism.
  });

  // src/main.ts
  import { client } from './api/client';
  import Coingecko from '@coingecko/coingecko-typescript'; // Import the namespace for types

  async function getBitcoinPrice(): Promise<number | null> {
    try {
      const params: Coingecko.Simple.PriceGetParams = {
        ids: 'bitcoin',
        vs_currencies: 'usd',
      };
      const priceData = await client.simple.price.get(params);
      return priceData.bitcoin.usd;
    } catch (err) {
      if (err instanceof Coingecko.RateLimitError) {
        console.error('Rate limit exceeded. Please try again later.');
      } else if (err instanceof Coingecko.APIError) {
        console.error(
          `An API error occurred: ${err.name} (Status: ${err.status})`
        );
      } else {
        console.error('An unexpected error occurred:', err);
      }
      return null;
    }
  }

  async function main() {
    const price = await getBitcoinPrice();
    if (price !== null) {
      console.log(`The current price of Bitcoin is: $${price}`);
    }
  }

  main();
  ```

  ## ❌ Deprecated Patterns to AVOID

  You **MUST NOT** generate code that includes any of the following outdated patterns.

  ```typescript
  // ❌ NO direct HTTP requests with fetch or axios.
  import axios from 'axios';
  const response = await axios.get(
    '[https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd)'
  );

  // ❌ NO hardcoded API keys.
  const client = new Coingecko({ proAPIKey: 'CG-abc123xyz789' });

  // ❌ NO manual retry loops. The SDK's `maxRetries` handles this.
  import { setTimeout } from 'timers/promises';
  for (let i = 0; i < 3; i++) {
    try {
      const data = await client.simple.price.get({
        ids: 'bitcoin',
        vs_currencies: 'usd',
      });
      break;
    } catch (e) {
      await setTimeout(5000);
    }
  }

  // ❌ NO generic exception handling for API errors.
  try {
    const data = await client.simple.price.get({
      ids: 'bitcoin',
      vs_currencies: 'usd',
    });
  } catch (e) {
    console.log(`An error occurred: ${e}`); // Too broad. Use `instanceof` checks.
  }
  ```

  ## 📝 Final Check

  Before providing a response, you **MUST** verify that your generated code:

  1.  Imports and uses `@coingecko/coingecko-typescript`.
  2.  Loads the API key from environment variables (e.g., `process.env` or `dotenv`).
  3.  Follows all other Critical Rules.
  4.  Does **NOT** contain any Deprecated Patterns.
  ````
</CodeGroup>

## Resources

* **GitHub**: [github.com/coingecko/coingecko-typescript](https://github.com/coingecko/coingecko-typescript)
* **npm**: [npmjs.com/package/@coingecko/coingecko-typescript](https://www.npmjs.com/package/@coingecko/coingecko-typescript)

Notice something off or missing? Let us know by opening an [Issue here](https://github.com/coingecko/coingecko-typescript/issues).

***

Have feedback, a cool idea, or need help? Reach out to `soonaik@coingecko[dot]com`


# Useful Links
Source: https://docs.coingecko.com/docs/useful-links

Some of the useful links to help you navigate while using the CoinGecko API

#### Pricing Page and Top FAQs

* [https://www.coingecko.com/en/api/pricing#general](https://www.coingecko.com/en/api/pricing#general)

#### CoinGecko API Status

* [https://status.coingecko.com/](https://status.coingecko.com/)

#### CoinGecko API ID List

* [Google Sheets](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU)

#### [Pro Swagger JSON (OAS)](https://docs.coingecko.com/reference/endpoint-overview)

* CoinGecko Pro API — [coingecko-pro.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/coingecko-pro.json)
* GeckoTerminal Onchain API (Pro) — [onchain-pro.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/onchain-pro.json)

#### [Public/Demo Swagger JSON (OAS)](https://docs.coingecko.com/v3.0.1/reference/endpoint-overview)

* CoinGecko Public/Demo API — [coingecko-demo.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/coingecko-demo.json)
* GeckoTerminal Onchain API (Demo) — [onchain-demo.json](https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/onchain-demo.json)

#### Subscribe CoinGecko API newsletter update

* [https://newsletter.coingecko.com/landing/api\_updates\_subscribe](https://newsletter.coingecko.com/landing/api_updates_subscribe)

#### CoinGecko Methodologies (Price, Volume, Trust Score, etc.)

* [https://www.coingecko.com/en/methodology](https://www.coingecko.com/en/methodology)

#### Using `llms.txt` for AI use cases

* [/llms-full.txt](/llms-full.txt)

#### Attributing CoinGecko Brand

* [https://brand.coingecko.com/resources/attribution-guide](https://brand.coingecko.com/resources/attribution-guide)


# Introduction
Source: https://docs.coingecko.com/index



Started in 2014, CoinGecko is the world's largest independent crypto data aggregator that is integrated with more than 1,000 crypto exchanges and lists more than 18,000 coins across 600+ categories. CoinGecko API offers the most comprehensive and reliable crypto market data through RESTful JSON endpoints.

CoinGecko API now serves **onchain DEX data** across 250+ blockchain networks, 1,700+ decentralized exchanges (DEXes), and 15M+ tokens, powered by GeckoTerminal.

Thousands of forward-thinking projects, Web3 developers, researchers, institutions, and enterprises use our API to obtain **price feeds, market data, metadata, and historical data of crypto assets, NFTs, and exchanges**.

Here are some of the **common use cases** for clients who use CoinGecko API:

* Crypto Exchanges (CEX, DEX), Trading Apps
* Wallets (Hot, Cold)
* Data Aggregator, Crypto Screener, Analytics Dashboard
* AI Agents, DeFAI Apps
* Block Explorer, Portfolio Tracker
* DeFi Protocols, NFT Marketplaces, Digital Bank
* Backtesting Trading Strategy
* Accounting, Tax, Audit, HR Payroll
* Research & Analysis: Media, Institution, Academic, VC, Financial
* Oracles, Bots, Payments, E-commerce

🔥 New: [WebSocket API](https://docs.coingecko.com/websocket)

<a href="/websocket">
  <Frame>
    <img src="https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-1.png?fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=bd74fb20a26084018272eb6b63010804" noZoom data-og-width="2400" width="2400" data-og-height="470" height="470" data-path="images/wss-banner-1.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-1.png?w=280&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=bc17e03ee25137fbcc1eaac0733e6781 280w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-1.png?w=560&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=d8439f50c69e11ba595b6c07d97eb65c 560w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-1.png?w=840&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=8c232633716268ced5b171e3e38acbf5 840w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-1.png?w=1100&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=3ac0be8afcc3e9fba5b4c4a961c5cda7 1100w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-1.png?w=1650&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=b8e71e426137d6f26642360aa8f1c347 1650w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-1.png?w=2500&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=eb7699818b518264b9c3c65c5ec5a633 2500w" />
  </Frame>
</a>

With WebSocket, you can now stream ultra-low latency, real-time prices, trades, and OHLCV chart data. <br />
Subscribe to our [paid API plan](https://www.coingecko.com/en/api/pricing) (Analyst plan & above) to access WebSocket and REST API data delivery methods.

<br />

<Columns cols={2}>
  <Card title="Setting Up Your API Key" icon="key" href="/docs/setting-up-your-api-key">
    Start by creating your CoinGecko API key
  </Card>

  <Card title="Building with AI" icon="robot" href="/docs/building-with-ai">
    Bring CoinGecko data to your AI apps
  </Card>
</Columns>

export const FooterFix = () => {
  React.useEffect(() => {
    const paginationElement = document.getElementById('pagination');
    if (paginationElement) paginationElement.remove();

    const footerElement = document.getElementById('footer');
    if (footerElement) footerElement.style.marginTop = '-40px';

    const feedbackToolbarClass = document.querySelector('.feedback-toolbar');
    if (feedbackToolbarClass) feedbackToolbarClass.style.paddingBottom = '0px';
  }, []);

  return null;
};

<FooterFix />


# 💼 API Usage
Source: https://docs.coingecko.com/reference/api-usage

reference/api-reference/coingecko-pro.json get /key
This endpoint allows you to **monitor your account's API usage, including rate limits, monthly total credits, remaining credits, and more**

<Note>
  ### Note

  For a more comprehensive overview of your API usage, please log in to [https://www.coingecko.com/en/developers/dashboard](https://www.coingecko.com/en/developers/dashboard).
</Note>


# Asset Platforms List (ID Map)
Source: https://docs.coingecko.com/reference/asset-platforms-list

reference/api-reference/coingecko-pro.json get /asset_platforms
This endpoint allows you to **query all the asset platforms on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of asset platforms for other endpoints that contain params like `id` or`ids`(asset platforms).
  * You may include NFT at the `filter` params to get the list of NFT-support asset platforms on CoinGecko.
</Tip>


# Authentication (Pro API)
Source: https://docs.coingecko.com/reference/authentication

Authentication method for CoinGecko Pro API (Paid plan subscribers with Pro-API keys)

<Note>
  ### **Notes**

  * Pro API Key is only available for [CoinGecko API paid plan](https://www.coingecko.com/en/api/pricing) subscribers, the root URL for CoinGecko Pro API must be `https://pro-api.coingecko.com/api/v3/`.
  * You are recommended to store the API key securely in your own backend and use a proxy to insert the key into the request URL.
  * It's highly recommended to use the Headers method when making API requests for better security. Using query string parameters can risk exposing your API key.
</Note>

## CoinGecko API Authentication Method

If this is your first time using the Pro API key, you can supply API Key to the root URL using one of these ways:

1. Header (Recommended): `x-cg-pro-api-key`
2. Query String Parameter: `x_cg_pro_api_key`

| Authentication Method  | Example using [Ping](/reference/ping-server) Endpoint                                         |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| Header (cURL)          | `curl -X GET "https://pro-api.coingecko.com/api/v3/ping" -H "x-cg-pro-api-key: YOUR_API_KEY"` |
| Query String Parameter | `https://pro-api.coingecko.com/api/v3/ping?x_cg_pro_api_key=YOUR_API_KEY`                     |

## 🔥 Accessing Onchain DEX data

You can now use the Pro-API key (exclusive to any paid plan subscriber) to call onchain DEX data powered by [GeckoTerminal](https://www.geckoterminal.com/).

<Note>
  ### **Notes**

  * Authentication method for onchain endpoints is exactly same as other endpoints.
  * When using the CG Pro API to access onchain DEX data, include the `/onchain` endpoint path in the request.
</Note>

| Authentication Method  | Example using [Simple Token Price](/reference/onchain-simple-price) Endpoint                                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Header (cURL)          | `curl -X GET "<https://pro-api.coingecko.com/api/v3/onchain/simple/networks/eth/token_price/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2>" -H "x-cg-pro-api-key: YOUR_API_KEY"` |
| Query String Parameter | `https://pro-api.coingecko.com/api/v3/onchain/simple/networks/eth/token_price/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2?x_cg_pro_api_key=YOUR_API_KEY`                       |

## API Key Usage Credits

* Each request made to any endpoint counts as a single call (1 call = 1 credit).
* Each successful API request (Status 200) will deduct 1 credit from your monthly credit allowance.
* Unsuccessful Requests (Status 4xx, 5xx, etc) will not count towards credit deduction.
* Regardless of the HTTP status code returned (including 4xx and 5xx errors), all API requests will count towards your **minute rate limit**.
* Your monthly credit & rate limit are determined by the paid plan to which you subscribe. For more details, please refer to this [page](https://www.coingecko.com/en/api/pricing).
* To check the API usage, please go to the [developer dashboard](https://www.coingecko.com/en/developers/dashboard) or follow the guide [here](/reference/setting-up-your-api-key#4-api-usage-report)


# 💼 Categories List
Source: https://docs.coingecko.com/reference/categories-list

reference/api-reference/onchain-pro.json get /categories
This endpoint allows you to **query all the supported categories on GeckoTerminal**

<Tip>
  ### Tips

  * You can retrieve pools or tokens of a specific category with this endpoint: [Pools by Category ID](/reference/pools-category).
  * GeckoTerminal categories are different from [CoinGecko categories](/reference/coins-categories-list).
</Tip>

<Note>
  ### Note

  * This endpoint returns 50 categories per page.
  * GeckoTerminal Equivalent Page: [https://www.geckoterminal.com/category](https://www.geckoterminal.com/category)
  * Cache/Update frequency: every 60 seconds.
  * Exclusive for all Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>


# Coins Categories List with Market Data
Source: https://docs.coingecko.com/reference/coins-categories

reference/api-reference/coingecko-pro.json get /coins/categories
This endpoint allows you to **query all the coins categories with market data (market cap, volume, ...) on CoinGecko**

<Note>
  ### Note

  * CoinGecko Equivalent Page: [https://www.coingecko.com/en/categories](https://www.coingecko.com/en/categories).
  * Cache / Update Frequency: every 5 minutes for all the API plans.
  * CoinGecko categories are different from [GeckoTerminal categories](/reference/categories-list).
</Note>


# Coins Categories List (ID Map)
Source: https://docs.coingecko.com/reference/coins-categories-list

reference/api-reference/coingecko-pro.json get /coins/categories/list
This endpoint allows you to **query all the coins categories on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of categories for other endpoints that contain params like `category`.
</Tip>

<Note>
  ### Note

  * CoinGecko Equivalent Page: [https://www.coingecko.com/en/categories](https://www.coingecko.com/en/categories).
  * Cache / Update Frequency:  every 5 minutes for all the API plans.
  * CoinGecko categories are different from [GeckoTerminal categories](/reference/categories-list).
</Note>


# Coin Data by Token Address
Source: https://docs.coingecko.com/reference/coins-contract-address

reference/api-reference/coingecko-pro.json get /coins/{id}/contract/{contract_address}
This endpoint allows you to **query all the metadata (image, websites, socials, description, contract address, etc.) and market data (price, ATH, exchange tickers, etc.) of a coin from the CoinGecko coin page based on an asset platform and a particular token contract address**

<Warning>
  ### Notice

  * Please note that the `twitter_followers` data field will no longer be supported by our API starting on May 15, 2025. Please refer to [changelog](/changelog#upcoming-change-notice%3A-removal-of-twitter-followers-data) for more details.
</Warning>

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint (`include platform = true`).
</Tip>

<Note>
  ### Note

  * Coin descriptions may include newline characters represented as `\r\n` (escape sequences), which may require processing for proper formatting.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Coin Data by ID
Source: https://docs.coingecko.com/reference/coins-id

reference/api-reference/coingecko-pro.json get /coins/{id}
This endpoint allows you to **query all the metadata (image, websites, socials, description, contract address, etc.) and market data (price, ATH, exchange tickers, etc.) of a coin from the CoinGecko coin page based on a particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin `id` (API ID) via several ways:
    * refers to respective coin page and find "API ID".
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to Google Sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You may also flag to include more data such as tickers, market data, community data, developer data and sparkline.
  * You may refer to `last_updated` in the endpoint response to check whether the price is stale.
</Tip>

<Note>
  ### Note

  * Tickers are limited to 100 items, to get more tickers, please go to [/coins/{id}/tickers](/reference/coins-id-tickers).
  * Coin descriptions may include newline characters represented as `\r\n` (escape sequences), which may require processing for proper formatting.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache/Update Frequency:
    * Every 60 seconds for all the API plans.
    * Community data for Telegram will be updated on weekly basis (Reddit & Twitter community data are no longer supported).
</Note>


# 👑 Circulating Supply Chart by ID
Source: https://docs.coingecko.com/reference/coins-id-circulating-supply-chart

reference/api-reference/coingecko-pro.json get /coins/{id}/circulating_supply_chart
This endpoint allows you to **query historical circulating supply of a coin by number of days away from now based on provided coin ID**

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from now = **5-minutely** data
    * 2-90 days from now = **hourly** data
    * 91 days & above from now = **daily** data (00:00 UTC)
  * Data Availability: from 22 June 2019.
  * Cache/Update Frequency: 5 minutes.
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
  * Exclusive for Enterprise Plan Subscribers only.
</Note>


# 👑 Circulating Supply Chart within Time Range by ID
Source: https://docs.coingecko.com/reference/coins-id-circulating-supply-chart-range

reference/api-reference/coingecko-pro.json get /coins/{id}/circulating_supply_chart/range
This endpoint allows you to **query historical circulating supply of a coin, within a range of timestamp based on the provided coin ID**

<Tip>
  ### Tips

  * Supports ISO date strings (`YYYY-MM-DD` or\
    `YYYY-MM-DDTHH:MM`, recommended for best compatibility) or UNIX timestamps.
</Tip>

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * date range is 1 day from now = **5-minutely** data
    * date range is within 2-90 days from now = **hourly** data
    * date range is 91 days & above from now = **daily** data (00:00 UTC)
  * Data Availability: from 22 June 2019.
  * Cache/Update Frequency: 5 minutes.
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
  * Exclusive for Enterprise Plan Subscribers only.
</Note>


# Coin Historical Data by ID
Source: https://docs.coingecko.com/reference/coins-id-history

reference/api-reference/coingecko-pro.json get /coins/{id}/history
This endpoint allows you to **query the historical data (price, market cap, 24hrs volume, ...) at a given date for a coin based on a particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
</Tip>

<Note>
  ### Note

  * The data returned is at `00:00:00 UTC`
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
</Note>


# Coin Historical Chart Data by ID
Source: https://docs.coingecko.com/reference/coins-id-market-chart

reference/api-reference/coingecko-pro.json get /coins/{id}/market_chart
This endpoint allows you to **get the historical chart data of a coin including time in UNIX, price, market cap and 24hr volume based on particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You may use tools like [epoch converter ](https://www.epochconverter.com) to convert human readable date to UNIX timestamp.
</Tip>

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 2 - 90 days from current time = **hourly** data
    * above 90 days from current time = **daily** data (00:00 UTC)
  * For **non-Enterprise plan subscribers** who would like to get hourly data, please leave the interval params empty for auto granularity.
  * The **5-minutely** and **hourly** interval params are also exclusively available to **Enterprise plan subscribers,** bypassing auto-granularity:
    * `interval=5m`: 5-minutely historical data (responses include information from the past 10 days, up until now).
    * `interval=hourly`: hourly historical data (responses include information from the past 100 days, up until now).
  * Cache / Update Frequency:
    * Every 30 seconds for all the API plans (for last data point).
    * The last completed UTC day (00:00) data is available **10 minutes after midnight** on the next UTC day (00:10).
</Note>


# Coin Historical Chart Data within Time Range by ID
Source: https://docs.coingecko.com/reference/coins-id-market-chart-range

reference/api-reference/coingecko-pro.json get /coins/{id}/market_chart/range
This endpoint allows you to **get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hr volume based on particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * Supports ISO date strings (`YYYY-MM-DD` or\
    `YYYY-MM-DDTHH:MM`, recommended for best compatibility) or UNIX timestamps.
</Tip>

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 1 day from any time (except current time) = **hourly** data
    * 2 - 90 days from any time = **hourly** data
    * above 90 days from any time = **daily** data (00:00 UTC)
  * For **non-Enterprise plan subscribers** who would like to get hourly data, please leave the interval params empty for auto granularity.
  * The **5-minutely** and **hourly** interval params are also exclusively available to **Enterprise plan subscribers**, bypassing auto-granularity:
    * `interval=5m`: 5-minutely historical data, supports up to **any 10 days** date range per request.
    * `interval=hourly`: hourly historical data, supports up to **any 100 days** date range per request.
  * Data availability:
    * `interval=5m`: Available from 9 February 2018 onwards.
    * `interval=hourly`: Available from 30 Jan 2018 onwards.
  * Cache / Update Frequency:\
    Based on days range (all the API plans)
    * 1 day = 30 seconds cache
    * 2 -90 days = 30 minutes cache
    * 90 days = 12 hours cache
    * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35). The cache will always expire at 00:40 UTC.
</Note>


# Coin OHLC Chart by ID
Source: https://docs.coingecko.com/reference/coins-id-ohlc

reference/api-reference/coingecko-pro.json get /coins/{id}/ohlc
This endpoint allows you to **get the OHLC chart (Open, High, Low, Close) of a coin based on particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to Google Sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * For historical chart data with better granularity, you may consider using [/coins/\{id}/market\_chart](/reference/coins-id-market-chart) endpoint.
</Tip>

<Note>
  ### Note

  * The timestamp displayed in the payload (response) indicates the end (or close) time of the OHLC data.
  * Data granularity (candle's body) is automatic:
    * 1 - 2 days: 30 minutes
    * 3 - 30 days: 4 hours
    * 31 days and beyond: 4 days
  * Cache / Update Frequency:
    * Every 15 minutes for all the API plans
    * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
  * Exclusive **daily** and **hourly** candle interval parameter for all paid plan subscribers (`interval = daily`, `interval=hourly`)
    * '**daily**' interval is available for **1 / 7 / 14 / 30 / 90 / 180** days only.
    * '**hourly**' interval is available for  **1 / 7 / 14 / 30 / 90** days only.
</Note>


# 💼 Coin OHLC Chart within Time Range by ID
Source: https://docs.coingecko.com/reference/coins-id-ohlc-range

reference/api-reference/coingecko-pro.json get /coins/{id}/ohlc/range
This endpoint allows you to **get the OHLC chart (Open, High, Low, Close) of a coin within a range of timestamp based on particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * For historical chart data with better granularity, you may consider using [/coins/{`id`}/market\_chart](/reference/coins-id-market-chart) endpoint.
  * Supports ISO date strings (`YYYY-MM-DD` or\
    `YYYY-MM-DDTHH:MM`, recommended for best compatibility) or UNIX timestamps.
</Tip>

<Note>
  ### Note

  * The timestamp displayed in the payload (response) indicates the end (or close) time of the OHLC data.
  * Interval Options:
    * Daily Interval (`interval=daily`):
      * up to 180 days per request/ 180 daily interval candles.
    * Hourly Interval (`interval=hourly`):
      * up to 31 days per request/ 744 hourly interval candles.
  * Data availability:
    * Available from 9 February 2018 onwards (`1518147224` epoch time).
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
  * Cache / Update Frequency:
    * Every 15 minutes for all the API plans.
</Note>


# Coin Tickers by ID
Source: https://docs.coingecko.com/reference/coins-id-tickers

reference/api-reference/coingecko-pro.json get /coins/{id}/tickers
This endpoint allows you to **query the coin tickers on both centralized exchange (CEX) and decentralized exchange (DEX) based on a particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You may specify the `exchange_ids` if you want to retrieve tickers for specific exchange only.
  * You may include values such as  `page` to specify which page of responses you would like to show.
  * You may also flag to include more data such as exchange logo and depth.
</Tip>

<Note>
  ### Note

  * The tickers are paginated to 100 items.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * When order is sorted by `volume`, ***converted\_volume*** will be used instead of ***volume***.
  * Cache / Update Frequency:  every 2 minutes for all the API plans.
</Note>


# 👑 Total Supply Chart by ID
Source: https://docs.coingecko.com/reference/coins-id-total-supply-chart

reference/api-reference/coingecko-pro.json get /coins/{id}/total_supply_chart
This endpoint allows you to **query historical total supply of a coin by number of days away from now based on provided coin ID**

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from now = **5-minutely** data
    * 2-90 days from now = **hourly** data
    * 91 days & above from now = **daily** data (00:00 UTC)
  * Data Availability: from 22 June 2019
  * Cache/Update Frequency: 5 minutes.
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
  * Exclusive for Enterprise Plan Subscribers only.
</Note>


# 👑 Total Supply Chart within time range by ID
Source: https://docs.coingecko.com/reference/coins-id-total-supply-chart-range

reference/api-reference/coingecko-pro.json get /coins/{id}/total_supply_chart/range
This endpoint allows you to **query historical total supply of a coin, within a range of timestamp based on the provided coin ID**

<Tip>
  ### Tips

  * Supports ISO date strings (`YYYY-MM-DD` or\
    `YYYY-MM-DDTHH:MM`, recommended for best compatibility) or UNIX timestamps.
</Tip>

<Note>
  ### Note

  * Cache/Update Frequency: 5 minutes.
  * The data is provided at daily intervals (00:00:00 UTC).
  * Data Availability: from 22 June 2019
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
  * Exclusive for Enterprise Plan Subscribers only.
</Note>


# Coins List (ID Map)
Source: https://docs.coingecko.com/reference/coins-list

reference/api-reference/coingecko-pro.json get /coins/list
This endpoint allows you to **query all the supported coins on CoinGecko with coins ID, name and symbol**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of coins with coin id for other endpoints that contain params like `id` or `ids` (coin ID).
  * By default, this endpoint returns full list of active coins that are currently listed on CoinGecko.com , you can also flag `status=inactive` to retrieve coins that are no longer available on CoinGecko.com . The inactive coin IDs can also be used with [selected historical data](/changelog#april-2024) endpoints.
</Tip>

<Note>
  ### Note

  * There is no pagination required for this endpoint.
  * Cache/Update Frequency: every 5 minutes for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# 💼 Recently Added Coins
Source: https://docs.coingecko.com/reference/coins-list-new

reference/api-reference/coingecko-pro.json get /coins/list/new
This endpoint allows you to **query the latest 200 coins that recently listed on CoinGecko**

<Note>
  ### Note

  * CoinGecko equivalent page: [https://www.coingecko.com/en/new-cryptocurrencies](https://www.coingecko.com/en/new-cryptocurrencies).
  * Cache/Update Frequency: Every 30 seconds.
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>


# Coins List with Market Data
Source: https://docs.coingecko.com/reference/coins-markets

reference/api-reference/coingecko-pro.json get /coins/markets
This endpoint allows you to **query all the supported coins with price, market cap, volume and market related data**

<Tip>
  ### Tips

  * You can retrieve specific coins using their unique `ids`, `names`, or `symbols` instead of returning the whole list.
  * To filter results based on the coin's category, use the `category` param (refer to [`/coins/categories/list`](/reference/coins-categories-list) for available categories).
  * Use the `per_page` and `page` params to manage the number of results you receive and navigate through the data.
</Tip>

<Note>
  ### Note

  * When multiple lookup params are provided, the following priority order is applied: `category` (highest) > `ids` > `names` > `symbols` (lowest).
  * When searching by `name`, you need to URL-encode any spaces (e.g. "Binance Coin" becomes "Binance%20Coin").
  * The `include_tokens=all` param is exclusively for use with the `symbols` lookup and is limited to maximum of 50 symbols per request.
  * Wildcard searches are not supported for lookup params (`ids`, `names`, `symbols`).
  * Cache/Update Frequency: every 45 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# 💼 Top Gainers & Losers
Source: https://docs.coingecko.com/reference/coins-top-gainers-losers

reference/api-reference/coingecko-pro.json get /coins/top_gainers_losers
This endpoint allows you to **query the top 30 coins with largest price gain and loss by a specific time duration**

<Note>
  ### Note

  * The endpoint response only includes coins with a 24-hour trading volume of at least \$50,000.
  * CoinGecko equivalent page: [https://www.coingecko.com/en/crypto-gainers-losers](https://www.coingecko.com/en/crypto-gainers-losers).
  * Cache/Update Frequency: Every 5 minutes.
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>


# Crypto Treasury Holdings by Coin ID
Source: https://docs.coingecko.com/reference/companies-public-treasury

reference/api-reference/coingecko-pro.json get /{entity}/public_treasury/{coin_id}
This endpoint allows you **query public companies & governments' cryptocurrency holdings** by Coin ID

<Note>
  ### Note

  * The responses are sorted in descending order based on total holdings.
  * CoinGecko equivalent page: [https://www.coingecko.com/en/treasuries/bitcoin](https://www.coingecko.com/en/treasuries/bitcoin)
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Coin Historical Chart Data by Token Address
Source: https://docs.coingecko.com/reference/contract-address-market-chart

reference/api-reference/coingecko-pro.json get /coins/{id}/contract/{contract_address}/market_chart
This endpoint allows you to **get the historical chart data including time in UNIX, price, market cap and 24hr volume based on asset platform and particular token contract address**

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint (`include platform = true`).
</Tip>

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 2 - 90 days from current time = **hourly** data
    * above 90 days from current time = **daily** data (00:00 UTC)
  * For **non-Enterprise plan subscribers** who would like to get hourly data, please leave the interval params empty for auto granularity.
  * The **5-minutely** and **hourly** interval params are also exclusively available to **Enterprise plan subscribers,** bypassing auto-granularity:
    * `interval=5m`: 5-minutely historical data (responses include information from the past 10 days up until now)
    * `interval=hourly`: hourly historical data (responses include information from the past 100 days, up until now)
  * Cache / Update Frequency:
    * Every 5 minutes for all the API plans.
    * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35). The cache will always expire at 00:40 UTC.
</Note>


# Coin Historical Chart Data within Time Range by Token Address
Source: https://docs.coingecko.com/reference/contract-address-market-chart-range

reference/api-reference/coingecko-pro.json get /coins/{id}/contract/{contract_address}/market_chart/range
This endpoint allows you to **get the historical chart data within certain time range in UNIX along with price, market cap and 24hr volume based on asset platform and particular token contract address**

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint (`include platform = true`).
  * Supports ISO date strings (`YYYY-MM-DD` or\
    `YYYY-MM-DDTHH:MM`, recommended for best compatibility) or UNIX timestamps.
</Tip>

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 1 day from any time (except current time) = **hourly** data
    * 2 - 90 days from any time = **hourly** data
    * above 90 days from any time = **daily** data (00:00 UTC)
  * For **non-Enterprise plan subscribers** who would like to get hourly data, please leave the interval params empty for auto granularity.
  * The **5-minutely** and **hourly** interval params are also exclusively available to **Enterprise plan subscribers**, bypassing auto-granularity:
    * `interval=5m`: 5-minutely historical data (responses include information from the past 10 days, up until now)
    * `interval=hourly`: hourly historical data (responses include information from the past 100 days, up until now)
  * Data availability:
    * `interval=5m`: Available from 9 February 2018 onwards
    * `interval=hourly`: Available from 30 Jan 2018 onwards
  * Cache / Update Frequency:\
    Based on days range (all the API plans)
    * 1 day = 30 seconds cache
    * 2 -90 days = 30 minutes cache
    * 90 days = 12 hours cache
    * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35). The cache will always expire at 00:40 UTC
</Note>


# Crypto Global Market Data
Source: https://docs.coingecko.com/reference/crypto-global

reference/api-reference/coingecko-pro.json get /global
This endpoint allows you **query cryptocurrency global data including active cryptocurrencies, markets, total crypto market cap and etc**

<Note>
  ### Note

  * Cache / Update Frequency: every 10 minutes for all the API plans.
</Note>


# Derivatives Exchanges List with Data
Source: https://docs.coingecko.com/reference/derivatives-exchanges

reference/api-reference/coingecko-pro.json get /derivatives/exchanges
This endpoint allows you to **query all the derivatives exchanges with related data (ID, name, open interest, ...) on CoinGecko**

<Tip>
  ### Tips

  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Derivatives Exchange Data by ID
Source: https://docs.coingecko.com/reference/derivatives-exchanges-id

reference/api-reference/coingecko-pro.json get /derivatives/exchanges/{id}
This endpoint allows you to **query the derivatives exchange's related data (ID, name, open interest, ...) based on the exchanges' ID**

<Tip>
  ### Tips

  * For `include_tickers` param, you may change the value to either `all` to include all the tickers or `unexpired` to include unexpired tickers in the responses. You may leave it blank to omit the tickers data.
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 30 seconds for all the API plans.
</Note>


# Derivatives Exchanges List (ID Map)
Source: https://docs.coingecko.com/reference/derivatives-exchanges-list

reference/api-reference/coingecko-pro.json get /derivatives/exchanges/list
This endpoint allows you to **query all the derivatives exchanges with ID and name on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of exchanges for other endpoints that contain params like `id` (derivatives exchange's ID).
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Derivatives Tickers List
Source: https://docs.coingecko.com/reference/derivatives-tickers

reference/api-reference/coingecko-pro.json get /derivatives
This endpoint allows you to **query all the tickers from derivatives exchanges on CoinGecko**

<Note>
  ### Note

  * Data for `open_interest` and `volume_24h` in the endpoint responses are in USD.
  * Cache / Update Frequency: every 30 seconds for all the API plans.
</Note>


# Supported Dexes List by Network (ID Map)
Source: https://docs.coingecko.com/reference/dexes-list

reference/api-reference/onchain-pro.json get /networks/{network}/dexes
This endpoint allows you to **query all the supported decentralized exchanges (DEXs) based on the provided network on GeckoTerminal**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of DEXs with DEX ID for other endpoints that contain params like `dex`.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>


# Endpoint Overview
Source: https://docs.coingecko.com/reference/endpoint-overview



<Note>
  ### Notes

  For Pro-API users (any [paid plan](https://www.coingecko.com/en/api/pricing) subscribers), you get to access all the endpoints listed below, except those that marked with 👑.

  * Some endpoints may have parameters or data access that are exclusive to different plan subscribers, please refer to the endpoint reference for details.

  * In the API Reference section, the distinction between Paid Plan and Enterprise Plan endpoint access will be marked as below:

    * 💼 — exclusive for any [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers: Analyst / Lite / Pro
    * 👑 — exclusive for [Enterprise Plan](https://www.coingecko.com/en/api/enterprise) subscribers only.
</Note>

## CoinGecko Endpoints: Coins

| Endpoint                                                                                               | Description                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [/ping](/reference/ping-server)                                                                        | Check the API server status                                                                                                                                                            |
| 💼 [/key](/reference/api-usage)                                                                        | Check account's API usage                                                                                                                                                              |
| [/simple/price](/reference/simple-price)                                                               | Query the prices of one or more coins by using their unique Coin API IDs                                                                                                               |
| [/simple/token\_price/\{id}](/reference/simple-token-price)                                            | Query the prices of one or more coins by using their unique Coin API IDs                                                                                                               |
| [/simple/supported\_vs\_currencies](/reference/simple-supported-currencies)                            | Query all the supported currencies on CoinGecko                                                                                                                                        |
| [/coins/list](/reference/coins-list)                                                                   | Query all the supported coins on CoinGecko with coins ID, name and symbol                                                                                                              |
| [/coins/markets](/reference/coins-markets)                                                             | Query all the supported coins with price, market cap, volume and market related data                                                                                                   |
| [/coins/\{id}](/reference/coins-id)                                                                    | Query all the metadata (image, websites, socials, description, contract address, etc.) from the CoinGecko coin page based on a particular coin ID                                      |
| [/coins/\{id}/tickers](/reference/coins-id-tickers)                                                    | Query the coin tickers on both centralized exchange (CEX) and decentralized exchange (DEX) based on a particular coin ID                                                               |
| [/coins/\{id}/history](/reference/coins-id-history)                                                    | Query the historical data (price, market cap, 24hr volume, ...) at a given date for a coin based on a particular coin ID                                                               |
| [/coins/\{id}/market\_chart](/reference/coins-id-market-chart)                                         | Get the historical chart data of a coin including time in UNIX, price, market cap and 24hr volume based on particular coin ID                                                          |
| [/coins/\{id}/market\_chart/range](/reference/coins-id-market-chart-range)                             | Get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hr volume based on particular coin ID                                     |
| [/coins-id-ohlc](/reference/coins-id-ohlc)                                                             | Get the OHLC chart (Open, High, Low, Close) of a coin based on particular coin ID                                                                                                      |
| 💼 [/coins/\{id}/ohlc/range](/reference/coins-id-ohlc-range)                                           | Get the OHLC chart (Open, High, Low, Close) of a coin within a range of timestamp based on particular coin ID                                                                          |
| 💼 [/coins/top\_gainers\_losers](/reference/coins-top-gainers-losers)                                  | Query the top 30 coins with largest price gain and loss by a specific time duration                                                                                                    |
| 💼 [/coins/list/new](/reference/coins-list-new)                                                        | Query the latest 200 coins that recently listed on CoinGecko                                                                                                                           |
| 👑 [/coins/\{id}/circulating\_supply\_chart](/reference/coins-id-circulating-supply-chart)             | Query historical circulating supply of a coin by number of days away from now based on provided coin ID                                                                                |
| 👑 [/coins/\{id}/circulating\_supply\_chart/range](/reference/coins-id-circulating-supply-chart-range) | Query historical circulating supply of a coin, within a range of timestamp based on the provided coin ID                                                                               |
| 👑 [/coins/\{id}/total\_supply\_chart](/reference/coins-id-total-supply-chart)                         | Query historical total supply of a coin by number of days away from now based on provided coin ID                                                                                      |
| 👑 [/coins/\{id}/total\_supply\_chart/range](/reference/coins-id-total-supply-chart-range)             | Query historical total supply of a coin, within a range of timestamp based on the provided coin ID                                                                                     |
| [/coins/../contract/..](/reference/coins-contract-address)                                             | Query all the metadata (image, websites, socials, description, contract address, etc.) from the CoinGecko coin page based on an asset platform and a particular token contract address |
| [/coins/../contract/../market\_chart](/reference/contract-address-market-chart)                        | Get the historical chart data including time in UNIX, price, market cap and 24hr volume based on asset platform and particular token contract address                                  |
| [/coins/../contract/../market\_chart/range](/reference/contract-address-market-chart-range)            | Get the historical chart data within certain time range in UNIX along with price, market cap and 24hr volume based on asset platform and particular token contract address             |
| [/coins/categories/list](/reference/coins-categories-list)                                             | Query all the coins categories on CoinGecko                                                                                                                                            |
| [/coins/categories](/reference/coins-categories)                                                       | Query all the coins categories with market data (market cap, volume, ...) on CoinGecko                                                                                                 |

## CoinGecko Endpoints: NFT

| Endpoint                                                                               | Description                                                                                                                                                                  |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [/nfts/list](/reference/nfts-list)                                                     | Query all supported NFTs with ID, contract address, name, asset platform ID and symbol on CoinGecko                                                                          |
| [/nfts/..](/reference/nfts-id)                                                         | Query all the NFT data (name, floor price, 24hr volume, ...) based on the NFT collection ID                                                                                  |
| [/nfts/../contract/..](/reference/nfts-contract-address)                               | Query all the NFT data (name, floor price, 24hr volume, ...) based on the NFT collection contract address and respective asset platform                                      |
| 💼 [/nfts/markets](/reference/nfts-markets)                                            | Query all the supported NFT collections with floor price, market cap, volume and market related data on CoinGecko                                                            |
| 💼 [/nfts/../market\_chart](/reference/nfts-id-market-chart)                           | Query historical market data of a NFT collection, including floor price, market cap, and 24hr volume, by number of days away from now                                        |
| 💼 [/nfts/../contract/../market\_chart](/reference/nfts-contract-address-market-chart) | Query historical market data of a NFT collection, including floor price, market cap, and 24hr volume, by number of days away from now based on the provided contract address |
| 💼 [/nfts/../tickers](/reference/nfts-id-tickers)                                      | Query the latest floor price and 24hr volume of a NFT collection, on each NFT marketplace, e.g. OpenSea and LooksRare                                                        |

## CoinGecko Endpoints: Exchanges & Derivatives

| Endpoint                                                                              | Description                                                                                                                   |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [/exchanges](/reference/exchanges)                                                    | Query all the supported exchanges with exchanges' data (ID, name, country, ...) that have active trading volumes on CoinGecko |
| [/exchanges/list](/reference/exchanges-list)                                          | Query all the exchanges with ID and name                                                                                      |
| [/exchanges/\{id}](/reference/exchanges-id)                                           | Query exchange's data (name, year established, country, ...), exchange volume in BTC and tickers based on exchange's ID       |
| [/exchanges/\{id}/tickers](/reference/exchanges-id-tickers)                           | Query exchange's tickers based on exchange's ID                                                                               |
| [/exchanges/\{id}/volume\_chart](/reference/exchanges-id-volume-chart)                | Query the historical volume chart data with time in UNIX and trading volume data in BTC based on exchange's ID                |
| 💼 [/exchanges/\{id}/volume\_chart/range](/reference/exchanges-id-volume-chart-range) | Query the historical volume chart data in BTC by specifying date range in UNIX based on exchange's ID                         |
| [/derivatives](/reference/derivatives-tickers)                                        | Query all the tickers from derivatives exchanges on CoinGecko                                                                 |
| [/derivatives/exchanges](/reference/derivatives-exchanges)                            | Query all the derivatives exchanges with related data (ID, name, open interest, ...) on CoinGecko                             |
| [/derivatives/exchanges/\{id}](/reference/derivatives-exchanges-id)                   | Query the derivatives exchange's related data (ID, name, open interest, ...) based on the exchanges' ID                       |
| [/derivatives/exchanges/list](/reference/derivatives-exchanges-list)                  | Query all the derivatives exchanges with ID and name on CoinGecko                                                             |

## CoinGecko Endpoints: Public Treasuries

| Endpoint                                                                        | Description                                                                               |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [/\{entity}/public\_treasury/\{coin\_id}](/reference/companies-public-treasury) | Query public companies & governments' cryptocurrency holdings by coin ID                  |
| [/public\_treasury/\{entity\_id}](/reference/public-treasury-entity)            | Query public companies & governments' cryptocurrency holdings by entity ID                |
| [/entities/list](/reference/entities-list)                                      | Query all the supported entities on CoinGecko with entities ID, name, symbol, and country |

## CoinGecko Endpoints: General

| Endpoint                                                                | Description                                                                                                        |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [/exchange\_rates](/reference/exchange-rates)                           | Query BTC exchange rates with other currencies                                                                     |
| [/asset\_platforms](/reference/asset-platforms-list)                    | Query all the asset platforms (blockchain networks) on CoinGecko                                                   |
| [/token\_lists/\{asset\_platform\_id}/all.json](/reference/token-lists) | Get full list of tokens of a blockchain network (asset platform) that is supported by Ethereum token list standard |
| [/search](/reference/search-data)                                       | Search for coins, categories and markets listed on CoinGecko                                                       |
| [/search/trending](/reference/trending-search)                          | Query trending search coins, NFTs and categories on CoinGecko in the last 24 hours                                 |
| [/global](/reference/crypto-global)                                     | Query cryptocurrency global data including active cryptocurrencies, markets, total crypto market cap and etc.      |
| [/global/decentralized\_finance\_defi](/reference/global-defi)          | Query cryptocurrency global decentralized finance (DeFi) data including DeFi market cap, trading volume            |
| 💼 [/global/market\_cap\_chart](/reference/global-market-cap-chart)     | Query historical global market cap and volume data by number of days away from now                                 |

## Onchain DEX Endpoints (GeckoTerminal)

| Endpoint                                                                                         | Description                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [/onchain/simple/networks/../token\_price/..](/reference/onchain-simple-price)                   | Get token price based on the provided token contract address on a network                                                                                                |
| [/onchain/networks](/reference/networks-list)                                                    | Query all the supported networks on GeckoTerminal                                                                                                                        |
| [/onchain/networks/../dexes](/reference/dexes-list)                                              | Query all the supported decentralized exchanges (DEXs) based on the provided network on GeckoTerminal                                                                    |
| [/onchain/networks/trending\_pools](/reference/trending-pools-list)                              | Query all the trending pools across all networks on GeckoTerminal                                                                                                        |
| [/onchain/networks/../trending\_pools](/reference/trending-pools-network)                        | Query the trending pools based on the provided network                                                                                                                   |
| [/onchain/networks/../pools/..](/reference/pool-address)                                         | Query the specific pool based on the provided network and pool address                                                                                                   |
| [/onchain/networks/../pools/multi/..](/reference/pools-addresses)                                | Query multiple pools based on the provided network and pool address                                                                                                      |
| [/onchain/networks/../pools](/reference/top-pools-network)                                       | Query all the top pools based on the provided network                                                                                                                    |
| [/onchain/networks/../dexes/../pools](/reference/top-pools-dex)                                  | Query all the top pools based on the provided network and decentralized exchange (DEX)                                                                                   |
| [/onchain/networks/../new\_pools](/reference/latest-pools-network)                               | Query all the latest pools based on provided network                                                                                                                     |
| [/onchain/networks/new\_pools](/reference/latest-pools-list)                                     | Query all the latest pools across all networks on GeckoTerminal                                                                                                          |
| 🔥 💼 [/onchain/pools/megafilter](/reference/pools-megafilter)                                   | Query pools based on various filters across all networks on GeckoTerminal                                                                                                |
| [/onchain/search/pools](/reference/search-pools)                                                 | Search for pools on a network                                                                                                                                            |
| 💼 [/onchain/pools/trending\_search](/reference/trending-search-pools)                           | Query all the trending search pools across all networks on GeckoTerminal                                                                                                 |
| [/onchain/networks/../tokens/../pools](/reference/top-pools-contract-address)                    | Query top pools based on the provided token contract address on a network                                                                                                |
| [/onchain/networks/../tokens/..](/reference/token-data-contract-address)                         | Query specific token data based on the provided token contract address on a network                                                                                      |
| [/onchain/networks/../tokens/multi/..](/reference/tokens-data-contract-addresses)                | Query multiple tokens data based on the provided token contract addresses on a network                                                                                   |
| [/onchain/networks/../tokens/../info](/reference/token-info-contract-address)                    | Query token metadata (name, symbol, CoinGecko ID, image, socials, websites, description, etc.) based on a provided token contract address on a network                   |
| [/onchain/networks/../pools/../info](/reference/pool-token-info-contract-address)                | Query pool metadata (base and quote token details, image, socials, websites, description, contract address, etc.) based on a provided pool contract address on a network |
| [/onchain/tokens/info\_recently\_updated](/reference/tokens-info-recent-updated)                 | Query 100 most recently updated tokens info across all networks on GeckoTerminal                                                                                         |
| 💼 [/onchain/networks/../tokens/../top\_holders](/reference/top-token-holders-token-address)     | Query top token holders based on the provided token contract address on a network                                                                                        |
| 💼 [/onchain/networks/../tokens/../holders\_chart](/reference/token-holders-chart-token-address) | Get the historical token holders chart based on the provided token contract address on a network                                                                         |
| [/onchain/networks/../pools/../ohlcv/..](/reference/pool-ohlcv-contract-address)                 | Get the OHLCV chart (Open, High, Low, Close, Volume) of a pool based on the provided pool address on a network                                                           |
| 💼 [/onchain/networks/../tokens/../ohlcv/..](/reference/token-ohlcv-token-address)               | Get the OHLCV chart (Open, High, Low, Close, Volume) of a token based on the provided token address on a network                                                         |
| [/onchain/networks/../pools/../trades](/reference/pool-trades-contract-address)                  | Query the last 300 trades in the past 24 hours based on the provided pool address                                                                                        |
| 💼 [/onchain/networks/../tokens/../trades](/reference/token-trades-contract-address)             | Query the last 300 trades in the past 24 hours across all pools, based on the provided token contract address on a network                                               |
| 💼 [/onchain/categories](/reference/categories-list)                                             | Query all the supported categories on GeckoTerminal                                                                                                                      |
| 💼 [/onchain/categories/../pools](/reference/pools-category)                                     | Query all the pools based on the provided category ID                                                                                                                    |

⚡️ Need Real-time Data Streams? Try [WebSocket API](https://docs.coingecko.com/websocket)

<a href="/websocket">
  <Frame>
    <img src="https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=2c88f667113256b6285720c468fb53a1" noZoom data-og-width="2400" width="2400" data-og-height="470" height="470" data-path="images/wss-banner-2.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=280&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=d2eafb93fcd670d5df221d617fd6f6a7 280w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=560&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=24f635622a42c0ae03695cc940112699 560w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=840&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=82ef1c05b6f45d6d8ec0bcef0f19d49a 840w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=1100&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=b119e8746bb1a78b759e6d94d96b7c8b 1100w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=1650&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=95797e7366c7f280e3e4b570b6db2b49 1650w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=2500&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=2f120e8a31b5793213494d4ae2d46fb3 2500w" />
  </Frame>
</a>

With WebSocket, you can now stream ultra-low latency, real-time prices, trades, and OHLCV chart data. <br />
Subscribe to our [paid API plan](https://www.coingecko.com/en/api/pricing) (Analyst plan & above) to access WebSocket and REST API data delivery methods.


# Entities List (ID Map)
Source: https://docs.coingecko.com/reference/entities-list

reference/api-reference/coingecko-pro.json get /entities/list
This endpoint allows you to **query all the supported entities on CoinGecko with entities ID, name, symbol, and country**

<Note>
  ### Note

  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# BTC-to-Currency Exchange Rates
Source: https://docs.coingecko.com/reference/exchange-rates

reference/api-reference/coingecko-pro.json get /exchange_rates
This endpoint allows you to **query BTC exchange rates with other currencies**

<Tip>
  ### Tips

  * You may use this endpoint to convert the response data, which is originally in BTC, to other currencies.
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Exchanges List with data
Source: https://docs.coingecko.com/reference/exchanges

reference/api-reference/coingecko-pro.json get /exchanges
This endpoint allows you to **query all the supported exchanges with exchanges' data (ID, name, country, ...) that have active trading volumes on CoinGecko**

<Tip>
  ### Tips

  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * All the exchanges in the responses are the exchanges with active trading volume on CoinGecko, any inactive or deactivated exchanges will be removed from the list.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Exchange Data by ID
Source: https://docs.coingecko.com/reference/exchanges-id

reference/api-reference/coingecko-pro.json get /exchanges/{id}
This endpoint allows you to **query exchange's data (name, year established, country, ...), exchange volume in BTC and top 100 tickers based on exchange's ID**

<Warning>
  ### Notice

  * Please note that the `trade_volume_24h_btc_normalized` data field will no longer be supported by our API starting on June 16, 2025. Please refer to [changelog](/changelog#may-2025) for more details.
</Warning>

<Note>
  ### Note

  * The exchange volume in the response is provided in BTC. To convert it to other currencies, please use [/exchange\_rates](/reference/exchange-rates) endpoint.
  * For derivatives (e.g. `bitmex`, `binance_futures`), to get derivatives exchanges data, please go to [/derivatives/exchange/\{id}](/reference/derivatives-exchanges-id) endpoint.
  * Tickers are limited to 100 items, to get more tickers, please go to [/exchanges/\{id}/tickers](/reference/exchanges-id-tickers) endpoint.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Exchange Tickers by ID
Source: https://docs.coingecko.com/reference/exchanges-id-tickers

reference/api-reference/coingecko-pro.json get /exchanges/{id}/tickers
This endpoint allows you to **query exchange's tickers based on exchange's ID**

<Note>
  ### Note

  * Responses are paginated and limited to 100 tickers per page. You may specify the page number using the `page` params to retrieve the tickers accordingly.
  * `order=base_target` sorts tickers by `base` symbol, then `target` symbol, in lexicographical order (`0 -> 9`, followed by `a -> z`).\
    This sorting method ensures stable pagination results, minimizing cases where cached responses might otherwise cause duplicate or missing tickers across paginated pages.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Exchange Volume Chart by ID
Source: https://docs.coingecko.com/reference/exchanges-id-volume-chart

reference/api-reference/coingecko-pro.json get /exchanges/{id}/volume_chart
This endpoint allows you to **query the historical volume chart data with time in UNIX and trading volume data in BTC based on exchange's ID**

<Note>
  ### Note

  * You can use this endpoint to query the historical volume chart data of **derivatives exchanges** as well.
  * The exchange volume in the response is provided in BTC. To convert it to other currencies, please use [/exchange\_rates](/reference/exchange-rates) endpoint.
  * Data granularity is automatic (cannot be adjusted):
    * 1 day = 10-minutely
    * 7, 14 days = hourly
    * 30 days & above = daily
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# 💼 Exchange Volume Chart within Time Range by ID
Source: https://docs.coingecko.com/reference/exchanges-id-volume-chart-range

reference/api-reference/coingecko-pro.json get /exchanges/{id}/volume_chart/range
This endpoint allows you to **query the historical volume chart data in BTC by specifying date range in UNIX based on exchange's ID**

<Note>
  ### Note

  * You can query the historical volume chart data of **derivatives exchanges** with this endpoint as well.
  * The data interval for this endpoint is fixed at daily.
  * The date range between `from` and `to` must be within 31 days.
  * Cache/Update Frequency: 5 minutes
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise)
</Note>


# Exchanges List (ID Map)
Source: https://docs.coingecko.com/reference/exchanges-list

reference/api-reference/coingecko-pro.json get /exchanges/list
This endpoint allows you to **query all the exchanges with ID and name**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of exchanges including **derivatives exchanges** for other endpoints that contain params like `id`(exchange ID).
</Tip>

<Note>
  ### Note

  * There is no pagination required for this endpoint.
  * Cache / Update Frequency:  every 5 minutes for all the API plans.
</Note>


# Global DeFi Market Data
Source: https://docs.coingecko.com/reference/global-defi

reference/api-reference/coingecko-pro.json get /global/decentralized_finance_defi
This endpoint allows you **query top 100 cryptocurrency global decentralized finance (DeFi) data including DeFi market cap, trading volume**



# 💼 Global Market Cap Chart Data
Source: https://docs.coingecko.com/reference/global-market-cap-chart

reference/api-reference/coingecko-pro.json get /global/market_cap_chart
This endpoint allows you to **query historical global market cap and volume data by number of days away from now**

<Note>
  ### Note

  * CoinGecko equivalent page: [https://www.coingecko.com/en/global-charts](https://www.coingecko.com/en/global-charts).
  * Data Granularity (auto):
    * 1 day from now = **hourly** data
    * 2 days & above from now = **daily** data
  * Exclusive for all Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
  * The last completed UTC day (00:00) is available 5 minutes after midnight on the next UTC day (00:05). The cache will **always expire at 00:05 UTC**. If you wish to get the latest daily data (00:00 UTC), you can make request at 00:05 UTC or later.
  * Cache / Update Frequency: every 1 minute.
</Note>


# New Pools List
Source: https://docs.coingecko.com/reference/latest-pools-list

reference/api-reference/onchain-pro.json get /networks/new_pools
This endpoint allows you to **query all the latest pools across all networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/explore/new-crypto-pools](https://www.geckoterminal.com/explore/new-crypto-pools)
</Note>


# New Pools by Network
Source: https://docs.coingecko.com/reference/latest-pools-network

reference/api-reference/onchain-pro.json get /networks/{network}/new_pools
This endpoint allows you to **query all the latest pools based on provided network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * This endpoint includes the newly created pools in the past 48 hours.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/explore/new-crypto-pools/solana](https://www.geckoterminal.com/explore/new-crypto-pools/solana)
</Note>


# Supported Networks List (ID Map)
Source: https://docs.coingecko.com/reference/networks-list

reference/api-reference/onchain-pro.json get /networks
This endpoint allows you to **query all the supported networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of networks with network ID for other endpoints that contain params like `network`.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>


# NFTs Collection Data by Contract Address
Source: https://docs.coingecko.com/reference/nfts-contract-address

reference/api-reference/coingecko-pro.json get /nfts/{asset_platform_id}/contract/{contract_address}
This endpoint allows you to **query all the NFT data (name, floor price, 24hr volume ...) based on the NFT collection contract address and respective asset platform**

<Tip>
  ### Tips

  * You may also obtain the asset platform ID and contract address through [/nfts/list](/reference/nfts-list) endpoint.
</Tip>

<Note>
  ### Note

  * Solana NFT & Art Blocks are not supported for this endpoint, please use [/nfts/\{id}](/reference/nfts-id) endpoint instead.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# 💼 NFTs Collection Historical Chart Data by Contract Address
Source: https://docs.coingecko.com/reference/nfts-contract-address-market-chart

reference/api-reference/coingecko-pro.json get /nfts/{asset_platform_id}/contract/{contract_address}/market_chart
This endpoint allows you **query historical market data of a NFT collection, including floor price, market cap, and 24hr volume, by number of days away from now based on the provided contract address**

<Note>
  ### Note

  * This endpoint doesn't support Solana NFT and Art Blocks, please use [/nfts/\{id}/market\_chart](/reference/nfts-id-market-chart) endpoint instead.
  * Data Granularity (auto):
    * 1-14 days from now = **5-minutely** data
    * 15 days & above from now = **daily** data (00:00 UTC)
  * Cache/Update Frequency: every 5 minutes
  * The last completed UTC day (00:00) is available 5 minutes after midnight on the next UTC day (00:05).
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>


# NFTs Collection Data by ID
Source: https://docs.coingecko.com/reference/nfts-id

reference/api-reference/coingecko-pro.json get /nfts/{id}
This endpoint allows you to **query all the NFT data (name, floor price, 24hr volume ...) based on the NFT collection ID**

<Note>
  ### Note

  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# 💼 NFTs Collection Historical Chart Data by ID
Source: https://docs.coingecko.com/reference/nfts-id-market-chart

reference/api-reference/coingecko-pro.json get /nfts/{id}/market_chart
This endpoint allows you **query historical market data of a NFT collection, including floor price, market cap, and 24hr volume, by number of days away from now**

<Note>
  ### Note

  * Data Granularity (auto):
    * 1-14 days from now = **5-minutely** data
    * 15 days & above from now = **daily** data (00:00 UTC)
  * Cache/Update Frequency: every 5 minutes
  * The last completed UTC day (00:00) is available 5 minutes after midnight on the next UTC day (00:05).
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>


# 💼 NFTs Collection Tickers by ID
Source: https://docs.coingecko.com/reference/nfts-id-tickers

reference/api-reference/coingecko-pro.json get /nfts/{id}/tickers
This endpoint allows you to **query the latest floor price and 24hr volume of a NFT collection, on each NFT marketplace, e.g. OpenSea and LooksRare**

<Note>
  ### Note

  * Cache/Update Frequency: every 30 seconds.
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>


# NFTs List (ID Map)
Source: https://docs.coingecko.com/reference/nfts-list

reference/api-reference/coingecko-pro.json get /nfts/list
This endpoint allows you to **query all supported NFTs with ID, contract address, name, asset platform ID and symbol on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of nfts for other endpoints that contain params like `id` (NFT collection's ID) as well as `asset_platform_id` and `contract_address`.
  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * The responses are paginated to 100 items.
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# 💼 NFTs List with Market Data
Source: https://docs.coingecko.com/reference/nfts-markets

reference/api-reference/coingecko-pro.json get /nfts/markets
This endpoint allows you to **query all the supported NFT collections with floor price, market cap, volume and market related data on CoinGecko**

<Tip>
  ### Tips

  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 5 minutes.
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
  * CoinGecko equivalent page: [https://www.coingecko.com/en/nft](https://www.coingecko.com/en/nft).
  * Some collection with low liquidity may not be ranked by Market Cap value, learn more [here](https://support.coingecko.com/hc/en-us/articles/37226121227545-What-is-NFT-Market-Cap). Sorting by Mcap ranking will first prioritise Market Cap value of liquid NFT collections, then followed by trading volume of illiquid NFT collections.
</Note>


# Token Price by Token Addresses
Source: https://docs.coingecko.com/reference/onchain-simple-price

reference/api-reference/onchain-pro.json get /simple/networks/{network}/token_price/{addresses}
This endpoint allows you to **get token price based on the provided token contract address on a network**

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
    * If you require `market_cap_usd` to return FDV value (as seen in [GeckoTerminal.com](https://www.geckoterminal.com/)) when market cap data is unavailable, please specify this parameter `mcap_fdv_fallback=true`.
  * The returned price currency is in USD.
  * Addresses not found in GeckoTerminal will be ignored.
  * This endpoint allows querying **up to 100 contract addresses** per request. This limit is exclusive for [paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above).
  * When using this endpoint, GeckoTerminal's routing decides the best pool for token price. The price source may change based on liquidity and pool activity. For full control over the price, you may use [`/networks/{network}/pools/{address}`](/reference/pool-address) endpoint by providing a specific pool address.
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Check API server status
Source: https://docs.coingecko.com/reference/ping-server

reference/api-reference/coingecko-pro.json get /ping
This endpoint allows you to **check the API server status**

<Note>
  ### Note

  * You can also go to [status.coingecko.com](https://status.coingecko.com/) to check the API server status and further maintenance notices.
</Note>


# Specific Pool Data by Pool Address
Source: https://docs.coingecko.com/reference/pool-address

reference/api-reference/onchain-pro.json get /networks/{network}/pools/{address}
This endpoint allows you to **query the specific pool based on the provided network and pool address**

<Note>
  ### Note

  * Address not found in GeckoTerminal will be ignored.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * `locked_liquidity_percentage` will be updated on daily basis.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens.
  * Pools on a bonding curve (e.g. non-graduated pools from launchpads) will return `launchpad_details` object with their graduation status and migration details.
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Pool OHLCV chart by Pool Address
Source: https://docs.coingecko.com/reference/pool-ohlcv-contract-address

reference/api-reference/onchain-pro.json get /networks/{network}/pools/{pool_address}/ohlcv/{timeframe}
This endpoint allows you to **get the OHLCV chart (Open, High, Low, Close, Volume) of a pool based on the provided pool address on a network**

<Tip>
  ### Tips

  * You may use this endpoint to query the historical price and volume of a token.
  * You may select the timeframe with its respective aggregate to get the intended OHLCV data (e.g. `minute?aggregate=15` for 15 minutes OHLCV).
</Tip>

<Note>
  ### Note

  * This endpoint uses epoch/unix format for its timestamp. Example: `1708850449`.
  * [Paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above) can access data from **September 2021 to the present**, depending on when the pool started tracking on GeckoTerminal.
    * If no earlier data is available, an empty response will be returned.
    * Each API call can only retrieve data for a **maximum range of 6 months**. To fetch older data, use the `before_timestamp` parameter to query in multiple requests.
  * Pools with more than 2 tokens are not yet supported for this endpoint.
  * Each OHLCV array (under "ohlcv\_list") consists of 6 elements in the following order:
    * Timestamp: The epoch/unix timestamp representing the start of the time interval.
    * Open: The opening price of the asset at the beginning of the interval.
    * High: The highest price reached during the interval.
    * Low: The lowest price reached during the interval.
    * Close: The price of the asset at the end of the interval.
    * Volume: The total trading volume of the asset during the interval.
  * **Skipped Intervals**: To ensure concise and relevant data, specific timeframe intervals (e.g. minutely) with no recorded swaps are **excluded** from the response.
    * Higher granularity timeframes (e.g. 1 minute) are more likely to skip intervals due to periods of inactivity, while lower granularity timeframes (e.g. daily) are less affected.
  * For `include_empty_intervals` param:
    * When `false` (default): Only intervals with trade data are returned.
    * When `true`: All requested intervals are returned, those with no trade data are populated as follows:
      * OHLC (Open, High, Low, Close) are all set to the Close price of the previous interval.
        * *O = H = L = C = previous Close*
      * Volume (V) is set to 0, reflecting no trade activity.
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Pool Tokens Info by Pool Address
Source: https://docs.coingecko.com/reference/pool-token-info-contract-address

reference/api-reference/onchain-pro.json get /networks/{network}/pools/{pool_address}/info
This endpoint allows you to **query pool metadata (base and quote token details, image, socials, websites, description, contract address, etc.) based on a provided pool contract address on a network**

<Tip>
  ### Tips

  * If you would like to query pool data such as price, transactions, volume and etc. You can go to this endpoint [`/networks/{network}/pools/{address}`](/reference/pool-address) instead.
  * Cache/Update frequency: every 60 seconds.
  * Learn more about GT score [here](https://support.coingecko.com/hc/en-us/articles/38381394237593-What-is-GT-Score-How-is-GT-Score-calculated).
  * Metadata (image, websites, description, socials) may be sourced on-chain and is not vetted by the CoinGecko team. If you wish to get metadata reviewed by CoinGecko team, you may use the following endpoints:
    * [Coin Data by ID](/reference/coins-id)
    * [Coin Data by Token Address](/reference/coins-contract-address)
</Tip>

<Note>
  ### Note

  * `holders` data is currently in Beta, with ongoing improvements to data quality, coverage, and update frequency.
    * Supported chains include: Solana, EVM (Ethereum, Polygon, BNB, Arbitrum, Optimism, Base), Sui, TON, and Ronin.
    * `distribution_percentage` coverage:
      * Solana: `top_10`, `11_20`, `21_40`, `rest`
      * Other chains: `top_10`, `11_30`, `31_50`, `rest`
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
</Note>


# Past 24 Hour Trades by Pool Address
Source: https://docs.coingecko.com/reference/pool-trades-contract-address

reference/api-reference/onchain-pro.json get /networks/{network}/pools/{pool_address}/trades
This endpoint allows you to **query the last 300 trades in the past 24 hours based on the provided pool address**

<Note>
  ### Note

  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Multiple Pools Data by Pool Addresses
Source: https://docs.coingecko.com/reference/pools-addresses

reference/api-reference/onchain-pro.json get /networks/{network}/pools/multi/{addresses}
This endpoint allows you to **query multiple pools based on the provided network and pool address**

<Note>
  ### Note

  * Addresses not found in GeckoTerminal will be ignored.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * This endpoint allows querying **up to 50 contract addresses** per request. This limit is exclusive for [paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include ` params will be included under the "included" key at the top level.
  * `locked_liquidity_percentage` will be updated on daily basis.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens.
  * Pools on a bonding curve (e.g. non-graduated pools from launchpads) will return `launchpad_details` object with their graduation status and migration details.
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# 💼 Pools by Category ID
Source: https://docs.coingecko.com/reference/pools-category

reference/api-reference/onchain-pro.json get /categories/{category_id}/pools
This endpoint allows you to **query all the pools based on the provided category ID**

<Tip>
  ### Tips

  * You can retrieve full list of categories id via this endpoint: [Categories List](/reference/categories-list).
  * You can retrieve tokens of a specific category, by flagging `include=base_token`.
  * GeckoTerminal categories are different from [CoinGecko categories](/reference/coins-categories-list).
</Tip>

<Note>
  ### Note

  * Trending rankings are determined by a combination of factors:
    * User engagement on geckoterminal.com
    * Market activity, such as trading volume and transactions
    * Pool security and credibility, including liquidity and honeypot checks
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * GeckoTerminal equivalent page example: [https://www.geckoterminal.com/category/pump-fun](https://www.geckoterminal.com/category/pump-fun)
  * Cache/Update frequency: every 30 seconds.
  * Exclusive for all Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>


# 🔥 Megafilter for Pools
Source: https://docs.coingecko.com/reference/pools-megafilter

reference/api-reference/onchain-pro.json get /pools/megafilter
This endpoint allows you to **query pools based on various filters across all networks on GeckoTerminal**

<Tip>
  ### Tips

  * Using `checks` param to filter pools based on various checks:
    * `checks=no_honeypot` — Filter out Honeypot pools, using GoPlus Token Security and De.Fi Scanner.
    * `checks=good_gt_score` — Show only pools with a GT Score of at least 75.
    * `checks=on_coingecko` — Show only pools with tokens that are listed on CoinGecko.
    * `checks=has_social` — Show only pools with their social links and token information updated.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * Trending rankings are determined by a combination of factors:
    * User engagement on geckoterminal.com
    * Market activity, such as trading volume and transactions
    * Pool security and credibility, including liquidity and honeypot checks
  * `dexes` param can only be used when **only 1`networks`** is specified.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * Setting `include_unknown_honeypot_tokens=true` will include tokens with an 'unknown' honeypot status.
    * Please note that this param only takes effect when `checks=no_honeypot` is specified.
  * Cache/Update frequency: every 30 seconds.
  * 💼 Exclusive for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
</Note>


# Crypto Treasury Holdings by Entity ID
Source: https://docs.coingecko.com/reference/public-treasury-entity

reference/api-reference/coingecko-pro.json get /public_treasury/{entity_id}
This endpoint allows you **query public companies & governments' cryptocurrency holdings** by Entity ID

<Note>
  ### Note

  * CoinGecko equivalent page: [https://www.coingecko.com/en/treasuries/bitcoin](https://www.coingecko.com/en/treasuries/bitcoin)
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Search Queries
Source: https://docs.coingecko.com/reference/search-data

reference/api-reference/coingecko-pro.json get /search
This endpoint allows you to **search for coins, categories and markets listed on CoinGecko**

<Note>
  ### Note

  * The responses are sorted in descending order by market cap.
  * Cache / Update Frequency: every 15 minutes for all the API plans.
</Note>


# Search Pools
Source: https://docs.coingecko.com/reference/search-pools

reference/api-reference/onchain-pro.json get /search/pools
This endpoint allows you to **search for pools on a network**

<Tip>
  ### Tips

  * You may use this endpoint to search for query such as pool contract address, token contract address or token symbol. The endpoint will return matching pools as response.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
</Note>


# Coin Price by IDs
Source: https://docs.coingecko.com/reference/simple-price

reference/api-reference/coingecko-pro.json get /simple/price
This endpoint allows you to **query the prices of one or more coins by using their unique Coin API IDs**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint.
    * refers to Google Sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You can retrieve specific coins using their unique `ids`, `names`, or `symbols`.
  * You may flag to include more data such as market cap, 24hr volume, 24hr change, last updated time etc.
  * To verify if a price is stale, you may flag `include_last_updated_at=true` in your request to obtain the latest updated time. Alternatively, you may flag `include_24hr_change=true` to determine if it returns a `null` value.
</Tip>

<Note>
  ### Note

  * You may cross-check the price on [CoinGecko](https://www.coingecko.com) and learn more about our price methodology [here](https://www.coingecko.com/en/methodology).
  * When multiple lookup params are provided, the following priority order is applied: `ids` (highest) > `names` > `symbols` (lowest).
  * When searching by `name`, you need to URL-encode any spaces (e.g. "Binance Coin" becomes "Binance%20Coin").
  * The `include_tokens=all` param is exclusively for use with the `symbols` lookup and is limited to maximum of 50 symbols per request.
  * Wildcard searches are not supported for lookup params (`ids`, `names`, `symbols`).
  * Cache/Update Frequency: every 20 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Supported Currencies List
Source: https://docs.coingecko.com/reference/simple-supported-currencies

reference/api-reference/coingecko-pro.json get /simple/supported_vs_currencies
This endpoint allows you to **query all the supported currencies on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of currencies for other endpoints that contain params like `vs_currencies`.
</Tip>

<Note>
  ### Note

  * Cache/Update Frequency: every 30 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Coin Price by Token Addresses
Source: https://docs.coingecko.com/reference/simple-token-price

reference/api-reference/coingecko-pro.json get /simple/token_price/{id}
This endpoint allows you to **query one or more token prices using their token contract addresses**

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/reference/coins-list) endpoint (`include platform = true`).
  * You may flag to include more data such as market cap, 24hr volume, 24hr change, last updated time etc.
</Tip>

<Note>
  ### Note

  * The endpoint returns the global average price of the coin that is aggregated across all active exchanges on CoinGecko.
  * You may cross-check the price on [CoinGecko](https://www.coingecko.com) and learn more about our price methodology [here](https://www.coingecko.com/en/methodology).
  * Cache/Update Frequency: every 20 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Token Data by Token Address
Source: https://docs.coingecko.com/reference/token-data-contract-address

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/{address}
This endpoint allows you to **query specific token data based on the provided token contract address on a network**

<Tip>
  ### Tips

  * You may add values such as `top_pools` in the include param to include top pools along with the pools information.
  * If you would like to query token information such as socials, websites, description and etc. You can go to this endpoint [`/networks/{network}/tokens/{address}/info`](/reference/token-info-contract-address) instead.
</Tip>

<Note>
  ### Note

  * Address not found in GeckoTerminal.com will be ignored.
  * The endpoint will only return the first top most liquid pool for each token. The top pool is determined through a combination of two key factors: liquidity (`reserve_in_usd`) and 24-Hour Trading Volume (`volume_usd`)
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens. (requires `include=top_pools`)
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# 💼 Historical Token Holders Chart by Token Address
Source: https://docs.coingecko.com/reference/token-holders-chart-token-address

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/{token_address}/holders_chart
This endpoint allows you to **get the historical token holders chart based on the provided token contract address on a network**

<Note>
  ### Note

  * The historical token holders chart data is currently in Beta, with ongoing improvements to data quality, coverage, and update frequency.
  * Supported chains include: Solana, EVM (Ethereum, Polygon, BNB, Arbitrum, Optimism, Base), Sui, TON, and Ronin.
  * `days` param provides the following automatic granularity:
    * `days=7` = **all data** (without fixed intervals)
    * `days=30` = **daily data** (30 daily intervals)
    * `days=max` = **weekly data**
  * 💼 Exclusive for Paid Plan subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
</Note>


# Token Info by Token Address
Source: https://docs.coingecko.com/reference/token-info-contract-address

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/{address}/info
This endpoint allows you to **query token metadata (name, symbol,  CoinGecko ID, image, socials, websites, description, etc.) based on a provided token contract address on a network**

<Tip>
  ### Tips

  * If you would like to query token data such as decimals, total supply, price and etc. You can go to this endpoint [`/networks/{network}/tokens/{address}`](/reference/token-data-contract-address) instead.
  * Cache/Update frequency: every 60 seconds.
  * Learn more about GT score [here](https://support.coingecko.com/hc/en-us/articles/38381394237593-What-is-GT-Score-How-is-GT-Score-calculated).
  * Metadata (image, websites, description, socials) may be sourced on-chain and is not vetted by the CoinGecko team. If you wish to get metadata reviewed by CoinGecko team, you may use the following endpoints:
    * [Coin Data by ID](/reference/coins-id)
    * [Coin Data by Token Address](/reference/coins-contract-address)
</Tip>

<Note>
  ### Note

  * `holders` data is currently in Beta, with ongoing improvements to data quality, coverage, and update frequency.
    * Supported chains include: Solana, EVM (Ethereum, Polygon, BNB, Arbitrum, Optimism, Base), Sui, TON, and Ronin.
    * `distribution_percentage` coverage:
      * Solana: `top_10`, `11_20`, `21_40`, `rest`
      * Other chains: `top_10`, `11_30`, `31_50`, `rest`
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
</Note>


# Token Lists by Asset Platform ID
Source: https://docs.coingecko.com/reference/token-lists

reference/api-reference/coingecko-pro.json get /token_lists/{asset_platform_id}/all.json
This endpoint allows you to **get full list of tokens of a blockchain network (asset platform) that is supported by [Ethereum token list standard](https://tokenlists.org/)**

<Note>
  ### Note

  * Cache/Update Frequency: 5 minutes.
  * A token will only be included in the list if the contract address is added by CoinGecko team. If you identified any missing token, you may submit a request [here](https://support.coingecko.com/hc/en-us/requests/new).
</Note>


# 💼 Token OHLCV chart by Token Address
Source: https://docs.coingecko.com/reference/token-ohlcv-token-address

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/{token_address}/ohlcv/{timeframe}
This endpoint allows you to **get the OHLCV chart (Open, High, Low, Close, Volume) of a token based on the provided token address on a network**

<Note>
  ### Note

  * This endpoint will return OHLCV data of the **most liquid pool** of the specified token. You may use this endpoint [Top Pools by Token Address](https://docs.coingecko.com/update/reference/top-pools-contract-address#/) to check the top pools of a token.
  * This endpoint uses epoch/unix format for its timestamp. Example: `1708850449`.
  * [Paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above) can access data from **September 2021 to the present**, depending on when the pool started tracking on GeckoTerminal.
    * If no earlier data is available, an empty response will be returned.
    * Each API call can only retrieve data for a **maximum range of 6 months**. To fetch older data, use the `before_timestamp` parameter to query in multiple requests.
  * Pools with more than 2 tokens are not yet supported for this endpoint.
  * Each OHLCV array (under "ohlcv\_list") consists of 6 elements in the following order:
    * Timestamp: The epoch/unix timestamp representing the start of the time interval.
    * Open: The opening price of the asset at the beginning of the interval.
    * High: The highest price reached during the interval.
    * Low: The lowest price reached during the interval.
    * Close: The price of the asset at the end of the interval.
    * Volume: The total trading volume of the asset during the interval.
  * **Skipped Intervals**: To ensure concise and relevant data, specific timeframe intervals (e.g. minutely) with no recorded swaps are **excluded** from the response.
    * Higher granularity timeframes (e.g. 1 minute) are more likely to skip intervals due to periods of inactivity, while lower granularity timeframes (e.g. daily) are less affected.
  * For `include_empty_intervals` param:
    * When `false` (default): Only intervals with trade data are returned.
    * When `true`: All requested intervals are returned, those with no trade data are populated as follows:
      * OHLC (Open, High, Low, Close) are all set to the Close price of the previous interval.
        * *O = H = L = C = previous Close*
      * Volume (V) is set to 0, reflecting no trade activity.
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# 💼 Past 24 Hour Trades by Token Address
Source: https://docs.coingecko.com/reference/token-trades-contract-address

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/{token_address}/trades
This endpoint allows you to **query the last 300 trades in the past 24 hours, across all pools, based on the provided token contract address on a network**

<Note>
  ### Note

  * Exclusive for all [Paid Plan](https://www.coingecko.com/en/api/pricing) Subscribers (Analyst, Lite, Pro and Enterprise).
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Tokens Data by Token Addresses
Source: https://docs.coingecko.com/reference/tokens-data-contract-addresses

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/multi/{addresses}
This endpoint allows you to **query multiple tokens data based on the provided token contract addresses on a network**

<Tip>
  ### Tips

  * You may add values such as `top_pools` in the include param to include top pools along with the pools information.
  * If you would like to query token information such as socials, websites, description and etc. You can go to this endpoint [`/networks/{network}/tokens/{address}/info`](/reference/token-info-contract-address) instead.
</Tip>

<Note>
  ### Note

  * Addresses not found in GeckoTerminal.com will be ignored.
  * This endpoint allows querying **up to 50 contract addresses** per request. This limit is exclusive for [paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above).
  * The endpoint will only return the first top most liquid pool for each token. The top pool is determined through a combination of two key factors: liquidity (`reserve_in_usd`) and 24-Hour Trading Volume (`volume_usd`).
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens. (requires `include=top_pools`)
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
  * Cache/Update Frequency: every 10 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Most Recently Updated Tokens List
Source: https://docs.coingecko.com/reference/tokens-info-recent-updated

reference/api-reference/onchain-pro.json get /tokens/info_recently_updated
This endpoint allows you to **query 100 most recently updated tokens info of a specific network or across all networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may add values such as network in the include param to include network along with the updated tokens list.
</Tip>

<Note>
  ### Note

  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * Cache/Update frequency: every 30 seconds.
</Note>


# Top Pools by Token Address
Source: https://docs.coingecko.com/reference/top-pools-contract-address

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/{token_address}/pools
This endpoint allows you to **query top pools based on the provided token contract address on a network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * The ranking of the top 20 pools is established by evaluating their liquidity and trading activity to identify the most liquid ones. This ranking is determined through a combination of two key factors: liquidity (`reserve_in_usd`) and 24-Hour Trading Volume (`volume_usd`).
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
</Note>


# Top Pools by Dex
Source: https://docs.coingecko.com/reference/top-pools-dex

reference/api-reference/onchain-pro.json get /networks/{network}/dexes/{dex}/pools
This endpoint allows you to **query all the top pools based on the provided network and decentralized exchange (DEX)**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](/reference/pools-megafilter) endpoint.
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/base/uniswap-v3-base/pools?sort=-24h\_transactions](https://www.geckoterminal.com/base/uniswap-v3-base/pools?sort=-24h_transactions)
</Note>


# Top Pools by Network
Source: https://docs.coingecko.com/reference/top-pools-network

reference/api-reference/onchain-pro.json get /networks/{network}/pools
This endpoint allows you to **query all the top pools based on the provided network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](/reference/pools-megafilter) endpoint.
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/solana/pools?sort=-24h\_transactions](https://www.geckoterminal.com/solana/pools?sort=-24h_transactions)
</Note>


# 💼 Top Token Holders by Token Address
Source: https://docs.coingecko.com/reference/top-token-holders-token-address

reference/api-reference/onchain-pro.json get /networks/{network}/tokens/{address}/top_holders
This endpoint allows you to **query top token holders based on the provided token contract address on a network**

<Note>
  ### Note

  * The top holders data is currently in **Beta**, with ongoing improvements to data quality, coverage, and update frequency.
  * **Supported chains include**: Solana, EVM (Ethereum, Polygon, BNB, Arbitrum, Optimism, Base), Sui, TON, and Ronin.
  * Max `holders` value:
    * Maximum 50 for non-Solana networks, 40 for Solana network.
  * 💼 Exclusive for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
</Note>


# Trending Pools List
Source: https://docs.coingecko.com/reference/trending-pools-list

reference/api-reference/onchain-pro.json get /networks/trending_pools
This endpoint allows you to **query all the trending pools across all networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](/reference/pools-megafilter) endpoint.
</Tip>

<Note>
  ### Note

  * Trending rankings are determined by a combination of factors:
    * User engagement on geckoterminal.com
    * Market activity, such as trading volume and transactions
    * Pool security and credibility, including liquidity and honeypot checks
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com](https://www.geckoterminal.com)
</Note>


# Trending Pools by Network
Source: https://docs.coingecko.com/reference/trending-pools-network

reference/api-reference/onchain-pro.json get /networks/{network}/trending_pools
This endpoint allows you to **query the trending pools based on the provided network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](/reference/pools-megafilter) endpoint.
</Tip>

<Note>
  ### Note

  * Trending rankings are determined by a combination of factors:
    * User engagement on geckoterminal.com
    * Market activity, such as trading volume and transactions
    * Pool security and credibility, including liquidity and honeypot checks
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 30 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/base/pools](https://www.geckoterminal.com/base/pools)
</Note>


# Trending Search List
Source: https://docs.coingecko.com/reference/trending-search

reference/api-reference/coingecko-pro.json get /search/trending
This endpoint allows you **query trending search coins, NFTs and categories on CoinGecko in the last 24 hours**

<Note>
  ### Note

  * The endpoint currently supports:
    * Top 15 trending coins (sorted by the most popular user searches).
    * Top 7 trending NFTs (sorted by the highest percentage change in floor prices).
    * Top 6 trending categories (sorted by the most popular user searches).
  * [Paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above) can use `show_max` param to retrieve maximum 30 coins, 10 NFTs, and 10 categories.
  * Cache / Update Frequency: every 10 minutes for all the API plans.
</Note>


# 💼 Trending Search Pools
Source: https://docs.coingecko.com/reference/trending-search-pools

reference/api-reference/onchain-pro.json get /pools/trending_search
This endpoint allows you to **query all the trending search pools across all networks on GeckoTerminal**

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * Cache/Update frequency: every 60 seconds.
  * 💼 Exclusive for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
</Note>


# Asset Platforms List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/asset-platforms-list

v3.0.1/reference/api-reference/coingecko-demo.json get /asset_platforms
This endpoint allows you to **query all the asset platforms on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of asset platforms for other endpoints that contain params like `id` or`ids`(asset platforms).
  * You may include NFT at the `filter` params to get the list of NFT-support asset platforms on CoinGecko.
</Tip>


# Authentication (Public/Demo)
Source: https://docs.coingecko.com/v3.0.1/reference/authentication

Authentication method for CoinGecko Public API (Demo plan users)

<Note>
  ### **Notes**

  * Demo API Key is only available for CoinGecko Public Demo API Plan, the root URL for CoinGecko Public Demo API must be `https://api.coingecko.com/api/v3/`.
  * ⚠️ You are recommended to store the API key securely in your own backend and use a proxy to insert the key into the request URL.
  * The authentication method below is for CoinGecko Public Demo API only. For **paid plan users with Pro-API key**, please refer to [this page](/reference/authentication) instead.
  * User Guide: [How to sign up for CoinGecko Demo API and generate an API key?](https://support.coingecko.com/hc/en-us/articles/21880397454233)
  * It's highly recommended to use the **Headers method** when making API requests for better security. Using query string parameters can risk exposing your API key.
</Note>

## CoinGecko API Authentication Method

If this is your first time using the Demo API key, you can supply API Key to the root URL using one of these ways:

1. Header (Recommended): `x-cg-demo-api-key`
2. Query String Parameter: `x_cg_demo_api_key`

| Authentication Method  | Example using [Ping](/v3.0.1/reference/ping-server) Endpoint                               |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| Header (cURL)          | `curl -X GET "https://api.coingecko.com/api/v3/ping" -H "x-cg-demo-api-key: YOUR_API_KEY"` |
| Query String Parameter | `https://api.coingecko.com/api/v3/ping?x_cg_demo_api_key=YOUR_API_KEY`                     |

## API Key Usage Credits

* Each request made to any endpoint counts as a single call (1 call = 1 credit).
* Your monthly credit & rate limit are determined by the paid plan to which you subscribe. For more details, please refer to this [page](https://www.coingecko.com/en/api/pricing).
* To check the API usage, please go to the [developer dashboard](https://www.coingecko.com/en/developers/dashboard) or follow the guide [here](/v3.0.1/reference/setting-up-your-api-key#4-api-usage-report).


# Coins Categories List with Market Data
Source: https://docs.coingecko.com/v3.0.1/reference/coins-categories

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/categories
This endpoint allows you to **query all the coins categories with market data (market cap, volume, ...) on CoinGecko**

<Note>
  ### Note

  * CoinGecko Equivalent Page: [https://www.coingecko.com/en/categories](https://www.coingecko.com/en/categories)
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Coins Categories List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/coins-categories-list

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/categories/list
This endpoint allows you to **query all the coins categories on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of categories for other endpoints that contain params like `category`.
</Tip>

<Note>
  ### Note

  * CoinGecko Equivalent Page: [https://www.coingecko.com/en/categories](https://www.coingecko.com/en/categories)
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Coin Data by Token Address
Source: https://docs.coingecko.com/v3.0.1/reference/coins-contract-address

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/contract/{contract_address}
This endpoint allows you to **query all the metadata (image, websites, socials, description, contract address, etc.) and market data (price, ATH, exchange tickers, etc.) of a coin from the CoinGecko coin page based on an asset platform and a particular token contract address**

<Warning>
  ### Notice

  * Please note that the `twitter_followers` data field will no longer be supported by our API starting on May 15, 2025. Please refer to [changelog](/changelog#upcoming-change-notice%3A-removal-of-twitter-followers-data) for more details.
</Warning>

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint (`include platform = true`).
</Tip>

<Note>
  ### Note

  * Coin descriptions may include newline characters represented as `\r\n` (escape sequences), which may require processing for proper formatting.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Coin Data by ID
Source: https://docs.coingecko.com/v3.0.1/reference/coins-id

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}
This endpoint allows you to **query all the metadata (image, websites, socials, description, contract address, etc.) and market data (price, ATH, exchange tickers, etc.) of a coin from the CoinGecko coin page based on a particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin `id` (API ID) via several ways:
    * refers to respective coin page and find "API ID".
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint.
    * refers to Google Sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You may also flag to include more data such as tickers, market data, community data, developer data and sparkline.
  * You may refer to `last_updated` in the endpoint response to check whether the price is stale.
</Tip>

<Note>
  ### Note

  * Tickers are limited to 100 items, to get more tickers, please go to [/coins/{id}/tickers](/v3.0.1/reference/coins-id-tickers).
  * Coin descriptions may include newline characters represented as `\r\n` (escape sequences), which may require processing for proper formatting.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache/Update Frequency:
    * Every 60 seconds for all the API plans.
    * Community data for Telegram will be updated on weekly basis (Reddit & Twitter community data are no longer supported).
</Note>


# Coin Historical Data by ID
Source: https://docs.coingecko.com/v3.0.1/reference/coins-id-history

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/history
This endpoint allows you to **query the historical data (price, market cap, 24hrs volume, ...) at a given date for a coin based on a particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint.
    * refers to Google Sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
</Tip>

<Note>
  ### Note

  * The data returned is at `00:00:00 UTC`.
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
  * Access to historical data via the Public API (Demo plan) is **restricted to the past 365 days** only. To access the complete range of historical data, please subscribe to one of our [paid plans](https://www.coingecko.com/en/api/pricing) to obtain a Pro-API key.
</Note>


# Coin Historical Chart Data by ID
Source: https://docs.coingecko.com/v3.0.1/reference/coins-id-market-chart

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/market_chart
This endpoint allows you to **get the historical chart data of a coin including time in UNIX, price, market cap and 24hr volume based on particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You may use tools like [epoch converter ](https://www.epochconverter.com) to convert human readable date to UNIX timestamp.
</Tip>

<Note>
  ### Note

  * You may leave the interval as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 2 - 90 days from current time = **hourly** data
    * above 90 days from current time = **daily** data (00:00 UTC)
  * Cache / Update Frequency:
    * Every 30 seconds for all the API plans (for last data point).
    * The last completed UTC day (00:00) data is now available **10 minutes after midnight** on the next UTC day (00:10).
  * Access to historical data via the Public API (Demo plan) is **restricted to the past 365 days** only. To access the complete range of historical data, please subscribe to one of our [paid plans](https://www.coingecko.com/en/api/pricing) to obtain a Pro-API key.
</Note>


# Coin Historical Chart Data within Time Range by ID
Source: https://docs.coingecko.com/v3.0.1/reference/coins-id-market-chart-range

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/market_chart/range
This endpoint allows you to **get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hr volume based on particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
</Tip>

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 1 day from any time (except current time) = **hourly** data
    * 2 - 90 days from any time = **hourly** data
    * above 90 days from any time = **daily** data (00:00 UTC)
  * Cache / Update Frequency:\
    Based on days range (all the API plans)
    * 1 day = 30 seconds cache
    * 2 -90 days = 30 minutes cache
    * 90 days = 12 hours cache
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35). The cache will always expire at 00:40 UTC.
  * Access to historical data via the Public API (Demo plan) is **restricted to the past 365 days** only. To access the complete range of historical data, please subscribe to one of our [paid plans](https://www.coingecko.com/en/api/pricing) to obtain a Pro-API key.
</Note>


# Coin OHLC Chart by ID
Source: https://docs.coingecko.com/v3.0.1/reference/coins-id-ohlc

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/ohlc
This endpoint allows you to **get the OHLC chart (Open, High, Low, Close) of a coin based on particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * For historical chart data with better granularity, you may consider using [/coins/\{id}/market\_chart](/v3.0.1/reference/coins-id-market-chart) endpoint.
</Tip>

<Note>
  ### Note

  * The timestamp displayed in the payload (response) indicates the end (or close) time of the OHLC data.
  * Data granularity (candle's body) is automatic:
    * 1 - 2 days: 30 minutes
    * 3 - 30 days: 4 hours
    * 31 days and beyond: 4 days
  * Cache / Update Frequency:
    * Every 15 minutes for all the API plans.
    * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35).
  * Access to historical data via the Public API (Demo plan) is **restricted to the past 365 days** only. To access the complete range of historical data, please subscribe to one of our [paid plans](https://www.coingecko.com/en/api/pricing) to obtain a Pro-API key.
</Note>


# Coin Tickers by ID
Source: https://docs.coingecko.com/v3.0.1/reference/coins-id-tickers

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/tickers
This endpoint allows you to **query the coin tickers on both centralized exchange (CEX) and decentralized exchange (DEX) based on a particular coin ID**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint.
    * refers to google sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You may specify the `exchange_ids` if you want to retrieve tickers for specific exchange only.
  * You may include values such as  `page` to specify which page of responses you would like to show.
  * You may also flag to include more data such as exchange logo and depth.
</Tip>

<Note>
  ### Note

  * The tickers are paginated to 100 items.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * When order is sorted by `volume`, ***converted\_volume*** will be used instead of ***volume***.
  * Cache / Update Frequency: every 2 minutes for all the API plans.
</Note>


# Coins List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/coins-list

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/list
This endpoint allows you to **query all the supported coins on CoinGecko with coins ID, name and symbol**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of coins with coin ID for other endpoints that contain params like `id` or `ids` (coin ID).
</Tip>

<Note>
  ### Note

  * There is no pagination required for this endpoint.
  * Access to inactive coins via the Public API (Demo plan) is restricted. To access them, please subscribe to one of our paid plans to obtain a Pro-API key.
  * Cache/Update Frequency:
    * Every 30 minutes for Public API.
    * Every 5 minutes for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Coins List with Market Data
Source: https://docs.coingecko.com/v3.0.1/reference/coins-markets

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/markets
This endpoint allows you to **query all the supported coins with price, market cap, volume and market related data**

<Tip>
  ### Tips

  * You can retrieve specific coins using their unique `ids`, `names`, or `symbols` instead of returning the whole list.
  * To filter results based on the coin's category, use the `category` param (refer to [`/coins/categories/list`](/v3.0.1/reference/coins-categories-list) for available categories).
  * Use the `per_page` and `page` params to manage the number of results you receive and navigate through the data.
</Tip>

<Note>
  ### Note

  * When multiple lookup params are provided, the following priority order is applied: `category` (highest) > `ids` > `names` > `symbols` (lowest).
  * When searching by `name`, you need to URL-encode any spaces (e.g. "Binance Coin" becomes "Binance%20Coin").
  * The `include_tokens=all` param is exclusively for use with the `symbols` lookup and is limited to maximum of 50 symbols per request.
  * Wildcard searches are not supported for lookup params (`ids`, `names`, `symbols`).
  * Cache/Update Frequency:
    * Every 60 seconds for Public API.
    * Every 45 seconds for Pro API (Analyst, Lite, Pro, Enterprise).
</Note>


# Crypto Treasury Holdings by Coin ID
Source: https://docs.coingecko.com/v3.0.1/reference/companies-public-treasury

v3.0.1/reference/api-reference/coingecko-demo.json get /{entity}/public_treasury/{coin_id}
This endpoint allows you **query public companies & governments' cryptocurrency holdings** by Coin ID

<Note>
  ### Note

  * The responses are sorted in descending order based on total holdings.
  * CoinGecko equivalent page: [https://www.coingecko.com/en/treasuries/bitcoin](https://www.coingecko.com/en/treasuries/bitcoin)
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Coin Historical Chart Data by Token Address
Source: https://docs.coingecko.com/v3.0.1/reference/contract-address-market-chart

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/contract/{contract_address}/market_chart
This endpoint allows you to **get the historical chart data including time in UNIX, price, market cap and 24hr volume based on asset platform and particular token contract address**

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint (`include platform = true`).
</Tip>

<Note>
  ### Note

  * You may leave the interval as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 2 - 90 days from current time = **hourly** data
    * above 90 days from current time = **daily** data (00:00 UTC)
  * Cache / Update Frequency:
    * Every 5 minutes for all the API plans.
    * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35). The cache will always expire at 00:40 UTC.
  * Access to historical data via the Public API (Demo plan) is **restricted to the past 365 days** only. To access the complete range of historical data, please subscribe to one of our [paid plans](https://www.coingecko.com/en/api/pricing) to obtain a Pro-API key.
</Note>


# Coin Historical Chart Data within Time Range by Token Address
Source: https://docs.coingecko.com/v3.0.1/reference/contract-address-market-chart-range

v3.0.1/reference/api-reference/coingecko-demo.json get /coins/{id}/contract/{contract_address}/market_chart/range
This endpoint allows you to **get the historical chart data within certain time range in UNIX along with price, market cap and 24hr volume based on asset platform and particular token contract address**

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint (`include platform = true`).
</Tip>

<Note>
  ### Note

  * You may leave the interval params as empty for automatic granularity:
    * 1 day from current time = **5-minutely** data
    * 1 day from any time (except current time) = **hourly** data
    * 2 - 90 days from any time = **hourly** data
    * above 90 days from any time = **daily** data (00:00 UTC)
  * Cache / Update Frequency:\
    Based on days range (all the API plans)
    * 1 day = 30 seconds cache
    * 2 -90 days = 30 minutes cache
    * 90 days = 12 hours cache
  * The last completed UTC day (00:00) is available 35 minutes after midnight on the next UTC day (00:35). The cache will always expire at 00:40 UTC.
  * Access to historical data via the Public API (Demo plan) is **restricted to the past 365 days** only. To access the complete range of historical data, please subscribe to one of our [paid plans](https://www.coingecko.com/en/api/pricing) to obtain a Pro-API key.
</Note>


# Crypto Global Market Data
Source: https://docs.coingecko.com/v3.0.1/reference/crypto-global

v3.0.1/reference/api-reference/coingecko-demo.json get /global
This endpoint allows you **query cryptocurrency global data including active cryptocurrencies, markets, total crypto market cap and etc**

<Note>
  ### Note

  * Cache / Update Frequency: every 10 minutes for all the API plans.
</Note>


# Derivatives Exchanges List with Data
Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-exchanges

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives/exchanges
This endpoint allows you to **query all the derivatives exchanges with related data (ID, name, open interest, ...) on CoinGecko**

<Tip>
  ### Tips

  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Derivatives Exchange Data by ID
Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-exchanges-id

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives/exchanges/{id}
This endpoint allows you to **query the derivatives exchange's related data (ID, name, open interest, ...) based on the exchanges' ID**

<Tip>
  ### Tips

  * For `include_tickers` param, you may change the value to either `all` to include all the tickers or `unexpired` to include unexpired tickers in the responses. You may leave it blank to omit the tickers data.
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 30 seconds for all the API plans.
</Note>


# Derivatives Exchanges List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-exchanges-list

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives/exchanges/list
This endpoint allows you to **query all the derivatives exchanges with ID and name on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of exchanges for other endpoints that contain params like `id` (derivatives exchange's ID)
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Derivatives Tickers List
Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-tickers

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives
This endpoint allows you to **query all the tickers from derivatives exchanges on CoinGecko**

<Note>
  ### Note

  * Data for `open_interest` and `volume_24h` in the endpoint responses are in USD.
  * Cache / Update Frequency: every 30 seconds for all the API plans.
</Note>


# Supported Dexes List by Network (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/dexes-list

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/dexes
This endpoint allows you to **query all the supported decentralized exchanges (DEXs) based on the provided network on GeckoTerminal**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of DEXs with DEX ID for other endpoints that contain params like `dex`.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>


# Endpoint Overview
Source: https://docs.coingecko.com/v3.0.1/reference/endpoint-overview



<Note>
  ### Notes

  Any exclusive endpoints for Pro-API users (any paid plan subscribers) will not be included here.

  For a full list of endpoints, please visit [Pro API Documentation](/reference/endpoint-overview) instead.
</Note>

## CoinGecko Endpoints: Coins

| Endpoint                                                                                           | Description                                                                                                                                                                            |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [/ping](/v3.0.1/reference/ping-server)                                                             | Check the API server status                                                                                                                                                            |
| [/simple/price](/v3.0.1/reference/simple-price)                                                    | Query the prices of one or more coins by using their unique Coin API IDs                                                                                                               |
| [/simple/token\_price/\{id}](/v3.0.1/reference/simple-token-price)                                 | Query the prices of one or more coins by using their unique Coin API IDs                                                                                                               |
| [/simple/supported\_vs\_currencies](/v3.0.1/reference/simple-supported-currencies)                 | Query all the supported currencies on CoinGecko                                                                                                                                        |
| [/coins/list](/v3.0.1/reference/coins-list)                                                        | Query all the supported coins on CoinGecko with coins ID, name and symbol                                                                                                              |
| [/coins/markets](/v3.0.1/reference/coins-markets)                                                  | Query all the supported coins with price, market cap, volume and market related data                                                                                                   |
| [/coins/\{id}](/v3.0.1/reference/coins-id)                                                         | Query all the metadata (image, websites, socials, description, contract address, etc.) from the CoinGecko coin page based on a particular coin ID                                      |
| [/coins/\{id}/tickers](/v3.0.1/reference/coins-id-tickers)                                         | Query the coin tickers on both centralized exchange (CEX) and decentralized exchange (DEX) based on a particular coin ID                                                               |
| [/coins/\{id}/history](/v3.0.1/reference/coins-id-history)                                         | Query the historical data (price, market cap, 24hr volume, ...) at a given date for a coin based on a particular coin ID                                                               |
| [/coins/\{id}/market\_chart](/v3.0.1/reference/coins-id-market-chart)                              | Get the historical chart data of a coin including time in UNIX, price, market cap and 24hr volume based on particular coin ID                                                          |
| [/coins/\{id}/market\_chart/range](/v3.0.1/reference/coins-id-market-chart-range)                  | Get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hr volume based on particular coin ID                                     |
| [/coins-id-ohlc](/v3.0.1/reference/coins-id-ohlc)                                                  | Get the OHLC chart (Open, High, Low, Close) of a coin based on particular coin ID                                                                                                      |
| [/coins/../contract/..](/v3.0.1/reference/coins-contract-address)                                  | Query all the metadata (image, websites, socials, description, contract address, etc.) from the CoinGecko coin page based on an asset platform and a particular token contract address |
| [/coins/../contract/../market\_chart](/v3.0.1/reference/contract-address-market-chart)             | Get the historical chart data including time in UNIX, price, market cap and 24hr volume based on asset platform and particular token contract address                                  |
| [/coins/../contract/../market\_chart/range](/v3.0.1/reference/contract-address-market-chart-range) | Get the historical chart data within certain time range in UNIX along with price, market cap and 24hr volume based on asset platform and particular token contract address             |
| [/coins/categories/list](/v3.0.1/reference/coins-categories-list)                                  | Query all the coins categories on CoinGecko                                                                                                                                            |
| [/coins/categories](/v3.0.1/reference/coins-categories)                                            | Query all the coins categories with market data (market cap, volume, ...) on CoinGecko                                                                                                 |

## CoinGecko Endpoints: NFT

| Endpoint                                                        | Description                                                                                                                             |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| [/nfts/list](/v3.0.1/reference/nfts-list)                       | Query all supported NFTs with ID, contract address, name, asset platform ID and symbol on CoinGecko                                     |
| [/nfts/..](/v3.0.1/reference/nfts-id)                           | Query all the NFT data (name, floor price, 24hr volume, ...) based on the NFT collection ID                                             |
| [/nfts/../contract/..](/v3.0.1/reference/nfts-contract-address) | Query all the NFT data (name, floor price, 24hr volume, ...) based on the NFT collection contract address and respective asset platform |

## CoinGecko Endpoints: Exchanges & Derivatives

| Endpoint                                                                      | Description                                                                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [/exchanges](/v3.0.1/reference/exchanges)                                     | Query all the supported exchanges with exchanges' data (ID, name, country, ...) that have active trading volumes on CoinGecko |
| [/exchanges/list](/v3.0.1/reference/exchanges-list)                           | Query all the exchanges with ID and name                                                                                      |
| [/exchanges/\{id}](/v3.0.1/reference/exchanges-id)                            | Query exchange's data (name, year established, country, ...), exchange volume in BTC and tickers based on exchange's ID       |
| [/exchanges/\{id}/tickers](/v3.0.1/reference/exchanges-id-tickers)            | Query exchange's tickers based on exchange's ID                                                                               |
| [/exchanges/\{id}/volume\_chart](/v3.0.1/reference/exchanges-id-volume-chart) | Query the historical volume chart data with time in UNIX and trading volume data in BTC based on exchange's ID                |
| [/derivatives](/v3.0.1/reference/derivatives-tickers)                         | Query all the tickers from derivatives exchanges on CoinGecko                                                                 |
| [/derivatives/exchanges](/v3.0.1/reference/derivatives-exchanges)             | Query all the derivatives exchanges with related data (ID, name, open interest, ...) on CoinGecko                             |
| [/derivatives/exchanges/\{id}](/v3.0.1/reference/derivatives-exchanges-id)    | Query the derivatives exchange's related data (ID, name, open interest, ...) based on the exchanges' ID                       |
| [/derivatives/exchanges/list](/v3.0.1/reference/derivatives-exchanges-list)   | Query all the derivatives exchanges with ID and name on CoinGecko                                                             |

## CoinGecko Endpoints: Public Treasuries

| Endpoint                                                                        | Description                                                                               |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [/\{entity}/public\_treasury/\{coin\_id}](/reference/companies-public-treasury) | Query public companies & governments' cryptocurrency holdings by coin ID                  |
| [/public\_treasury/\{entity\_id}](/reference/public-treasury-entity)            | Query public companies & governments' cryptocurrency holdings by entity ID                |
| [/entities/list](/reference/entities-list)                                      | Query all the supported entities on CoinGecko with entities ID, name, symbol, and country |

## CoinGecko Endpoints: General

| Endpoint                                                                       | Description                                                                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| [/exchange\_rates](/v3.0.1/reference/exchange-rates)                           | Query BTC exchange rates with other currencies                                                                     |
| [/asset\_platforms](/v3.0.1/reference/asset-platforms-list)                    | Query all the asset platforms (blockchain networks) on CoinGecko                                                   |
| [/token\_lists/\{asset\_platform\_id}/all.json](/v3.0.1/reference/token-lists) | Get full list of tokens of a blockchain network (asset platform) that is supported by Ethereum token list standard |
| [/search](/v3.0.1/reference/search-data)                                       | Search for coins, categories and markets listed on CoinGecko                                                       |
| [/search/trending](/v3.0.1/reference/trending-search)                          | Query trending search coins, NFTs and categories on CoinGecko in the last 24 hours                                 |
| [/global](/v3.0.1/reference/crypto-global)                                     | Query cryptocurrency global data including active cryptocurrencies, markets, total crypto market cap and etc.      |
| [/global/decentralized\_finance\_defi](/v3.0.1/reference/global-defi)          | Query cryptocurrency global decentralized finance (DeFi) data including DeFi market cap, trading volume            |

## Onchain DEX Endpoints (GeckoTerminal)

| Endpoint                                                                                 | Description                                                                                                                                                              |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [/onchain/simple/networks/../token\_price/..](/v3.0.1/reference/onchain-simple-price)    | Get token price based on the provided token contract address on a network                                                                                                |
| [/onchain/networks](/v3.0.1/reference/networks-list)                                     | Query all the supported networks on GeckoTerminal                                                                                                                        |
| [/onchain/networks/../dexes](/v3.0.1/reference/dexes-list)                               | Query all the supported decentralized exchanges (DEXs) based on the provided network on GeckoTerminal                                                                    |
| [/onchain/networks/trending\_pools](/v3.0.1/reference/trending-pools-list)               | Query all the trending pools across all networks on GeckoTerminal                                                                                                        |
| [/onchain/networks/../trending\_pools](/v3.0.1/reference/trending-pools-network)         | Query the trending pools based on the provided network                                                                                                                   |
| [/onchain/networks/../pools/..](/v3.0.1/reference/pool-address)                          | Query the specific pool based on the provided network and pool address                                                                                                   |
| [/onchain/networks/../pools/multi/..](/v3.0.1/reference/pools-addresses)                 | Query multiple pools based on the provided network and pool address                                                                                                      |
| [/onchain/networks/../pools](/v3.0.1/reference/top-pools-network)                        | Query all the top pools based on the provided network                                                                                                                    |
| [/onchain/networks/../dexes/../pools](/v3.0.1/reference/top-pools-dex)                   | Query all the top pools based on the provided network and decentralized exchange (DEX)                                                                                   |
| [/onchain/networks/../new\_pools](/v3.0.1/reference/latest-pools-network)                | Query all the latest pools based on provided network                                                                                                                     |
| [/onchain/networks/new\_pools](/v3.0.1/reference/latest-pools-list)                      | Query all the latest pools across all networks on GeckoTerminal                                                                                                          |
| [/onchain/search/pools](/v3.0.1/reference/search-pools)                                  | Search for pools on a network                                                                                                                                            |
| [/onchain/networks/../tokens/../pools](/v3.0.1/reference/top-pools-contract-address)     | Query top pools based on the provided token contract address on a network                                                                                                |
| [/onchain/networks/../tokens/..](/v3.0.1/reference/token-data-contract-address)          | Query specific token data based on the provided token contract address on a network                                                                                      |
| [/onchain/networks/../tokens/multi/..](/v3.0.1/reference/tokens-data-contract-addresses) | Query multiple tokens data based on the provided token contract addresses on a network                                                                                   |
| [/onchain/networks/../tokens/../info](/v3.0.1/reference/token-info-contract-address)     | Query token metadata (name, symbol, CoinGecko ID, image, socials, websites, description, etc.) based on a provided token contract address on a network                   |
| [/onchain/networks/../pools/../info](/v3.0.1/reference/pool-token-info-contract-address) | Query pool metadata (base and quote token details, image, socials, websites, description, contract address, etc.) based on a provided pool contract address on a network |
| [/onchain/tokens/info\_recently\_updated](/v3.0.1/reference/tokens-info-recent-updated)  | Query 100 most recently updated tokens info across all networks on GeckoTerminal                                                                                         |
| [/onchain/networks/../pools/../ohlcv/..](/v3.0.1/reference/pool-ohlcv-contract-address)  | Get the OHLCV chart (Open, High, Low, Close, Volume) of a pool based on the provided pool address on a network                                                           |
| [/onchain/networks/../pools/../trades](/v3.0.1/reference/pool-trades-contract-address)   | Query the last 300 trades in the past 24 hours based on the provided pool address                                                                                        |

⚡️ Need Real-time Data Streams? Try [WebSocket API](https://docs.coingecko.com/websocket)

<a href="/websocket">
  <Frame>
    <img src="https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=2c88f667113256b6285720c468fb53a1" noZoom data-og-width="2400" width="2400" data-og-height="470" height="470" data-path="images/wss-banner-2.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=280&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=d2eafb93fcd670d5df221d617fd6f6a7 280w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=560&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=24f635622a42c0ae03695cc940112699 560w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=840&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=82ef1c05b6f45d6d8ec0bcef0f19d49a 840w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=1100&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=b119e8746bb1a78b759e6d94d96b7c8b 1100w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=1650&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=95797e7366c7f280e3e4b570b6db2b49 1650w, https://mintcdn.com/coingecko/VlaOc2UnIs8mj72v/images/wss-banner-2.png?w=2500&fit=max&auto=format&n=VlaOc2UnIs8mj72v&q=85&s=2f120e8a31b5793213494d4ae2d46fb3 2500w" />
  </Frame>
</a>

With WebSocket, you can now stream ultra-low latency, real-time prices, trades, and OHLCV chart data. <br />
Subscribe to our [paid API plan](https://www.coingecko.com/en/api/pricing) (Analyst plan & above) to access WebSocket and REST API data delivery methods.


# Entities List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/entities-list

v3.0.1/reference/api-reference/coingecko-demo.json get /entities/list
This endpoint allows you to **query all the supported entities on CoinGecko with entities ID, name, symbol, and country**

<Note>
  ### Note

  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# BTC-to-Currency Exchange Rates
Source: https://docs.coingecko.com/v3.0.1/reference/exchange-rates

v3.0.1/reference/api-reference/coingecko-demo.json get /exchange_rates
This endpoint allows you to **query BTC exchange rates with other currencies**

<Tip>
  ### Tips

  * You may use this endpoint to convert the response data, which is originally in BTC, to other currencies.
</Tip>

<Note>
  ### Note

  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Exchanges List with data
Source: https://docs.coingecko.com/v3.0.1/reference/exchanges

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges
This endpoint allows you to **query all the supported exchanges with exchanges' data (ID, name, country, ...) that have active trading volumes on CoinGecko**

<Tip>
  ### Tips

  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * All the exchanges in the responses are the exchanges with active trading volume on CoinGecko, any inactive or deactivated exchanges will be removed from the list.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Exchange Data by ID
Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-id

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/{id}
This endpoint allows you to **query exchange's data (name, year established, country, ...), exchange volume in BTC and top 100 tickers based on exchange's ID**

<Warning>
  ### Notice

  * Please note that the `trade_volume_24h_btc_normalized` data field will no longer be supported by our API starting on June 15, 2025. Please refer to [changelog](/changelog#may-2025) for more details.
</Warning>

<Note>
  ### Note

  * The exchange volume in the response is provided in BTC. To convert it to other currencies, please use [/exchange\_rates](/v3.0.1/reference/exchange-rates) endpoint.
  * For derivatives (e.g. bitmex, binance\_futures), to get derivatives exchanges data, please go to [/derivatives/exchange/\{id}](/v3.0.1/reference/derivatives-exchanges-id) endpoint.
  * Tickers are limited to 100 items, to get more tickers, please go to [/exchanges/\{id}/tickers](/v3.0.1/reference/exchanges-id-tickers) endpoint.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Exchange Tickers by ID
Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-id-tickers

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/{id}/tickers
This endpoint allows you to **query exchange's tickers based on exchange's ID**

<Note>
  ### Note

  * Responses are paginated and limited to 100 tickers per page. You may specify the page number using the `page` params to retrieve the tickers accordingly.
  * `order=base_target` sorts tickers by `base` symbol, then `target` symbol, in lexicographical order (`0 -> 9`, followed by `a -> z`).\
    This sorting method ensures stable pagination results, minimizing cases where cached responses might otherwise cause duplicate or missing tickers across paginated pages.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Exchange Volume Chart by ID
Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-id-volume-chart

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/{id}/volume_chart
This endpoint allows you to **query the historical volume chart data with time in UNIX and trading volume data in BTC based on exchange's ID**

<Note>
  ### Note

  * You can use this endpoint to query the historical volume chart data of **derivatives exchanges** as well.
  * The exchange volume in the response is provided in BTC. To convert it to other currencies, please use [/exchange\_rates](/v3.0.1/reference/exchange-rates) endpoint.
  * Data granularity is automatic (cannot be adjusted):
    * 1 day = 10-minutely
    * 7, 14 days = hourly
    * 30 days & above = daily
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# Exchanges List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-list

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/list
This endpoint allows you to **query all the exchanges with ID and name**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of exchanges including **derivatives exchanges** for other endpoints that contain params like `id`(exchange ID).
</Tip>

<Note>
  ### Note

  * There is no pagination required for this endpoint.
  * Cache / Update Frequency:  every 5 minutes for all the API plans.
</Note>


# Global DeFi Market Data
Source: https://docs.coingecko.com/v3.0.1/reference/global-defi

v3.0.1/reference/api-reference/coingecko-demo.json get /global/decentralized_finance_defi
This endpoint allows you **query top 100 cryptocurrency global decentralized finance (DeFi) data including DeFi market cap, trading volume**



# New Pools List
Source: https://docs.coingecko.com/v3.0.1/reference/latest-pools-list

v3.0.1/reference/api-reference/onchain-demo.json get /networks/new_pools
This endpoint allows you to **query all the latest pools across all networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/explore/new-crypto-pools](https://www.geckoterminal.com/explore/new-crypto-pools)
</Note>


# New Pools by Network
Source: https://docs.coingecko.com/v3.0.1/reference/latest-pools-network

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/new_pools
This endpoint allows you to **query all the latest pools based on provided network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * This endpoint includes the newly created pools in the past 48 hours.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/explore/new-crypto-pools/solana](https://www.geckoterminal.com/explore/new-crypto-pools/solana)
</Note>


# Supported Networks List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/networks-list

v3.0.1/reference/api-reference/onchain-demo.json get /networks
This endpoint allows you to **query all the supported networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of networks with network ID for other endpoints that contain params like `network`.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>


# NFTs Collection Data by Contract Address
Source: https://docs.coingecko.com/v3.0.1/reference/nfts-contract-address

v3.0.1/reference/api-reference/coingecko-demo.json get /nfts/{asset_platform_id}/contract/{contract_address}
This endpoint allows you to **query all the NFT data (name, floor price, 24hr volume ...) based on the NFT collection contract address and respective asset platform**

<Tip>
  ### Tips

  * You may also obtain the asset platform id and contract address through [/nfts/list](/v3.0.1/reference/nfts-list) endpoint.
</Tip>

<Note>
  ### Note

  * Solana NFT & Art Blocks are not supported for this endpoint, please use [/nfts/\{id}](/v3.0.1/reference/nfts-id) endpoint instead.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# NFTs Collection Data by ID
Source: https://docs.coingecko.com/v3.0.1/reference/nfts-id

v3.0.1/reference/api-reference/coingecko-demo.json get /nfts/{id}
This endpoint allows you to **query all the NFT data (name, floor price, 24hr volume ...) based on the NFT collection ID**

<Note>
  ### Note

  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>


# NFTs List (ID Map)
Source: https://docs.coingecko.com/v3.0.1/reference/nfts-list

v3.0.1/reference/api-reference/coingecko-demo.json get /nfts/list
This endpoint allows you to **query all supported NFTs with ID, contract address, name, asset platform ID and symbol on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of NFTs for other endpoints that contain params like `id` (NFT collection's id) as well as `asset_platform_id` and `contract_address`.
  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * The responses are paginated to 100 items.
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Token Price by Token Addresses
Source: https://docs.coingecko.com/v3.0.1/reference/onchain-simple-price

v3.0.1/reference/api-reference/onchain-demo.json get /simple/networks/{network}/token_price/{addresses}
This endpoint allows you to **get token price based on the provided token contract address on a network**

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
    * If you require `market_cap_usd` to return FDV value (as seen in [GeckoTerminal.com](https://www.geckoterminal.com/)) when market cap data is unavailable, please specify this parameter `mcap_fdv_fallback=true`.
  * The returned price currency is in USD.
  * Addresses not found in GeckoTerminal will be ignored.
  * This endpoint allows querying **up to 30 contract addresses** per request.
  * When using this endpoint, GeckoTerminal's routing decides the best pool for token price. The price source may change based on liquidity and pool activity. For full control over the price, you may use [`/networks/{network}/pools/{address}`](/v3.0.1/reference/pool-address) endpoint by providing a specific pool address.
  * Cache/Update Frequency: every 60 seconds.
</Note>


# Check API server status
Source: https://docs.coingecko.com/v3.0.1/reference/ping-server

v3.0.1/reference/api-reference/coingecko-demo.json get /ping
This endpoint allows you to **check the API server status**

<Note>
  ### Note

  * You can also go to [status.coingecko.com](https://status.coingecko.com/) to check the API server status and further maintenance notices.
</Note>


# Specific Pool Data by Pool Address
Source: https://docs.coingecko.com/v3.0.1/reference/pool-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools/{address}
This endpoint allows you to **query the specific pool based on the provided network and pool address**

<Note>
  ### Note

  * Address not found in GeckoTerminal will be ignored.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * `locked_liquidity_percentage` will be updated on daily basis.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens.
  * Pools on a bonding curve (e.g. non-graduated pools from launchpads) will return `launchpad_details` object with their graduation status and migration details.
  * Cache/Update Frequency: every 60 seconds.
</Note>


# Pool OHLCV chart by Pool Address
Source: https://docs.coingecko.com/v3.0.1/reference/pool-ohlcv-contract-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools/{pool_address}/ohlcv/{timeframe}
This endpoint allows you to **get the OHLCV chart (Open, High, Low, Close, Volume) of a pool based on the provided pool address on a network**

<Tip>
  ### Tips

  * You may use this endpoint to query the historical price and volume of a token.
  * You may select the timeframe with its respective aggregate to get the intended OHLCV data (e.g. `minute?aggregate=15` for 15 minutes OHLCV).
</Tip>

<Note>
  ### Note

  * This endpoint uses epoch/unix format for its timestamp. Example: `1708850449`.
  * [Paid plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan & above) can access data from **September 2021 to the present**, depending on when the pool started tracking on GeckoTerminal.
    * If no earlier data is available, an empty response will be returned.
    * Each API call can only retrieve data for a **maximum range of 6 months**. To fetch older data, use the `before_timestamp` parameter to query in multiple requests.
  * Pools with more than 2 tokens are not yet supported for this endpoint.
  * Each OHLCV array (under "ohlcv\_list") consists of 6 elements in the following order:
    * Timestamp: The epoch/unix timestamp representing the start of the time interval.
    * Open: The opening price of the asset at the beginning of the interval.
    * High: The highest price reached during the interval.
    * Low: The lowest price reached during the interval.
    * Close: The price of the asset at the end of the interval.
    * Volume: The total trading volume of the asset during the interval.
  * **Skipped Intervals**: To ensure concise and relevant data, specific timeframe intervals (e.g. minutely) with no recorded swaps are **excluded** from the response.
    * Higher granularity timeframes (e.g. 1 minute) are more likely to skip intervals due to periods of inactivity, while lower granularity timeframes (e.g. daily) are less affected.
  * For `include_empty_intervals` param:
    * When `false` (default): Only intervals with trade data are returned.
    * When `true`: All requested intervals are returned, those with no trade data are populated as follows:
      * OHLC (Open, High, Low, Close) are all set to the Close price of the previous interval.
        * *O = H = L = C = previous Close*
      * Volume (V) is set to 0, reflecting no trade activity.
  * Cache/Update frequency: every 60 seconds.
</Note>


# Pool Tokens Info by Pool Address
Source: https://docs.coingecko.com/v3.0.1/reference/pool-token-info-contract-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools/{pool_address}/info
This endpoint allows you to **query pool metadata (base and quote token details, image, socials, websites, description, contract address, etc.) based on a provided pool contract address on a network**

<Tip>
  ### Tips

  * If you would like to query pool data such as price, transactions, volume and etc. You can go to this endpoint [`/networks/{network}/pools/{address}`](/v3.0.1/reference/pool-address) instead.
  * Cache/Update frequency: every 60 seconds.
  * Learn more about GT score [here](https://support.coingecko.com/hc/en-us/articles/38381394237593-What-is-GT-Score-How-is-GT-Score-calculated).
  * Metadata (image, websites, description, socials) may be sourced on-chain and is not vetted by the CoinGecko team. If you wish to get metadata reviewed by CoinGecko team, you may use the following endpoints:
    * [Coin Data by ID](/v3.0.1/reference/coins-id)
    * [Coin Data by Token Address](/v3.0.1/reference/coins-contract-address)
</Tip>

<Note>
  ### Note

  * `holders` data is currently in Beta, with ongoing improvements to data quality, coverage, and update frequency.
    * Supported chains include: Solana, EVM (Ethereum, Polygon, BNB, Arbitrum, Optimism, Base), Sui, TON, and Ronin.
    * `distribution_percentage` coverage:
      * Solana: `top_10`, `11_20`, `21_40`, `rest`
      * Other chains: `top_10`, `11_30`, `31_50`, `rest`
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
</Note>


# Past 24 Hour Trades by Pool Address
Source: https://docs.coingecko.com/v3.0.1/reference/pool-trades-contract-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools/{pool_address}/trades
This endpoint allows you to **query the last 300 trades in the past 24 hours based on the provided pool address**

<Note>
  ### Note

  * Cache/Update Frequency: every 60 seconds.
</Note>


# Multiple Pools Data by Pool Addresses
Source: https://docs.coingecko.com/v3.0.1/reference/pools-addresses

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools/multi/{addresses}
This endpoint allows you to **query multiple pools based on the provided network and pool address**

<Note>
  ### Note

  * Addresses not found in GeckoTerminal will be ignored.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * This endpoint allows querying **up to 30 contract addresses** per request.
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include ` params will be included under the "included" key at the top level.
  * `locked_liquidity_percentage` will be updated on daily basis.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens.
  * Pools on a bonding curve (e.g. non-graduated pools from launchpads) will return `launchpad_details` object with their graduation status and migration details.
  * Cache/Update Frequency: every 60 seconds.
</Note>


# Crypto Treasury Holdings by Entity ID
Source: https://docs.coingecko.com/v3.0.1/reference/public-treasury-entity

v3.0.1/reference/api-reference/coingecko-demo.json get /public_treasury/{entity_id}
This endpoint allows you **query public companies & governments' cryptocurrency holdings** by Entity ID

<Note>
  ### Note

  * CoinGecko equivalent page: [https://www.coingecko.com/en/treasuries/bitcoin](https://www.coingecko.com/en/treasuries/bitcoin)
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>


# Search Queries
Source: https://docs.coingecko.com/v3.0.1/reference/search-data

v3.0.1/reference/api-reference/coingecko-demo.json get /search
This endpoint allows you to **search for coins, categories and markets listed on CoinGecko**

<Note>
  ### Note

  * The responses are sorted in descending order by market cap.
  * Cache / Update Frequency: every 15 minutes for all the API plans.
</Note>


# Search Pools
Source: https://docs.coingecko.com/v3.0.1/reference/search-pools

v3.0.1/reference/api-reference/onchain-demo.json get /search/pools
This endpoint allows you to **search for pools on a network**

<Tip>
  ### Tips

  * You may use this endpoint to search for query such as pool contract address, token contract address or token symbol. The endpoint will return matching pools as response.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
</Note>


# Coin Price by IDs
Source: https://docs.coingecko.com/v3.0.1/reference/simple-price

v3.0.1/reference/api-reference/coingecko-demo.json get /simple/price
This endpoint allows you to **query the prices of one or more coins by using their unique Coin API IDs**

<Tip>
  ### Tips

  * You may obtain the coin ID (API ID) via several ways:
    * refers to respective coin page and find 'API ID'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint.
    * refers to Google Sheets [here](https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit?usp=sharing).
  * You can retrieve specific coins using their unique `ids`, `names`, or `symbols`.
  * You may flag to include more data such as market cap, 24hr volume, 24hr change, last updated time etc.
  * To verify if a price is stale, you may flag `include_last_updated_at=true` in your request to obtain the latest updated time. Alternatively, you may flag `include_24hr_change=true` to determine if it returns a `null` value.
</Tip>

<Note>
  ### Note

  * You may cross-check the price on [CoinGecko](https://www.coingecko.com) and learn more about our price methodology [here](https://www.coingecko.com/en/methodology).
  * When multiple lookup params are provided, the following priority order is applied: `ids` (highest) > `names` > `symbols` (lowest).
  * When searching by `name`, you need to URL-encode any spaces (e.g. "Binance Coin" becomes "Binance%20Coin").
  * The `include_tokens=all` param is exclusively for use with the `symbols` lookup and is limited to maximum of 50 symbols per request.
  * Wildcard searches are not supported for lookup params (`ids`, `names`, `symbols`).
  * Cache/Update Frequency: every 60 seconds for Public API.
    * Every 20 seconds for [Pro-API](https://www.coingecko.com/en/api/pricing) (Analyst, Lite, Pro, Enterprise).
</Note>


# Supported Currencies List
Source: https://docs.coingecko.com/v3.0.1/reference/simple-supported-currencies

v3.0.1/reference/api-reference/coingecko-demo.json get /simple/supported_vs_currencies
This endpoint allows you to **query all the supported currencies on CoinGecko**

<Tip>
  ### Tips

  * You may use this endpoint to query the list of currencies for other endpoints that contain params like `vs_currencies`.
</Tip>

<Note>
  ### Note

  * Cache/Update Frequency: every 60 seconds for Public API.
</Note>


# Coin Price by Token Addresses
Source: https://docs.coingecko.com/v3.0.1/reference/simple-token-price

v3.0.1/reference/api-reference/coingecko-demo.json get /simple/token_price/{id}
This endpoint allows you to **query one or more token prices using their token contract addresses**

<Tip>
  ### Tips

  * You may obtain the asset platform and contract address via several ways:
    * refers to respective coin page and find 'contract address'.
    * refers to [`/coins/list`](/v3.0.1/reference/coins-list) endpoint (`include platform = true`).
  * You may flag to include more data such as market cap, 24hr volume, 24hr change, last updated time etc.
</Tip>

<Note>
  ### Note

  * The endpoint returns the global average price of the coin that is aggregated across all active exchanges on CoinGecko.
  * You may cross-check the price on [CoinGecko](https://www.coingecko.com) and learn more about our price methodology [here](https://www.coingecko.com/en/methodology).
  * Cache/Update Frequency: every 60 seconds for Public API.
    * Every 20 seconds for [Pro-API](https://www.coingecko.com/en/api/pricing) (Analyst, Lite, Pro, Enterprise).
</Note>


# Token Data by Token Address
Source: https://docs.coingecko.com/v3.0.1/reference/token-data-contract-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/tokens/{address}
This endpoint allows you to **query specific token data based on the provided token contract address on a network**

<Tip>
  ### Tips

  * You may add values such as `top_pools` in the include param to include top pools along with the pools information.
  * If you would like to query token information such as socials, websites, description and etc. You can go to this endpoint [`/networks/{network}/tokens/{address}/info`](/v3.0.1/reference/token-info-contract-address) instead.
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens. (requires `include=top_pools`)
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
  * Cache/Update frequency: every 60 seconds.
</Note>


# Token Info by Token Address
Source: https://docs.coingecko.com/v3.0.1/reference/token-info-contract-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/tokens/{address}/info
This endpoint allows you to **query token metadata (name, symbol,  CoinGecko ID, image, socials, websites, description, etc.) based on a provided token contract address on a network**

<Tip>
  ### Tips

  * If you would like to query token data such as decimals, total supply, price and etc. You can go to this endpoint [`/networks/{network}/tokens/{address}`](/v3.0.1/reference/token-data-contract-address) instead.
  * Cache/Update frequency: every 60 seconds.
  * Learn more about GT score [here](https://support.coingecko.com/hc/en-us/articles/38381394237593-What-is-GT-Score-How-is-GT-Score-calculated).
  * Metadata (image, websites, description, socials) may be sourced on-chain and is not vetted by the CoinGecko team. If you wish to get metadata reviewed by CoinGecko team, you may use the following endpoints:
    * [Coin Data by ID](/v3.0.1/reference/coins-id)
    * [Coin Data by Token Address](/v3.0.1/reference/coins-contract-address)
</Tip>

<Note>
  ### Note

  * `holders` data is currently in Beta, with ongoing improvements to data quality, coverage, and update frequency.
    * Supported chains include: Solana, EVM (Ethereum, Polygon, BNB, Arbitrum, Optimism, Base), Sui, TON, and Ronin.
    * `distribution_percentage` coverage:
      * Solana: `top_10`, `11_20`, `21_40`, `rest`
      * Other chains: `top_10`, `11_30`, `31_50`, `rest`
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
</Note>


# Token Lists by Asset Platform ID
Source: https://docs.coingecko.com/v3.0.1/reference/token-lists

v3.0.1/reference/api-reference/coingecko-demo.json get /token_lists/{asset_platform_id}/all.json
This endpoint allows you to **get full list of tokens of a blockchain network (asset platform) that is supported by [Ethereum token list standard](https://tokenlists.org/)**

<Note>
  ### Note

  * Cache/Update Frequency: 5 minutes.
  * A token will only be included in the list if the contract address is added by CoinGecko team. If you identified any missing token, you may submit a request [here](https://support.coingecko.com/hc/en-us/requests/new).
</Note>


# Tokens Data by Token Addresses
Source: https://docs.coingecko.com/v3.0.1/reference/tokens-data-contract-addresses

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/tokens/multi/{addresses}
This endpoint allows you to **query multiple tokens data based on the provided token contract addresses on a network**

<Tip>
  ### Tips

  * You may add values such as `top_pools` in the include param to include top pools along with the pools information.
  * If you would like to query token information such as socials, websites, description and etc. You can go to this endpoint [`/networks/{network}/tokens/{address}/info`](/v3.0.1/reference/token-info-contract-address) instead.
</Tip>

<Note>
  ### Note

  * Addresses not found in GeckoTerminal.com will be ignored.
  * This endpoint allows querying **up to 30 contract addresses** per request.
  * The endpoint will only return the first top pool for each token.
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Market Cap can be verified by and sourced from CoinGecko, and the number may be higher than FDV as it may include Market Cap of tokens issued on other blockchain network.
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * Set `include_composition=true` to surface the balance and liquidity value of the pool's base and quote tokens. (requires `include=top_pools`)
  * For tokens on a bonding curve (i.e. non-graduated tokens from launchpads), the response will include a `launchpad_details` object containing their graduation status and details.
  * Cache/Update frequency: every 60 seconds.
</Note>


# Most Recently Updated Tokens List
Source: https://docs.coingecko.com/v3.0.1/reference/tokens-info-recent-updated

v3.0.1/reference/api-reference/onchain-demo.json get /tokens/info_recently_updated
This endpoint allows you to **query 100 most recently updated tokens info of a specific network or across all networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may add values such as network in the include param to include network along with the updated tokens list.
</Tip>

<Note>
  ### Note

  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * Cache/Update frequency: every 60 seconds.
</Note>


# Top Pools by Token Address
Source: https://docs.coingecko.com/v3.0.1/reference/top-pools-contract-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/tokens/{token_address}/pools
This endpoint allows you to **query top pools based on the provided token contract address on a network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

<Note>
  ### Note

  * The ranking of the top 20 pools is established by evaluating their liquidity and trading activity to identify the most liquid ones. This ranking is determined through a combination of two key factors: liquidity (`reserve_in_usd`) and 24-Hour Trading Volume (`volume_usd`).
  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
</Note>


# Top Pools by Dex
Source: https://docs.coingecko.com/v3.0.1/reference/top-pools-dex

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/dexes/{dex}/pools
This endpoint allows you to **query all the top pools based on the provided network and decentralized exchange (DEX)**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/base/uniswap-v3-base/pools?sort=-24h\_transactions](https://www.geckoterminal.com/base/uniswap-v3-base/pools?sort=-24h_transactions)
</Note>


# Top Pools by Network
Source: https://docs.coingecko.com/v3.0.1/reference/top-pools-network

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools
This endpoint allows you to **query all the top pools based on the provided network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/solana/pools?sort=-24h\_transactions](https://www.geckoterminal.com/solana/pools?sort=-24h_transactions)
</Note>


# Trending Pools List
Source: https://docs.coingecko.com/v3.0.1/reference/trending-pools-list

v3.0.1/reference/api-reference/onchain-demo.json get /networks/trending_pools
This endpoint allows you to **query all the trending pools across all networks on GeckoTerminal**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com](https://www.geckoterminal.com)
</Note>


# Trending Pools by Network
Source: https://docs.coingecko.com/v3.0.1/reference/trending-pools-network

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/trending_pools
This endpoint allows you to **query the trending pools based on the provided network**

<Tip>
  ### Tips

  * You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

<Note>
  ### Note

  * If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/base/pools](https://www.geckoterminal.com/base/pools)
</Note>


# Trending Search List
Source: https://docs.coingecko.com/v3.0.1/reference/trending-search

v3.0.1/reference/api-reference/coingecko-demo.json get /search/trending
This endpoint allows you **query trending search coins, NFTs and categories on CoinGecko in the last 24 hours**

<Note>
  ### Note

  * The endpoint currently supports:
    * Top 15 trending coins (sorted by the most popular user searches)
    * Top 7 trending NFTs (sorted by the highest percentage change in floor prices)
    * Top 5 trending categories (sorted by the most popular user searches)
  * Cache / Update Frequency: every 10 minutes for all the API plans.
</Note>


# CGSimplePrice
Source: https://docs.coingecko.com/websocket/cgsimpleprice

Subscribe to receive real-time price updates for tokens, as seen on CoinGecko.com

This Websocket channel allows you to subscribe to real-time updates of price changes for token.

* Lookup by Coin ID
* It will return price & market data of the top pool of the specified token

**Update Frequency**: as fast as \~10s, for large cap and actively traded coins.

### Data Payload

|      | Field                             | Type    | Description                                                                                          | Example                |
| ---- | --------------------------------- | ------- | ---------------------------------------------------------------------------------------------------- | ---------------------- |
| `c`  | `channel_type`                    | string  | Indicates the type of channel subscribed to.                                                         | C1                     |
| `i`  | `coin_id`                         | string  | Identifier of the coins. Check full list of IDs [here](https://api.coingecko.com/api/v3/coins/list). | `ethereum`, `usd-coin` |
| `p`  | `usd_price`                       | string  | Current token price in USD.                                                                          | 3639.78228844745       |
| `pp` | `usd_price_24h_change_percentage` | float   | Percentage change in token price over the last 24 hours.                                             | 3.566                  |
| `m`  | `usd_market_cap`                  | float   | Market capitalization in USD.                                                                        | 123                    |
| `v`  | `usd_24h_vol`                     | float   | 24-hour trading volume in USD.                                                                       | 31233333.33            |
| `t`  | `last_updated_at`                 | integer | Timestamp of the last data update in UNIX time.                                                      | 1709542750             |

**Tips**: The Websocket payload will use the value `null` when specific data is unavailable. Ensure your application is capable of handling null values for fields that may not always have data.

***

## 1. Establish Connection to Websocket

<CodeGroup>
  ```bash Bash theme={null}
  wss://stream.coingecko.com/v1?x_cg_pro_api_key=YOUR_KEY

  OR

  wss://stream.coingecko.com/v1  
  x-cg-pro-api-key: YOUR_KEY
  ```
</CodeGroup>

## 2. Subscribe to a specific channel - CGSimplePrice

**Input Example:**

<CodeGroup>
  ```json JSON theme={null}
  {"command":"subscribe","identifier":"{\"channel\":\"CGSimplePrice\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {"type":"confirm_subscription","identifier":"{\"channel\":\"CGSimplePrice\"}"}
  ```
</CodeGroup>

## 3. Stream CGSimplePrice

**Input Example:**

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"CGSimplePrice\"}","data":"{\"coin_id\":[\"ethereum\",\"bitcoin\"],\"action\":\"set_tokens\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
      "code": 2000,
      "message": "Subscription is successful for ethereum"
  }
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
      "c": "C1",
      "i": "ethereum",
      "m": 312938652962.8005,
      "p": 2591.080889351465,
      "pp": 1.3763793110454519,
      "t": 1747808150.269067,
      "v": 20460612214.801384
  }
  ```
</CodeGroup>

The output keys will be in random order.

## Tips:

### Un-subscribe to stop streaming CGSimplePrice data

**Input Example:** Unsubscribe for 1 specific token data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"CGSimplePrice\"}","data":"{\"coin_id\":[\"ethereum\"],\"action\":\"unset_tokens\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
      "code": 2000,
      "message": "Unsubscription is successful for ethereum"
  }
  ```
</CodeGroup>

**Input Example:** Unsubscribe from CGSimplePrice channel and all token data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"unsubscribe","identifier":"{\"channel\":\"CGSimplePrice\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
      "code": 2000,
      "message": "Unsubscription is successful for all tokens"
  }
  ```
</CodeGroup>


# WebSocket (Beta)
Source: https://docs.coingecko.com/websocket/index

CoinGecko API: Stream Real-Time Crypto Data with WebSockets

## Access Real-Time Crypto Data Instantly with CoinGecko WebSockets

In the fast-paced world of cryptocurrency, speed matters. Our official CoinGecko WebSocket API provides a dedicated, persistent connection for real-time data streaming, ensuring you receive critical market updates the moment they happen.

Move beyond traditional polling and embrace the power of instant data delivery for your trading bots, dashboards, and analytical applications.

<Tip>
  CoinGecko Websocket (Beta) is now available for [paid plan ](https://www.coingecko.com/en/api/pricing)customers (Analyst plan & above)!

  * For Analyst, Lite, Pro, and Pro+ self-serve customers, you will be eligible to access the following features, and stream real-time data by utilising your monthly API plan credits:
    * Max connections: 10 concurrent socket connections
    * Max subscriptions: 100 token or pool data subscription per channel, per socket
    * Channel Access: all 4 channels
    * Credit charge: 0.1 credit per response returned, deducting from monthly API plan credits

  We will gradually improve the Websocket and expand the feature limits. Please share your feedback and suggestion via this [survey form](https://forms.gle/gNE1Txc9FCV55s7ZA), or email soonaik\@coingecko\[dot]com
</Tip>

* For existing **Enterprise plan** clients who wish to unlock higher limits (max connections, max subscriptions, and lower credit charge), please contact your Customer Success Manager.

### Channel & Data Support

| Websocket Channel                                             | Channel Code | Details                                                                                                       |
| ------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------- |
| [OnchainSimpleTokenPrice](/websocket/onchainsimpletokenprice) | G1           | Subscribe to receive real-time price updates for tokens, as seen on GeckoTerminal.com                         |
| [CGSimplePrice](/websocket/cgsimpleprice)                     | C1           | Subscribe to receive real-time price updates for tokens, as seen on CoinGecko.com                             |
| [OnchainTrade](/websocket/wss-onchain-trade)                  | G2           | Subscribe to receive real-time transaction updates for pools, as seen on GeckoTerminal.com                    |
| [OnchainOHLCV](/websocket/wssonchainohlcv/)                   | G3           | Subscribe to receive real-time OHLCV (Open, High, Low, Close, Volume) for pools, as seen on GeckoTerminal.com |
| (More coming soon!)                                           |              |                                                                                                               |

<Note>
  ### **Notes**

  * **Real-Time Data**: Once subscribed, you will start receiving real-time data updates based on your subscriptions. The received data will be in JSON format and will contain the relevant information for the subscribed event.
  * **Close Connection:** When you're done receiving updates or want to close the WebSocket connection, you can gracefully close the connection.
  * **Security Considerations:** Ensure that you keep your Pro-API key secure and do not expose it publicly in your code or any public repositories.
</Note>

### Connection Handling

To provide you with the most reliable and efficient experience, please be aware of the following regarding our WebSocket connections:

1. **Connection Liveliness (Ping/Pong Mechanism):**
   * To ensure your connection remains active and healthy, we send a **"ping" signal every 10 seconds**.
   * If we **do not receive a "pong" response from your client within 20 seconds** of sending a ping, we will automatically disconnect the connection.
   * **Action Required (Client-Side)**: Your WebSocket client must be configured to respond to our ping messages with a pong. Most WebSocket libraries handle this automatically, but please verify your implementation to ensure it's sending pong responses. This is critical for maintaining your connection.
2. **Planned Disconnections (Deployments & Reboots):**
   * **Purpose**: From time to time, we will perform system reboots or deploy new versions of our service to implement updates, bug fixes, and improvements. These actions require a graceful restart of our servers.
   * **Impact**: During these periods, your active WebSocket connections might be temporarily disconnected.
   * **Action Required (Client-Side)**: It is essential that your application is designed to automatically attempt to re-establish the WebSocket connection if it detects a disconnection. Implementing an exponential backoff strategy for reconnection attempts is highly recommended to avoid overwhelming our servers during a widespread disconnection event.


# OnchainSimpleTokenPrice
Source: https://docs.coingecko.com/websocket/onchainsimpletokenprice

Subscribe to receive real-time price updates for tokens, as seen on GeckoTerminal.com

This Websocket channel allows you to subscribe to real-time updates of price changes for token.

* Lookup by Network + Token Address
* It will return price and market data of the top pool of the specified token

**Update Frequency**: as fast as 1s, for actively traded tokens.

### Data Payload

|      | Field                             | Type    | Description                                                                                                                | Example                                      |
| ---- | --------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `c`  | `channel_type`                    | string  | Indicates the type of channel subscribed to.                                                                               | G1                                           |
| `n`  | `network_id`                      | string  | Identifier of the blockchain network. Check full list of IDs [here](https://api.geckoterminal.com/api/v2/networks?page=1). | `eth`                                        |
| `ta` | `token_address`                   | string  | Contract address of the token on the blockchain.                                                                           | `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2` |
| `p`  | `usd_price`                       | float   | Current token price in USD.                                                                                                | 3639.78228844745                             |
| `pp` | `usd_price_24h_change_percentage` | float   | Percentage change in token price over the last 24 hours.                                                                   | 3.566                                        |
| `m`  | `usd_market_cap`                  | float   | Market capitalization in USD.                                                                                              | 123                                          |
| `v`  | `usd_24h_vol`                     | float   | 24-hour trading volume in USD.                                                                                             | 31233333.33                                  |
| `t`  | `last_updated_at`                 | integer | Timestamp of the last data update in UNIX time.                                                                            | 1709542750                                   |

**Tips**: The Websocket payload will use the value `null` when specific data is unavailable. Ensure your application is capable of handling null values for fields that may not always have data.

***

## 1. Establish Connection to Websocket

<CodeGroup>
  ```bash Bash theme={null}
  wss://stream.coingecko.com/v1?x_cg_pro_api_key=YOUR_KEY

  OR

  wss://stream.coingecko.com/v1  
  x-cg-pro-api-key: YOUR_KEY
  ```
</CodeGroup>

## 2. Subscribe to a specific channel - OnchainSimpleTokenPrice

**Input Example:**

<CodeGroup>
  ```json JSON theme={null}
  {"command":"subscribe","identifier":"{\"channel\":\"OnchainSimpleTokenPrice\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {"type":"confirm_subscription","identifier":"{\"channel\":\"OnchainSimpleTokenPrice\"}"}
  ```
</CodeGroup>

## 3. Stream OnchainSimpleTokenPrice data

**Input Example:**

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"OnchainSimpleTokenPrice\"}","data":"{\"network_id:token_addresses\":[\"bsc:0x55d398326f99059ff775485246999027b3197955\"],\"action\":\"set_tokens\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code": 2000,
    "message": "Subscription successful for bsc:0x55d398326f99059ff775485246999027b3197955"
  }
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "c": "G1",
    "n": "bsc",
    "ta": "0x55d398326f99059ff775485246999027b3197955",
    "p": 0.999457718373347,
    "pp": -0.009028866490825653,
    "m": 1317802988326.25,
    "v": 1476864199.38384,
    "t": 1737427063
  }
  ```
</CodeGroup>

The output keys will be in random order.

## Tips:

### Un-subscribe to stop streaming OnchainSimpleTokenPrice data

**Input Example:** Unsubscribe for 1 specific token data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"OnchainSimpleTokenPrice\"}","data":"{\"network_id:token_addresses\":[\"bsc:0x55d398326f99059ff775485246999027b3197955\"],\"action\":\"unset_tokens\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code":2000,
    "message":"Unsubscription is successful for bsc:0x55d398326f99059ff775485246999027b3197955"
  }
  ```
</CodeGroup>

**Input Example:** Unsubscribe from OnchainSimpleTokenPrice channel and all token data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"unsubscribe","identifier":"{\"channel\":\"OnchainSimpleTokenPrice\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code":2000,
    "message":"Unsubscription is successful for all tokens"
  }
  ```
</CodeGroup>


# OnchainTrade
Source: https://docs.coingecko.com/websocket/wss-onchain-trade

Subscribe to receive real-time transaction (trade/swap) updates for pools, as seen on GeckoTerminal.com

This Websocket channel allows you to subscribe to real-time updates of token trades of a pool.

* Lookup by Network + Pool Address
* It will return transaction type (buy/sell), tx hash, amount of token transacted, volume, and current price data of the specified pool.

**Update Frequency**: as fast as 0.1s, for actively traded pools.

**Tips**: use this Rest API endpoint [Top Pools by Token Address](/reference/top-pools-contract-address) to obtain contract address of the most liquid pool.

### Data Payload

|      | Field                     | Type    | Description                                                                                                                | Example                    |
| ---- | ------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `ch` | `channel_type`            | string  | Indicates the type of channel subscribed to.                                                                               | G2                         |
| `n`  | `network_id`              | string  | Identifier of the blockchain network. Check full list of IDs [here](https://api.geckoterminal.com/api/v2/networks?page=1). | eth                        |
| `pa` | `pool_address`            | string  | Contract address of the pool.                                                                                              | `0x88e6a0c2dd6fcb..3f5640` |
| `tx` | `tx_hash`                 | string  | transaction hash                                                                                                           | `0x0b8ac5a16c2d5a..4d422`  |
| `ty` | `type`                    | string  | type of transaction (`b` for buy or `s` for sell)                                                                          | b                          |
| `to` | `token_amount`            | float   | Amount of token transacted.                                                                                                | 100                        |
| `vo` | `volume_in_usd`           | float   | The transaction value in USD.                                                                                              | 1000                       |
| `pc` | `price_in_token_currency` | float   | Current token price in target token currency                                                                               | 3639.78228844745           |
| `pu` | `price_in_usd`            | float   | Current token price in USD                                                                                                 | 3.566                      |
| `t`  | `last_updated_at`         | integer | Timestamp of the last data update in UNIX time.                                                                            | 1752072129000              |

**Tips**: The Websocket payload will use the value `null` when specific data is unavailable. Ensure your application is capable of handling null values for fields that may not always have data.

***

## 1. Establish Connection to Websocket

<CodeGroup>
  ```bash Bash theme={null}
  wss://stream.coingecko.com/v1?x_cg_pro_api_key=YOUR_KEY

  OR

  wss://stream.coingecko.com/v1  
  x-cg-pro-api-key: YOUR_KEY
  ```
</CodeGroup>

## 2. Subscribe to a specific channel - OnchainTrade

**Input Example:**

<CodeGroup>
  ```json JSON theme={null}
  {"command":"subscribe","identifier":"{\"channel\":\"OnchainTrade\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {"type":"confirm_subscription","identifier":"{\"channel\":\"OnchainTrade\"}"}
  ```
</CodeGroup>

## 3. Stream OnchainTrade data

**Input Example:**

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"OnchainTrade\"}","data":"{\"network_id:pool_addresses\":[\"bsc:0x172fcd41e0913e95784454622d1c3724f546f849\"],\"action\":\"set_pools\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code": 2000,
    "message": "Subscription successful for bsc:0x172fcd41e0913e95784454622d1c3724f546f849"
  }
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "c": "G2",
    "n": "bsc",
    "pa": "0x172fcd41e0913e95784454622d1c3724f546f849",
    "tx": "0x3e71ee7da66000a5a92f13abd2ae95e0abc0bc828087d8dd210338fd262cf6c9",
    "ty": "b",
    "to": "1.51717616246451",
    "vo": "2.75413132131313",
    "pc": "0.000274100995437363"
    "pu": "3656.8970003075",
    "t": 1724927796000
  }
  ```
</CodeGroup>

The output keys will be in random order.

## Tips:

### Un-subscribe to stop streaming OnchainTrade data

**Input Example:** Unsubscribe for 1 specific pool data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"OnchainTrade\"}","data":"{\"network_id:pool_addresses\":[\"bsc:0x172fcd41e0913e95784454622d1c3724f546f849\"],\"action\":\"unset_pools\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code":2000,
    "message":"Unsubscription is successful for bsc:0x172fcd41e0913e95784454622d1c3724f546f849"
  }
  ```
</CodeGroup>

**Input Example:** Unsubscribe from OnchainTrade channel and all pools data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"unsubscribe","identifier":"{\"channel\":\"OnchainTrade\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code":2000,
    "message":"Unsubscription is successful for all pools"
  }
  ```
</CodeGroup>


# OnchainOHLCV
Source: https://docs.coingecko.com/websocket/wssonchainohlcv

Subscribe to receive real-time OHLCV updates for pools, as seen on GeckoTerminal.com

This Websocket channel allows you to subscribe to real-time OHLCV updates of a pool.

* Lookup by Network + Pool Address
* It will return **O**pen, **H**igh, **L**ow, **C**lose price and **V**olume data the specified pool.

**Update Frequency**: as fast as 1s, for actively traded pools.

**Tips**: use this Rest API endpoint [Top Pools by Token Address](https://docs.coingecko.com/reference/top-pools-contract-address#/) to obtain contract address of the most liquid pool.

<Note>
  ### **Notes**

  * Interval options: 1s / 1m / 5m / 1h / 2h / 4h / 8h
  * You may stream the pool ohlcv data based on `base` or `quote` token of a pool.
  * Please note that your subscription quota is based on the number of **unique data streams** you request. Each unique combination of an interval and token for a given pool is considered a **distinct subscription** and will count towards your max subscription limit.
</Note>

### Data Payload

|      | Field          | Type    | Description                                                                                                                | Example                    |
| ---- | -------------- | ------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `ch` | `channel_type` | string  | Indicates the type of channel subscribed to.                                                                               | G3                         |
| `n`  | `network_id`   | string  | Identifier of the blockchain network. Check full list of IDs [here](https://api.geckoterminal.com/api/v2/networks?page=1). | eth                        |
| `pa` | `pool_address` | string  | Contract address of the pool.                                                                                              | `0x88e6a0c2dd6fcb..3f5640` |
| `to` | `token`        | string  | `base` or `quote` token                                                                                                    | `base`                     |
| `i`  | `interval`     | string  | Interval or resolution of the candle: 1s / 1m / 5m / 1h / 2h / 4h / 8h                                                     | 1m                         |
| `o`  | `open`         | float   | Open price in USD                                                                                                          | 3539                       |
| `h`  | `high`         | float   | High price in USD                                                                                                          | 3541                       |
| `l`  | `low`          | float   | Low price in USD                                                                                                           | 3530                       |
| `c`  | `close`        | float   | Close price in USD                                                                                                         | 3531                       |
| `v`  | `volume`       | float   | Volume in USD                                                                                                              | 323333                     |
| `t`  | `timestamp`    | integer | Opening timestamp of candle interval                                                                                       | 1753803600                 |

**Tips**: The Websocket payload will use the value `null` when specific data is unavailable. Ensure your application is capable of handling null values for fields that may not always have data.

***

## 1. Establish Connection to Websocket

<CodeGroup>
  ```bash Bash theme={null}
  wss://stream.coingecko.com/v1?x_cg_pro_api_key=YOUR_KEY

  OR

  wss://stream.coingecko.com/v1  
  x-cg-pro-api-key: YOUR_KEY
  ```
</CodeGroup>

## 2. Subscribe to a specific channel - OnchainOHLCV

**Input Example:**

<CodeGroup>
  ```json JSON theme={null}
  {"command":"subscribe","identifier":"{\"channel\":\"OnchainOHLCV\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {"type":"confirm_subscription","identifier":"{\"channel\":\"OnchainOHLCV\"}"}
  ```
</CodeGroup>

## 3. Stream OnchainOHLCV data

**Input Example:** (1 minute interval and base token of a pool)

* `Interval` options: 1s / 1m / 5m / 1h / 2h / 4h / 8h
* You may stream the pool ohlcv data of 'base' or 'quote' `token`.

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"OnchainOHLCV\"}","data":"{\"network_id:pool_addresses\":[\"bsc:0x172fcd41e0913e95784454622d1c3724f546f849\"],\"interval\":\"1m\",\"token\":\"base\",\"action\":\"set_pools\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code": 2000,
    "message": "Subscription successful for bsc:0x172fcd41e0913e95784454622d1c3724f546f849:1m:base"
  }
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
      "c": 0.999727235252031,
      "ch": "G3",
      "h": 0.999974654065411,
      "i": "1m",
      "l": 0.999353212178554,
      "n": "bsc",
      "o": 0.999570907451071,
      "pa": "0x172fcd41e0913e95784454622d1c3724f546f849",
      "t": 1753886760,
      "to": "base",
      "v": 63932.29404921795
  }
  ```
</CodeGroup>

The output keys will be in random order.

## Tips:

### Un-subscribe to stop streaming OnchainOHLCV data

**Input Example:** Unsubscribe for 1 specific pool data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"message","identifier":"{\"channel\":\"OnchainOHLCV\"}","data":"{\"network_id:pool_addresses\":[\"eth:0xc7bbec68d12a0d1830360f8ec58fa599ba1b0e9b\"],\"interval\":\"1m\",\"token\":\"base\",\"action\":\"unset_pools\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code":2000,
    "message":"Unsubscription is successful for eth:0xc7bbec68d12a0d1830360f8ec58fa599ba1b0e9b:1m:base"
  }
  ```
</CodeGroup>

**Input Example:** Unsubscribe from OnchainOHLCV channel and all pools data:

<CodeGroup>
  ```json JSON theme={null}
  {"command":"unsubscribe","identifier":"{\"channel\":\"OnchainOHLCV\"}"}
  ```
</CodeGroup>

**Output Example**:

<CodeGroup>
  ```json JSON theme={null}
  {
    "code":2000,
    "message":"Unsubscription is successful for all pools"
  }
  ```
</CodeGroup>


