# Feature Specification: Multi-Account Twitter Bot Support

**Feature Branch**: `feat/#1/core-functionalities`  
**Created**: 2026-01-11  
**Status**: Draft  
**Input**: User description: "As I have mentioned in @.specify\memory\constitution.md , I am building a telegram bot pretty much same as https://github.com/EleftheriaBatsou/cosineai-x-telegram-notifier/tree/main , the only major feature of mine is that I want it to support more than one x/twitter accounts. Be advised, I already open issue at https://github.com/g405h3n/telegram-bot-for-twitter/issues/1 . I just noticed that this project, as an enhanced version, should retrieve x/twitter posts of multiple accounts' posts more easily -- Make a x/twitter list of multiple x/twitter accounts, and I could use https://docs.x.com/x-api/lists/get-list-posts API to retrieve x/twitter posts easily. I think this is the major difference of my project and that 'cosineai-x-telegram-notifier' project."

## Clarifications

### Session 2026-01-11
- Q: How should the code from the referenced GitHub repository be borrowed? → A: Copy the relevant code files into this project
- Q: How should the persistent state for each account be stored? → A: Single JSON file with all accounts, similar to the original repo's last_seen.json
- Q: What is the polling interval for checking new tweets? → A: Scheduled daily at 6:00 AM Asia/Shanghai via GitHub Actions workflow

### Session 2026-01-11 (Update)
- Major enhancement: Use Twitter list API (get-list-posts) to retrieve posts from multiple accounts by maintaining a Twitter list containing all monitored accounts, simplifying API calls and improving efficiency.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configure Multiple Twitter Accounts (Priority: P1)

As a user, I want to configure multiple Twitter/X accounts to monitor so that I can receive notifications from several accounts in my Telegram bot.

**Why this priority**: This is the core feature that differentiates from the original single-account bot, enabling multi-account monitoring from inception.

**Independent Test**: Can be fully tested by configuring one additional account beyond the original and verifying it is monitored independently, delivering value of expanded monitoring without breaking single-account functionality.

**Acceptance Scenarios**:

1. **Given** a configuration file with multiple account usernames, **When** the bot initializes, **Then** it validates all configured accounts and prepares state for each.
2. **Given** a valid configuration with two accounts, **When** the bot runs, **Then** it checks for new tweets from both accounts simultaneously.
3. **Given** an invalid account in the configuration, **When** the bot runs, **Then** it logs an error for that account but continues monitoring valid accounts.

---

### User Story 2 - Receive Notifications for New Tweets (Priority: P1)

As a user, I want to receive Telegram notifications only for new original tweets from each monitored account so that I stay updated on fresh content without noise from replies or retweets.

**Why this priority**: Notification purity is essential for user experience, ensuring users get relevant updates.

**Independent Test**: Can be fully tested by monitoring one account and verifying notifications are sent only for original tweets, delivering clean notification value.

**Acceptance Scenarios**:

1. **Given** a monitored account posts a new original tweet, **When** the bot checks, **Then** it sends a Telegram message with the tweet details.
2. **Given** a monitored account replies to another tweet, **When** the bot checks, **Then** no notification is sent.
3. **Given** the bot runs for the first time on an account, **When** it initializes state, **Then** no notifications are sent for existing historical tweets.

---

### User Story 3 - Graceful Error Handling for Multiple Accounts (Priority: P2)

As a user, I want the bot to continue monitoring other accounts even if one account fails so that a single issue doesn't break the entire monitoring system.

**Why this priority**: API resilience ensures reliability in a multi-account setup where external API failures are common.

**Independent Test**: Can be fully tested by simulating a failure on one account (e.g., invalid token) and verifying other accounts continue to be monitored, delivering fault-tolerant value.

**Acceptance Scenarios**:

1. **Given** one account's API token is invalid, **When** the bot checks all accounts, **Then** it logs the error for that account and continues checking other accounts.
2. **Given** the Twitter API is temporarily down, **When** the bot checks, **Then** it retries with exponential backoff and logs the attempt.
3. **Given** an account reaches rate limits, **When** the bot checks, **Then** it waits appropriately and logs the rate limit event.

---

### Edge Cases

- What happens when a Twitter account is suspended or deleted? The bot should log the issue and skip that account without affecting others.
- How does the system handle accounts with no new tweets for extended periods? State remains persistent and no unnecessary notifications are sent.
- What if the Telegram bot token is invalid? The system should validate tokens at startup and fail gracefully with clear error messages.
- How does the bot behave if the configuration file is corrupted or missing accounts? It should validate configuration at startup and provide feedback.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support configuration of multiple Twitter/X account usernames.
- **FR-002**: System MUST maintain persistent state recording the last seen tweet ID from the list to avoid duplicates.
- **FR-003**: System MUST send Telegram notifications ONLY for new original tweets, filtering out replies, retweets, and quotes.
- **FR-004**: System MUST include robust error handling with retry logic and exponential backoff for all API calls.
- **FR-005**: System MUST degrade gracefully if one account fails, continuing to monitor other accounts.
- **FR-006**: System MUST log all monitoring activities with timestamps, account identifiers, and outcome details.
- **FR-007**: System MUST validate that required secrets are present before attempting API calls.
- **FR-008**: On first run for any account, the system MUST initialize state WITHOUT sending messages for historical posts.

### Key Entities *(include if feature involves data)*

- **Twitter List**: Represents a curated list on Twitter containing multiple accounts to monitor; managed by the system.
- **Twitter Account**: Represents a monitored account included in the list with username.
- **Telegram Notification**: Represents a message sent to the configured chat with tweet details from accounts in the list.

## Implementation Approach

- Code borrowing: Copy relevant files from https://github.com/EleftheriaBatsou/cosineai-x-telegram-notifier/tree/main into this project and adapt for multi-account support.
- API strategy: Use Twitter list API (get-list-posts) by creating and managing a Twitter list containing all monitored accounts, allowing efficient retrieval of posts from multiple accounts in a single API call.
- Persistent state: Stored in a single JSON file for all accounts, mirroring the original repository's last_seen.json approach.
- Scheduling: Bot runs daily at 6:00 AM Asia/Shanghai timezone via GitHub Actions workflow to stay within free Twitter API plan.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can configure multiple Twitter accounts (list size managed by user to balance efficiency and pagination) and receive daily notifications at 6:00 AM Asia/Shanghai for new tweets posted since the last run.
- **SC-002**: System continues monitoring 90% of accounts even when 10% experience API failures.
- **SC-003**: No duplicate notifications sent for the same tweet across multiple runs.
- **SC-004**: All monitoring activities are logged with clear distinction between normal operation and errors.
