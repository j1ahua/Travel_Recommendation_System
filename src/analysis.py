import pandas as pd

def aggregate_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group data by country and calculate the total annual tourist counts per country.
    """
    country_summary = df.groupby('country')['annual_tourist_count'].sum().reset_index()
    return country_summary