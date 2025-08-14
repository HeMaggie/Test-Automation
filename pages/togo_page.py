from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class TogoPage(BasePage):

	def __init__(self, driver):
		super().__init__(driver)

	def is_customer_page(self):
		is_open = False
		CUSTOMERPAGE_ID = (By.ID, "pickw")
		if self.find_element(*CUSTOMERPAGE_ID).value_of_css_property("display") == "block":
			is_open = True
		return is_open

	def open_customer_page(self):
		CINFO_ID = (By.ID, "cinfo")
		cinfo = self.find_element(*CINFO_ID)
		self.driver.execute_script("arguments[0].click();", cinfo)

	def enter_customer_info(self, phone='8888888888', name='test', address=''):
		#make sure customerinfo page is open before entering phone
		if not self.is_customer_page():
			self.open_customer_page()

		#phone field with wait for interactable element
		PHONE_ID = (By.ID, "pickphone")
		phone_field = self.wait_for_element_visible(PHONE_ID, timeout=10)
		if phone_field and not phone_field.get_attribute("value"):
			# Ensure element is clickable before interacting
			phone_field = self.wait_for_element_clickable(PHONE_ID, timeout=5)
			if phone_field:
				phone_field.clear()  # Clear any existing value
				self.send_key_slowly(phone_field, phone)

		#name field with wait
		NAME_ID = (By.ID, "pickname")
		name_field = self.wait_for_element_clickable(NAME_ID, timeout=5)
		#if auto filled, then do nothing, else enter a name
		if name_field and not name_field.get_attribute("value"):
			name_field.clear()
			self.send_key_slowly(name_field, name)

		#address field (optional - may not exist on all pages)
		ADDRESS_ID = (By.ID, "addr1")
		address_field = self.wait_for_element(ADDRESS_ID, timeout=3)
		# Address field is optional, so we don't fail if it's not found

		#submit or cancel with wait
		SUBMIT_ID = (By.ID, "picksubmit")
		submit_btn = self.wait_for_element_clickable(SUBMIT_ID, timeout=10)
		if submit_btn:
			self.driver.execute_script("arguments[0].click();", submit_btn)
		else:
			# Fallback to regular click
			submit_btn = self.find_element(*SUBMIT_ID)
			self.driver.execute_script("arguments[0].click();", submit_btn)





