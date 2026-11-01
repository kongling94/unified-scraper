"""Smoke tests for XClient (requires real accounts to fully pass)."""

import pytest
import asyncio
from unified_scraper import AccountManager, XClient

@pytest.mark.smoke
def test_x_search_no_accounts():
    mgr = AccountManager(":memory:")
    client = XClient(mgr)
    with pytest.raises(RuntimeError, match="No available accounts"):
        asyncio.run(client.search("AI"))

@pytest.mark.smoke
def test_x_user_tweets_no_accounts():
    mgr = AccountManager(":memory:")
    client = XClient(mgr)
    with pytest.raises(RuntimeError, match="No available accounts"):
        asyncio.run(client.user_tweets("elonmusk"))

@pytest.mark.smoke
def test_proxy_passthrough():
    """Verify proxy is stored and returned on account."""
    mgr = AccountManager(":memory:")
    mgr.add("u1", "token", "ct0", proxy="http://127.0.0.1:8080")
    acc = mgr.get_available()
    assert acc is not None
    assert acc.proxy == "http://127.0.0.1:8080"
