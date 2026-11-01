# Unified Scraper

统一网页爬取框架，整合 [Scrapling](https://github.com/D4Vinci/Scrapling) 的通用爬取能力与 [twscrape](https://github.com/vladkens/twscrape) 的 X/Twitter 专用能力。

## Docker Compose 部署

```bash
docker compose up -d --build
```

服务启动后：`http://localhost:8080`

## DeepSeek Harness 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/status` | 服务状态 |
| GET | `/accounts` | 查看账号列表 |
| POST | `/search` | X 搜索 `{"query":"AI","limit":10}` |
| POST | `/accounts/add` | 添加账号 `{"username":"","auth_token":"","ct0":""}` |
| POST | `/accounts/lock` | 锁定账号 |
| POST | `/accounts/unlock` | 解锁账号 |

示例：
```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/accounts/add \
  -H "Content-Type: application/json" \
  -d '{"username":"u1","auth_token":"xxx","ct0":"yyy"}'
curl -X POST http://localhost:8080/search \
  -H "Content-Type: application/json" \
  -d '{"query":"AI"}'
```

## 当地开发

```bash
pip install -e .
python examples/basic_usage.py
python examples/spider_example.py
python -m pytest tests/ -q
```

## 当前功能

- ✅ HTTP Fetcher + CSS 解析
- ✅ StealthyFetcher（Playwright）
- ✅ AccountManager 轮换 + 锁定 + API
- ✅ XClient 真实 GraphQL 请求（需更新 query ID）
- ✅ Spider 并发爬取框架
- ✅ Docker Compose + 完整管理 API
- ✅ 基础单元测试

详细进度见 `DEVELOPMENT.md`。
