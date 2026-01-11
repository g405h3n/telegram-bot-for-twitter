# Data Model: Multi-Account Twitter Bot Support

## Entities

### Twitter List
- **id**: String (unique ID of the managed Twitter list)
- **name**: String (name of the list, e.g., "Monitored Accounts")
- **member_accounts**: List of strings (usernames of accounts in the list)

**Relationships**: Created and managed by the system; contains all monitored accounts for efficient API calls.

### Twitter Account
- **username**: String (unique identifier for the account to monitor)
- **user_id**: String (Twitter user ID for API calls)

**Relationships**: Added to the Twitter list. Validation: Username must be valid Twitter handle.

### Telegram Notification
- **tweet_text**: String (content of the tweet)
- **tweet_url**: String (link to the tweet on X/Twitter)
- **account_username**: String (username of the account that posted the tweet)

**Relationships**: Sent per new tweet from accounts in the list. No persistent storage; generated on-demand.

### Tweet (Transient)
- **id**: String (unique tweet ID)
- **text**: String (tweet content)
- **created_at**: String (ISO timestamp)
- **referenced_tweets**: List of dicts (e.g., [{"type": "quoted", "id": "..."}])
- **author_id**: String (ID of the account that posted the tweet)

**Relationships**: Fetched from Twitter list API; filtered for originals only. Used to update state and generate notifications.

## State Management
- Persistent state: Single JSON file `state/last_seen.json` with structure `{"list_id": "last_tweet_id"}`
- Configuration: Loaded from GitHub secrets (TWITTER_LIST_ID, TWITTER_USERNAMES) at runtime.
- Atomic updates: Overwrite files on changes.
- Initialization: On first run, set last tweet ID without notifications.