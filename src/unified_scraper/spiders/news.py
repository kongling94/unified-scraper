"""News spiders for tech / AI / finance sites."""

from typing import List, Dict, Any, AsyncGenerator
from .base import Spider
from ..models import Article

class TechCrunchSpider(Spider):
    name = "techcrunch"
    start_urls = ["https://techcrunch.com/"]
    category = "tech"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h2.post-block__title a",
            ".post-block__title a",
            "article h2 a",
        ])
        links = response.css("h2.post-block__title a")
        for i, title in enumerate(titles[:15]):
            href = links[i].attributes.get("href", "") if i < len(links) else ""
            yield Article(
                source="TechCrunch",
                title=title,
                url=href,
                category=self.category,
            ).to_dict()

class TheVergeSpider(Spider):
    name = "theverge"
    start_urls = ["https://www.theverge.com/"]
    category = "tech"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h2 a",
            ".c-entry-box--compact__title a",
            "article h2 a",
        ])
        for title in titles[:15]:
            yield Article(
                source="The Verge",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()

class HackerNewsSpider(Spider):
    name = "hackernews"
    start_urls = ["https://news.ycombinator.com/"]
    category = "tech"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.css(".titleline > a")
        scores = response.text_content(".score")
        for i, node in enumerate(titles[:20]):
            title = node.text(strip=True)
            href = node.attributes.get("href", "")
            score = scores[i] if i < len(scores) else None
            yield Article(
                source="Hacker News",
                title=title,
                url=href,
                category=self.category,
                engagement={"score": score},
            ).to_dict()

class CNBCSpider(Spider):
    name = "cnbc"
    start_urls = ["https://www.cnbc.com/"]
    category = "finance"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            ".Card-title",
            "h2 a",
            ".headline a",
        ])
        for title in titles[:15]:
            yield Article(
                source="CNBC",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()
