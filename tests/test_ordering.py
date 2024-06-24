import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.dinein_page import DineinPage
from pages.ordering_page import OrderingPage
from pages.cart_page import CartPage
import time

@pytest.fixture(scope="module")
def login(login_page):
	username = login_page.login("3309")
	#check if log in succeeds
	if username != "Login":
		login_page.set_login_status(True)
	else:
		login_page.set_login_status(False)
	print(f"Login Status: {login_page.login_status}")
	return login_page.login_status

@pytest.fixture
def dinein(browser, login):
	if login:
		dinein_page = DineinPage(browser)
		dinein_page.select_table(1) 
		dinein_page.select_guest(1)
		return dinein_page
	else:
		pytest.fail("Login failed, cannot proceed with dein-in")


@pytest.mark.parametrize(
	"menu,category,item,discount,subtotal,tax,tip,total",
	[
		("00Regular","1","7",0,10,1,0,11),
		("00Regular","1","22",0,10,1,0,11),
		("00Regular","1","49",0,13,1.3,0,14.3)
	]
)
def test_item_to_cart(browser, dinein, menu,category,item,discount,subtotal,tax,tip,total):
	ordering_page = OrderingPage(browser)
	ordering_page.add_item_to_cart(menu,category,item)  #menu, category_id, item_id
	cart_page = CartPage(browser)

	#change "tip after tax" setting
	#if discount > 0 : add discount
	#if tip > 0: add tips

	real_discount = cart_page.get_discount()
	real_subtotal = cart_page.get_subtotal()
	real_tax = cart_page.get_tax()
	real_tip = cart_page.get_tip()
	real_total = cart_page.get_total()
	
	ordering_page.enter_order()

	#check database

	#assert error
	assert discount == real_discount, f'Discount is "{real_discount}", should be "{discount}"'
	assert subtotal == real_subtotal, f'Subtotal is "{real_subtotal}", should be "{subtotal}"'
	assert tax == real_tax,  f'Tax is "{real_tax}", should be "{tax}"'
	assert tip == real_tip,  f'Tip is "{real_tip}", should be "{tip}"'
	assert total == real_total,  f'Total is "{real_total}", should be "{total}"'



