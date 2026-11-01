"""Example of custom sections and auto-save."""

from unified_scraper.spiders import TechCrunchSpider, ArxivSpider, CoinTelegraphSpider, YouTubeSearchSpider
from unified_scraper.utils import generate_report

def collect():
    items = []
    for Spider in (TechCrunchSpider, ArxivSpider, CoinTelegraphSpider):
        try:
            items.extend(Spider().start())
        except Exception as e:
            print(getattr(Spider, "name", ""), e)
    return items

if __name__ == "__main__":
    results = collect()
    print(f"Collected {len(results)} items")

    custom = {
        "AI 与技术热点": ["ai", "arxiv", "techcrunch", "github"],
        "金融与加密": ["coin", "finance", "reuters"],
        "视频趋势": ["youtube", "bilibili"],
    }

    result = generate_report(
        results,
        title="自定义章节快照",
        format="html",
        dedupe=True,
        custom_sections=custom,
        auto_save=True,
        output_dir="reports",
    )

    print("Saved to:", result["saved_path"])
    print("Open the HTML file in a browser.")
