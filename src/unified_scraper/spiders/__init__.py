"""Spider framework inspired by Scrapling."""

from .base import Spider
from .news import (
    TechCrunchSpider,
    TheVergeSpider,
    ArsTechnicaSpider,
    WiredSpider,
    VentureBeatSpider,
    HackerNewsSpider,
    CNBCSpider,
    ReutersSpider,
    YahooFinanceSpider,
    RedditSpider,
)
from .youtube import YouTubeSearchSpider
from .more import CoinDeskSpider, SeekingAlphaSpider, BilibiliHotSpider
from .research import (
    ArxivSpider,
    PapersWithCodeSpider,
    GitHubTrendingSpider,
    CoinTelegraphSpider,
    MITTechReviewSpider,
)

__all__ = [
    "Spider",
    "TechCrunchSpider",
    "TheVergeSpider",
    "ArsTechnicaSpider",
    "WiredSpider",
    "VentureBeatSpider",
    "HackerNewsSpider",
    "CNBCSpider",
    "ReutersSpider",
    "YahooFinanceSpider",
    "RedditSpider",
    "YouTubeSearchSpider",
    "CoinDeskSpider",
    "SeekingAlphaSpider",
    "BilibiliHotSpider",
    "ArxivSpider",
    "PapersWithCodeSpider",
    "GitHubTrendingSpider",
    "CoinTelegraphSpider",
    "MITTechReviewSpider",
]
