from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class OrderingPage(BasePage):
	"""docstring for OrderingPage"""
	def __init__(self, driver):
		super().__init__(driver)

	def find_item(self, menu_name, category_id, item_id): 
		#menu_name:00Regular, category_id:1, item_id:551
		#select menu
		self.menu_helper(menu_name)

		#select category
		self.category_helper(category_id)

		#select item
		ITEM_ID = (By.CSS_SELECTOR, f'.item[iid="{item_id}"]')
		item = self.find_element(*ITEM_ID)

		return item

	def add_item_to_cart(self, menu_name, category_id, item_id):
		#click the item
		item = self.find_item(menu_name, category_id, item_id)
		coption = item.get_attribute("coptions")      #modifier groups
		item_classes = item.get_attribute("class")    #item classes

		#if with subitems
		if "gotsub" in item_classes:
			self.subitem_helper(item)
		else:
			self.driver.execute_script("arguments[0].click()",item)

		#if with modifiers, add modifiers and submit to cart
		if self.is_valid_format(coption):  #check if coption is in '-1-2-' format
			self.modifier_helper(coption)


	def edit_from_cart(self):
		return None

	def enter_order(self):
		self.find_element(By.ID, "enter").click()

	def menu_helper(self, menu_name):
		MENU_NAME = (By.CSS_SELECTOR, f'.pmenu[data-umenu="{menu_name}"]')
		menu = self.find_element(*MENU_NAME)
		self.driver.execute_script("arguments[0].click()",menu)
		#Error Handler??

	def category_helper(self,category_id):
		CATEGOTY_ID = (By.CSS_SELECTOR, f'.cat[cid="{category_id}"]')
		self.find_element(*CATEGOTY_ID).click()
		#Error Handler??

	def modifier_helper(self,coption):
		coptions = coption.strip('-').split('-')
		for n in coptions:
			#find all the coptions in grp n: data-grp
			MOD_ID = (By.CSS_SELECTOR, f'.mcrow .c0[data-grp="{n}"]')
			mods = self.find_elements(*MOD_ID)
			for m in range(0,len(mods)):
				mods[m].click()
				break  #just choose 1 from each grp for now

		MOD_SUBMIT_ID = (By.CSS_SELECTOR, '#comboitem .osubmit')
		mod_submit_btn = self.find_element(*MOD_SUBMIT_ID)
		mod_submit_btn.click()
		

	def subitem_helper(self,item):
		SUBITEM_ID = (By.CSS_SELECTOR, '.itemsub')
		itemsub = item.find_elements(*SUBITEM_ID)

		if len(itemsub) == 0: return
		for i in range(0,len(itemsub)):
			itemsub[i].click()
			break  #Just need to click one for now
		

		