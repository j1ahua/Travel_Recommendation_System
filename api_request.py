import requests
import random
import pandas as pd
import time
import os

# Your TripAdvisor API key
API_KEY = "73C769C061084D5897E90895E9D2C0B0"

# Base URLs for TripAdvisor API endpoints
SEARCH_URL = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"
DETAILS_URL_TEMPLATE = "https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"

# Comprehensive list of European cities with approximate coordinates
EUROPEAN_CITIES = [
    {"city": "Paris", "latitude": 48.8566, "longitude": 2.3522},
    {"city": "London", "latitude": 51.5074, "longitude": -0.1278},
    {"city": "Rome", "latitude": 41.9028, "longitude": 12.4964},
    {"city": "Berlin", "latitude": 52.5200, "longitude": 13.4050},
    {"city": "Madrid", "latitude": 40.4168, "longitude": -3.7038},
    {"city": "Vienna", "latitude": 48.2082, "longitude": 16.3738},
    {"city": "Prague", "latitude": 50.0755, "longitude": 14.4378},
    {"city": "Barcelona", "latitude": 41.3851, "longitude": 2.1734},
    {"city": "Amsterdam", "latitude": 52.3676, "longitude": 4.9041},
    {"city": "Moscow", "latitude": 55.7558, "longitude": 37.6173},
    {"city": "Istanbul", "latitude": 41.0082, "longitude": 28.9784},  # partly in Europe
    {"city": "Lisbon", "latitude": 38.7223, "longitude": -9.1393},
    {"city": "Budapest", "latitude": 47.4979, "longitude": 19.0402},
    {"city": "Stockholm", "latitude": 59.3293, "longitude": 18.0686},
    {"city": "Copenhagen", "latitude": 55.6761, "longitude": 12.5683},
    {"city": "Dublin", "latitude": 53.3498, "longitude": -6.2603},
    {"city": "Oslo", "latitude": 59.9139, "longitude": 10.7522},
    {"city": "Zurich", "latitude": 47.3769, "longitude": 8.5417}
]

# Comprehensive set of European countries for filtering
EUROPEAN_COUNTRIES = {
    "Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium",
    "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary",
    "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia",
    "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia",
    "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom", "Vatican City"
}

# Function to generate city-based coordinates with a small random offset
def get_city_based_coordinates():
    city = random.choice(EUROPEAN_CITIES)
    # Small offset to add variability (in degrees)
    lat_offset = random.uniform(-0.2, 0.2)
    lon_offset = random.uniform(-0.2, 0.2)
    return city["latitude"] + lat_offset, city["longitude"] + lon_offset

def get_random_coordinates_europe():
    """Return completely random coordinates within Europe's bounding box."""
    # Approximate bounding box for Europe:
    # Latitude: 35° N to 70° N, Longitude: -10° W to 40° E
    lat = random.uniform(35, 70)
    lon = random.uniform(-10, 40)
    return lat, lon

# Function to create a nearby search query using city-based coordinates
def get_nearby_query():
    lat, lon = get_city_based_coordinates()
    coordinate_string = f"{lat},{lon}" # 50km radius
    return coordinate_string

# Function to fetch location data using nearby search (coordinates only)
def fetch_nearby_locations():
    location_str = get_nearby_query()
    params = {
        "latLong": location_str,   # using the new coordinate string format
        "radius": 50000,            # radius in meters (50 km)
        "radiusUnit": "km",
        "key": API_KEY,
        "language": "en",
        "limit": 10                 # up to 10 results per request
    }

    headers = {"accept": "application/json"}
    print("Nearby search parameters:", params)
    
    response = requests.get(SEARCH_URL, params=params, headers=headers)
    print("Nearby search response status:", response.status_code)
    print("Nearby search response text:", response.text)
    
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# Retry mechanism to ensure a valid nearby search result is returned
def fetch_valid_nearby_locations(max_attempts=5):
    for attempt in range(max_attempts):
        data = fetch_nearby_locations()
        if data:
            print(f"Data found on attempt {attempt+1}")
            return data
        else:
            print(f"No results for attempt {attempt+1}, trying new coordinates...")
            time.sleep(1)  # Delay before next try
    print("Max attempts reached. No valid data found.")
    return []

# Function to fetch location details using the location ID
def fetch_location_details(location_id, retry_attempts=3):
    url = DETAILS_URL_TEMPLATE.format(location_id=location_id)
    params = {"key": API_KEY, "language": "en"}
    headers = {"accept": "application/json"}
    
    for attempt in range(retry_attempts):
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"429 Limit Exceeded for {location_id}. Attempt {attempt+1}/{retry_attempts}. Waiting before retrying...")
            # Wait longer with each retry (exponential backoff)
            time.sleep(2 ** (attempt + 1))
        else:
            print(f"Details Error for {location_id}: {response.status_code}, {response.text}")
            break
    return {}

# Function to merge basic search results with detailed data
def merge_location_data(basic, details):
    merged = {
        "location_id": basic.get("location_id"),
        "name": basic.get("name")
    }
    # Flatten the nested address object if available
    address = basic.get("address_obj", {})
    merged["city"] = address.get("city")
    merged["country"] = address.get("country")
    
    # Add details from the location details response
    merged["latitude"] = details.get("latitude")
    merged["longitude"] = details.get("longitude")
    merged["rating"] = details.get("rating")
    merged["num_reviews"] = details.get("num_reviews")
    merged["price_level"] = details.get("price_level")
    
    category = details.get("category", {})
    merged["category"] = category.get("name")
    
    return merged

# Function to filter out results that are not in Europe
def filter_european_results(locations):
    filtered = []
    for loc in locations:
        # Check the country field from the merged data
        country = loc.get("country")
        if country in EUROPEAN_COUNTRIES:
            filtered.append(loc)
    return filtered

def append_to_csv(df, csv_path):
    if not os.path.exists(csv_path):
        df.to_csv(csv_path, index=False, mode='w', header=True)
    else:
        df.to_csv(csv_path, index=False, mode='a', header=False)
    print(f"Data appended to {csv_path}")

# Main function to collect data and save it into a CSV file within a "data" folder
def main():
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    csv_path = os.path.join(data_folder, "tripadvisor_europe_nearby_destinations.csv")
    
    total_iterations = 440
    
    for i in range(total_iterations):
        print(f"Iteration {i+1}/{total_iterations}")
        # Use the retry mechanism to get valid nearby search results
        basic_data_list = fetch_valid_nearby_locations(max_attempts=5)
        if not basic_data_list:
            print("No data returned after maximum attempts. Skipping iteration.")
            continue
        
        all_results = []
        # For each basic location result, fetch details and merge the data
        for basic in basic_data_list:
            location_id = basic.get("location_id")
            if location_id:
                details = fetch_location_details(location_id)
                merged_data = merge_location_data(basic, details)
                all_results.append(merged_data)
                time.sleep(0.5)  # Small delay between detail requests
        
        # Filter results to only include European locations
        european_results = filter_european_results(all_results)
        
        if european_results:
            columns_to_keep = [
                "location_id", "name", "city", "country", 
                "latitude", "longitude", "rating", "num_reviews", "price_level",
                "category"
            ]
            df = pd.DataFrame(european_results)
            df = df[columns_to_keep]
            append_to_csv(df, csv_path)
        else:
            print("No European data collected in this iteration.")
        
        # Delay between iterations to control API usage (adjust as needed)
        time.sleep(1)
    
    print("Script complete.")

if __name__ == "__main__":
    main()