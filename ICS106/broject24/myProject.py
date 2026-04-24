


import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.stradivarius.com")

    yield driver

    driver.quit()

from selenium.webdriver.common.by import By
from page.base_page import BasePage


class SearchPage(BasePage):
    PRODUCTS = (By.XPATH, "//a[contains(@class,'product')]")
    PRICES = (By.XPATH, "//span[contains(@class,'price')]")

    def products_count(self):
        return len(self.get_elements(self.PRODUCTS))

    def first_prices(self):
        prices = self.get_elements(self.PRICES)[:3]
        result = []

        for p in prices:
            try:
                result.append(float(p.text.replace("₪", "").replace("$", "")))
            except:
                pass

        return result
from pages.home_page import HomePage
from pages.search_page import SearchPage

def test_search(driver):
    home = HomePage(driver)
    home.search("dress")

    search = SearchPage(driver)
    assert search.products_count() > 0, "לא נמצאו מוצרים — החיפוש לא עובד"

    # תובנה: החיפוש מחזיר תוצאות תקינות

def test_prices(driver):
    home = HomePage(driver)
    home.search("shirt")

    search = SearchPage(driver)
    prices = search.first_prices()

    for price in prices:
        assert price < 500, f"מחיר חריג: {price}"

    # תובנה: המחירים בטווח הגיוני למוצרי האתר

def test_products_exist(driver):
    home = HomePage(driver)
    home.search("pants")

    search = SearchPage(driver)
    assert search.products_count() > 0

    # תובנה: עמוד התוצאות נטען בצורה תקינה


def test_search_url(driver):
    home = HomePage(driver)
    home.search("jacket")

    assert "search" in driver.current_url.lower()

    # תובנה: האתר מעביר לדף תוצאות חיפוש נכון
