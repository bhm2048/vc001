import argparse
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


def list_quotes():
    if not os.path.exists(QUOTES_FILE):
        print("尚無已儲存的名言。")
        return
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        quotes = json.load(f)
    if not quotes:
        print("尚無已儲存的名言。")
        return
    for i, q in enumerate(quotes, 1):
        print(f"{i}. \"{q['content']}\" — {q['author']}")


def fetch_and_save(count):
    for _ in range(count):
        content, author = fetch_quote()
        print(f'"{content}"')
        print(f"— {author}")
        save_quote(content, author)
        print(f"(已儲存至 {QUOTES_FILE})\n")


def main():
    parser = argparse.ArgumentParser(description="抓取並儲存名言")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--count", type=int, default=1, metavar="N", help="抓取 N 則名言（預設為 1）")
    group.add_argument("--list", action="store_true", help="列出所有已儲存的名言")
    args = parser.parse_args()

    if args.list:
        list_quotes()
    else:
        fetch_and_save(args.count)


if __name__ == "__main__":
    main()
