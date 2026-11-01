"""Additional spiders: CoinDesk, Seeking Alpha, Bilibili."""

from typing import Dict, Any, AsyncGenerator
from .base import Spider
from ..models import Article, Video

class CoinDeskSpider(Spider):
    name = "coindesk"
    start_urls = ["https://www.coindesk.com/"]
    category = "finance"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h2 a",
            ".card-title a",
            "article h2",
        ])
        for title in titles[:15]:
            yield Article(
                source="CoinDesk",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()

class SeekingAlphaSpider(Spider):
    name = "seekingalpha"
    start_urls = ["https://seekingalpha.com/"]
    category = "finance"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h3 a",
            ".title a",
            "article h3",
        ])
        for title in titles[:15]:
            yield Article(
                source="Seeking Alpha",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()

class BilibiliHotSpider(Spider):
    name = "bilibili_hot"
    start_urls = ["https://www.bilibili.com/v/popular/all"]
    category = "video"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            ".video-name",
            "h3",
            ".title",
        ])
        for title in titles[:15]:
            yield Video(
                source="Bilibili",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()
