from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

# ----------------------------
# Setup
# ----------------------------
driver = webdriver.Chrome()
query = "laptops"
driver.get(f"https://www.lenovo.com/us/en/{query}/results/")

# Wait for laptop links to appear
time.sleep(3)
title_elem = driver.find_element(By.XPATH, "//a[starts-with(@id, 'pc-title_')]")
title = title_elem.text.strip()
pdp_url = title_elem.get_attribute("href")
print(f"Laptop found: {title}")
print(f"PDP URL: {pdp_url}")

# ----------------------------
# Visit PDP + scrape tech specs
# ----------------------------
tech_url = pdp_url + "#tech_specs"
driver.get(tech_url)

# Wait for specs to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".specs-wrapper-box"))
)

# Collect all spec wrappers
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

# ----------------------------
# Save to HTML file
# ----------------------------
data_folder = os.path.join(os.getcwd(), "data_lenovo")
os.makedirs(data_folder, exist_ok=True)

file_path = os.path.join(data_folder, "lenovo_first_laptop.html")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(f"<h2>{title}</h2>\n")
    f.write(specs_html)

print(f"Tech specs saved to: {file_path}")

driver.quit()
