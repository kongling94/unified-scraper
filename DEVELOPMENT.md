# Development Plan & Acceptance Criteria

## Phase 1: Foundation (Day 1-3)
- [x] Repo structure
- [x] AccountManager basic
- [ ] HTTP Fetcher real implementation
- [ ] StealthyFetcher Playwright integration

## Phase 2: X Core (Day 4-7)
- [ ] XClient GraphQL search
- [ ] Account rotation on rate limit
- [ ] User timeline

## Phase 3: General Scraping (Day 8-10)
- [ ] Adaptive element tracking
- [ ] Full Spider framework
- [ ] Markdown export

## Phase 4: Testing (Day 11-13)
- [ ] Unit tests for AccountManager
- [ ] Integration test for news sites
- [ ] X search smoke test

## Acceptance Criteria
1. Can scrape quotes.toscrape.com and extract text
2. Can add X accounts and rotate them
3. XClient.search returns structured results (or clear error if no accounts)
4. All public APIs have type hints and docstrings
5. README covers install + 2 working examples
