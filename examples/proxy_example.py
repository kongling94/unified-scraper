"""Example of adding accounts with proxies."""

from unified_scraper import AccountManager, XClient
import asyncio

mgr = AccountManager("proxied_accounts.db")

# Add accounts with optional proxies
mgr.add("user1", "auth_token_1", "ct0_1", proxy="http://proxy1:8080")
mgr.add("user2", "auth_token_2", "ct0_2")  # no proxy

print("Accounts:")
for a in mgr.list_accounts():
    print(f"  {a.username} proxy={a.proxy} locked={a.locked}")

async def demo():
    client = XClient(mgr)
    try:
        results = await client.search("AI", limit=3)
        print("Search results:", results)
    except Exception as e:
        print("Expected if tokens are fake:", e)

asyncio.run(demo())
