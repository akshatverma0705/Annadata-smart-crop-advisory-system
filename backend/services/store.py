"""
Farm Profile & Advisory History Store
Manages user farm profile, advisory logs, soil health cards, and historical scans.
"""

from typing import Dict, Any, List
import datetime

DEFAULT_FARM_PROFILE = {
    "farmer_name": "किसान भाई (Kisan Bhai)",
    "phone": "+91 9520412093",
    "location": "इंदौर , मध्य प्रदेश",
    "farm_size_acres": 2.5,
    "soil_type": "दोमट (Loamy)",
    "primary_crop": "गेहूं",
    "sowing_date": "15 नवंबर 2025",
    "last_updated": "12 मई 2026",
    "soil_health_score": 78,
    "crop_suitability_pct": 92
}

DEFAULT_ADVISORY_ITEMS = [
    {
        "id": "adv-crop",
        "category": "crop",
        "title_hi": "फसल सलाह",
        "title_en": "Crop Advisory",
        "icon": "eco",
        "icon_class": "green-icon",
        "summary_hi": "आपकी मिट्टी और मौसम के हिसाब से गेहूं की फसल उपयुक्त है।",
        "details_hi": "दोमट मिट्टी और 18-25°C तापमान में HD-3086 या DBW-187 किस्म 92% अनुकूलता के साथ अधिकतम 35 क्विंटल/एकड़ उपज देने में सक्षम है।",
        "action_label_hi": "विस्तार से देखें"
    },
    {
        "id": "adv-fert",
        "category": "fertilizer",
        "title_hi": "खाद सलाह",
        "title_en": "Fertilizer Advisory",
        "icon": "compost",
        "icon_class": "brown-icon",
        "summary_hi": "नाइट्रोजन की कमी है। 7 दिनों में यूरिया का उपयोग करें।",
        "details_hi": "मिट्टी परीक्षण में N का स्तर 42 किग्रा/एकड़ (कम) है। पहली सिंचाई के बाद प्रति एकड़ 30 किग्रा यूरिया या 4 मिली/लीटर नैनो यूरिया का पर्णीय छिड़काव करें।",
        "action_label_hi": "विस्तार से देखें"
    },
    {
        "id": "adv-irrig",
        "category": "irrigation",
        "title_hi": "सिंचाई सलाह",
        "title_en": "Irrigation Advisory",
        "icon": "water_drop",
        "icon_class": "blue-icon",
        "summary_hi": "मिट्टी में नमी 32% है। 2 दिनों में हल्की सिंचाई करें।",
        "details_hi": "गेहूं के कल्ले फूटने (Crown Root Initiation) की महत्वपूर्ण अवस्था पर 5-6 सेमी हल्की सिंचाई करें। तेज हवा होने पर सिंचाई न करें।",
        "action_label_hi": "विस्तार से देखें"
    },
    {
        "id": "adv-pest",
        "category": "pest",
        "title_hi": "कीट एवं रोग सलाह",
        "title_en": "Pest & Disease Advisory",
        "icon": "warning",
        "icon_class": "orange-icon",
        "summary_hi": "पत्तियों पर पीला/भूरा रतुआ (Rust) का खतरा है। खेत की नियमित जाँच करें।",
        "details_hi": "मौसम में उच्च आर्द्रता के कारण रतुआ फफूंद का खतरा बढ़ गया है। रोकथाम के लिए प्रोपिकोनाजोल 1 मिली/लीटर या 5 मिली नीम तेल का निवारक स्प्रे करें।",
        "action_label_hi": "विस्तार से देखें"
    },
    {
        "id": "adv-weather",
        "category": "weather",
        "title_hi": "मौसम सलाह",
        "title_en": "Weather Advisory",
        "icon": "cloud",
        "icon_class": "purple-icon",
        "summary_hi": "आने वाले 3 दिनों में 18 मिमी बारिश होने की संभावना है।",
        "details_hi": "मध्यम बारिश के पूर्वानुमान को देखते हुए सिंचाई स्थगित करें और कीटनाशक छिड़काव के लिए बारिश थमने की प्रतीक्षा करें।",
        "action_label_hi": "विस्तार से देखें"
    }
]

HISTORY_RECORDS = [
    {
        "id": "hist-001",
        "date": "12 मई 2026",
        "type_hi": "रोग पहचान (Leaf Rust)",
        "result_hi": "गेहूं की पत्ती रस्ट (94% विश्वास)",
        "action_taken_hi": "प्रोपिकोनाजोल 25% EC का छिड़काव किया गया"
    },
    {
        "id": "hist-002",
        "date": "28 अप्रैल 2026",
        "type_hi": "मिट्टी जाँच रिपोर्ट",
        "result_hi": "स्वास्थ्य स्कोर 78/100 (मध्यम N, पर्याप्त P/K)",
        "action_taken_hi": "डीएपी और पोटाश बेसल डोज पूरा किया"
    },
    {
        "id": "hist-003",
        "date": "15 मार्च 2026",
        "type_hi": "सिंचाई अलर्ट",
        "result_hi": "मिट्टी नमी 28% पर 45 मिमी सिंचाई अनुशंसित",
        "action_taken_hi": "ड्रिप सिंचाई द्वारा 2 घंटे जल प्रवाह"
    }
]

class DataStore:
    def __init__(self):
        self.profile = dict(DEFAULT_FARM_PROFILE)
        self.advisory = list(DEFAULT_ADVISORY_ITEMS)
        self.history = list(HISTORY_RECORDS)

    def get_profile(self) -> Dict[str, Any]:
        return self.profile

    def update_profile(self, new_data: Dict[str, Any]) -> Dict[str, Any]:
        self.profile.update(new_data)
        self.profile["last_updated"] = datetime.date.today().strftime("%d %B %Y")
        return self.profile

    def get_advisory(self) -> List[Dict[str, Any]]:
        return self.advisory

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def add_history(self, type_hi: str, result_hi: str, action_taken_hi: str):
        today_str = datetime.date.today().strftime("%d %B %Y")
        item = {
            "id": f"hist-{len(self.history) + 1:03d}",
            "date": today_str,
            "type_hi": type_hi,
            "result_hi": result_hi,
            "action_taken_hi": action_taken_hi
        }
        self.history.insert(0, item)
        return item

store = DataStore()
