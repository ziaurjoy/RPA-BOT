import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

import mysql.connector

# first time error throw becouse db not created.So error handle
# if db all ready created so not throw error
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="amazonscriptingdb"
    )
except:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
    )

mycursor = mydb.cursor()

try:
    mycursor.execute("CREATE DATABASE amazonscriptingdb")
except:
    pass

try:
	mycursor.execute("CREATE TABLE product_collects(Id INT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(255), price VARCHAR(225), shipment VARCHAR(225), feature TEXT, image_url VARCHAR(225), update_status BOOLEAN DEFAULT false)")
except:
    pass

product_collects_sql = "INSERT INTO product_collects (title, price, shipment, feature, image_url, update_status) VALUES (%s, %s, %s, %s, %s, %s)"


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

	for i in range(5):
		search_key = input('Plese Input The Search key for Amazon : ')


		# this method working for searching key query result items and return all item links
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
					link = item.find_element(By.TAG_NAME, 'a').get_attribute("href")
					search_item_list.append(link)
				except NoSuchElementException:
					continue
			return search_item_list
		
		links = search_item_product_link(driver=driver, search_key=search_key)


		# this method view to product details page and collect data and save to database
		def product_information_save_db(driver, link):
			try:
				driver.set_page_load_timeout(300)
				driver.get(link)
			except:
				return True
			try:
				driver.implicitly_wait(1)
				title = driver.find_element(By.ID, "productTitle").text
			except NoSuchElementException:
				title = ''
			try:
				driver.implicitly_wait(1)
				price = driver.find_element(By.CLASS_NAME, "reinventPricePriceToPayMargin").text
			except NoSuchElementException:
				price = ''
			try:
				driver.implicitly_wait(1)
				shipment = driver.find_element(By.ID, "deliveryBlockContainer").text
			except NoSuchElementException:
				shipment = ''

			try:
				driver.implicitly_wait(1)
				feature = driver.find_element(By.ID, "featurebullets_feature_div").text
			except NoSuchElementException:
				feature = ''

			try:
				driver.implicitly_wait(1)
				image_div_element = driver.find_element(By.ID, "imgTagWrapperId")
				image_url = image_div_element.find_element(By.TAG_NAME, "img").get_attribute("src")
			except NoSuchElementException:
				image_url = ''
			if title != '':
				value_product_details = (title, price, shipment, feature, image_url, False)
				# execute sql query
				mycursor.execute(product_collects_sql, value_product_details)
				mydb.commit()  # push data for database table
				return int(mycursor.lastrowid)
			return True
		
		
		# this method work to query db to last save data in database and update value 
		def query_db_and_update(id):
			try:
				sql = f"SELECT * FROM product_collects WHERE id ={id}"
				mycursor.execute(sql)
				get_data = mycursor.fetchone()

				title = get_data[1]
				price = get_data[2]
				shipment = get_data[3]
				feature = get_data[4]
				image_url = get_data[5]
				update_status = True

				query_sql = "Update product_collects SET title=%s, price=%s, shipment=%s, feature=%s, image_url=%s, update_status=%s WHERE id=%s"
				mycursor.execute(query_sql, (title, price, shipment, feature, image_url, update_status, id))
				mydb.commit()
			except:
				pass


		for link in links:
			if type(link) == str: # some time link_list in None so type error becouse statwith not support None value
				if link.startswith('https://www.amazon.com/')==True and link.startswith('https://www.amazon.com/gp/help/')==False and link.startswith('https://www.amazon.com/s?k=')==False: # Only work item product details link
					id = product_information_save_db(driver, link) # this method save data in database and return this id or error return true
					if type(id) == int:
						query_db_and_update(id) # query item and update 
					else:
						continue
				else:
					continue
			else:
				continue

			
	print("All Data Save In DataBase Please Check Database")