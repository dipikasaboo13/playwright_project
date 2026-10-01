"""Shared eBay page behavior: error recovery and cart-count locators."""

import re

import pytest
from playwright.sync_api import Locator, Page, Response, expect


EBAY_URL = "https://www.ebay.com/"


class EbayPage:
    """Behavior shared by eBay's home, results, and item pages."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def recover_from_error_page(
        self, stage: str, response: Response | None = None, retry_url: str | None = None
    ) -> bool:
        """Follow eBay's error-page link once; return True if recovery happened."""
        status = response.status if response else None

        error_message = self.page.get_by_text("Something went wrong on our end")
        error_page = self.page.title() == "Error Page | eBay" or error_message.is_visible()
        if status != 403 and not error_page:
            if status is not None and status != 200:
                pytest.fail(f"eBay {stage} returned HTTP {status}.")
            return False

        home_link = self.page.get_by_role("link", name=re.compile(r"go to homepage", re.I))
        home_link.click()

        expect(self.page.get_by_role("link", name=re.compile(r"go to homepage", re.I))).not_to_be_visible()
        return True

    def cart_with_count(self, count: int) -> Locator:
        """Return the header cart link with a particular item count."""

        return self.page.get_by_role(
            "link", name=re.compile(f"Your shopping cart contains {count} items?")
        )

    def cart_count(self) -> int:
        """Read the count from eBay's header cart badge."""
        badge = self.page.locator(".gh-cart .gh-badge")
        if badge.count() == 0:
            return 0
        else:
            return int(badge.inner_text())
