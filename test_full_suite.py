"""
Comprehensive Full Suite Automated Verification for Annadata Platform
"""

import sys
import io
import requests

# Fix windows terminal encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_all():
    print("==================================================")
    print(" ANNADATA FULL-STACK INTEGRATION TEST SUITE")
    print("==================================================")

    # 1. Health
    r = requests.get(f"{BASE_URL}/api/health")
    assert r.status_code == 200, f"Health failed: {r.status_code}"
    print(f"✅ [1/10] /api/health -> 200 OK | Database: {r.json().get('database')}")

    # 2. Frontend HTML Routes
    for page in ["/", "/login", "/admin", "/home.css", "/app.js"]:
        r = requests.get(f"{BASE_URL}{page}")
        assert r.status_code == 200, f"Page {page} failed: {r.status_code}"
        print(f"✅ [2/10] Route '{page}' -> 200 OK ({len(r.content)} bytes)")

    # 3. Farmer Auth
    r = requests.post(f"{BASE_URL}/api/auth/farmer/login", json={"phone": "9520412093", "password": "kisan123"})
    assert r.status_code == 200 and r.json().get("success"), f"Farmer login failed: {r.text}"
    farmer = r.json()["farmer"]
    print(f"✅ [3/10] Farmer Login -> Success ({farmer['name']}, {farmer['location']})")

    # 4. Admin Auth
    r = requests.post(f"{BASE_URL}/api/auth/admin/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200 and r.json().get("success"), f"Admin login failed: {r.text}"
    admin = r.json()["admin"]
    print(f"✅ [4/10] Admin Login -> Success ({admin['full_name']}, {admin['role']})")

    # 5. Admin Dashboard Stats
    r = requests.get(f"{BASE_URL}/api/admin/dashboard-stats")
    assert r.status_code == 200
    stats = r.json()
    print(f"✅ [5/10] Admin DB Stats -> Total Farmers: {stats['total_farmers']}, Scans: {stats['total_scans']}, Mandis: {stats['total_mandi_entries']}")

    # 6. Dashboard Summary
    r = requests.get(f"{BASE_URL}/api/dashboard-summary")
    assert r.status_code == 200
    d_data = r.json()
    print(f"✅ [6/10] Dashboard Summary -> 5 Mini Cards & Weather ({d_data['weather']['current']['temperature_c']}°C)")

    # 7. AI Crop Recommendation
    r = requests.post(f"{BASE_URL}/api/recommend-crop", json={
        "nitrogen": 95, "phosphorus": 45, "potassium": 40,
        "temperature": 23, "humidity": 65, "ph": 6.8, "rainfall": 80
    })
    assert r.status_code == 200
    c_res = r.json()
    print(f"✅ [7/10] AI ML Crop Recommendation -> {c_res['recommended_crop_hi']} ({c_res['suitability_percentage']}%)")

    # 8. Leaf Disease Detection
    with open("frontend/assets/leaf.jpg", "rb") as f:
        r = requests.post(f"{BASE_URL}/api/detect-disease", files={"file": ("leaf.jpg", f, "image/jpeg")}, data={"crop_hint": "Wheat"})
    assert r.status_code == 200
    d_res = r.json()
    print(f"✅ [8/10] Leaf Disease Vision Model -> {d_res['disease_name_hi']} ({d_res['confidence_score']}%)")

    # 9. Fertilizer Schedule Plan
    r = requests.post(f"{BASE_URL}/api/fertilizer-plan", json={
        "nitrogen": 40, "phosphorus": 35, "potassium": 45, "ph": 6.8,
        "farm_size_acres": 2.5, "crop": "Wheat", "soil_type": "दोमट"
    })
    assert r.status_code == 200
    f_res = r.json()
    print(f"✅ [9/10] Fertilizer Optimization -> Urea: {f_res['fertilizer_requirements']['urea_bags']} bags, Savings: ₹{f_res['cost_analysis']['estimated_savings_inr']}")

    # 10. Mandi Rates & Yield Prediction
    r_mandi = requests.get(f"{BASE_URL}/api/mandi-prices?crop=Wheat")
    r_yield = requests.post(f"{BASE_URL}/api/yield-estimate", json={"crop": "Wheat", "soil_score": 78, "farm_size_acres": 2.5})
    assert r_mandi.status_code == 200 and r_yield.status_code == 200
    print(f"✅ [10/10] Mandi Rate: ₹{r_mandi.json()['modal_price_inr']}/qtl | Projected Yield: {r_yield.json()['estimated_yield_per_acre']} qtl/acre")

    print("\n🎉 ALL 10 TEST PHASES PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_all()
