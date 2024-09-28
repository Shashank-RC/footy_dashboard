import pandas as pd
from flask import Flask, render_template, request
from apisetup import get_standings

app = Flask(__name__)

def get_standings_dataframe(league_id, season):
    data = get_standings(league_id, season)
    if data and data['response']:
        standings = data['response'][0]['league']['standings'][0]
        df = pd.DataFrame(standings)
        df['team'] = df['team'].apply(lambda x: x['name'])  # Extract team name
        df = df[['rank', 'team', 'points', 'goalsDiff']]
        print(df)  # Debugging: Print the DataFrame to the console
        return df
    else:
        print("No data available or API returned an error.")
        return pd.DataFrame()

@app.route('/', methods=['GET', 'POST'])
def index():
    league_id = 39  # Default to EPL
    season = 2022   # Default to 2022
    if request.method == 'POST':
        league_id = int(request.form['league'])
        season = int(request.form['season'])

    df = get_standings_dataframe(league_id, season)

    if not df.empty:
        # Debugging: Print the HTML table being rendered
        print(df.to_html(classes='data'))
        return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, league_id=league_id, season=season)
    else:
        return "<h1>No standings data available</h1>"

if __name__ == '__main__':
    app.run(debug=True)
