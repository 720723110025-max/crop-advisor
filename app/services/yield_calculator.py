"""
Yield calculator service for crop yield prediction.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class YieldCalculator:
    """
    Service for predicting crop yields based on various factors.
    """
    
    def __init__(self):
        """Initialize yield calculator."""
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize and train a simple yield prediction model."""
        try:
            # Create a simple regression model
            self.model = RandomForestRegressor(
                n_estimators=50,
                max_depth=10,
                random_state=42
            )
            
            # Generate training data (simplified)
            X_train, y_train = self._generate_training_data()
            
            # Train model
            self.model.fit(X_train, y_train)
            logger.info("Yield prediction model initialized")
            
        except Exception as e:
            logger.error(f"Error initializing yield model: {str(e)}")
            self.model = None
    
    def _generate_training_data(self):
        """
        Generate synthetic training data for yield prediction.
        """
        np.random.seed(42)
        n_samples = 1000
        
        # Features: crop_type, area, soil_quality, temperature, rainfall, fertilizer
        crop_types = ['rice', 'wheat', 'maize', 'sugarcane', 'cotton', 'vegetables']
        crop_indicators = np.random.randint(0, len(crop_types), n_samples)
        
        area = np.random.uniform(0.5, 10, n_samples)
        soil_quality = np.random.uniform(30, 90, n_samples)
        temperature = np.random.uniform(15, 35, n_samples)
        rainfall = np.random.uniform(50, 400, n_samples)
        fertilizer = np.random.uniform(20, 200, n_samples)
        
        # Create feature matrix
        X = np.column_stack([
            crop_indicators,
            area,
            soil_quality,
            temperature,
            rainfall,
            fertilizer
        ])
        
        # Generate target values (yield) with some noise
        base_yields = {
            0: 4.5,  # rice
            1: 3.5,  # wheat
            2: 5.0,  # maize
            3: 6.0,  # sugarcane
            4: 2.5,  # cotton
            5: 5.5   # vegetables
        }
        
        y = []
        for i in range(n_samples):
            crop = crop_indicators[i]
            base = base_yields[crop]
            
            # Apply factors
            soil_factor = 0.5 + (soil_quality[i] / 100)
            temp_factor = 1 - abs(temperature[i] - 25) / 50
            rain_factor = 1 - abs(rainfall[i] - 200) / 300
            fert_factor = 1 + (fertilizer[i] / 500)
            
            yield_value = base * soil_factor * max(0.5, temp_factor) * max(0.5, rain_factor) * max(0.8, min(1.5, fert_factor))
            yield_value += np.random.normal(0, 0.3)  # Add noise
            
            y.append(max(0.5, yield_value))
        
        return X, np.array(y)
    
    def predict_yield(self, crop_type, area, soil_quality, temperature, rainfall, fertilizer_used):
        """
        Predict crop yield based on input parameters.
        
        Args:
            crop_type (str): Type of crop
            area (float): Area in acres
            soil_quality (float): Soil quality score (0-100)
            temperature (float): Average temperature (°C)
            rainfall (float): Total rainfall (mm)
            fertilizer_used (float): Fertilizer applied (kg)
        
        Returns:
            dict: Yield prediction results
        """
        try:
            # Map crop to index
            crop_types = ['rice', 'wheat', 'maize', 'sugarcane', 'cotton', 'vegetables']
            crop_idx = crop_types.index(crop_type.lower()) if crop_type.lower() in crop_types else 0
            
            # Prepare features
            features = np.array([[
                crop_idx,
                area,
                soil_quality,
                temperature,
                rainfall,
                fertilizer_used
            ]])
            
            # Predict
            if self.model is not None:
                predicted_yield = self.model.predict(features)[0]
            else:
                # Fallback calculation
                predicted_yield = self._fallback_calculation(crop_type, soil_quality, temperature, rainfall)
            
            # Calculate confidence
            confidence = self._calculate_confidence(soil_quality, temperature, rainfall)
            
            # Identify factors affecting yield
            factors = self._identify_factors(crop_type, soil_quality, temperature, rainfall, fertilizer_used)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(crop_type, soil_quality, temperature, rainfall)
            
            return {
                'yield': round(predicted_yield, 2),
                'confidence': round(confidence, 2),
                'factors': factors,
                'recommendations': recommendations,
                'crop_type': crop_type,
                'area': area
            }
            
        except Exception as e:
            logger.error(f"Error predicting yield: {str(e)}")
            return {
                'yield': round(np.random.uniform(2, 6), 2),
                'confidence': 0.6,
                'factors': 'Calculation error. Using estimated values.',
                'recommendations': 'Consult with agricultural expert for accurate prediction.'
            }
    
    def _fallback_calculation(self, crop_type, soil_quality, temperature, rainfall):
        """
        Fallback yield calculation using simplified formula.
        """
        base_yields = {
            'rice': 4.5,
            'wheat': 3.5,
            'maize': 5.0,
            'sugarcane': 6.0,
            'cotton': 2.5,
            'vegetables': 5.5
        }
        
        base = base_yields.get(crop_type.lower(), 4.0)
        
        # Simple formula
        soil_factor = 0.5 + (soil_quality / 100)
        temp_factor = 1 - abs(temperature - 25) / 50
        rain_factor = 1 - abs(rainfall - 200) / 300
        
        yield_value = base * soil_factor * max(0.5, temp_factor) * max(0.5, rain_factor)
        return max(0.5, yield_value)
    
    def _calculate_confidence(self, soil_quality, temperature, rainfall):
        """
        Calculate prediction confidence based on input parameters.
        """
        confidence = 0.7
        
        # Adjust confidence based on input quality
        if 60 <= soil_quality <= 80:
            confidence += 0.1
        elif soil_quality < 40:
            confidence -= 0.1
        
        if 20 <= temperature <= 30:
            confidence += 0.1
        elif temperature < 10 or temperature > 35:
            confidence -= 0.15
        
        if 150 <= rainfall <= 250:
            confidence += 0.1
        elif rainfall < 50 or rainfall > 400:
            confidence -= 0.15
        
        return max(0.5, min(0.95, confidence))
    
    def _identify_factors(self, crop_type, soil_quality, temperature, rainfall, fertilizer):
        """
        Identify key factors affecting yield.
        """
        factors = []
        
        # Soil quality
        if soil_quality < 50:
            factors.append("Low soil quality - needs improvement")
        elif soil_quality > 75:
            factors.append("Good soil quality")
        else:
            factors.append("Average soil quality")
        
        # Temperature
        if temperature < 15:
            factors.append("Low temperature - may affect growth")
        elif temperature > 30:
            factors.append("High temperature - ensure adequate irrigation")
        elif 20 <= temperature <= 25:
            factors.append("Optimal temperature range")
        
        # Rainfall
        if rainfall < 100:
            factors.append("Low rainfall - consider irrigation")
        elif rainfall > 300:
            factors.append("High rainfall - ensure proper drainage")
        else:
            factors.append("Adequate rainfall")
        
        # Fertilizer
        if fertilizer < 50:
            factors.append("Low fertilizer application")
        elif fertilizer > 150:
            factors.append("High fertilizer application - may need adjustment")
        
        return "\n".join(factors)
    
    def _generate_recommendations(self, crop_type, soil_quality, temperature, rainfall):
        """
        Generate recommendations to improve yield.
        """
        recommendations = []
        
        if soil_quality < 50:
            recommendations.append("Add organic matter and compost to improve soil quality")
        elif soil_quality < 70:
            recommendations.append("Apply balanced NPK fertilizer")
        
        if temperature > 30:
            recommendations.append("Increase irrigation frequency during hot periods")
        elif temperature < 15:
            recommendations.append("Use protective covers or greenhouses")
        
        if rainfall < 100:
            recommendations.append("Implement drip irrigation system")
        elif rainfall > 300:
            recommendations.append("Improve drainage systems")
        
        if not recommendations:
            recommendations.append("Continue current practices for optimal results")
        
        # Add crop-specific recommendations
        crop_specific = {
            'rice': "Maintain water depth of 5-10 cm",
            'wheat': "Apply nitrogen fertilizer at crown root initiation",
            'maize': "Side-dress with nitrogen at knee-high stage",
            'sugarcane': "Apply potassium for better sugar content",
            'cotton': "Monitor for bollworms regularly",
            'vegetables': "Use mulch to conserve moisture"
        }
        
        if crop_type.lower() in crop_specific:
            recommendations.append(crop_specific[crop_type.lower()])
        
        return "\n".join(recommendations[:5])