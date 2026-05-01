# Hummingbot - Getting Started

**Pages:** 24

---

## Broker - Hummingbot

**URL:** https://hummingbot.org/installation/orchestration

**Contents:**
- Broker
- Phase I¶
- Phase II¶
- Future phases¶

Hummingbot's brokers module allows for remote control and monitoring of multi-bot environments in a distributed context , so that bots can "live" on different machines and infrastructures (e.g. having a bot local and another bot on AWS).

To achieve this approach, there is an MQTT layer for bots to connect remotely to message brokers, as a single point of reference, using asynchronous bidirectional communication channels (push/pull). In this architecture, bots can be considered as clients to the overall environment. Bot scaling is seamless and does not require any further setup, anyone can connect any number of bots the a message broker (e.g. RabbitMQ, EMQX etc) without any other dependencies.

See the following repos for more information:

Watch the February 2023 community call that contains a demo of this feature:

Thanks to klpanagi and TheHolyRoger for your work! 🙏

In this Phase, an event and data layer will be integrated into the Hummingbot codebase to support receiving and handling remote events via the message broker (MQTT), such as the case of TradingView signals.

An MQTTEventListener will be developed and integrated into the hummingbot codebase, which will provide configuration for setting the URIs of the events to listen on. Upon receiving an event, a handling callback provided by the user/developer will be executed by the MQTTEventListener, so that users operate/develop their strategy based on the input event.

See this Notion doc for an overview of the project. This is an ongoing project funded by Proposal HIP-20.

---

## Installation - Hummingbot

**URL:** https://hummingbot.org/hummingbot-api/installation/

**Contents:**
- Installation¶
- Prerequisites¶
- Install with Docker (Recommended)¶
  - 1. Clone the repository¶
  - 2. Run the setup script¶
  - 3. Start the API¶
- Install from Source (for Developers)¶
  - 1. Clone and setup¶
  - 2. Install dependencies¶
  - 3. Start the API in development mode¶

This guide covers all available installation methods for Hummingbot API.

The easiest way to get started with Hummingbot API is using Docker.

The setup script will:

Default credentials if you press Enter: admin / admin

This pulls the required Docker images and runs Hummingbot API using Docker Compose and the configuration defined in the docker-compose.yml file.

The API will be accessible at http://localhost:8000. You can view the interactive Swagger UI documentation at http://localhost:8000/docs.

If you're developing or contributing to Hummingbot API, you can install from source.

This starts the Broker and Postgres DB containers and runs the API using uvicorn with auto-reload enabled for development.

The API will be accessible at http://localhost:8000.

The Hummingbot API Client is a Python library that provides a convenient interface for interacting with the Hummingbot API.

Once installed, you can verify the API is running:

Open your browser and navigate to: - Interactive API docs: http://localhost:8000/docs - Alternative API docs: http://localhost:8000/redoc

The installation creates a .env file with your configuration. You can modify these settings:

If Docker containers fail to start:

If port 8000 is already in use on your system, you can change it by modifying the configuration depending on your setup:

Update the ports mapping in your docker-compose.yml file to use a different external port. For example, to use port 8001 instead:

Edit the ./run.sh script to include the --port flag in the uvicorn command. For example, to run on port 8001:

Make sure the new port you choose is not already in use.

For source installation issues:

After installation, proceed to the Quickstart Guide to learn how to:

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot-api
cd hummingbot-api
```

Example 2 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot-api
cd hummingbot-api
./setup.sh
```

Example 3 (unknown):
```unknown
make install
```

Example 4 (unknown):
```unknown
./run.sh --dev
```

---

## Install via Docker - Hummingbot

**URL:** https://hummingbot.org/installation

**Contents:**
- Install via Docker
- Install Docker Compose¶
- Installation (Client Only)¶
  - Clone Hummingbot Repo¶
  - Launch Hummingbot¶
  - Attach to Instance¶
- Dev Branch | Older Versions¶
  - Development Branch¶
  - Previous Versions¶
- Gateway: Required for DEX Trading¶

We recommend installing Hummingbot using Docker if you want the simplest, easiest installation method and don't need to modify the Hummingbot codebase.

Hummingbot uses Docker Compose, a tool for defining and running multi-container Docker applications.

Install Docker Desktop from the official Docker website

Desktop Users: Install Docker Desktop from official site

Headless Servers (VPS like AWS EC2 or Digital Ocean): curl -fsSL https://get.docker.com -o get-docker.sh sh get-docker.sh

Always run commands in: Ubuntu Terminal (Start Menu → Ubuntu)

These instructions help you launch the standalone Hummingbot client.

Open a terminal and run the following commands to clone the Hummingbot Github repo and enter the root folder:

This will start to download the latest Hummingbot image if it's not already on your system.

The -d flag runs Hummingbot in detached mode. Attach to it by running the command:

You should now see the Hummingbot welcome screen:

To get started with Hummingbot, check out the following pages and guides:

If you need to install the development branch or an older version of Hummingbot, follow these steps:

To use the latest development version, browse to the hummingbot folder and open the docker-compose.yml file using any text editor. Look for the image field, and replace latest with development.

To install a specific older version, replace the image field with the desired version. The version tags will follow this format: version-x.x.x For example, to install version 2.0.0, replace the image field with:

Essential for Decentralized Exchanges

Gateway must be installed separately to trade on these supported DEXs: - Uniswap (Ethereum) - PancakeSwap (BNB Chain) - Trader Joe (Avalanche) - dYdX (Starkware) - And 30+ others

Gateway acts as middleware that enables Hummingbot to interact with blockchain-based decentralized exchanges. To set up, follow the instructions in Gateway - Installation to generate certificates and connect Gateway to Hummingbot.

**Examples:**

Example 1 (unknown):
```unknown
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

Example 2 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot.git
  cd hummingbot
```

Example 3 (unknown):
```unknown
docker compose up -d
```

Example 4 (unknown):
```unknown
docker attach hummingbot
```

---

## Install via Source - Hummingbot

**URL:** https://hummingbot.org/installation/source/

**Contents:**
- Install from Source¶
- Install Dependencies¶
  - 🛠️ macOS Setup Instructions¶
    - ✅ Install Xcode Command Line Tools¶
    - ✅ Install Anaconda (Recommended for macOS)¶
  - 🔹 Option 1: Graphical Installer (Beginner-Friendly)¶
  - 🔹 Option 2: Command Line Installer¶
  - 🐧 Linux Setup Instructions¶
    - ✅ Install/Update System Packages¶
    - ✅ Install Anaconda¶

This method is recommended for developers and users who need to modify Hummingbot's source code. Most users should prefer Docker installation.

These are essential for compiling some Python dependencies.

We recommend using the full Anaconda distribution instead of lighter alternatives like Miniconda. Anaconda includes a broader set of preinstalled packages, which helps prevent dependency conflicts and installation errors commonly encountered with Miniconda.

You can install Anaconda using either the graphical interface or the command line.

Use this method if you're comfortable with the terminal.

For macOS with Intel (x86): curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-x86_64.sh bash Anaconda3-2024.10-1-MacOSX-x86_64.sh

For macOS with Apple Silicon (M1/M2/M3): curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-arm64.sh bash Anaconda3-2024.10-1-MacOSX-arm64.sh

This may take a while to complete and may require a system restart.

Once the Ubuntu distribution is installed, open the Ubuntu terminal and follow the instructions in the Linux section to install the dependencies.

Run all install commands below in an Ubuntu terminal, not Windows Command Prompt or PowerShell.

Clone the repository git clone https://github.com/hummingbot/hummingbot.git cd hummingbot

Install the environment and dependencies ./install

Activate the environment conda activate hummingbot

Compile the code ./compile

Launch Hummingbot ./start

You should see the Hummingbot welcome screen:

To get started with Hummingbot, check out the following pages and guides:

If you need to install the development branch or an older version of Hummingbot, follow these steps:

To use the latest development version, first clone the repository and then switch to the development branch:

To install a specific older version, first list the available tags to find the correct version:

Once you've identified the desired version (e.g., v2.1.0), switch to it using:

The tags for previous versions follow this format: vx.x.x (e.g., v2.1.0).

Essential for Decentralized Exchanges

Gateway must be installed separately to trade on these supported DEXs: - Uniswap (Ethereum) - PancakeSwap (BNB Chain) - Trader Joe (Avalanche) - dYdX (Starkware) - And 30+ others

Gateway acts as middleware that enables Hummingbot to interact with blockchain-based decentralized exchanges. To set up, follow the instructions in Gateway - Installation to generate certificates and connect Gateway to Hummingbot.

**Examples:**

Example 1 (unknown):
```unknown
xcode-select --install
```

Example 2 (unknown):
```unknown
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-x86_64.sh
bash Anaconda3-2024.10-1-MacOSX-x86_64.sh
```

Example 3 (unknown):
```unknown
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-arm64.sh
bash Anaconda3-2024.10-1-MacOSX-arm64.sh
```

Example 4 (unknown):
```unknown
sudo apt update && sudo apt upgrade -y && sudo apt install -y gcc build-essential
```

---

## 1.16.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/1.16.0/

**Contents:**
- Release Notes - Version 1.16.0¶
- Community Call Recaps¶
- Hummingbot Dashboard¶
- Installation Improvements¶
- Market Orders Support¶
- New Bounties Documentation¶
- New Script Examples¶
- New Chain/DEX Connectors: Algorand/Tinyman¶
- New SPOT CEX Connector: Foxbit¶
- New PERP CEX Connector: Phemex¶

Released on May 29, 2023

We are very excited to ship the May 2023 release of Hummingbot (v1.16.0) today!

This release adds the first iteration of Hummingbot Dashboard, a powerful new way to visualize and analyze your strategies. It also greatly simplifies the Docker installation process, added market orders support to top exchange connectors, and introduces connectors to the Algorand blockchain, Phemex, and more!

New trades DB columns

This release adds new columns to the trades database stored for each strategy/script to support the new Hummingbot Dashboard. As a result, we recommend that if you are updating from an older version of Hummingbot and want to run an strategy created using that older version, you should back up and delete the associated .sqlite file related to that strategy located in the /data folder. Failure to do so may result in errors upon re-starting the strategy.

Gateway users will also need to update Gateway to v1.16 after updating the Hummingbot client and then run the gateway-setup script to regenerate your configs then re-run the gateway connect ... command again from within Hummingbot. Otherwise, you'll get an error message about "Unhandled error in background task: 'chain_type'" when running Gateway.

With this release, Hummingbot now offers a multi-arch Docker image that supports both x86 and arm64 architectures. Users no longer need to download a separate Docker image for ARM builds.

See below for what's new this month!

In the last Community Call, Mike discussed the highlights from the v1.15.0 release, the new Bounties initiative, & community member TheHolyRoger presented Phase 2 of the Orchestration Module:

In the last How-To Call, Fede discussed how to use Hummingbot's Telegram integration in conjunction with custom scripts and deployments:

Each month, we livestream two community calls on our Discord server:

Check out the Hummingbot Events Calendar for links to these monthly calls and other upcoming events.

Formerly called Streamlit-Apps, the new Hummingbot Dashboard lets you visualize and analyze a strategy, even as it's running in real-time.

This is an experimental new module that we are still prototyping, and we welcome the community to test out and provide feedback. We plan to make significant improvements to this dashboard in the next few releases.

We have streamlined the installation process so that there is a single environment.yml file in the setup folder. In addition, the Hummingbot Docker image can now be built using a simple command for multiple architectures, making it more accessible across a range of systems, including x86 and ARM architectures. These modifications are expected to enhance the overall user experience by simplifying the setup process and making Hummingbot more adaptable across a wide range of systems.

Pull Request: #6229, #6297

Following our Technical Roadmap, we are expanding our connectors to support to include all order types offered by an exchange. In this release, we and community developers have added the integration of market_order and limit_maker_order types for the following exchanges:

Pull Request: #6279, #6305, #6308

Bounties offer a platform for those seeking development work on exchange connectors, strategies, bug fixes, and more to connect with skilled developers capable of building these solutions.

Check out our new guides for prospective Contributors and Sponsors:

This release added the following new Script examples and improvements to existing ones:

1overN_portfolio: This strategy aims to create a 1/N cryptocurrency portfolio, providing perfect diversification without parametrization and giving a reasonable baseline performance. Thanks to Botcamp member Roland Kofler for this contribution! 🙏

spot_perp_arb: This script improves upon and addresses problems with the current spot perp arbitrage strategy. It is designed to simultaneously initiate a long position in the spot market and a short position in the perpetual market when the opening signal is triggered. These positions are then closed upon receiving the closing signal. The profit is generated from the corrective motion between the spot price and the perpetual price. Thanks to Botcamp member riven314 for this contribution! 🙏

download_candles.py: This script was improved by incorporating the capacity to download data across various intervals, thereby allowing simultaneous access to multiple timeframes. Pull Request: #6289

Algorand a fully decentralized, secure, and scalable blockchain which provides a common platform for building products and services for a borderless economy. Tinyman is a decentralized trading protocol which utilizes the fast and secure framework of the Algorand blockchain.

See Algorand for the chain docs and the Tinyman exchange connector docs.

Pull Requests: #6277, #0090

Snapshot Proposal: https://snapshot.org/#/hbot-prp.eth/proposal/0x08a53dead66043ee8e8b0e65229a99b52be2e212a640e992eb72c9b4cd388701

Thanks to CoinAlpha for this contribution! 🙏

Foxbit is a leading cryptocurrency trading platform recognized for its high liquidity in the Brazilian market. Founded in 2014, Foxbit is built on the principles of agility, transparency, and security, and is primarily geared towards Brazil-based users offering rapid Bitcoin trading with a 0% deposit fee against the Brazilian Real.

See the Foxbit connector documentation for more information.

Snapshot Proposal: https://snapshot.org/#/hbot-prp.eth/proposal/0x8bb5b1341970a59988e3bcf635e3576c48f0ca3a0d1d86b9463b8be0b44d00b8

Thanks to mfavareto-vitra for this contribution! 🙏

Phemex is a crypto derivatives trading exchange. Based in Singapore, it was launched in 2019 by former executives from Morgan Stanley. The project is rapidly gaining popularity due to low fees and deep liquidity, offering user-friendly charting and wallet interface, no-KYC, tight/fast execution spreads, as well as spot, contract, and margin trading.

See the Phemex Perpetual connector documentation for more information.

Snapshot Proposal: https://snapshot.org/#/hbot-prp.eth/proposal/0x6f4f16e7cebffe5258138b841963849d9a9d185e5afa714c5d769687c0ed8899

Thanks to CoinAlpha for this contribution! 🙏

---

## Install via Docker - Hummingbot

**URL:** https://hummingbot.org/installation/docker

**Contents:**
- Install via Docker
- Install Docker Compose¶
- Installation (Client Only)¶
  - Clone Hummingbot Repo¶
  - Launch Hummingbot¶
  - Attach to Instance¶
- Dev Branch | Older Versions¶
  - Development Branch¶
  - Previous Versions¶
- Gateway: Required for DEX Trading¶

We recommend installing Hummingbot using Docker if you want the simplest, easiest installation method and don't need to modify the Hummingbot codebase.

Hummingbot uses Docker Compose, a tool for defining and running multi-container Docker applications.

Install Docker Desktop from the official Docker website

Desktop Users: Install Docker Desktop from official site

Headless Servers (VPS like AWS EC2 or Digital Ocean): curl -fsSL https://get.docker.com -o get-docker.sh sh get-docker.sh

Always run commands in: Ubuntu Terminal (Start Menu → Ubuntu)

These instructions help you launch the standalone Hummingbot client.

Open a terminal and run the following commands to clone the Hummingbot Github repo and enter the root folder:

This will start to download the latest Hummingbot image if it's not already on your system.

The -d flag runs Hummingbot in detached mode. Attach to it by running the command:

You should now see the Hummingbot welcome screen:

To get started with Hummingbot, check out the following pages and guides:

If you need to install the development branch or an older version of Hummingbot, follow these steps:

To use the latest development version, browse to the hummingbot folder and open the docker-compose.yml file using any text editor. Look for the image field, and replace latest with development.

To install a specific older version, replace the image field with the desired version. The version tags will follow this format: version-x.x.x For example, to install version 2.0.0, replace the image field with:

Essential for Decentralized Exchanges

Gateway must be installed separately to trade on these supported DEXs: - Uniswap (Ethereum) - PancakeSwap (BNB Chain) - Trader Joe (Avalanche) - dYdX (Starkware) - And 30+ others

Gateway acts as middleware that enables Hummingbot to interact with blockchain-based decentralized exchanges. To set up, follow the instructions in Gateway - Installation to generate certificates and connect Gateway to Hummingbot.

**Examples:**

Example 1 (unknown):
```unknown
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

Example 2 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot.git
  cd hummingbot
```

Example 3 (unknown):
```unknown
docker compose up -d
```

Example 4 (unknown):
```unknown
docker attach hummingbot
```

---

## Perp Connector Developer Checklist - Hummingbot

**URL:** https://hummingbot.org/developers/connectors/perp-connector-checklist/

**Contents:**
- Perpetual Connector v2.1¶
- Prerequisites¶
- API Checklist¶
- Build Process¶
  - Constants¶
  - Web Utils¶
  - Utils¶
  - Order Book Data Source¶
  - Auth¶
  - User Stream Data Source¶

Before proceeding with the setup of the Spot Connector, ensure that you have the Hummingbot source version installed on your system. Follow the detailed installation instructions provided at Hummingbot Installation Guide.

Add to the constant files the following variables

connector_name_api_order_book_data_source.py

test_connector_name_api_order_book_data_source.py

Now we are going to start implementing the functionalities of the Order Book Data source but in a TDD way.

listen_for_subscriptions

listen_for_order_book_diffs

listen_for_order_book_snapshots

listen_for_funding_info

test_connector_name_auth.py

connector_name_api_user_stream_data_source.py

test_connector_name_api_user_stream_data_source.py

Now we are going to start implementing the functionalities of the User Stream Data source but in a TDD way.

If you need Listen Key:

listen_for_user_stream

connector_name_exchange.py

test_connector_name_exchange.py

A lot of test are already in the Generic test class! But you have to implement some methods to let it work.

Methods for the Generic test class

Methods to implement of ExchangePyBase

Methods to implement of PerpetualDerivativePyBase

update_time_synchronizer

_user_stream_event_listener

Add connector_name_api_key and connector_name_api_secret to the conf_global_TEMPLATE.yml

---

## Installation - Hummingbot

**URL:** https://hummingbot.org/hummingbot-api/installation

**Contents:**
- Installation¶
- Prerequisites¶
- Install with Docker (Recommended)¶
  - 1. Clone the repository¶
  - 2. Run the setup script¶
  - 3. Start the API¶
- Install from Source (for Developers)¶
  - 1. Clone and setup¶
  - 2. Install dependencies¶
  - 3. Start the API in development mode¶

This guide covers all available installation methods for Hummingbot API.

The easiest way to get started with Hummingbot API is using Docker.

The setup script will:

Default credentials if you press Enter: admin / admin

This pulls the required Docker images and runs Hummingbot API using Docker Compose and the configuration defined in the docker-compose.yml file.

The API will be accessible at http://localhost:8000. You can view the interactive Swagger UI documentation at http://localhost:8000/docs.

If you're developing or contributing to Hummingbot API, you can install from source.

This starts the Broker and Postgres DB containers and runs the API using uvicorn with auto-reload enabled for development.

The API will be accessible at http://localhost:8000.

The Hummingbot API Client is a Python library that provides a convenient interface for interacting with the Hummingbot API.

Once installed, you can verify the API is running:

Open your browser and navigate to: - Interactive API docs: http://localhost:8000/docs - Alternative API docs: http://localhost:8000/redoc

The installation creates a .env file with your configuration. You can modify these settings:

If Docker containers fail to start:

If port 8000 is already in use on your system, you can change it by modifying the configuration depending on your setup:

Update the ports mapping in your docker-compose.yml file to use a different external port. For example, to use port 8001 instead:

Edit the ./run.sh script to include the --port flag in the uvicorn command. For example, to run on port 8001:

Make sure the new port you choose is not already in use.

For source installation issues:

After installation, proceed to the Quickstart Guide to learn how to:

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot-api
cd hummingbot-api
```

Example 2 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot-api
cd hummingbot-api
./setup.sh
```

Example 3 (unknown):
```unknown
make install
```

Example 4 (unknown):
```unknown
./run.sh --dev
```

---

## Post-Installation - Hummingbot

**URL:** https://hummingbot.org/installation/post-installation/

**Contents:**
- Post-Installation
- Folder structure¶
- Launching Hummingbot¶
  - Docker¶
  - Source¶
- Exiting Hummingbot¶
- Updating Hummingbot¶
  - Docker¶
  - Source¶
- Keeping bots running in background¶

Hummingbot is local client software that you run on your own machine, so you have full control over how it’s configured and where you save your files. No one else can access your data and secrets!

Your Hummingbot folder contains the following folders: hummingbot ┣ conf ┣ connectors ┣ strategies ┣ scripts ┣ logs ┣ data ┣ scripts ┣ hummingbot

Here is what each folder contains:

/conf: General folder for configuration files

/conf/connectors: Exchange API keys encrypted by your password

/conf/strategies: Strategy config files that you can create and import

/conf/scripts: Script config files that you can create --script-config

/logs: Log files generated by your scripts and strategies

/data: SQLite databases and CSV files for the trades executed by your scripts and strategies

/scripts: This folder contains the sample scripts, and you can add new scripts here to make them available to the start command

If you used Docker Compose to deploy Hummingbot, you can launch the network from the directory that contains the docker-compose.yml file with: docker compose up -d

Then, attach to it (typically, the container name is hummingbot): docker attach <container-name>

If you installed Hummingbot from source, make sure that the hummingbot conda environment has been activated before you run Hummingbot: conda activate hummingbot

If you have made any changes, make sure to re-compile the code with ./compile to ensure that any changes to Cython files are compiled before running Hummingbot: ./compile

Afterwards, from the root directory, run this command: ./start

Running the exit command cancels all outstanding orders and exit the Hummingbot interface. In case of errors, the command exit -f will force the application to close.

You can also press the keyboard shortcut CTRL + C twice to exit.

Once a month, we publish an official release of Hummingbot and Hummingbot Gateway, marked by code release on Github and DockerHub and the publication of the release notes.

Subscribe to the Hummingbot Newletter to get notified when a new release ships.

Users of the Docker version of Hummingbot can update their instances to the latest image, which is updated with each release (e.g. hummingbot/hummingbot:latest).

See Useful Docker Commands for how to manage your containers. For example, you can update the Compose project for the latest images:

For users who have installed from source, they can update their Hummingbot branches to master (with every release) or development branch (updated continually):

Press keys Ctrl + P then Ctrl + Q in sequence to detach from Docker, i.e., return to the command line. This exits out of Hummingbot without shutting down the container instance.

Use docker attach [container_name] to attach to an already-running bot in the background.

Use either tmux or screen to run multiple bots installed from source. Check out these external links how to use them.

When using screen to run an instance in the background, run either of the following commands: screen or screen -S $NAME, where $NAME is what you wish to call this background instance. Use the latter to be more explicit if you want to run multiple bots.

Navigate to the folder where your separate Hummingbot is installed, then start the bot like normal.

To exit the screen (detach), press Ctrl + A then Ctrl + D in sequence.

To list all running instances, use screen -ls.

Log back into the screen by using either screen or screen -r $NAME to open a specific instance.

Thank you to Discord user @matha for this question and @pfj for the solution!

**Examples:**

Example 1 (unknown):
```unknown
hummingbot
    ┣ conf
        ┣ connectors
        ┣ strategies
        ┣ scripts
    ┣ logs
    ┣ data
    ┣ scripts
    ┣ hummingbot
```

Example 2 (unknown):
```unknown
docker compose up -d
```

Example 3 (unknown):
```unknown
docker attach <container-name>
```

Example 4 (unknown):
```unknown
conda activate hummingbot
```

---

## Quickstart - Hummingbot

**URL:** https://hummingbot.org/hummingbot-api/quickstart

**Contents:**
- Quickstart
- Prerequisites¶
- Setup Python Client (Optional)¶
- List Available Exchanges¶
- Get Connector Configuration¶
- Add Exchange Credentials¶
- View Your Portfolio¶
- Get Trading Rules¶
- Place a Limit Order¶
- Complete Example¶

This guide demonstrates how to use Hummingbot API to add exchange credentials, view your portfolio, and place a market order.

If you want to use the Python client for the examples below:

Install the Hummingbot API Client: pip install hummingbot-api-client

Create a new Python file (e.g., hummingbot_api_demo.py): touch hummingbot_api_demo.py

Add the following code to initialize the client: import asyncio from hummingbot_api_client import HummingbotAPIClient # Create client instance client = HummingbotAPIClient( base_url="http://localhost:8000", username="admin", password="admin" )

To run any of the examples below, use: python hummingbot_api_demo.py

Get a list of all available exchange connectors. Note that spot and perpetual markets are separate connectors (e.g., hyperliquid for spot and hyperliquid_perpetual for perps).

Before adding credentials, check what configuration fields are required for your connector:

Add your exchange credentials to the API. By default, only the master_account is created. You can add multiple accounts with different names if needed.

Check your portfolio balances across all connected exchanges:

Before placing orders, fetch the trading rules for your intended trading pair to understand order size limits and price increments:

Execute a limit sell order for HYPE:

Geo-Restriction Error

If you receive an error like: { "detail": "Failed to place trade: No order book exists for 'HYPE-USDC'." } This may indicate you are geo-restricted from trading on the exchange. Check your API logs for more details: docker logs hummingbot-api

Here's a complete example that performs all three operations:

Save this code to hummingbot_api_demo.py:

Run the script: python hummingbot_api_demo.py

Now that you've completed the quickstart, explore more advanced features:

For the complete API reference, visit the API documentation when your API is running.

**Examples:**

Example 1 (unknown):
```unknown
pip install hummingbot-api-client
```

Example 2 (unknown):
```unknown
touch hummingbot_api_demo.py
```

Example 3 (python):
```python
import asyncio
from hummingbot_api_client import HummingbotAPIClient

# Create client instance
client = HummingbotAPIClient(
    base_url="http://localhost:8000",
    username="admin",
    password="admin"
)
```

Example 4 (unknown):
```unknown
python hummingbot_api_demo.py
```

---

## Installation Methods Comparison - Hummingbot

**URL:** https://hummingbot.org/installation/install-overview/

**Contents:**
- Installation Methods Comparison¶
- Core Options¶
- When to Choose Which?¶
- FAQ¶

Dashboard + Hummingbot Choose if:

Limitations: - Less low-level control - Requires more system resources

Docker Standalone Choose if:

Limitations: - Can't modify core code - Manual certificate management

Source Installation Choose if:

Limitations: - Complex setup - Dependency conflicts possible

Can I run multiple methods together? Yes - Dashboard can manage Docker instances while you run separate source installations.

Which is most resource-efficient? Docker standalone (no GUI overhead), followed by Source.

How to switch versions? - Dashboard: Automatic through UI - Docker: Edit image: tag - Source: git checkout tags

---

## 1.21.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/1.21.0/

**Contents:**
- Hummingbot v1.21.0 Release Notes¶
- Introduction¶
- How to Update¶
  - Docker¶
  - Source¶
- Monthly Community Call¶
- New Quickstart Guide: Intro to Dashboard¶
- New Dashboard Features¶
  - Authentication Module¶
  - V2 Strategy Framework Improvements¶

Released on October 30, 2023

We're thrilled to present Hummingbot version 1.21.0! This version introduces a new 9-step Intro to Dashboard quickstart guide, along with a new authentication module in Dashboard. It also features a smoother and faster startup process due to the refactored trading pair fetcher, along with a significant Dexalot connector fix!

Clone the latest hummingbot/deploy-examples repository and use the hummingbot-update.sh script under the /bash_scripts folder.

Alternatively, run the following command to pull the latest Docker image:

Update your Hummingbot branch to this release by running:

Join the Wednesday Nov 1st community call on Discord to learn about the new features in this release and other Hummingbot news. Here is the recording of the event:

For more community events, check out the Hummingbot Events Calendar.

We're thrilled to introduce a new Quickstart guide that shows users how to set up and use Dashboard. While it's still under active development, we expect Dashboard to become the main entry point for new Hummingbot users in the future.

See Quickstart - Intro to Dashboard or watch the first video below:

Under Active Development

Dashboard is slated for incorporation into official Hummingbot releases before end of this year, but it is still under active development and new features and improvements are being added continuously. We highly encourage user feedback at this stage; feel free to share your thoughts and suggestions on Discord or Github. If you're excited to explore its capabilities, check out the beta.

This release implemented authentication functionality within the Streamlit framework, which lets you require users to login to access any page in Dashboard, thereby enhancing security. This authentication can be enabled / disabled depending on user preference.

See Setting up Dashboard in the Intro to Dashboard guide.

In #6526, Hummingbot no longer fetches trading pairs from all connectors at startup. Instead, by default it will only fetch pairs from exchanges where the user has added API keys, as well as the Paper Trade exchanges, defined in conf_client.yml.

This should result in a faster startup process, plus fewer errors in the log from geo-restricted connectors.

There is a new configuration variable fetch_pairs_from_all_exchanges in conf_client.yml, which is set to False by default. If the variable is True, pairs are fetched from all exchange connectors, maintaining the previous behavior.

Thanks to isreallee82 for this contribution! 🙏

Per the Epoch 6 quarterly Poll results, not all connectors received enough community support to reach the 200,000 HBOT Connector Inclusion Threshold, and they will be removed during Q4 2023.

CEX Poll Results removed connectors:

DEX Poll Results removed connectors:

All connectors in the Chain Poll Results met the threshold.

**Examples:**

Example 1 (unknown):
```unknown
docker pull hummingbot/hummingbot:latest
```

Example 2 (unknown):
```unknown
git pull origin master
```

---

## 2.0.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/2.0.0/

**Contents:**
- Hummingbot v2.0.0 Release Notes¶
- Introduction¶
- How to Update¶
  - Docker¶
  - Source¶
- Hummingbot 2.0 Highlights¶
  - Deploy Repo¶
  - Dashboard¶
- New XRPL Connector (Python)¶
- New Balancer Connector¶

Released on July 3, 2024

Hummingbot 2.0 introduces a major update that revolutionizes the bot trading experience with the new Dashboard GUI. This upgrade transitions away from the traditional Hummingbot command-line interface (CLI), offering a more intuitive and visually appealing interface. Now, you can generate and backtest strategies before deploying them as Hummingbot instances, making Hummingbot 2.0 a powerful tool for both novice and experienced Hummingbot users.

Re-run the Deploy setup script: git clone https://github.com/hummingbot/deploy.git cd deploy bash setup.sh

For individual images, exit running containers, pull the latest images, and restart: docker compose down docker pull hummingbot/hummingbot:latest docker compose up -d

Update the branches of each repo to this release by running: git pull origin master

Hummingbot Deploy is a dedicated repo that allows users to quickly deploy Hummingbot using the Dashboard as the front end UI. The compose file spins up containers for the Dashboard, Backend-API as well as the Hummingbot Broker.

For more info check out the Hummingbot 2.0 Quickstart Guide. Some highlights:

This PR enhances the current XRPL API connector by transitioning it to a fully Python-based implementation, eliminating the need for the Hummingbot Gateway. Users can now utilize the XRPL connector similarly to a standard CEX connector by executing the connect XRPL command. This upgrade significantly boosts the connector's performance and enhances stability for user trading activities.

Thanks to mlguys for this contribution! 🙏

Pull Request: #280 - Added Balancer connector

Thanks to vic-en for this contribution! 🙏

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

## Linux - Hummingbot

**URL:** https://hummingbot.org/installation/linux/

**Contents:**
- Linux
- Prerequisites¶
  - Cloud server or local machine¶
  - Update Dependencies¶
  - Miniconda / Anaconda¶
- Install Hummingbot¶
- Launch Hummingbot¶
- Other Useful Commands¶
  - Update Hummingbot to latest master release¶
  - Update Hummingbot to development branch¶

The instructions below help you install a standalone Hummingbot instance from source on Linux-based machines.

On new Ubuntu instances, you may need to install the build-essentials package:

Hummingbot uses conda, an open source environment manager to manage dependencies for Python. You can install conda using either Miniconda or Anaconda.

Download the installer for your environment and run it:

Follow the prompts on the installer screens. If you are unsure about any setting, accept the defaults.

To make the changes take effect, close and then re-open your terminal window.

After you have installed the dependencies, run the following commands to install Hummingbot from source:

The conda activate hummingbot command should add a (hummingbot) label in front of your command line, which lets you know that you are inside the conda environment. If not, check if conda was installed correctly and reinstall if necessary.

From inside the conda environment, run the following command to launch Hummingbot:

You should see the Hummingbot welcome screen:

To get started with Hummingbot, check out the following docs:

If you need to run DEX bots, install Hummingbot Gateway.

**Examples:**

Example 1 (unknown):
```unknown
sudo apt update && sudo apt upgrade -y && sudo apt install -y gcc build-essential
```

Example 2 (unknown):
```unknown
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Example 3 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot.git
cd hummingbot
./install
conda activate hummingbot
./compile
```

Example 4 (unknown):
```unknown
git pull origin master
```

---

## 1.14.0 - Hummingbot

**URL:** https://hummingbot.org/release-notes/1.14.0/

**Contents:**
- Release Notes - Version 1.14.0¶
- New Quickstart Guide¶
- Revamped Installation Section¶
- New Doc Pages¶
- Orchestration Module: Phase 2¶
- New Perpetual CEX Connector: kucoin_perpetual¶
- New AMM DEX Connector and Chain: xsswap / xdc-chain¶
- New CLOB DEX Connector: dexalot¶
- PositionExecutor Improvements¶
- hedge Strategy updates¶

Released on March 30, 2023

We are very excited to ship the March 2023 release of Hummingbot (v1.14.0) today! This release focused on improving the docs by adding a new Quickstart guide, revamping the Installation section, and generally adding more video 📺 content to many pages!

In addition, this release added new kucoin_perpetual CEX connector, new DEX connectors for dexalot (CLOB DEX on Avalanche) and xsswap (AMM DEX on XDC Chain), and updates to the Orchestation Module, hedge strategy, and PositionExecutor components.

See below for what's new this month!

Hummingbot has evolved from a simple market making bot into a framework that lets users define custom strategies that automate order book data collection and order execution across multiple crypto exchanges.

To help users understand how to use Scripts to build custom strategies, the new Quickstart Guide teaches you how to build and customize a market making strategy over 5 exercises.

We have streamlined and simplified the Installation section, adding OS-specific guides and a new Docker page that explains how to deploy various Hummingbot configurations using Docker.

This release introduced the following new documentation pages and sections:

This PR implements the features of Phase 2 for HIP-Bot Orchestration.

It provides interfaces for subscribing to external topics and listening to messages through the EEventQueueFactory, EEventListenerFactory, ETopicQueueFactory, and ETopicListenerFactory classes. The specification defines a base URI format for consuming external events, and URI slashes are transformed to dots for multi-broker and multi-protocol support. Finally, this PR extends the global configuration and adds the mqtt_external_events parameter for globally enabling/disabling external events feature for bot instances.

See the Orchestration Module documentation for more information.

Thanks to klpanagi and TheHolyRoger for this contribution! 🙏

Since Kucoin is a Silver connector maintained by Hummingbot Foundation,the Foundation allocates HBOT tokens to fund a bounty for a community developer to add a perpetual connector.

Kucoin is a centralized cryptocurrency exchange platform that was launched in 2017 and is based in Seychelles. The platform operates its own native token, Kucoin Shares (KCS), which provides users with various benefits such as reduced trading fees and a share of the platform's revenue. Kucoin has gained popularity among cryptocurrency traders due to its competitive trading fees, diverse range of digital assets, and innovative features.

See the Kucoin Perpetual documentation for more information.

There may be some issues not yet identified outside our testing. If you run into a bug with the connector please report them on our Github page

Thanks to ethicrypt for this contribution! 🙏

Pull Requests: #6114, #0045

XDC is a public blockchain that aims to provide a fast and efficient infrastructure for decentralized applications and enterprise use cases. It is built on top of the Ethereum codebase and uses a proof-of-stake consensus algorithm to validate transactions and create new blocks.

See the XDC Chain and XSSwap documentation for more information.

Thanks to CoinAlpha for this contribution! 🙏

Pull Requests: #6153, #0065

Dexalot is a revolutionary decentralized exchange aiming at bringing the traditional centralized exchange look and feel, through a decentralized on-chain application. It is built on Avalanche, the fastest smart contracts platform in the blockchain industry.

See the Dexalot connector documentation for more information.

Thanks to CoinAlpha for this contribution! 🙏

We improved the PositionExecutor Smart Component introduced in the last release:

The first improvement is a minor change to the simple_directional_strategy_example script, which involves setting the bounds of the Relative Strength Index (RSI) as described in the strategy. This change improves the accuracy of the strategy by ensuring that the RSI is calculated within the specified bounds.

The second improvement is related to the reporting of the PositionExecutor. The update provides more detailed reporting by showing cumulative fees, profit and loss (PNL) in quote asset, and amount in both base and quote asset. This additional information provides users with a clear and concise view of their trading performance.

Overall, these improvements enhance the accuracy and transparency of the Simple directional strategy and provide more comprehensive reporting capabilities for the PositionExecutor, allowing users to make more informed trading decisions.

Disable Auto Set Position: In response to user feedback, we've added the ability to disable the auto set position feature on some exchanges, such as Bybit, that have experienced issues with this feature. You now have greater control over your position management.

Interval Logging: We've also added interval logging to help you keep track of your Hedge Strategy performance. This will allow you to review your trading activity at a glance and make informed decisions going forward.

Active Orders Management: To ensure that active orders are cancelled at the correct time, we've moved the check and cancel active orders function to the start of the tick. This improvement ensures that you're always trading with accurate information.

Timestamp Update: We've made an update to the way timestamps are handled to prevent network and exchange errors from skipping the current hedge cycle. The last timestamp is now updated only at the end of the cycle, ensuring that your trades are executed as intended.

Thanks to leastchaos for this contribution! 🙏

---

## Spot Connector Developer Checklist - Hummingbot

**URL:** https://hummingbot.org/developers/connectors/spot-connector-checklist/

**Contents:**
- Spot Connector v2.1¶
- Prerequisites¶
- API Checklist¶
- Directory Setup¶
  - Connector¶
  - Tests¶
- Build Process¶
  - CONSTANTS¶
  - Web Utils¶
  - Utils¶

Before proceeding with the setup of the Spot Connector, ensure that you have the Hummingbot source version installed on your system. Follow the detailed installation instructions provided at Hummingbot Installation Guide.

Create connector folder inside hummingbot/hummingbot/connector/exchange called connector_name.

connector_name = the name of the connector in lowercase and separated with underscores if applies.

Example without underscore: binance

Example with underscore: crypto_com

Create the following files inside of the connector folder:

Create test folder dwad inside hummingbot/test/hummingbot/exchange called connector_name.

Create the following files inside of the test folder:

Add to the constant files the following variables

connector_name_order_book.py

For now we will not implement any method, the only purpose of this step because we need to import this class in the connector_name_api_order_book_data_source.py and we don’t want to have errors.

connector_name_api_order_book_data_source.py

test_connector_name_api_order_book_data_source.py

Now we are going to start implementing the functionalities of the Order Book Data source but in a TDD way.

listen_for_subscriptions

listen_for_order_book_diffs

listen_for_order_book_snapshots

connector_name_auth.py

test_connector_name_auth.py

Replace binance for connector_name.

connector_name_api_user_stream_data_source.py

test_connector_name_api_user_stream_data_source.py

Now we are going to start implementing the functionalities of the User Stream Data source but in a TDD way.

If you need Listen Key:

listen_for_user_stream

connector_name_exchange.py

test_connector_name_exchange.py

Replace binance for connector_name.

A lot of tests are already in the Generic test class! But you have to implement some methods to let it work.

trade_event_for_full_fill_websocket_update

Methods to implement of ExchangePyBase

update_time_synchronizer

_user_stream_event_listener

Add connector_name_api_key and connector_name_api_secret to the conf_global_TEMPLATE.yml

---

## Installation - Hummingbot

**URL:** https://hummingbot.org/installation/

**Contents:**
- Hummingbot V2 + Dashboard¶
- System Requirements¶
  - Cloud server or local machine¶
  - Docker Compose¶
- Installation Steps¶
- Standalone Hummingbot¶

Hummingbot 2.0 now features a Dashboard GUI, replacing the traditional CLI for a more intuitive experience.

The recommended installation method, especially for new users, is Hummingbot + Dashboard, allowing you to easily create, backtest, and deploy strategies.

Other standalone installation options like Docker and Source are still available.

Hummingbot uses Docker Compose, a tool for defining and running multi-container Docker applications.

Install Docker Desktop from the official Docker website

Desktop Users: Install Docker Desktop from official site

Headless Servers (VPS like AWS EC2 or Digital Ocean): curl -fsSL https://get.docker.com -o get-docker.sh sh get-docker.sh

Always run commands in: Ubuntu Terminal (Start Menu → Ubuntu)

Hummingbot Deploy is a dedicated repo that allows users to quickly deploy Hummingbot using the Dashboard as the front end UI. The compose file spins up containers for the Dashboard, Backend-API as well as the Hummingbot Broker.

The setup script will pull the Docker images defined in repo's docker-compose.yml file and start them as new containers:

After all containers have started, access the Dashboard at http://localhost:8501 in your browser.

If you are using a cloud server or VPS, replace localhost with the IP of your server. You may need to edit the firewall rules to allow inbound connections to the necessary ports.

Install from Source →

See Installation Overview for comparison of different methods.

**Examples:**

Example 1 (unknown):
```unknown
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

Example 2 (unknown):
```unknown
git clone https://github.com/hummingbot/deploy.git
cd deploy
bash setup.sh
```

Example 3 (unknown):
```unknown
[+] Running 7/7
 ✔ Network deploy_emqx-bridge   Created
 ✔ Volume "deploy_emqx-data"    Created
 ✔ Volume "deploy_emqx-log"     Created
 ✔ Volume "deploy_emqx-etc"     Created
 ✔ Container dashboard          Started 
 ✔ Container backend-api        Started 
 ✔ Container hummingbot-broker  Started
```

---

## Installation & Setup - Hummingbot

**URL:** https://hummingbot.org/gateway/installation

**Contents:**
- Installation & Setup
- Install with Docker¶
- Install from Source¶
  - Install Prerequisites¶
  - Install and Setup Gateway¶
  - Run Setup Script¶
  - Optional: Generate Certificates¶
- Running Gateway¶
  - Development vs Production Modes¶
  - Development Mode (Default)¶

Hummingbot Gateway is an API/CLI client that exposes standardized REST endpoints to interact with blockchain networks and decentralized exchanges (DEXs). It provides a language-agnostic approach to interacting with these protocols through a unified interface.

There are two main ways to install Gateway:

This assumes that you want to use Gateway alongside Hummingbot to enable DEX trading. The Docker process enables seamless communication between the two services.

1 - Navigate to your Hummingbot directory

2 - Edit docker-compose.yml and uncomment the Gateway-related lines: gateway: restart: always container_name: gateway image: hummingbot/gateway:latest ports: - "15888:15888" volumes: - "./gateway-files/conf:/home/gateway/conf" - "./gateway-files/logs:/home/gateway/logs" - "./certs:/home/gateway/certs" environment: - GATEWAY_PASSPHRASE=admin - DEV=true

3 - Start both services docker compose up -d [+] Running 3/3 ✔ Network hummingbot_default Created 0.0s ✔ Container hummingbot Started 0.2s ✔ Container gateway Started

4 - Attach to Hummingbot docker attach hummingbot

After setting your password, you should see Gateway: 🟢 ONLINE in the upper right corner.

By default, Gateway runs in development mode (DEV=true) which uses HTTP for easier setup. For production environments requiring HTTPS, set DEV=false and ensure certificates are properly configured.

You can install Gateway on a standalone basis and then link it to Hummingbot manually. These instructions assume that you have already installed Hummingbot on the machine where you are installing Gateway, either from source or via Docker. See Installation for how to install Hummingbot.

Install the following dependencies:

The new version of Gateway uses pnpm instead of npm because it efficiently handles dependencies with a disk space-saving approach. Since Gateway imports multiple libraries with redundant dependencies, pnpm creates a single content-addressable storage for all packages, significantly reducing installation size and improving performance.

First, install NodeJS 20+ using the sudo administrator prefix: # For Ubuntu 20+ sudo apt update && sudo apt install -y curl curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - sudo apt install -y nodejs

Afterwards, install pnpm: sudo npm install -g pnpm

Clone the Gateway repo and navigate into the folder: # Clone repository git clone https://github.com/hummingbot/gateway.git cd gateway

Install and build Javascript dependencies defined in package.json: pnpm install pnpm build

The gateway-setup.sh script, located in the root Gateway directory, copies the default Gateway configuration files from /src/templates to /conf/ folder.

Run the script: pnpm run setup

The script will prompt you to select which configurations to update:

For a fresh installation, select all options. The script will preserve any existing wallet configurations and defaultWallet settings.

Certificate generation is optional. By default, Gateway runs in development mode (HTTP) which doesn't require certificates. You only need certificates if you want to run Gateway in production mode (HTTPS).

If you want to enable HTTPS mode for secure communication:

To connect Hummingbot to Gateway running in HTTPS mode, set gateway_use_ssl: true in Hummingbot's conf_client.yml.

Gateway can run in one of two modes:

Development Mode (HTTP) - Default

Production Mode (HTTPS) - Optional

HTTPS is no longer required to connect to Hummingbot. By default, both Gateway and Hummingbot are configured to use HTTP for easier setup. You can change the gateway_use_ssl setting in Hummingbot's conf_client.yml to switch between HTTP and HTTPS modes.

For development mode (HTTP), which is now the default and works with Hummingbot: pnpm start --passphrase=<PASSPHRASE> --dev

Or simply: pnpm start --passphrase=<PASSPHRASE>

The passphrase is required for endpoints that handle wallet operations.

If the server has started successfully, you should see: bigint: Failed to load bindings, pure JS will be used (try npm run rebuild?) ╔██████╗ █████╗ ████████╗███████╗██╗ ██╗ █████╗ ██╗ ██╗ ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝██║ ██║██╔══██╗╚██╗ ██╔╝ ██║ ███╗███████║ ██║ █████╗ ██║ █╗ ██║███████║ ╚████╔╝ ██║ ██║██╔══██║ ██║ ██╔══╝ ██║███╗██║██╔══██║ ╚██╔╝ ╚██████╔╝██║ ██║ ██║ ███████╗╚███╔███╔╝██║ ██║ ██║ ╚═════╝ ╚═╝ ╚═╝ ╚═╝ ╚══════╝ ╚══╝╚══╝ ╚═╝ ╚═╝ ╚═╝ 2025-04-04 10:09:59 | info | ⚡️ Gateway version 2.8.0 starting at http://localhost:15888 2025-04-04 10:09:59 | info | Checking for processes using port 15888... 2025-04-04 10:09:59 | info | No process found using port 15888 2025-04-04 10:09:59 | info | 🔴 Running in development mode with (unsafe!) HTTP endpoints 2025-04-04 10:09:59 | info | Read token file from conf/lists/solana.json, content length: 619791 2025-04-04 10:09:59 | info | Parsed token count: 3859 2025-04-04 10:09:59 | info | Loaded 3859 tokens for mainnet-beta 2025-04-04 10:09:59 | info | 📓 Documentation available at http://localhost:15888/docs

For production mode (HTTPS), which requires SSL certificates:

If the server has started successfully, you should see: bigint: Failed to load bindings, pure JS will be used (try npm run rebuild?) ╔██████╗ █████╗ ████████╗███████╗██╗ ██╗ █████╗ ██╗ ██╗ ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝██║ ██║██╔══██╗╚██╗ ██╔╝ ██║ ███╗███████║ ██║ █████╗ ██║ █╗ ██║███████║ ╚████╔╝ ██║ ██║██╔══██║ ██║ ██╔══╝ ██║███╗██║██╔══██║ ╚██╔╝ ╚██████╔╝██║ ██║ ██║ ███████╗╚███╔███╔╝██║ ██║ ██║ ╚═════╝ ╚═╝ ╚═╝ ╚═╝ ╚══════╝ ╚══╝╚══╝ ╚═╝ ╚═╝ ╚═╝ 2025-04-04 10:12:32 | info | ⚡️ Gateway version 2.8.0 starting at https://localhost:15888 2025-04-04 10:12:32 | info | Checking for processes using port 15888... 2025-04-04 10:12:32 | info | No process found using port 15888 2025-04-04 10:12:32 | info | 🟢 Running in secured mode with behind HTTPS endpoints 2025-04-04 10:12:33 | info | Read token file from conf/lists/solana.json, content length: 619791 2025-04-04 10:12:33 | info | Parsed token count: 3859 2025-04-04 10:12:33 | info | Loaded 3859 tokens for mainnet-beta 2025-04-04 10:12:33 | info | 📓 Documentation available at https://localhost:15888/docs

Once Gateway is running, go back to your Hummingbot client or restart it if you have exited. In the upper right corner, you should see GATEWAY: 🟢 ONLINE if your Hummingbot client is successfully connected to Gateway.

If you see GATEWAY: OFFLINE, check that:

Gateway provides interactive API documentation through Swagger UI when running in development mode. This interface allows you to:

To access the Swagger documentation:

Each endpoint in the documentation displays detailed information (method, path, description, parameters, request/response examples) and allows you to test API calls directly by filling in parameters and viewing the server's response.

The documentation is automatically generated from the Gateway route files, ensuring it's always up to date with the latest API changes.

**Examples:**

Example 1 (unknown):
```unknown
gateway:
   restart: always
   container_name: gateway
   image: hummingbot/gateway:latest
   ports:
     - "15888:15888"
   volumes:
     - "./gateway-files/conf:/home/gateway/conf"
     - "./gateway-files/logs:/home/gateway/logs"
     - "./certs:/home/gateway/certs"
   environment:
     - GATEWAY_PASSPHRASE=admin
     - DEV=true
```

Example 2 (unknown):
```unknown
docker compose up -d

[+] Running 3/3
 ✔ Network hummingbot_default  Created                                                                                                                                              0.0s 
 ✔ Container hummingbot        Started                                                                                                                                              0.2s 
 ✔ Container gateway           Started
```

Example 3 (unknown):
```unknown
docker attach hummingbot
```

Example 4 (unknown):
```unknown
# For Ubuntu 20+
sudo apt update && sudo apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## Install via Docker - Hummingbot

**URL:** https://hummingbot.org/installation/docker/

**Contents:**
- Install via Docker
- Install Docker Compose¶
- Installation (Client Only)¶
  - Clone Hummingbot Repo¶
  - Launch Hummingbot¶
  - Attach to Instance¶
- Dev Branch | Older Versions¶
  - Development Branch¶
  - Previous Versions¶
- Gateway: Required for DEX Trading¶

We recommend installing Hummingbot using Docker if you want the simplest, easiest installation method and don't need to modify the Hummingbot codebase.

Hummingbot uses Docker Compose, a tool for defining and running multi-container Docker applications.

Install Docker Desktop from the official Docker website

Desktop Users: Install Docker Desktop from official site

Headless Servers (VPS like AWS EC2 or Digital Ocean): curl -fsSL https://get.docker.com -o get-docker.sh sh get-docker.sh

Always run commands in: Ubuntu Terminal (Start Menu → Ubuntu)

These instructions help you launch the standalone Hummingbot client.

Open a terminal and run the following commands to clone the Hummingbot Github repo and enter the root folder:

This will start to download the latest Hummingbot image if it's not already on your system.

The -d flag runs Hummingbot in detached mode. Attach to it by running the command:

You should now see the Hummingbot welcome screen:

To get started with Hummingbot, check out the following pages and guides:

If you need to install the development branch or an older version of Hummingbot, follow these steps:

To use the latest development version, browse to the hummingbot folder and open the docker-compose.yml file using any text editor. Look for the image field, and replace latest with development.

To install a specific older version, replace the image field with the desired version. The version tags will follow this format: version-x.x.x For example, to install version 2.0.0, replace the image field with:

Essential for Decentralized Exchanges

Gateway must be installed separately to trade on these supported DEXs: - Uniswap (Ethereum) - PancakeSwap (BNB Chain) - Trader Joe (Avalanche) - dYdX (Starkware) - And 30+ others

Gateway acts as middleware that enables Hummingbot to interact with blockchain-based decentralized exchanges. To set up, follow the instructions in Gateway - Installation to generate certificates and connect Gateway to Hummingbot.

**Examples:**

Example 1 (unknown):
```unknown
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

Example 2 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot.git
  cd hummingbot
```

Example 3 (unknown):
```unknown
docker compose up -d
```

Example 4 (unknown):
```unknown
docker attach hummingbot
```

---

## Quickstart - Hummingbot

**URL:** https://hummingbot.org/hummingbot-api/quickstart/

**Contents:**
- Quickstart
- Prerequisites¶
- Setup Python Client (Optional)¶
- List Available Exchanges¶
- Get Connector Configuration¶
- Add Exchange Credentials¶
- View Your Portfolio¶
- Get Trading Rules¶
- Place a Limit Order¶
- Complete Example¶

This guide demonstrates how to use Hummingbot API to add exchange credentials, view your portfolio, and place a market order.

If you want to use the Python client for the examples below:

Install the Hummingbot API Client: pip install hummingbot-api-client

Create a new Python file (e.g., hummingbot_api_demo.py): touch hummingbot_api_demo.py

Add the following code to initialize the client: import asyncio from hummingbot_api_client import HummingbotAPIClient # Create client instance client = HummingbotAPIClient( base_url="http://localhost:8000", username="admin", password="admin" )

To run any of the examples below, use: python hummingbot_api_demo.py

Get a list of all available exchange connectors. Note that spot and perpetual markets are separate connectors (e.g., hyperliquid for spot and hyperliquid_perpetual for perps).

Before adding credentials, check what configuration fields are required for your connector:

Add your exchange credentials to the API. By default, only the master_account is created. You can add multiple accounts with different names if needed.

Check your portfolio balances across all connected exchanges:

Before placing orders, fetch the trading rules for your intended trading pair to understand order size limits and price increments:

Execute a limit sell order for HYPE:

Geo-Restriction Error

If you receive an error like: { "detail": "Failed to place trade: No order book exists for 'HYPE-USDC'." } This may indicate you are geo-restricted from trading on the exchange. Check your API logs for more details: docker logs hummingbot-api

Here's a complete example that performs all three operations:

Save this code to hummingbot_api_demo.py:

Run the script: python hummingbot_api_demo.py

Now that you've completed the quickstart, explore more advanced features:

For the complete API reference, visit the API documentation when your API is running.

**Examples:**

Example 1 (unknown):
```unknown
pip install hummingbot-api-client
```

Example 2 (unknown):
```unknown
touch hummingbot_api_demo.py
```

Example 3 (python):
```python
import asyncio
from hummingbot_api_client import HummingbotAPIClient

# Create client instance
client = HummingbotAPIClient(
    base_url="http://localhost:8000",
    username="admin",
    password="admin"
)
```

Example 4 (unknown):
```unknown
python hummingbot_api_demo.py
```

---

## Broker - Hummingbot

**URL:** https://hummingbot.org/installation/broker/

**Contents:**
- Broker
- Phase I¶
- Phase II¶
- Future phases¶

Hummingbot's brokers module allows for remote control and monitoring of multi-bot environments in a distributed context , so that bots can "live" on different machines and infrastructures (e.g. having a bot local and another bot on AWS).

To achieve this approach, there is an MQTT layer for bots to connect remotely to message brokers, as a single point of reference, using asynchronous bidirectional communication channels (push/pull). In this architecture, bots can be considered as clients to the overall environment. Bot scaling is seamless and does not require any further setup, anyone can connect any number of bots the a message broker (e.g. RabbitMQ, EMQX etc) without any other dependencies.

See the following repos for more information:

Watch the February 2023 community call that contains a demo of this feature:

Thanks to klpanagi and TheHolyRoger for your work! 🙏

In this Phase, an event and data layer will be integrated into the Hummingbot codebase to support receiving and handling remote events via the message broker (MQTT), such as the case of TradingView signals.

An MQTTEventListener will be developed and integrated into the hummingbot codebase, which will provide configuration for setting the URIs of the events to listen on. Upon receiving an event, a handling callback provided by the user/developer will be executed by the MQTTEventListener, so that users operate/develop their strategy based on the input event.

See this Notion doc for an overview of the project. This is an ongoing project funded by Proposal HIP-20.

---

## Installation & Setup - Hummingbot

**URL:** https://hummingbot.org/gateway/installation/

**Contents:**
- Installation & Setup
- Install with Docker¶
- Install from Source¶
  - Install Prerequisites¶
  - Install and Setup Gateway¶
  - Run Setup Script¶
  - Optional: Generate Certificates¶
- Running Gateway¶
  - Development vs Production Modes¶
  - Development Mode (Default)¶

Hummingbot Gateway is an API/CLI client that exposes standardized REST endpoints to interact with blockchain networks and decentralized exchanges (DEXs). It provides a language-agnostic approach to interacting with these protocols through a unified interface.

There are two main ways to install Gateway:

This assumes that you want to use Gateway alongside Hummingbot to enable DEX trading. The Docker process enables seamless communication between the two services.

1 - Navigate to your Hummingbot directory

2 - Edit docker-compose.yml and uncomment the Gateway-related lines: gateway: restart: always container_name: gateway image: hummingbot/gateway:latest ports: - "15888:15888" volumes: - "./gateway-files/conf:/home/gateway/conf" - "./gateway-files/logs:/home/gateway/logs" - "./certs:/home/gateway/certs" environment: - GATEWAY_PASSPHRASE=admin - DEV=true

3 - Start both services docker compose up -d [+] Running 3/3 ✔ Network hummingbot_default Created 0.0s ✔ Container hummingbot Started 0.2s ✔ Container gateway Started

4 - Attach to Hummingbot docker attach hummingbot

After setting your password, you should see Gateway: 🟢 ONLINE in the upper right corner.

By default, Gateway runs in development mode (DEV=true) which uses HTTP for easier setup. For production environments requiring HTTPS, set DEV=false and ensure certificates are properly configured.

You can install Gateway on a standalone basis and then link it to Hummingbot manually. These instructions assume that you have already installed Hummingbot on the machine where you are installing Gateway, either from source or via Docker. See Installation for how to install Hummingbot.

Install the following dependencies:

The new version of Gateway uses pnpm instead of npm because it efficiently handles dependencies with a disk space-saving approach. Since Gateway imports multiple libraries with redundant dependencies, pnpm creates a single content-addressable storage for all packages, significantly reducing installation size and improving performance.

First, install NodeJS 20+ using the sudo administrator prefix: # For Ubuntu 20+ sudo apt update && sudo apt install -y curl curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - sudo apt install -y nodejs

Afterwards, install pnpm: sudo npm install -g pnpm

Clone the Gateway repo and navigate into the folder: # Clone repository git clone https://github.com/hummingbot/gateway.git cd gateway

Install and build Javascript dependencies defined in package.json: pnpm install pnpm build

The gateway-setup.sh script, located in the root Gateway directory, copies the default Gateway configuration files from /src/templates to /conf/ folder.

Run the script: pnpm run setup

The script will prompt you to select which configurations to update:

For a fresh installation, select all options. The script will preserve any existing wallet configurations and defaultWallet settings.

Certificate generation is optional. By default, Gateway runs in development mode (HTTP) which doesn't require certificates. You only need certificates if you want to run Gateway in production mode (HTTPS).

If you want to enable HTTPS mode for secure communication:

To connect Hummingbot to Gateway running in HTTPS mode, set gateway_use_ssl: true in Hummingbot's conf_client.yml.

Gateway can run in one of two modes:

Development Mode (HTTP) - Default

Production Mode (HTTPS) - Optional

HTTPS is no longer required to connect to Hummingbot. By default, both Gateway and Hummingbot are configured to use HTTP for easier setup. You can change the gateway_use_ssl setting in Hummingbot's conf_client.yml to switch between HTTP and HTTPS modes.

For development mode (HTTP), which is now the default and works with Hummingbot: pnpm start --passphrase=<PASSPHRASE> --dev

Or simply: pnpm start --passphrase=<PASSPHRASE>

The passphrase is required for endpoints that handle wallet operations.

If the server has started successfully, you should see: bigint: Failed to load bindings, pure JS will be used (try npm run rebuild?) ╔██████╗ █████╗ ████████╗███████╗██╗ ██╗ █████╗ ██╗ ██╗ ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝██║ ██║██╔══██╗╚██╗ ██╔╝ ██║ ███╗███████║ ██║ █████╗ ██║ █╗ ██║███████║ ╚████╔╝ ██║ ██║██╔══██║ ██║ ██╔══╝ ██║███╗██║██╔══██║ ╚██╔╝ ╚██████╔╝██║ ██║ ██║ ███████╗╚███╔███╔╝██║ ██║ ██║ ╚═════╝ ╚═╝ ╚═╝ ╚═╝ ╚══════╝ ╚══╝╚══╝ ╚═╝ ╚═╝ ╚═╝ 2025-04-04 10:09:59 | info | ⚡️ Gateway version 2.8.0 starting at http://localhost:15888 2025-04-04 10:09:59 | info | Checking for processes using port 15888... 2025-04-04 10:09:59 | info | No process found using port 15888 2025-04-04 10:09:59 | info | 🔴 Running in development mode with (unsafe!) HTTP endpoints 2025-04-04 10:09:59 | info | Read token file from conf/lists/solana.json, content length: 619791 2025-04-04 10:09:59 | info | Parsed token count: 3859 2025-04-04 10:09:59 | info | Loaded 3859 tokens for mainnet-beta 2025-04-04 10:09:59 | info | 📓 Documentation available at http://localhost:15888/docs

For production mode (HTTPS), which requires SSL certificates:

If the server has started successfully, you should see: bigint: Failed to load bindings, pure JS will be used (try npm run rebuild?) ╔██████╗ █████╗ ████████╗███████╗██╗ ██╗ █████╗ ██╗ ██╗ ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝██║ ██║██╔══██╗╚██╗ ██╔╝ ██║ ███╗███████║ ██║ █████╗ ██║ █╗ ██║███████║ ╚████╔╝ ██║ ██║██╔══██║ ██║ ██╔══╝ ██║███╗██║██╔══██║ ╚██╔╝ ╚██████╔╝██║ ██║ ██║ ███████╗╚███╔███╔╝██║ ██║ ██║ ╚═════╝ ╚═╝ ╚═╝ ╚═╝ ╚══════╝ ╚══╝╚══╝ ╚═╝ ╚═╝ ╚═╝ 2025-04-04 10:12:32 | info | ⚡️ Gateway version 2.8.0 starting at https://localhost:15888 2025-04-04 10:12:32 | info | Checking for processes using port 15888... 2025-04-04 10:12:32 | info | No process found using port 15888 2025-04-04 10:12:32 | info | 🟢 Running in secured mode with behind HTTPS endpoints 2025-04-04 10:12:33 | info | Read token file from conf/lists/solana.json, content length: 619791 2025-04-04 10:12:33 | info | Parsed token count: 3859 2025-04-04 10:12:33 | info | Loaded 3859 tokens for mainnet-beta 2025-04-04 10:12:33 | info | 📓 Documentation available at https://localhost:15888/docs

Once Gateway is running, go back to your Hummingbot client or restart it if you have exited. In the upper right corner, you should see GATEWAY: 🟢 ONLINE if your Hummingbot client is successfully connected to Gateway.

If you see GATEWAY: OFFLINE, check that:

Gateway provides interactive API documentation through Swagger UI when running in development mode. This interface allows you to:

To access the Swagger documentation:

Each endpoint in the documentation displays detailed information (method, path, description, parameters, request/response examples) and allows you to test API calls directly by filling in parameters and viewing the server's response.

The documentation is automatically generated from the Gateway route files, ensuring it's always up to date with the latest API changes.

**Examples:**

Example 1 (unknown):
```unknown
gateway:
   restart: always
   container_name: gateway
   image: hummingbot/gateway:latest
   ports:
     - "15888:15888"
   volumes:
     - "./gateway-files/conf:/home/gateway/conf"
     - "./gateway-files/logs:/home/gateway/logs"
     - "./certs:/home/gateway/certs"
   environment:
     - GATEWAY_PASSPHRASE=admin
     - DEV=true
```

Example 2 (unknown):
```unknown
docker compose up -d

[+] Running 3/3
 ✔ Network hummingbot_default  Created                                                                                                                                              0.0s 
 ✔ Container hummingbot        Started                                                                                                                                              0.2s 
 ✔ Container gateway           Started
```

Example 3 (unknown):
```unknown
docker attach hummingbot
```

Example 4 (unknown):
```unknown
# For Ubuntu 20+
sudo apt update && sudo apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## Installation - Hummingbot

**URL:** https://hummingbot.org/mcp/installation/

**Contents:**
- Hummingbot MCP Server Installation Guide¶
- 📋 Prerequisites¶
- ⚙️ Installing via Docker MCP Catalog¶
- 🔗 Connecting an MCP Client¶
- 🛠️ JSON MCP Integration¶
  - Gemini CLI¶
    - Installation¶
    - Configuration¶
  - Codex CLI¶
    - Installation¶

This guide will walk you through installing and configuring the Hummingbot MCP Server, connecting it with AI assistants such as Claude CLI, Gemini CLI, or Codex CLI, and troubleshooting common issues.

Before starting, make sure you have:

💡 Tip: Ensure Docker Desktop has the MCP Toolkit feature enabled.

Open Docker Desktop → navigate to MCP Toolkit → Catalog. Search for the Hummingbot MCP Server and click ➕ Install.

Go to the Configuration tab for the installed server.

Set the following environment variables:

If your Hummingbot API is running locally, use: http://host.docker.internal:8000 instead of http://localhost:8000

After entering your values, click the checkbox on the right to save.

Once the server is configured, connect it with your MCP clients:

In Docker Desktop → MCP Toolkit → Clients Choose your AI client (e.g., Claude Desktop, Cursor, VS Code). Click Connect to establish a link.

For clients not listed, you can:

Run MCP Gateway manually: docker mcp gateway run

Or add the server manually in your client configuration:

Gemini CLI is Google’s open-source AI agent that integrates Gemini models into your terminal.

👉 Gemini CLI Installation Guide

Navigate to the config folder:

Edit the settings.json file

Add MCP server configuration:

Open Gemini and verify the connection by running:

✅ You should see hummingbot-mcp in the output.

Codex CLI is OpenAI’s local coding agent designed for developer workflows.

👉 Codex CLI Installation Guide

The MCP instructions below will also work with the IDE version of Codex for VSCode / Cursor etc. If you want Codex in your code editor see the - IDE installation guide

Navigate to the config folder:

Add the MCP server configuration:

Run Codex and and verify the connection by running:

✅ Codex should now detect and connect to the Hummingbot MCP server.

Once configured, try commands like:

"Show me my portfolio balances"

"List all active trading bots"

"Get the current BTC-USDT price on Binance"

📢 Need help? Join our Discord community or visit the GitHub repository for the latest updates.

**Examples:**

Example 1 (unknown):
```unknown
docker mcp gateway run
```

Example 2 (unknown):
```unknown
"mcp": {
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"],
      "type": "stdio"
    }
  }
}
```

Example 3 (unknown):
```unknown
cd ~/.gemini
```

Example 4 (unknown):
```unknown
nano settings.json
```

---

## Raspberry pi - Hummingbot

**URL:** https://hummingbot.org/installation/raspberry-pi/

**Contents:**
- Raspberry pi
- Prerequisites¶
  - Download 64-bit OS¶
  - Load the image file to your Raspberry Pi’s SD card¶
- Install from Source¶

Hummingbot doesn't require much power, so some users have run successfully run multiple instances on a single Raspberry Pi. The following steps are for the Raspberry Pi but it should also work with any other device that uses the same ARM architecture.

Running Hummingbot on a Raspberry Pi or similar device has the same main benefit of running it on a cloud server: having a dedicated machine for Hummingbot. Raspberry Pi’s are relatively low cost, easy to set up, and, of course, don’t have the monthly charges associated with a cloud provider.

To run Hummingbot on a Raspberry Pi, a 64-bit OS is required as it won't work with 32-bit. You can download the 64-bit OS from the Raspberry Pi website or from the Ubuntu website.

You can also choose between CLI (command line) and Desktop GUI versions but you'll get more performance with just using the CLI version.

The Raspberry Pi has an easy to follow guide with alternatives on how to load the SD card with a Raspberry Pi OS from different operating systems.

Once the OS is installed and booted then you can follow the steps below to install Hummingbot using either Docker or Source

Update the repository and install important dependencies: sudo apt update sudo apt upgrade -y sudo apt-get install build-essential libssl-dev libffi-dev gcc python3-dev -y

Install Miniforge: wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh sh Miniforge3-Linux-aarch64.sh

Restart the terminal: exec bash

Install conda-build: conda install conda-build

Clone the Hummingbot repository: git clone https://github.com/hummingbot/hummingbot.git

If you need to switch branches (ie. development branch) then after cloning the repository use the command git checkout [branch_name] to switch branches. For example, to switch to the development branch use git checkout development

Change directory into the Hummingbot folder: cd hummingbot

If you are using Ubuntu 22.04 you'll need to go into the ./setup folder first and edit the environment.yml file and change "cryptography==2.8" to "cryptography==3.1.1" before running the ./install command otherwise you'll get an error "could not build wheels for cryptography"

Run the install command: ./install

Activate the conda environment: conda activate hummingbot

Clean your Hummingbot directory and then compile:

Launch Hummingbot: ./start

**Examples:**

Example 1 (unknown):
```unknown
sudo apt update
sudo apt upgrade -y
sudo apt-get install build-essential libssl-dev libffi-dev gcc python3-dev -y
```

Example 2 (unknown):
```unknown
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh
sh Miniforge3-Linux-aarch64.sh
```

Example 3 (unknown):
```unknown
conda install conda-build
```

Example 4 (unknown):
```unknown
git clone https://github.com/hummingbot/hummingbot.git
```

---
