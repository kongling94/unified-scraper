"""Account pool manager for X scraping (based on twscrape design)."""

from typing import List, Optional
import sqlite3
import random
from datetime import datetime

class Account:
    def __init__(self, username: str, auth_token: str, ct0: str, proxy: Optional[str] = None, locked: bool = False):
        self.username = username
        self.auth_token = auth_token
        self.ct0 = ct0
        self.proxy = proxy
        self.locked = locked

    def cookies(self) -> dict:
        return {"auth_token": self.auth_token, "ct0": self.ct0}

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
                    locked INTEGER DEFAULT 0,
                    last_used TEXT
                )
            """)

    def add(self, username: str, auth_token: str, ct0: str, proxy: Optional[str] = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO accounts (username, auth_token, ct0, proxy, locked) VALUES (?, ?, ?, ?, 0)",
                (username, auth_token, ct0, proxy)
            )

    def get_available(self) -> Optional[Account]:
        """Get a random available (unlocked) account."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT username, auth_token, ct0, proxy, locked FROM accounts WHERE locked = 0"
            ).fetchall()
            if not rows:
                return None
            row = random.choice(rows)
            # Update last_used
            conn.execute(
                "UPDATE accounts SET last_used = ? WHERE username = ?",
                (datetime.utcnow().isoformat(), row[0])
            )
            return Account(row[0], row[1], row[2], row[3], bool(row[4]))

    def lock(self, username: str):
        """Mark an account as locked (e.g. after rate limit)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE accounts SET locked = 1 WHERE username = ?", (username,))

    def unlock(self, username: str):
        """Unlock an account."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE accounts SET locked = 0 WHERE username = ?", (username,))

    def list_accounts(self) -> List[Account]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT username, auth_token, ct0, proxy, locked FROM accounts").fetchall()
            return [Account(r[0], r[1], r[2], r[3], bool(r[4])) for r in rows]
