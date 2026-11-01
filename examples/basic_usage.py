"""Basic usage example for unified-scraper."""

import asyncio
from unified_scraper import Fetcher, AccountManager, XClient

# 1. General web scraping with real parsing
fetcher = Fetcher()
page = fetcher.get("https://quotes.toscrape.com/")
print(f"Status: {page.status_code}")
quotes = page.text_content(".quote .text")
print(f"Found {len(quotes)} quotes:")
for q in quotes[:3]:
    print("-", q)

# 2. Account management with rotation & locking
mgr = AccountManager("example_accounts.db")
# Uncomment to add real accounts
# mgr.add("testuser", "your_auth_token", "your_ct0")
print(f"Available accounts: {len(mgr.list_accounts())}")

# 3. X client (GraphQL ready)
async def demo_x():
    client = XClient(mgr)
    try:
        results = await client.search("AI OR OpenAI", limit=5)
        print("Search results:", results)
    except RuntimeError as e:
        print("X search:", e)

asyncio.run(demo_x())
