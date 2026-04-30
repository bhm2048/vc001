"""main 模組的單元測試。"""

import json

import pytest

from main import fetch_and_save, list_quotes, save_quote


# ---------------------------------------------------------------------------
# save_quote
# ---------------------------------------------------------------------------


def test_save_quote_creates_file(tmp_path, monkeypatch):
    """quotes.json 不存在時，應建立檔案並寫入第一筆。"""
    monkeypatch.chdir(tmp_path)

    save_quote("Hello world.", "Unknown")

    quotes_file = tmp_path / "quotes.json"
    assert quotes_file.exists()
    data = json.loads(quotes_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["content"] == "Hello world."
    assert data[0]["author"] == "Unknown"


def test_save_quote_appends(tmp_path, monkeypatch):
    """quotes.json 已存在時，應 append 而非覆蓋舊資料。"""
    monkeypatch.chdir(tmp_path)

    save_quote("First quote.", "Author A")
    save_quote("Second quote.", "Author B")

    data = json.loads((tmp_path / "quotes.json").read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["content"] == "First quote."
    assert data[1]["content"] == "Second quote."


def test_save_quote_has_fetched_at_field(tmp_path, monkeypatch):
    """儲存的每筆資料都必須含 fetched_at 欄位。"""
    monkeypatch.chdir(tmp_path)

    save_quote("Time check.", "Clock")

    data = json.loads((tmp_path / "quotes.json").read_text(encoding="utf-8"))
    assert "fetched_at" in data[0]
    assert data[0]["fetched_at"]  # 非空字串


# ---------------------------------------------------------------------------
# list_quotes
# ---------------------------------------------------------------------------


def test_list_quotes_no_file(tmp_path, monkeypatch, capsys):
    """quotes.json 不存在時，應印出提示訊息。"""
    monkeypatch.chdir(tmp_path)

    list_quotes()

    assert "尚無已儲存的名言" in capsys.readouterr().out


def test_list_quotes_empty(tmp_path, monkeypatch, capsys):
    """quotes.json 存在但為空陣列時，應印出提示訊息。"""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "quotes.json").write_text("[]", encoding="utf-8")

    list_quotes()

    assert "尚無已儲存的名言" in capsys.readouterr().out


def test_list_quotes_with_data(tmp_path, monkeypatch, capsys):
    """有資料時，應依序印出格式正確的名言。"""
    monkeypatch.chdir(tmp_path)
    quotes = [
        {"content": "Be yourself.", "author": "Oscar Wilde", "fetched_at": "2026-01-01T00:00:00+00:00"},
        {"content": "Stay hungry.", "author": "Steve Jobs", "fetched_at": "2026-01-02T00:00:00+00:00"},
    ]
    (tmp_path / "quotes.json").write_text(
        json.dumps(quotes, ensure_ascii=False), encoding="utf-8"
    )

    list_quotes()

    out = capsys.readouterr().out
    assert "Be yourself." in out
    assert "Oscar Wilde" in out
    assert "Stay hungry." in out
    assert "Steve Jobs" in out


# ---------------------------------------------------------------------------
# fetch_and_save
# ---------------------------------------------------------------------------


def test_fetch_and_save_calls_count(tmp_path, monkeypatch, mocker):
    """fetch_and_save(n) 應呼叫 fetch_quote 恰好 n 次，並呼叫 save_quote n 次。"""
    monkeypatch.chdir(tmp_path)
    mock_fetch = mocker.patch("main.fetch_quote", return_value=("Quote.", "Author"))

    fetch_and_save(3)

    assert mock_fetch.call_count == 3
    data = json.loads((tmp_path / "quotes.json").read_text(encoding="utf-8"))
    assert len(data) == 3
