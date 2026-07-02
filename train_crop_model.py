import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

print("Loading dataset...")

df = pd.read_csv("data/crop_recommendation_dataset.csv")

X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

scaler = StandardScaler()
X = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/crop_recommendation_model.pkl")
joblib.dump(scaler, "models/crop_scaler.pkl")

print("✅ Crop model trained successfully!")
print("✅ Model saved in models folder")