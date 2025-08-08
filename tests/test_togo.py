import pytest
import time
from pages.togo_page import TogoPage
from pages.ordering_page import OrderingPage
from pages.cart_page import CartPage
from database.get_mypos import GetMypos
from config import Config

@pytest.fixture(scope="module")
def login_togo(browser, login_page):
    username = login_page.login(Config.TEST_USERS['kwickpos']['username'], "cart")
    if username != "Login":
        login_page.set_login_status(True)
    else:
        login_page.set_login_status(False)
    return login_page.login_status

@pytest.fixture
def togo_setup(browser, login_togo):
    if not login_togo:
        pytest.fail("Login failed, cannot proceed with togo tests")
    
    togo_page = TogoPage(browser)
    if not togo_page.is_customer_page():
        togo_page.open_customer_page()
    
    togo_page.enter_customer_info()
    return togo_page

def test_togo_customer_info_entry(togo_setup):
    """Test that customer information can be entered successfully"""
    togo_page = togo_setup
    assert togo_page is not None, "TogoPage setup failed"

def test_togo_order_flow(browser, togo_setup):
    """Test complete togo order flow with item selection"""
    ordering_page = OrderingPage(browser)
    
    # Add a simple item to cart
    ordering_page.add_item_to_cart("00Regular", "1", "7")
    
    cart_page = CartPage(browser)
    time.sleep(0.5)
    
    # Verify item was added
    subtotal = cart_page.get_subtotal()
    assert subtotal > 0, "No items in cart"
    
    # Complete the order
    ordering_page.enter_order()
    
    # Verify order was created in database
    time.sleep(1)
    db = GetMypos()
    last_order = db.get_myorder("order by order_id desc limit 1")
    assert last_order is not None, "Order not found in database"
    assert float(last_order['food']) > 0, "Order total is 0"