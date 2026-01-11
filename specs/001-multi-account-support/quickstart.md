# Quickstart: Multi-Account Twitter Bot

## Prerequisites
- Python 3.10+
- GitHub repository with Actions enabled

## Setup Steps
1. Copy adapted `monitor.py` to your repo.
2. Add `requirements.txt`: `requests>=2.31.0,<3`
3. Create GitHub Secrets:
   - TWITTER_BEARER_TOKEN (for reading)
   - TELEGRAM_BOT_TOKEN
    - TWITTER_USERNAMES: Comma-delimited usernames, e.g., "user1,user2"
   - TWITTER_LIST_ID: The ID of the Twitter list containing the accounts
4. Add `.github/workflows/monitor.yml` for daily runs at 6:00 AM Asia/Shanghai.
5. Run manually to validate accounts and save list configuration.

