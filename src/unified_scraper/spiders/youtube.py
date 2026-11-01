"""YouTube search spider (browser-based)."""

from typing import List, Dict, Any, AsyncGenerator, Optional
import re
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
        result = self.stealth.fetch(url, wait_selector="ytd-video-renderer")
        class FakeResp:
            def __init__(self, r):
                self.text = r.get("html", "")
                self.status_code = 200 if r.get("status") == "success" else 500
                self.url = r.get("url", url)
                self._raw = r
            def text_content(self, sel):
                # simple fallback
                return []
            def css(self, sel):
                return []
        return FakeResp(result)

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        html = response.text or ""
        # Extract titles from common patterns
        titles = re.findall(r'"title":\{"runs":\[\{"text":"(.*?)"\}', html)
        views = re.findall(r'"viewCountText":\{"simpleText":"(.*?)"\}', html)
        published = re.findall(r'"publishedTimeText":\{"simpleText":"(.*?)"\}', html)
        video_ids = re.findall(r'"videoId":"(.*?)"', html)

        count = min(self.max_results, len(titles) or 5)
        for i in range(count):
            title = titles[i] if i < len(titles) else f"Result {i+1}"
            view = views[i] if i < len(views) else None
            pub = published[i] if i < len(published) else None
            vid = video_ids[i] if i < len(video_ids) else None
            url = f"https://www.youtube.com/watch?v={vid}" if vid else response.url
            yield Video(
                source="YouTube",
                title=title,
                url=url,
                video_id=vid,
                views=view,
                published_at=pub,
                category=self.category,
            ).to_dict()

    def start(self, urls: Optional[List[str]] = None):
        search_url = f"https://www.youtube.com/results?search_query={self.query.replace(' ', '+')}"
        return super().start([search_url])
