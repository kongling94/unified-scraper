"""Research-oriented spiders: arXiv, Papers with Code, GitHub Trending, etc."""

from typing import Dict, Any, AsyncGenerator
from .base import Spider
from ..models import Article

class ArxivSpider(Spider):
    name = "arxiv"
    start_urls = ["https://arxiv.org/list/cs.AI/recent", "https://arxiv.org/list/cs.LG/recent"]
    category = "ai"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            ".list-title",
            "dt + dd .list-title",
            "h3",
        ])
        for title in titles[:20]:
            clean = title.replace("Title:", "").strip()
            yield Article(
                source="arXiv",
                title=clean,
                url=response.url,
                category=self.category,
            ).to_dict()

class PapersWithCodeSpider(Spider):
    name = "paperswithcode"
    start_urls = ["https://paperswithcode.com/"]
    category = "ai"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h1 a",
            ".paper-title",
            "article h2",
        ])
        for title in titles[:15]:
            yield Article(
                source="Papers with Code",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()

class GitHubTrendingSpider(Spider):
    name = "github_trending"
    start_urls = ["https://github.com/trending"]
    category = "tech"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h2 a",
            ".h3 a",
            "article h2",
        ])
        for title in titles[:20]:
            yield Article(
                source="GitHub Trending",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()

class CoinTelegraphSpider(Spider):
    name = "cointelegraph"
    start_urls = ["https://cointelegraph.com/"]
    category = "finance"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h2 a",
            ".post-card-inline__title",
            "article h2",
        ])
        for title in titles[:15]:
            yield Article(
                source="CoinTelegraph",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()

class MITTechReviewSpider(Spider):
    name = "mit_tech_review"
    start_urls = ["https://www.technologyreview.com/"]
    category = "ai"

    async def parse(self, response) -> AsyncGenerator[Dict[str, Any], None]:
        titles = response.adaptive("titles", [
            "h3 a",
            ".teaserItem__title",
            "article h2",
        ])
        for title in titles[:15]:
            yield Article(
                source="MIT Technology Review",
                title=title,
                url=response.url,
                category=self.category,
            ).to_dict()
