from flask import Flask, render_template, request
from apisetup import get_standings, get_live_scores, get_fixtures, search_player_by_name, get_team_data
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load('match_outcome_model.pkl')
scaler = joblib.load('processed_data.pkl')[-1]  # Load scaler from processed data
@app.route('/predict', methods=['GET', 'POST'])
def predict_match():
    prediction = None
    if request.method == 'POST':
        # Extract form data
        goal_difference = float(request.form['goal_difference'])

        # Prepare input data for prediction
        input_data = np.array([[goal_difference]])
        input_data = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Translate prediction into readable form
        if prediction == 1:
            prediction = "Home Team Wins"
        elif prediction == -1:
            prediction = "Away Team Wins"
        else:
            prediction = "Draw"

    return render_template('predict.html', prediction=prediction)

# Function to transform standings for display
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
    
    df = pd.DataFrame(clean_standings)
    return df

# Function to transform live scores for display
def transform_live_scores(data):
    matches = data['response']
    
    live_matches = []
    for match in matches:
        live_matches.append({
            "league": match['league']['name'],
            "home_team": f"<img src='{match['teams']['home']['logo']}' width='20'> {match['teams']['home']['name']}",
            "away_team": f"<img src='{match['teams']['away']['logo']}' width='20'> {match['teams']['away']['name']}",
            "score": f"{match['goals']['home']} - {match['goals']['away']}",
            "status": match['fixture']['status']['short']
        })

    df = pd.DataFrame(live_matches)
    return df

# Function to transform fixtures for display
def transform_fixtures(data):
    matches = data['response']
    
    fixtures = []
    for match in matches:
        fixtures.append({
            "date": match['fixture']['date'],
            "home_team": f"<img src='{match['teams']['home']['logo']}' width='20'> {match['teams']['home']['name']}",
            "away_team": f"<img src='{match['teams']['away']['logo']}' width='20'> {match['teams']['away']['name']}",
            "status": match['fixture']['status']['long']
        })

    df = pd.DataFrame(fixtures)
    return df

# Route for player search
@app.route('/players', methods=['GET', 'POST'])
def search_players():
    player_data = None
    error_message = None

    if request.method == 'POST':
        player_name = request.form['player_name']
        player_data = search_player_by_name(player_name)

        if 'error' in player_data:
            error_message = player_data['error']
            player_data = None

    return render_template('players.html', player_data=player_data, error_message=error_message)

# Route for team data
@app.route('/teams', methods=['GET'])
def team_data():
    team_id = request.args.get('team_id', default=33)  # Default to Manchester United
    team_data = get_team_data(team_id)

    return render_template('teams.html', team_data=team_data)

# Main index route for standings, live scores, and fixtures
@app.route('/', methods=['GET', 'POST'])
def index():
    league_id = 39  # Default to EPL
    season = 2022   # Default to 2022
    error_message = None
    standings = None
    live_scores = None
    fixtures = None

    if request.method == 'POST':
        league_id = int(request.form['league'])
        season = int(request.form['season'])

    # Fetch standings
    data = get_standings(league_id, season)
    if 'error' in data:
        error_message = data['error']
    else:
        standings = transform_standings_data(data)

    # Fetch live scores
    live_data = get_live_scores()
    if 'error' in live_data:
        error_message = live_data['error']
    else:
        live_scores = transform_live_scores(live_data)

    # Fetch fixtures
    fixture_data = get_fixtures(league_id, season)
    if 'error' in fixture_data:
        error_message = fixture_data['error']
    else:
        fixtures = transform_fixtures(fixture_data)

    standings_html = standings.to_html(classes='table table-striped table-hover', index=False, escape=False) if standings is not None else None
    live_scores_html = live_scores.to_html(classes='table table-striped table-hover', index=False, escape=False) if live_scores is not None else None
    fixtures_html = fixtures.to_html(classes='table table-striped table-hover', index=False, escape=False) if fixtures is not None else None

    return render_template('index.html', standings=standings_html, live_scores=live_scores_html, fixtures=fixtures_html, league_id=league_id, season=season, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
