"""
Services package — lazy imports to avoid crashing on missing TensorFlow / heavy deps.
"""

__all__ = [
    'WeatherService',
]


def __getattr__(name):
    if name == 'WeatherService':
        from app.services.weather_service import WeatherService
        return WeatherService
    raise AttributeError(name)
