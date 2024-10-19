import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load preprocessed data
X_train, X_test, y_train, y_test, scaler = joblib.load('processed_data.pkl')

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make Predictions
y_pred = model.predict(X_test)

# Evaluate Model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")
print(classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model, 'match_outcome_model.pkl')
print("Trained model saved as match_outcome_model.pkl")
