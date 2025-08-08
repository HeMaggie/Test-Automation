import pytest
from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.dinein_page import DineinPage
from pages.ordering_page import OrderingPage
from database.ssh import ssh_run_command
from database.get_mypos import GetMypos
from config import Config
import time 


#Setup Server Environment
@pytest.fixture(scope="module",autouse=True)
def setup_command():
	#clear db
	ssh_run_command(Config.SERVER_IP, Config.SSH_USERNAME, Config.SSH_PASSWORD, "php 64cleardb.php")


@pytest.fixture(scope="module")
def browser():
	manager = BrowserManager(browser_name = 'chrome')
	driver = manager.start_browser()
	yield driver
	manager.close_browser()

@pytest.fixture(scope="module")
def login_page(browser):
	login_page = LoginPage(browser)
	login_page.open(Config.SERVER_URL)
	yield login_page

#Update setting in database before each full test preocess
@pytest.fixture(scope="module", params=[
    {"store_tip": 0, "tipbefored": 0},
    {"store_tip": 0, "tipbefored": 1},
    {"store_tip": 1, "tipbefored": 0},
    {"store_tip": 1, "tipbefored": 1}
])

def setup_settings(browser, request):
	setting_dict = request.param	
	db = GetMypos(Config.SERVER_IP)
	db.update_mystore_settings(setting_dict)
	ssh_run_command(Config.SERVER_IP, Config.SSH_USERNAME, Config.SSH_PASSWORD, "systemctl restart apache2")

	time.sleep(1)
	return setting_dict

@pytest.fixture(scope="module")
def serverip():
	return Config.SERVER_IP





