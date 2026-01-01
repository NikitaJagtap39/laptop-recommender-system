import pandas as pd

# Replace with your CSV file path
csv_file = "dell_all_laptops.csv"

# Read CSV into a DataFrame
df = pd.read_csv(csv_file)

# Display the DataFrame
print(df)

# Optional: Display first 5 rows nicely
print(df.head())
