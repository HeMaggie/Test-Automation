import time
import re 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage():
	def __init__(self,driver):
		self.driver = driver

	def find_element(self, *locator):
		return self.driver.find_element(*locator)

	def find_elements(self, *locator):
		return self.driver.find_elements(*locator)

	def wait_for_element(self, locator, timeout=10):
		try:
			return WebDriverWait(self.driver, timeout).until(
				EC.presence_of_element_located(locator)
			)
		except TimeoutException:
			return None

	def wait_for_element_clickable(self, locator, timeout=10):
		try:
			return WebDriverWait(self.driver, timeout).until(
				EC.element_to_be_clickable(locator)
			)
		except TimeoutException:
			return None

	def wait_for_element_visible(self, locator, timeout=10):
		try:
			return WebDriverWait(self.driver, timeout).until(
				EC.visibility_of_element_located(locator)
			)
		except TimeoutException:
			return None
	
	def send_key_slowly(self, element, text):
		for t in text:
			element.send_keys(t)
			time.sleep(0.1)

	def is_valid_format(self,s):
		pattern = r"^-.*-$"
		return bool(re.match(pattern,s))

	def open(self,url):
		self.driver.get(url)
