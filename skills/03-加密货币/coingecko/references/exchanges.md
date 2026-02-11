# Coingecko - Exchanges

**Pages:** 14

---

## Exchange Volume Chart by ID

**URL:** llms-txt#exchange-volume-chart-by-id

Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-id-volume-chart

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/{id}/volume_chart
This endpoint allows you to **query the historical volume chart data with time in UNIX and trading volume data in BTC based on exchange's ID**

* You can use this endpoint to query the historical volume chart data of **derivatives exchanges** as well.
  * The exchange volume in the response is provided in BTC. To convert it to other currencies, please use [/exchange\_rates](/v3.0.1/reference/exchange-rates) endpoint.
  * Data granularity is automatic (cannot be adjusted):
    * 1 day = 10-minutely
    * 7, 14 days = hourly
    * 30 days & above = daily
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>

---

## Derivatives Tickers List

**URL:** llms-txt#derivatives-tickers-list

Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-tickers

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives
This endpoint allows you to **query all the tickers from derivatives exchanges on CoinGecko**

* Data for `open_interest` and `volume_24h` in the endpoint responses are in USD.
  * Cache / Update Frequency: every 30 seconds for all the API plans.
</Note>

---

## 💼 Exchange Volume Chart within Time Range by ID

**URL:** llms-txt#💼-exchange-volume-chart-within-time-range-by-id

Source: https://docs.coingecko.com/reference/exchanges-id-volume-chart-range

reference/api-reference/coingecko-pro.json get /exchanges/{id}/volume_chart/range
This endpoint allows you to **query the historical volume chart data in BTC by specifying date range in UNIX based on exchange's ID**

* You can query the historical volume chart data of **derivatives exchanges** with this endpoint as well.
  * The data interval for this endpoint is fixed at daily.
  * The date range between `from` and `to` must be within 31 days.
  * Cache/Update Frequency: 5 minutes
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise)
</Note>

---

## Derivatives Exchange Data by ID

**URL:** llms-txt#derivatives-exchange-data-by-id

Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-exchanges-id

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives/exchanges/{id}
This endpoint allows you to **query the derivatives exchange's related data (ID, name, open interest, ...) based on the exchanges' ID**

* For `include_tickers` param, you may change the value to either `all` to include all the tickers or `unexpired` to include unexpired tickers in the responses. You may leave it blank to omit the tickers data.
</Tip>

* Cache / Update Frequency: every 30 seconds for all the API plans.
</Note>

---

## Supported Dexes List by Network (ID Map)

**URL:** llms-txt#supported-dexes-list-by-network-(id-map)

Source: https://docs.coingecko.com/v3.0.1/reference/dexes-list

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/dexes
This endpoint allows you to **query all the supported decentralized exchanges (DEXs) based on the provided network on GeckoTerminal**

* You may use this endpoint to query the list of DEXs with DEX ID for other endpoints that contain params like `dex`.
  * You may include values such as `page` to specify which page of responses you would like to show.
</Tip>

---

## Exchanges List with data

**URL:** llms-txt#exchanges-list-with-data

Source: https://docs.coingecko.com/v3.0.1/reference/exchanges

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges
This endpoint allows you to **query all the supported exchanges with exchanges' data (ID, name, country, ...) that have active trading volumes on CoinGecko**

* You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

* All the exchanges in the responses are the exchanges with active trading volume on CoinGecko, any inactive or deactivated exchanges will be removed from the list.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>

---

## Derivatives Exchanges List with Data

**URL:** llms-txt#derivatives-exchanges-list-with-data

Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-exchanges

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives/exchanges
This endpoint allows you to **query all the derivatives exchanges with related data (ID, name, open interest, ...) on CoinGecko**

* You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

* Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>

---

## Exchanges List (ID Map)

**URL:** llms-txt#exchanges-list-(id-map)

Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-list

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/list
This endpoint allows you to **query all the exchanges with ID and name**

* You may use this endpoint to query the list of exchanges including **derivatives exchanges** for other endpoints that contain params like `id`(exchange ID).
</Tip>

* There is no pagination required for this endpoint.
  * Cache / Update Frequency:  every 5 minutes for all the API plans.
</Note>

---

## 💼 Global Market Cap Chart Data

**URL:** llms-txt#💼-global-market-cap-chart-data

Source: https://docs.coingecko.com/reference/global-market-cap-chart

reference/api-reference/coingecko-pro.json get /global/market_cap_chart
This endpoint allows you to **query historical global market cap and volume data by number of days away from now**

* CoinGecko equivalent page: [https://www.coingecko.com/en/global-charts](https://www.coingecko.com/en/global-charts).
  * Data Granularity (auto):
    * 1 day from now = **hourly** data
    * 2 days & above from now = **daily** data
  * Exclusive for all Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
  * The last completed UTC day (00:00) is available 5 minutes after midnight on the next UTC day (00:05). The cache will **always expire at 00:05 UTC**. If you wish to get the latest daily data (00:00 UTC), you can make request at 00:05 UTC or later.
  * Cache / Update Frequency: every 1 minute.
</Note>

---

## 💼 NFTs List with Market Data

**URL:** llms-txt#💼-nfts-list-with-market-data

Source: https://docs.coingecko.com/reference/nfts-markets

reference/api-reference/coingecko-pro.json get /nfts/markets
This endpoint allows you to **query all the supported NFT collections with floor price, market cap, volume and market related data on CoinGecko**

* You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

* Cache / Update Frequency: every 5 minutes.
  * Exclusive for Paid Plan Subscribers (Analyst, Lite, Pro and Enterprise).
  * CoinGecko equivalent page: [https://www.coingecko.com/en/nft](https://www.coingecko.com/en/nft).
  * Some collection with low liquidity may not be ranked by Market Cap value, learn more [here](https://support.coingecko.com/hc/en-us/articles/37226121227545-What-is-NFT-Market-Cap). Sorting by Mcap ranking will first prioritise Market Cap value of liquid NFT collections, then followed by trading volume of illiquid NFT collections.
</Note>

---

## Exchange Tickers by ID

**URL:** llms-txt#exchange-tickers-by-id

Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-id-tickers

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/{id}/tickers
This endpoint allows you to **query exchange's tickers based on exchange's ID**

* Responses are paginated and limited to 100 tickers per page. You may specify the page number using the `page` params to retrieve the tickers accordingly.
  * `order=base_target` sorts tickers by `base` symbol, then `target` symbol, in lexicographical order (`0 -> 9`, followed by `a -> z`).\
    This sorting method ensures stable pagination results, minimizing cases where cached responses might otherwise cause duplicate or missing tickers across paginated pages.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>

---

## BTC-to-Currency Exchange Rates

**URL:** llms-txt#btc-to-currency-exchange-rates

Source: https://docs.coingecko.com/v3.0.1/reference/exchange-rates

v3.0.1/reference/api-reference/coingecko-demo.json get /exchange_rates
This endpoint allows you to **query BTC exchange rates with other currencies**

* You may use this endpoint to convert the response data, which is originally in BTC, to other currencies.
</Tip>

* Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>

---

## Exchange Data by ID

**URL:** llms-txt#exchange-data-by-id

Source: https://docs.coingecko.com/v3.0.1/reference/exchanges-id

v3.0.1/reference/api-reference/coingecko-demo.json get /exchanges/{id}
This endpoint allows you to **query exchange's data (name, year established, country, ...), exchange volume in BTC and top 100 tickers based on exchange's ID**

<Warning>
  ### Notice

* Please note that the `trade_volume_24h_btc_normalized` data field will no longer be supported by our API starting on June 15, 2025. Please refer to [changelog](/changelog#may-2025) for more details.
</Warning>

* The exchange volume in the response is provided in BTC. To convert it to other currencies, please use [/exchange\_rates](/v3.0.1/reference/exchange-rates) endpoint.
  * For derivatives (e.g. bitmex, binance\_futures), to get derivatives exchanges data, please go to [/derivatives/exchange/\{id}](/v3.0.1/reference/derivatives-exchanges-id) endpoint.
  * Tickers are limited to 100 items, to get more tickers, please go to [/exchanges/\{id}/tickers](/v3.0.1/reference/exchanges-id-tickers) endpoint.
  * When `dex_pair_format=symbol`, the DEX pair `base` and `target` are displayed in symbol format (e.g. `WETH`, `USDC`) instead of as contract addresses.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>

---

## Derivatives Exchanges List (ID Map)

**URL:** llms-txt#derivatives-exchanges-list-(id-map)

Source: https://docs.coingecko.com/v3.0.1/reference/derivatives-exchanges-list

v3.0.1/reference/api-reference/coingecko-demo.json get /derivatives/exchanges/list
This endpoint allows you to **query all the derivatives exchanges with ID and name on CoinGecko**

* You may use this endpoint to query the list of exchanges for other endpoints that contain params like `id` (derivatives exchange's ID)
</Tip>

* Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>

---
