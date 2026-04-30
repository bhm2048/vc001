"""fetcher 模組的單元測試。"""

import pytest
import requests

from quote_fetcher.fetcher import fetch_quote


def test_fetch_quote_success(mocker):
    """正常路徑：API 回傳有效 JSON，應解析出 (content, author)。"""
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{"q": "Be yourself.", "a": "Oscar Wilde"}]
    mock_response.raise_for_status.return_value = None
    mocker.patch("quote_fetcher.fetcher.requests.get", return_value=mock_response)

    content, author = fetch_quote()

    assert content == "Be yourself."
    assert author == "Oscar Wilde"


def test_fetch_quote_http_error(mocker):
    """錯誤路徑：HTTP 4xx/5xx，應向上拋出 HTTPError。"""
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    mocker.patch("quote_fetcher.fetcher.requests.get", return_value=mock_response)

    with pytest.raises(requests.HTTPError):
        fetch_quote()


def test_fetch_quote_timeout(mocker):
    """錯誤路徑：網路逾時，應拋出 Timeout。"""
    mocker.patch(
        "quote_fetcher.fetcher.requests.get",
        side_effect=requests.exceptions.Timeout("Request timed out"),
    )

    with pytest.raises(requests.exceptions.Timeout):
        fetch_quote()
