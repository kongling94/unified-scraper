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
| POST | `/accounts/add` | 添加账号 `{"username":"","auth_token":"","ct0":"","proxy":""}` |
| POST | `/accounts/lock` | 锁定账号 |
| POST | `/accounts/unlock` | 解锁账号 |

示例：
```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/accounts/add \
  -H "Content-Type: application/json" \
  -d '{"username":"u1","auth_token":"xxx","ct0":"yyy","proxy":"http://proxy:8080"}'
curl -X POST http://localhost:8080/search \
  -H "Content-Type: application/json" \
  -d '{"query":"AI"}'
```

## 当地开发

```bash
pip install -e .
python examples/basic_usage.py
python examples/proxy_example.py
python examples/spider_example.py
python examples/user_timeline_example.py
python examples/user_id_and_endpoints_example.py
python examples/adaptive_markdown_example.py
python -m pytest tests/ -q
```

## 当前功能

- ✅ HTTP Fetcher + CSS 解析 + Adaptive 元素追踪
- ✅ StealthyFetcher（Playwright）
- ✅ AccountManager 轮换 + 锁定 + 代理 + API
- ✅ XClient 搜索 + User Timeline（富解析 + 代理 + 用户 ID 解析）
- ✅ 额外端点骨架：回复、点赞
- ✅ Spider 并发爬取 + 中间件 + 错误处理
- ✅ Markdown 导出
- ✅ Docker Compose + 完整管理 API
- ✅ 单元测试 + 集成测试 + X 冒烟测试

详细进度见 `DEVELOPMENT.md`。
