"""X client wrapping GraphQL endpoints (based on twscrape)."""

from typing import Optional, List, Dict, Any
import httpx
import json
from ..accounts import AccountManager, Account

class XClient:
    """X scraping client with account rotation and proxy support."""

    # Note: Query IDs change frequently. Update from twscrape when needed.
    SEARCH_QUERY_ID = "nK1dw4oV3k4w5T8tJ2"
    USER_TWEETS_QUERY_ID = "V7H0Ap3_Hh2FyS75OCDO3Q"
    USER_BY_SCREEN_NAME_QUERY_ID = "G3KGOASz96M-Qu0nwmGXNg"
    TWEET_DETAIL_QUERY_ID = "nBS-WpgA6ZG0CyNHD517JQ"  # example
    LIKES_QUERY_ID = "eSSNB9Q2Q7m8m8m8m8m8m8"  # example, replace

    def __init__(self, account_manager: AccountManager):
        self.accounts = account_manager
        self._user_id_cache: Dict[str, str] = {}

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

    def _client(self, account: Account) -> httpx.AsyncClient:
        proxies = account.proxy if account.proxy else None
        return httpx.AsyncClient(
            headers=self._headers(account),
            timeout=30.0,
            proxies=proxies,
            follow_redirects=True,
        )

    def _parse_tweets(self, data: dict, account: Account) -> List[Dict[str, Any]]:
        tweets = []
        try:
            candidates = [
                data.get("data", {}).get("search_by_raw_query", {}).get("search_timeline", {}).get("timeline", {}),
                data.get("data", {}).get("user", {}).get("result", {}).get("timeline", {}),
                data.get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get("timeline", {}),
                data.get("data", {}).get("threaded_conversation_with_injections_v2", {}).get("instructions", []),
            ]
            # Handle both timeline dict and raw instructions list
            timeline = {}
            instructions = []
            for c in candidates:
                if isinstance(c, dict) and c.get("instructions"):
                    timeline = c
                    instructions = c.get("instructions", [])
                    break
                elif isinstance(c, list):
                    instructions = c
                    break

            for inst in instructions:
                entries = inst.get("entries") or inst.get("moduleItems") or []
                for entry in entries:
                    content = entry.get("content", {}) or entry.get("item", {}).get("itemContent", {})
                    item = content.get("itemContent", {}) or content
                    tweet_results = item.get("tweet_results", {}).get("result", {})
                    if not tweet_results:
                        continue
                    if "tweet" in tweet_results:
                        tweet_results = tweet_results["tweet"]
                    legacy = tweet_results.get("legacy", {})
                    user_result = (
                        tweet_results.get("core", {}).get("user_results", {}).get("result", {})
                        or tweet_results.get("user", {}).get("result", {})
                    )
                    user_legacy = user_result.get("legacy", {}) if user_result else {}
                    tweets.append({
                        "id": legacy.get("id_str"),
                        "text": legacy.get("full_text") or legacy.get("text"),
                        "user": user_legacy.get("screen_name"),
                        "user_name": user_legacy.get("name"),
                        "created_at": legacy.get("created_at"),
                        "favorite_count": legacy.get("favorite_count"),
                        "retweet_count": legacy.get("retweet_count"),
                        "reply_count": legacy.get("reply_count"),
                        "quote_count": legacy.get("quote_count"),
                        "lang": legacy.get("lang"),
                    })
        except Exception:
            pass
        return tweets or [{"status": "ok", "raw_keys": list(data.keys()), "account": account.username}]

    async def resolve_user_id(self, username: str) -> Optional[str]:
        """Resolve screen name to user ID."""
        if username in self._user_id_cache:
            return self._user_id_cache[username]

        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts")

        variables = {"screen_name": username}
        features = {"hidden_profile_likes_enabled": True, "responsive_web_graphql_exclude_directive_enabled": True}
        url = f"https://twitter.com/i/api/graphql/{self.USER_BY_SCREEN_NAME_QUERY_ID}/UserByScreenName"
        params = {"variables": json.dumps(variables), "features": json.dumps(features)}

        async with self._client(account) as client:
            try:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    user_id = data.get("data", {}).get("user", {}).get("result", {}).get("rest_id")
                    if user_id:
                        self._user_id_cache[username] = user_id
                        return user_id
                self.accounts.lock(account.username)
            except Exception:
                self.accounts.lock(account.username)
        return None

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
        params = {"variables": json.dumps(variables), "features": json.dumps(features)}

        async with self._client(account) as client:
            try:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    return self._parse_tweets(resp.json(), account)
                else:
                    self.accounts.lock(account.username)
                    return [{"status": "http_error", "code": resp.status_code, "account": account.username, "text": resp.text[:200]}]
            except Exception as e:
                self.accounts.lock(account.username)
                raise RuntimeError(f"Request failed with account {account.username}: {e}") from e

    async def user_tweets(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user timeline using GraphQL."""
        user_id = await self.resolve_user_id(username)
        if not user_id:
            return [{"status": "user_not_found", "username": username}]

        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts")

        variables = {
            "userId": user_id,
            "count": min(limit, 20),
            "includePromotedContent": False,
            "withVoice": True,
            "withV2Timeline": True,
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

        url = f"https://twitter.com/i/api/graphql/{self.USER_TWEETS_QUERY_ID}/UserTweets"
        params = {"variables": json.dumps(variables), "features": json.dumps(features)}

        async with self._client(account) as client:
            try:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    tweets = self._parse_tweets(resp.json(), account)
                    for t in tweets:
                        t["requested_user"] = username
                        t["user_id"] = user_id
                    return tweets
                else:
                    self.accounts.lock(account.username)
                    return [{"status": "http_error", "code": resp.status_code, "account": account.username, "user": username, "text": resp.text[:200]}]
            except Exception as e:
                self.accounts.lock(account.username)
                raise RuntimeError(f"User timeline failed with account {account.username}: {e}") from e

    async def tweet_replies(self, tweet_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get replies to a tweet using GraphQL."""
        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts")

        variables = {
            "focalTweetId": tweet_id,
            "with_rux_injections": False,
            "includePromotedContent": False,
            "withCommunity": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withBirdwatchNotes": True,
            "withVoice": True,
            "withV2Timeline": True,
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

        url = f"https://twitter.com/i/api/graphql/{self.TWEET_DETAIL_QUERY_ID}/TweetDetail"
        params = {"variables": json.dumps(variables), "features": json.dumps(features)}

        async with self._client(account) as client:
            try:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    tweets = self._parse_tweets(resp.json(), account)
                    for t in tweets:
                        t["focal_tweet_id"] = tweet_id
                    return tweets
                else:
                    self.accounts.lock(account.username)
                    return [{"status": "http_error", "code": resp.status_code, "account": account.username, "tweet_id": tweet_id, "text": resp.text[:200]}]
            except Exception as e:
                self.accounts.lock(account.username)
                raise RuntimeError(f"Replies failed with account {account.username}: {e}") from e

    async def user_likes(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get tweets liked by a user using GraphQL."""
        user_id = await self.resolve_user_id(username)
        if not user_id:
            return [{"status": "user_not_found", "username": username}]

        account = self.accounts.get_available()
        if not account:
            raise RuntimeError("No available accounts")

        variables = {
            "userId": user_id,
            "count": min(limit, 20),
            "includePromotedContent": False,
            "withVoice": True,
            "withV2Timeline": True,
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

        url = f"https://twitter.com/i/api/graphql/{self.LIKES_QUERY_ID}/Likes"
        params = {"variables": json.dumps(variables), "features": json.dumps(features)}

        async with self._client(account) as client:
            try:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    tweets = self._parse_tweets(resp.json(), account)
                    for t in tweets:
                        t["liked_by"] = username
                    return tweets
                else:
                    self.accounts.lock(account.username)
                    return [{"status": "http_error", "code": resp.status_code, "account": account.username, "user": username, "text": resp.text[:200]}]
            except Exception as e:
                self.accounts.lock(account.username)
                raise RuntimeError(f"Likes failed with account {account.username}: {e}") from e
