"""Account pool manager for X scraping (based on twscrape design)."""

from typing import List, Optional, Dict
import sqlite3
from pathlib import Path

class Account:
    def __init__(self, username: str, auth_token: str, ct0: str, proxy: Optional[str] = None):
        self.username = username
        self.auth_token = auth_token
        self.ct0 = ct0
        self.proxy = proxy
        self.locked = False

class AccountManager:
    """Manages a pool of X accounts with rotation and rate-limit awareness."""

    def __init__(self, db_path: str = "accounts.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    username TEXT PRIMARY KEY,
                    auth_token TEXT,
                    ct0 TEXT,
                    proxy TEXT,
                    locked INTEGER DEFAULT 0
                )
            """)

    def add(self, username: str, auth_token: str, ct0: str, proxy: Optional[str] = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, 0)",
                (username, auth_token, ct0, proxy)
            )

    def get_available(self) -> Optional[Account]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT username, auth_token, ct0, proxy FROM accounts WHERE locked = 0 LIMIT 1"
            ).fetchone()
            if row:
                return Account(*row)
        return None
