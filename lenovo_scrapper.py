#Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

#Initializing Chrome Driver
driver = webdriver.Chrome()

#Search query
query = "laptops"
driver.get(f"https://www.lenovo.com/us/en/{query}/results/")
time.sleep(3)

#Create the data folder
data_folder = os.path.join(os.getcwd(), "data_lenovo")
os.makedirs(data_folder, exist_ok=True)

#Click "Load more results" until all laptops are loaded
last_count = 0
while True:
    
    # Scroll to bottom to trigger lazy-loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # wait for lazy-load

    try:
        # Try clicking "Load more results" button
        load_more_btn = driver.find_element(By.CSS_SELECTOR, "button.pc_more")
        driver.execute_script("arguments[0].click();", load_more_btn)
        print("Clicked 'Load more results'...")
        time.sleep(2)  # wait for more results to load
    except:
        pass

    #Collecting all laptop links
    title_elems = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'pc-title_')]")
    print(f"Total laptops found: {len(title_elems)}")

    # Count current laptops loaded in DOM
    title_elems = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'pc-title_')]")
    current_count = len(title_elems)
    print(f"Laptops loaded so far: {current_count}")

    # Stop if no new laptops are loaded
    if current_count == last_count:
        print("All laptops loaded.")
        break
    last_count = current_count

products = []
seen_urls = set()
for elem in title_elems:
    title = elem.text.strip()
    pdp_url = elem.get_attribute("href")
    if pdp_url not in seen_urls:
        products.append((title, pdp_url))
        seen_urls.add(pdp_url)

print(f"Total unique laptops found: {len(products)}")


#Visiting each PDP to scrape tech specs
for i, (title, pdp_url) in enumerate(products, start=1):
    try:
        tech_url = pdp_url + "#tech_specs"
        driver.get(tech_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".specs-wrapper-box"))
        )

        wrappers = driver.find_elements(By.CSS_SELECTOR, ".specs-wrapper-box .specs-wrapper")
        specs_html = ""
        for wrapper in wrappers:
            section_name = wrapper.find_element(By.CSS_SELECTOR, ".group-headline").text
            specs_html += f"<h3>{section_name}</h3>\n"

            items = wrapper.find_elements(By.CSS_SELECTOR, ".specs-table .item")
            for item in items:
                spec_name = item.find_element(By.CSS_SELECTOR, ".specs-table-th .spec-title").text
                spec_value = item.find_element(By.CSS_SELECTOR, ".specs-table-td").get_attribute("outerHTML")
                specs_html += f"<b>{spec_name}:</b> {spec_value}<br><br>\n"

        safe_title = "".join(c if c.isalnum() else "_" for c in title)
        file_path = os.path.join(data_folder, f"lenovo_{i}_{safe_title}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"<h2>{title}</h2>\n")
            f.write(specs_html)

        print(f"Saved {i}: {title}")

    except Exception as e:
        print(f"Failed to scrape {title}: {e}")
        continue

driver.quit()
print("Scraping complete!")
