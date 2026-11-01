"""Example research data collection pipeline."""

from unified_scraper.spiders.news import TechCrunchSpider, TheVergeSpider, HackerNewsSpider, CNBCSpider
from unified_scraper.utils import generate_report

def collect_news():
    spiders = [
        TechCrunchSpider(),
        TheVergeSpider(),
        HackerNewsSpider(),
        CNBCSpider(),
    ]
    all_articles = []
    for spider in spiders:
        try:
            results = spider.start()
            print(f"{spider.name}: {len(results)} items")
            all_articles.extend(results)
        except Exception as e:
            print(f"{spider.name} failed: {e}")
    return all_articles

if __name__ == "__main__":
    articles = collect_news()
    report = generate_report(articles, title="Tech & Finance News Snapshot", format="markdown")
    with open("research_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nCollected {len(articles)} articles. Saved to research_report.md")
