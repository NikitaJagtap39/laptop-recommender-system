import os
import re
import pandas as pd
from bs4 import BeautifulSoup


# -------------------------
# Clean text helper
# -------------------------
def clean_text(text):
    if not text:
        return None
    text = re.sub(r'\[\d+\]', '', text)   # remove [1], [24], etc
    text = re.sub(r'\s+', ' ', text)      # normalize spaces
    return text.strip()


# -------------------------
# Parse ONE HP laptop HTML
# -------------------------
def parse_hp_laptop(html):
    soup = BeautifulSoup(html, "lxml")
    laptop = {}

    # ---- Title ----
    title_tag = soup.find("h3", class_="Wb-t_gh")
    if title_tag:
        laptop["Title"] = clean_text(title_tag.get_text())

    # ---- Technical Specifications ----
    spec_blocks = soup.find_all(
        "div",
        attrs={"data-test-hook": "@hpstellar/pdp/tech-specs__detailedSpec"}
    )

    for block in spec_blocks:
        key_tag = block.find("p")
        if not key_tag:
            continue

        key = clean_text(key_tag.get_text())

        value_tags = block.find_all("span", class_="cust-html")
        if not value_tags:
            continue

        value = clean_text(value_tags[-1].get_text(" ", strip=True))

        if key and value:
            laptop[key] = value

    return laptop


# -------------------------
# MAIN FUNCTION
# -------------------------
def main():
    html_folder = r"D:\Laptop Recommendation Project\data_hp"
    output_csv = r"D:\Laptop Recommendation Project\hp_laptops.csv"

    all_laptops = []

    for file_name in os.listdir(html_folder):
        if not file_name.lower().endswith(".html"):
            continue

        file_path = os.path.join(html_folder, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        laptop_data = parse_hp_laptop(html)
        laptop_data["SourceFile"] = file_name  # optional
        all_laptops.append(laptop_data)

    # Convert to DataFrame
    df = pd.DataFrame(all_laptops)

    # Save CSV
    df.to_csv(output_csv, index=False)

    print(f"✅ Parsed {len(df)} HP laptops")
    print(f"📁 CSV saved at: {output_csv}")


# -------------------------
# Run script
# -------------------------
if __name__ == "__main__":
    main()
