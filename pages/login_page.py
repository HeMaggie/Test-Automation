from selenium import webdriver
from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class LoginPage(BasePage):
	#For table page - login btn
	TABLE_LOGIN_BTN = (By.ID,'seatlogin')

	#for cart page - login btn
	CART_LOGIN_BTN = (By.ID,"login")
	PASSWORD_INPUT = (By.ID,"loginp")
	LOGIN_SUBMIT = (By.ID,"loginSubmit")


	def __init__(self, driver):
		super().__init__(driver)
		self.login_status = False
		self.login_button_text = "Login"

	def open(self,url):
		super().open(url)
	
	def login(self, password, page="table"):
		self.driver.delete_all_cookies()

		#find login button
		if page == "table":
			self.find_element(*self.TABLE_LOGIN_BTN).click()
		else:
			# Handle cart login button that might be intercepted
			cart_login_btn = self.find_element(*self.CART_LOGIN_BTN)
			self.driver.execute_script("arguments[0].scrollIntoView(true);", cart_login_btn)
			time.sleep(0.5)
			self.driver.execute_script("arguments[0].click();", cart_login_btn)

		#enter password
		pwd_input = self.find_element(*self.PASSWORD_INPUT)
		self.send_key_slowly(pwd_input,password)

		#submit password to log in
		self.find_element(*self.LOGIN_SUBMIT).click()
		time.sleep(0.5)

		self.login_button_text = self.find_element(*self.TABLE_LOGIN_BTN).text

		#check if log in succeeds
		time.sleep(0.5)
		if self.login_button_text != "Login":
			self.set_login_status(True)
		else:
			self.set_login_status(False)
		#print(f"Login Status: {self.login_status}")

		return self.login_button_text


	def set_login_status(self,status):
		self.login_status = status 




