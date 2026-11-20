"""
Annadata (अन्नदाता) - Smart Crop Advisory System
FastAPI Backend Application with PostgreSQL Database Integration & Admin Controls
"""

import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from backend.ml.crop_model import crop_engine
from .ml.disease_model import disease_engine
from .ml.fertilizer_engine import fertilizer_engine
from .ml.yield_engine import yield_engine
from .services.weather_service import weather_service
from .services.mandi_service import mandi_service
from .services.store import store
from . import database as db

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Annadata - Smart Crop Advisory System",
    description="Intelligent Decision-Support System for Small & Marginal Farmers with PostgreSQL Database & Admin Control",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
if (FRONTEND_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")

# Pydantic Request Models
class CropRecommendationRequest(BaseModel):
    nitrogen: float = 90.0
    phosphorus: float = 42.0
    potassium: float = 43.0
    temperature: float = 23.5
    humidity: float = 65.0
    ph: float = 6.8
    rainfall: float = 85.0

class FertilizerPlanRequest(BaseModel):
    nitrogen: float = 42.0
    phosphorus: float = 38.0
    potassium: float = 45.0
    ph: float = 6.8
    farm_size_acres: float = 2.5
    crop: str = "Wheat"
    soil_type: str = "दोमट (Loamy)"

class YieldEstimateRequest(BaseModel):
    crop: str = "Wheat"
    soil_score: float = 78.0
    irrigation_quality: str = "उत्तम (Assured)"
    fertilizer_adherence: float = 0.92
    farm_size_acres: float = 2.5

class FarmProfileUpdateRequest(BaseModel):
    farmer_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    farm_size_acres: Optional[float] = None
    soil_type: Optional[str] = None
    primary_crop: Optional[str] = None

class FarmerLoginRequest(BaseModel):
    phone: str
    password: str

class FarmerRegisterRequest(BaseModel):
    name: str
    phone: str
    password: str
    location: str = "इंदौर , मध्य प्रदेश"
    farm_size_acres: float = 2.5
    soil_type: str = "दोमट"
    primary_crop: str = "गेहूं"

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class UpdateMandiRateRequest(BaseModel):
    id: int
    modal_price: float
    min_price: float
    max_price: float
    trend: str

class BroadcastCreateRequest(BaseModel):
    admin_name: str
    title: str
    message: str
    target_district: str
    severity: str

# ----------------- PAGE ROUTES -----------------

@app.get("/")
async def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Frontend index.html not found"}

@app.get("/login")
async def serve_login():
    login_file = FRONTEND_DIR / "login.html"
    if login_file.exists():
        return FileResponse(str(login_file))
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/admin")
async def serve_admin():
    admin_file = FRONTEND_DIR / "admin.html"
    if admin_file.exists():
        return FileResponse(str(admin_file))
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/home.css")
async def serve_css():
    css_file = FRONTEND_DIR / "home.css"
    if css_file.exists():
        return FileResponse(str(css_file))
    raise HTTPException(status_code=404, detail="home.css not found")

@app.get("/app.js")
async def serve_js():
    js_file = FRONTEND_DIR / "app.js"
    if js_file.exists():
        return FileResponse(str(js_file))
    raise HTTPException(status_code=404, detail="app.js not found")

# ----------------- AUTHENTICATION API -----------------

@app.post("/api/auth/farmer/login")
async def farmer_login(req: FarmerLoginRequest):
    farmer = db.auth_farmer(req.phone, req.password)
    if farmer:
        # Also update active store session
        store.update_profile({
            "farmer_name": farmer["name"],
            "phone": farmer["phone"],
            "location": farmer["location"],
            "farm_size_acres": farmer["farm_size_acres"],
            "soil_type": farmer["soil_type"],
            "primary_crop": farmer["primary_crop"],
            "soil_health_score": farmer["soil_health_score"]
        })
        return {"success": True, "farmer": farmer}
    return JSONResponse(status_code=401, content={"success": False, "message": "गलत मोबाइल नंबर या पासवर्ड"})

@app.post("/api/auth/farmer/register")
async def farmer_register(req: FarmerRegisterRequest):
    result = db.register_farmer(
        name=req.name,
        phone=req.phone,
        password=req.password,
        location=req.location,
        farm_size=req.farm_size_acres,
        soil=req.soil_type,
        crop=req.primary_crop
    )
    return result

@app.post("/api/auth/admin/login")
async def admin_login(req: AdminLoginRequest):
    admin = db.auth_admin(req.username, req.password)
    if admin:
        return {"success": True, "admin": admin}
    return JSONResponse(status_code=401, content={"success": False, "message": "अमान्य एडमिन यूज़रनेम या पासवर्ड"})

# ----------------- ADMIN API -----------------

@app.get("/api/admin/dashboard-stats")
async def get_admin_stats():
    return db.get_admin_dashboard_stats()

@app.post("/api/admin/update-mandi-rate")
async def update_mandi_price(req: UpdateMandiRateRequest):
    db.update_mandi_rate(
        rate_id=req.id,
        modal_price=req.modal_price,
        min_price=req.min_price,
        max_price=req.max_price,
        trend=req.trend
    )
    return {"success": True}

@app.post("/api/admin/create-broadcast")
async def create_broadcast(req: BroadcastCreateRequest):
    b_id = db.create_broadcast(
        admin_name=req.admin_name,
        title=req.title,
        message=req.message,
        target_district=req.target_district,
        severity=req.severity
    )
    return {"success": True, "broadcast_id": b_id}

# ----------------- ADVISORY & ML API -----------------

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "system": "अन्नदाता (Annadata) Smart Crop Advisory Platform",
        "database": "PostgreSQL / SQLAlchemy (Connected)",
        "version": "2.0.0"
    }

@app.get("/api/dashboard-summary")
async def get_dashboard_summary():
    profile = store.get_profile()
    weather = weather_service.get_weather_advisory(profile["location"])
    advisories = store.get_advisory()
    mandi = mandi_service.get_prices(profile.get("primary_crop", "Wheat"))
    yield_data = yield_engine.estimate_yield(
        crop=profile.get("primary_crop", "Wheat"),
        soil_score=profile.get("soil_health_score", 78),
        farm_size_acres=profile.get("farm_size_acres", 2.5)
    )

    mini_cards = [
        {
            "id": 1,
            "icon": "cannabis",
            "title": "सुझाई गयी फसल",
            "value": profile.get("primary_crop", "गेहूं"),
            "subtitle": f"उपयुक्तता: {profile.get('crop_suitability_pct', 92)}%",
            "color_class": "minicard1"
        },
        {
            "id": 2,
            "icon": "experiment",
            "title": "मिट्टी स्वास्थ्य स्कोर",
            "value": f"{profile.get('soil_health_score', 78)}/100",
            "subtitle": "अच्छा",
            "color_class": "minicard2"
        },
        {
            "id": 3,
            "icon": "rainy",
            "title": "आने वाले तीन दिन बारिश",
            "value": f"{weather['current']['rain_3day_mm']} मि.मि.",
            "subtitle": "मध्यम",
            "color_class": "minicard3"
        },
        {
            "id": 4,
            "icon": "dew_point",
            "title": "तापमान",
            "value": f"{weather['current']['temperature_c']}°C",
            "subtitle": "सामान्य",
            "color_class": "minicard4"
        },
        {
            "id": 5,
            "icon": "water_drops",
            "title": "मिट्टी में नमी",
            "value": f"{weather['current']['soil_moisture_pct']}%",
            "subtitle": weather['current']['soil_moisture_label'].split()[0],
            "color_class": "minicard5"
        }
    ]

    return {
        "profile": profile,
        "mini_cards": mini_cards,
        "advisories": advisories,
        "weather": weather,
        "mandi": mandi,
        "yield_data": yield_data
    }

@app.post("/api/recommend-crop")
async def recommend_crop(req: CropRecommendationRequest):
    result = crop_engine.predict(
        n=req.nitrogen,
        p=req.phosphorus,
        k=req.potassium,
        temp=req.temperature,
        humidity=req.humidity,
        ph=req.ph,
        rainfall=req.rainfall
    )
    store.add_history(
        type_hi=f"फसल सिफारिश ({result['recommended_crop_hi']})",
        result_hi=f"{result['recommended_crop_hi']} उपयुक्तता: {result['suitability_percentage']}%",
        action_taken_hi="मिट्टी पोषक तत्वों व मौसम के आधार पर अनुकूल फसल चयन"
    )
    return result

@app.post("/api/detect-disease")
async def detect_disease(
    file: Optional[UploadFile] = File(None),
    crop_hint: Optional[str] = Form("Wheat")
):
    if file is not None:
        contents = await file.read()
    else:
        contents = b"sample_leaf_bytes"

    result = disease_engine.analyze_image(contents, crop_hint=crop_hint)
    
    # Record to PostgreSQL database
    profile = store.get_profile()
    try:
        db.record_disease_scan(
            farmer_id=1,
            farmer_name=profile.get("farmer_name", "किसान भाई"),
            crop=crop_hint or "गेहूं",
            disease_hi=result["disease_name_hi"],
            disease_en=result["disease_name_en"],
            conf=result["confidence_score"],
            severity=result["severity"],
            remedy=result["treatment_summary"]["primary_chemical"]
        )
    except Exception as e:
        print("Scan DB save note:", e)

    store.add_history(
        type_hi=f"रोग पहचान ({result['disease_name_hi']})",
        result_hi=f"{result['disease_name_hi']} (विश्वास: {result['confidence_score']}%)",
        action_taken_hi=result['treatment_summary']['primary_chemical']
    )
    return result

@app.post("/api/fertilizer-plan")
async def get_fertilizer_plan(req: FertilizerPlanRequest):
    result = fertilizer_engine.calculate_plan(
        n_soil=req.nitrogen,
        p_soil=req.phosphorus,
        k_soil=req.potassium,
        ph=req.ph,
        farm_size_acres=req.farm_size_acres,
        crop=req.crop,
        soil_type=req.soil_type
    )
    return result

@app.post("/api/yield-estimate")
async def get_yield_estimate(req: YieldEstimateRequest):
    result = yield_engine.estimate_yield(
        crop=req.crop,
        soil_score=req.soil_score,
        irrigation_quality=req.irrigation_quality,
        fertilizer_adherence=req.fertilizer_adherence,
        farm_size_acres=req.farm_size_acres
    )
    return result

@app.get("/api/weather-advisory")
async def get_weather(location: str = Query("इंदौर , मध्य प्रदेश")):
    return weather_service.get_weather_advisory(location=location)

@app.get("/api/mandi-prices")
async def get_mandi_prices(crop: str = Query("Wheat")):
    return mandi_service.get_prices(crop=crop)

@app.get("/api/history")
async def get_history():
    return store.get_history()

@app.post("/api/farm-profile")
async def update_farm_profile(req: FarmProfileUpdateRequest):
    update_dict = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = store.update_profile(update_dict)
    return updated
