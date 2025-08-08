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

		#phone field
		PHONE_ID = (By.ID, "pickphone")
		phone_field = self.find_element(*PHONE_ID)
		if not phone_field.get_attribute("value"):
			self.send_key_slowly(phone_field, phone)

		#name field
		NAME_ID = (By.ID, "pickname")
		name_field = self.find_element(*NAME_ID)
		#if auto filled, then do nothing, else enter a name
		if not name_field.get_attribute("value"):
			self.send_key_slowly(name_field, name)

		#address field
		ADDRESS_ID = (By.ID, "addr1")
		address_field = self.find_element(*ADDRESS_ID)

		#submit or cancel
		SUBMIT_ID = (By.ID, "picksubmit")
		submit_btn = self.find_element(*SUBMIT_ID)

		submit_btn.click()





