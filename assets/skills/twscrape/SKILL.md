---
name: twscrape
description: "twscrape Twitter/X scraping skill: account pool setup, async search, user/tweet collection, CLI usage, proxy configuration, and rate-limit troubleshooting. Use when extracting public Twitter/X data with twscrape."
---

# twscrape Skill

Use this skill to build or debug `twscrape` workflows for public Twitter/X data extraction with account rotation, async collection, CLI commands, and proxy-aware operation.

## When to Use This Skill

Trigger when any of these applies:
- Scraping Twitter/X search results, profiles, followers, timelines, replies, retweeters, media, or trends with `twscrape`.
- Setting up account pools, cookies, login flows, email verification, or account rotation.
- Choosing between Python async API and the `twscrape` CLI.
- Diagnosing rate limits, empty results, login failures, proxy failures, or suspended accounts.
- Exporting normalized tweet/user data for monitoring, analytics, research, or archival pipelines.

## Not For / Boundaries

- Not for bypassing access controls, private content, paid-only data, or platform restrictions.
- Not for guaranteed high-volume scraping; account health, platform changes, and endpoint limits can invalidate assumptions.
- Do not place real Twitter/X passwords, cookies, email passwords, or proxy credentials in examples, commits, logs, or issue reports.
- Required inputs: target query/user/tweet/list, collection limit, output format, account source, proxy requirements, and compliance constraints.
- If behavior differs from these notes, verify against `references/` and the upstream repository before changing production collectors.

## Quick Reference

### Common Patterns

**Install the library**
```bash
pip install twscrape
```

**Create an API client and add a cookie-backed account**
```python
from twscrape import API

api = API("accounts.db")
await api.pool.add_account(
    "username",
    "password",
    "email@example.com",
    "email-password",
    cookies="ct0=...; auth_token=...",
)
```

**Login all configured accounts**
```python
await api.pool.login_all()
```

**Search recent tweets**
```python
from twscrape import gather

tweets = await gather(api.search("python lang:en", limit=50))
```

**Fetch a user then collect timeline data**
```python
user = await api.user_by_login("xdevelopers")
tweets = await gather(api.user_tweets(user.id, limit=100))
```

**Collect followers or following**
```python
followers = await gather(api.followers(user.id, limit=100))
following = await gather(api.following(user.id, limit=100))
```

**Inspect tweet details and replies**
```python
tweet = await api.tweet_details(1234567890)
replies = await gather(api.tweet_replies(tweet.id, limit=50))
```

**Use the CLI for a small search**
```bash
twscrape search "python lang:en" --limit=20
```

**Manage accounts from the CLI**
```bash
twscrape add_accounts accounts.txt username:password:email:email_password
twscrape login_accounts --manual
twscrape accounts
```

**Set a global proxy**
```bash
export TWS_PROXY=socks5://user:pass@127.0.0.1:1080
twscrape search "bitcoin" --limit=20
```

**Enable debug logging**
```python
from twscrape.logger import set_log_level

set_log_level("DEBUG")
```

## Examples

### Example 1: Search Export

- Input: query `python lang:en`, limit `50`, output JSON Lines.
- Steps:
  1. Confirm at least one healthy account with `twscrape accounts`.
  2. Use `await gather(api.search(query, limit=50))`.
  3. Serialize selected fields such as `id`, `date`, `user.username`, and `rawContent`.
- Expected output / acceptance: a JSONL file with up to 50 tweet records and no credentials in logs.

### Example 2: User Monitoring

- Input: username `xdevelopers`, timeline limit `100`.
- Steps:
  1. Resolve the account with `await api.user_by_login(username)`.
  2. Collect `api.user_tweets(user.id, limit=100)`.
  3. Store tweet IDs and timestamps so later runs can deduplicate.
- Expected output / acceptance: user metadata plus a deduplicated timeline batch.

### Example 3: Rate-Limit Triage

- Input: collector returns no data or waits indefinitely.
- Steps:
  1. Run `twscrape accounts` and identify locked, suspended, or rate-limited accounts.
  2. Enable debug logging and retry the smallest failing query.
  3. Add healthy accounts or wait for endpoint-specific reset before scaling up.
- Expected output / acceptance: the failing mode is classified as account health, query syntax, proxy/network, or platform limit.

## References

- `references/index.md`: navigation for the local twscrape reference set.
- `references/installation.md`: installation and dependency notes.
- `references/account_management.md`: account pool, login, and rotation behavior.
- `references/api_methods.md`: Python API method reference.
- `references/cli_usage.md`: command-line usage.
- `references/proxy_config.md`: proxy configuration and precedence.
- `references/examples.md`: longer code examples and extraction patterns.

## Maintenance

- Sources: local `references/` extracted from upstream twscrape material and the upstream repository noted there.
- Last updated: 2026-04-28
- Known limits: Twitter/X endpoints and account policies change without notice; validate live collectors against a small sample before large runs.
