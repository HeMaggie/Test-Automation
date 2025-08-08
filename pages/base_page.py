import time
import re 

class BasePage():
	def __init__(self,driver):
		self.driver = driver

	def find_element(self, *locator):
		return self.driver.find_element(*locator)

	def find_elements(self, *locator):
		return self.driver.find_elements(*locator)
	
	def send_key_slowly(self, element, text):
		for t in text:
			element.send_keys(t)
			time.sleep(0.1)

	def is_valid_format(self,s):
		pattern = r"^-.*-$"
		return bool(re.match(pattern,s))

	def open(self,url):
		self.driver.get(url)
