import pandas as pd
import matplotlib.pyplot as plt
import analysis

def load_data(csv_path: str, encoding: str = "utf-8") -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Parameters:
        csv_path (str): Path to the CSV file.
        encoding (str): File encoding (default is "utf-8").
        
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    return pd.read_csv(csv_path, encoding=encoding)

def plot_tourist_distribution(country_tourists: pd.Series) -> None:
    """
    Plot a bar chart for the distribution of tourists by country.
    
    Parameters:
        country_tourists (pd.Series): Aggregated tourist counts by country.
    """
    plt.figure(figsize=(12, 6))
    country_tourists.sort_values(ascending=False).plot(kind='bar')
    plt.xlabel("Country")
    plt.ylabel("Total Tourists (in millions)")
    plt.title("Distribution of Tourists in Different Countries")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def main():
    # Define the path to your cleaned CSV file
    csv_path = "data/destinations_cleaned.csv"
    
    # Load the data
    df = load_data(csv_path)
    
    # Aggregate the tourist counts by country
    country_tourists = analysis.aggregate_by_country(df)
    
    # Plot the distribution of tourists by country
    plot_tourist_distribution(country_tourists)

if __name__ == '__main__':
    main()