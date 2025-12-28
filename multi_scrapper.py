#All the necessary libraries are imported
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()

#Opening the Dell laptops main listing page
query = "laptops"
driver.get(f"https://www.dell.com/en-us/shop/scc/scr/{query}")
time.sleep(2)

#Finding the elements which have laptop titles and count how many laptops were found
title_elems = driver.find_elements(By.CLASS_NAME, "ps-title")
print(f"{len(title_elems)} items found")

#Creating the data folder
data_folder = os.path.join(os.getcwd(), "data")
os.makedirs(data_folder, exist_ok=True)

#Extracting URL for each laptop for the title element
products = []
for elem in title_elems:
    link_elem = elem.find_element(By.TAG_NAME, "a")
    url = link_elem.get_attribute("href")
    if url.startswith("//"):
        url = "https:" + url
    title_html = elem.get_attribute("outerHTML")
    products.append((url, title_html))

#Visting each laptop's page and saving specs
for i, (url,title_html) in enumerate(products, start=1):
    driver.get(url)
    time.sleep(2)

    try:
        specs_elem = driver.find_element(By.CSS_SELECTOR, ".specs.list-unstyled")
        specs_html = specs_elem.get_attribute("outerHTML")

    except:
        specs_html = "No specs available"

    #Write both to a file
    file_path = os.path.join(data_folder,f"laptop{i}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("<h2>Title HTML</h2>\n")
        f.write(title_html + "\n\n")
        f.write("<h2>Specs HTML</h2>\n")
        f.write(specs_html)

    print(f"Saved laptop {i} to {file_path}")

driver.close()


