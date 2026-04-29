# CLAUDE.md

## 專案目的

從 [ZenQuotes API](https://zenquotes.io/api/random) 隨機抓取名言佳句，儲存至本地 `quotes.json`，並支援命令列列出已儲存的名言。

- `main.py` — CLI 入口，處理 `--count` 與 `--list` 參數，儲存名言至 JSON
- `fetcher.py` — 向 ZenQuotes API 發送 HTTP 請求並解析回應

## 技術棧

| 元件 | 版本 |
|------|------|
| Python | 3.x |
| requests | 2.33.x |
| argparse | 標準函式庫 |
| pytest | 測試框架 |
| pytest-cov | 覆蓋率報告 |

依賴版本鎖定於 `requirements.txt`。

## 編碼規範

### PEP 8
- 縮排使用 **4 個空格**，禁止 Tab
- 每行不超過 **88 字元**（與 Black 預設一致）
- 模組、函式、變數名稱使用 `snake_case`；類別使用 `PascalCase`
- 匯入依序分組：標準函式庫 → 第三方套件 → 本地模組，組間空一行

### Type Hints
所有函式簽名都必須加上型別標注：

```python
def fetch_quote() -> tuple[str, str]:
    ...

def save_quote(content: str, author: str) -> None:
    ...
```

### Docstrings（Google Style）
所有公開函式、模組必須加上 Google Style docstring：

```python
def save_quote(content: str, author: str) -> None:
    """將名言儲存至本地 JSON 檔案。

    Args:
        content: 名言內容。
        author: 名言作者。
    """
```

### Module Docstring
**每個 Python 檔案頂部都必須加上 module docstring**，格式如下：

```python
"""模組功能一句話描述。

詳細說明（可選）。
"""
```

## 測試規範

使用 **pytest** 撰寫測試，目標覆蓋率 **≥ 80%**。

```bash
# 執行測試並產生覆蓋率報告
pytest --cov=. --cov-report=term-missing

# 設定覆蓋率門檻（未達則失敗）
pytest --cov=. --cov-fail-under=80
```

測試原則：
- 對外部 HTTP 請求使用 `unittest.mock.patch` 或 `pytest-mock` 進行 mock
- 測試檔案放在 `tests/` 目錄，命名為 `test_<module>.py`
- 每個公開函式至少有一個正常路徑與一個錯誤路徑的測試案例

## Commit 訊息規範

使用 **Conventional Commits** 格式：

```
<type>(<scope>): <subject>

[body]

[footer]
```

常用 type：
| type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修復 bug |
| `chore` | 建置、依賴、設定等雜務 |
| `refactor` | 重構（不改變行為） |
| `test` | 新增或修改測試 |
| `docs` | 文件變更 |

範例：
```
feat(cli): add --count argument to fetch multiple quotes
fix(fetcher): handle network timeout with retry logic
chore: freeze dependencies in requirements.txt
```
