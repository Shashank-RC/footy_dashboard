import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key
API_KEY = os.getenv('FOOTBALL_API_KEY')

# In-memory cache to store API responses
cache = {}

def get_standings(league_id, season):
    cache_key = f"{league_id}_{season}"

    # Serve from cache if data exists
    if cache_key in cache:
        print(f"Serving from cache for {league_id} - {season}")
        return cache[cache_key]

    # API request if not cached
    url = f"https://v3.football.api-sports.io/standings?league={league_id}&season={season}"
    headers = {
        'x-apisports-key': API_KEY
    }

    print(f"Making request to API for league {league_id} and season {season}...")
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if 'response' in data and data['response']:
                cache[cache_key] = data  # Cache the response
                return data
            else:
                print("API returned no data for the selected league and season.")
                return {"error": "No data available for this selection."}
        elif response.status_code == 429:
            print("API rate limit exceeded.")
            return {"error": "API rate limit exceeded. Please try again later."}
        elif response.status_code == 401:
            print("Invalid API key.")
            return {"error": "Invalid API key. Please check your API key."}
        else:
            print(f"API returned an error: {response.status_code}")
            return {"error": f"API error: {response.status_code}"}
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": "An error occurred while fetching data. Please try again."}

def clear_cache():
    global cache
    cache = {}
    print("Cache cleared.")
