# Unified Scraper

统一网页爬取框架，整合 [Scrapling](https://github.com/D4Vinci/Scrapling) 的通用爬取能力与 [twscrape](https://github.com/vladkens/twscrape) 的 X/Twitter 专用能力。

## 设计目标

- **通用网页爬取**：基于 Scrapling 思路，支持 HTTP 快速请求、隐身浏览器、自适应解析、Spider 框架。
- **X 爬取**：基于 twscrape 思路，支持搜索、时间线、用户信息，使用登录账号 cookies。
- **账号管理**：集中管理 X 账号池，自动轮换、速率限制处理。
- **优化整合**：清晰模块划分、统一 API、便于扩展为 AI/科技资讯爬取。

## 目录结构

```
unified-scraper/
├── README.md
├── pyproject.toml
├── src/
│   ├── unified_scraper/
│   │   ├── __init__.py
│   │   ├── fetchers/          # 通用爬取（HTTP / Browser）
│   │   ├── x/                 # X 专用爬取
│   │   ├── accounts/          # X 账号管理
│   │   ├── spiders/           # Spider 框架
│   │   └── utils/
└── examples/
```

## 代码分析摘要

### Scrapling 优点
- 多种 Fetcher（HTTP、Stealthy Browser、Dynamic）
- 自适应元素定位
- Spider 并发与会话管理
- Cloudflare 绕过
- MCP / AI 友好

### twscrape 优点
- X GraphQL 接口封装
- 多账号池轮换
- 速率限制自动处理
- 登录 cookies 管理
- 搜索与时间线支持

### 整合方案
将两者的核心模块抽取并统一接口，添加账号管理层，使用者可以：
1. 用通用 Fetcher 爬新闻网站
2. 用 X 模块爬 X 上的讨论
3. 通过账号管理器统一处理多账号

## 快速开始

```bash
pip install -e .
```

（代码框架正在逐步完善）
