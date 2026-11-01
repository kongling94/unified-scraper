"""Example of fetching a user timeline."""

import asyncio
from unified_scraper import AccountManager, XClient

async def main():
    mgr = AccountManager("example_accounts.db")
    # mgr.add("your_user", "auth_token", "ct0")
    client = XClient(mgr)
    try:
        tweets = await client.user_tweets("elonmusk", limit=5)
        print(f"Got {len(tweets)} items")
        for t in tweets[:2]:
            print(t)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
