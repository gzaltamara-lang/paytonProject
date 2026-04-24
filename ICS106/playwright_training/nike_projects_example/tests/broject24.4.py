



from selenium.webdriver.common.by import By
from page.base_page import BasePage

class LoginPage(BasePage):

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.XPATH, "//h3[@data-test='error']")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_element(self.ERROR).text

    from selenium.webdriver.common.by import By
    from pages.base_page import BasePage

    class InventoryPage(BasePage):
        ITEMS = (By.CLASS_NAME, "inventory_item")
        PRICES = (By.CLASS_NAME, "inventory_item_price")
        ADD_TO_CART = (By.XPATH, "//button[contains(text(),'Add to cart')]")
        CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

        def get_items_count(self):
            return len(self.get_elements(self.ITEMS))

        def get_first_3_prices(self):
            prices = self.get_elements(self.PRICES)[:3]
            return [float(p.text.replace("$", "")) for p in prices]

        def add_first_item_to_cart(self):
            self.get_elements(self.ADD_TO_CART)[0].click()

        def go_to_cart(self):
            self.click(self.CART_ICON)
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):

    CART_ITEMS = (By.CLASS_NAME, "cart_item")

    def get_cart_items_count(self):
        return len(self.get_elements(self.CART_ITEMS))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

# 1. התחברות תקינה
def test_valid_login(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.get_items_count() > 0, "Login failed - no products found"


# 2. התחברות לא תקינה
def test_invalid_login(driver):
    login = LoginPage(driver)
    login.login("standard_user", "wrong_password")

    assert "Epic sadface" in login.get_error_message()


# 3. בדיקת מחירים
def test_prices_under_limit(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    prices = inventory.get_first_3_prices()

    assert len(prices) == 3

    for price in prices:
        assert price < 100, f"Price too high: {price}"


# 4. הוספה לעגלה
def test_add_to_cart(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert cart.get_cart_items_count() == 1


# 5. ניווט לעגלה
def test_navigation_to_cart(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.go_to_cart()

    assert "cart" in driver.current_url

    