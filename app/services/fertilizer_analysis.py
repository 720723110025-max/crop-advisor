"""
Fertilizer analysis service for nutrient recommendations.
"""

import numpy as np
import pandas as pd
from app.services.ml_models import MLService
import logging

logger = logging.getLogger(__name__)

class FertilizerAnalysisService:
    """
    Service for fertilizer analysis and recommendations.
    """
    
    def __init__(self):
        """Initialize fertilizer analysis service."""
        self.ml_service = MLService()
        
        # Crop nutrient requirements (kg/ha)
        self.crop_requirements = {
            'rice': {'N': 120, 'P': 60, 'K': 60, 'S': 20, 'Zn': 5},
            'wheat': {'N': 150, 'P': 60, 'K': 40, 'S': 15, 'Zn': 5},
            'maize': {'N': 180, 'P': 80, 'K': 60, 'S': 20, 'Zn': 6},
            'sugarcane': {'N': 200, 'P': 100, 'K': 120, 'S': 30, 'Zn': 8},
            'cotton': {'N': 100, 'P': 60, 'K': 60, 'S': 10, 'Zn': 4},
            'vegetables': {'N': 150, 'P': 80, 'K': 100, 'S': 20, 'Zn': 6}
        }
    
    def recommend_fertilizer(self, crop_type, nitrogen, phosphorus, potassium, ph=7.0, organic_matter=0):
        """
        Recommend fertilizer based on soil nutrients and crop requirements.
        
        Args:
            crop_type (str): Type of crop
            nitrogen (float): Current nitrogen level (ppm)
            phosphorus (float): Current phosphorus level (ppm)
            potassium (float): Current potassium level (ppm)
            ph (float): Soil pH
            organic_matter (float): Organic matter percentage
        
        Returns:
            dict: Fertilizer recommendation
        """
        try:
            # Get crop requirements
            crop_req = self.crop_requirements.get(crop_type.lower(), 
                                                  self.crop_requirements['rice'])
            
            # Calculate nutrient deficiencies
            N_deficit = max(0, crop_req['N'] - nitrogen)
            P_deficit = max(0, crop_req['P'] - phosphorus)
            K_deficit = max(0, crop_req['K'] - potassium)
            
            # Determine which nutrient is most deficient
            deficits = {'Nitrogen': N_deficit, 'Phosphorus': P_deficit, 'Potassium': K_deficit}
            primary_deficit = max(deficits, key=deficits.get)
            
            # Select fertilizer based on primary deficit
            if primary_deficit == 'Nitrogen':
                fertilizer_name = 'Urea (46% N)'
                quantity = (N_deficit / 0.46) * 1.2  # 20% buffer
                application_method = 'Broadcast and incorporate into soil'
            elif primary_deficit == 'Phosphorus':
                fertilizer_name = 'DAP (18% N, 46% P2O5)'
                quantity = (P_deficit / 0.46) * 1.2
                application_method = 'Broadcast and incorporate into soil'
            else:
                fertilizer_name = 'MOP (60% K2O)'
                quantity = (K_deficit / 0.60) * 1.2
                application_method = 'Broadcast and incorporate into soil'
            
            # Adjust for pH
            if ph < 6.0 and primary_deficit != 'Nitrogen':
                application_method += ' (Consider lime application for pH correction)'
            elif ph > 7.5 and primary_deficit != 'Nitrogen':
                application_method += ' (Consider sulfur application for pH correction)'
            
            # Generate schedule
            schedule = self._generate_application_schedule(crop_type, primary_deficit)
            
            return {
                'fertilizer_name': fertilizer_name,
                'quantity': round(quantity, 2),
                'unit': 'kg/ha',
                'application_method': application_method,
                'application_schedule': schedule,
                'frequency': self._get_application_frequency(crop_type),
                'expected_improvement': self._get_expected_improvement(primary_deficit, crop_type)
            }
            
        except Exception as e:
            logger.error(f"Error in fertilizer recommendation: {str(e)}")
            return {
                'fertilizer_name': 'Balanced NPK Fertilizer (10-10-10)',
                'quantity': 100,
                'unit': 'kg/ha',
                'application_method': 'Broadcast and incorporate into soil',
                'application_schedule': 'Apply at planting and 30 days after planting',
                'frequency': 'Bi-annual',
                'expected_improvement': 'Improved crop growth and yield'
            }
    
    def _generate_application_schedule(self, crop_type, nutrient_type):
        """
        Generate fertilizer application schedule.
        """
        schedules = {
            'rice': {
                'Nitrogen': 'Apply 30% at planting, 40% at tillering, 30% at panicle initiation.',
                'Phosphorus': 'Apply 100% at planting.',
                'Potassium': 'Apply 50% at planting, 50% at panicle initiation.'
            },
            'wheat': {
                'Nitrogen': 'Apply 30% at planting, 40% at tillering, 30% at booting.',
                'Phosphorus': 'Apply 100% at planting.',
                'Potassium': 'Apply 100% at planting.'
            },
            'maize': {
                'Nitrogen': 'Apply 30% at planting, 40% at knee-high, 30% at tasseling.',
                'Phosphorus': 'Apply 100% at planting.',
                'Potassium': 'Apply 100% at planting.'
            }
        }
        
        crop_schedule = schedules.get(crop_type.lower(), schedules['rice'])
        return crop_schedule.get(nutrient_type, 'Apply as per local agricultural recommendations.')
    
    def _get_application_frequency(self, crop_type):
        """
        Get application frequency based on crop type.
        """
        frequencies = {
            'rice': 'Every 30-45 days',
            'wheat': 'Every 45-60 days',
            'maize': 'Every 30-45 days',
            'sugarcane': 'Every 30-45 days',
            'cotton': 'Every 45-60 days',
            'vegetables': 'Every 15-30 days'
        }
        return frequencies.get(crop_type.lower(), 'Every 30-45 days')
    
    def _get_expected_improvement(self, nutrient_type, crop_type):
        """
        Get expected improvement from fertilizer application.
        """
        improvements = {
            'Nitrogen': 'Increased vegetative growth and higher protein content.',
            'Phosphorus': 'Better root development and improved flowering.',
            'Potassium': 'Improved disease resistance and better fruit quality.'
        }
        return improvements.get(nutrient_type, 'Overall improvement in crop health and yield.')