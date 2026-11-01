"""Base Spider class for concurrent crawling."""

from typing import List, Dict, Any, AsyncGenerator, Optional
import asyncio
from ..fetchers import Fetcher

class Spider:
    name: str = "base"
    start_urls: List[str] = []
    concurrent_requests: int = 4

    def __init__(self):
        self.fetcher = Fetcher()

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        """Override this method to extract data."""
        yield {"url": getattr(response, "url", None), "status": getattr(response, "status_code", None)}

    async def fetch(self, url: str):
        return self.fetcher.get(url)

    async def crawl(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Run concurrent crawl and collect results."""
        urls = urls or self.start_urls
        semaphore = asyncio.Semaphore(self.concurrent_requests)
        results = []

        async def worker(url):
            async with semaphore:
                resp = await self.fetch(url)
                async for item in self.parse(resp):
                    results.append(item)

        await asyncio.gather(*(worker(u) for u in urls))
        return results

    def start(self, urls: Optional[List[str]] = None):
        """Synchronous entry point."""
        return asyncio.run(self.crawl(urls))
