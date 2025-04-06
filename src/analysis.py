import pandas as pd

def aggregate_by_country(df: pd.DataFrame) -> pd.Series:
    """
    Group data by country and calculate the total annual tourist counts per country.
    """
    avg_tourists_by_countries = df.groupby("Country")["Approximate Annual Tourists(million)"].sum()
    return avg_tourists_by_countries