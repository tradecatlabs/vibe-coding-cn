# Coingecko - Nfts

**Pages:** 2

---

## NFTs Collection Data by ID

**URL:** llms-txt#nfts-collection-data-by-id

Source: https://docs.coingecko.com/v3.0.1/reference/nfts-id

v3.0.1/reference/api-reference/coingecko-demo.json get /nfts/{id}
This endpoint allows you to **query all the NFT data (name, floor price, 24hr volume ...) based on the NFT collection ID**

* Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>

---

## NFTs List (ID Map)

**URL:** llms-txt#nfts-list-(id-map)

Source: https://docs.coingecko.com/v3.0.1/reference/nfts-list

v3.0.1/reference/api-reference/coingecko-demo.json get /nfts/list
This endpoint allows you to **query all supported NFTs with ID, contract address, name, asset platform ID and symbol on CoinGecko**

* You may use this endpoint to query the list of NFTs for other endpoints that contain params like `id` (NFT collection's id) as well as `asset_platform_id` and `contract_address`.
  * You may include values such as `per_page` and `page` to specify how many results you would like to show in the responses per page and which page of responses you would like to show.
</Tip>

* The responses are paginated to 100 items.
  * Cache / Update Frequency: every 5 minutes for all the API plans.
</Note>

---
