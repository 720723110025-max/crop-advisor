"""
Weather service for fetching and processing weather data.
"""

import os
import requests
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Service for fetching weather data from OpenWeatherMap API.
    """
    
    def __init__(self):
        """Initialize weather service with API key."""
        self.api_key = os.environ.get('OPENWEATHER_API_KEY', '')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
        self.units = 'metric'  # Celsius
        
    def get_current_weather(self, location, lat=None, lon=None):
        """
        Get current weather for a location or coordinates.
        
        Args:
            location (str): City name or coordinates
            lat (float): Latitude
            lon (float): Longitude
        
        Returns:
            dict: Current weather data
        """
        try:
            if not self.api_key or self.api_key == 'your_api_key_here':
                loc_str = location or (f"{lat},{lon}" if (lat and lon) else "New York")
                return self._generate_fake_weather(loc_str)
            
            url = f"{self.base_url}/weather"
            params = {
                'appid': self.api_key,
                'units': self.units
            }
            if lat and lon:
                params['lat'] = lat
                params['lon'] = lon
            else:
                params['q'] = location
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'location': data.get('name', location or f"{lat},{lon}"),
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'condition': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 10000) / 1000, # Convert meters to km
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {str(e)}")
            loc_str = location or (f"{lat},{lon}" if (lat and lon) else "New York")
            return self._generate_fake_weather(loc_str)
        except Exception as e:
            logger.error(f"Error processing weather data: {str(e)}")
            return self._generate_fake_weather(location)
    
    def get_forecast(self, location, days=5):
        """
        Get weather forecast for a location.
        
        Args:
            location (str): City name or coordinates
            days (int): Number of days forecast
        
        Returns:
            list: Forecast data
        """
        try:
            if not self.api_key or self.api_key == 'your_api_key_here':
                return self._generate_fake_forecast(location, days)
            
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': self.units,
                'cnt': days * 8  # 3-hour intervals
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            forecast = []
            for item in data['list'][:days * 8:8]:  # Daily forecast
                date = datetime.fromtimestamp(item['dt'])
                forecast.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'day': date.strftime('%A'),
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'condition': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'precipitation': item.get('rain', {}).get('3h', 0),
                    'wind_speed': item['wind']['speed']
                })
            
            return forecast
            
        except Exception as e:
            logger.error(f"Error fetching forecast: {str(e)}")
            return self._generate_fake_forecast(location, days)
    
    def get_farming_recommendations(self, weather_data):
        """
        Generate farming recommendations based on weather.
        
        Args:
            weather_data (dict): Current weather data
        
        Returns:
            list: Farming recommendations
        """
        recommendations = []
        
        if not weather_data:
            return ['Weather data not available for recommendations.']
        
        temp = weather_data.get('temperature', 25)
        humidity = weather_data.get('humidity', 60)
        condition = weather_data.get('condition', '').lower()
        wind_speed = weather_data.get('wind_speed', 5)
        
        # Temperature-based recommendations
        if temp > 35:
            recommendations.append("⚠️ High temperature! Provide shade and increase irrigation.")
        elif temp < 10:
            recommendations.append("⚠️ Low temperature! Use protective covers if needed.")
        elif 20 <= temp <= 30:
            recommendations.append("✅ Optimal temperature range for most crops.")
        
        # Humidity recommendations
        if humidity > 80:
            recommendations.append("⚠️ High humidity! Monitor for fungal diseases.")
        elif humidity < 40:
            recommendations.append("⚠️ Low humidity! Increase irrigation frequency.")
        elif 50 <= humidity <= 70:
            recommendations.append("✅ Optimal humidity level for crop growth.")
        
        # Weather condition recommendations
        if 'rain' in condition:
            recommendations.append("📊 Rain expected. Ensure proper drainage.")
            recommendations.append("💧 Reduce irrigation if rainfall is significant.")
        elif 'clear' in condition or 'sun' in condition:
            recommendations.append("☀️ Sunny weather. Great for field activities.")
            recommendations.append("💧 Consider irrigation if soil is dry.")
        
        if 'wind' in condition or wind_speed > 20:
            recommendations.append("💨 Strong winds! Consider windbreaks.")
            recommendations.append("⚠️ Check for crop lodging risks.")
        
        # General recommendations
        recommendations.append("📊 Monitor soil moisture regularly.")
        recommendations.append("🌱 Plan pest control activities.")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _generate_fake_weather(self, location):
        """
        Generate fake weather data when API is unavailable.
        """
        import random
        return {
            'location': location,
            'temperature': round(random.uniform(15, 35), 1),
            'feels_like': round(random.uniform(15, 35), 1),
            'humidity': random.randint(40, 80),
            'pressure': random.randint(1000, 1020),
            'condition': 'Partly cloudy',
            'icon': '02d',
            'wind_speed': random.randint(3, 15),
            'wind_direction': random.randint(0, 360),
            'visibility': random.randint(5, 15),
            'sunrise': '06:00',
            'sunset': '18:00',
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_fake_forecast(self, location, days):
        """
        Generate fake forecast data when API is unavailable.
        """
        import random
        forecast = []
        conditions = ['Sunny', 'Partly cloudy', 'Cloudy', 'Rainy', 'Light drizzle']
        
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': date.strftime('%A'),
                'temperature': round(random.uniform(15, 35), 1),
                'humidity': random.randint(40, 80),
                'condition': random.choice(conditions),
                'icon': '02d',
                'precipitation': round(random.uniform(0, 20), 1),
                'wind_speed': random.randint(3, 15)
            })
        
        return forecast