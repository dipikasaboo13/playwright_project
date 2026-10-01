"""An eBay item page and its Add to cart action."""


import pytest
from playwright.sync_api import expect

from pages.base_page import EbayPage


class ItemPage(EbayPage):
    """A single listing and its Add to cart action."""

    def add_to_cart(self) -> None:
        """Add the listing to the cart and dismiss the confirmation dialog."""
        add_button = self.page.get_by_text("Add to cart", exact=True).first
        add_button.click()

        # Confirm the cart action before closing the dialog.
        added_dialog = self.page.get_by_role("dialog", name="Added to cart")
        expect(added_dialog).to_be_visible()
        added_dialog.get_by_role("button", name="Close dialog").click()
