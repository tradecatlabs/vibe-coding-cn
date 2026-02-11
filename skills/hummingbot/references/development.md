# Hummingbot - Development

**Pages:** 13

---

## Contributions - Hummingbot

**URL:** https://hummingbot.org/developers/contributions/

**Contents:**
- Contributions
- Workflow¶
  - 1. Fork the repository¶
  - 2. Add remote¶
  - 3. Creating your branch¶
  - 4. Commit changes to a branch¶
  - 5. Rebase upstream changes¶
  - 6. Create a pull request¶
  - 7. Create a proposal in Snapshot ⚡️¶
  - 8. Code review¶

All contributors should adhere to the code conventions used in the Hummingbot repository. The guidelines are outlined below.

Use GitHub's interface to make a fork of the repo and clone it to your local machine.

Add the Hummingbot repo as an upstream remote, and fetch upstream data:

Create your local branch and should follow this naming convention:

Create and switch to a new local branch called feat/[branch_name] based on development of the remote upstream.

Make commits to your branch and make sure that you only make relevant changes. If you find yourself making unrelated changes, create a new branch for those changes. Prefix each commit like so:

Commit message guidelines:

When you are done making changes, you can begin getting your code merged into the main repository. The first step is to rebase upstream changes into your branch.

This will start the rebase process. You must commit all of your changes before doing this. If there are no conflicts, this should roll all of your changes back on top of the changes from upstream, leading to an excellent, clean, linear commit history.

If there are conflicting changes, git will start yelling at you partway through the rebasing process. Then, git will pause rebasing to allow you to sort out the conflicts. You do this the same way you solve merge conflicts, by checking all of the files git says have been changed in both histories and picking the versions you want. Be aware that these changes will show up in your pull request, so try and incorporate upstream changes as much as possible.

You pick a file by git add ing it - you do not make commits during a rebase.

Make a clear pull request from your fork and branch to the upstream development branch, detailing exactly what changes you made and what feature this should add. The clearer your pull request is, the faster you can get your changes incorporated into this repository.

It is important to check Allow edits by maintainers for the Hummingbot team to update your branch with development whenever needed.

If the development team requests changes, you should make more commits to your branch to address these, then follow this process again from rebasing onwards.

Once you get back here, make a comment requesting a further review, and someone will look at your code again. If it addresses the requests, it will get merged. Else, repeat the process.

If you want your contribution to be reviewed, merged into the official Hummingbot codebase and included in ongoing monthly releases, you need to get a Proposal approved.

Create a new proposal in the appropriate Snapshot sub-space following the instructions on the Proposals page. Make sure that you have at least 200,000 HBOT to create a New Connector Proposal, or 1 HBOT for a Pull Request Proposal. The voting period is 7 days and the HBOT holders will decide if your proposal will be accepted or rejected.

Once the PRP is approved, your code will be tested by the QA team and if pass all the test Tech Review DAO will review the code.

Fix any changes requested by your reviewer, fix issues raised by a tester, and push your fixes as a single new commit.

Once the pull request has been reviewed and accepted; it will be merged by a member of the Hummingbot development team.

Tests are very important. Submit tests if your pull request contains new, testable behavior. See Unit test coverage for more information.

It is required to present a minimum 80% unit test coverage of all the changes included in a pull request. Some components are, however, excluded from this validation (for example all UI components).

To calculate the diff-coverage locally on your computer, run make development-diff-cover after running all tests.

This is to help you organize your process.

If you followed all of these guidelines and made good changes, you should have no problem getting your changes merged.

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/{user_github_handle}/hummingbot.git
```

Example 2 (unknown):
```unknown
git remote add upstream https://github.com/hummingbot/hummingbot.git
git fetch upstream
```

Example 3 (unknown):
```unknown
git checkout -b feat/[branch_name] upstream/development
```

Example 4 (unknown):
```unknown
git pull --rebase upstream development
```

---

## 2.7.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.7.0/

**Contents:**
- Hummingbot v2.7.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - 🔌 Hummingbot API¶
  - 🧰 Hummingbot API Client¶
  - 📊 Dashboard Update¶
  - 🧠 Headless Mode¶
  - Other Updates¶

Released on July 16, 2025

Other Hummingbot repositories such as Dashboard, Hummingbot-API (formerly backend-api), Hummingbot API Client, Quants-Lab, and Deploy follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

See the full changelogs on GitHub:

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

The backend-api has been renamed to hummingbot-api, marking a major revamp of the codebase with improvements in architecture, modularity, and developer experience.

⚙️ Standardized and production-ready API for managing bots, executing trades, and monitoring multi-exchange portfolios.

🔄 Expanded capabilities now include direct trading, portfolio rebalancing, and account management — all via API.

🤖 AI-ready design, enabling agentic trading workflows and seamless integration with LLMs like Claude.

📦 New repository: github.com/hummingbot/hummingbot-api

📚 Documentation: Hummingbot API Overview | Quickstart Guide

We introduce a modern, asynchronous Python client for interacting with the new Hummingbot API. Designed with modular router support to simplify integration with trading, portfolio, and bot management endpoints.

Built for developers creating custom tools, dashboards, and automation workflows.

Used as the interface layer in Hummingbot Dashboard v2.7.0.

🔗 GitHub: hummingbot-api-client

📦 PyPI: pypi.org/project/hummingbot-api-client

📚 Documentation: See examples in the API Quickstart Guide

Hummingbot Dashboard has been completely rebuilt to use the new Hummingbot API using the API Client, providing:

Enhanced Performance: Faster load times and more responsive UI through the new API architecture

Improved Reliability: Better error handling and connection management

Unified Backend: All operations now go through the standardized Hummingbot API

Future-Ready: Foundation for upcoming features like multi-user support and advanced portfolio analytics

All dashboard pages have been updated to work with the new architecture. Documentation updates for each page coming soon.

📚 Documentation: Dashboard Overview

Run Hummingbot without the graphical user interface (GUI), reducing memory usage by up to 40%. This lightweight mode enables you to deploy and manage more bots on resource-constrained environments, such as VPS or cloud instances.

To run in headless mode, use the quickstart script with the --headless flag: bin/hummingbot_quickstart.py --headless -p PASSWORD -f CONFIG_FILE_NAME [-c SCRIPT_CONFIG]

🔗 Pull Request: #7673

📚 Documentation: Headless Mode

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

Example 4 (unknown):
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
        direction LR
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

---

## 2.3.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.3.0/

**Contents:**
- Hummingbot v2.3.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - Ongoing Refactor of Gateway DEX Connectors¶
  - New Cross-Exchange Market Making (XEMM) V2 Controller¶
  - New GridStrike V2 Controller¶
  - New BingX Spot Connector¶
  - New Bitmart Perpetual Connector¶

Released on February 3, 2025

Other Hummingbot repositories such as Dashboard, Backend-API, Quant-Lab, and Deploy follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

See the full changelogs on GitHub:

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

With the exponential rise of DEX trading in recent months on Solana, the Gateway middleware needed to be refactored to support Solana DEXs, enable Concentrated Liquidity Market Making (CLMM) strategies, and modernize the tech stack. This is a multi-month effort to improve the Gateway middleware and make it more efficient, secure, and easier to maintain. See NCP-22 for more details.

In this release, we have streamlined the Gateway codebase to focus on two chain architectures: Solana and Ethereum. Ethereum L2 networks like Base along with EVM-compatible chains like Avalanche, Polygon, and BSC are now handled by the Ethereum chain connector, while Solana and other SVM-compatible chains are handled by the Solana chain connector. We have also refactored the Uniswap DEX connector to use this new Ethereum class and added a Jupiter DEX connector on Solana.

As part of the Gateway refactor, we've upgraded the underlying web framework from Express to Fastify. This modernization brings several key benefits including automatic OpenAPI/Swagger documentation generation for all API endpoints, significantly improved performance compared to Express, built-in request Typescript validation.

In the next release, we plan to add support for Meteora and Raydium as CLMM DEX connectors on Solana, and enhance the Uniswap connector with LP functionality. The Gateway middleware will standardize CLMM endpoints across all supported DEXs to provide a unified interface for liquidity provision. We will also publish comprehensive documentation to help the community migrate their custom DEX connectors to the new Gateway architecture.

Check out one of our recent weekly Youtube livestream demo to see the new Meteora connector in action!

Pull Requests: Hummingbot - #7367 | Gateway -#380

This release introduces a new V2-compatible version of the Cross Exchange Market Making (XEMM) strategy, one of Hummingbot's original core strategies. The new implementation provides users with greater flexibility and control over their market making activities across different exchanges. Users can now configure multiple order levels, monitor performance through Dashboard, and run multiple XEMM instances concurrently.

See the xemm_multiple_levels controller for the new implementation, which can be initialized with the v2_with_controllers script like other V2 controllers.

Pull Request: Hummingbot #7369

This release also introduces a new strategy, GridStrike, that combines aspects of grid trading, market making, and directional trading into a single advanced strategy. It allows users to maintain a grid of buy and sell orders around the current price of an asset with inventory-based risk management.

See the grid_strike controller for the new implementation, which can be initialized with the v2_with_controllers script like other V2 controllers.

Pull Request: Hummingbot #7374

This release adds support for BingX spot markets in Hummingbot #7280. This proposal was submitted by Robotter Labs in collaboration with BingX, aiming to enhance Hummingbot's capabilities by integrating BingX Exchange. See the BingX documentation for more information.

Thanks to danilo-robotter-ai for this contribution! 🙏

We are excited to announce the addition of Bitmart as a new exchange partner of Hummingbot Foundation. Bitmart is a leading global digital asset trading platform that provides spot and derivatives trading services to over 9 million users worldwide When you run Hummingbot on Bitmart, a portion of your trading fees automatically goes to support the Foundation at no additional cost to you.

This release adds support for a Bitmart perpetual connector in Hummingbot #7368 with the bounty, funded by the Bitmart team. See the Bitmart documentation for more information.

Thanks to tomasgaudino for this contribution! 🙏

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## 2.6.1 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.6.0/

**Contents:**
- Hummingbot v2.6.1 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - Gateway Refactor Updates¶
  - Improved Backtesting Performance¶
  - Controller Improvements¶
  - New XRPL Connector Guide¶
  - Improved MEXC Connector¶

Released on June 9, 2025

The Hummingbot client release was updated to v2.6.1 on June 12, 2025 to hot-fix critical issues with the market making controllers.

Other Hummingbot repositories such as Dashboard, Backend-API, Quant-Lab, and Deploy follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

See the full changelogs on GitHub:

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

This release makes substantial progress toward completing the Gateway simplification initiative approved in HGP-63, whichs to streamline Gateway's architecture and improve its maintainability. The refactor establishes a new standard for DEX connectors that significantly reduces complexity while improving performance and developer experience.

This release updates the Uniswap and Ethereum connectors to the new simplified standard, serving as reference implementations for future connector development. Additionally, this update completes the refactoring of Solana DEX connectors including Jupiter, Raydium, and Meteora.

Now that the refactor is complete, Hummingbot Foundation will publish bounties to refactor other Gateway connectors and review/merge pull requests to add other Ethereum Virtual Machine (EVM) and Solana Virtual Machine (SVM) based DEXs.

Updated Test Scripts:

The following scripts have been updated to test the refactored connectors:

The next release will introduce major improvements to transaction handling and the Hummingbot-Gateway communication interface:

This PR introduces significant performance improvements to the backtesting engine by optimizing timestamp-based lookups. The key changes include:

Replaced timestamp-based filtering with pandas datetime index lookups in ExecutorSimulation class, using searchsorted for efficient timestamp lookups (by far the most impactful change)

Modified BacktestingEngineBase to use datetime index for all timestamp operations

Updated both DCAExecutorSimulator and PositionExecutorSimulator to use datetime-based slicing instead of timestamp filtering

These changes have resulted in a performance improvement of over 40% in backtesting operations by:

Eliminating expensive DataFrame filtering operations

Leveraging pandas' optimized datetime index operations

Reducing memory usage by avoiding creation of intermediate filtered DataFrames

Special thanks to WuonParticle for this contribution! 🙏

Controller Framework & Strategy Enhancements

Added global stop-loss, per-strategy leverage support, and automatic position-reduction on opposite signals, giving V2 controllers stronger risk controls.

This release introduces a new statistical-arbitrage controller that continuously computes hedge ratios and Z-scores, maintains balanced paired orders, and uses live funding-rate data to fine-tune signals—streaming real-time metrics like hedge ratio, funding, and pair PnL throughout execution.

generic.basic_order_example simplified (async update loop, dynamic mid-price, lower default leverage)

Candle helpers and sample scripts updated to showcase the new API surface

Binance Connector Reliability Improvements (Perpetual & Spot)

We've published a comprehensive guide on using the XRP Ledger (XRPL) connector with Hummingbot. The guide covers:

Check out the full guide: Using XRP Ledger with Hummingbot

This release includes significant improvements to the MEXC connector's reliability and stability:

These improvements make the MEXC connector more reliable for long-running trading sessions and reduce the likelihood of unexpected disconnections.

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## 2.5.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.5.0/

**Contents:**
- Hummingbot v2.5.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - conda Environment Upgrade¶
  - PMM Controller and PositionsHeld¶
  - Gateway New vs Legacy¶
  - Improvements to Existing Exchange Connectors¶
  - Other Updates¶

Released on April 21, 2025

Other Hummingbot repositories such as Dashboard, Backend-API, Quant-Lab, and Deploy follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

See the full changelogs on GitHub:

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

The latest update upgrades Hummingbot's core environment to Python 3.12, bringing performance improvements and modern language features. The Anaconda/Miniconda environment has been streamlined to rely primarily on native conda packages, simplifying setup and maintenance. This upgrade makes Hummingbot faster and enables the use of modern Python libraries.

Key libraries, including Pydantic (now V2), have been updated to for better performance and compatibility. Additionally, test suites now utilize Python's asyncio framework, enhancing testing efficiency and reliability.

Special thanks to MementoRC for this huge contribution! 🙏

The latest release introduces a new feature in the Strategy V2 framework: PositionsHeld, which tracks a global set of spot balances and perpetual positions held by stopped Executors. StopExecutorAction can now be called with keep_position=true to maintain positions after stopping execution.

This new feature can be used by any strategy, and is ideal for market making strategies. It allows a strategy to track an inventory position that includes the amounts held for each asset and the unrealized P&L of each position, enabling more sophisticated strategies that skew prices and spreads based on inventory held.

This release also adds a new PMM Controller, a new strategy that leverages the PositionsHeld feature to provide a modernized V2 version of the Pure Market Making V1 strategy.

To learn more about how to use the PMM Controller, watch these recent Hummingbot livestream :

The 2.5 release introduces significant architectural changes to how the Hummingbot client interacts with Gateway, marking a major evolution in the platform's capabilities.

Legacy Gateway (v2.2)

For installation, refer to:

Pull Request: Hummingbot | Gateway

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## 2.8.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.8.0/

**Contents:**
- Hummingbot v2.8.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - 🔗 Gateway 2.8.0 - Major Architecture Refactor¶
    - 🏗️ Architecture Overhaul¶
    - 🎮 Gateway Commands in Hummingbot¶
    - 🔄 Revamped DEX Connectors¶
    - 🛠️ Legacy Connector Updates¶

Released on August 21, 2025

Other Hummingbot repositories such as Dashboard, Hummingbot-API, Hummingbot API Client, Quants-Lab, Deploy and the newly released Hummingbot MCP follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

See the full changelogs on GitHub:

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

This release completes the NCP-22 Gateway refactor, introducing a completely revamped architecture with standardized schemas, native Gateway commands in Hummingbot, and modernized DEX connectors.

Standardized Schemas: Implemented three universal trading schemas across all DEX connectors:

New Configuration System:

Added comprehensive Gateway commands directly in the Hummingbot client:

Standardized existing Gateway connectors to align with the new architecture. The following connectors are ready for v2.8.0 schema implementation with bounties available:

See the DEX Connectors page for full details on upgrading these connectors to the v2.8.0 standard.

For users upgrading from Gateway v2.7 or earlier, see the Gateway Installation Guide for complete setup instructions.

We introduced the Hummingbot MCP (Model Context Protocol) Server, a new server module that connects Hummingbot with AI agents, automation frameworks, and external tools via the MCP standard.

📦 Repository: github.com/hummingbot/mcp

📚 Documentation: Hummingbot MCP Overview

hummingbot/hummingbot-api

hummingbot/hummingbot

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## Certification - Hummingbot

**URL:** https://hummingbot.org/certification

**Contents:**
- Certification
- Benefits of Certification¶
- Certification Process¶
  - 1. Submit Strategy Template and Video¶
  - 2. Pass Review by Hummingbot Maintainers¶
  - 3. Present at Demo Day¶

Hummingbot certified market makers and strategy developers have successfully completed a Hummingbot Botcamp cohort, demonstrating their ability to design, code, and present a custom trading strategy.

Watch the Demo Day video from the last cohort (Cohort 11):

See Certifications List for current certified developers.

Earning your Hummingbot certificate offers several valuable benefits:

Botcamp Member Profile: Your personal profile will be featured on botcamp.xyz/members, showcasing your skills, strategies, and achievements to the broader community. This public profile serves as a portfolio of your work and helps you connect with potential employers, collaborators, and bounty sponsors.

NFT Certificate: Upon completion of the certification process, you'll receive a unique certificate in the form of an Ethereum NFT. This serves as formal recognition of your skills and achievements in the Hummingbot ecosystem. Here are examples of the NFT certificates provided to a recent batch of Botcamp graduates: Cohort 9 NFTs. The top strategy presenters in each cohort also receive an additional Cohort MVP NFT.

Certifications List: Your name and credentials will be included in the master list of certified developers. This list is maintained on the Hummingbot website and serves as a public record of all certified developers. Being listed here can increase your visibility within the community and enhance your credibility as a Hummingbot developer to potential employers and bounty sponsors.

LinkedIn Certification: You'll be able to add your Hummingbot certification to your LinkedIn profile, showcasing your skills on this professional networking platform. For more information on adding the certification to LinkedIn, see LinkedIn's help article or this walkthrough.

Discord Badge: You'll receive special certification badge(s) on the Hummingbot Discord server. This badge system integrates with Discord's role system, giving you special recognition within the Hummingbot community. It's a great way to showcase your expertise and connect with other certified developers.

The Hummingbot certification process is designed to be comprehensive and challenging, ensuring that participants have the skills to code and operate custom algorithmic trading strategies. This process is overseen by the core maintainers of the Hummingbot codebase.

The certification process involves completing a Hummingbot Botcamp cohort and submitting a strategy template and video for presentation at Demo Day. Botcamp members can also submit strategies for certification after their cohort ends, allowing them to continue building and refining their trading strategies.

Botcamp participants are expected to:

After submitting their strategy template and video, Hummingbot maintainers will evaluate the work based on the following criteria:

After the review process, the accepted strategies are presented at Demo Day, the capstone event for each Botcamp cohort.

Past Demo Day presentations can be viewed on the Hummingbot YouTube channel.

---

## 2.1.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.1.0/

**Contents:**
- Hummingbot v2.1.0 Release Notes¶
- Introduction¶
- How to Update¶
  - Docker¶
  - Source¶
- Hummingbot 2.1.0 Highlights¶
  - CEX Connector Improvements¶
  - V2 Framework Enhancements¶
  - Updated Dexalot Connector¶
  - New DEX Connectors¶

Released on October 28, 2024

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master

The bybit_perpetual connector has been upgraded to use the latest v5 API version, aligning it with the spot connector in #7196. Thanks to tomasgaudino for this fix! 🙏

Enhanced coinbase_advanced_trade connector with improved reliability and performance in #7220. Thanks to isreallee82 for this contribution! 🙏

Several core improvements have been made to the V2 Framework:

This release introduces a fully Python-based implementation of the Dexalot connector, removing the Gateway dependency in #7219. Users can now:

We added support for ETCSwap on Ethereum Classic, expanding DEX trading options for users in #340.

Based on approval from community voting, the Tegro exchange connector was added in #7148.

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master
```

---

## 2.2.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.2.0/

**Contents:**
- Hummingbot v2.2.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - New Solana and Jupiter DEX Connectors¶
  - New Hyperliquid Spot Connector¶
  - New Arbitrage Controller¶
  - New GridStrike Controller¶
  - Improvements to Existing Exchange Connectors¶

Released on December 26, 2024

The Dashboard, Backend-API, and Deploy repositories will now follow a continuous deployment model without fixed version releases. This approach allows for more frequent updates and improved maintainability of these components.

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

In this release, Hummingbot #7334 & Gateway #374 introduces new connectors for the Solana blockchain and the Jupiter DEX aggregator to the Gateway middleware, along with a Solana class in the Hummingbot client to interface with them.

Users can now use the Arbitrage Controller (see below) or the AMM arbitrage V1 strategy to run arbitrage strategies between Jupiter and other Hummingbot-supported exchanges. See the Jupiter documentation for more information.

This release adds support for Hyperliquid spot markets in Hummingbot #7282, funded by the Hyperliquid Connector Pot voted by the HBOT token holders in quarterly polls. See the Hyperliquid documentation for more information.

Thanks to isreallee82 for this contribution! 🙏

The new Arbitrage controller is a revamped V2 version of our legacy arbitrage strategies. It enables high-performance arbitrage trading between any two spot exchanges (AMM or CLOB), using the new ArbitrageExecutor component to manage order execution.

The strategy includes several key features:

Similarly, rhe new GridStrike Strategy V2 controller introduces a classic grid strategy to the V2 framework that allows users to create and maintain a grid of orders within specified price ranges, and uses the new GridExecutor component to manage them.

The strategy includes several key features:

Pull Requests: Hummingbot #7285 | Backend-API #46 | Dashboard #190.

Dexalot: The dexalot connector has been upgraded to the latest API version in #7291. Thanks to yancong001 for this contribution! 🙏

Bybit: Improved the bybit_perpetual balance fetching in #7279. Thanks to tomasgaudino for this fix! 🙏

Binance: Fixed the binance websocket reconnection issue in #7310. Thanks to komposter for this fix! 🙏

Hyperliquid: The issue with the hyperliquid auth exemption for public data has been fixed in #7328. Thanks to isreallee82 for this fix! 🙏

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## 2.9.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.9.0

**Contents:**
- Hummingbot v2.9.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - ✨ Updated Quants Lab for R&D¶
  - 🥞 PancakeSwap Connector¶
  - 🚀 RPC Provider Abstraction System¶
  - 🏗️ Connector Architecture Improvements¶
  - Other Updates¶

Released on September 24, 2025

See the full changelogs on GitHub:

Other Hummingbot repositories such as Dashboard, Hummingbot-API, Hummingbot API Client, Quants-Lab, Deploy and Hummingbot MCP follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

We've completely overhauled the hummingbot/quants-lab repository, transforming it into a comprehensive platform for quantitative trading research. This refactor includes a reorganized codebase, a new task scheduling system, Telegram/Discord/email notifications, and example Jupyter notebooks for data collection, screeners, notifiers, and other tasks.

See the Quants Lab Documentation for detailed information and installation guide.

We have refactored and restored the PancakeSwap connector to Gateway, enabling trading and liquidity provision using the modernized Gateway architecture on the largest DEX on BNB Chain and other EVM networks.

This connector was built by vic-en as part of a HBOT bounty. Thanks @vic-en for this contribution! 🙏

After #506 and #508, Gateway now features a flexible RPC provider abstraction system that significantly improves blockchain connectivity and performance for DEX trading. This system allows you to easily switch between standard RPC endpoints and specialized providers optimized for specific networks, ensuring low latency, high availability, and accurate blockchain data.

See the RPC Provider Configuration Guide for detailed setup instructions and supported networks.

In #7742, we've completed a major architectural refactor to decouple exchange connectors from the global configuration system, making them more modular and easier to use across different Hummingbot components and external applications.

This change is primarily architectural and doesn't affect the user experience in the main Hummingbot client, but significantly improves developer experience when building with Hummingbot components.

hummingbot/hummingbot

hummingbot/hummingbot-api

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## 2.4.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.4.0/

**Contents:**
- Hummingbot v2.4.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - New Solana DEX Connectors¶
  - Core Environment Upgrade and Tests¶
  - New Derive Spot and Perpetual Connector¶
  - Improvements to Existing Exchange Connectors¶
  - Other Updates¶

Released on March 3, 2025

Other Hummingbot repositories such as Dashboard, Backend-API, Quant-Lab, and Deploy follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

See the full changelogs on GitHub:

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

With the continuous refactor of Gateway approved in NCP-22, this release introduces new connectors for Solana DEXs Meteora and Raydium, as well as standardized request and response interfaces for CLMM, AMM, and Swap request and responses in Gateway. In addition, Gateway can now be used as a standalone CLI. This marks a significant step towards a flexible yet standardized blueprint for adding back past Gateway connectors and supporting future DEX connectors.

The next release (2.5.0) will begin modifying the Hummingbot client to take advantage of the new CLMM and AMM connectors in Gateway, including sample Hummingbot scripts leveraging that showcase how traders can build effective strategies using these new components. As a preview, check out the video demo below for a Hummingbot script that automate Meteora LP positions by dynamically opens, monitors, and closes positions based on user-defined parameters.

Pull Requests: Hummingbot - #7457 | Gateway -#403

This release introduces significant updates to modernize the Hummingbot environment and improve its performance and maintainability. It replaces the outdated nose test framework with pytest, removes the legacy, deprecated Telegram integration in preparation for an forthcoming update, and upgrades important libraries like Pydantic for faster performance. Collectively, these changes streamline dependency management, provide a more robust and modern testing suite, and make the codebase leaner and easier to maintain.

Pull Request: Hummingbot #7403

This release adds support for spot and perpetual connectors to Derive, a decentralized CLOB trading protocol. See pull request Hummingbot #7432 which was supported by a bounty funded by the Derive team.

While the bounty was just for the CLOB perpetual connector, the developer also generously added the CLO spot connector in Hummingbot #7383. Thanks to isreallee82 for this contribution! 🙏

See the Derive documentation for more information.

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## 2.9.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.9.0/

**Contents:**
- Hummingbot v2.9.0 Release Notes¶
- How to Update¶
  - Docker¶
  - Source¶
- Release Highlights¶
  - ✨ Updated Quants Lab for R&D¶
  - 🥞 PancakeSwap Connector¶
  - 🚀 RPC Provider Abstraction System¶
  - 🏗️ Connector Architecture Improvements¶
  - Other Updates¶

Released on September 24, 2025

See the full changelogs on GitHub:

Other Hummingbot repositories such as Dashboard, Hummingbot-API, Hummingbot API Client, Quants-Lab, Deploy and Hummingbot MCP follow a continuous deployment model without fixed version releases. Use the main branch for these repositories.

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master # Hummingbot git pull origin main # Gateway

Afterwards, follow the instructions to re-install dependencies and compile the codebase for each repository. See Install Hummingbot from Source and Install Gateway from Source.

We've completely overhauled the hummingbot/quants-lab repository, transforming it into a comprehensive platform for quantitative trading research. This refactor includes a reorganized codebase, a new task scheduling system, Telegram/Discord/email notifications, and example Jupyter notebooks for data collection, screeners, notifiers, and other tasks.

See the Quants Lab Documentation for detailed information and installation guide.

We have refactored and restored the PancakeSwap connector to Gateway, enabling trading and liquidity provision using the modernized Gateway architecture on the largest DEX on BNB Chain and other EVM networks.

This connector was built by vic-en as part of a HBOT bounty. Thanks @vic-en for this contribution! 🙏

After #506 and #508, Gateway now features a flexible RPC provider abstraction system that significantly improves blockchain connectivity and performance for DEX trading. This system allows you to easily switch between standard RPC endpoints and specialized providers optimized for specific networks, ensuring low latency, high availability, and accurate blockchain data.

See the RPC Provider Configuration Guide for detailed setup instructions and supported networks.

In #7742, we've completed a major architectural refactor to decouple exchange connectors from the global configuration system, making them more modular and easier to use across different Hummingbot components and external applications.

This change is primarily architectural and doesn't affect the user experience in the main Hummingbot client, but significantly improves developer experience when building with Hummingbot components.

hummingbot/hummingbot

hummingbot/hummingbot-api

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 2 (unknown):
```unknown
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

Example 3 (unknown):
```unknown
git pull origin master # Hummingbot
git pull origin main # Gateway
```

---

## 1.9.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/1.9.0/

**Contents:**
- Release Notes - Version 1.9.0¶
- New Sample Scripts from Botcamp¶
- New Connector: Eve Exchange¶
- New Community Tool: Manage Bot Cycles¶
- All Changes¶
  - Developer updates¶
  - Gateway updates¶
  - Bug fixes¶

Released on October 28, 2022

We are very excited to ship the October 2022 Hummingbot release (v1.9.0) today!

We're excited to launch Botcamp, an intensive 4-week bootcamp that teaches you to create custom trading strategies as simple Hummingbot scripts.

This release added script examples created by participants in the beta Botcamp cohort:

All scripts examples can be found here.

Eve brings together all the necessary features for individuals & businesses to harness the power of crypto, in a single low-cost platform — powered by EVE token.

The purpose of this folder structure and scripts is to make it easier to manage multiple bots and launch them all at once on your computer or server.

Thanks to mlguys for this contribution! 🙏

https://github.com/hummingbot/community-tools

---
