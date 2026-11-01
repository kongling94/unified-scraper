"""Example of adaptive parsing and Markdown export."""

from unified_scraper import Fetcher
from unified_scraper.utils import to_markdown, quotes_to_markdown

fetcher = Fetcher()
page = fetcher.get("https://quotes.toscrape.com/")

quotes = page.adaptive("quotes", [".quote .text", "span.text"])
print(f"Extracted {len(quotes)} quotes with adaptive selectors")

md = quotes_to_markdown(quotes[:5], title="Top Quotes")
print(md)

# Save to file
with open("quotes.md", "w", encoding="utf-8") as f:
    f.write(md)
print("Saved to quotes.md")
