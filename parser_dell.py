import os
from bs4 import BeautifulSoup
import pandas as pd

# Folder containing all 64 HTML files
dell_html_folder = r"D:\Laptop Recommendation Project\data"

# List to hold all laptops data
all_laptops = []

# Loop through all HTML files
for filename in os.listdir(dell_html_folder):
    if filename.endswith(".html"):
        filepath = os.path.join(dell_html_folder, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Extract laptop name
        name_tag = soup.select_one("h3.ps-title a")
        name = name_tag.text.strip() if name_tag else "N/A"

        # Extract specs
        specs_list = soup.select("ul.specs li")
        specs_dict = {}
        for li in specs_list:
            key_tag = li.find("div", class_="h5 font-weight-bold mb-0")
            value_tag = li.find("p")
            if key_tag and value_tag:
                key = key_tag.text.strip()
                value = value_tag.text.strip()
                specs_dict[key] = value

        # Normalize keys to consistent CSV columns
        normalized_keys = {
            "Processor": "Processor",
            "Operating System": "OS",
            "Graphics Card": "Graphics",
            "Memory": "RAM",
            "Storage": "Storage",
            "Weight": "Weight",
            "Display": "Display",
            "Keyboard": "Keyboard",
            "Ports": "Ports",
            "Camera": "Camera",
            "Battery": "Battery",
            "Touchpad": "Touchpad"
        }

        data = {"Name": name}
        for k, v in normalized_keys.items():
            data[v] = specs_dict.get(k, "")

        # Append to list
        all_laptops.append(data)

# Create DataFrame
df = pd.DataFrame(all_laptops)

# Save all laptops to a single CSV
df.to_csv("dell_all_laptops.csv", index=False, encoding="utf-8")
print(f"Saved {len(df)} laptops to dell_all_laptops.csv")
