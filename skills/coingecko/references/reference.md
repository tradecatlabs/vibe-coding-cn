# Coingecko - Reference

**Pages:** 9

---

## 💼 API Usage

**URL:** llms-txt#💼-api-usage

Source: https://docs.coingecko.com/reference/api-usage

reference/api-reference/coingecko-pro.json get /key
This endpoint allows you to **monitor your account's API usage, including rate limits, monthly total credits, remaining credits, and more**

For a more comprehensive overview of your API usage, please log in to [https://www.coingecko.com/en/developers/dashboard](https://www.coingecko.com/en/developers/dashboard).
</Note>

---

## Supported Networks List (ID Map)

**URL:** llms-txt#supported-networks-list-(id-map)

Source: https://docs.coingecko.com/v3.0.1/reference/networks-list

v3.0.1/reference/api-reference/onchain-demo.json get /networks
This endpoint allows you to **query all the supported networks on GeckoTerminal**

* You may use this endpoint to query the list of networks with network ID for other endpoints that contain params like `network`.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

---

## Check API server status

**URL:** llms-txt#check-api-server-status

Source: https://docs.coingecko.com/v3.0.1/reference/ping-server

v3.0.1/reference/api-reference/coingecko-demo.json get /ping
This endpoint allows you to **check the API server status**

* You can also go to [status.coingecko.com](https://status.coingecko.com/) to check the API server status and further maintenance notices.
</Note>

---

## Supported Currencies List

**URL:** llms-txt#supported-currencies-list

Source: https://docs.coingecko.com/v3.0.1/reference/simple-supported-currencies

v3.0.1/reference/api-reference/coingecko-demo.json get /simple/supported_vs_currencies
This endpoint allows you to **query all the supported currencies on CoinGecko**

* You may use this endpoint to query the list of currencies for other endpoints that contain params like `vs_currencies`.
</Tip>

* Cache/Update Frequency: every 60 seconds for Public API.
</Note>

---

## Asset Platforms List (ID Map)

**URL:** llms-txt#asset-platforms-list-(id-map)

Source: https://docs.coingecko.com/v3.0.1/reference/asset-platforms-list

v3.0.1/reference/api-reference/coingecko-demo.json get /asset_platforms
This endpoint allows you to **query all the asset platforms on CoinGecko**

* You may use this endpoint to query the list of asset platforms for other endpoints that contain params like `id` or`ids`(asset platforms).
  * You may include NFT at the `filter` params to get the list of NFT-support asset platforms on CoinGecko.
</Tip>

---

## Past 24 Hour Trades by Pool Address

**URL:** llms-txt#past-24-hour-trades-by-pool-address

Source: https://docs.coingecko.com/v3.0.1/reference/pool-trades-contract-address

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools/{pool_address}/trades
This endpoint allows you to **query the last 300 trades in the past 24 hours based on the provided pool address**

* Cache/Update Frequency: every 60 seconds.
</Note>

---

## Entities List (ID Map)

**URL:** llms-txt#entities-list-(id-map)

Source: https://docs.coingecko.com/v3.0.1/reference/entities-list

v3.0.1/reference/api-reference/coingecko-demo.json get /entities/list
This endpoint allows you to **query all the supported entities on CoinGecko with entities ID, name, symbol, and country**

* Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>

---

## Top Pools by Network

**URL:** llms-txt#top-pools-by-network

Source: https://docs.coingecko.com/v3.0.1/reference/top-pools-network

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/pools
This endpoint allows you to **query all the top pools based on the provided network**

* You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

* If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/solana/pools?sort=-24h\_transactions](https://www.geckoterminal.com/solana/pools?sort=-24h_transactions)
</Note>

---

## Top Pools by Dex

**URL:** llms-txt#top-pools-by-dex

Source: https://docs.coingecko.com/v3.0.1/reference/top-pools-dex

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/dexes/{dex}/pools
This endpoint allows you to **query all the top pools based on the provided network and decentralized exchange (DEX)**

* You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

* If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/base/uniswap-v3-base/pools?sort=-24h\_transactions](https://www.geckoterminal.com/base/uniswap-v3-base/pools?sort=-24h_transactions)
</Note>

---
