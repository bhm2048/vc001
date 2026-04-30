"""Pydantic request / response models for the FastAPI web API."""

from pydantic import BaseModel, Field


class Quote(BaseModel):
    """單則名言的資料結構。"""

    content: str
    author: str
    fetched_at: str


class FetchResponse(BaseModel):
    """POST /quotes/fetch 的回應：本次新增的名言列表。"""

    saved: list[Quote]


class QuoteListResponse(BaseModel):
    """GET /quotes 的回應：所有已儲存的名言及總數。"""

    quotes: list[Quote]
    total: int = Field(description="已儲存名言的總數")
