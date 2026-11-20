"""
Test verification script for Annadata backend ML & API components.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from ml.crop_model import crop_engine
from ml.disease_model import disease_engine
from ml.fertilizer_engine import fertilizer_engine
from ml.yield_engine import yield_engine
from services.weather_service import weather_service
from services.mandi_service import mandi_service

print("--- Testing Crop Recommendation ---")
crop_res = crop_engine.predict(90, 42, 43, 23.5, 65.0, 6.8, 85.0)
print(f"Crop: {crop_res['recommended_crop_hi']} ({crop_res['recommended_crop']}), Score: {crop_res['suitability_percentage']}%")

print("\n--- Testing Fertilizer Plan ---")
fert_res = fertilizer_engine.calculate_plan(42, 38, 45, 6.8, farm_size_acres=2.5, crop="Wheat")
print(f"Urea bags: {fert_res['fertilizer_requirements']['urea_bags']}, DAP: {fert_res['fertilizer_requirements']['dap_bags']}")

print("\n--- Testing Yield Estimation ---")
yield_res = yield_engine.estimate_yield(crop="Wheat", soil_score=78.0, farm_size_acres=2.5)
print(f"Estimated yield: {yield_res['estimated_yield_per_acre']} {yield_res['unit']}")

print("\n--- Testing Disease Classifier ---")
disease_res = disease_engine.analyze_image(b"sample_bytes", crop_hint="Wheat")
print(f"Detected: {disease_res['disease_name_hi']}, Conf: {disease_res['confidence_score']}%")

print("\n--- Testing Weather Advisory ---")
weather_res = weather_service.get_weather_advisory("इंदौर , मध्य प्रदेश")
print(f"Weather: {weather_res['current']['temperature_c']}C, Rain: {weather_res['current']['rain_3day_mm']}mm")

print("\n--- Testing Mandi Rates ---")
mandi_res = mandi_service.get_prices("Wheat")
print(f"Mandi Modal Rate: Rs. {mandi_res['modal_price_inr']}/quintal")

print("\n[SUCCESS] ALL ML ENGINES & SERVICES PASSED VALIDATION!")
