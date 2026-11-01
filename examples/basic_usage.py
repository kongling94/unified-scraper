"""Basic usage example for unified-scraper."""

from unified_scraper import Fetcher, AccountManager, XClient

# General web scraping
fetcher = Fetcher()
page = fetcher.get("https://quotes.toscrape.com/")
print(page.status_code)

# X account management
mgr = AccountManager()
# mgr.add("user1", "auth_token_here", "ct0_here")

# X client
# client = XClient(mgr)
# results = await client.search("AI OR OpenAI")
