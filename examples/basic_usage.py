"""Basic usage example for unified-scraper."""

import asyncio
from unified_scraper import Fetcher, StealthyFetcher, AccountManager, XClient

# 1. General web scraping with real parsing
fetcher = Fetcher()
page = fetcher.get("https://quotes.toscrape.com/")
print(f"HTTP Status: {page.status_code}")
quotes = page.text_content(".quote .text")
print(f"Found {len(quotes)} quotes:")
for q in quotes[:2]:
    print("-", q)

# 2. Stealthy browser fetcher
stealth = StealthyFetcher(headless=True)
result = stealth.fetch("https://quotes.toscrape.com/", wait_selector=".quote")
print(f"Stealth status: {result['status']}, title: {result.get('title', 'N/A')}")

# 3. Account management with rotation & locking
mgr = AccountManager("example_accounts.db")
print(f"Available accounts: {len(mgr.list_accounts())}")

# 4. X client (GraphQL structure ready)
async def demo_x():
    client = XClient(mgr)
    try:
        results = await client.search("AI OR OpenAI", limit=5)
        print("Search results:", results)
    except RuntimeError as e:
        print("X search:", e)

asyncio.run(demo_x())
