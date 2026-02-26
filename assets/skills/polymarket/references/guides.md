# Polymarket - Guides

**Pages:** 3

---

## Example

**URL:** llms-txt#example

* **\[Event]** Where will Barron Trump attend College?
  * **\[Market]** Will Barron attend Georgetown?
  * **\[Market]** Will Barron attend NYU?
  * **\[Market]** Will Barron attend UPenn?
  * **\[Market]** Will Barron attend Harvard?
  * **\[Market]** Will Barron attend another college?

---

## How to Fetch Markets

**URL:** llms-txt#how-to-fetch-markets

**Contents:**
- Overview
- 1. Fetch by Slug
  - How to Extract the Slug
  - API Endpoints
  - Examples
- 2. Fetch by Tags
  - Discover Available Tags
  - Using Tags in Market Requests
  - Additional Tag Filtering
- 3. Fetch All Active Markets

Source: https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide

<Tip>Both the getEvents and getMarkets are paginated. See [pagination section](#pagination) for details.</Tip>
This guide covers the three recommended approaches for fetching market data from the Gamma API, each optimized for different use cases.

There are three main strategies for retrieving market data:

1. **By Slug** - Best for fetching specific individual markets or events
2. **By Tags** - Ideal for filtering markets by category or sport
3. **Via Events Endpoint** - Most efficient for retrieving all active markets

**Use Case:** When you need to retrieve a specific market or event that you already know about.

Individual markets and events are best fetched using their unique slug identifier. The slug can be found directly in the Polymarket frontend URL.

### How to Extract the Slug

From any Polymarket URL, the slug is the path segment after `/event/` or `/market/`:

**For Events:** [GET /events/slug/{slug}](/api-reference/events/list-events)

**For Markets:** [GET /markets/slug/{slug}](/api-reference/markets/list-markets)

**Use Case:** When you want to filter markets by category, sport, or topic.

Tags provide a powerful way to categorize and filter markets. You can discover available tags and then use them to filter your market requests.

### Discover Available Tags

**General Tags:** [GET /tags](/api-reference/tags/list-tags)

**Sports Tags & Metadata:** [GET /sports](/api-reference/sports/get-sports-metadata-information)

The `/sports` endpoint returns comprehensive metadata for sports including tag IDs, images, resolution sources, and series information.

### Using Tags in Market Requests

Once you have tag IDs, you can use them with the `tag_id` parameter in both markets and events endpoints.

**Markets with Tags:** [GET /markets](/api-reference/markets/list-markets)

**Events with Tags:** [GET /events](/api-reference/events/list-events)

### Additional Tag Filtering

* Use `related_tags=true` to include related tag markets
* Exclude specific tags with `exclude_tag_id`

## 3. Fetch All Active Markets

**Use Case:** When you need to retrieve all available active markets, typically for broader analysis or market discovery.

The most efficient approach is to use the `/events` endpoint and work backwards, as events contain their associated markets.

**Events Endpoint:** [GET /events](/api-reference/events/list-events)

**Markets Endpoint:** [GET /markets](/api-reference/markets/list-markets)

* `order=id` - Order by event ID
* `ascending=false` - Get newest events first
* `closed=false` - Only active markets
* `limit` - Control response size
* `offset` - For pagination

This approach gives you all active markets ordered from newest to oldest, allowing you to systematically process all available trading opportunities.

For large datasets, use pagination with `limit` and `offset` parameters:

* `limit=50` - Return 50 results per page
* `offset=0` - Start from the beginning (increment by limit for subsequent pages)

**Pagination Examples:**

```bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
https://polymarket.com/event/fed-decision-in-october?tid=1758818660485
                            ↑
                  Slug: fed-decision-in-october
```

Example 2 (unknown):
```unknown
***

## 2. Fetch by Tags

**Use Case:** When you want to filter markets by category, sport, or topic.

Tags provide a powerful way to categorize and filter markets. You can discover available tags and then use them to filter your market requests.

### Discover Available Tags

**General Tags:** [GET /tags](/api-reference/tags/list-tags)

**Sports Tags & Metadata:** [GET /sports](/api-reference/sports/get-sports-metadata-information)

The `/sports` endpoint returns comprehensive metadata for sports including tag IDs, images, resolution sources, and series information.

### Using Tags in Market Requests

Once you have tag IDs, you can use them with the `tag_id` parameter in both markets and events endpoints.

**Markets with Tags:** [GET /markets](/api-reference/markets/list-markets)

**Events with Tags:** [GET /events](/api-reference/events/list-events)
```

Example 3 (unknown):
```unknown
### Additional Tag Filtering

You can also:

* Use `related_tags=true` to include related tag markets
* Exclude specific tags with `exclude_tag_id`

***

## 3. Fetch All Active Markets

**Use Case:** When you need to retrieve all available active markets, typically for broader analysis or market discovery.

The most efficient approach is to use the `/events` endpoint and work backwards, as events contain their associated markets.

**Events Endpoint:** [GET /events](/api-reference/events/list-events)

**Markets Endpoint:** [GET /markets](/api-reference/markets/list-markets)

### Key Parameters

* `order=id` - Order by event ID
* `ascending=false` - Get newest events first
* `closed=false` - Only active markets
* `limit` - Control response size
* `offset` - For pagination

### Examples
```

Example 4 (unknown):
```unknown
This approach gives you all active markets ordered from newest to oldest, allowing you to systematically process all available trading opportunities.

### Pagination

For large datasets, use pagination with `limit` and `offset` parameters:

* `limit=50` - Return 50 results per page
* `offset=0` - Start from the beginning (increment by limit for subsequent pages)

**Pagination Examples:**
```

---

## Market Orders

**URL:** llms-txt#market-orders

**Contents:**
- Video Walkthrough
- Placing a Market Order

Once you've [signed up](../get-started/how-to-signup) and [deposited funds](../get-started/how-to-deposit), you're ready to start trading on Polymarket. Here's a step-by-step guide to get you started.

<iframe width="560" height="315" src="https://www.youtube.com/embed/1lFgkHLqo28?si=i7e61-roRsOVeRMW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

## Placing a Market Order

\_Before trading, you'll want to visit the [markets page](https://polymarket.com/markets) to find a market that interests you.

<Steps>
  <Steps.Step>
    ### [Choose a market](https://polymarket.com/markets)

Locate the 'buy' modal, on the right side of the screen. Click the outcome you want to buy (usually Yes or No), then enter the dollar amount you wish to invest.
  </Steps.Step>

<Steps.Step>
    ### Buy shares

Click **Buy** and confirm the transaction in your wallet. Once your trade goes through, you'll receive a notification confirming its success.

<Tip>Congrats, you're officially a Polymarket trader!</Tip>
  </Steps.Step>

<Steps.Step>
    ### Share your bet slip

You'll also see a bet slip to share on social media. We love sending \$\$\$ to traders who post their trades on Twitter and tag us!
  </Steps.Step>
</Steps>

Simple, right? If you think you've got the hang of it, it's time to learn about more advanced trading and order types. [Limit Orders](../trading/limit-orders/).

---
