# Necessary Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import random

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Search query
query = "laptops"

# Create the data folder
data_folder = os.path.join(os.getcwd(), "data")
os.makedirs(data_folder, exist_ok=True)

products = []

# Loop through multiple pages (e.g., first 10 pages)
for page in range(1, 5):
    driver.get(f"https://www.dell.com/en-us/shop/scc/scr/{query}?page={page}")
    time.sleep(random.uniform(2, 4))  # random delay to mimic human behavior

    # Find all laptop title elements on this page
    title_elems = driver.find_elements(By.CLASS_NAME, "ps-title")
    print(f"Page {page}: {len(title_elems)} items found")

    # Extract URL and title HTML for each laptop
    for elem in title_elems:
        link_elem = elem.find_element(By.TAG_NAME, "a")
        url = link_elem.get_attribute("href")
        if url.startswith("//"):
            url = "https:" + url
        title_html = elem.get_attribute("outerHTML")
        products.append((url, title_html))

# Visit each laptop page and save specs
for i, (url, title_html) in enumerate(products, start=1):
    driver.get(url)
    time.sleep(random.uniform(2, 4))  # random delay to avoid blocks

    try:
        specs_elem = driver.find_element(By.CSS_SELECTOR, ".specs.list-unstyled")
        specs_html = specs_elem.get_attribute("outerHTML")
    except:
        specs_html = "No specs available"

    # Write both title and specs HTML to a file
    file_path = os.path.join(data_folder, f"laptop{i}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("<h2>Title HTML</h2>\n")
        f.write(title_html + "\n\n")
        f.write("<h2>Specs HTML</h2>\n")
        f.write(specs_html)

    print(f"Saved laptop {i} to {file_path}")

driver.close()
