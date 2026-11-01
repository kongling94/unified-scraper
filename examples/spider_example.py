"""Example of using the Spider framework."""

from unified_scraper.spiders import Spider

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    async def parse(self, response):
        quotes = response.text_content(".quote .text")
        for q in quotes:
            yield {"quote": q, "url": response.url}

if __name__ == "__main__":
    spider = QuotesSpider()
    results = spider.start()
    print(f"Collected {len(results)} items")
    for r in results[:3]:
        print(r)
