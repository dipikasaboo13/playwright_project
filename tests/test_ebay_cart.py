"""A guest searches for a book and adds the first result to the cart."""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage


@pytest.mark.ui
def test_first_book_can_be_added_to_cart(
    ebay_home_page: HomePage, page: Page, browser_name: str, search_term: str, pause_at_end: None
) -> None:
    """Verify that a guest can add the first search result to the cart."""
    # The fixture opens eBay in a fresh browser context, so this is a guest cart.
    before = ebay_home_page.cart_count()
    results_page = ebay_home_page.search_for(search_term)
    item_page = results_page.open_first_book()
    item_page.add_to_cart()

    # The page object supplies the locator; the test states what must be true.
    expect(item_page.cart_with_count(before + 1)).to_be_visible()

    print("Item has been successfully added to the cart.")
