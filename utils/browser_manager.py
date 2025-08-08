from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class BrowserManager:
	def __init__(self,browser_name = 'chrome'):
		self.browser_name = browser_name
		self.driver = None

	def start_browser(self):
		if self.browser_name == 'chrome':
			#self.driver = webdriver.Chrome()
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument("--start-maximized")
			chrome_options.add_argument("--log-level=3")
			service = Service(ChromeDriverManager().install())
			self.driver = webdriver.Chrome(service=service, options=chrome_options)
		elif self.browser_name == 'firefox':
			self.driver = webdriver.Firefox()
		else:
			print("error")	
		#self.driver.maximize_window()
		return self.driver

	def close_browser(self):
		if self.driver:
			self.driver.quit()




