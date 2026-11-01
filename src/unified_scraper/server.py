"""HTTP management server for DeepSeek Harness integration."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import asyncio
from .accounts import AccountManager
from .x import XClient
from .utils import generate_report
from .spiders import (
    TechCrunchSpider, TheVergeSpider, HackerNewsSpider,
    CoinDeskSpider, RedditSpider, YouTubeSearchSpider,
    ArxivSpider, GitHubTrendingSpider, CoinTelegraphSpider, MITTechReviewSpider,
)

account_manager = AccountManager("/app/accounts.db")
x_client = XClient(account_manager)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "ok", "service": "unified-scraper"})
        elif self.path == "/status":
            accounts = account_manager.list_accounts()
            self._json(200, {
                "accounts_count": len(accounts),
                "endpoints": ["/health", "/status", "/search", "/accounts", "/report"]
            })
        elif self.path == "/accounts":
            accounts = account_manager.list_accounts()
            self._json(200, {
                "accounts": [{"username": a.username, "locked": a.locked, "proxy": a.proxy} for a in accounts]
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length else "{}"
        data = json.loads(body)

        if self.path == "/search":
            query = data.get("query", "")
            limit = data.get("limit", 10)
            if not query:
                self._json(400, {"error": "query is required"})
                return
            try:
                results = asyncio.run(x_client.search(query, limit=limit))
                self._json(200, {"query": query, "results": results, "status": "success"})
            except Exception as e:
                self._json(500, {"error": str(e), "query": query})

        elif self.path == "/report":
            sources = data.get("sources", ["techcrunch", "hn", "arxiv"])
            fmt = data.get("format", "markdown")
            title = data.get("title", "Research Report")
            dedupe = data.get("dedupe", True)
            items = []
            spider_map = {
                "techcrunch": TechCrunchSpider,
                "verge": TheVergeSpider,
                "hn": HackerNewsSpider,
                "coindesk": CoinDeskSpider,
                "arxiv": ArxivSpider,
                "github": GitHubTrendingSpider,
                "cointelegraph": CoinTelegraphSpider,
                "mit": MITTechReviewSpider,
                "reddit_ml": lambda: RedditSpider("MachineLearning"),
                "youtube": lambda: YouTubeSearchSpider(data.get("query", "AI"), 5),
            }
            for src in sources:
                try:
                    cls = spider_map.get(src)
                    if not cls:
                        continue
                    spider = cls() if not callable(cls) else cls()
                    items.extend(spider.start())
                except Exception:
                    continue
            report = generate_report(items, title=title, format=fmt, dedupe=dedupe)
            self._json(200, {
                "status": "success",
                "count": len(items),
                "format": fmt,
                "deduped": dedupe,
                "report": report,
            })

        elif self.path == "/accounts/add":
            username = data.get("username")
            auth_token = data.get("auth_token")
            ct0 = data.get("ct0")
            proxy = data.get("proxy")
            if not all([username, auth_token, ct0]):
                self._json(400, {"error": "username, auth_token, ct0 required"})
                return
            account_manager.add(username, auth_token, ct0, proxy)
            self._json(200, {"status": "added", "username": username})

        elif self.path == "/accounts/lock":
            username = data.get("username")
            if not username:
                self._json(400, {"error": "username required"})
                return
            account_manager.lock(username)
            self._json(200, {"status": "locked", "username": username})

        elif self.path == "/accounts/unlock":
            username = data.get("username")
            if not username:
                self._json(400, {"error": "username required"})
                return
            account_manager.unlock(username)
            self._json(200, {"status": "unlocked", "username": username})

        else:
            self.send_response(404)
            self.end_headers()

    def _json(self, code: int, data: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

def run(port=8080):
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Management server running on http://0.0.0.0:{port}")
    print("Endpoints: /health /status /accounts /search /report /accounts/add ...")
    server.serve_forever()

if __name__ == "__main__":
    run()
