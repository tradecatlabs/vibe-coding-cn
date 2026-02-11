# Coingecko - Market Data

**Pages:** 3

---

## 💼 NFTs Collection Historical Chart Data by ID

**URL:** llms-txt#💼-nfts-collection-historical-chart-data-by-id

Source: https://docs.coingecko.com/reference/nfts-id-market-chart

reference/api-reference/coingecko-pro.json get /nfts/{id}/market_chart
This endpoint allows you **query historical market data of a NFT collection, including floor price, market cap, and 24hr volume, by number of days away from now**

* Data Granularity (auto):
    * 1-14 days from now = **5-minutely** data
    * 15 days & above from now = **daily** data (00:00 UTC)
  * Cache/Update Frequency: every 5 minutes
  * The last completed UTC day (00:00) is available 5 minutes after midnight on the next UTC day (00:05).
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>

---

## 💼 NFTs Collection Historical Chart Data by Contract Address

**URL:** llms-txt#💼-nfts-collection-historical-chart-data-by-contract-address

Source: https://docs.coingecko.com/reference/nfts-contract-address-market-chart

reference/api-reference/coingecko-pro.json get /nfts/{asset_platform_id}/contract/{contract_address}/market_chart
This endpoint allows you **query historical market data of a NFT collection, including floor price, market cap, and 24hr volume, by number of days away from now based on the provided contract address**

* This endpoint doesn't support Solana NFT and Art Blocks, please use [/nfts/\{id}/market\_chart](/reference/nfts-id-market-chart) endpoint instead.
  * Data Granularity (auto):
    * 1-14 days from now = **5-minutely** data
    * 15 days & above from now = **daily** data (00:00 UTC)
  * Cache/Update Frequency: every 5 minutes
  * The last completed UTC day (00:00) is available 5 minutes after midnight on the next UTC day (00:05).
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>

---

## 💼 NFTs Collection Tickers by ID

**URL:** llms-txt#💼-nfts-collection-tickers-by-id

Source: https://docs.coingecko.com/reference/nfts-id-tickers

reference/api-reference/coingecko-pro.json get /nfts/{id}/tickers
This endpoint allows you to **query the latest floor price and 24hr volume of a NFT collection, on each NFT marketplace, e.g. OpenSea and LooksRare**

* Cache/Update Frequency: every 30 seconds.
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
</Note>

---
