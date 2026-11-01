"""YouTube search spider (browser-based)."""

from typing import List, Dict, Any, AsyncGenerator, Optional
from .base import Spider
from ..models import Video
from ..fetchers import StealthyFetcher

class YouTubeSearchSpider(Spider):
    name = "youtube_search"
    category = "video"

    def __init__(self, query: str = "AI", max_results: int = 10):
        super().__init__()
        self.query = query
        self.max_results = max_results
        self.stealth = StealthyFetcher(headless=True)

    async def fetch(self, url: str):
        # Override to use browser for YouTube
        result = self.stealth.fetch(url, wait_selector="ytd-video-renderer")
        class FakeResp:
            def __init__(self, r):
                self.text = r.get("html", "")
                self.status_code = 200 if r.get("status") == "success" else 500
                self.url = r.get("url", url)
        return FakeResp(result)

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        # Basic extraction from rendered HTML
        titles = response.text_content("#video-title") if hasattr(response, "text_content") else []
        # Fallback simple parse
        if not titles and response.text:
            # very rough
            pass
        for title in titles[:self.max_results]:
            yield Video(
                source="YouTube",
                title=title,
                url=f"https://www.youtube.com/results?search_query={self.query}",
                category=self.category,
            ).to_dict()

    def start(self, urls: Optional[List[str]] = None):
        search_url = f"https://www.youtube.com/results?search_query={self.query.replace(' ', '+')}"
        return super().start([search_url])
