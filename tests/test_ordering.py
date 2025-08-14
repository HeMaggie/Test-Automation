import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.dinein_page import DineinPage
from pages.togo_page import TogoPage
from pages.ordering_page import OrderingPage
from pages.cart_page import CartPage
from database.get_mypos import GetMypos
from database.ssh import ssh_run_command
from config import Config
import time
from decimal import Decimal

#1. define order type
#order type value: "dinein", "walkin"

# Remove hardcoded ORDER_TYPE - will be parameterized

# Parameterize order types at function level for clean test isolation
@pytest.fixture(scope="function", params=["dinein", "walkin"])
def order_type(request):
	"""Fixture that provides both order types for testing"""
	return request.param

@pytest.fixture(scope="function")
def login(browser, login_page, order_type):
	# Always do fresh login for each test
	if order_type == "dinein":
		username = login_page.login(Config.TEST_USERS['kwickpos']['password'])
	else:
		username = login_page.login(Config.TEST_USERS['kwickpos']['password'],"cart")
	#check if log in succeeds
	if username != "Login":
		login_page.set_login_status(True)
	else:
		login_page.set_login_status(False)
	return login_page.login_status

@pytest.fixture
def ordering(browser, login, order_type):
	#time.sleep(1)
	if not login:
		pytest.fail("Login failed, cannot proceed with ordering")

	#refresh to apply updates of db settings before ordering
	time.sleep(0.5)
	base_page = BasePage(browser)
	# Try to find reload button with wait, if not found, just refresh the page
	reload_btn = base_page.wait_for_element_clickable((By.ID, "kwickhelp"), timeout=5)
	if reload_btn:
		browser.execute_script("arguments[0].click();", reload_btn)
	else:
		# Fallback: just refresh the browser if element not found
		browser.refresh()
	time.sleep(1)

	#hard coded for now, need to automatically get it later
	if order_type == "dinein":
		dinein_page = DineinPage(browser)
		try:
			dinein_page.select_table(1) 
			dinein_page.select_guest(1)
		except Exception as e:
			print(f"Dinein setup failed: {e}")
		return browser  # Return browser instead of page object
	elif order_type == "walkin":
		# First, click the walkin button to navigate to walkin page
		base_page = BasePage(browser)
		WALKIN_BTN = (By.ID, "side_walkin")
		walkin_btn = base_page.wait_for_element_clickable(WALKIN_BTN, timeout=10)
		if walkin_btn:
			print("Clicking walkin button to switch to walkin mode")
			browser.execute_script("arguments[0].click();", walkin_btn)
			time.sleep(1)  # Wait for page to load
		
		togo_page = TogoPage(browser)
		try:
			#make sure the customerinfo page is open before entering cinfo
			if not togo_page.is_customer_page():
				togo_page.open_customer_page()		
			#enter customerinfo
			togo_page.enter_customer_info()
		except Exception as e:
			print(f"Togo setup failed: {e}")
			# Continue anyway - some tests might not need customer info
		return browser  # Return browser instead of page object

#====== Test Cases ========

TIP_V = DISC_V = 2
TIP_P = DISC_P = 10

#menu_arr{menu_name:{"category_id":((item_id,item_price))}}
menu_arr =  {
				"00Regular":
				{
					"1": [("7",10)]
					#"1": [("7",10),("22",10),("49",13),("50",13)],
					#"2": [("51",10),("52",10),("53",13),("54",13)],
					#"3": [("55",10),("56",10),("57",13),("58",13)],
					#"4": [("59",10),("60",10),("61",13),("62",13)]
				}
            }
                
test_cases = []

for m, cat in menu_arr.items():  #menu: 00Regular
    for c, items in cat.items():  #category: 1,2,3,4
        for i in items: #items: [("7",10),("22",10),("49",13),("50",13)]
			##menu,category,item_id,price,discount,tip
            test_cases.append((m, c, i[0], i[1], ('%', 5), ('$', 5))) 
            test_cases.append((m, c, i[0], i[1], ('%', 5), ('%', 5)))
            test_cases.append((m, c, i[0], i[1], ('$', 5), ('$', 5)))
            test_cases.append((m, c, i[0], i[1], ('$', 5), ('%', 5)))


#======= Start Testing =======
@pytest.mark.parametrize(
	"menu,category,item,price,discount,tip",
	test_cases
)

#browser and setup_settings from the conftest page
def test_item_to_cart(browser, serverip, setup_settings, ordering, menu,category,item,price,discount,tip):

	ordering_page = OrderingPage(browser)
	ordering_page.add_item_to_cart(menu,category,item)  #menu, category_id, item_id
	cart_page = CartPage(browser)

	#Preset Settings
	#Change "tip after tax" setting
	tip_after_tax = setup_settings["store_tip"]
	tip_b4_disc = setup_settings["tipbefored"]

	tax_rate = 0.1
	if category in ("1", "3"):
		tax_rate = 0.1
	elif category in ("2", "4"):
		tax_rate = 0.1


	#=======Calculations based on formula=======
	#Discount
	disc_type = discount[0]
	disc_rate = discount[1]
	disc_val = disc_rate
	if disc_type == '%':
		disc_val = price * disc_rate / 100  # disc_type == %
		
	#Subtotal
	subtotal_val = price - disc_val
	#Tax
	tax_val = subtotal_val * tax_rate
	#Tip
	tip_type = tip[0]
	tip_rate = tip[1]
	tip_val = tip_rate
	if tip_type == '%' and tip_after_tax == 0:  #subtotal
		if tip_b4_disc == 0:
			tip_val = subtotal_val * tip_rate / 100 
		else:
			tip_val = (subtotal_val + disc_val) * tip_rate / 100

	elif tip_type == '%': #tip_after_tax = 1, total
		if tip_b4_disc == 0:
			tip_val = (subtotal_val + tax_val) * tip_rate / 100  
		else:
			tip_val = (subtotal_val + disc_val + tax_val) * tip_rate / 100  

	#Total
	total_val = subtotal_val + tax_val + tip_val    ###round(2)??
	
	#round(2)
	disc_val = round(disc_val,2)
	subtotal_val = round(subtotal_val,2)
	tax_val = round(tax_val,2)
	tip_val = round(tip_val,2)
	total_val = round(total_val,2)

	#=================check cart =================
	#Add discounts & tips
	if disc_rate != 0:
		cart_page.add_discount(disc_type,disc_rate)

	if tip_rate != 0:
		cart_page.add_tip(tip_type,tip_rate)

	#Get the real cart amount
	time.sleep(2)  # Wait longer for cart to update
	print(f"\n=== DEBUG: Getting cart values ===")
	cart_discount = cart_page.get_discount()
	print(f"Got discount: {cart_discount}")
	cart_subtotal = cart_page.get_subtotal()
	print(f"Got subtotal: {cart_subtotal}")
	cart_tax = cart_page.get_tax()
	print(f"Got tax: {cart_tax}")
	cart_tip = cart_page.get_tip()
	print(f"Got tip: {cart_tip}")
	cart_total = cart_page.get_total()
	print(f"Got total: {cart_total}")
	
	# Debug output
	print(f"\n=== DEBUG: Test Parameters ===")
	print(f"Item price: {price}")
	print(f"Discount: {discount} (type={disc_type}, rate={disc_rate})")
	print(f"Tip: {tip} (type={tip_type}, rate={tip_rate})")
	print(f"\n=== Expected Calculations ===")
	print(f"Expected discount: {disc_val}")
	print(f"Expected subtotal: {subtotal_val}")
	print(f"Expected tax: {tax_val}")
	print(f"Expected tip: {tip_val}")
	print(f"Expected total: {total_val}")
	print(f"\n=== Actual Cart Values ===")
	print(f"Cart discount: {cart_discount}")
	print(f"Cart subtotal: {cart_subtotal}")
	print(f"Cart tax: {cart_tax}")
	print(f"Cart tip: {cart_tip}")
	print(f"Cart total: {cart_total}")
	


	#assert error BEFORE entering order
	#print(setup_settings)
	#Cart == Formula
	assert cart_discount == disc_val, f'Discount is "{cart_discount}", should be "{disc_val}"'
	assert cart_subtotal == subtotal_val, f'Subtotal is "{cart_subtotal}", should be "{subtotal_val}"'
	assert cart_tax == tax_val,  f'Tax is "{cart_tax}", should be "{tax_val}"'
	assert cart_tip == tip_val,  f'Tip is "{cart_tip}", should be "{tip_val}"'
	assert cart_total == total_val,  f'Total is "{cart_total}", should be "{total_val}"'

	#Enter Order after validation
	ordering_page.enter_order()


	#=============check database==============
	# Wait longer for database to process the order
	time.sleep(3)
	db = GetMypos(serverip)
	# Try to get the last order with retry logic
	retry_count = 0
	last_order = None
	while retry_count < 3:
		try:
			orders = db.get_myorder("order by order_id desc limit 1")
			if orders and len(orders) > 0:
				last_order = orders[0]  # Get first item from list
				break
		except Exception as e:
			print(f"Database query attempt {retry_count + 1} failed: {e}")
		time.sleep(1)
		retry_count += 1
	
	if not last_order:
		pytest.fail("Could not retrieve order from database after 3 attempts")
	db_order_id = last_order['order_id']
	db_discount = last_order['discountvalue']
	db_subtotal = last_order['food'] - db_discount
	db_tax = last_order['tax']
	db_tip = abs(last_order['tip'])
	db_total = last_order['amount'] + db_tip
	#print (last_order)

	#float
	db_discount = float(db_discount)
	db_subtotal = float(db_subtotal)
	db_tax = float(db_tax)
	db_tip = float(db_tip) 
	db_total = float(db_total)

	# database == Formula
	assert db_discount == disc_val, f'Discount is "{db_discount}", should be "{disc_val}"'
	assert db_subtotal == subtotal_val, f'Subtotal is "{db_subtotal}", should be "{subtotal_val}"'
	assert db_tax == tax_val,  f'Tax is "{db_tax}", should be "{tax_val}"'
	assert db_tip == tip_val,  f'Tip is "{db_tip}", should be "{tip_val}"'
	assert db_total == total_val ,  f'Total is "{db_total}", should be "{total_val}"' 




