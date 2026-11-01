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
python examples/png_and_structured_example.py
python examples/html_report_example.py
```

### 当前内置 Spider

**科技 / AI**：TechCrunch, The Verge, Ars Technica, Wired, VentureBeat, Hacker News, arXiv, Papers with Code, GitHub Trending, MIT Technology Review

**金融**：CNBC, Reuters, Yahoo Finance, CoinDesk, Seeking Alpha, CoinTelegraph

**社区**：Reddit

**视频**：YouTube、Bilibili

## 爬虫报告呈现形式

支持五种格式（默认去重）：

| 格式 | 说明 |
|------|------|
| `markdown` | 默认，便于编辑与存档 |
| `html` | 卡片式网页，可直接浏览器打开分享 |
| `png` | 长图，适合微信/社媒转发（需 `pip install pillow`） |
| `json` | 结构化 |
| `text` | 纯文本 |

支持固定章节结构（`structured=True`）：
- **热点摘要**（AI / 科技）
- **待关注**（金融）
- **已结论**
- **其他**

```python
from unified_scraper.utils import generate_report

# 结构化 HTML
html = generate_report(results, title="每日快照", format="html", structured=True)

# PNG 长图
png = generate_report(results, title="每日快照", format="png")
with open("report.png", "wb") as f:
    f.write(png)
```

## DeepSeek Harness 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/search` | X 搜索 |
| POST | `/report` | 生成报告（markdown/html/json/text + dedupe） |
| POST | `/accounts/add` | 添加账号 |

## 当前功能

- ✅ 多源研究 Spider
- ✅ 报告自动去重
- ✅ HTML 卡片式报告 + 固定章节结构
- ✅ PNG 长图导出
- ✅ Harness `/report`
- ✅ 统一数据模型 + X 爬取 + Docker

详细进度见 `DEVELOPMENT.md`。
