import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load historical match data
data = pd.read_csv('historical_matches.csv')

# Fill any missing values (basic preprocessing)
data.fillna(0, inplace=True)

# Feature Engineering
data['goal_difference'] = data['home_goals'] - data['away_goals']
data['result'] = data.apply(lambda x: 1 if x['home_goals'] > x['away_goals'] else (-1 if x['home_goals'] < x['away_goals'] else 0), axis=1)

# Features and Target
features = ['goal_difference']
target = 'result'

X = data[features]
y = data[target]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize Features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save processed data to use later
import joblib
joblib.dump((X_train, X_test, y_train, y_test, scaler), 'processed_data.pkl')

print("Data preprocessing completed and saved.")
