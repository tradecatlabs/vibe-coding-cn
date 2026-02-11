# Coingecko - Contract

**Pages:** 1

---

## NFTs Collection Data by Contract Address

**URL:** llms-txt#nfts-collection-data-by-contract-address

Source: https://docs.coingecko.com/v3.0.1/reference/nfts-contract-address

v3.0.1/reference/api-reference/coingecko-demo.json get /nfts/{asset_platform_id}/contract/{contract_address}
This endpoint allows you to **query all the NFT data (name, floor price, 24hr volume ...) based on the NFT collection contract address and respective asset platform**

* You may also obtain the asset platform id and contract address through [/nfts/list](/v3.0.1/reference/nfts-list) endpoint.
</Tip>

* Solana NFT & Art Blocks are not supported for this endpoint, please use [/nfts/\{id}](/v3.0.1/reference/nfts-id) endpoint instead.
  * Cache / Update Frequency: every 60 seconds for all the API plans.
</Note>

---
