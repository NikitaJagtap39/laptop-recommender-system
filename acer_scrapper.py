# Importing Necessary Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

# Initialize Chrome driver
driver = webdriver.Chrome()
driver.get("https://www.acer.com/us-en/laptops")

# Create data folder
data_folder = os.path.join(os.getcwd(), "data_acer")
os.makedirs(data_folder, exist_ok=True)

# -------------------------------
# STEP 1: WAIT FOR LAPTOP LINKS
# -------------------------------
try:
    laptop_links = WebDriverWait(driver, 25).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//a[.//p[contains(@class,'agw-card-title')]]")
        )
    )
except:
    print("Laptop cards did not load.")
    driver.quit()
    exit()

print(f"Total laptops found: {len(laptop_links)}")

# Store title + URL
products = []

for link in laptop_links:
    try:
        title = link.find_element(
            By.XPATH, ".//p[contains(@class,'agw-card-title')]"
        ).text.strip()

        url = link.get_attribute("href")
        if url.startswith("/"):
            url = "https://www.acer.com" + url

        products.append((title, url))
    except:
        continue

# -----------------------------------
# STEP 2: VISIT PDP + TECH SPECS
# -----------------------------------
for i, (title, pdp_url) in enumerate(products, start=1):
    try:
        specs_url = pdp_url + "#pdpSpecs"
        driver.get(specs_url)

        # Wait for specs tables
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-tabcontainerindex='1']//table")
            )
        )

        # Collect all spec tables HTML
        tables = driver.find_elements(
            By.XPATH,
            "//div[@data-tabcontainerindex='1']//table[contains(@class,'agw-table_techSpec')]"
        )

        specs_html = ""
        for table in tables:
            specs_html += table.get_attribute("outerHTML") + "\n\n"

        # Save HTML file
        file_path = os.path.join(data_folder, f"acer_laptop_{i}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("<h2>Title</h2>\n")
            f.write(f"<p>{title}</p>\n\n")
            f.write("<h2>Technical Specifications</h2>\n")
            f.write(specs_html)

        print(f"Saved {i}: {title}")

    except Exception as e:
        print(f"Failed on {title}: {e}")
        continue

driver.quit()
print("Scraping complete!")