"""The eBay search results page."""

from pages.base_page import EbayPage
from pages.item_page import ItemPage


class SearchResultsPage(EbayPage):
    """The search results list."""

    def open_first_book(self) -> "ItemPage":
        """Open the first search result in its new tab."""

        search_result = self.page.locator(".srp-results")
        first_book = search_result.locator(".s-card__link").first

        # eBay opens the selected listing in a new tab.
        with self.page.expect_popup() as popup:
            first_book.click()
        item_page = popup.value


        item = ItemPage(item_page)
        return item
