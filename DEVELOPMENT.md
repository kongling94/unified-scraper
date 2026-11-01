# Development Plan & Acceptance Criteria

## Phase 1: Foundation (Day 1-3)
- [x] Repo structure
- [x] AccountManager basic + rotation & locking
- [x] HTTP Fetcher real implementation + CSS parsing
- [x] StealthyFetcher Playwright integration

## Phase 2: X Core (Day 4-7)
- [x] XClient real GraphQL search request + basic parsing
- [x] Account rotation on rate limit (lock mechanism)
- [x] User timeline GraphQL implementation

## Phase 3: General Scraping (Day 8-10)
- [x] Adaptive element tracking
- [x] Spider concurrent framework + middleware + error handling
- [x] Markdown export

## Phase 4: Testing (Day 11-13)
- [x] Unit tests for AccountManager
- [x] Integration test for news sites + adaptive + markdown
- [ ] X search smoke test

## Deployment
- [x] Dockerfile
- [x] docker-compose.yml
- [x] Full management API (search + account CRUD)

## Acceptance Criteria
1. Can scrape quotes.toscrape.com and extract text ✅
2. Can add X accounts and rotate them ✅
3. XClient.search returns structured results (or clear error) ✅
4. XClient.user_tweets available ✅
5. Adaptive selectors + Markdown export ✅
6. Supports Docker Compose deployment and Harness management ✅
