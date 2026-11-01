# Unified Scraper

统一网页爬取框架，整合 [Scrapling](https://github.com/D4Vinci/Scrapling) 的通用爬取能力与 [twscrape](https://github.com/vladkens/twscrape) 的 X/Twitter 专用能力。

## Docker Compose 部署

```bash
docker compose up -d --build
```

服务启动后：
- 管理接口：`http://localhost:8080`
- 健康检查：`GET /health`
- 状态：`GET /status`
- 搜索接口：`POST /search` （JSON: `{"query": "AI"}`）

## DeepSeek Harness 管理

部署后可通过 DeepSeek Harness 调用以下接口进行管理操作：

- `GET /health` — 检查服务状态
- `GET /status` — 查看当前能力
- `POST /search` — 触发 X 搜索（需配置账号）

示例（Harness 内可直接调用）：
```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/search -H "Content-Type: application/json" -d '{"query":"AI"}'
```

## 当地开发

```bash
pip install -e .
python examples/basic_usage.py
```

## 当前功能

- ✅ HTTP Fetcher + CSS 解析
- ✅ StealthyFetcher（Playwright）
- ✅ AccountManager 轮换 + 锁定
- ✅ XClient GraphQL 结构
- ✅ Docker Compose 部署 + 管理接口

详细进度见 `DEVELOPMENT.md`。
