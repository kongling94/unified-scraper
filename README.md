# Unified Scraper

统一网页爬取框架，整合 [Scrapling](https://github.com/D4Vinci/Scrapling) 的通用爬取能力与 [twscrape](https://github.com/vladkens/twscrape) 的 X/Twitter 专用能力。

面向金融、科技、AI 领域研究与社媒分析的数据采集框架。

## Docker Compose 部署

```bash
docker compose up -d --build
```

服务启动后：`http://localhost:8080`

## 研究数据采集示例

```bash
python examples/research_pipeline_example.py
```

当前内置 Spider：
- TechCrunch
- The Verge
- Hacker News
- CNBC
- YouTube 搜索（浏览器模式）

统一输出为 `Article` / `Video` 结构，便于后续分析与报告生成。

## 爬虫报告展示形式

- **Markdown**（默认）
- **JSON**
- **Text**

```python
from unified_scraper.utils import generate_report
report = generate_report(results, title="AI & Finance News", format="markdown")
```

## DeepSeek Harness 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/status` | 服务状态 |
| GET | `/accounts` | 查看账号列表 |
| POST | `/search` | X 搜索 |
| POST | `/accounts/add` | 添加账号（支持 proxy） |

## 当地开发

```bash
pip install -e .
python examples/research_pipeline_example.py
python examples/report_example.py
```

## 当前功能

- ✅ 通用 Fetcher + Adaptive 解析
- ✅ 研究向 Spider（TechCrunch / The Verge / HN / CNBC / YouTube）
- ✅ 统一数据模型（Article / Video）
- ✅ X 爬取 + 账号管理 + 代理
- ✅ 报告生成（Markdown / JSON / Text）
- ✅ Docker Compose + 管理 API

详细进度见 `DEVELOPMENT.md`。
