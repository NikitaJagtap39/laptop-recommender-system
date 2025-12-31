# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import random

# Initializing the Chrome Driver
driver = webdriver.Chrome()

# Search query
query = "laptops"
driver.get(f"https://www.asus.com/us/{query}/all-products/")

# Create the data folder
data_folder = os.path.join(os.getcwd(), "data_asus")
os.makedirs(data_folder, exist_ok=True)

# Scroll until all laptops are loaded
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("Finished scrolling")

# Extract product URLs and titles
products = []

title_elems = driver.find_elements(By.TAG_NAME, "h2")
print(f"Total laptops found: {len(title_elems)}")

for elem in title_elems:
    try:
        title_html = elem.get_attribute("outerHTML")
        
        # Navigate up to the <a> tag to get the product page
        link_elem = elem.find_element(By.XPATH, "./ancestor::a")
        product_url = link_elem.get_attribute("href")
        
        if product_url:
            products.append((product_url, title_html))
    except:
        continue

# Visiting individual tech specs pages and saving
for i, (product_url, title_html) in enumerate(products, start=1):
    driver.get(product_url)
    time.sleep(random.uniform(3, 5))
    
    specs_html = ""
    
    # Detect layout type
    techspec_rows = driver.find_elements(By.CLASS_NAME, "TechSpec__rowTable__1LR9D")
    productspec_rows = driver.find_elements(By.CLASS_NAME, "ProductSpec__row__wSwCC")
    
    if techspec_rows:
        # TechSpec layout
        for row in techspec_rows:
            try:
                title = row.find_element(By.CLASS_NAME, "rowTableTitle").text
                value = row.find_element(By.CLASS_NAME, "TechSpec__rowTableItems__KYWXp").text
                specs_html += f"<p><b>{title}</b>: {value}</p>\n"
            except:
                continue
    elif productspec_rows:
        # ProductSpec layout
        for row in productspec_rows:
            try:
                title = row.find_element(By.CLASS_NAME, "ProductSpec__productSpecItemTitle__JVvSd").text
                values = [span.text for span in row.find_elements(By.CSS_SELECTOR, ".ProductSpec__rowDescriptionItem__FIUcR span") if span.text.strip()]
                specs_html += f"<p><b>{title}</b>: {', '.join(values)}</p>\n"
            except:
                continue
    else:
        specs_html = "No techspecs found"

    # Save to file
    file_path = os.path.join(data_folder, f"asus_laptop_{i}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("<h2>Title</h2>\n")
        f.write(title_html + "\n\n")
        f.write("<h2>Tech Specs</h2>\n")
        f.write(specs_html)

    print(f"Saved ASUS laptop {i} to {file_path}")

driver.quit()
