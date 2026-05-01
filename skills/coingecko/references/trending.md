# Coingecko - Trending

**Pages:** 2

---

## Trending Pools by Network

**URL:** llms-txt#trending-pools-by-network

Source: https://docs.coingecko.com/v3.0.1/reference/trending-pools-network

v3.0.1/reference/api-reference/onchain-demo.json get /networks/{network}/trending_pools
This endpoint allows you to **query the trending pools based on the provided network**

* You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

* If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com/base/pools](https://www.geckoterminal.com/base/pools)
</Note>

---

## Trending Pools List

**URL:** llms-txt#trending-pools-list

Source: https://docs.coingecko.com/v3.0.1/reference/trending-pools-list

v3.0.1/reference/api-reference/onchain-demo.json get /networks/trending_pools
This endpoint allows you to **query all the trending pools across all networks on GeckoTerminal**

* You may include values such as `page` to specify which page of responses you would like to show.
  * For more flexibility in retrieving an exact list of pools that match your specific needs, consider using the [/pools/megafilter](https://docs.coingecko.com/reference/pools-megafilter) endpoint (available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers \[Analyst plan or above].)
</Tip>

* If the token's market cap is not verified by the team, the API response will return `null` for its market cap value, even though it has a displayed value on GeckoTerminal, which might not be accurate as it often matches the Fully Diluted Valuation (FDV).
  * Attributes specified in the `include` param will be returned under the top-level "included" key.
  * This endpoint returns up to 20 pools per page. Use the `page` param to navigate more results.
  * `page`: Pagination beyond 10 pages is available for [Paid Plan](https://www.coingecko.com/en/api/pricing) subscribers (Analyst plan or above).
  * Cache/Update frequency: every 60 seconds.
  * GeckoTerminal equivalent page (example): [https://www.geckoterminal.com](https://www.geckoterminal.com)
</Note>

---
