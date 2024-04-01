import requests
from selene import browser, have
import allure
from tests_demoshop.conftest import DOMAIN_URL, LOGIN, PASSWORD
from utils.utils import post_demowebshop


def test_add_to_cart_book():
    with allure.step("Get user cookie"):
        response = post_demowebshop("login", data={"Email": LOGIN, "Password": PASSWORD},
                                    allow_redirects=False)
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})

    with allure.step("Add product to user's cart"):
        add_to_cart_url = "https://demowebshop.tricentis.com/addproducttocart/catalog/13/1/1"
        requests.post(add_to_cart_url, cookies={"NOPCOMMERCE.AUTH": cookie}, allow_redirects=False)

    with allure.step("Open cart page"):
        browser.open(DOMAIN_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open("https://demowebshop.tricentis.com/cart")

    with allure.step("Check items in cart"):
        browser.element('[class="product-name"]').should(have.text('Computing and Internet'))

    with allure.step('Delete items'):
        browser.element('[name=removefromcart]').click()
        browser.element('[name=updatecart]').click()

    with allure.step('Check empty cart'):
        browser.element('[class=order-summary-content]').should(have.text('Your Shopping Cart is empty!'))
