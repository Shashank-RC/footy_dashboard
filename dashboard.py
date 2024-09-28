import pandas as pd
from apisetup import get_standings

def get_standings_dataframe(league_id, season):
    print("Fetching data...")  # Debugging statement
    data = get_standings(league_id, season)
    if data:
        print("Data fetched successfully!")  # Debugging statement
        standings = data['response'][0]['league']['standings'][0]
        df = pd.DataFrame(standings)
        df = df[['rank', 'team', 'points', 'goalsDiff', 'all']]
        return df
    else:
        print("No data found!")  # Debugging statement
        return pd.DataFrame()

# Example usage: Get EPL standings for the 2023 season
if __name__ == "__main__":
    print("Running dashboard.py")  # Debugging statement
    df = get_standings_dataframe(39, 2022)
    if not df.empty:
        print(df)
    else:
        print("The DataFrame is empty.")
