"""Simple HTTP management server for DeepSeek Harness integration."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "unified-scraper"}).encode())
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "accounts": "use AccountManager",
                "endpoints": ["/health", "/status", "/search"]
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/search":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            data = json.loads(body) if body else {}
            # Placeholder for X search via XClient
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "query": data.get("query"),
                "status": "accepted",
                "note": "Connect to XClient here"
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8080):
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Management server running on http://0.0.0.0:{port}")
    print("DeepSeek Harness can call /health, /status, /search")
    server.serve_forever()

if __name__ == "__main__":
    run()
