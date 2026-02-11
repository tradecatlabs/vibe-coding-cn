# Coingecko - Authentication

**Pages:** 3

---

## Authentication (Public/Demo)

**URL:** llms-txt#authentication-(public/demo)

**Contents:**
- CoinGecko API Authentication Method
- API Key Usage Credits

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

---

## Authentication (Pro API)

**URL:** llms-txt#authentication-(pro-api)

**Contents:**
- CoinGecko API Authentication Method
- 🔥 Accessing Onchain DEX data
- API Key Usage Credits

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

---

## Setting Up Your API Key

**URL:** llms-txt#setting-up-your-api-key

**Contents:**
- 1. Creating a new API Key
- 2. Making API Request
- 3. Edit or Delete API Key
- 4. API Usage Report
- 5. Others
  - Call Consumption Alerts
  - Overage Option (Beta)

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

---
