import pandas as pd
import requests
import time

# Your TripAdvisor API key and details endpoint
API_KEY = "73C769C061084D5897E90895E9D2C0B0"
DETAILS_URL_TEMPLATE = "https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"

def fetch_location_details(location_id, retry_attempts=3):
    """
    Fetch location details for a given location_id with retry mechanism.
    Returns the details JSON if successful, otherwise an empty dict.
    """
    url = DETAILS_URL_TEMPLATE.format(location_id=location_id)
    params = {"key": API_KEY, "language": "en"}
    headers = {"accept": "application/json"}
    
    for attempt in range(retry_attempts):
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"429 Error for {location_id} on attempt {attempt+1}. Retrying...")
            time.sleep(2 ** (attempt + 1))  # Exponential backoff
        else:
            print(f"Details Error for {location_id}: {response.status_code}, {response.text}")
            break
    return {}

def update_missing_details(csv_path):
    """
    Reads the CSV file, identifies rows that are missing all required details,
    updates those rows by fetching location details, and writes back to CSV.
    """
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_path)
    
    # List of required columns we want to update if they're all missing
    required_columns = ['latitude', 'longitude', 'rating', 'num_reviews', 'price_level', 'category']
    
    # Ensure all required columns exist; if not, create them with default value None
    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    # Identify rows where all required columns are missing
    missing_mask = (
        df['latitude'].isnull() & 
        df['longitude'].isnull() & 
        df['rating'].isnull() & 
        df['num_reviews'].isnull() & 
        df['price_level'].isnull() & 
        df['category'].isnull()
    )
    num_missing = missing_mask.sum()
    print(f"Found {num_missing} rows with all required details missing.")
    
    # Process each row that is missing all required columns
    for i in range(1):  #remove after testing
        
        for index, row in df[missing_mask].iterrows():
            location_id = row['location_id']
            print(f"Updating location {location_id} at index {index}...")
            details = fetch_location_details(location_id)
            if details:
                for col in required_columns:
                    df.at[index, col] = details.get(col)
                print(f"Location {location_id} updated successfully.")
            else:
                print(f"Failed to update location {location_id}.")
            time.sleep(1)  # Delay between detail requests to avoid rate limits
    
    # Write the updated DataFrame back to CSV
    df.to_csv(csv_path, index=False)
    print("CSV file updated.")

# Specify the path to your CSV file
csv_path = "data/tripadvisor_europe_nearby_destinations.csv"

# Call the function to update missing details
update_missing_details(csv_path)