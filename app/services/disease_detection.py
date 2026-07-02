"""
Disease detection service using computer vision and deep learning.
"""

import os
import cv2
import numpy as np
from PIL import Image
from app.services.ml_models import MLService
import logging

logger = logging.getLogger(__name__)

class DiseaseDetectionService:
    """
    Service for detecting plant diseases from leaf images.
    """
    
    def __init__(self):
        """Initialize disease detection service."""
        self.ml_service = MLService()
        self.image_size = (128, 128)
    
    def preprocess_image(self, image_array):
        """
        Preprocess image for model input.
        
        Args:
            image_array (np.ndarray): Input image array
        
        Returns:
            np.ndarray: Preprocessed image
        """
        try:
            # Resize image
            if image_array.shape[:2] != self.image_size:
                image_array = cv2.resize(image_array, self.image_size)
            
            # Convert to RGB if needed
            if len(image_array.shape) == 2:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
            elif image_array.shape[2] == 4:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
            
            # Normalize
            image_array = image_array.astype(np.float32) / 255.0
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image_array
    
    def detect_disease(self, image_array, crop_type='Unknown'):
        """
        Detect disease in leaf image.
        
        Args:
            image_array (np.ndarray): Input leaf image
            crop_type (str): Type of crop
        
        Returns:
            dict: Disease detection results
        """
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_array)
            
            # Get prediction from ML model
            # For now, we'll use the fallback method since we need a trained model
            # In production, this would use the actual deep learning model
            
            # Simulate disease detection based on image characteristics
            disease_result = self._simulate_disease_detection(processed_image, crop_type)
            
            return disease_result
            
        except Exception as e:
            logger.error(f"Error in disease detection: {str(e)}")
            return {
                'disease': 'Unknown',
                'confidence': 0.0,
                'severity': 'Unknown',
                'symptoms': 'Error in detection process',
                'causes': 'Unable to analyze image',
                'prevention': 'Please upload a clearer image',
                'treatment': 'Consult with agricultural expert'
            }
    
    def _simulate_disease_detection(self, image, crop_type):
        """
        Simulate disease detection using image analysis.
        This is a placeholder for the actual deep learning model.
        """
        try:
            # Analyze image characteristics
            # This is a simplified simulation
            mean_color = np.mean(image, axis=(0, 1))
            std_color = np.std(image, axis=(0, 1))
            
            # Simple rules based on color analysis
            # In production, this would use a trained CNN
            
            # Check for yellowish leaves (possible nutrient deficiency or disease)
            if mean_color[1] > mean_color[0] and mean_color[1] > mean_color[2]:
                diseases = [
                    {'name': 'Nitrogen Deficiency', 'confidence': 0.75},
                    {'name': 'Leaf Spot', 'confidence': 0.60},
                    {'name': 'Chlorosis', 'confidence': 0.55}
                ]
            elif mean_color[0] < 100 and mean_color[1] < 100:
                diseases = [
                    {'name': 'Bacterial Blight', 'confidence': 0.70},
                    {'name': 'Fungal Infection', 'confidence': 0.65}
                ]
            elif np.any(image[:, :, 0] > 200) and np.any(image[:, :, 1] < 100):
                diseases = [
                    {'name': 'Rust Disease', 'confidence': 0.80},
                    {'name': 'Leaf Blight', 'confidence': 0.72}
                ]
            else:
                diseases = [
                    {'name': 'Healthy', 'confidence': 0.90},
                    {'name': 'Minor Infection', 'confidence': 0.40}
                ]
            
            # Select the most likely disease
            best_disease = max(diseases, key=lambda x: x['confidence'])
            
            # Get disease information
            disease_info = self._get_disease_information(best_disease['name'])
            
            return {
                'disease': best_disease['name'],
                'confidence': best_disease['confidence'],
                'severity': self._get_severity(best_disease['confidence']),
                'crop_type': crop_type,
                **disease_info
            }
            
        except Exception as e:
            logger.error(f"Error in disease simulation: {str(e)}")
            return {
                'disease': 'Unknown',
                'confidence': 0.0,
                'severity': 'Unknown',
                'symptoms': 'Unable to analyze',
                'causes': 'Unknown',
                'prevention': 'Please consult an expert',
                'treatment': 'Seek professional advice'
            }
    
    def _get_severity(self, confidence):
        """
        Determine disease severity based on confidence score.
        """
        if confidence > 0.8:
            return 'High'
        elif confidence > 0.6:
            return 'Moderate'
        else:
            return 'Mild'
    
    def _get_disease_information(self, disease_name):
        """
        Get detailed information about a disease.
        """
        disease_info = {
            'Nitrogen Deficiency': {
                'symptoms': 'Yellowing of older leaves, stunted growth, pale green color.',
                'causes': 'Insufficient nitrogen in soil, leaching, or poor soil conditions.',
                'prevention': 'Apply nitrogen-rich fertilizers. Use crop rotation with legumes.',
                'treatment': 'Apply urea or other nitrogen fertilizers. Use compost and manure.'
            },
            'Leaf Spot': {
                'symptoms': 'Dark brown or black spots on leaves, yellow halos around spots.',
                'causes': 'Fungal spores spread by wind and water splash.',
                'prevention': 'Ensure proper spacing. Avoid overhead irrigation.',
                'treatment': 'Apply fungicides. Remove infected leaves.'
            },
            'Bacterial Blight': {
                'symptoms': 'Water-soaked spots that turn brown, leaf wilting.',
                'causes': 'Bacterial infection spread by rain, irrigation, and insects.',
                'prevention': 'Use disease-free seeds. Practice crop rotation.',
                'treatment': 'Apply copper-based bactericides. Remove infected plants.'
            },
            'Fungal Infection': {
                'symptoms': 'White or gray powdery growth on leaves, deformed growth.',
                'causes': 'High humidity, poor air circulation, overcrowding.',
                'prevention': 'Ensure good ventilation. Avoid overhead watering.',
                'treatment': 'Apply appropriate fungicides. Use neem oil sprays.'
            },
            'Rust Disease': {
                'symptoms': 'Orange, yellow, or brown pustules on leaves.',
                'causes': 'Fungal spores spread by wind and insects.',
                'prevention': 'Use resistant varieties. Maintain proper plant spacing.',
                'treatment': 'Apply fungicides. Remove and destroy infected plants.'
            },
            'Leaf Blight': {
                'symptoms': 'Large brown or gray spots on leaves, leaf death.',
                'causes': 'Fungal infection, often during wet weather.',
                'prevention': 'Use resistant varieties. Ensure good drainage.',
                'treatment': 'Apply fungicides. Remove infected plant parts.'
            }
        }
        
        return disease_info.get(disease_name, {
            'symptoms': 'Please consult with agricultural expert for accurate diagnosis.',
            'causes': 'Unknown cause. Seek expert advice.',
            'prevention': 'Practice good crop management and regular monitoring.',
            'treatment': 'Consult with agricultural expert for proper treatment.'
        })