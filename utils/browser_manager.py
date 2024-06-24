from selenium import webdriver 

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
			self.driver = webdriver.Chrome(options=chrome_options)
		elif self.browser_name == 'firefox':
			self.driver = webdriver.Firefox()
		else:
			print("error")	
		#self.driver.maximize_window()
		return self.driver

	def close_browser(self):
		if self.driver:
			self.driver.quit()




