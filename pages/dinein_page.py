from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class DineinPage(BasePage):

	def __init__(self, driver):
		super().__init__(driver)

	def select_table(self, seatId):
		TABLE_SELECTOR = f'a[seat="{seatId}"]'
		TABLE_ID = (By.CSS_SELECTOR,TABLE_SELECTOR)
		###Having issue right now: seat not clickable, blocked by "floor"
		#self.find_element(*TABLE_ID).click()
		###so need to click through js code
		element = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located(TABLE_ID)
		)
		table = self.find_element(*TABLE_ID)

		#check if table been selected, color == #00a7d1 ?
		if table.value_of_css_property("background-color") == "rgba(0, 167, 209, 1)": 
			self.driver.execute_script("arguments[0].click();", table)
		elif seatId + 1 <= 100:
			self.select_table(seatId + 1)
		else: 
			print("No seat is available! ")

	def select_guest(self, num):
		GUEST_SELECTOR = f'.guests[data-v="{num}"]' 
		GUEST_NUM = (By.CSS_SELECTOR, GUEST_SELECTOR)
		#wait until clickable
		element = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located(GUEST_NUM)
		)
		self.find_element(*GUEST_NUM).click()

	def table_status(self):
		return None





