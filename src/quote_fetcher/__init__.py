"""quote_fetcher：從 ZenQuotes API 抓取並儲存名言的工具。"""

from .fetcher import fetch_quote
from .storage import list_quotes, load_quotes, save_quote

__all__ = ["fetch_quote", "load_quotes", "save_quote", "list_quotes"]
