# Unified Scraper

统一网页爬取框架，整合 [Scrapling](https://github.com/D4Vinci/Scrapling) 的通用爬取能力与 [twscrape](https://github.com/vladkens/twscrape) 的 X/Twitter 专用能力。

## 当前状态（Phase 1 完成，Phase 2 进行中）

- ✅ HTTP Fetcher + CSS 解析（selectolax）
- ✅ StealthyFetcher（Playwright）
- ✅ AccountManager 轮换 + 锁定
- ✅ XClient GraphQL 结构就绪（需更新 query ID）
- ⏳ Spider 框架完善中

## 快速开始

```bash
pip install -e .
python examples/basic_usage.py
```

## 使用示例

```python
from unified_scraper import Fetcher, StealthyFetcher, AccountManager, XClient

# HTTP
f = Fetcher()
page = f.get("https://quotes.toscrape.com/")
print(page.text_content(".quote .text")[:2])

# Browser
s = StealthyFetcher()
print(s.fetch("https://quotes.toscrape.com/"))

# X
mgr = AccountManager()
# mgr.add("user", "auth_token", "ct0")
client = XClient(mgr)
# await client.search("AI")
```

详细进度见 `DEVELOPMENT.md`。
