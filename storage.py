"""名言的本地儲存與讀取邏輯。"""

import json
import os
from datetime import datetime, timezone

QUOTES_FILE = "quotes.json"


def load_quotes() -> list[dict]:
    """從 quotes.json 讀取所有已儲存的名言。

    Returns:
        已儲存的名言列表；檔案不存在時回傳空 list。
    """
    if not os.path.exists(QUOTES_FILE):
        return []
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_quote(content: str, author: str) -> None:
    """將一則名言 append 至 quotes.json。

    Args:
        content: 名言內容。
        author: 名言作者。
    """
    quotes = load_quotes()
    quotes.append({
        "content": content,
        "author": author,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    })
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)


def list_quotes() -> None:
    """印出所有已儲存的名言；無資料時顯示提示訊息。"""
    quotes = load_quotes()
    if not quotes:
        print("尚無已儲存的名言。")
        return
    for i, q in enumerate(quotes, 1):
        print(f"{i}. \"{q['content']}\" — {q['author']}")
