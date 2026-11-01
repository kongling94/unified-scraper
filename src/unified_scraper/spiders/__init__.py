"""Spider framework inspired by Scrapling."""

from .base import Spider
from .news import TechCrunchSpider, TheVergeSpider, HackerNewsSpider, CNBCSpider
from .youtube import YouTubeSearchSpider

__all__ = [
    "Spider",
    "TechCrunchSpider",
    "TheVergeSpider",
    "HackerNewsSpider",
    "CNBCSpider",
    "YouTubeSearchSpider",
]
