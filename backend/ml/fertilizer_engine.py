"""
Fertilizer & Soil Nutrient Optimization Engine
Calculates soil deficits and generates customized split-dose fertilizer schedules.
Includes commercial fertilizer conversions (Urea, DAP, MOP, SSP), cost estimates, and organic amendments.
"""

from typing import Dict, Any, List

CROP_NUTRIENT_REQUIREMENTS = {
    "Wheat": {"n": 50, "p": 25, "k": 18, "zinc": 5, "name_hi": "गेहूं", "stages": ["बुवाई के समय (Basal)", "पहली सिंचाई / 21 दिन (CRI)", "दूसरी सिंचाई / 45 दिन (Booting)"]},
    "Rice": {"n": 48, "p": 24, "k": 20, "zinc": 6, "name_hi": "चावल / धान", "stages": ["रोपाई के समय (Basal)", "कल्ले फूटते समय / 25 दिन (Tillering)", "गोभ अवस्था / 45 दिन (Panicle)"]},
    "Maize": {"n": 45, "p": 24, "k": 16, "zinc": 5, "name_hi": "मक्का", "stages": ["बुवाई के समय", "घुटने तक ऊंचाई / 30 दिन", "नरमंजरी / 50 दिन"]},
    "Mustard": {"n": 35, "p": 18, "k": 15, "zinc": 4, "sulphur": 10, "name_hi": "सरसों", "stages": ["बुवाई के समय", "पहली सिंचाई / 30 दिन"]},
    "Cotton": {"n": 40, "p": 20, "k": 20, "zinc": 5, "name_hi": "कपास", "stages": ["बुवाई के समय", "शाखाएं बनते समय / 35 दिन", "फूल व टिंडे बनते समय / 60 दिन"]},
    "Sugarcane": {"n": 100, "p": 45, "k": 45, "zinc": 10, "name_hi": "गन्ना", "stages": ["बुवाई के समय", "45 दिन पर", "90 दिन पर", "120 दिन पर मिट्टी चढ़ाते समय"]},
    "Soybean": {"n": 12, "p": 28, "k": 18, "zinc": 4, "sulphur": 8, "name_hi": "सोयाबीन", "stages": ["बुवाई के समय (Basal)"]},
    "Chickpea": {"n": 10, "p": 25, "k": 15, "zinc": 3, "name_hi": "चना", "stages": ["बुवाई के समय (Basal)"]}
}

class FertilizerAdvisoryEngine:
    def __init__(self):
        pass

    def calculate_plan(self, n_soil: float, p_soil: float, k_soil: float, 
                       ph: float, farm_size_acres: float = 2.5, 
                       crop: str = "Wheat", soil_type: str = "दोमट (Loamy)") -> Dict[str, Any]:
        """
        Computes nutrient deficits, soil health score, commercial fertilizer bags,
        and chronological application splits.
        """
        crop_req = CROP_NUTRIENT_REQUIREMENTS.get(crop, CROP_NUTRIENT_REQUIREMENTS["Wheat"])
        
        # Soil health categorization
        n_status = "कम (Deficient)" if n_soil < 50 else ("सामान्य (Optimal)" if n_soil <= 100 else "अधिक (High)")
        p_status = "कम (Deficient)" if p_soil < 25 else ("सामान्य (Optimal)" if p_soil <= 50 else "अधिक (High)")
        k_status = "कम (Deficient)" if k_soil < 25 else ("सामान्य (Optimal)" if k_soil <= 50 else "अधिक (High)")

        # Calculate deficiency multiplier
        n_factor = 1.25 if n_soil < 50 else (1.0 if n_soil <= 100 else 0.75)
        p_factor = 1.25 if p_soil < 25 else (1.0 if p_soil <= 50 else 0.75)
        k_factor = 1.25 if k_soil < 25 else (1.0 if k_soil <= 50 else 0.75)

        # Net nutrient demand per acre in kg
        net_n_per_acre = crop_req["n"] * n_factor
        net_p_per_acre = crop_req["p"] * p_factor
        net_k_per_acre = crop_req["k"] * k_factor

        # Total farm demand
        total_n = net_n_per_acre * farm_size_acres
        total_p = net_p_per_acre * farm_size_acres
        total_k = net_k_per_acre * farm_size_acres

        # Convert to commercial fertilizers:
        # 1. DAP (18% N, 46% P2O5)
        dap_kg = (total_p / 0.46)
        n_from_dap = dap_kg * 0.18

        # 2. Remaining Nitrogen via Urea (46% N)
        remaining_n = max(0, total_n - n_from_dap)
        urea_kg = remaining_n / 0.46

        # 3. Potassium via MOP (60% K2O)
        mop_kg = total_k / 0.60

        # 4. Zinc Sulphate (21%)
        zinc_kg = (crop_req.get("zinc", 5)) * farm_size_acres

        # Bag counts (50kg standard bag)
        dap_bags = round(dap_kg / 50.0, 1)
        urea_bags = round(urea_kg / 50.0, 1)
        mop_bags = round(mop_kg / 50.0, 1)
        zinc_bags = round(zinc_kg / 25.0, 1) # 25kg bag

        # Soil health score (out of 100)
        n_score = min(30, (n_soil / 80.0) * 30)
        p_score = min(25, (p_soil / 40.0) * 25)
        k_score = min(25, (k_soil / 40.0) * 25)
        ph_score = 20 if (6.5 <= ph <= 7.5) else (15 if (6.0 <= ph <= 8.0) else 10)
        health_score = int(n_score + p_score + k_score + ph_score)
        health_score = min(96, max(45, health_score))

        # Split Application Schedule
        schedule = [
            {
                "stage_hi": "1. बुवाई के समय (Basal Dose)",
                "timing": "बुवाई / रोपाई से ठीक पहले",
                "items_hi": [
                    f"DAP: {round(dap_kg, 1)} कि.ग्रा. ({dap_bags} बोरी)",
                    f"MOP (पोटाश): {round(mop_kg, 1)} कि.ग्रा. ({mop_bags} बोरी)",
                    f"यूरिया: {round(urea_kg * 0.33, 1)} कि.ग्रा. (1/3 हिस्सा)",
                    f"जिंक सल्फेट: {round(zinc_kg, 1)} कि.ग्रा."
                ],
                "instructions_hi": "DAP और पोटाश को बीज के 2-3 इंच नीचे मिट्टी में अच्छी तरह मिलाएं। जिंक को DAP के साथ सीधे न मिलाएं, 2-3 दिन बाद दें।"
            },
            {
                "stage_hi": "2. पहली सिंचाई / 20-25 दिन बाद (Top Dressing 1)",
                "timing": "पहली सिंचाई के तुरंत बाद (ओट आने पर)",
                "items_hi": [
                    f"यूरिया: {round(urea_kg * 0.33, 1)} कि.ग्रा. (1/3 हिस्सा)",
                    "नैनो यूरिया (वैकल्पिक): 4 मिली/लीटर पानी"
                ],
                "instructions_hi": "खेत में हल्की नमी होने पर यूरिया का समान छिड़काव करें ताकि पौधों में कल्ले तेजी से फूटें।"
            },
            {
                "stage_hi": "3. दूसरी सिंचाई / 40-45 दिन बाद (Top Dressing 2)",
                "timing": "गाभा / बाली बनने की शुरुआती अवस्था",
                "items_hi": [
                    f"यूरिया: {round(urea_kg * 0.34, 1)} कि.ग्रा. (शेष 1/3 हिस्सा)",
                    "घुलनशील पोटाश 00:00:50 (10 ग्राम/लीटर) पर्णीय छिड़काव"
                ],
                "instructions_hi": "अंतिम यूरिया दें। दानों के भराव और चमक के लिए पोटाश का स्प्रे लाभप्रद रहेगा।"
            }
        ]

        # Estimated Market Cost
        # Subsidized approx rates: Urea ₹266/bag, DAP ₹1350/bag, MOP ₹1700/bag, Zinc ₹40/kg
        est_cost = int((urea_bags * 266) + (dap_bags * 1350) + (mop_bags * 1700) + (zinc_kg * 40))
        unguided_excess_cost = int(est_cost * 1.35)
        savings = unguided_excess_cost - est_cost

        # Soil conditioning tips
        ph_remedy_hi = ""
        if ph < 6.0:
            ph_remedy_hi = "मिट्टी अम्लीय (Acidic) है। 2-3 क्विंटल प्रति एकड़ चूना (Agricultural Lime) मिलाएं।"
        elif ph > 8.0:
            ph_remedy_hi = "मिट्टी क्षारीय (Alkaline) है। 1.5-2 क्विंटल प्रति एकड़ जिप्सम (Gypsum) डालें।"
        else:
            ph_remedy_hi = "मिट्टी का pH संतुलित (आदर्श) है।"

        organic_remedy_hi = f"मिट्टी में जैविक कार्बन सुधारने हेतु प्रति एकड़ 4-5 ट्रॉली अच्छी सड़ी गोबर खाद (FYM) या 1 टन वर्मीकम्पोस्ट डालें।"

        return {
            "crop": crop,
            "crop_hi": crop_req["name_hi"],
            "farm_size_acres": farm_size_acres,
            "soil_type": soil_type,
            "soil_health_score": health_score,
            "soil_health_label": "अच्छा (Good)" if health_score >= 75 else ("मध्यम (Moderate)" if health_score >= 60 else "सुधार योग्य (Needs Care)"),
            "nutrient_status": {
                "nitrogen": {"value": n_soil, "status": n_status},
                "phosphorus": {"value": p_soil, "status": p_status},
                "potassium": {"value": k_soil, "status": k_status},
                "ph": {"value": ph, "remedy_hi": ph_remedy_hi}
            },
            "fertilizer_requirements": {
                "urea_kg": round(urea_kg, 1),
                "urea_bags": urea_bags,
                "dap_kg": round(dap_kg, 1),
                "dap_bags": dap_bags,
                "mop_kg": round(mop_kg, 1),
                "mop_bags": mop_bags,
                "zinc_kg": round(zinc_kg, 1)
            },
            "schedule": schedule,
            "organic_remedy_hi": organic_remedy_hi,
            "cost_analysis": {
                "estimated_cost_inr": est_cost,
                "estimated_savings_inr": savings,
                "savings_text_hi": f"संतुलित खाद प्रयोग से आप लगभग ₹{savings:,} की अनावश्यक खाद लागत बचा रहे हैं।"
            },
            "voice_text_hi": f"आपके {farm_size_acres} एकड़ {crop_req['name_hi']} के खेत के लिए {urea_bags} बोरी यूरिया, {dap_bags} बोरी डीएपी और {mop_bags} बोरी पोटाश की संस्तुति है। डीएपी और पोटाश बुवाई के समय दें।"
        }

fertilizer_engine = FertilizerAdvisoryEngine()
