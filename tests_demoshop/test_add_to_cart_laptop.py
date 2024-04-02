import requests
from selene import browser, have
import allure
from tests_demoshop.conftest import LOGIN, PASSWORD
from utils.utils import post_demowebshop


def test_add_to_cart_laptop():
    with allure.step("Get user cookie"):
        response = post_demowebshop("login", data={"Email": LOGIN, "Password": PASSWORD},
                                    allow_redirects=False)
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})

    with allure.step("Add product to user's cart"):
        add_to_cart_url = "https://demowebshop.tricentis.com/addproducttocart/catalog/31/1/1"
        requests.post(add_to_cart_url, cookies={"NOPCOMMERCE.AUTH": cookie})

    with allure.step("Open cart page"):
        browser.open("http://demowebshop.tricentis.com")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open("https://demowebshop.tricentis.com/cart")

    with allure.step("Check items in cart"):
        browser.element('.product-name').should(have.text('14.1-inch Laptop'))

    with allure.step('Delete items'):
        browser.element('[name=removefromcart]').click()
        browser.element('[name=updatecart]').click()

    with allure.step('Check empty cart'):
        browser.element('.order-summary-content').should(have.text('Your Shopping Cart is empty!'))
