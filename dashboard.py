from flask import Flask, render_template, request
from apisetup import get_standings
import pandas as pd

app = Flask(__name__)

# Transform and clean the API data to display specific fields
def transform_standings_data(data):
    standings = data['response'][0]['league']['standings'][0]
    
    clean_standings = []
    for team_data in standings:
        clean_standings.append({
            "rank": team_data['rank'],
            "team": f"<img src='{team_data['team']['logo']}' width='20'> {team_data['team']['name']}",
            "points": team_data['points'],
            "goalsDiff": team_data['goalsDiff'],
            "form": team_data['form'],
            "matches_played": team_data['all']['played'],
            "wins": team_data['all']['win'],
            "draws": team_data['all']['draw'],
            "losses": team_data['all']['lose'],
            "home_wins": team_data['home']['win'],
            "goals_for": team_data['all']['goals']['for']
        })
    
    # Convert to a DataFrame
    df = pd.DataFrame(clean_standings)
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    league_id = 39  # Default to EPL
    season = 2022   # Default to 2022
    error_message = None

    if request.method == 'POST':
        league_id = int(request.form['league'])
        season = int(request.form['season'])

    # Fetch data and handle potential errors
    data = get_standings(league_id, season)

    if 'error' in data:
        error_message = data['error']
        df = None
    else:
        df = transform_standings_data(data)

    if df is not None:
        # Render the HTML table with logos and clean data
        html_table = df.to_html(classes='table table-striped table-hover', index=False, escape=False)  # escape=False to render HTML in 'team' column
        return render_template('index.html', tables=html_table, league_id=league_id, season=season, error_message=error_message)
    else:
        return render_template('index.html', error_message=error_message, league_id=league_id, season=season)

if __name__ == '__main__':
    app.run(debug=True)
