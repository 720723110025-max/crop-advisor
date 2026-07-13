"""
Irrigation optimization service for smart water management.
"""

import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class IrrigationOptimizer:
    """
    Service for optimizing irrigation schedules based on crop, soil, and weather.
    """
    
    def __init__(self):
        """Initialize irrigation optimizer."""
        # Crop water requirements (mm per day)
        self.crop_water_requirements = {
            'rice': {'min': 4, 'max': 8, 'critical': 6},
            'wheat': {'min': 3, 'max': 6, 'critical': 4},
            'maize': {'min': 4, 'max': 7, 'critical': 5},
            'sugarcane': {'min': 6, 'max': 10, 'critical': 8},
            'cotton': {'min': 3, 'max': 6, 'critical': 4},
            'vegetables': {'min': 3, 'max': 5, 'critical': 4},
            'pulses': {'min': 2, 'max': 4, 'critical': 3},
            'fruits': {'min': 3, 'max': 6, 'critical': 4}
        }
        
        # Soil moisture thresholds by crop type
        self.moisture_thresholds = {
            'rice': {'min': 60, 'max': 100, 'critical': 75},
            'wheat': {'min': 50, 'max': 80, 'critical': 65},
            'maize': {'min': 55, 'max': 85, 'critical': 70},
            'sugarcane': {'min': 60, 'max': 90, 'critical': 75},
            'cotton': {'min': 50, 'max': 75, 'critical': 60},
            'vegetables': {'min': 55, 'max': 80, 'critical': 65},
            'pulses': {'min': 45, 'max': 70, 'critical': 55},
            'fruits': {'min': 50, 'max': 75, 'critical': 60}
        }
    
    def get_irrigation_advice(self, crop_type, soil_moisture, temperature, humidity, rainfall):
        """
        Get irrigation advice based on crop, soil, and weather conditions.
        
        Args:
            crop_type (str): Type of crop
            soil_moisture (float): Current soil moisture (%)
            temperature (float): Current temperature (°C)
            humidity (float): Current humidity (%)
            rainfall (float): Recent rainfall (mm)
        
        Returns:
            dict: Irrigation advice
        """
        try:
            # Get crop parameters
            crop_params = self.crop_water_requirements.get(
                crop_type.lower(), 
                {'min': 3, 'max': 6, 'critical': 4.5}
            )
            
            moisture_threshold = self.moisture_thresholds.get(
                crop_type.lower(),
                {'min': 50, 'max': 80, 'critical': 65}
            )
            
            # Calculate water requirement based on weather
            base_water_need = crop_params['critical']
            
            # Adjust for temperature
            temp_factor = 1.0
            if temperature > 30:
                temp_factor = 1.3
            elif temperature > 25:
                temp_factor = 1.15
            elif temperature < 15:
                temp_factor = 0.7
            
            # Adjust for humidity
            humidity_factor = 1.0
            if humidity < 40:
                humidity_factor = 1.2
            elif humidity > 80:
                humidity_factor = 0.7
            
            # Adjust for rainfall
            rainfall_factor = 1.0
            if rainfall > 20:
                rainfall_factor = 0.5
            elif rainfall > 10:
                rainfall_factor = 0.75
            elif rainfall > 5:
                rainfall_factor = 0.9
            
            # Calculate total water requirement
            water_requirement = base_water_need * temp_factor * humidity_factor * rainfall_factor
            
            # Check if irrigation is needed
            needs_irrigation = False
            timing_hours = 0
            duration_hours = 0
            
            if soil_moisture < moisture_threshold['critical']:
                needs_irrigation = True
                # Calculate when to irrigate (urgent)
                moisture_deficit = moisture_threshold['critical'] - soil_moisture
                timing_hours = max(0, 2 - moisture_deficit / 10)
                
                # Calculate irrigation duration
                duration_hours = (water_requirement / 10) * 0.5  # Rough estimate
                duration_hours = max(0.5, min(duration_hours, 3))
            
            # Determine irrigation method
            method = self._get_irrigation_method(crop_type, soil_moisture)
            
            # Generate notes
            notes = self._generate_irrigation_notes(
                needs_irrigation, 
                soil_moisture, 
                moisture_threshold,
                water_requirement
            )
            
            return {
                'needs_irrigation': needs_irrigation,
                'water_requirement': round(water_requirement, 1),
                'timing_hours': round(timing_hours, 1),
                'duration_hours': round(duration_hours, 1),
                'method': method,
                'notes': notes,
                'soil_moisture': soil_moisture,
                'critical_moisture': moisture_threshold['critical']
            }
            
        except Exception as e:
            logger.error(f"Error in irrigation advice: {str(e)}")
            return {
                'needs_irrigation': True,
                'water_requirement': 5.0,
                'timing_hours': 2,
                'duration_hours': 1,
                'method': 'Drip irrigation',
                'notes': 'Error in calculation. Please check manually.',
                'soil_moisture': soil_moisture,
                'critical_moisture': 60
            }
    
    def _get_irrigation_method(self, crop_type, soil_moisture):
        """
        Determine best irrigation method based on crop and soil conditions.
        """
        if crop_type.lower() == 'rice':
            return 'Flood irrigation'
        elif crop_type.lower() in ['vegetables', 'fruits']:
            return 'Drip irrigation'
        elif soil_moisture < 40:
            return 'Sprinkler irrigation'
        else:
            return 'Furrow irrigation'
    
    def _generate_irrigation_notes(self, needs_irrigation, soil_moisture, threshold, water_req):
        """
        Generate detailed irrigation notes.
        """
        notes = []
        
        if needs_irrigation:
            notes.append(f"⚠️ Irrigation needed. Current soil moisture: {soil_moisture}%")
            notes.append(f"💧 Water requirement: {water_req:.1f} mm per day")
            notes.append("🌱 Apply water slowly to avoid runoff")
            
            if soil_moisture < threshold['min']:
                notes.append("🚨 Critical moisture level! Irrigate immediately")
        else:
            notes.append(f"✅ Soil moisture is adequate at {soil_moisture}%")
            notes.append("📊 Continue monitoring soil moisture")
        
        # Add seasonal advice
        month = datetime.now().month
        if month in [3, 4, 5]:  # Spring
            notes.append("🌱 Spring season - increase irrigation for new growth")
        elif month in [6, 7, 8]:  # Summer
            notes.append("☀️ Summer season - irrigate early morning or evening")
        elif month in [9, 10, 11]:  # Fall
            notes.append("🍂 Fall season - reduce irrigation frequency")
        else:  # Winter
            notes.append("❄️ Winter season - irrigate only when necessary")
        
        return "\n".join(notes)
    
    def estimate_schedule(self, crop_type, start_date, duration_days):
        """
        Estimate irrigation schedule for a period.
        
        Args:
            crop_type (str): Type of crop
            start_date (datetime): Start date
            duration_days (int): Number of days
        
        Returns:
            list: Schedule of irrigation events
        """
        try:
            crop_params = self.crop_water_requirements.get(
                crop_type.lower(),
                {'min': 3, 'max': 6, 'critical': 4.5}
            )
            
            schedule = []
            current_date = start_date
            
            for day in range(duration_days):
                # Determine if irrigation is needed
                # Simplified: irrigate every 2-3 days based on crop
                if day % 2 == 0:  # Every 2 days
                    schedule.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'water_amount': round(crop_params['critical'] * 1.2, 1),
                        'duration_hours': round(crop_params['critical'] / 10, 1),
                        'method': self._get_irrigation_method(crop_type, 60)
                    })
                
                current_date += timedelta(days=1)
            
            return schedule
            
        except Exception as e:
            logger.error(f"Error estimating schedule: {str(e)}")
            return []