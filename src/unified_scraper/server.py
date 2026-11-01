"""HTTP management server for DeepSeek Harness integration."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import asyncio
from .accounts import AccountManager
from .x import XClient

# Global manager (persists via volume)
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
                "endpoints": ["/health", "/status", "/search", "/accounts"]
            })
        elif self.path == "/accounts":
            accounts = account_manager.list_accounts()
            self._json(200, {
                "accounts": [{"username": a.username, "locked": a.locked} for a in accounts]
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/search":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            data = json.loads(body) if body else {}
            query = data.get("query", "")
            limit = data.get("limit", 10)

            if not query:
                self._json(400, {"error": "query is required"})
                return

            try:
                # Run async search in sync context
                results = asyncio.run(x_client.search(query, limit=limit))
                self._json(200, {
                    "query": query,
                    "results": results,
                    "status": "success"
                })
            except Exception as e:
                self._json(500, {"error": str(e), "query": query})
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
    print("DeepSeek Harness endpoints: /health, /status, /accounts, /search")
    server.serve_forever()

if __name__ == "__main__":
    run()
