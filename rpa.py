import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver


class RPA:
	# this code useing without open browser
	# ====================================
	# chromeoption = Options()
	# chromeoption.add_argument('--headless')
	# driver = webdriver.Chrome(options=chromeoption)

	# input searching key and open browser

	option = webdriver.ChromeOptions()
	option.add_argument("--incognito")
	driver = webdriver.Chrome(options=option)
	driver.set_window_size(1200, 800)
	driver.delete_all_cookies()
	time.sleep(10)

	for i in range(5):
		search_key = input('search : ')
		driver.set_page_load_timeout(300)
		driver.get('https://www.amazon.com/')
		time.sleep(2)
		search_input_element = driver.find_element(By.ID, 'twotabsearchtextbox')

		search_input_element.send_keys(search_key)
		time.sleep(0.2)
		driver.implicitly_wait(5000)
		# Exactly Same key search.don't use recommend key for amazon
		search_input_element.send_keys(Keys.ENTER)
		time.sleep(10)
	input('break')