"""Full research pipeline: tech, AI, finance, community, video."""

from unified_scraper.spiders import (
    TechCrunchSpider,
    TheVergeSpider,
    ArsTechnicaSpider,
    WiredSpider,
    VentureBeatSpider,
    HackerNewsSpider,
    CNBCSpider,
    ReutersSpider,
    YahooFinanceSpider,
    RedditSpider,
    YouTubeSearchSpider,
)
from unified_scraper.utils import generate_report

def collect_all():
    spiders = [
        TechCrunchSpider(),
        TheVergeSpider(),
        ArsTechnicaSpider(),
        WiredSpider(),
        VentureBeatSpider(),
        HackerNewsSpider(),
        CNBCSpider(),
        ReutersSpider(),
        YahooFinanceSpider(),
        RedditSpider("MachineLearning"),
        RedditSpider("artificial"),
        YouTubeSearchSpider(query="AI news", max_results=5),
    ]
    all_items = []
    for spider in spiders:
        try:
            results = spider.start()
            print(f"{spider.name}: {len(results)} items")
            all_items.extend(results)
        except Exception as e:
            print(f"{spider.name} failed: {e}")
    return all_items

if __name__ == "__main__":
    items = collect_all()
    report = generate_report(items, title="Finance / Tech / AI Research Snapshot", format="markdown")
    with open("full_research_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nTotal collected: {len(items)} items. Saved to full_research_report.md")
