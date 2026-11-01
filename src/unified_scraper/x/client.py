"""X client wrapping GraphQL endpoints (based on twscrape)."""

from typing import Optional, List, Dict, Any
import httpx
import json
from ..accounts import AccountManager, Account

class XClient:
    """X scraping client with account rotation."""

    # Note: Query IDs change frequently. Update from twscrape when needed.
    SEARCH_QUERY_ID = "nK1dw4oV3k4w5T8tJ2"  # example, replace with latest

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
            "content-type": "application/json",
        }

    async def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search tweets using GraphQL."""
        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts. Add accounts via AccountManager.add()")

        variables = {
            "rawQuery": query,
            "count": min(limit, 20),
            "querySource": "typed_query",
            "product": "Latest",
        }
        features = {
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "tweetypie_unmention_optimization_enabled": True,
            "vibe_api_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False,
        }

        url = f"https://twitter.com/i/api/graphql/{self.SEARCH_QUERY_ID}/SearchTimeline"
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features),
        }

        async with httpx.AsyncClient(headers=self._headers(account), timeout=30.0) as client:
            try:
                # resp = await client.get(url, params=params)
                # data = resp.json()
                # Parse tweets from data here
                return [{
                    "query": query,
                    "account_used": account.username,
                    "status": "graphql_structure_ready",
                    "note": "Update SEARCH_QUERY_ID from latest twscrape and uncomment the real request."
                }]
            except Exception as e:
                self.accounts.lock(account.username)
                raise RuntimeError(f"Request failed with account {account.username}: {e}") from e

    async def user_tweets(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user timeline."""
        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts")
        return [{
            "username": username,
            "account_used": account.username,
            "status": "structure_ready"
        }]
