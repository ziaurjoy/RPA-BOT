import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # for suppressing the browser


class RPA:
	# this code useing without open browser
	# ====================================
	# chromeoption = Options()
	# chromeoption.add_argument('--headless')
	# driver = webdriver.Chrome(options=chromeoption)
	# driver.delete_all_cookies()
	

	# input searching key and open browser

	option = webdriver.ChromeOptions()
	option.add_argument("--incognito")
	driver = webdriver.Chrome(options=option)
	driver.set_window_size(1200, 800)
	driver.delete_all_cookies()
	driver.set_page_load_timeout(300)
	driver.get('https://www.amazon.com/')
	time.sleep(3)

	for i in range(2):
		search_key = input('Plese Input The Search key for Amazon : ')
		def search_item_product_link(driver, search_key):
			search_input_element = driver.find_element(By.ID, 'twotabsearchtextbox')
			search_input_element.clear()
			search_input_element.send_keys(search_key)
			time.sleep(0.2)
			driver.implicitly_wait(5000)
			# Exactly Same key search.don't use recommend key for amazon
			search_input_element.send_keys(Keys.ENTER)
			time.sleep(5)
			# select all item for query result
			search_items = driver.find_elements(By.CLASS_NAME, 's-result-item')
			search_item_list = []  # search all item links append this list

			for item in search_items:
				try:
					driver.implicitly_wait(1)
					link = item.find_element(
						By.TAG_NAME, 'a').get_attribute("href")
					search_item_list.append(link)
				except NoSuchElementException:
					continue
			return search_item_list
		links = search_item_product_link(driver=driver, search_key=search_key)
		print('==================================================')
		print(links)
		print('==================================================')
			
	input('break')