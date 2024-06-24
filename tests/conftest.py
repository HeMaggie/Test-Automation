import pytest
from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.dinein_page import DineinPage
from pages.ordering_page import OrderingPage
import time

url = 'http://192.168.9.64'
#url = 'http://192.168.1.88'

@pytest.fixture(scope="module")
def browser():
	manager = BrowserManager(browser_name = 'chrome')
	driver = manager.start_browser()
	yield driver
	manager.close_browser()

@pytest.fixture(scope="module")
def login_page(browser):
	login_page = LoginPage(browser)
	login_page.open(url)
	yield login_page


