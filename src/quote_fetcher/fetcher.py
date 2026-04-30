"""向 ZenQuotes API 發送 HTTP 請求並解析名言資料。"""

import requests


def fetch_quote() -> tuple[str, str]:
    """從 ZenQuotes API 抓取一則隨機名言。

    Returns:
        (content, author) 名言內容與作者的 tuple。

    Raises:
        requests.HTTPError: HTTP 回應狀態碼為 4xx/5xx 時。
        requests.exceptions.Timeout: 請求逾時時。
    """
    response = requests.get("https://zenquotes.io/api/random", timeout=10)
    response.raise_for_status()
    data = response.json()[0]
    return data["q"], data["a"]
