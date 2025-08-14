from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time
import time

class CartPage(BasePage):
	def __init__(self, driver):
		super().__init__(driver)

	def get_discount(self):
		DISCOUNT_ID = (By.CSS_SELECTOR, "#rightw #bts #stbl #discount")

		#2 cases: -5.00, or -1.00 10%
		try:
			discount_text = self.find_element(*DISCOUNT_ID).text
			if not discount_text or discount_text == "Discount":
				return 0.0
			discount_split = discount_text.split()
			discount_val = 0

			if len(discount_split) == 1:
				discount_val = abs(float(discount_split[0]))  #-5.00
			else: 
				discount_pct = discount_split[-1]  #-1 10%
				discount_val = abs(float(discount_split[0]))
			return discount_val
		except:
			return 0.0

	def get_subtotal(self):
		SUBTOTAL_ID = (By.CSS_SELECTOR, "#rightw #bts #stbl #sub")
		try:
			subtotal_text = self.find_element(*SUBTOTAL_ID).text
			if not subtotal_text or subtotal_text == "Subtotal":
				return 0.0
			subtotal = float(subtotal_text)
			return subtotal
		except:
			return 0.0
		
	def get_tax(self):
		TAX_ID = (By.CSS_SELECTOR,"#rightw #bts #stbl #tax")
		try:
			tax_text = self.find_element(*TAX_ID).text
			if not tax_text or tax_text == "Tax":
				return 0.0
			tax = float(tax_text)
			return tax
		except:
			return 0.0
		
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
		try:
			total_text = self.find_element(*TOTAL_ID).text
			if not total_text or total_text == "Total":
				return 0.0
			total = float(total_text)
			return total
		except:
			return 0.0
		
	def add_tip(self, tip_type, tip_amount):
		if tip_amount == 0: 
			return

		TIP_ID = (By.CSS_SELECTOR, "#rightstrip #tip")
		tip_btn = self.wait_for_element_clickable(TIP_ID, timeout=10)
		if tip_btn:
			self.driver.execute_script("arguments[0].scrollIntoView(true);", tip_btn)
			time.sleep(0.5)
			self.driver.execute_script("arguments[0].click();", tip_btn)
		else:
			# Fallback
			tip_btn = self.find_element(*TIP_ID)
			self.driver.execute_script("arguments[0].click();", tip_btn)

		#1. preset $tip (tip_type = '$')
		time.sleep(1)  # Wait for tip modal to fully load
		if tip_type == '$':
			# For dollar tips, manually enter the amount using number pad
			print(f"DEBUG: Entering dollar tip amount: {tip_amount}")
			# Enter each digit of the tip amount
			for digit in str(tip_amount):
				# Try different element types for the digit keys
				digit_key = (By.XPATH, f"//div[@id='vipPercent']//*[@class='dkey' and normalize-space(text())='{digit}']")
				digit_btn = self.wait_for_element_clickable(digit_key, timeout=2)
				if digit_btn:
					print(f"Clicking digit: {digit}")
					self.driver.execute_script("arguments[0].click()", digit_btn)
					time.sleep(0.2)
			
			# After entering amount, check if there's a submit button
			TIP_SUBMIT = (By.ID, "vipsubmit")
			submit_btn = self.wait_for_element_clickable(TIP_SUBMIT, timeout=2)
			if submit_btn:
				print("Clicking tip submit button")
				self.driver.execute_script("arguments[0].click()", submit_btn)
				# Always show what buttons are available for debugging
				all_tips = self.find_elements(By.CSS_SELECTOR, '#vipCoupon .discount')
				if all_tips:
					print("DEBUG: Available tip/discount buttons after clicking:")
					for tip in all_tips:
						print(f"  - Value: {tip.get_attribute('data-value')}, Text: {tip.text}")
			else:
				print(f"WARNING: Could not find tip button for ${tip_amount}")
				# List all available tip buttons for debugging
				all_tips = self.find_elements(By.CSS_SELECTOR, '#vipCoupon .discount')
				if all_tips:
					print("Available discount buttons in #vipCoupon:")
					for tip in all_tips:
						print(f"  - Value: {tip.get_attribute('data-value')}, Text: {tip.text}")
				# Also check for dkey elements
				all_dkeys = self.find_elements(By.CSS_SELECTOR, '#vipPercent .dkey')
				if all_dkeys:
					print("Available dkey buttons in #vipPercent:")
					for key in all_dkeys:
						print(f"  - Value: {key.get_attribute('data-value')}, Text: {key.text}")
		else:
			#2. preset %tip
			print(f"DEBUG: Looking for tip percentage button with value: {tip_amount}")
			TIP_PCT = (By.CSS_SELECTOR, f'#vipCoupon .discount[data-value="{tip_amount}"]')
			tip_pct_btn = self.wait_for_element_clickable(TIP_PCT, timeout=5)
			if tip_pct_btn:
				self.driver.execute_script("arguments[0].click()",tip_pct_btn)
			else:
				print(f"WARNING: Could not find tip button for {tip_amount}%")		

		#click submit when manually enter amount
		'''TIP_SUBMIT = (By.ID, "vipsubmit")
		submit_btn = self.find_element(*TIP_SUBMIT)
		self.driver.execute_script("arguments[0].click()",submit_btn)'''

		#=============to be deleted============
		#time.sleep(2)

		#return??

	def add_discount(self, disc_type, disc_amount): #(abs, 5) or (pct, 5)
		if disc_amount == 0: 
			return
		DISCOUNT_ID = (By.CSS_SELECTOR, "#rightw #bts #stbl #discount")
		discount_btn = self.wait_for_element_clickable(DISCOUNT_ID, timeout=10)
		if discount_btn:
			self.driver.execute_script("arguments[0].scrollIntoView(true);", discount_btn)
			time.sleep(0.5)
			self.driver.execute_script("arguments[0].click();", discount_btn)
		else:
			# Fallback
			discount_btn = self.find_element(*DISCOUNT_ID)
			self.driver.execute_script("arguments[0].click();", discount_btn)

		#1. preset $disc (tip_type = 'd')
		if disc_type == '$':
			disc_amount = '-' + str(disc_amount)
			#print(disc_amount)
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
		#time.sleep(2)


	def remove_tax(self):
		TAX_ID = (By.CSS_SELECTOR,"#rightw #bts #stbl #tax")
		tax_btn = self.find_element(*TAX_ID)
		tax_btn.click()
		
		TAX_ROMOVE_ID = (By.CSS_SELECTOR,".taxno")
		tax_remove_btn = self.find_element(*TAX_ROMOVE_ID)
		tax_remove_btn.click()






		