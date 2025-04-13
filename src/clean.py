import pandas as pd
import csv

def clean_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace missing or empty descriptions with a default message.
    """
    df["Description"] = df["Description"].fillna("").replace(r"^\s*$", "Description not found.", regex=True)
    df["Description"] = df["Description"].apply(lambda x: x if isinstance(x, str) else "Description not found.")
    return df

def parse_tourist_count(value) -> float:
    """
    Convert a tourist count value from a string to a float (in millions).

    Handles cases like:
      - "500,000" -> 0.5 (raw number converted to millions)
      - "35 million" -> 35
      - "35-40 million" -> average of 35 and 40 (i.e., 37.5)

    If the string includes "million", it is assumed the number is already in millions.
    If not, the raw number is divided by 1e6.

    Returns None if conversion fails.
    """
    if isinstance(value, (int, float)):
        return value
    

    if pd.isna(value):
        return None

    # Convert value to a clean string and remove commas
    s = str(value).lower().strip().replace(',', '')

    if "million" in s:
        s = s.replace("million", "").strip()
        if '-' in s:
            parts = s.split('-')
            try:
                nums = [float(part.strip()) for part in parts if part.strip()]
                return sum(nums) / len(nums)
            except ValueError:
                return None
        else:
            try:
                return float(s)
            except ValueError:
                return None
    else:
        if '-' in s:
            parts = s.split('-')
            try:
                nums = [float(part.strip()) for part in parts if part.strip()]
                raw = sum(nums) / len(nums)
            except ValueError:
                return None
        else:
            try:
                raw = float(s)
            except ValueError:
                return None
        return raw / 1e6

def clean_approx_annual_tourists(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and convert the 'Approximate Annual Tourists' column from a string to a float in millions.
    """
    column_name = "Approximate Annual Tourists"
    if column_name in df.columns:
        df[column_name] = df[column_name].apply(parse_tourist_count)
    df.rename(columns={column_name: 'Approximate Annual Tourists(million)'},inplace = False)

    return df

def check_duplicates(df: pd.DataFrame):
    """
    Identify and print duplicate rows in the DataFrame.
    """
    duplicates = df.duplicated()
    print("Duplicate rows:")
    print(duplicates)

def main():
    csv_path = "data/destinations.csv"
    
    # Load the CSV file with the appropriate encoding
    df = pd.read_csv(csv_path, encoding='utf-8')
    original_df = df.copy()
    
    # Clean descriptions and annual tourist counts
    df = clean_descriptions(df)
    df = clean_approx_annual_tourists(df)
    
    # Save the cleaned DataFrame back to CSV
    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL,
        quotechar='"'
    )
    print("All missing or empty descriptions have been replaced with 'Description not found.'")
    
    # Check for duplicate rows
    check_duplicates(df)

if __name__ == '__main__':
    main()