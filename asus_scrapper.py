from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

# Initialize Chrome Driver
driver = webdriver.Chrome()

# Search query
query = "laptops"
driver.get(f"https://www.asus.com/us/{query}/all-products/")
time.sleep(3)

# Create the data folder
data_folder = os.path.join(os.getcwd(), "data_asus")
os.makedirs(data_folder, exist_ok=True)

# Scroll to load all laptops
last_count = 0
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    title_elems = driver.find_elements("xpath", "//a[contains(@class,'headingRow')]")
    current_count = len(title_elems)
    print(f"Laptops loaded so far: {current_count}")

    if current_count == last_count:
        print("All laptops loaded.")
        break
    last_count = current_count

# Collect unique laptop URLs
products = []
seen_urls = set()
for elem in title_elems:
    title = elem.text.strip()
    pdp_url = elem.get_attribute("href")
    
    # Convert ROG laptops to proper spec URL
    if "rog-strix" in pdp_url:
        pdp_url = pdp_url.rstrip("/") + "/spec/"
    else:
        pdp_url = pdp_url.rstrip("/") + "/techspec/"
    
    if pdp_url not in seen_urls:
        products.append((title, pdp_url))
        seen_urls.add(pdp_url)

print(f"Total unique laptops found: {len(products)}")

# Scrape tech specs
for i, (title, pdp_url) in enumerate(products, start=1):
    try:
        driver.get(pdp_url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Wait for spec rows to appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.TechSpec__rowTable__1LR9D, div.SpecSection__row__2ob1N"))
        )

        specs_html = ""
        
        # Try both Asus and ROG row selectors
        rows = driver.find_elements("css selector", "div.TechSpec__rowTable__1LR9D, div.SpecSection__row__2ob1N")
        for row in rows:
            try:
                spec_title = row.find_element("css selector", ".rowTableTitle, .SpecSection__label__27zS1").text.strip()
            except:
                spec_title = ""
            
            try:
                spec_value = row.find_element(
                    "css selector", ".TechSpec__rowTableItems__KYWXp:not(.TechSpec__rowImage__35vd6), .SpecSection__value__3Yr6g"
                ).text.strip()
            except:
                spec_value = ""
            
            if spec_title or spec_value:
                specs_html += f"<b>{spec_title}:</b> {spec_value}<br><br>\n"

        # Save to HTML
        safe_title = "".join(c if c.isalnum() else "_" for c in title)
        file_path = os.path.join(data_folder, f"asus_{i}_{safe_title}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"<h2>{title}</h2>\n")
            f.write(specs_html)

        print(f"Saved {i}: {title}")

    except Exception as e:
        print(f"Failed to scrape {title}: {e}")
        continue

driver.quit()
print("Scraping complete!")
