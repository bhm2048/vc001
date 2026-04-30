"""FastAPI web API：將 quote-fetcher 的核心功能包裝成 HTTP 端點。"""

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from .fetcher import fetch_quote
from .schemas import FetchResponse, Quote, QuoteListResponse
from .storage import load_quotes, save_quote

app = FastAPI(title="Quote Fetcher API", version="0.1.0")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/quotes/random", response_model=Quote, summary="抓取一則新名言（不儲存）")
def get_random_quote() -> Quote:
    """從 ZenQuotes API 即時抓取一則名言並回傳，不寫入本地儲存。"""
    try:
        content, author = fetch_quote()
    except Exception as exc:
        raise HTTPException(status_code=502, detail="上游 API 發生錯誤") from exc
    from datetime import datetime, timezone
    return Quote(
        content=content,
        author=author,
        fetched_at=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/quotes", response_model=QuoteListResponse, summary="列出所有已儲存的名言")
def list_saved_quotes() -> QuoteListResponse:
    """回傳 quotes.json 中所有已儲存的名言。"""
    raw = load_quotes()
    quotes = [Quote(**q) for q in raw]
    return QuoteListResponse(quotes=quotes, total=len(quotes))


@app.post("/quotes/fetch", response_model=FetchResponse, status_code=201, summary="抓取並儲存名言")
def fetch_and_store(
    count: int = Query(default=1, ge=1, le=50, description="要抓取的名言數量"),
) -> FetchResponse:
    """從 ZenQuotes API 抓取 count 則名言，逐一儲存至 quotes.json 後回傳。"""
    saved: list[Quote] = []
    for _ in range(count):
        try:
            content, author = fetch_quote()
        except Exception as exc:
            raise HTTPException(status_code=502, detail="上游 API 發生錯誤") from exc
        save_quote(content, author)
        raw = load_quotes()
        saved.append(Quote(**raw[-1]))
    return FetchResponse(saved=saved)


def run() -> None:
    """uvicorn 啟動入口，供 quote-fetcher-api 指令使用。"""
    uvicorn.run("quote_fetcher.api:app", host="0.0.0.0", port=8000, reload=False)
