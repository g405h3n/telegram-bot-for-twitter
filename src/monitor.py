import json
import logging
import os
import pathlib
import sys
from typing import Dict, List, Optional, cast

import requests

TWITTER_API_BASE = "https://api.twitter.com/2"
STATE_DIR = pathlib.Path("state")
STATE_FILE = STATE_DIR / "last_seen.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def _env(name: str, default: Optional[str] = None, required: bool = True) -> str:
    val = os.getenv(name, default)
    if required and not val:
        logging.error(f"Missing required environment variable: {name}")
        sys.exit(1)
    return cast(str, val)


def get_user_id(username: str, bearer: str) -> Optional[str]:
    url = f"{TWITTER_API_BASE}/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer}"}
    params = {"user.fields": "id"}
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    if resp.status_code != 200:
        logging.error(f"Error fetching user id for {username}: {resp.status_code} {resp.text}")
        return None
    data = resp.json()
    return data["data"]["id"]


def validate_usernames(usernames: List[str], bearer: str) -> List[str]:
    valid = []
    for username in usernames:
        user_id = get_user_id(username, bearer)
        if user_id:
            valid.append(username)
            logging.info(f"Validated account: {username}")
        else:
            logging.error(f"Invalid or inaccessible account: {username}")
    return valid


def fetch_original_tweets(user_id: str, bearer: str, since_id: Optional[str]) -> List[Dict]:
    url = f"{TWITTER_API_BASE}/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {bearer}"}
    params = {
        "max_results": 20,
        "exclude": "replies,retweets",
        "tweet.fields": "created_at,referenced_tweets",
    }
    if since_id:
        params["since_id"] = since_id

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code != 200:
        print(f"Error fetching tweets: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)
    payload = resp.json()
    tweets = payload.get("data", [])

    # Exclude quotes: if referenced_tweets contains a 'quoted' type, skip
    originals: List[Dict] = []
    for t in tweets:
        ref = t.get("referenced_tweets", [])
        if any(r.get("type") == "quoted" for r in ref):
            continue
        originals.append(t)

    # Sort oldest -> newest for sending in order
    originals.sort(key=lambda x: x["id"])
    return originals


def load_state() -> Dict[str, str]:
    if not STATE_FILE.exists():
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state: Dict[str, str]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)


def send_telegram_message(bot_token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, json=payload, timeout=20)
    if resp.status_code != 200:
        print(f"Telegram send error: {resp.status_code} {resp.text}", file=sys.stderr)


def main() -> None:
    #
    # Validate and load GitHub secrets.
    twitter_bearer_token = _env("TWITTER_BEARER_TOKEN")
    twitter_usernames = [u.strip() for u in _env("TWITTER_USERNAMES").split(",") if u.strip()]
    twitter_list_id = _env("TWITTER_LIST_ID")
    telegram_bot_token = _env("TELEGRAM_BOT_TOKEN")
    logging.info("All required secrets validated")
    #
    # WARN: Ensure twitter usernames are all valid manually.
    # WARN: Skip this to reduce API requests.
    # valid_twitter_usernames = validate_usernames(twitter_usernames, twitter_bearer_token)
    # if not valid_twitter_usernames:
    #     logging.error("No valid twitter_usernames found")
    #     sys.exit(1)
    #


if __name__ == "__main__":
    main()
