"""Fast HTTP fetcher with browser impersonation (inspired by Scrapling Fetcher)."""

import httpx
from typing import Optional, Dict, Any, List
from selectolax.parser import HTMLParser

class Fetcher:
    """Lightweight HTTP fetcher with optional browser TLS fingerprinting."""

    def __init__(self, impersonate: str = "chrome", headers: Optional[Dict] = None, timeout: float = 30.0):
        self.impersonate = impersonate
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.timeout = timeout

    def get(self, url: str, **kwargs) -> "Response":
        """Perform a GET request."""
        with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
            resp = client.get(url, **kwargs)
            return Response(resp)

    def post(self, url: str, **kwargs) -> "Response":
        """Perform a POST request."""
        with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
            resp = client.post(url, **kwargs)
            return Response(resp)

class Response:
    def __init__(self, resp: httpx.Response):
        self.status_code = resp.status_code
        self.text = resp.text
        self.content = resp.content
        self.url = str(resp.url)
        self._tree = None

    @property
    def tree(self):
        if self._tree is None:
            self._tree = HTMLParser(self.text)
        return self._tree

    def css(self, selector: str) -> List[Any]:
        """Select elements using CSS selector."""
        return self.tree.css(selector)

    def text_content(self, selector: str) -> List[str]:
        """Extract text from elements matching the selector."""
        return [node.text(strip=True) for node in self.css(selector) if node.text(strip=True)]
