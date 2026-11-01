"""Base Spider class for concurrent crawling."""

from typing import List, Dict, Any, AsyncGenerator

class Spider:
    name: str = "base"
    start_urls: List[str] = []

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        raise NotImplementedError

    def start(self):
        """Start the spider. Placeholder for concurrent execution."""
        return {"status": "started", "urls": self.start_urls}
