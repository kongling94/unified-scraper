"""Integration tests."""

import pytest
from unified_scraper import Fetcher
from unified_scraper.utils import to_markdown

@pytest.mark.integration
def test_quotes_scrape_and_markdown():
    fetcher = Fetcher()
    page = fetcher.get("https://quotes.toscrape.com/")
    assert page.status_code == 200
    quotes = page.adaptive("quotes", [".quote .text", ".quote span.text"])
    assert len(quotes) > 0
    md = to_markdown([{"quote": q} for q in quotes[:2]], title="Sample Quotes")
    assert "# Sample Quotes" in md
    assert quotes[0] in md

def test_adaptive_fallback():
    fetcher = Fetcher()
    page = fetcher.get("https://quotes.toscrape.com/")
    result = page.adaptive("missing", [".does-not-exist", ".also-missing"])
    assert result == []
