# Unified Scraper

统一网页爬取框架，整合 [Scrapling](https://github.com/D4Vinci/Scrapling) 的通用爬取能力与 [twscrape](https://github.com/vladkens/twscrape) 的 X/Twitter 专用能力。

面向金融、科技、AI 领域研究与社媒分析的数据采集框架。

## Docker Compose 部署

```bash
docker compose up -d --build
```

服务启动后：`http://localhost:8080`

## 研究数据采集

```bash
python examples/custom_sections_and_save_example.py
python examples/png_and_structured_example.py
```

### 当前内置 Spider

**科技 / AI**：TechCrunch, The Verge, Ars Technica, Wired, VentureBeat, Hacker News, arXiv, Papers with Code, GitHub Trending, MIT Technology Review

**金融**：CNBC, Reuters, Yahoo Finance, CoinDesk, Seeking Alpha, CoinTelegraph

**社区**：Reddit

**视频**：YouTube、Bilibili

## 爬虫报告功能

- 多格式：`markdown` / `html` / `png` / `json` / `text`
- 自动去重
- 固定章节（`structured=true`）或**自定义章节**
- **自动落盘**（`auto_save=true`）

### 自定义章节示例

```python
custom = {
    "AI 与技术热点": ["ai", "arxiv", "techcrunch"],
    "金融与加密": ["coin", "finance"],
    "视频趋势": ["youtube", "bilibili"],
}
result = generate_report(
    results,
    title="自定义快照",
    format="html",
    custom_sections=custom,
    auto_save=True,
    output_dir="reports",
)
print(result["saved_path"])
```

### Harness 调用

```bash
curl -X POST http://localhost:8080/report \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["techcrunch", "arxiv", "cointelegraph"],
    "format": "html",
    "custom_sections": {
      "AI热点": ["ai", "arxiv"],
      "金融": ["coin", "finance"]
    },
    "auto_save": true,
    "dedupe": true
  }'
```

返回中会包含 `saved_path`。

## 当前功能

- ✅ 多源研究 Spider
- ✅ 报告去重 + 自定义章节 + 自动落盘
- ✅ HTML 卡片 / PNG 长图
- ✅ Harness `/report` 完整支持
- ✅ Docker Compose

详细进度见 `DEVELOPMENT.md`。
