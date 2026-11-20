"""
Weather Service & Agromet Advisory Engine
Provides 5-day agro-meteorological forecasts, rain predictions, and irrigation/spray advisories.
"""

from typing import Dict, Any, List
import datetime

DISTRICT_WEATHER_DATA = {
    "इंदौर , मध्य प्रदेश": {"temp": 28, "humidity": 62, "soil_moisture": 32, "rain_3day_mm": 18, "condition": "आंशिक बादल (Partly Cloudy)", "wind_kmh": 12},
    "भोपाल , मध्य प्रदेश": {"temp": 29, "humidity": 58, "soil_moisture": 30, "rain_3day_mm": 12, "condition": "धूप (Sunny)", "wind_kmh": 10},
    "उज्जैन , मध्य प्रदेश": {"temp": 27, "humidity": 65, "soil_moisture": 34, "rain_3day_mm": 22, "condition": "हल्की बारिश (Light Showers)", "wind_kmh": 14},
    "जयपुर , राजस्थान": {"temp": 32, "humidity": 40, "soil_moisture": 22, "rain_3day_mm": 0, "condition": "गर्म व शुष्क (Dry & Clear)", "wind_kmh": 16},
    "करनाल , हरियाणा": {"temp": 26, "humidity": 70, "soil_moisture": 38, "rain_3day_mm": 15, "condition": "बादल छाए रहेंगे (Cloudy)", "wind_kmh": 8},
    "नासिक , महाराष्ट्र": {"temp": 26, "humidity": 68, "soil_moisture": 35, "rain_3day_mm": 25, "condition": "रिमझिम बारिश (Drizzle)", "wind_kmh": 15},
    "वाराणसी , उत्तर प्रदेश": {"temp": 30, "humidity": 60, "soil_moisture": 28, "rain_3day_mm": 5, "condition": "साफ आसमान (Clear)", "wind_kmh": 9}
}

class WeatherAdvisoryService:
    def __init__(self):
        pass

    def get_weather_advisory(self, location: str = "इंदौर , मध्य प्रदेश") -> Dict[str, Any]:
        info = DISTRICT_WEATHER_DATA.get(location, DISTRICT_WEATHER_DATA["इंदौर , मध्य प्रदेश"])
        
        # 5-Day Forecast Generation
        today = datetime.date.today()
        days_hi = ["सोम", "मंगल", "बुध", "गुरु", "शुक्र", "शनि", "रवि"]
        
        forecast = []
        for i in range(5):
            day_date = today + datetime.timedelta(days=i)
            day_name = days_hi[day_date.weekday()]
            
            # Forecast dynamics
            day_temp = info["temp"] + (i % 3 - 1)
            rain_chance = max(10, min(90, int(info["rain_3day_mm"] * 3.5 - i * 8)))
            rain_mm = round(max(0.0, info["rain_3day_mm"] * (0.5 - i * 0.1)), 1)
            
            forecast.append({
                "day": f"{day_name} ({day_date.strftime('%d %b')})",
                "temp_max": day_temp + 3,
                "temp_min": day_temp - 6,
                "rain_chance_pct": rain_chance,
                "rain_mm": rain_mm,
                "icon": "rainy" if rain_chance > 50 else ("partly_cloudy_day" if rain_chance > 25 else "sunny")
            })

        # Agromet Advisories
        irrigation_advice_hi = ""
        if info["rain_3day_mm"] > 15:
            irrigation_advice_hi = f"अगले 3 दिनों में लगभग {info['rain_3day_mm']} मिमी बारिश की संभावना है। कृपया सिंचाई 2 दिनों के लिए टालें और जल निकासी नाली साफ रखें।"
        elif info["soil_moisture"] < 25:
            irrigation_advice_hi = "मिट्टी में नमी 25% से कम है। 24 घंटे के भीतर हल्की सिंचाई तुरंत करें।"
        else:
            irrigation_advice_hi = "मिट्टी में पर्याप्त नमी है। नियमित अंतराल पर ही हल्की सिंचाई करें।"

        spray_window_hi = ""
        if info["wind_kmh"] > 15 or info["rain_3day_mm"] > 10:
            spray_window_hi = "तेज हवा या बारिश की संभावना के कारण आज कीटनाशक/फफूंदनाशक का छिड़काव न करें।"
        else:
            spray_window_hi = "सुबह 7 से 10 बजे के बीच छिड़काव के लिए मौसम सर्वोत्तम है।"

        return {
            "location": location,
            "current": {
                "temperature_c": info["temp"],
                "humidity_pct": info["humidity"],
                "soil_moisture_pct": info["soil_moisture"],
                "rain_3day_mm": info["rain_3day_mm"],
                "condition": info["condition"],
                "wind_kmh": info["wind_kmh"],
                "soil_moisture_label": "अच्छी (Good)" if info["soil_moisture"] >= 30 else "कम (Low)"
            },
            "advisories": {
                "irrigation_hi": irrigation_advice_hi,
                "spray_window_hi": spray_window_hi,
                "sowing_hi": "वर्तमान मौसम बीज अंकुरण और वानस्पतिक वृद्धि के लिए अत्यंत अनुकूल है।"
            },
            "forecast_5days": forecast,
            "available_locations": list(DISTRICT_WEATHER_DATA.keys())
        }

weather_service = WeatherAdvisoryService()
