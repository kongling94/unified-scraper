"""Example of user ID resolution and additional endpoints."""

import asyncio
from unified_scraper import AccountManager, XClient

async def main():
    mgr = AccountManager("example_accounts.db")
    # mgr.add("your_user", "auth_token", "ct0")
    client = XClient(mgr)

    # Resolve user ID
    try:
        user_id = await client.resolve_user_id("elonmusk")
        print("Resolved user ID:", user_id)
    except Exception as e:
        print("Resolve failed:", e)

    # User timeline (now uses resolved ID)
    try:
        tweets = await client.user_tweets("elonmusk", limit=3)
        print("Timeline:", tweets[:1])
    except Exception as e:
        print("Timeline failed:", e)

    # Structure-ready endpoints
    print("Replies stub:", await client.tweet_replies("1234567890"))
    print("Likes stub:", await client.user_likes("elonmusk"))

if __name__ == "__main__":
    asyncio.run(main())
