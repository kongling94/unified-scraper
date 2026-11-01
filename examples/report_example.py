"""Example of generating crawler reports."""

from unified_scraper import Fetcher
from unified_scraper.utils.report import generate_report

fetcher = Fetcher()
page = fetcher.get("https://quotes.toscrape.com/")
quotes = page.adaptive("quotes", [".quote .text"])

results = [{"quote": q, "source": "quotes.toscrape.com"} for q in quotes[:5]]

# Markdown report
md = generate_report(results, title="Quotes Report", format="markdown")
print(md)
with open("report.md", "w", encoding="utf-8") as f:
    f.write(md)

# JSON report
js = generate_report(results, title="Quotes Report", format="json")
with open("report.json", "w", encoding="utf-8") as f:
    f.write(js)

print("\nSaved report.md and report.json")
