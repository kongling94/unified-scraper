"""General web fetchers inspired by Scrapling."""

from .http import Fetcher
from .stealth import StealthyFetcher

__all__ = ["Fetcher", "StealthyFetcher"]
