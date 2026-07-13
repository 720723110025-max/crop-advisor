from datetime import datetime

class WeatherModel:

    def get_weather(self):

        return {

            "location":"Coimbatore",

            "temperature":30,

            "humidity":74,

            "rainfall":20,

            "wind_speed":12,

            "condition":"Partly Cloudy",

            "updated_at":datetime.utcnow()

        }

    def irrigation_advice(self, weather):

        if weather["rainfall"] > 60:

            return "🌧 Heavy rainfall expected. Do not irrigate."

        elif weather["humidity"] > 80:

            return "💧 Soil moisture is high. Irrigation not required."

        elif weather["temperature"] > 35:

            return "☀ High temperature. Irrigate early morning."

        else:

            return "✅ Irrigate once every 3-5 days."