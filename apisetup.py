import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key
API_KEY = os.getenv('FOOTBALL_API_KEY')

if not API_KEY:
    print("API key is missing! Make sure it's set correctly in your .env file.")
else:
    print("API key loaded successfully.")

BASE_URL = "https://v3.football.api-sports.io/"

def get_standings(league_id, season):
    url = f"{BASE_URL}standings?league={league_id}&season={season}"
    headers = {
        'x-apisports-key': API_KEY
    }
    print(f"Making request to API for league {league_id} and season {season}...")

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'errors' in data and data['errors']:
                print(f"API returned an error: {data['errors']}")
                return None
            print("API request successful!")
            return data  # Return the response as JSON
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Test the API connection by fetching EPL standings for 2022
if __name__ == "__main__":
    print("Testing API connection...")

    league_id = 39  # EPL ID
    season = 2022   # Free plan allows up to 2022 season
    data = get_standings(league_id, season)

    # Print the raw data to inspect the structure
    if data:
        print("Raw API response:", data)
    else:
        print("No data returned from API or an error occurred.")
