"""CLI 入口：抓取名言並儲存，或列出已儲存的名言。"""

import argparse

from .fetcher import fetch_quote
from .storage import QUOTES_FILE, list_quotes, save_quote


def fetch_and_save(count: int) -> None:
    """抓取指定數量的名言並逐一儲存。

    Args:
        count: 要抓取的名言數量。
    """
    for _ in range(count):
        content, author = fetch_quote()
        print(f'"{content}"')
        print(f"— {author}")
        save_quote(content, author)
        print(f"(已儲存至 {QUOTES_FILE})\n")


def main() -> None:
    """解析命令列參數並執行對應動作。"""
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
