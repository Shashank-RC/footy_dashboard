import pandas as pd
from apisetup import get_historical_matches

# Define leagues and seasons to collect data for
league_id = 39  # EPL
seasons = [2021, 2022]

all_matches = []

for season in seasons:
    data = get_historical_matches(league_id, season)
    if 'response' in data:
        for match in data['response']:
            match_data = {
                'fixture_id': match['fixture']['id'],
                'date': match['fixture']['date'],
                'home_team': match['teams']['home']['name'],
                'away_team': match['teams']['away']['name'],
                'home_goals': match['goals']['home'],
                'away_goals': match['goals']['away'],
                'status': match['fixture']['status']['long']
            }
            all_matches.append(match_data)

# Create DataFrame and save to CSV
df = pd.DataFrame(all_matches)
df.to_csv('historical_matches.csv', index=False)
print("Historical match data saved to historical_matches.csv")
