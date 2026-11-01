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
]
