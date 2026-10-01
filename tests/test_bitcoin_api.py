"""Contract checks for CoinGecko's public Bitcoin endpoint."""

import math
from urllib.parse import urlparse

import pytest
from playwright.sync_api import Error, Playwright

from test_data.api_data import BASE_URL, COIN_URL, CURRENCIES
from utils.assertions import assert_positive_number


@pytest.fixture(scope="module")
def bitcoin(playwright: Playwright):
    """Fetch Bitcoin data once for all API contract checks in this module."""
    request = playwright.request.new_context(base_url= BASE_URL)

    try:
        response = request.get(COIN_URL, timeout=60000)
    except Error as exc:
        pytest.fail(f"CoinGecko request to {COIN_URL} failed: {exc}")

    # Validate the request response
    if response.status != 200:
        pytest.fail(
            f"CoinGecko {COIN_URL} returned HTTP {response.status}: "
            f"{response.text()[:500]}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        pytest.fail(f"CoinGecko {COIN_URL} returned invalid JSON: {exc}")
        
    assert isinstance(data, dict), "Expected a JSON object"
    assert data.get("id") == "bitcoin", "Expected CoinGecko response id to be bitcoin"
    assert isinstance(data.get("market_data"), dict), "Expected market_data to be an object"
    assert isinstance(data.get("links"), dict), "Expected links to be an object"
    return data



@pytest.mark.api
@pytest.mark.parametrize("currency", CURRENCIES)
def test_current_price_in_requested_currency(bitcoin: dict, currency: str) -> None:
    """Check that each requested currency has a positive current price."""
    price = bitcoin["market_data"]["current_price"].get(currency)
    assert_positive_number(price, f"current_price.{currency}")


@pytest.mark.api
@pytest.mark.parametrize("field", ("market_cap", "total_volume"))
@pytest.mark.parametrize("currency", CURRENCIES)
def test_market_value_is_available(bitcoin: dict, field: str, currency: str) -> None:
    """Check that market cap and volume exist in each requested currency."""
    value = bitcoin["market_data"][field].get(currency)
    assert_positive_number(value, f"{field}.{currency}")


@pytest.mark.api
def test_24_hour_price_change_percentage(bitcoin: dict) -> None:
    """Check that the daily price change is a finite number."""
    change = bitcoin["market_data"].get("price_change_percentage_24h")
    assert type(change) in (int, float), f"24-hour change should be numeric, got {change!r}"
    assert math.isfinite(change), "24-hour change should be finite"


@pytest.mark.api
def test_homepage_url_is_present(bitcoin: dict) -> None:
    """Check that CoinGecko provides at least one usable homepage URL."""
    homepages = bitcoin["links"].get("homepage")
    assert isinstance(homepages, list), "Expected links.homepage to be a list"
    valid_urls = []
    for url in homepages:
        if isinstance(url, str):
            parsed_url = urlparse(url)
            if parsed_url.scheme in ("http", "https") and parsed_url.netloc:
                valid_urls.append(url)

    assert len(valid_urls) > 0, "Expected at least one non-empty homepage URL"
