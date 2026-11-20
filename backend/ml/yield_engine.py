"""
Yield Estimation & Harvest Projection Engine
Calculates expected crop yield (quintals/acre) and generates growth curve projections.
"""

from typing import Dict, Any, List

CROP_BASELINE_YIELDS = {
    # Base yield, Max potential, Unit
    "Wheat": {"base": 28.0, "max": 42.0, "name_hi": "गेहूं", "unit": "क्विंटल / एकड़", "months": ["जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई"]},
    "Rice": {"base": 30.0, "max": 48.0, "name_hi": "धान / चावल", "unit": "क्विंटल / एकड़", "months": ["जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर"]},
    "Maize": {"base": 32.0, "max": 45.0, "name_hi": "मक्का", "unit": "क्विंटल / एकड़", "months": ["जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर"]},
    "Mustard": {"base": 12.0, "max": 18.5, "name_hi": "सरसों", "unit": "क्विंटल / एकड़", "months": ["अक्टूबर", "नवंबर", "दिसंबर", "जनवरी", "फरवरी"]},
    "Cotton": {"base": 14.0, "max": 24.0, "name_hi": "कपास", "unit": "क्विंटल / एकड़", "months": ["जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर"]},
    "Soybean": {"base": 10.5, "max": 16.0, "name_hi": "सोयाबीन", "unit": "क्विंटल / एकड़", "months": ["जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर"]},
    "Sugarcane": {"base": 350.0, "max": 520.0, "name_hi": "गन्ना", "unit": "क्विंटल / एकड़", "months": ["मई", "जुलाई", "सितंबर", "नवंबर", "जनवरी"]}
}

class YieldEstimationEngine:
    def __init__(self):
        pass

    def estimate_yield(self, crop: str = "Wheat", soil_score: float = 78.0, 
                       irrigation_quality: str = "उत्तम (Assured)", 
                       fertilizer_adherence: float = 0.92,
                       weather_risk_factor: float = 0.95,
                       farm_size_acres: float = 2.5) -> Dict[str, Any]:
        
        info = CROP_BASELINE_YIELDS.get(crop, CROP_BASELINE_YIELDS["Wheat"])
        base = info["base"]
        max_potential = info["max"]

        # Factor multipliers
        soil_factor = 0.8 + (soil_score / 100.0) * 0.35 # 0.8 to 1.15
        
        irrig_multiplier = 1.08 if "उत्तम" in irrigation_quality or "Assured" in irrigation_quality else (1.0 if "मध्यम" in irrigation_quality else 0.82)
        fert_multiplier = 0.85 + (fertilizer_adherence * 0.25)
        
        # Total yield per acre
        est_yield_acre = base * soil_factor * irrig_multiplier * fert_multiplier * weather_risk_factor
        est_yield_acre = min(max_potential, max(base * 0.6, est_yield_acre))
        est_yield_acre = round(est_yield_acre, 1)

        total_production = round(est_yield_acre * farm_size_acres, 1)

        # Status
        if est_yield_acre >= base * 1.15:
            status_hi = "उत्कृष्ट (Excellent)"
        elif est_yield_acre >= base * 0.95:
            status_hi = "अच्छी (Good)"
        else:
            status_hi = "औसत (Average - सुधार योग्य)"

        # Generate Monthly Progression Curve Points (for 5 months)
        # S-Curve growth: 15% -> 40% -> 68% -> 88% -> 100% of final yield weight
        months = info["months"]
        ratios = [0.15, 0.40, 0.65, 0.88, 1.0]
        curve_points = []
        svg_points = []
        
        # SVG coordinate space: x from 20 to 380, y from 175 (0%) to 20 (100%)
        # Map monthly value to y
        for i, (m, r) in enumerate(zip(months, ratios)):
            val = round(est_yield_acre * r, 1)
            curve_points.append({"month": m, "yield_val": val})
            x_coord = 20 + i * 90
            # 0 is y=175, max is y=20 (height ~155 px)
            y_coord = int(175 - ((val / max_potential) * 155))
            svg_points.append({"x": x_coord, "y": max(15, min(175, y_coord)), "month": m, "val": val})

        svg_polyline = " ".join([f"{p['x']},{p['y']}" for p in svg_points])

        return {
            "crop": crop,
            "crop_hi": info["name_hi"],
            "farm_size_acres": farm_size_acres,
            "estimated_yield_per_acre": est_yield_acre,
            "total_farm_production": total_production,
            "unit": info["unit"],
            "status_hi": status_hi,
            "district_average": round(base * 0.96, 1),
            "max_potential": max_potential,
            "factors": [
                {"name": "मिट्टी स्वास्थ्य", "score": f"{int(soil_score)}/100", "impact": "सकारात्मक (+8%)"},
                {"name": "मौसम स्थिति", "score": "अनुकूल", "impact": "सामान्य (+4%)"},
                {"name": "सिंचाई व्यवस्था", "score": irrigation_quality, "impact": "सकारात्मक (+6%)"},
                {"name": "खाद प्रबंधन", "score": f"{int(fertilizer_adherence * 100)}% अनुपालन", "impact": "सकारात्मक (+7%)"}
            ],
            "curve_points": curve_points,
            "svg_polyline": svg_polyline,
            "svg_points": svg_points,
            "voice_text_hi": f"आपके {farm_size_acres} एकड़ खेत में {info['name_hi']} की अनुमानित उपज {est_yield_acre} क्विंटल प्रति एकड़ रहेगी। कुल अनुमानित पैदावार {total_production} क्विंटल होगी।"
        }

yield_engine = YieldEstimationEngine()
