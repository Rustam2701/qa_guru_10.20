import requests
from selene import browser, have
import allure
from tests_demoshop.conftest import DOMAIN_URL, LOGIN, PASSWORD


def test_add_to_cart_computer():
    with allure.step("Get user cookie"):
        response = requests.post(url=DOMAIN_URL + "login", data={"Email": LOGIN, "Password": PASSWORD},
                                 allow_redirects=False)
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Add product to user's cart"):
        add_to_cart_url = "https://demowebshop.tricentis.com/addproducttocart/details/72/1"
        requests.post(add_to_cart_url, cookies={"NOPCOMMERCE.AUTH": cookie})

    with allure.step("Open cart page"):
        browser.open("http://demowebshop.tricentis.com")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open("https://demowebshop.tricentis.com/cart")

    with allure.step("Check items in cart"):
        browser.element('[class="product-name"]').should(have.text('Build your own cheap computer'))

    with allure.step(''):
        browser.element('[name=removefromcart]').click()
        browser.element('[name=updatecart]').click()

    with allure.step("Check items in cart"):
        browser.element('[class=order-summary-content]').should(have.text('Your Shopping Cart is empty!'))
