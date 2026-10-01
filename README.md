# FIS QA Automation

Pytest checks for adding a book to an eBay guest cart and validating Bitcoin market data from CoinGecko.

## Setup

Requires Python and uv

```bash
uv sync
uv run playwright install chromium
```

## Run

```bash
uv run pytest                              # Run all checks
uv run pytest -m api                       # CoinGecko API checks
uv run pytest -m ui --browser chromium     # eBay UI check
uv run pytest --html=report.html --self-contained-html      # with HTML report
```

The UI test accepts `--search-term "book"`. Each run writes a JUnit XML report to `test_output/results.xml`. On UI failures, Playwright traces and screenshots are saved in `test_output/`; the failure report also lists each open page URL and a full-page screenshot path, including the item popup.

## Reports
You can find reports in `report.html`


## Assumptions made: 
The project makes these assumptions:
### eBay UI Test

- The test runs against the US eBay website: https://www.ebay.com/.
- By default, it searches for **“book”**. A different search term can be provided using `--search-term`.
- The test assumes that clicking the first product opens the listing in a new browser tab.
- Each test starts with a fresh browser session, so the user is treated as a guest and the cart is expected to be empty. After adding the product, the test verifies that the cart count increases by one.
- After clicking **“Add to cart”**, the test expects the **“Added to cart”** confirmation dialog to appear.
- eBay may occasionally show an error page. The test tries to recover from this once before failing.
- The test only adds a product to the cart. It does not proceed with checkout or make a purchase.

### CoinGecko API Test

- The API tests use CoinGecko's public Bitcoin endpoint and expect a successful `200` response.
- The test verifies that the current price, market cap, and total volume are available for **USD, GBP, and EUR** and that their values are greater than zero.
- The 24-hour price change can be positive, negative, or zero, but it must contain a valid numeric value.
- The response should contain at least one valid homepage URL starting with `http` or `https`.
- The Bitcoin data is fetched once and reused across the tests in the module to avoid making unnecessary API calls.



## Design approach used:

### eBay cart test:
This test uses Playwright to open eBay, search for a book, open a listing, and add it to the cart. It then checks that the item was added and the cart count went up.
The test uses the Page Object Model to keep things organized. HomePage, SearchResultsPage, and ItemPage each handle the actions for one part of the site. Shared actions, like checking the cart count, are handled by EbayPage. This keeps the test steps clear and makes the page interactions easier to maintain.

### CoinGecko API test:
This test calls CoinGecko’s Bitcoin endpoint and checks that it returns price, market cap, and trading volume for USD, GBP, and EUR. It also checks that the 24-hour price change is a valid number and that the response includes a homepage URL.
It uses Playwright to make API calls and  pytest to run the checks and share the API response across them.

If a test fails, Playwright tracing is enabled for the browser test, and the trace and failure screenshots are saved in the test_output/ folder to help investigate what went wrong. CoinGecko failures report request errors, HTTP status and a short response excerpt, or malformed JSON and missing response fields.
