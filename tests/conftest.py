import pytest
from itertools import product
from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.dinein_page import DineinPage
from pages.ordering_page import OrderingPage
from database.ssh import ssh_run_command
from database.get_mypos import GetMypos
from config import Config
import time 


#Setup Server Environment
@pytest.fixture(scope="session",autouse=True)
def setup_command():
	#clear db
	ssh_run_command(Config.SERVER_IP, Config.SSH_USERNAME, Config.SSH_PASSWORD, "php 64cleardb.php")


# Use module scope for better performance - browser stays open for entire test module
@pytest.fixture(scope="module")
def browser():
	manager = BrowserManager(browser_name = 'chrome')
	driver = manager.start_browser()
	yield driver
	manager.close_browser()

@pytest.fixture(scope="function")
def login_page(browser):
	login_page = LoginPage(browser)
	login_page.open(Config.SERVER_URL)
	yield login_page
	# Minimal cleanup - clear cookies and navigate to home
	try:
		browser.delete_all_cookies()
		browser.get(Config.SERVER_URL)
	except:
		pass  # Ignore cleanup errors

#Update setting in database before each full test process
# Add new settings to the keys list and they'll automatically get all combinations
@pytest.fixture(scope="function", params=[
    dict(zip(["store_tip", "tipbefored", "support.taxb4discountnew"], values))
    for values in product([0, 1], repeat=3)
])

def setup_settings(browser, request):
	setting_dict = request.param	
	db = GetMypos(Config.SERVER_IP)
	db.update_mystore_settings(setting_dict)
	ssh_run_command(Config.SERVER_IP, Config.SSH_USERNAME, Config.SSH_PASSWORD, "systemctl restart apache2")

	time.sleep(1)
	return setting_dict

@pytest.fixture(scope="function")
def serverip():
	return Config.SERVER_IP

# Lightweight cleanup between tests
@pytest.fixture(autouse=True)
def quick_reset(browser):
	"""Minimal reset between tests - just clear cart and modals"""
	yield
	# After test cleanup
	try:
		# Quick JavaScript cleanup without full page reload
		browser.execute_script("""
			// Clear cart if exists
			if (typeof clearCart === 'function') {
				clearCart();
			}
			// Close any open modals
			var modals = document.querySelectorAll('.modal.show, .modal.in');
			modals.forEach(function(modal) {
				modal.style.display = 'none';
				modal.classList.remove('show', 'in');
			});
			// Remove modal backdrops
			var backdrops = document.querySelectorAll('.modal-backdrop');
			backdrops.forEach(function(backdrop) {
				backdrop.remove();
			});
		""")
	except:
		# If JavaScript cleanup fails, do nothing - test will handle its own setup
		pass