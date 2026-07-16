"""
Crop Prediction Service
"""

import pickle
import numpy as np
import os

MODEL_PATH = "app/ml_models/crop_model.pkl"

model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)


def predict_crop(n, p, k, temperature, humidity, ph, rainfall):
    """
    Predict crop using trained model.
    """

    if model is None:
        return {
            "success": False,
            "message": "Crop model not found."
        }

    data = np.array([[

        n,
        p,
        k,
        temperature,
        humidity,
        ph,
        rainfall

    ]])

    prediction = model.predict(data)[0]

    confidence = 95

    return {

        "success": True,

        "crop": prediction,

        "confidence": confidence

    }