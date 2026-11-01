"""Base Spider class for concurrent crawling."""

from typing import List, Dict, Any, AsyncGenerator, Optional, Callable
import asyncio
import logging
from ..fetchers import Fetcher

logger = logging.getLogger(__name__)

class Spider:
    name: str = "base"
    start_urls: List[str] = []
    concurrent_requests: int = 4
    request_delay: float = 0.0

    def __init__(self):
        self.fetcher = Fetcher()
        self.middlewares: List[Callable] = []

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        """Override this method to extract data."""
        yield {"url": getattr(response, "url", None), "status": getattr(response, "status_code", None)}

    async def fetch(self, url: str):
        return self.fetcher.get(url)

    def add_middleware(self, fn: Callable):
        self.middlewares.append(fn)

    async def _apply_middlewares(self, item: Dict[str, Any]) -> Dict[str, Any]:
        for mw in self.middlewares:
            item = await mw(item) if asyncio.iscoroutinefunction(mw) else mw(item)
        return item

    async def crawl(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Run concurrent crawl and collect results."""
        urls = urls or self.start_urls
        semaphore = asyncio.Semaphore(self.concurrent_requests)
        results = []

        async def worker(url):
            async with semaphore:
                try:
                    if self.request_delay:
                        await asyncio.sleep(self.request_delay)
                    resp = await self.fetch(url)
                    async for item in self.parse(resp):
                        processed = await self._apply_middlewares(item)
                        results.append(processed)
                except Exception as e:
                    logger.error(f"Failed to crawl {url}: {e}")
                    results.append({"url": url, "error": str(e)})

        await asyncio.gather(*(worker(u) for u in urls))
        return results

    def start(self, urls: Optional[List[str]] = None):
        """Synchronous entry point."""
        return asyncio.run(self.crawl(urls))
