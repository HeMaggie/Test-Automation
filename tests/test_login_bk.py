import pytest
from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.dinein_page import DineinPage
from pages.ordering_page import OrderingPage
import time

'''#@pytest.fixture (scope="module")
def browser():
	manager = BrowserManager(browser_name = 'chrome')
	driver = manager.start_browser()
	yield driver
	manager.close_browser()

def test_user_flow(browser):
	url = 'http://192.168.9.64'
	#url = 'http://192.168.1.88'
	login_page = LoginPage(browser)
	login_page.open(url)
	username = login_page.login("3309")
	#check if log in succeeds
	if username != "Login":
		login_page.set_login_status(True)
	else:
		login_page.set_login_status(False)
	print(f"Login Status: {login_page.login_status}")

	time.sleep(0.5)
	dinein_page = DineinPage(browser)
	dinein_page.select_table(1)
	time.sleep(0.5)
	dinein_page.select_guest(1)

	ordering_page = OrderingPage(browser)
	ordering_page.add_item_to_cart(7)
	time.sleep(1)
	ordering_page.enter_order()
	time.sleep(10)
'''