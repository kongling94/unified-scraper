"""Unified data models for finance / tech / AI research scraping."""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime

@dataclass
class Article:
    source: str
    title: str
    url: str
    content: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    category: str = "general"  # finance / tech / ai
    engagement: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Video:
    source: str
    title: str
    url: str
    video_id: Optional[str] = None
    description: Optional[str] = None
    channel: Optional[str] = None
    published_at: Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    category: str = "video"
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
