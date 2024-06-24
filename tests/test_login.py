from pages.login_page import LoginPage
import pytest
import time

url = 'http://192.168.1.88'

@pytest.fixture
def login_page(browser):
	login_page = LoginPage(browser)
	login_page.open(url)
	yield login_page

@pytest.mark.parametrize("password,expected_text",[("3309","kwickpos"),("000","boss")])
def test_successful_login(login_page, password, expected_text):
	login_button_text = login_page.login(password)
	time.sleep(0.5)
	assert login_button_text == expected_text, f"Login failed with correct password: {password}"

@pytest.mark.parametrize("password",[("acd"),("def")])
def test_unsuccessful_login(login_page, password):
	login_button_text = login_page.login(password)
	assert login_button_text == "Login", f"Login succeeded with incorrect password: {password}"

@pytest.mark.parametrize("password,expected_text",[("3309","kwickpos"),("000","boss")])
def test_login_button_text(login_page, password, expected_text):
	login_button_text = login_page.login(password)
	time.sleep(0.5)
	assert login_button_text == expected_text, f"The text of the login button is: {login_button_text}"

