import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class PosTest(unittest.TestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    #todo
    #if logged in, need to log out first
    def test_login_seatlogin(self):
        driver = self.driver
        driver.get("http://192.168.7.54")
        #find login button (seat page)
        btn_login = driver.find_element(By.ID, "seatlogin")
        btn_login.click()
        #enter password 3309
        element = driver.find_element(By.ID, "loginp")
        element.send_keys("3309")
        #click submit button to log in
        btn_submit = driver.find_element(By.ID, "loginSubmit")
        btn_submit.click()

        TABLE_SELECTOR = f'a[seat="3"]'
        TABLE_ID = (By.CSS_SELECTOR,TABLE_SELECTOR)
        element = driver.find_element(*TABLE_ID)
        element.click()

        time.sleep(60)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

