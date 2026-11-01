"""Generate an HTML card-style research report."""

from unified_scraper.spiders import TechCrunchSpider, HackerNewsSpider, ArxivSpider
from unified_scraper.utils import generate_report

def collect():
    items = []
    for Spider in (TechCrunchSpider, HackerNewsSpider, ArxivSpider):
        try:
            items.extend(Spider().start())
        except Exception as e:
            print(Spider.name, e)
    return items

if __name__ == "__main__":
    results = collect()
    html = generate_report(
        results,
        title="科技 / AI 每日快照",
        format="html",
        dedupe=True,
    )
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved report.html ({len(results)} items before final dedupe)")
    print("Open report.html in a browser to view the card layout.")
