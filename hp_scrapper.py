#Importing Necessary Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os 
import random

#Intializing the Chrome Driver
driver = webdriver.Chrome()

#Search query
query = "laptops"
driver.get(f"https://www.hp.com/us-en/shop/vwa/{query}")

# Create the data folder
data_folder = os.path.join(os.getcwd(), "data_hp")
os.makedirs(data_folder, exist_ok=True)

#Clicking "LOAD MORE" until all pages are covered
while True:
    try:
        load_more = driver.find_element(
            By.XPATH, "//span[normalize-space()='Load more']"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", load_more)
        time.sleep(random.uniform(2, 4))
        print("Clicked Load more")
    except:
        print("No Load More available")
        break

#Finding all laptop titles
title_elems = driver.find_elements(By.CLASS_NAME, "Wb-t_gh")
print(f"Total laptops found: {len(title_elems)}")

products = []

for elem in title_elems:
    try:
        # Title HTML
        title_html = elem.get_attribute("outerHTML")

        # Product URL is in parent <a>
        parent_link = elem.find_element(By.XPATH, "./ancestor::a")
        url = parent_link.get_attribute("href")

        products.append((url, title_html))
    except:
        continue

#Visit all laptop pages and save html
for i, (url, title_html) in enumerate(products, start=1):
    driver.get(url)
    time.sleep(random.uniform(3, 5))

    specs_html = ""

    try:
        spec_blocks = driver.find_elements(
            By.XPATH,
            "//div[@data-test-hook='@hpstellar/pdp/tech-specs__detailedSpec']"
        )

        for block in spec_blocks:
            specs_html += block.get_attribute("outerHTML") + "\n"

    except:
        specs_html = "No specs found"

    #Saving the HTML
    file_path = os.path.join(data_folder, f"hp_laptop_{i}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("<h2>Title</h2>\n")
        f.write(title_html + "\n\n")
        f.write("<h2>Technical Specifications</h2>\n")
        f.write(specs_html)

    print(f"Saved HP laptop {i}")

driver.quit()
