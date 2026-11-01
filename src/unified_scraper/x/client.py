"""X client wrapping GraphQL endpoints (based on twscrape)."""

from typing import Optional, List, Dict, Any
import httpx
from ..accounts import AccountManager, Account

class XClient:
    """X scraping client with account rotation."""

    GRAPHQL_URL = "https://twitter.com/i/api/graphql"

    def __init__(self, account_manager: AccountManager):
        self.accounts = account_manager

    def _headers(self, account: Account) -> Dict[str, str]:
        return {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "x-csrf-token": account.ct0,
            "cookie": f"auth_token={account.auth_token}; ct0={account.ct0}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en",
        }

    async def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search tweets using GraphQL (placeholder for full implementation)."""
        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts. Add accounts via AccountManager.add()")

        # Example endpoint structure (actual query ID changes frequently)
        # In production, copy latest from twscrape
        url = f"{self.GRAPHQL_URL}/SearchTimeline"
        params = {
            "variables": {
                "rawQuery": query,
                "count": min(limit, 20),
                "querySource": "typed_query",
                "product": "Latest",
            },
            "features": {},  # fill with current features from twscrape
        }

        async with httpx.AsyncClient(headers=self._headers(account)) as client:
            try:
                # resp = await client.get(url, params=params)
                # For now return structured placeholder that shows account was used
                return [{
                    "query": query,
                    "account_used": account.username,
                    "status": "ready_for_graphql_implementation",
                    "note": "Replace with real GraphQL call. See twscrape source for query IDs."
                }]
            except Exception as e:
                self.accounts.lock(account.username)
                raise RuntimeError(f"Request failed with account {account.username}: {e}") from e

    async def user_tweets(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user timeline (placeholder)."""
        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts")
        return [{
            "username": username,
            "account_used": account.username,
            "status": "ready_for_implementation"
        }]
