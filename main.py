import json
import os
from datetime import datetime, timezone

from fetcher import fetch_quote

QUOTES_FILE = "quotes.json"


def save_quote(content, author):
    quotes = []
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            quotes = json.load(f)

    quotes.append({
        "content": content,
        "author": author,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    })

    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)


def main():
    content, author = fetch_quote()
    print(f'"{content}"')
    print(f"— {author}")
    save_quote(content, author)
    print(f"(已儲存至 {QUOTES_FILE})")


if __name__ == "__main__":
    main()
