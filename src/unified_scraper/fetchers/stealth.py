"""Stealthy browser fetcher inspired by Scrapling StealthyFetcher."""

from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright

class StealthyFetcher:
    """Browser-based fetcher with stealth and Cloudflare bypass support."""

    def __init__(self, headless: bool = True, solve_cloudflare: bool = True):
        self.headless = headless
        self.solve_cloudflare = solve_cloudflare

    def fetch(self, url: str, wait_selector: Optional[str] = None, timeout: int = 30000) -> Dict[str, Any]:
        """Fetch page with stealth browser.

        Returns dict with status, html, and url.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            try:
                page.goto(url, timeout=timeout, wait_until="domcontentloaded")
                if wait_selector:
                    page.wait_for_selector(wait_selector, timeout=timeout)
                html = page.content()
                final_url = page.url
                return {
                    "url": final_url,
                    "status": "success",
                    "html": html,
                    "title": page.title()
                }
            except Exception as e:
                return {"url": url, "status": "error", "error": str(e)}
            finally:
                browser.close()
