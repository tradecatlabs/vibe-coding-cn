---
name: hummingbot
description: "Hummingbot trading bot framework skill: connector setup, scripts, market making, arbitrage, Gateway DEX operations, headless quickstart, candles, market data provider, and troubleshooting for crypto trading bots."
---

# hummingbot Skill

Use this skill to operate, configure, or extend Hummingbot bots and Gateway connectors with explicit risk controls and version-aware references.

## When to Use This Skill

Trigger when any of these applies:
- Running Hummingbot strategies, scripts, or headless bot instances.
- Configuring CEX/DEX connectors, API keys, Gateway routes, or blockchain RPC providers.
- Building market-making, arbitrage, liquidity, or custom script strategies.
- Using candles, order book snapshots, mid-price, volume-for-price, or market data provider APIs.
- Debugging connector failures, Docker/runtime issues, Gateway command errors, or strategy config problems.

## Not For / Boundaries

- Not financial advice, profitability guarantees, or unattended live-trading approval.
- Never paste real exchange API keys, private keys, mnemonics, or wallet secrets into prompts, examples, logs, or commits.
- Use paper/sandbox/small-size validation before live capital; many connectors have exchange-specific limits and failure modes.
- Required inputs: Hummingbot version, install mode, connector, trading pair, strategy/script, config file, live/paper mode, and exact logs.
- Gateway and connector schemas evolve; verify against `references/` and the running version before production deployment.

## Quick Reference

### Common Patterns

**Run a headless quickstart**
```bash
bin/hummingbot_quickstart.py --headless -p PASSWORD -f CONFIG_FILE_NAME
```

**Run a script config**
```bash
bin/hummingbot_quickstart.py -p PASSWORD -f simple_pmm_example_config.py -c conf_simple_pmm_example_config_1.yml
```

**List Gateway connectors**
```text
gateway list
```

**Inspect Gateway swap syntax**
```text
gateway swap --help
```

**Get a mid price from the market data provider**
```python
price = self.market_data_provider.get_price_by_type(
    "binance",
    "BTC-USDT",
    PriceType.MidPrice,
)
```

**Get price by quote volume**
```python
price = self.market_data_provider.get_price_by_volume(
    "binance",
    "BTC-USDT",
    10000,
    True,
)
```

**Get an order book snapshot**
```python
snapshot = self.market_data_provider.get_order_book_snapshot("binance", "BTC-USDT")
```

**Create a candle feed**
```python
candles = CandlesFactory.get_candle(
    connector="kucoin",
    trading_pair="ETH-USDT",
    interval="1m",
    max_records=100,
)
```

**Update Docker deployment images**
```bash
docker compose down
docker pull hummingbot/hummingbot:latest
docker compose up -d
```

## Examples

### Example 1: Headless Bot Smoke Test

- Input: password, strategy config file, optional script config.
- Steps:
  1. Start with `bin/hummingbot_quickstart.py --headless`.
  2. Confirm logs show connector initialization and strategy start.
  3. Stop the bot and inspect final status before enabling live size.
- Expected output / acceptance: the bot starts from config without interactive prompts and exits cleanly.

### Example 2: Gateway Connector Triage

- Input: failing Gateway command and connector name.
- Steps:
  1. Run `gateway list` to verify connector availability.
  2. Run `gateway swap --help` or the specific command help.
  3. Compare arguments with the connector/network schema in `references/trading.md`.
- Expected output / acceptance: failure is classified as missing connector, bad args, RPC/network issue, or credential/config issue.

### Example 3: Strategy Market Data Hook

- Input: connector `binance`, pair `BTC-USDT`, needed price type.
- Steps:
  1. Use `market_data_provider` for mid price or volume-aware price.
  2. Keep API calls outside tight loops when cached data is sufficient.
  3. Log connector/pair/price source for later debugging.
- Expected output / acceptance: strategy reads a deterministic price source without blocking order logic.

## References

- `references/index.md`: navigation for local Hummingbot references.
- `references/getting_started.md`: install and first-run material.
- `references/configuration.md`: bot and connector configuration.
- `references/connectors.md`: exchange connector catalog and notes.
- `references/strategies.md`: strategy and script material.
- `references/trading.md`: Gateway and trading operations.
- `references/development.md`: development, headless, and release-related notes.
- `references/troubleshooting.md`: common failure modes.

## Maintenance

- Sources: local `references/` extracted from Hummingbot documentation.
- Last updated: 2026-04-28
- Known limits: connector support and Gateway schemas change frequently; validate against the installed Hummingbot version.
