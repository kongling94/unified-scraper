"""Example of generating a deduplicated research report."""

from unified_scraper.spiders import (
    TechCrunchSpider,
    ArxivSpider,
    GitHubTrendingSpider,
    CoinTelegraphSpider,
    MITTechReviewSpider,
)
from unified_scraper.utils import generate_report

def collect():
    spiders = [
        TechCrunchSpider(),
        ArxivSpider(),
        GitHubTrendingSpider(),
        CoinTelegraphSpider(),
        MITTechReviewSpider(),
    ]
    items = []
    for s in spiders:
        try:
            items.extend(s.start())
        except Exception as e:
            print(s.name, e)
    return items

if __name__ == "__main__":
    raw = collect()
    print(f"Raw items: {len(raw)}")

    # With deduplication (default)
    report = generate_report(raw, title="Deduped Research Snapshot", format="markdown", dedupe=True)
    with open("deduped_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("Saved deduped_report.md")
