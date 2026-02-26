# twscrape Examples

## Basic Search Example

```python
import asyncio
from twscrape import API, gather

async def main():
    api = API()

    # Search for tweets
    tweets = await gather(api.search("elon musk", limit=20))

    for tweet in tweets:
        print(f"{tweet.user.username}: {tweet.rawContent}")

asyncio.run(main())
```

## User Profile Analysis

```python
async def analyze_user(username):
    api = API()

    # Get user info
    user = await api.user_by_login(username)
    print(f"User: {user.displayname}")
    print(f"Followers: {user.followersCount}")
    print(f"Following: {user.followingCount}")

    # Get recent tweets
    tweets = await gather(api.user_tweets(user.id, limit=50))
    print(f"Recent tweets: {len(tweets)}")

    return user, tweets
```

## Follower Network Collection

```python
async def collect_network(user_id):
    api = API()

    # Collect followers
    followers = await gather(api.followers(user_id, limit=100))
    print(f"Collected {len(followers)} followers")

    # Collect following
    following = await gather(api.following(user_id, limit=100))
    print(f"Collected {len(following)} following")

    return followers, following
```

## Advanced Search with Filters

```python
async def advanced_search():
    api = API()

    # Search with language filter
    en_tweets = await gather(api.search("python lang:en", limit=20))

    # Search with date filter
    recent_tweets = await gather(api.search("AI since:2024-01-01", limit=20))

    # Search from specific user
    user_tweets = await gather(api.search("from:elonmusk", limit=20))

    # Search with media
    media_tweets = await gather(api.search("cats filter:media", limit=20))

    return en_tweets, recent_tweets, user_tweets, media_tweets
```

## Tweet Thread Analysis

```python
async def analyze_thread(tweet_id):
    api = API()

    # Get tweet details
    tweet = await api.tweet_details(tweet_id)
    print(f"Tweet: {tweet.rawContent}")

    # Get replies
    replies = await gather(api.tweet_replies(tweet_id, limit=100))
    print(f"Replies: {len(replies)}")

    # Get retweeters
    retweeters = await gather(api.retweeters(tweet_id, limit=100))
    print(f"Retweeters: {len(retweeters)}")

    return tweet, replies, retweeters
```

## Batch User Processing

```python
async def process_multiple_users(usernames):
    api = API()
    results = []

    tasks = []
    for username in usernames:
        task = api.user_by_login(username)
        tasks.append(task)

    users = await asyncio.gather(*tasks)

    for user in users:
        if user:
            print(f"Processed: {user.displayname}")
            results.append(user)

    return results

# Usage
usernames = ["elonmusk", "xdevelopers", "github"]
users = await process_multiple_users(usernames)
```

## Real-time Monitoring

```python
async def monitor_keywords(keywords, limit=100):
    api = API()

    for keyword in keywords:
        print(f"\\nMonitoring: {keyword}")

        async for tweet in api.search(keyword, limit=limit):
            print(f"[{tweet.date}] @{tweet.user.username}: {tweet.rawContent[:100]}")

            # Process tweet
            if tweet.likeCount > 1000:
                print(f"  -> Popular tweet! {tweet.likeCount} likes")

# Usage
await monitor_keywords(["python", "javascript", "ai"], limit=50)
```

## Data Export to JSON

```python
import json

async def export_user_data(username, output_file):
    api = API()

    user = await api.user_by_login(username)
    tweets = await gather(api.user_tweets(user.id, limit=100))

    data = {
        'user': user.dict(),
        'tweets': [tweet.dict() for tweet in tweets]
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Exported to {output_file}")

# Usage
await export_user_data("elonmusk", "elon_data.json")
```

## Trends Analysis

```python
async def analyze_trends():
    api = API()

    # Get different trend categories
    news_trends = await gather(api.trends("news"))
    sport_trends = await gather(api.trends("sport"))

    print("News Trends:")
    for trend in news_trends[:10]:
        print(f"  - {trend}")

    print("\\nSport Trends:")
    for trend in sport_trends[:10]:
        print(f"  - {trend}")

    return news_trends, sport_trends
```

## Using Context Manager for Early Termination

```python
from contextlib import aclosing

async def find_specific_tweet(query, target_id):
    api = API()

    async with aclosing(api.search(query)) as gen:
        async for tweet in gen:
            if tweet.id == target_id:
                print(f"Found target tweet: {tweet.rawContent}")
                return tweet

            if tweet.id < target_id:
                print("Target not found in results")
                break

    return None
```

## Account Setup Example

```python
async def setup_accounts():
    api = API()

    # Add accounts with cookies (more stable)
    cookies = "abc=12; ct0=xyz"
    await api.pool.add_account(
        "user1",
        "password1",
        "user1@example.com",
        "mail_password1",
        cookies=cookies
    )

    # Add account with credentials
    await api.pool.add_account(
        "user2",
        "password2",
        "user2@example.com",
        "mail_password2"
    )

    # Login all accounts
    await api.pool.login_all()

    print("Accounts setup complete")
```

## Proxy Configuration Example

```python
async def use_proxy():
    # Global proxy
    proxy = "http://user:pass@proxy.example.com:8080"
    api = API(proxy=proxy)

    # Make requests through proxy
    user = await api.user_by_login("elonmusk")
    print(f"User: {user.displayname}")

    # Change proxy dynamically
    api.proxy = "socks5://user:pass@127.0.0.1:1080"
    tweets = await gather(api.search("python", limit=10))

    # Disable proxy
    api.proxy = None
    more_tweets = await gather(api.search("javascript", limit=10))
```

## Error Handling

```python
async def safe_user_lookup(username):
    api = API()

    try:
        user = await api.user_by_login(username)
        return user
    except Exception as e:
        print(f"Error fetching user {username}: {e}")
        return None

async def bulk_lookup_with_errors(usernames):
    results = []
    for username in usernames:
        user = await safe_user_lookup(username)
        if user:
            results.append(user)

    return results
```

## Complete Workflow Example

```python
import asyncio
import json
from twscrape import API, gather
from twscrape.logger import set_log_level

async def complete_workflow():
    # Setup
    api = API("my_data.db")
    set_log_level("INFO")

    # Add accounts
    await api.pool.add_account(
        "user1", "pass1", "email1@example.com", "mail_pass1",
        cookies="cookie_string_here"
    )

    # Search and analyze
    query = "python programming"
    tweets = await gather(api.search(query, limit=100))

    # Extract user data
    users = {}
    for tweet in tweets:
        if tweet.user.username not in users:
            users[tweet.user.username] = {
                'user': tweet.user.dict(),
                'tweets': []
            }
        users[tweet.user.username]['tweets'].append(tweet.dict())

    # Export results
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    print(f"Processed {len(tweets)} tweets from {len(users)} users")

if __name__ == "__main__":
    asyncio.run(complete_workflow())
```
