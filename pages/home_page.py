"""The eBay homepage and its search box."""

import pytest
from pages.base_page import EBAY_URL, EbayPage
from pages.search_results_page import SearchResultsPage


class HomePage(EbayPage):
    """The eBay homepage and its search box."""

    def open(self) -> None:
        """Load the eBay homepage and recover from a transient error page."""
        response = self.page.goto(EBAY_URL, wait_until="domcontentloaded")
        if response is None:
            pytest.fail("eBay home page returned no response.")
        self.recover_from_error_page("home page", response, retry_url=EBAY_URL)

    def search_for(self, search_term: str) -> "SearchResultsPage":
        """Submit a search and return the results page object."""
        search = self.page.get_by_placeholder("Search for anything")
        search.fill(search_term)
        search.press("Enter")
        self.recover_from_error_page("search results", retry_url=self.page.url)
        return SearchResultsPage(self.page)
