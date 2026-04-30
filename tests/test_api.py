"""FastAPI 端點的整合測試。"""

import json

import pytest
from fastapi.testclient import TestClient

from quote_fetcher.api import app

client = TestClient(app)

FAKE_QUOTE = ("Be yourself.", "Oscar Wilde")


# ---------------------------------------------------------------------------
# GET /quotes/random
# ---------------------------------------------------------------------------


def test_get_random_quote_success(mocker):
    """正常路徑：回傳 200 且含 content、author、fetched_at 欄位。"""
    mocker.patch("quote_fetcher.api.fetch_quote", return_value=FAKE_QUOTE)

    resp = client.get("/quotes/random")

    assert resp.status_code == 200
    data = resp.json()
    assert data["content"] == "Be yourself."
    assert data["author"] == "Oscar Wilde"
    assert "fetched_at" in data


def test_get_random_quote_upstream_error(mocker):
    """錯誤路徑：上游 API 失敗時回傳 502。"""
    mocker.patch("quote_fetcher.api.fetch_quote", side_effect=RuntimeError("timeout"))

    resp = client.get("/quotes/random")

    assert resp.status_code == 502


# ---------------------------------------------------------------------------
# GET /quotes
# ---------------------------------------------------------------------------


def test_list_quotes_empty(tmp_path, monkeypatch):
    """quotes.json 不存在時回傳空列表，total 為 0。"""
    monkeypatch.chdir(tmp_path)

    resp = client.get("/quotes")

    assert resp.status_code == 200
    data = resp.json()
    assert data["quotes"] == []
    assert data["total"] == 0


def test_list_quotes_with_data(tmp_path, monkeypatch):
    """有資料時回傳正確的名言列表與 total。"""
    monkeypatch.chdir(tmp_path)
    quotes = [
        {"content": "Stay hungry.", "author": "Steve Jobs", "fetched_at": "2026-01-01T00:00:00+00:00"},
        {"content": "Think different.", "author": "Apple", "fetched_at": "2026-01-02T00:00:00+00:00"},
    ]
    (tmp_path / "quotes.json").write_text(json.dumps(quotes), encoding="utf-8")

    resp = client.get("/quotes")

    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert data["quotes"][0]["content"] == "Stay hungry."
    assert data["quotes"][1]["author"] == "Apple"


# ---------------------------------------------------------------------------
# POST /quotes/fetch
# ---------------------------------------------------------------------------


def test_fetch_and_store_default(tmp_path, monkeypatch, mocker):
    """不帶 count 時預設抓 1 則，回傳 201 且 saved 含 1 筆。"""
    monkeypatch.chdir(tmp_path)
    mocker.patch("quote_fetcher.api.fetch_quote", return_value=FAKE_QUOTE)

    resp = client.post("/quotes/fetch")

    assert resp.status_code == 201
    data = resp.json()
    assert len(data["saved"]) == 1
    assert data["saved"][0]["content"] == "Be yourself."


def test_fetch_and_store_count(tmp_path, monkeypatch, mocker):
    """count=3 時回傳 3 筆並寫入 quotes.json。"""
    monkeypatch.chdir(tmp_path)
    mocker.patch("quote_fetcher.api.fetch_quote", return_value=FAKE_QUOTE)

    resp = client.post("/quotes/fetch?count=3")

    assert resp.status_code == 201
    assert len(resp.json()["saved"]) == 3
    saved = json.loads((tmp_path / "quotes.json").read_text(encoding="utf-8"))
    assert len(saved) == 3


def test_fetch_and_store_count_too_large():
    """count > 50 應回傳 422 Unprocessable Entity。"""
    resp = client.post("/quotes/fetch?count=51")

    assert resp.status_code == 422


def test_fetch_and_store_upstream_error(tmp_path, monkeypatch, mocker):
    """上游 API 失敗時回傳 502。"""
    monkeypatch.chdir(tmp_path)
    mocker.patch("quote_fetcher.api.fetch_quote", side_effect=RuntimeError("timeout"))

    resp = client.post("/quotes/fetch")

    assert resp.status_code == 502
