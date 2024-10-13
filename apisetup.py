import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key
API_KEY = os.getenv('FOOTBALL_API_KEY')

# In-memory cache to store API responses
cache = {}

# Function to get standings
def get_standings(league_id, season):
    cache_key = f"{league_id}_{season}"

    if cache_key in cache:
        print(f"Serving from cache for {league_id} - {season}")
        return cache[cache_key]

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
                cache[cache_key] = data
                return data
            else:
                print("API returned no data for the selected league and season.")
                return {"error": "No data available for this selection."}
        elif response.status_code == 429:
            return {"error": "API rate limit exceeded. Please try again later."}
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your API key."}
        else:
            return {"error": f"API error: {response.status_code}"}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": "An error occurred while fetching data. Please try again."}

# Function to get live scores
def get_live_scores():
    url = f"https://v3.football.api-sports.io/fixtures?live=all"
    headers = {
        'x-apisports-key': API_KEY
    }

    print("Fetching live scores...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and data['response']:
                return data
            else:
                return {"error": "No live matches available at the moment."}
        else:
            return {"error": f"API error: {response.status_code}"}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": "An error occurred while fetching live scores."}

# Function to get fixtures
def get_fixtures(league_id, season):
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season={season}"
    headers = {
        'x-apisports-key': API_KEY
    }

    print(f"Fetching fixtures for league {league_id} and season {season}...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and data['response']:
                return data
            else:
                return {"error": "No fixtures available for this selection."}
        else:
            return {"error": f"API error: {response.status_code}"}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": "An error occurred while fetching fixtures."}
