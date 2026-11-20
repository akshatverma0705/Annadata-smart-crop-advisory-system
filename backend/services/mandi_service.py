"""
Mandi Market Rates & Price Trend Tracker
Provides APMC market arrivals, minimum/maximum/modal prices, MSP comparisons, and market trend forecasts.
"""

from typing import Dict, Any, List

MANDI_RATES_DATA = {
    "Wheat": {
        "crop_hi": "गेहूं",
        "msp_inr": 2275,
        "modal_price_inr": 2480,
        "min_price_inr": 2350,
        "max_price_inr": 2620,
        "trend": "rising",
        "trend_pct": "+2.8%",
        "mandis": [
            {"mandi": "इंदौर मंडी (Indore APMC)", "state": "मध्य प्रदेश", "distance_km": 12, "modal_price": 2510, "arrival_tonnes": 450},
            {"mandi": "उज्जैन मंडी (Ujjain APMC)", "state": "मध्य प्रदेश", "distance_km": 54, "modal_price": 2470, "arrival_tonnes": 380},
            {"mandi": "देवास मंडी (Dewas APMC)", "state": "मध्य प्रदेश", "distance_km": 36, "modal_price": 2490, "arrival_tonnes": 220},
            {"mandi": "भोपाल मंडी (Karond APMC)", "state": "मध्य प्रदेश", "distance_km": 185, "modal_price": 2460, "arrival_tonnes": 510}
        ]
    },
    "Soybean": {
        "crop_hi": "सोयाबीन",
        "msp_inr": 4892,
        "modal_price_inr": 4650,
        "min_price_inr": 4400,
        "max_price_inr": 4850,
        "trend": "stable",
        "trend_pct": "+0.4%",
        "mandis": [
            {"mandi": "इंदौर मंडी", "state": "मध्य प्रदेश", "distance_km": 12, "modal_price": 4680, "arrival_tonnes": 800},
            {"mandi": "धार मंडी", "state": "मध्य प्रदेश", "distance_km": 60, "modal_price": 4620, "arrival_tonnes": 410}
        ]
    },
    "Chickpea": {
        "crop_hi": "चना (Gram)",
        "msp_inr": 5440,
        "modal_price_inr": 5850,
        "min_price_inr": 5600,
        "max_price_inr": 6100,
        "trend": "rising",
        "trend_pct": "+3.5%",
        "mandis": [
            {"mandi": "इंदौर मंडी", "state": "मध्य प्रदेश", "distance_km": 12, "modal_price": 5900, "arrival_tonnes": 290},
            {"mandi": "उज्जैन मंडी", "state": "मध्य प्रदेश", "distance_km": 54, "modal_price": 5820, "arrival_tonnes": 180}
        ]
    },
    "Mustard": {
        "crop_hi": "सरसों",
        "msp_inr": 5650,
        "modal_price_inr": 5420,
        "min_price_inr": 5200,
        "max_price_inr": 5680,
        "trend": "falling",
        "trend_pct": "-1.2%",
        "mandis": [
            {"mandi": "जयपुर मंडी", "state": "राजस्थान", "distance_km": 580, "modal_price": 5450, "arrival_tonnes": 1200},
            {"mandi": "मुरैना मंडी", "state": "मध्य प्रदेश", "distance_km": 520, "modal_price": 5390, "arrival_tonnes": 650}
        ]
    },
    "Cotton": {
        "crop_hi": "कपास",
        "msp_inr": 7020,
        "modal_price_inr": 7250,
        "min_price_inr": 6900,
        "max_price_inr": 7550,
        "trend": "rising",
        "trend_pct": "+1.8%",
        "mandis": [
            {"mandi": "खरगोन मंडी", "state": "मध्य प्रदेश", "distance_km": 140, "modal_price": 7300, "arrival_tonnes": 520},
            {"mandi": "खंडवा मंडी", "state": "मध्य प्रदेश", "distance_km": 130, "modal_price": 7210, "arrival_tonnes": 380}
        ]
    },
    "Tomato": {
        "crop_hi": "टमाटर",
        "msp_inr": 0,
        "modal_price_inr": 1800,
        "min_price_inr": 1400,
        "max_price_inr": 2300,
        "trend": "rising",
        "trend_pct": "+8.2%",
        "mandis": [
            {"mandi": "इंदौर चोइथराम मंडी", "state": "मध्य प्रदेश", "distance_km": 8, "modal_price": 1850, "arrival_tonnes": 180},
            {"mandi": "नासिक पिंपलगांव मंडी", "state": "महाराष्ट्र", "distance_km": 420, "modal_price": 1950, "arrival_tonnes": 950}
        ]
    }
}

class MandiService:
    def __init__(self):
        pass

    def get_prices(self, crop: str = "Wheat") -> Dict[str, Any]:
        data = MANDI_RATES_DATA.get(crop, MANDI_RATES_DATA["Wheat"])
        return {
            "crop": crop,
            "crop_hi": data["crop_hi"],
            "modal_price_inr": data["modal_price_inr"],
            "min_price_inr": data["min_price_inr"],
            "max_price_inr": data["max_price_inr"],
            "msp_inr": data["msp_inr"],
            "trend": data["trend"],
            "trend_pct": data["trend_pct"],
            "trend_label_hi": "बढ़त पर (Bullish)" if data["trend"] == "rising" else ("स्थिर (Stable)" if data["trend"] == "stable" else "गिरावट (Bearish)"),
            "mandis": data["mandis"],
            "available_crops": list(MANDI_RATES_DATA.keys()),
            "voice_text_hi": f"{data['crop_hi']} का आज का मंडी भाव ₹{data['modal_price_inr']} प्रति क्विंटल है। बाजार में {data['trend_pct']} की प्रवृत्ति है।"
        }

mandi_service = MandiService()
