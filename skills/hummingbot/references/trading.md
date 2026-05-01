# Hummingbot - Trading

**Pages:** 3

---

## Overview - Hummingbot

**URL:** https://hummingbot.org/gateway/

**Contents:**
- Overview
- What is Gateway?¶
- In This Section¶
- Key Features¶
  - Connector Schemas¶
- Installation¶
- Architecture¶
- Governance and Maintenance¶
- Contributing¶
- History¶

Hummingbot Gateway is a Typescript-based API server that standardizes interactions with blockchain networks and decentralized exchanges (DEXs). It acts as a middleware layer, providing a unified interface for performing actions like checking balances, executing trades, and managing wallets across different protocols.

Gateway is a companion service to the Python-based Hummingbot client, exposing standardized REST API endpoints for trading and liquidity-related functionality on DEXs. This enables Hummingbot to run strategies that operate across both centralized (CEX) and decentralized exchanges seamlessly.

For detailed implementation guides and examples for each schema, see DEX Connectors.

Gateway can be installed alongside Hummingbot to enable trading on AMM DEXs, or as a standalone API server. For detailed installation instructions, see Installation & Setup.

When running Gateway in DEV mode, access the interactive Swagger API documentation at: http://localhost:15888/docs

Gateway follows a modular architecture with clear separation of concerns:

Like other connectors, Gateway DEX connectors require ongoing maintenance: fixing bugs, addressing user issues, and keeping up with updates to both the exchange/blockchain API as well as improvements to the Hummingbot connector standard.

Hummingbot Foundation maintains certain reference connectors as the standard and utilizes a community-based maintenance process. We assign Bounties to community developers to upgrade and fix bugs for each exchange's connectors in the codebase.

Each quarter, Exchange Connector Polls allocates HBOT bounties toward the top CEX connectors and determines which exchange connectors should be included in the codebase going forward. This process also determines which blockchains and networks that Gateway supports.

See the Connector Pots tab in HBOT Tracker for the current allocations for each exchange.

Gateway is part of the open source Hummingbot project. Ways to contribute:

For more information about Gateway's history and architecture decisions, see:

**Examples:**

Example 1 (javascript):
```javascript
/src
├── chains/               # Blockchain-specific implementations
│   └── {chain}/         # Each blockchain (ethereum, solana, etc.)
├── connectors/           # DEX-specific implementations
│   ├── {dex}/           # Each DEX connector directory
│   │   ├── router-routes/   # DEX aggregator operations
│   │   ├── amm-routes/      # AMM pool operations
│   │   └── clmm-routes/     # Concentrated liquidity operations
├── services/             # Core services (config, logging, tokens)
├── schemas/              # API request/response schemas
├── templates/            # Base classes and interfaces for connectors
├── tokens/               # Token lists and metadata
├── pools/                # Liquidity pool configurations
└── wallet/               # Wallet management
```

---

## Overview - Hummingbot

**URL:** https://hummingbot.org/gateway

**Contents:**
- Overview
- What is Gateway?¶
- In This Section¶
- Key Features¶
  - Connector Schemas¶
- Installation¶
- Architecture¶
- Governance and Maintenance¶
- Contributing¶
- History¶

Hummingbot Gateway is a Typescript-based API server that standardizes interactions with blockchain networks and decentralized exchanges (DEXs). It acts as a middleware layer, providing a unified interface for performing actions like checking balances, executing trades, and managing wallets across different protocols.

Gateway is a companion service to the Python-based Hummingbot client, exposing standardized REST API endpoints for trading and liquidity-related functionality on DEXs. This enables Hummingbot to run strategies that operate across both centralized (CEX) and decentralized exchanges seamlessly.

For detailed implementation guides and examples for each schema, see DEX Connectors.

Gateway can be installed alongside Hummingbot to enable trading on AMM DEXs, or as a standalone API server. For detailed installation instructions, see Installation & Setup.

When running Gateway in DEV mode, access the interactive Swagger API documentation at: http://localhost:15888/docs

Gateway follows a modular architecture with clear separation of concerns:

Like other connectors, Gateway DEX connectors require ongoing maintenance: fixing bugs, addressing user issues, and keeping up with updates to both the exchange/blockchain API as well as improvements to the Hummingbot connector standard.

Hummingbot Foundation maintains certain reference connectors as the standard and utilizes a community-based maintenance process. We assign Bounties to community developers to upgrade and fix bugs for each exchange's connectors in the codebase.

Each quarter, Exchange Connector Polls allocates HBOT bounties toward the top CEX connectors and determines which exchange connectors should be included in the codebase going forward. This process also determines which blockchains and networks that Gateway supports.

See the Connector Pots tab in HBOT Tracker for the current allocations for each exchange.

Gateway is part of the open source Hummingbot project. Ways to contribute:

For more information about Gateway's history and architecture decisions, see:

**Examples:**

Example 1 (javascript):
```javascript
/src
├── chains/               # Blockchain-specific implementations
│   └── {chain}/         # Each blockchain (ethereum, solana, etc.)
├── connectors/           # DEX-specific implementations
│   ├── {dex}/           # Each DEX connector directory
│   │   ├── router-routes/   # DEX aggregator operations
│   │   ├── amm-routes/      # AMM pool operations
│   │   └── clmm-routes/     # Concentrated liquidity operations
├── services/             # Core services (config, logging, tokens)
├── schemas/              # API request/response schemas
├── templates/            # Base classes and interfaces for connectors
├── tokens/               # Token lists and metadata
├── pools/                # Liquidity pool configurations
└── wallet/               # Wallet management
```

---

## Overview - Hummingbot

**URL:** https://hummingbot.org/hummingbot-api/

**Contents:**
- Hummingbot API¶
- Overview¶
- Key Features¶
- Architecture¶
  - Key Components¶
- Use Cases¶
- Getting Started¶
- API Routers¶
  - 🐳 Docker Management¶
  - 💼 Account Management¶

The backend-api has been renamed to hummingbot-api, marking a major revamp of the codebase with improvements in architecture, modularity, and developer experience.

Hummingbot API is a comprehensive RESTful API framework designed for managing trading operations across multiple exchanges. It allows individual traders and teams to deploy custom, private servers for trade execution, portfolio management, and data collection, bot deployment, and other use cases.

GitHub Repository: github.com/hummingbot/hummingbot-api

The Hummingbot API enables various trading applications:

The guides include Docker setup and Python API client examples to get you trading in minutes.

The Hummingbot API provides the following key routers:

Manage Docker containers and instances running Hummingbot

Handle exchange account credentials and configurations

Discover and manage available exchange connectors

Monitor and analyze portfolio performance across exchanges

Execute trades, manage orders, and monitor positions

Configure and deploy trading strategies with real-time updates

Access real-time and historical market data

Deploy, configure, and manage multiple bot instances

Run strategy backtests with historical data

The API uses HTTP Basic Authentication:

A modern, asynchronous Python client is available for interacting with the Hummingbot API. This client is used by the Hummingbot Dashboard as the interface layer for all API communications.

**Examples:**

Example 1 (unknown):
```unknown
graph TB
    subgraph "Clients"
        direction LR
        CUSTOM[Custom Apps]
        DASH[Hummingbot<br/>Dashboard]
        AI[AI Agents]
    end

    subgraph "Hummingbot API"
        direction LR
        API["FastAPI<br/>Server<br/>"]
        PG[(PostgreSQL<br/>Database)]
        MQTT[EMQX<br/>Message Broker]
    end

    subgraph "Bots"
        BOTS[Hummingbot<br/>Instances]
    end

    subgraph "Exchanges"
        EX[Binance, OKX,<br/>Hyperliquid, etc.]
    end

    %% Client connections using API Client
    DASH -->|Hummingbot API Client| API

    %% Bot connections
    BOTS <-->|Commands & Updates| MQTT

    %% Exchange connections
    BOTS <-->|Trade & Data| EX
    API <-->|Trade & Data| EX

    %% Apply theme colors
    classDef clientStyle stroke:#5FFFD7,stroke-width:3px
    classDef apiStyle stroke:#00B1BB,stroke-width:3px
    classDef botsStyle stroke:#E549FF,stroke-width:3px

    class DASH clientStyle
    class API,PG,MQTT apiStyle
    class BOTS botsStyle
```

Example 2 (unknown):
```unknown
pip install hummingbot-api-client
```

Example 3 (python):
```python
from hummingbot_api_client import HummingbotAPIClient

# Initialize client
client = HummingbotAPIClient(
    base_url="http://localhost:8000",
    username="your-username",
    password="your-password"
)

# Get portfolio data
portfolio = await client.get_portfolio()

# Execute a trade
order = await client.create_order(
    connector="binance",
    trading_pair="BTC-USDT",
    order_type="limit",
    side="buy",
    amount=0.001,
    price=50000
)
```

---
