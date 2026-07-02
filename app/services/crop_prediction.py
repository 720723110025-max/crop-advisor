"""
Crop prediction service using machine learning.
"""

import numpy as np
import pandas as pd
from app.services.ml_models import MLService
import logging

logger = logging.getLogger(__name__)

class CropPredictionService:
    """
    Service for crop prediction and recommendations.
    """
    
    def __init__(self):
        """Initialize crop prediction service."""
        self.ml_service = MLService()
    
    def predict_crop(self, features_df):
        """
        Predict crop based on soil and climate features.
        
        Args:
            features_df (pd.DataFrame): DataFrame with soil and climate parameters
        
        Returns:
            dict: Prediction results
        """
        try:
            # Extract features
            features = features_df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].values[0]
            
            # Get prediction from ML model
            prediction = self.ml_service.predict_crop(features)
            
            # Generate suggestions based on prediction
            suggestions = self._generate_suggestions(prediction['crop'], features_df.iloc[0])
            
            # Get all top recommendations
            all_recommendations = []
            if 'probabilities' in prediction and prediction['probabilities']:
                sorted_probs = sorted(
                    prediction['probabilities'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                all_recommendations = [
                    {'crop': crop, 'confidence': prob}
                    for crop, prob in sorted_probs
                ]
            
            return {
                'status': 'success',
                'crop': prediction['crop'],
                'confidence': prediction['confidence'],
                'suggestions': suggestions,
                'all_recommendations': all_recommendations
            }
            
        except Exception as e:
            logger.error(f"Error in crop prediction: {str(e)}")
            return {
                'status': 'error',
                'message': f'Prediction failed: {str(e)}'
            }
    
    def _generate_suggestions(self, crop, features):
        """
        Generate farming suggestions based on crop and conditions.
        """
        suggestions = []
        
        # Soil-based suggestions
        ph = features.get('ph', 7.0)
        nitrogen = features.get('N', 50)
        phosphorus = features.get('P', 50)
        potassium = features.get('K', 50)
        
        if ph < 6.0:
            suggestions.append(f"Apply lime to increase soil pH. Current pH: {ph:.2f} (ideal for {crop}: 6.0-7.0)")
        elif ph > 7.5:
            suggestions.append(f"Apply sulfur to decrease soil pH. Current pH: {ph:.2f} (ideal for {crop}: 6.0-7.0)")
        
        if nitrogen < 40:
            suggestions.append("Low nitrogen levels detected. Consider adding nitrogen-rich fertilizers.")
        elif nitrogen > 120:
            suggestions.append("High nitrogen levels. Reduce nitrogen application to prevent vegetative growth.")
        
        if phosphorus < 30:
            suggestions.append("Phosphorus levels are low. Apply phosphorus fertilizers for better root development.")
        
        if potassium < 30:
            suggestions.append("Potassium levels are low. Add potassium-rich fertilizers for disease resistance.")
        
        # Climate-based suggestions
        temp = features.get('temperature', 25)
        humidity = features.get('humidity', 70)
        rainfall = features.get('rainfall', 200)
        
        if temp > 35:
            suggestions.append("High temperature detected. Provide shade or increase irrigation.")
        elif temp < 10:
            suggestions.append("Low temperature detected. Use protective covers or greenhouses.")
        
        if humidity > 85:
            suggestions.append("High humidity. Monitor for fungal diseases.")
        elif humidity < 40:
            suggestions.append("Low humidity. Increase irrigation frequency.")
        
        if rainfall > 300:
            suggestions.append("Excessive rainfall. Ensure proper drainage.")
        elif rainfall < 100:
            suggestions.append("Low rainfall. Implement irrigation system.")
        
        # Specific crop suggestions
        crop_specific = {
            'rice': [
                "Maintain water depth of 5-10 cm during vegetative stage.",
                "Apply zinc fertilizer for better yield.",
                "Monitor for stem borer and leaf folder pests."
            ],
            'wheat': [
                "Apply nitrogen fertilizer in two split doses.",
                "Irrigate at critical stages: crown root initiation and flowering.",
                "Monitor for rust and powdery mildew."
            ],
            'maize': [
                "Plant in well-drained soil.",
                "Apply nitrogen at side-dressing stage.",
                "Monitor for stem borer and fall armyworm."
            ],
            'sugarcane': [
                "Apply organic manure before planting.",
                "Irrigate at 7-10 day intervals.",
                "Monitor for red rot and smut diseases."
            ],
            'cotton': [
                "Apply potassium for fiber quality.",
                "Monitor for bollworms and aphids.",
                "Use integrated pest management strategies."
            ]
        }
        
        if crop in crop_specific:
            suggestions.extend(crop_specific[crop])
        
        # Add general suggestions
        suggestions.append(f"Use certified seeds for {crop} to ensure high yield.")
        suggestions.append("Monitor crop regularly for pest and disease outbreaks.")
        suggestions.append("Maintain proper weed management.")
        
        # Limit to top 5 suggestions
        return "\n".join(suggestions[:5])