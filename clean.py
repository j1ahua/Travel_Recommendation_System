import pandas as pd
import wikipedia
import csv

# Load your CSV
csv_path = "data/destinations.csv"
df = pd.read_csv(csv_path, encoding='latin1')

# Replace missing or empty descriptions
df["Description"] = df["Description"].fillna("").replace(r"^\s*$", "Description not found.", regex=True)
df["Description"] = df["Description"].apply(lambda x: x if isinstance(x, str) else "Description not found.")

# Save it back
df.to_csv("data/destinations.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL, quotechar='"')
print("All missing or empty descriptions filled with 'Description not found.'")