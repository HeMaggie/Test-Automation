from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class CartPage(BasePage):
	def __init__(self, driver):
		super().__init__(driver)

	def get_discount(self):
		DISCOUNT_ID = (By.CSS_SELECTOR, "#rightw #bts #stbl #discount")

		#2 cases: -5.00, or -1.00 10%
		discount_text = self.find_element(*DISCOUNT_ID).text
		discount_split = discount_text.split()
		discount_val = 0

		if len(discount_split) == 1:
			discount_val = abs(float(discount_split[0]))  #-5.00
		else: 
			discount_pct = discount_split[-1]  #-1 10%
			discount_val = abs(float(discount_split[0]))
		return discount_val

	def get_subtotal(self):
		SUBTOTAL_ID = (By.CSS_SELECTOR, "#rightw #bts #stbl #sub")
		subtotal_text = self.find_element(*SUBTOTAL_ID).text
		subtotal = float(subtotal_text)
		return subtotal
		
	def get_tax(self):
		TAX_ID = (By.CSS_SELECTOR,"#rightw #bts #stbl #tax")
		tax_text = self.find_element(*TAX_ID).text
		tax = float(tax_text)
		return tax
		
	def get_tip(self):
		TIP_ID = (By.CSS_SELECTOR, "#rightstrip #tip")

		#3 cases: Tips, "Tips $1.00" or "15% Tips\n1.65"
		tip_text = self.find_element(*TIP_ID).text
		tip_split = tip_text.split()
		tip_val = 0 

		if len(tip_split) == 2: 
			tip_val = float(tip_split[1][1:])
		elif len(tip_split) == 3:
			tip_pct = tip_text.split()[0]
			tip_val = float(tip_text.split()[-1])

		return tip_val 

	def get_total(self):
		TOTAL_ID = (By.CSS_SELECTOR, "#rightw #bts #stbl #total")
		total_text = self.find_element(*TOTAL_ID).text
		total = float(total_text)
		return total
		
	def add_tip(self, tip_type, tip_amount):
		TIP_ID = (By.CSS_SELECTOR, "#rightstrip #tip")
		tip_btn = self.find_element(*TIP_ID)
		tip_btn.click()

		#1. preset $tip (tip_type = 'd')
		if tip_type == 'abs':
			tip_amount = '-' + str(tip_amount)
			print(tip_amount)
			TIP_DOLLAR = (By.CSS_SELECTOR, f'#vipCoupon .discount[data-value="{tip_amount}"]')
			tip_dollar_btn = self.find_element(*TIP_DOLLAR)
			self.driver.execute_script("arguments[0].click()",tip_dollar_btn)
			#what if the tip amount was not preset??? 
		else:
			#2. preset %tip
			TIP_PCT = (By.CSS_SELECTOR, f'#vipCoupon .discount[data-value="{tip_amount}"]')
			tip_pct_btn = self.find_element(*TIP_PCT)
			self.driver.execute_script("arguments[0].click()",tip_pct_btn)
			#what if the tip percentage was not preset???		

		#click submit when manually enter amount
		'''TIP_SUBMIT = (By.ID, "vipsubmit")
		submit_btn = self.find_element(*TIP_SUBMIT)
		self.driver.execute_script("arguments[0].click()",submit_btn)'''

		#=============to be deleted============
		time.sleep(2)

		#return??

	def add_discount(self, disc_type, disc_amount):
		DISCOUNT_ID = (By.CSS_SELECTOR, "#rightw #bts #stbl #discount")
		discount_btn = self.find_element(*DISCOUNT_ID)
		discount_btn.click()

		#1. preset $disc (tip_type = 'd')
		if disc_type == 'abs':
			disc_amount = '-' + str(disc_amount)
			print(disc_amount)
			DISC_DOLLAR = (By.CSS_SELECTOR, f'#vipCoupon .discount[data-value="{disc_amount}"]')
			disc_dollar_btn = self.find_element(*DISC_DOLLAR)
			self.driver.execute_script("arguments[0].click()",disc_dollar_btn)
			#what if the tip amount was not preset??? 
		else:
			#2. preset %disc
			DISC_PCT = (By.CSS_SELECTOR, f'#vipCoupon .discount[data-value="{disc_amount}"]')
			disc_pct_btn = self.find_element(*DISC_PCT)
			self.driver.execute_script("arguments[0].click()",disc_pct_btn)
			#what if the tip percentage was not preset???		

		#click submit when manually enter amount
		'''DISC_SUBMIT = (By.ID, "vipsubmit")
		submit_btn = self.find_element(*DISC_SUBMIT)
		self.driver.execute_script("arguments[0].click()",submit_btn)'''

		#=============to be deleted============
		time.sleep(2)


	def remove_tax(self):
		TAX_ID = (By.CSS_SELECTOR,"#rightw #bts #stbl #tax")
		tax_btn = self.find_element(*TAX_ID)
		tax_btn.click()
		
		TAX_ROMOVE_ID = (By.CSS_SELECTOR,".taxno")
		tax_remove_btn = self.find_element(*TAX_ROMOVE_ID)
		tax_remove_btn.click()






		