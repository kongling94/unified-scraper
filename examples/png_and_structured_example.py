"""Generate structured HTML and PNG reports."""

from unified_scraper.spiders import TechCrunchSpider, HackerNewsSpider, ArxivSpider, CoinTelegraphSpider
from unified_scraper.utils import generate_report

def collect():
    items = []
    for Spider in (TechCrunchSpider, HackerNewsSpider, ArxivSpider, CoinTelegraphSpider):
        try:
            items.extend(Spider().start())
        except Exception as e:
            print(getattr(Spider, "name", Spider), e)
    return items

if __name__ == "__main__":
    results = collect()
    print(f"Collected {len(results)} items")

    # Structured HTML
    html = generate_report(
        results,
        title="金融 / 科技 / AI 每日快照",
        format="html",
        dedupe=True,
        structured=True,
    )
    with open("structured_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved structured_report.html")

    # PNG long image
    try:
        png_bytes = generate_report(
            results,
            title="每日快照",
            format="png",
            dedupe=True,
        )
        with open("report.png", "wb") as f:
            f.write(png_bytes)
        print("Saved report.png")
    except RuntimeError as e:
        print("PNG skipped:", e)
        print("Install with: pip install pillow")
