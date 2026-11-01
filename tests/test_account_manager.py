"""Unit tests for AccountManager."""

import os
import tempfile
from unified_scraper.accounts import AccountManager

def test_add_and_list():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test.db")
        mgr = AccountManager(db)
        mgr.add("user1", "token1", "ct01")
        mgr.add("user2", "token2", "ct02", proxy="http://proxy")
        accounts = mgr.list_accounts()
        assert len(accounts) == 2
        assert accounts[0].username == "user1"
        assert accounts[1].proxy == "http://proxy"

def test_lock_unlock():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test.db")
        mgr = AccountManager(db)
        mgr.add("user1", "token1", "ct01")
        mgr.lock("user1")
        assert mgr.get_available() is None
        mgr.unlock("user1")
        acc = mgr.get_available()
        assert acc is not None
        assert acc.username == "user1"
