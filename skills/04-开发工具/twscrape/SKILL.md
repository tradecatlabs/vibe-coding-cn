# twscrape

Python library for scraping Twitter/X data using GraphQL API with account rotation and session management.

## When to use this skill

Use this skill when:
- Working with Twitter/X data extraction and scraping
- Need to bypass Twitter API limitations with account rotation
- Building social media monitoring or analytics tools
- Extracting tweets, user profiles, followers, trends from Twitter/X
- Need async/parallel scraping operations for large-scale data collection
- Looking for alternatives to official Twitter API

## Quick Reference

### Installation

```bash
pip install twscrape
```

### Basic Setup

```python
import asyncio
from twscrape import API, gather

async def main():
    api = API()  # Uses accounts.db by default

    # Add accounts (with cookies - more stable)
    cookies = "abc=12; ct0=xyz"
    await api.pool.add_account("user1", "pass1", "email@example.com", "mail_pass", cookies=cookies)

    # Or add accounts (with login/password - less stable)
    await api.pool.add_account("user2", "pass2", "email2@example.com", "mail_pass2")
    await api.pool.login_all()

asyncio.run(main())
```

### Common Operations

```python
# Search tweets
await gather(api.search("elon musk", limit=20))

# Get user info
await api.user_by_login("xdevelopers")
user = await api.user_by_id(2244994945)

# Get user tweets
await gather(api.user_tweets(user_id, limit=20))
await gather(api.user_tweets_and_replies(user_id, limit=20))
await gather(api.user_media(user_id, limit=20))

# Get followers/following
await gather(api.followers(user_id, limit=20))
await gather(api.following(user_id, limit=20))

# Tweet operations
await api.tweet_details(tweet_id)
await gather(api.retweeters(tweet_id, limit=20))
await gather(api.tweet_replies(tweet_id, limit=20))

# Trends
await gather(api.trends("news"))
```

## Key Features

### 1. Multiple API Support
- **Search API**: Standard Twitter search functionality
- **GraphQL API**: Advanced queries and data extraction
- **Automatic switching**: Based on rate limits and availability

### 2. Async/Await Architecture
```python
# Parallel scraping
async for tweet in api.search("elon musk"):
    print(tweet.id, tweet.user.username, tweet.rawContent)
```

### 3. Account Management
- Add multiple accounts for rotation
- Automatic rate limit handling
- Session persistence across runs
- Email verification support (IMAP or manual)

### 4. Data Models
- SNScrape-compatible models
- Easy conversion to dict/JSON
- Raw API response access available

## Core API Methods

### Search Operations

#### `search(query, limit, kv={})`
Search tweets by query string.

**Parameters:**
- `query` (str): Search query (supports Twitter search syntax)
- `limit` (int): Maximum number of tweets to return
- `kv` (dict): Additional parameters (e.g., `{"product": "Top"}` for Top tweets)

**Returns:** AsyncIterator of Tweet objects

**Example:**
```python
# Latest tweets
async for tweet in api.search("elon musk", limit=20):
    print(tweet.rawContent)

# Top tweets
await gather(api.search("python", limit=20, kv={"product": "Top"}))
```

### User Operations

#### `user_by_login(username)`
Get user information by username.

**Example:**
```python
user = await api.user_by_login("xdevelopers")
print(user.id, user.displayname, user.followersCount)
```

#### `user_by_id(user_id)`
Get user information by user ID.

#### `followers(user_id, limit)`
Get user's followers.

#### `following(user_id, limit)`
Get users that the user follows.

#### `verified_followers(user_id, limit)`
Get only verified followers.

#### `subscriptions(user_id, limit)`
Get user's Twitter Blue subscriptions.

### Tweet Operations

#### `tweet_details(tweet_id)`
Get detailed information about a specific tweet.

#### `tweet_replies(tweet_id, limit)`
Get replies to a tweet.

#### `retweeters(tweet_id, limit)`
Get users who retweeted a specific tweet.

#### `user_tweets(user_id, limit)`
Get tweets from a user (excludes replies).

#### `user_tweets_and_replies(user_id, limit)`
Get tweets and replies from a user.

#### `user_media(user_id, limit)`
Get tweets with media from a user.

### Other Operations

#### `list_timeline(list_id)`
Get tweets from a Twitter list.

#### `trends(category)`
Get trending topics by category.

**Categories:** "news", "sport", "entertainment", etc.

## Account Management

### Adding Accounts

**With cookies (recommended):**
```python
cookies = "abc=12; ct0=xyz"  # String or JSON format
await api.pool.add_account("user", "pass", "email@example.com", "mail_pass", cookies=cookies)
```

**With credentials:**
```python
await api.pool.add_account("user", "pass", "email@example.com", "mail_pass")
await api.pool.login_all()
```

### CLI Account Management

```bash
# Add accounts from file
twscrape add_accounts accounts.txt username:password:email:email_password

# Login all accounts
twscrape login_accounts

# Manual email verification
twscrape login_accounts --manual

# List accounts and status
twscrape accounts

# Re-login specific accounts
twscrape relogin user1 user2

# Retry failed logins
twscrape relogin_failed
```

## Proxy Configuration

### Per-Account Proxy
```python
proxy = "http://login:pass@example.com:8080"
await api.pool.add_account("user", "pass", "email@example.com", "mail_pass", proxy=proxy)
```

### Global Proxy
```python
api = API(proxy="http://login:pass@example.com:8080")
```

### Environment Variable
```bash
export TWS_PROXY=socks5://user:pass@127.0.0.1:1080
twscrape search "elon musk"
```

### Dynamic Proxy Changes
```python
api.proxy = "socks5://user:pass@127.0.0.1:1080"
doc = await api.user_by_login("elonmusk")
api.proxy = None  # Disable proxy
```

**Priority:** `api.proxy` > `TWS_PROXY` env var > account-specific proxy

## CLI Usage

### Search Operations
```bash
twscrape search "QUERY" --limit=20
twscrape search "elon musk lang:es" --limit=20 > data.txt
twscrape search "python" --limit=20 --raw  # Raw API responses
```

### User Operations
```bash
twscrape user_by_login USERNAME
twscrape user_by_id USER_ID
twscrape followers USER_ID --limit=20
twscrape following USER_ID --limit=20
twscrape verified_followers USER_ID --limit=20
twscrape user_tweets USER_ID --limit=20
```

### Tweet Operations
```bash
twscrape tweet_details TWEET_ID
twscrape tweet_replies TWEET_ID --limit=20
twscrape retweeters TWEET_ID --limit=20
```

### Trends
```bash
twscrape trends sport
twscrape trends news
```

### Custom Database
```bash
twscrape --db custom-accounts.db <command>
```

## Advanced Usage

### Raw API Responses
```python
async for response in api.search_raw("elon musk"):
    print(response.status_code, response.json())
```

### Stopping Iteration
```python
from contextlib import aclosing

async with aclosing(api.search("elon musk")) as gen:
    async for tweet in gen:
        if tweet.id < 200:
            break
```

### Convert Models to Dict/JSON
```python
user = await api.user_by_id(user_id)
user_dict = user.dict()
user_json = user.json()
```

### Enable Debug Logging
```python
from twscrape.logger import set_log_level
set_log_level("DEBUG")
```

## Environment Variables

- **`TWS_PROXY`**: Global proxy for all accounts
  Example: `socks5://user:pass@127.0.0.1:1080`

- **`TWS_WAIT_EMAIL_CODE`**: Timeout for email verification (default: 30 seconds)

- **`TWS_RAISE_WHEN_NO_ACCOUNT`**: Raise exception when no accounts available instead of waiting
  Values: `false`, `0`, `true`, `1` (default: `false`)

## Rate Limits & Limitations

### Rate Limits
- Rate limits reset **every 15 minutes** per endpoint
- Each account has **separate limits** for different operations
- Accounts automatically rotate when limits are reached

### Tweet Limits
- `user_tweets` and `user_tweets_and_replies` return approximately **3,200 tweets maximum** per user
- This is a Twitter/X platform limitation

### Account Status
- Rate limits vary based on:
  - Account age
  - Account verification status
  - Account activity history

### Handling Rate Limits
The library automatically:
- Switches to next available account
- Waits for rate limit reset if all accounts exhausted
- Tracks rate limit status per endpoint

## Common Patterns

### Large-Scale Data Collection
```python
async def collect_user_data(username):
    user = await api.user_by_login(username)

    # Collect tweets
    tweets = await gather(api.user_tweets(user.id, limit=100))

    # Collect followers
    followers = await gather(api.followers(user.id, limit=100))

    # Collect following
    following = await gather(api.following(user.id, limit=100))

    return {
        'user': user,
        'tweets': tweets,
        'followers': followers,
        'following': following
    }
```

### Search with Filters
```python
# Language filter
await gather(api.search("python lang:en", limit=20))

# Date filter
await gather(api.search("AI since:2024-01-01", limit=20))

# From specific user
await gather(api.search("from:elonmusk", limit=20))

# With media
await gather(api.search("cats filter:media", limit=20))
```

### Batch Processing
```python
async def process_users(usernames):
    tasks = []
    for username in usernames:
        task = api.user_by_login(username)
        tasks.append(task)

    users = await asyncio.gather(*tasks)
    return users
```

## Troubleshooting

### Login Issues
- **Use cookies instead of credentials** for more stable authentication
- Enable **manual email verification** with `--manual` flag
- Check **email password** is correct for IMAP access

### Rate Limit Problems
- **Add more accounts** for better rotation
- **Increase wait time** between requests
- **Monitor account status** with `twscrape accounts`

### No Data Returned
- **Check account status** - they may be suspended or rate limited
- **Verify query syntax** - use Twitter search syntax
- **Try different accounts** - some may have better access

### Connection Issues
- **Configure proxy** if behind firewall
- **Check network connectivity**
- **Verify Twitter/X is accessible** from your location

## Resources

- **GitHub Repository**: https://github.com/vladkens/twscrape
- **Installation**: `pip install twscrape`
- **Development Version**: `pip install git+https://github.com/vladkens/twscrape.git`

## References

For detailed API documentation and examples, see the reference files in the `references/` directory:

- `references/installation.md` - Installation and setup
- `references/api_methods.md` - Complete API method reference
- `references/account_management.md` - Account configuration and management
- `references/cli_usage.md` - Command-line interface guide
- `references/proxy_config.md` - Proxy configuration options
- `references/examples.md` - Code examples and patterns

---

**Repository**: https://github.com/vladkens/twscrape
**Stars**: 1998+
**Language**: Python
**License**: MIT
