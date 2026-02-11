# Hummingbot - Configuration

**Pages:** 24

---

## 

**URL:** https://hummingbot.org/dashboard/config-10.png

---

## 1.6.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/1.6.0/

**Contents:**
- Release Notes - Version 1.6.0¶
- Config Management Refactoring¶
- New Gateway DEX Connector: UniswapLP¶
- Restored Strategy: Uniswap-V3 LP¶
- New Gateway DEX Connector: Quickswap¶
- New Spot and Perpetual Exchange Connectors: Bitmex¶
- New Spot Exchange Connector: Latoken¶
- Developer Updates¶
  - Hummingbot changes¶
  - Gateway changes¶

Released on July 26, 2022

Install via Docker: Linux | Windows | macOS | Raspberry Pi

Binary builds are no longer supported. Docker and Source are now the only supported methods of install.

We are very excited to ship the July 2022 Hummingbot release (v1.6.0) today!

In 5428, Hummingbot's configuration management system was significantly overhauled. The new approach uses pydantic models to define the configuration maps. Aside from built-in validation functionality, this approach also allows the automatic generation of JSON schemas which is a big first step in the direction of decoupling the bot from its interface. Another major step in that direction is significantly restricting the use of global variables when dealing with the global config map (now renamed to client config map) and the AllConnectorSettings class.

The approach to storing and retrieving secure configs has also been refactored. We no longer store secure configs in the client config map (former global config map). Those are only stored in the Security class (which is still unfortunately accessed globally). In addition, the secure values are no longer stored separate from non-secure configs — they are both part of the same config map and stored in the same yaml file.

When returning users log in to version 1.6.0, they will be prompted to enter their password to migrate their old configurations to the new configuration schema. If the configuration is successful, users will see the screen below"

As this new version will automatically migrate any old configuration files due to the config management refactoring, we strongly advise users to create a backup of the config files first prior to updating the bots to 1.6.0. The migration process may also take some time or may encounter issues so it's advisable to implement the update at a more convenient period. Lastly, make sure to remove any existing scripts you have and download instead the latest helper scripts (create.sh, update.sh) from our installation page.

We are excited to re-introduce a connector for Uniswap that supports the Uniswap V3 AI, enabling users to add and remove concentrated liquidity ranges.

See the Uniswap documentation for more information.

Because Gateway now supports the UniswapLP connector, we have restored the Uniswap V3 LP strategy that allows users to create a bot that adds concentrated liquidity ranges and dynamically adjusts them given flucutations in market price and volatility.

See the uniswap-lp-v3 documentation for more information.

Quickswap is the leading AMM DEX on the Polygon Network.

See the quickswap documentation for more information.

Bitmex is a cryptocurrency exchange and derivative trading platform. It is owned and operated by HDR Global Trading Limited, which is registered in the Seychelles.

Latoken is a rapidly growing crypto exchange focusing on liquidity for new tokens.

See the latoken documentation for more information.

---

## Configuration - Hummingbot

**URL:** https://hummingbot.org/gateway/configuration/

**Contents:**
- Configuration
- Configuration Overview¶
  - Configuration Structure¶
  - Root Configuration¶
  - Server Configuration¶
  - Chain Configuration¶
  - Connector Configuration¶
    - Example: Jupiter Configuration¶
  - Network Configuration¶
    - Example: Solana mainnet-beta Configuration¶

Gateway uses a modular configuration system that allows you to customize various aspects of its operation. This guide explains the configuration structure and how to modify it to suit your needs.

Gateway's configuration system consists of YAML files located in the /conf directory, along with JSON files for tokens and pools organized by chain and connector.

The initial configuration files are created automatically using the default templates in /src/templates when you run the setup script during installation.

The /conf/ folder contains the following types of configuration files:

The root.yml file serves as the entry point for Gateway's configuration system. It defines which configuration files are loaded and their corresponding schema files.

This file tells Gateway:

The server.yml file controls the core Gateway server behavior, including ports, logging, and security settings.

Chain configuration files (e.g., /conf/chains/solana.yml) now contain only the default network and wallet settings for each blockchain.

When you connect a wallet using gateway connect, it automatically becomes the defaultWallet for that chain. The defaultNetwork determines which network configuration Gateway uses by default for that chain.

Network-specific configurations are now stored in separate files under /conf/chains/{chain}/{network}.yml

Connector configuration files (e.g., /conf/connectors/jupiter.yml) define settings specific to each DEX connector, including slippage tolerance, routing preferences, and API configurations.

Configuration Options Explained:

slippagePct: Maximum acceptable price slippage for trades. If the execution price deviates more than this percentage from the quoted price, the transaction will fail.

priorityLevel: Controls transaction priority on Solana. Higher priority levels result in faster confirmation but cost more in fees. Set to veryHigh for time-sensitive trades.

maxLamports: Caps the maximum priority fee to prevent excessive costs during network congestion. 1,000,000 lamports = 0.001 SOL.

onlyDirectRoutes: When true, restricts swaps to direct pools only (no intermediate tokens). This can reduce price impact but may result in worse pricing or failed routes for less liquid pairs.

restrictIntermediateTokens: When true, only routes through major tokens (SOL, USDC, USDT) as intermediates. This increases reliability and reduces price impact risks.

apiKey: Optional API key for Jupiter's paid tier. The free tier (lite-api) is suitable for most users, while the paid tier offers higher rate limits and additional features.

Network configuration files (e.g., /conf/chains/solana/mainnet-beta.yml) contain the detailed settings for each blockchain network, including RPC endpoints and transaction parameters.

You can view the current configuration for any network using Gateway commands:

To update any network setting, use gateway config [namespace] update:

To change the RPC node provider for a blockchain network, you can either use Gateway commands or edit the configuration files directly.

Example for Solana mainnet (/conf/chains/solana/mainnet-beta.yml): nodeURL: https://your-preferred-node-provider.com/your-api-key nativeCurrencySymbol: SOL # Default compute units for a transaction # This sets the compute unit limit for transactions when not specified by the user defaultComputeUnits: 200000 # Confirmation polling interval in seconds # How often to check if a submitted transaction has been confirmed (inner retry loop) confirmRetryInterval: 0.5 # Number of confirmation polling attempts # How many times to poll for confirmation before considering the transaction unconfirmed confirmRetryCount: 10 # Floor percentile of recent priority fee samples used to estimate gasPrice for a transaction # Use the Nth percentile of recent priority fees as the base fee (90 = 90th percentile) basePriorityFeePct: 90 # Minimum priority fee per compute unit in lamports # This sets the floor for priority fees to ensure transactions are processed (default: 0.1 lamports/CU) minPriorityFeePerCU: 0.1

Example for Ethereum mainnet (/conf/chains/ethereum/mainnet.yml): chainID: 1 nodeURL: https://your-preferred-node-provider.com/your-api-key nativeCurrencySymbol: ETH minGasPrice: 0.1

The new Gateway endpoints accept addresses for baseToken and quoteToken in addition to symbols, so you should be able to use addresses directly before adding their symbols into the network's token list.

Gateway uses standardized token lists organized by chain and network. Each network has its own token list file that contains metadata for all supported tokens on that network.

The token list structure follows the Token Lists standard, which helps users avoid scams and find legitimate tokens across different networks.

Each AMM and CLMM DEX may have different pools for the same trading pair, with varying parameters like fee tier and bin step. Gateway now stores pool definitions in dedicated JSON files for each DEX connector.

Example pool entry: { "type": "amm", "network": "mainnet-beta", "baseSymbol": "WIF", "quoteSymbol": "SOL", "address": "EP2ib6dYdEeqD8MfE2ezHCxX3kP3K2eLKkirfPm5eyMx" }

For CLMM pools, use "type": "clmm" instead. The pool file structure allows you to specify different pools for different networks and trading types (AMM vs CLMM) within the same connector.

There are two ways to update your Gateway configurations:

Restart Gateway to apply changes

Always validate your configuration changes before applying them to a production environment. You can use the schema files referenced in root.yml to ensure your configurations are valid.

**Examples:**

Example 1 (unknown):
```unknown
version: 3
configurations:
  $namespace server:
    configurationPath: server.yml
    schemaPath: server-schema.json

  $namespace solana:
    configurationPath: solana.yml
    schemaPath: solana-schema.json

  $namespace jupiter:
    configurationPath: jupiter.yml
    schemaPath: jupiter-schema.json
```

Example 2 (unknown):
```unknown
# GMT Offset in hours (e.g. -8 for Pacific US Time, -5 for Eastern US Time)
GMTOffset: -8

# Port on which to run the Gateway server
port: 15888

# Port on which to run the Swagger documentation UI. 
# Set to 0 to serve docs at http://0.0.0.0:{port}/docs (same port as Gateway server)
# Set to a specific port (e.g. 8080) to serve docs separately at http://0.0.0.0:{docPort}
docsPort: 0

# Path to folder where Hummingbot generates self-signed certificates
certificatePath: ./certs/

# Path to folder where logs will be stored.
logPath: './logs'

# IPs allowed to access gateway. localhost is allowed by default.
ipWhitelist: []

# If true, logs will be stored in logPath and printed to stdout. If false, they
# will only be stored in logPath and not printed to stdout.
logToStdOut: true

# If true, the server will print detailed Fastify logs for each request and response to stdout. If false, only standard logs will be emitted.
fastifyLogs: false

# Nonce database
nonceDbPath: 'nonce.level'

# Transaction database
transactionDbPath: 'transaction.level'
```

Example 3 (unknown):
```unknown
defaultNetwork: mainnet-beta
defaultWallet: '<solana-wallet-address>'
```

Example 4 (unknown):
```unknown
# Default slippage percentage for swaps (as a decimal, e.g., 1 = 1%)
slippagePct: 1

# Priority level for swap transaction processing
# Options: medium, high, veryHigh
priorityLevel: 'veryHigh'

# Maximum priority fee in lamports (for dynamic priority fees)
# Used when priorityLevel is set and no explicit priorityFeeLamports is provided
maxLamports: 1000000

# Restrict routing to only go through 1 market
# Default: false (allows multi-hop routes for better prices)
onlyDirectRoutes: false

# Restrict routing through highly liquid intermediate tokens only
# Default: true (for better price and stability)
restrictIntermediateTokens: true

# Jupiter API key (optional)
# For free tier, leave empty (uses https://lite-api.jup.ag)
# For paid plans, generate key at https://portal.jup.ag (uses https://api.jup.ag)
apiKey: ''
```

---

## Commands - Hummingbot

**URL:** https://hummingbot.org/gateway/commands

**Contents:**
- Commands
- Installation and Setup¶
- gateway --help¶
- gateway ping¶
- gateway list¶
- gateway connect¶
  - Add regular wallet¶
  - Add hardware wallet¶
- gateway balance¶
- gateway config¶

This guide covers how to use Gateway commands within the Hummingbot client. Gateway commands allow you to manage wallets, execute swaps, manage liquidity positions, and configure Gateway settings directly from Hummingbot.

Before using Gateway commands, you need to have Gateway installed and running. Follow the Gateway Installation Guide to set up Gateway using either Docker or from source.

Once Gateway is running, you can verify the connection in Hummingbot:

If you see GATEWAY: 🔴 OFFLINE in the upper right corner:

To see all available Gateway commands and their descriptions:

Test the connection to Gateway and check node/chain status.

List all available chains, networks, and connectors.

Add a wallet for a specific chain. This is the primary way to connect your wallet to Gateway. After a wallet is successfully added, it automatically becomes the defaultWallet for that chain (ethereum or solana) in the Gateway configuration.

The wallet you add becomes the default wallet for all operations on that chain. You can check which wallet is currently set as default by running gateway config ethereum or gateway config solana.

Check token balances for connected wallets.

View and update Gateway configuration settings.

You may view the configuration for any namespace:

Gateway will automatically restart after any configuration change.

View or manage tokens in the token lists. usage: gateway token [-h] [symbol_or_address] [action] positional arguments: symbol_or_address Token symbol or address action Action to perform (update)

View and manage liquidity pool information.

Execute token swaps through DEX connectors.

Manage liquidity positions on AMM and CLMM pools.

Approve ERC-20 tokens for use with DEX connectors (Ethereum only).

Check token allowances for DEX connectors (Ethereum only).

Generate SSL certificates for secure Gateway communication. usage: gateway generate-certs [-h]

Afterwards, run pnpm run setup from the Gateway root directory to copy these certificates to Gateway.

**Examples:**

Example 1 (javascript):
```javascript
>>> gateway --help
usage:  gateway [-h] {allowance,approve,balance,config,connect,generate-certs,list,lp,ping,pool,swap,token} ...

positional arguments:
  {allowance,approve,balance,config,connect,generate-certs,list,lp,ping,pool,swap,token}
    allowance           Check token allowances for ethereum connectors
    approve             Approve token for use with ethereum connectors
    balance             Check token balances
    config              Show or update configuration
    connect             Add a wallet for a chain
    generate-certs      Create SSL certificate
    list                List available connectors
    lp                  Manage liquidity positions
    ping                Test node and chain/network status
    pool                View or update pool information
    swap                Swap tokens
    token               View or update token information
```

Example 2 (unknown):
```unknown
usage: gateway ping [-h] [chain]                                                                                                                                                   

  positional arguments:                                                                                                                                                              
    chain       Specific chain to test (optional)
```

Example 3 (unknown):
```unknown
>>> gateway ping

  Gateway service is online.                                                                                                                                                         

  Testing network status for 2 chains...                                                                                                                                             

  ethereum (base):                                                                                                                                                                   
    - RPC URL: https://small-dimensional-pine.base-mainnet.quiknode.pro/d01204cade4fab5                                                                                              
  2085cd0033c01bb2606a40c33                                                                                                                                                          
    - Current Block: 34463843                                                                                                                                                        
    - Native Currency: ETH                                                                                                                                                           
    - Status: ✓ Connected                                                                                                                                                            

  solana (mainnet-beta):                                                                                                                                                             
    - RPC URL: https://dry-dawn-hill.solana-mainnet.quiknode.pro/41bbd7ad405c552f91cc92                                                                                              
  8e044e5e04c66341d2                                                                                                                                                                 
    - Current Block: 361378534                                                                                                                                                       
    - Native Currency: SOL                                                                                                                                                           
    - Status: ✓ Connected
```

Example 4 (unknown):
```unknown
usage: gateway list [-h]
```

---

## Sample Scripts - Hummingbot

**URL:** https://hummingbot.org/scripts/examples/

**Contents:**
- Sample Scripts
- How to Run Scripts¶
- Starting Scripts¶
  - Simple PMM¶
  - Simple VWAP¶
  - Simple XEMM¶
  - AMM Data Feed¶
  - AMM Trade¶
  - LP Manage Position¶
  - Download Order Book and Trades¶

In the Hummingbot client, run a script with:

Scripts can be created both with and without config files. To create a configuration file for your script, execute:

This command auto-completes with scripts from the local /scripts directory that are configurable. You'll be prompted to specify strategy parameters, which are then saved in a YAML file within the conf/scripts directory. To run the script, use:

All sample scripts below can be found in the root /scripts folder and are available to run from the Hummingbot client by default.

These scripts are more complex and use StrategyV2 components such as Executors and the Market Data Provider.

Other example scripts can be found in sub-folders in the scripts folder:

To make a script available to run inside Hummingbot, copy or move the file into the root /scripts folder. For example:

**Examples:**

Example 1 (unknown):
```unknown
start --script [SCRIPT NAME]
```

Example 2 (unknown):
```unknown
create --script-config [SCRIPT_FILE]
```

Example 3 (unknown):
```unknown
start --script [SCRIPT_FILE] --conf [SCRIPT_CONFIG_FILE]
```

Example 4 (unknown):
```unknown
cp scripts/basic/format_status_example.py scripts
```

---

## Override Fees - Hummingbot

**URL:** https://hummingbot.org/global-configs/override-fees

**Contents:**
- Override Fees¶

By default, Hummingbot uses the default fees of the exchange. However, if you're on a VIP level getting discounts on fees, you can override this by editing the conf_fee_overrides.yml inside the conf or hummingbot_conf directory, depending on your installation method.

Exit and restart Hummingbot for the changes to take effect.

---

## Rate Limits - Hummingbot

**URL:** https://hummingbot.org/global-configs/rate-limits-share-pct

**Contents:**
- Rate Limits Share Pct¶
- How to use the parameter¶

Some exchanges impose rate limits per account. When running multiple bots using a single account, rate_limits_share_pct users to set a certain percentage of the total limit to each instance. When the bot is near the allocated limit, Hummingbot sends a notification as a warning so users can adjust their configuration before the account is banned.

For example, the rate limit for AscendEX is 100 requests per second. Your account will be banned for a certain period of time if you keep hitting the rate limit in 10 minutes (status code 429 or 100014).

Setting 50% for rate_limits_share_pct means we want the bot to send a notification when it starts to send 50 requests per second for that specific instance.

You can also configure this setting while the strategy is running. However, the strategy must be restarted for the changes to take effect.

---

## Kill Switch - Hummingbot

**URL:** https://hummingbot.org/global-configs/kill-switch

**Contents:**
- Kill Switch

Automatically stops the bot when it reaches a certain performance threshold, which can be either positive or negative. This feature uses the same performance calculation methodology as the history command.

You can always reconfigure this feature in two ways:

In past versions of Hummingbot (1.5.0 and below), the conf_client.yml file is named conf_global.yml

Note that when the market prices changes, so does the bot's performance and may trigger the kill switch. For example, we executed 13 trades and our performance are shown below.

After a while, the end price changed from 202.715 to 200.54 and so did our bot's performance even without making more trades. Since kill_switch_rate is set to -0.3 this will stop the strategy.

**Examples:**

Example 1 (unknown):
```unknown
Select your kill-switch mode (kill_switch_enabled/kill_switch_disabled)  >>>
At what profit/loss rate would you like the bot to stop? (e.g. -5 equals 5 percent loss) >>>
```

Example 2 (unknown):
```unknown
kill_switch_mode:
  kill_switch_rate: -5.0
```

Example 3 (unknown):
```unknown
Inventory:
      Market Asset  Starting   Current  Net Delta Trade Delta
  0  binance   ETH   10.0000   11.0000     1.0000      3.0000
  1  binance  USDT  500.0000  297.1580  -202.8420   -610.6340

Markets:
      Market     Pair Start Price       End Price  Trades Trade Value Delta
  0  binance  ETHUSDT     203.913  202.7150000000      13  -2.48900000 USDT

Performance:
  Started: 2020-05-26 10:28:03
  Duration: 0 days 00:07:06
  Total Trade Value Delta: -2.489 USDT
  Return %: -0.0985 %
```

Example 4 (unknown):
```unknown
Inventory:
      Market Asset  Starting   Current  Net Delta Trade Delta
  0  binance   ETH   10.0000   11.0000     1.0000      3.0000
  1  binance  USDT  500.0000  297.1580  -202.8420   -610.6340

Markets:
      Market     Pair Start Price       End Price  Trades Trade Value Delta
  0  binance  ETHUSDT     203.913  200.5400000000      13  -9.01400000 USDT

Performance:
  Started: 2020-05-26 10:28:03
  Duration: 0 days 02:09:13
  Total Trade Value Delta: -9.014 USDT
  Return %: -0.3598 %
```

---

## 

**URL:** https://hummingbot.org/dashboard/config-5.png

---

## 

**URL:** https://hummingbot.org/dashboard/config-9.png

---

## Config Files - Hummingbot

**URL:** https://hummingbot.org/client/config-files

**Contents:**
- Config Files
- Where config files are stored¶
- Script config files¶
  - Creating script config files¶
  - Starting configurable scripts¶
- Controller config files¶
  - Creating controller config files¶
  - Starting controller configs¶
- Strategy V1 config files¶
  - Creating Strategy V1 config files¶

A config file allows you to define the parameters used in a YAML file. Later, you can modify the values of this file, share it with others, and and import it into your strategy.

These configuration files created and used by Hummingbot are saved in the /conf directory of your instance, which you can edit directly with a standard text editor.

Starting in v1.24.0, Scripts can define a ScriptConfig class that defines configuration parameters that users can store in a YAML file.

This is an optional feature, and more basic scripts may elect to hardcode their parameters in the script file.

To create a configuration file for a compatible, run the create command and add the --script-config flag.

In the auto-complete dropdown, only the configurable scripts located in the /scripts folder will be shown.

Afterwards, you will be presented with prompts and default values defined in the config class above.

The last prompt will ask you to enter a name for the config file, which is saved in conf/scripts.

Run start with both --script and --conf flags to run a script with a configuration file.

The StrategyV2 framework abstracts strategy logic into Controllers. Each controller defines the config parameters that it accepts.

To create a controller configuration file, run the create command and add the -controller-config flag.

In the auto-complete dropdown, the controllers in each sub-folder in the /controllers folder will be shown.

Similar to the script config, you will be presented with prompts and default values defined in the controller.

The last prompt will ask you to enter a name for the config file, which is saved in conf/controllers.

To start a controller configuration, define the configuration file of the v2_generic_with_controllers.py loader script:

Afterwards, start the loader script by running: start --script v2_generic_with_controllers.py --conf conf_v2_generic_with_controllers_1.yml

The original Hummingbot V1 strategies also allowed users to define config files.

Run create command without the --script-config flag to create a Strategy V1 config file. The autocomplete command will display a list of the available V1 strategies, each one a folder in the /hummingbot/strategy folder.

Next, answer the prompts to configure your bot's behavior depending on the strategy you want to use.

The last prompt will ask you to enter a name for the config file. You can also specify the name of your file at the beginning by running create [file_name] command.

You can also skip the prompt by running import [file_name] command.

While Scripts are single files that contain the types and messages for their parameters, V1 Strategies have a separate pre-defined template configuration file defined by the strategy author.

Each V1 strategy template can be found here: Config Templates.

**Examples:**

Example 1 (unknown):
```unknown
class DManV3ScriptConfig(BaseClientModel):
    script_file_name: str = Field(default_factory=lambda: os.path.basename(__file__))

    # Account configuration
    exchange: str = Field("binance_perpetual", client_data=ClientFieldData(prompt_on_new=True, prompt=lambda mi: "Enter the name of the exchange where the bot will operate (e.g., binance_perpetual):"))
    trading_pairs: str = Field("DOGE-USDT,INJ-USDT", client_data=ClientFieldData(prompt_on_new=True, prompt=lambda mi: "List the trading pairs for the bot to trade on, separated by commas (e.g., BTC-USDT,ETH-USDT):"))
    leverage: int = Field(20, client_data=ClientFieldData(prompt_on_new=True, prompt=lambda mi: "Set the leverage to use for trading (e.g., 20 for 20x leverage):"))
```

Example 2 (unknown):
```unknown
create --script-config v2_generic_with_controllers
```

Example 3 (unknown):
```unknown
start --script v2_generic_with_controllers.py --conf conf_v2_generic_with_controllers_1.yml
```

Example 4 (python):
```python
>>>`import conf_pure_mm_1.yml`
Configuration from conf_pure_mm_1.yml file is imported.

Preliminary checks:
 - Exchange check: All connections confirmed.
 - Strategy check: All required parameters confirmed.
 -All checks: Confirmed.

Enter "start" to start market making

>>> start
```

---

## Balance Limit - Hummingbot

**URL:** https://hummingbot.org/global-configs/balance-limit

**Contents:**
- Balance Limit
- How It Works¶
- Example Scenario¶

Updated on version 0.35.0

Sets the amount limit on how much assets Hummingbot can use in an exchange or wallet. This can be useful when running multiple bots on different trading pairs with same tokens e.g. running a BTC-USDT pair and another bot on ETH-USDT using the same account.

You can set how much of a particular token the bot can use by running the command balance limit [exchange] [asset] [amount]. You can disable this feature by editing it in the global config file and set it to -1. While setting it to 0 will initially not place any order for a specific asset until a trade is executed to accumulate the said asset.

Run the balance command again or balance limit to confirm the limit has been applied.

Create pure market making strategy, run config to view the whole configuration.

Run balance limit binance ETH 0.0513 to set the balance limit to 0.0513 ETH. Run balance limit binance USDT 30 to set the balance limit to 30 USDT. Both ETH and USDT value is equivalent to $30.

Each order is 0.0188 equivalent to $11.20

Sell order gets filled. USDT available balance is now 30.1657

Another sell order gets filled, the available balance now shows 41.2069. Plus the open buy order, the "usable" balance on USDT is now at around $52.

After the two sell orders gets filled the remaining available balance in ETH is 0.0137 equivalent to $8.17. It means that after the next order_refresh_time it won't create sell order because the minimum order amount is $11.

Same process as the scenario above. After the two buy orders gets filled the remaining available balance in USDT is 7.5317 equivalent to $7.53. It means that after the next order_refresh_time it won't create buy order because the minimum order amount is $11.

**Examples:**

Example 1 (unknown):
```unknown
>>>  balance limit binance USDT 100
Limit for USDT on binance exchange set to 100.0
```

Example 2 (unknown):
```unknown
>>>  balance
Updating balances, please wait...

binance:
     Asset    Amount   
       BNB    0.0000   
       BTC    0.0000   
       ETH    0.0000   
     TFUEL    0.0187   
     THETA    0.5880   
      USDC    0.0090   
      USDT  158.8197  
       XRP    0.8440  
       XZC    0.0076
```

Example 3 (unknown):
```unknown
>>>  balance limit
Balance Limits per exchange...

binance
    Asset     Limit
     USDT  100.0000
```

---

## Commands - Hummingbot

**URL:** https://hummingbot.org/gateway/commands/

**Contents:**
- Commands
- Installation and Setup¶
- gateway --help¶
- gateway ping¶
- gateway list¶
- gateway connect¶
  - Add regular wallet¶
  - Add hardware wallet¶
- gateway balance¶
- gateway config¶

This guide covers how to use Gateway commands within the Hummingbot client. Gateway commands allow you to manage wallets, execute swaps, manage liquidity positions, and configure Gateway settings directly from Hummingbot.

Before using Gateway commands, you need to have Gateway installed and running. Follow the Gateway Installation Guide to set up Gateway using either Docker or from source.

Once Gateway is running, you can verify the connection in Hummingbot:

If you see GATEWAY: 🔴 OFFLINE in the upper right corner:

To see all available Gateway commands and their descriptions:

Test the connection to Gateway and check node/chain status.

List all available chains, networks, and connectors.

Add a wallet for a specific chain. This is the primary way to connect your wallet to Gateway. After a wallet is successfully added, it automatically becomes the defaultWallet for that chain (ethereum or solana) in the Gateway configuration.

The wallet you add becomes the default wallet for all operations on that chain. You can check which wallet is currently set as default by running gateway config ethereum or gateway config solana.

Check token balances for connected wallets.

View and update Gateway configuration settings.

You may view the configuration for any namespace:

Gateway will automatically restart after any configuration change.

View or manage tokens in the token lists. usage: gateway token [-h] [symbol_or_address] [action] positional arguments: symbol_or_address Token symbol or address action Action to perform (update)

View and manage liquidity pool information.

Execute token swaps through DEX connectors.

Manage liquidity positions on AMM and CLMM pools.

Approve ERC-20 tokens for use with DEX connectors (Ethereum only).

Check token allowances for DEX connectors (Ethereum only).

Generate SSL certificates for secure Gateway communication. usage: gateway generate-certs [-h]

Afterwards, run pnpm run setup from the Gateway root directory to copy these certificates to Gateway.

**Examples:**

Example 1 (javascript):
```javascript
>>> gateway --help
usage:  gateway [-h] {allowance,approve,balance,config,connect,generate-certs,list,lp,ping,pool,swap,token} ...

positional arguments:
  {allowance,approve,balance,config,connect,generate-certs,list,lp,ping,pool,swap,token}
    allowance           Check token allowances for ethereum connectors
    approve             Approve token for use with ethereum connectors
    balance             Check token balances
    config              Show or update configuration
    connect             Add a wallet for a chain
    generate-certs      Create SSL certificate
    list                List available connectors
    lp                  Manage liquidity positions
    ping                Test node and chain/network status
    pool                View or update pool information
    swap                Swap tokens
    token               View or update token information
```

Example 2 (unknown):
```unknown
usage: gateway ping [-h] [chain]                                                                                                                                                   

  positional arguments:                                                                                                                                                              
    chain       Specific chain to test (optional)
```

Example 3 (unknown):
```unknown
>>> gateway ping

  Gateway service is online.                                                                                                                                                         

  Testing network status for 2 chains...                                                                                                                                             

  ethereum (base):                                                                                                                                                                   
    - RPC URL: https://small-dimensional-pine.base-mainnet.quiknode.pro/d01204cade4fab5                                                                                              
  2085cd0033c01bb2606a40c33                                                                                                                                                          
    - Current Block: 34463843                                                                                                                                                        
    - Native Currency: ETH                                                                                                                                                           
    - Status: ✓ Connected                                                                                                                                                            

  solana (mainnet-beta):                                                                                                                                                             
    - RPC URL: https://dry-dawn-hill.solana-mainnet.quiknode.pro/41bbd7ad405c552f91cc92                                                                                              
  8e044e5e04c66341d2                                                                                                                                                                 
    - Current Block: 361378534                                                                                                                                                       
    - Native Currency: SOL                                                                                                                                                           
    - Status: ✓ Connected
```

Example 4 (unknown):
```unknown
usage: gateway list [-h]
```

---

## 

**URL:** https://hummingbot.org/dashboard/config-8.png

---

## Deploying Instances - Hummingbot

**URL:** https://hummingbot.org/dashboard/deploy/

**Contents:**
- Deploying Instances¶
- Bot Configuration¶
- Launch an Instance¶
- Delete a Controller Config¶

The Deploy V2 page in the Hummingbot Dashboard is designed for launching and managing Hummingbot trading instances. This page offers a streamlined interface to select configurations, set up instances, and deploy bots for automated trading.

Instance Name: A unique name for the bot instance you are about to deploy.

Available Images: Select the Docker image version of Hummingbot to use for the deployment. You can use different Hummingbot Docker versions like development or latest

Credentials: Select the account credentials that the bot will use for trading. This ensures that the bot has the necessary API keys and permissions to operate on the selected exchanges.

Configuration List: Displays all the available controller configurations that you have created and uploaded.

Choose one of the available configurations from the list by checking the box next to it.

Click the DELETE button to delete the config

---

## Config Files - Hummingbot

**URL:** https://hummingbot.org/client/config-files/

**Contents:**
- Config Files
- Where config files are stored¶
- Script config files¶
  - Creating script config files¶
  - Starting configurable scripts¶
- Controller config files¶
  - Creating controller config files¶
  - Starting controller configs¶
- Strategy V1 config files¶
  - Creating Strategy V1 config files¶

A config file allows you to define the parameters used in a YAML file. Later, you can modify the values of this file, share it with others, and and import it into your strategy.

These configuration files created and used by Hummingbot are saved in the /conf directory of your instance, which you can edit directly with a standard text editor.

Starting in v1.24.0, Scripts can define a ScriptConfig class that defines configuration parameters that users can store in a YAML file.

This is an optional feature, and more basic scripts may elect to hardcode their parameters in the script file.

To create a configuration file for a compatible, run the create command and add the --script-config flag.

In the auto-complete dropdown, only the configurable scripts located in the /scripts folder will be shown.

Afterwards, you will be presented with prompts and default values defined in the config class above.

The last prompt will ask you to enter a name for the config file, which is saved in conf/scripts.

Run start with both --script and --conf flags to run a script with a configuration file.

The StrategyV2 framework abstracts strategy logic into Controllers. Each controller defines the config parameters that it accepts.

To create a controller configuration file, run the create command and add the -controller-config flag.

In the auto-complete dropdown, the controllers in each sub-folder in the /controllers folder will be shown.

Similar to the script config, you will be presented with prompts and default values defined in the controller.

The last prompt will ask you to enter a name for the config file, which is saved in conf/controllers.

To start a controller configuration, define the configuration file of the v2_generic_with_controllers.py loader script:

Afterwards, start the loader script by running: start --script v2_generic_with_controllers.py --conf conf_v2_generic_with_controllers_1.yml

The original Hummingbot V1 strategies also allowed users to define config files.

Run create command without the --script-config flag to create a Strategy V1 config file. The autocomplete command will display a list of the available V1 strategies, each one a folder in the /hummingbot/strategy folder.

Next, answer the prompts to configure your bot's behavior depending on the strategy you want to use.

The last prompt will ask you to enter a name for the config file. You can also specify the name of your file at the beginning by running create [file_name] command.

You can also skip the prompt by running import [file_name] command.

While Scripts are single files that contain the types and messages for their parameters, V1 Strategies have a separate pre-defined template configuration file defined by the strategy author.

Each V1 strategy template can be found here: Config Templates.

**Examples:**

Example 1 (unknown):
```unknown
class DManV3ScriptConfig(BaseClientModel):
    script_file_name: str = Field(default_factory=lambda: os.path.basename(__file__))

    # Account configuration
    exchange: str = Field("binance_perpetual", client_data=ClientFieldData(prompt_on_new=True, prompt=lambda mi: "Enter the name of the exchange where the bot will operate (e.g., binance_perpetual):"))
    trading_pairs: str = Field("DOGE-USDT,INJ-USDT", client_data=ClientFieldData(prompt_on_new=True, prompt=lambda mi: "List the trading pairs for the bot to trade on, separated by commas (e.g., BTC-USDT,ETH-USDT):"))
    leverage: int = Field(20, client_data=ClientFieldData(prompt_on_new=True, prompt=lambda mi: "Set the leverage to use for trading (e.g., 20 for 20x leverage):"))
```

Example 2 (unknown):
```unknown
create --script-config v2_generic_with_controllers
```

Example 3 (unknown):
```unknown
start --script v2_generic_with_controllers.py --conf conf_v2_generic_with_controllers_1.yml
```

Example 4 (python):
```python
>>>`import conf_pure_mm_1.yml`
Configuration from conf_pure_mm_1.yml file is imported.

Preliminary checks:
 - Exchange check: All connections confirmed.
 - Strategy check: All required parameters confirmed.
 -All checks: Confirmed.

Enter "start" to start market making

>>> start
```

---

## Color Settings - Hummingbot

**URL:** https://hummingbot.org/global-configs/color-settings

**Contents:**
- Color Settings¶
- Changing the panel colors¶
- Reset colors to default¶

Starting with version 0.45, we added new global configuration parameters that allows users to customize the client's background colors.

To make changes to the panel colors, run config [parameter_name] inside the Hummingbot client. For example, the command for changing the log pane color is config log-pane and enter the hex code of the desired color.

You can use a hexadecimal color picker like the one here to choose colors: https://www.w3schools.com/colors/colors_picker.asp

Alternatively, you can edit these values in the conf_client.yml file located under the hummingbot_conf folder using a text editor.

In past versions of Hummingbot (1.5.0 and below), the conf_client.yml file is named conf_global.yml

Press CTRL + R while inside Hummingbot to reset the style to use its default colors.

**Examples:**

Example 1 (unknown):
```unknown
# Background color of the top pane
top-pane: '#000000'

# Background color of the bottom pane
bottom-pane: '#000000'

# Background color of the output pane
output-pane: '#282C2F'

# Background color of the input pane
input-pane: '#151819'

# Background color of the logs pane
logs-pane: '#151819'

# Terminal primary color (text)
terminal-primary: '#00FFE5'
```

---

## 

**URL:** https://hummingbot.org/dashboard/config-4.png

---

## Configuration - Hummingbot

**URL:** https://hummingbot.org/gateway/configuration

**Contents:**
- Configuration
- Configuration Overview¶
  - Configuration Structure¶
  - Root Configuration¶
  - Server Configuration¶
  - Chain Configuration¶
  - Connector Configuration¶
    - Example: Jupiter Configuration¶
  - Network Configuration¶
    - Example: Solana mainnet-beta Configuration¶

Gateway uses a modular configuration system that allows you to customize various aspects of its operation. This guide explains the configuration structure and how to modify it to suit your needs.

Gateway's configuration system consists of YAML files located in the /conf directory, along with JSON files for tokens and pools organized by chain and connector.

The initial configuration files are created automatically using the default templates in /src/templates when you run the setup script during installation.

The /conf/ folder contains the following types of configuration files:

The root.yml file serves as the entry point for Gateway's configuration system. It defines which configuration files are loaded and their corresponding schema files.

This file tells Gateway:

The server.yml file controls the core Gateway server behavior, including ports, logging, and security settings.

Chain configuration files (e.g., /conf/chains/solana.yml) now contain only the default network and wallet settings for each blockchain.

When you connect a wallet using gateway connect, it automatically becomes the defaultWallet for that chain. The defaultNetwork determines which network configuration Gateway uses by default for that chain.

Network-specific configurations are now stored in separate files under /conf/chains/{chain}/{network}.yml

Connector configuration files (e.g., /conf/connectors/jupiter.yml) define settings specific to each DEX connector, including slippage tolerance, routing preferences, and API configurations.

Configuration Options Explained:

slippagePct: Maximum acceptable price slippage for trades. If the execution price deviates more than this percentage from the quoted price, the transaction will fail.

priorityLevel: Controls transaction priority on Solana. Higher priority levels result in faster confirmation but cost more in fees. Set to veryHigh for time-sensitive trades.

maxLamports: Caps the maximum priority fee to prevent excessive costs during network congestion. 1,000,000 lamports = 0.001 SOL.

onlyDirectRoutes: When true, restricts swaps to direct pools only (no intermediate tokens). This can reduce price impact but may result in worse pricing or failed routes for less liquid pairs.

restrictIntermediateTokens: When true, only routes through major tokens (SOL, USDC, USDT) as intermediates. This increases reliability and reduces price impact risks.

apiKey: Optional API key for Jupiter's paid tier. The free tier (lite-api) is suitable for most users, while the paid tier offers higher rate limits and additional features.

Network configuration files (e.g., /conf/chains/solana/mainnet-beta.yml) contain the detailed settings for each blockchain network, including RPC endpoints and transaction parameters.

You can view the current configuration for any network using Gateway commands:

To update any network setting, use gateway config [namespace] update:

To change the RPC node provider for a blockchain network, you can either use Gateway commands or edit the configuration files directly.

Example for Solana mainnet (/conf/chains/solana/mainnet-beta.yml): nodeURL: https://your-preferred-node-provider.com/your-api-key nativeCurrencySymbol: SOL # Default compute units for a transaction # This sets the compute unit limit for transactions when not specified by the user defaultComputeUnits: 200000 # Confirmation polling interval in seconds # How often to check if a submitted transaction has been confirmed (inner retry loop) confirmRetryInterval: 0.5 # Number of confirmation polling attempts # How many times to poll for confirmation before considering the transaction unconfirmed confirmRetryCount: 10 # Floor percentile of recent priority fee samples used to estimate gasPrice for a transaction # Use the Nth percentile of recent priority fees as the base fee (90 = 90th percentile) basePriorityFeePct: 90 # Minimum priority fee per compute unit in lamports # This sets the floor for priority fees to ensure transactions are processed (default: 0.1 lamports/CU) minPriorityFeePerCU: 0.1

Example for Ethereum mainnet (/conf/chains/ethereum/mainnet.yml): chainID: 1 nodeURL: https://your-preferred-node-provider.com/your-api-key nativeCurrencySymbol: ETH minGasPrice: 0.1

The new Gateway endpoints accept addresses for baseToken and quoteToken in addition to symbols, so you should be able to use addresses directly before adding their symbols into the network's token list.

Gateway uses standardized token lists organized by chain and network. Each network has its own token list file that contains metadata for all supported tokens on that network.

The token list structure follows the Token Lists standard, which helps users avoid scams and find legitimate tokens across different networks.

Each AMM and CLMM DEX may have different pools for the same trading pair, with varying parameters like fee tier and bin step. Gateway now stores pool definitions in dedicated JSON files for each DEX connector.

Example pool entry: { "type": "amm", "network": "mainnet-beta", "baseSymbol": "WIF", "quoteSymbol": "SOL", "address": "EP2ib6dYdEeqD8MfE2ezHCxX3kP3K2eLKkirfPm5eyMx" }

For CLMM pools, use "type": "clmm" instead. The pool file structure allows you to specify different pools for different networks and trading types (AMM vs CLMM) within the same connector.

There are two ways to update your Gateway configurations:

Restart Gateway to apply changes

Always validate your configuration changes before applying them to a production environment. You can use the schema files referenced in root.yml to ensure your configurations are valid.

**Examples:**

Example 1 (unknown):
```unknown
version: 3
configurations:
  $namespace server:
    configurationPath: server.yml
    schemaPath: server-schema.json

  $namespace solana:
    configurationPath: solana.yml
    schemaPath: solana-schema.json

  $namespace jupiter:
    configurationPath: jupiter.yml
    schemaPath: jupiter-schema.json
```

Example 2 (unknown):
```unknown
# GMT Offset in hours (e.g. -8 for Pacific US Time, -5 for Eastern US Time)
GMTOffset: -8

# Port on which to run the Gateway server
port: 15888

# Port on which to run the Swagger documentation UI. 
# Set to 0 to serve docs at http://0.0.0.0:{port}/docs (same port as Gateway server)
# Set to a specific port (e.g. 8080) to serve docs separately at http://0.0.0.0:{docPort}
docsPort: 0

# Path to folder where Hummingbot generates self-signed certificates
certificatePath: ./certs/

# Path to folder where logs will be stored.
logPath: './logs'

# IPs allowed to access gateway. localhost is allowed by default.
ipWhitelist: []

# If true, logs will be stored in logPath and printed to stdout. If false, they
# will only be stored in logPath and not printed to stdout.
logToStdOut: true

# If true, the server will print detailed Fastify logs for each request and response to stdout. If false, only standard logs will be emitted.
fastifyLogs: false

# Nonce database
nonceDbPath: 'nonce.level'

# Transaction database
transactionDbPath: 'transaction.level'
```

Example 3 (unknown):
```unknown
defaultNetwork: mainnet-beta
defaultWallet: '<solana-wallet-address>'
```

Example 4 (unknown):
```unknown
# Default slippage percentage for swaps (as a decimal, e.g., 1 = 1%)
slippagePct: 1

# Priority level for swap transaction processing
# Options: medium, high, veryHigh
priorityLevel: 'veryHigh'

# Maximum priority fee in lamports (for dynamic priority fees)
# Used when priorityLevel is set and no explicit priorityFeeLamports is provided
maxLamports: 1000000

# Restrict routing to only go through 1 market
# Default: false (allows multi-hop routes for better prices)
onlyDirectRoutes: false

# Restrict routing through highly liquid intermediate tokens only
# Default: true (for better price and stability)
restrictIntermediateTokens: true

# Jupiter API key (optional)
# For free tier, leave empty (uses https://lite-api.jup.ag)
# For paid plans, generate key at https://portal.jup.ag (uses https://api.jup.ag)
apiKey: ''
```

---

## 

**URL:** https://hummingbot.org/dashboard/config-11.png

---

## Connect External Database - Hummingbot

**URL:** https://hummingbot.org/global-configs/external-db

**Contents:**
- Connect External Database
- Configuration parameters¶
- SQLAlchemy dialects¶
- 📘 Additional Resources¶

Community contibution

Contributor: fengkiej from Rupiah Token

Hummingbot stores trades in a local SQLite for database by default, but it may be limiting for some cases such as sharing data to external system, in some cases user may want to use their own preferred client/server RDBMS for it.

Other RDBMS are supported on Hummingbot through SQLAlchemy, it has included some widely used RDBMS dialects, i.e.:

These dialects requires separate DBAPI driver to be installed on Hummingbot's conda environment, see SQLAlchemy documentation for more information on appropriate DBAPI driver for each RDBMS. For example, to use PostgreSQL, psycopg2 need to be installed. Run the following command to install it using conda:

To configure RDBMS connection, we need to edit conf_client.yml in the /hummingbot_conf directory.

In past versions of Hummingbot (1.5.0 and below), the conf_client.yml file is named conf_global.yml

It is also possible to connect with available SQLAlchemy's external dialects (e.g. Amazon Redshift). But the feature is not currently supported in Hummingbot due to its various DSN format, use this at your own risk.

In this Youtube Video the Foundation's lead developer Fede, shows you how you can use Docker Compose to launch multiple instances that all save to a single Postgres database.

**Examples:**

Example 1 (unknown):
```unknown
conda install psycopg2
```

Example 2 (unknown):
```unknown
- Advanced database options, currently supports SQLAlchemy's included dialects
- Reference: https://docs.sqlalchemy.org/en/13/dialects/

db_engine: sqlite
db_host: 127.0.0.1
db_port: '3306'
db_username: username
db_password: password
db_name: dbname
```

---

## 

**URL:** https://hummingbot.org/dashboard/config-2.png

---

## 

**URL:** https://hummingbot.org/dashboard/config-7.png

---

## 

**URL:** https://hummingbot.org/dashboard/config-3.png

---
