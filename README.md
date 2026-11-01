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
python examples/deduped_report_example.py
python examples/full_research_pipeline.py
```

### 当前内置 Spider

**科技 / AI**
- TechCrunch, The Verge, Ars Technica, Wired, VentureBeat, Hacker News
- arXiv (cs.AI / cs.LG), Papers with Code, GitHub Trending, MIT Technology Review

**金融**
- CNBC, Reuters, Yahoo Finance, CoinDesk, Seeking Alpha, CoinTelegraph

**社区**
- Reddit（r/MachineLearning、r/artificial 等）

**视频**
- YouTube 搜索、Bilibili 热门

## 爬虫报告（支持去重）

默认会按标题去重（可关闭）。

```bash
curl -X POST http://localhost:8080/report \
  -H "Content-Type: application/json" \
  -d '{"sources":["techcrunch","arxiv","github","cointelegraph"],"format":"markdown","dedupe":true,"title":"Daily Snapshot"}'
```

Python：
```python
from unified_scraper.utils import generate_report
report = generate_report(results, title="Snapshot", format="markdown", dedupe=True)
```

## DeepSeek Harness 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/status` | 服务状态 |
| POST | `/search` | X 搜索 |
| POST | `/report` | 生成去重研究报告 |
| POST | `/accounts/add` | 添加账号 |

## 当前功能

- ✅ 多源研究 Spider（含 arXiv、GitHub Trending、CoinTelegraph 等）
- ✅ 报告自动去重（标题相似度）
- ✅ Harness `/report` 支持 `dedupe` 参数
- ✅ 统一数据模型 + X 爬取 + Docker

详细进度见 `DEVELOPMENT.md`。
