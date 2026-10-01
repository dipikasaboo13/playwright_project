"""Fixtures shared by browser tests in this folder."""

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage


@pytest.fixture
def ebay_home_page(page: Page) -> HomePage:
    """Open eBay using pytest-playwright's fresh ``page`` fixture."""
    home_page = HomePage(page)
    home_page.open()
    return home_page


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add options for selecting a search term and inspecting the result."""
    parser.addoption(
        "--search-term",
        action="store",
        default="book",
        help="eBay search term used by the cart UI test (default: book)",
    )
    parser.addoption(
        "--pause-at-end",
        action="store_true",
        help="keep the headed browser open after the UI test for manual inspection",
    )


@pytest.fixture
def search_term(request: pytest.FixtureRequest) -> str:
    """Return the eBay search term provided on the pytest command line."""
    return request.config.getoption("--search-term")


@pytest.fixture
def pause_at_end(request: pytest.FixtureRequest, page: Page) -> None:
    """Pause after the test when requested, before pytest closes the browser."""
    if request.config.getoption("--pause-at-end"):
        if not request.config.getoption("--headed"):
            pytest.fail("--pause-at-end requires --headed so you can inspect the page.")
        page.pause()
