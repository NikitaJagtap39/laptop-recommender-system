from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
query = "laptops"
driver.get(f"https://www.dell.com/en-us/shop/scc/scr/{query}")
time.sleep(2)

#Finding the laptop title in the class along with the URL
title_elem = driver.find_element(By.CLASS_NAME, "ps-title")
print(title_elem.get_attribute("outerHTML"))

# Searching inside the ps-title element, not the whole page
link_elem = title_elem.find_element(By.TAG_NAME, "a")

#Extracting the product URL and storing it as a python string
product_url = link_elem.get_attribute("href")

# // means 'use current protocol' but python needs full URL
if product_url.startswith("//"):
    product_url = "https:" + product_url

#Browser navigates to ONE laptop's page
driver.get(product_url)
time.sleep(2)

# CSS selector helps in extracting multiple classes 
specs_elem = driver.find_element(By.CSS_SELECTOR, ".specs.list-unstyled")

#Extracting specs
print(specs_elem.get_attribute("outerHTML"))


driver.close()
