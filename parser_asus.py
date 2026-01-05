import os
import re
import pandas as pd
from bs4 import BeautifulSoup

DATA_DIR = "data_asus"
OUTPUT_CSV = "asus_laptops_parsed.csv"

records = []

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

for file_name in os.listdir(DATA_DIR):
    if not file_name.lower().endswith(".html"):
        continue

    file_path = os.path.join(DATA_DIR, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    laptop = {}

    # ---------------------------------
    # 1. Laptop name from filename
    # ---------------------------------
    laptop_name = os.path.splitext(file_name)[0]
    laptop["title"] = laptop_name

    # ---------------------------------
    # 2. Price (if present)
    # ---------------------------------
    full_text = soup.get_text(" ", strip=True)
    price_match = re.search(r"\$[\d,]+\.\d{2}", full_text)
    laptop["price_usd"] = price_match.group() if price_match else None

    # ---------------------------------
    # 3. Parse all <b>Spec:</b> Value
    # ---------------------------------
    for b_tag in soup.find_all("b"):
        key = clean_text(b_tag.text.replace(":", ""))

        value_parts = []
        for elem in b_tag.next_siblings:
            if getattr(elem, "name", None) == "br":
                break
            if isinstance(elem, str):
                value_parts.append(elem)

        value = clean_text(" ".join(value_parts))

        if key and value:
            laptop[key] = value

    records.append(laptop)

print(f"Parsed {len(records)} ASUS laptops")

# ---------------------------------
# Convert to DataFrame
# ---------------------------------
df = pd.DataFrame(records)

# ---------------------------------
# Optional: reorder key columns
# ---------------------------------
priority_cols = [
    "title",
    "price_usd",
    "Model",
    "Processor",
    "Graphics",
    "Memory",
    "Storage",
    "Display",
    "Operating System",
    "Battery",
    "Weight"
]

df = df[[c for c in priority_cols if c in df.columns] +
        [c for c in df.columns if c not in priority_cols]]

# ---------------------------------
# Save
# ---------------------------------
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved to {OUTPUT_CSV}")
