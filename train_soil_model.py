import pandas as pd
import joblib
import os

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("data/soil_dataset.csv")

X = df[["nitrogen", "phosphorus", "potassium", "ph"]]
y = df["soil_type"]

# Create model
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))
])

# Train
model.fit(X, y)

# Save
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/soil_model.pkl")

print("✅ Soil model saved successfully!")