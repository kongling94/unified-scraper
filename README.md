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
python examples/full_research_pipeline.py
```

### 当前内置 Spider

**科技 / AI**
- TechCrunch, The Verge, Ars Technica, Wired, VentureBeat, Hacker News

**金融**
- CNBC, Reuters, Yahoo Finance, CoinDesk, Seeking Alpha

**社区**
- Reddit（r/MachineLearning、r/artificial 等）

**视频**
- YouTube 搜索（标题、视频 ID、播放量、发布时间）
- Bilibili 热门

统一输出为 `Article` / `Video` 结构。

## 爬虫报告展示形式

- **Markdown**（默认）
- **JSON**
- **Text**

Harness 可直接调用：
```bash
curl -X POST http://localhost:8080/report \
  -H "Content-Type: application/json" \
  -d '{"sources":["techcrunch","hn","coindesk"],"format":"markdown","title":"Daily Snapshot"}'
```

## DeepSeek Harness 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/status` | 服务状态 |
| GET | `/accounts` | 查看账号列表 |
| POST | `/search` | X 搜索 |
| POST | `/report` | 生成多源研究报告 |
| POST | `/accounts/add` | 添加账号（支持 proxy） |

## 当地开发

```bash
pip install -e .
python examples/full_research_pipeline.py
```

## 当前功能

- ✅ 通用 Fetcher + Adaptive 解析
- ✅ 多源研究 Spider（科技 / AI / 金融 / Reddit / YouTube / Bilibili）
- ✅ 统一数据模型（Article / Video）
- ✅ X 爬取 + 账号管理 + 代理
- ✅ 报告生成（Markdown / JSON / Text）+ Harness `/report`
- ✅ Docker Compose + 管理 API

详细进度见 `DEVELOPMENT.md`。
