import pytest
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

ORDER_TYPE = "walkin"

@pytest.fixture(scope="module")
def login(browser,login_page):
	if ORDER_TYPE == "dinein":
		username = login_page.login(Config.TEST_USERS['kwickpos']['username'])
	else:
		username = login_page.login(Config.TEST_USERS['kwickpos']['username'],"cart")
	#check if log in succeeds
	if username != "Login":
		login_page.set_login_status(True)
	else:
		login_page.set_login_status(False)
	return login_page.login_status

@pytest.fixture
def ordering(browser, login):
	#time.sleep(1)
	if not login:
		pytest.fail("Login failed, cannot proceed with ordering")

	#refresh to apply updates of db settings before ordering
	time.sleep(0.5)
	base_page = BasePage(browser)
	reload_btn = base_page.find_element(*(By.ID, "kwickhelp"))
	browser.execute_script("arguments[0].click();", reload_btn)
	#base_page.find_element(*(By.ID, "kwickhelp")).click()
	time.sleep(0.5)

	#hard coded for now, need to automatically get it later
	if ORDER_TYPE == "dinein":
		dinein_page = DineinPage(browser)
		dinein_page.select_table(1) 
		dinein_page.select_guest(1)
		return dinein_page
	elif ORDER_TYPE == "walkin":
		togo_page = TogoPage(browser)
		#make sure the customerinfo page is open before entering cinfo
		if not togo_page.is_customer_page():
			togo_page.open_customer_page()		
		#enter customerinfo
		togo_page.enter_customer_info()
		return togo_page

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
	time.sleep(0.5)
	cart_discount = cart_page.get_discount()
	cart_subtotal = cart_page.get_subtotal()
	cart_tax = cart_page.get_tax()
	cart_tip = cart_page.get_tip()
	cart_total = cart_page.get_total()
	


	#Enter Order
	ordering_page.enter_order()

	#assert error
	#print(setup_settings)
	#Cart == Formula
	assert cart_discount == disc_val, f'Discount is "{cart_discount}", should be "{disc_val}"'
	assert cart_subtotal == subtotal_val, f'Subtotal is "{cart_subtotal}", should be "{subtotal_val}"'
	assert cart_tax == tax_val,  f'Tax is "{cart_tax}", should be "{tax_val}"'
	assert cart_tip == tip_val,  f'Tip is "{cart_tip}", should be "{tip_val}"'
	assert cart_total == total_val,  f'Total is "{cart_total}", should be "{total_val}"'


	#=============check database==============
	time.sleep(1)
	db = GetMypos(serverip)
	last_order = db.get_myorder("order by order_id desc limit 1")
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




