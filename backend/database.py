"""
PostgreSQL & SQLAlchemy Database Layer for Annadata
Supports PostgreSQL (with automatic SQLite fallback for environments without local postgres server).
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, desc
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# Database Connection URL
# e.g., postgresql://postgres:postgres@localhost:5432/annadata
PG_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/annadata")
SQLITE_FALLBACK_URL = f"sqlite:///{Path(__file__).resolve().parent / 'annadata.db'}"

engine = None
try:
    # Try PostgreSQL first
    test_engine = create_engine(PG_URL, connect_args={"connect_timeout": 2} if "postgresql" in PG_URL else {})
    with test_engine.connect() as conn:
        pass
    engine = test_engine
    print("[DATABASE] Connected successfully to PostgreSQL server!")
except Exception as e:
    print(f"[DATABASE] PostgreSQL server not reachable ({e}). Falling back to local embedded database engine.")
    engine = create_engine(SQLITE_FALLBACK_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ----------------- SQLALCHEMY MODELS -----------------

class Farmer(Base):
    __tablename__ = "farmers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    location = Column(String(150), default="इंदौर , मध्य प्रदेश")
    farm_size_acres = Column(Float, default=2.5)
    soil_type = Column(String(100), default="दोमट (Loamy)")
    primary_crop = Column(String(100), default="गेहूं")
    soil_health_score = Column(Integer, default=78)
    created_at = Column(DateTime, default=datetime.utcnow)

    scans = relationship("DiseaseScan", back_populates="farmer")

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(String(150), default="मुख्य कृषि अधिकारी (Chief Agronomist)")
    created_at = Column(DateTime, default=datetime.utcnow)

class DiseaseScan(Base):
    __tablename__ = "disease_scans"
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=True)
    farmer_name = Column(String(100), default="किसान भाई")
    crop = Column(String(100), default="गेहूं")
    disease_name_hi = Column(String(150), nullable=False)
    disease_name_en = Column(String(150), nullable=False)
    confidence_score = Column(Float, nullable=False)
    severity = Column(String(100), default="मध्यम")
    remedy = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="scans")

class MandiRate(Base):
    __tablename__ = "mandi_rates"
    id = Column(Integer, primary_key=True, index=True)
    crop_en = Column(String(100), nullable=False)
    crop_hi = Column(String(100), nullable=False)
    mandi_name = Column(String(150), nullable=False)
    state = Column(String(100), nullable=False)
    modal_price = Column(Float, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    msp = Column(Float, default=0.0)
    trend = Column(String(50), default="rising")
    updated_at = Column(DateTime, default=datetime.utcnow)

class Broadcast(Base):
    __tablename__ = "broadcasts"
    id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    target_district = Column(String(150), default="सभी जिले (All Districts)")
    severity = Column(String(100), default="सामान्य")
    created_at = Column(DateTime, default=datetime.utcnow)

# ----------------- INITIALIZATION & SEEDING -----------------

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Seed Admin
    admin_user = db.query(Admin).filter(Admin.username == "admin").first()
    if not admin_user:
        admin_user = Admin(
            username="admin",
            email="admin@annadata.gov.in",
            password_hash=hash_password("admin123"),
            full_name="डॉ. राजेश शर्मा (वरिष्ठ कृषि वैज्ञानिक)",
            role="मुख्य कृषि सलाहकार एवं प्रशासक (Chief Agronomist & Admin)"
        )
        db.add(admin_user)
        db.commit()

    # Seed Farmers
    farmer1 = db.query(Farmer).filter(Farmer.phone == "9520412093").first()
    if not farmer1:
        farmer1 = Farmer(
            name="किसान भाई",
            phone="9520412093",
            password_hash=hash_password("kisan123"),
            location="इंदौर , मध्य प्रदेश",
            farm_size_acres=2.5,
            soil_type="दोमट",
            primary_crop="गेहूं",
            soil_health_score=78
        )
        db.add(farmer1)
        db.commit()
        db.refresh(farmer1)

        # Seed initial disease scan for farmer1
        scan1 = DiseaseScan(
            farmer_id=farmer1.id,
            farmer_name=farmer1.name,
            crop="गेहूं",
            disease_name_hi="पत्ती रस्ट (गेहूं)",
            disease_name_en="Leaf Rust (Puccinia triticina)",
            confidence_score=94.0,
            severity="मध्यम",
            remedy="प्रोपिकोनाजोल 25% EC @ 1 मिली प्रति लीटर पानी"
        )
        db.add(scan1)
        db.commit()

    farmer2 = db.query(Farmer).filter(Farmer.phone == "9876543210").first()
    if not farmer2:
        farmer2 = Farmer(
            name="रामप्रसाद पटेल",
            phone="9876543210",
            password_hash=hash_password("kisan123"),
            location="उज्जैन , मध्य प्रदेश",
            farm_size_acres=4.0,
            soil_type="काली मिट्टी",
            primary_crop="सोयाबीन",
            soil_health_score=82
        )
        db.add(farmer2)
        db.commit()

    # Seed Mandi Rates
    if db.query(MandiRate).count() == 0:
        rates = [
            MandiRate(crop_en="Wheat", crop_hi="गेहूं", mandi_name="इंदौर मंडी (Indore APMC)", state="मध्य प्रदेश", modal_price=2510, min_price=2350, max_price=2620, msp=2275, trend="rising"),
            MandiRate(crop_en="Wheat", crop_hi="गेहूं", mandi_name="उज्जैन मंडी (Ujjain APMC)", state="मध्य प्रदेश", modal_price=2470, min_price=2320, max_price=2580, msp=2275, trend="rising"),
            MandiRate(crop_en="Soybean", crop_hi="सोयाबीन", mandi_name="इंदौर मंडी", state="मध्य प्रदेश", modal_price=4680, min_price=4400, max_price=4850, msp=4892, trend="stable"),
            MandiRate(crop_en="Chickpea", crop_hi="चना (Gram)", mandi_name="इंदौर मंडी", state="मध्य प्रदेश", modal_price=5900, min_price=5600, max_price=6100, msp=5440, trend="rising"),
            MandiRate(crop_en="Mustard", crop_hi="सरसों", mandi_name="जयपुर मंडी", state="राजस्थान", modal_price=5450, min_price=5200, max_price=5680, msp=5650, trend="falling"),
            MandiRate(crop_en="Cotton", crop_hi="कपास", mandi_name="खरगोन मंडी", state="मध्य प्रदेश", modal_price=7300, min_price=6900, max_price=7550, msp=7020, trend="rising"),
            MandiRate(crop_en="Tomato", crop_hi="टमाटर", mandi_name="इंदौर चोइथराम मंडी", state="मध्य प्रदेश", modal_price=1850, min_price=1400, max_price=2300, msp=0, trend="rising")
        ]
        db.add_all(rates)
        db.commit()

    # Seed Broadcasts
    if db.query(Broadcast).count() == 0:
        b1 = Broadcast(
            admin_name="डॉ. राजेश शर्मा",
            title="यलो रस्ट (पीला रतुआ) पूर्व चेतावनी अलर्ट",
            message="आगामी 3 दिनों में नमी व शीतल हवाओं के कारण गेहूं की फसल में रतुआ रोग का प्रकोप हो सकता है। किसान भाई प्रोपिकोनाजोल या नीम तेल का छिड़काव तैयार रखें।",
            target_district="इंदौर एवं मालवा संभाग",
            severity="उच्च (High Alert)"
        )
        db.add(b1)
        db.commit()

    db.close()

# ----------------- DB OPERATIONS -----------------

def auth_farmer(phone: str, password: str) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    f = db.query(Farmer).filter(Farmer.phone == phone, Farmer.password_hash == hash_password(password)).first()
    if f:
        res = {
            "id": f.id,
            "name": f.name,
            "phone": f.phone,
            "location": f.location,
            "farm_size_acres": f.farm_size_acres,
            "soil_type": f.soil_type,
            "primary_crop": f.primary_crop,
            "soil_health_score": f.soil_health_score
        }
        db.close()
        return res
    db.close()
    return None

def auth_admin(username: str, password: str) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    a = db.query(Admin).filter((Admin.username == username) | (Admin.email == username), Admin.password_hash == hash_password(password)).first()
    if a:
        res = {
            "id": a.id,
            "username": a.username,
            "email": a.email,
            "full_name": a.full_name,
            "role": a.role
        }
        db.close()
        return res
    db.close()
    return None

def register_farmer(name: str, phone: str, password: str, location: str = "इंदौर , मध्य प्रदेश", farm_size: float = 2.5, soil: str = "दोमट", crop: str = "गेहूं") -> Dict[str, Any]:
    db = SessionLocal()
    exists = db.query(Farmer).filter(Farmer.phone == phone).first()
    if exists:
        db.close()
        return {"success": False, "error": "यह मोबाइल नंबर पहले से पंजीकृत है (Phone already registered)"}

    new_f = Farmer(
        name=name,
        phone=phone,
        password_hash=hash_password(password),
        location=location,
        farm_size_acres=farm_size,
        soil_type=soil,
        primary_crop=crop,
        soil_health_score=78
    )
    db.add(new_f)
    db.commit()
    db.refresh(new_f)
    f_id = new_f.id
    db.close()
    return {"success": True, "farmer_id": f_id, "name": name, "phone": phone}

def get_admin_dashboard_stats() -> Dict[str, Any]:
    db = SessionLocal()
    total_farmers = db.query(Farmer).count()
    total_scans = db.query(DiseaseScan).count()
    total_mandi_entries = db.query(MandiRate).count()

    farmers = db.query(Farmer).order_by(desc(Farmer.id)).limit(10).all()
    scans = db.query(DiseaseScan).order_by(desc(DiseaseScan.id)).limit(10).all()
    mandi_rates = db.query(MandiRate).order_by(MandiRate.id.asc()).all()
    broadcasts = db.query(Broadcast).order_by(desc(Broadcast.id)).limit(5).all()

    res = {
        "total_farmers": total_farmers,
        "total_scans": total_scans,
        "total_mandi_entries": total_mandi_entries,
        "recent_farmers": [
            {
                "id": f.id, "name": f.name, "phone": f.phone, "location": f.location,
                "farm_size_acres": f.farm_size_acres, "primary_crop": f.primary_crop,
                "soil_type": f.soil_type, "soil_health_score": f.soil_health_score,
                "created_at": f.created_at.strftime("%d %b %Y") if f.created_at else ""
            } for f in farmers
        ],
        "recent_scans": [
            {
                "id": s.id, "farmer_name": s.farmer_name, "crop": s.crop,
                "disease_name_hi": s.disease_name_hi, "disease_name_en": s.disease_name_en,
                "confidence_score": s.confidence_score, "severity": s.severity,
                "remedy": s.remedy, "created_at": s.created_at.strftime("%d %b %Y %H:%M") if s.created_at else ""
            } for s in scans
        ],
        "mandi_rates": [
            {
                "id": m.id, "crop_en": m.crop_en, "crop_hi": m.crop_hi,
                "mandi_name": m.mandi_name, "state": m.state,
                "modal_price": m.modal_price, "min_price": m.min_price, "max_price": m.max_price,
                "msp": m.msp, "trend": m.trend, "updated_at": m.updated_at.strftime("%d %b %Y") if m.updated_at else ""
            } for m in mandi_rates
        ],
        "broadcasts": [
            {
                "id": b.id, "admin_name": b.admin_name, "title": b.title,
                "message": b.message, "target_district": b.target_district,
                "severity": b.severity, "created_at": b.created_at.strftime("%d %b %Y") if b.created_at else ""
            } for b in broadcasts
        ]
    }
    db.close()
    return res

def update_mandi_rate(rate_id: int, modal_price: float, min_price: float, max_price: float, trend: str):
    db = SessionLocal()
    rate = db.query(MandiRate).filter(MandiRate.id == rate_id).first()
    if rate:
        rate.modal_price = modal_price
        rate.min_price = min_price
        rate.max_price = max_price
        rate.trend = trend
        rate.updated_at = datetime.utcnow()
        db.commit()
    db.close()
    return True

def create_broadcast(admin_name: str, title: str, message: str, target_district: str, severity: str):
    db = SessionLocal()
    b = Broadcast(
        admin_name=admin_name,
        title=title,
        message=message,
        target_district=target_district,
        severity=severity
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    b_id = b.id
    db.close()
    return b_id

def record_disease_scan(farmer_id: int, farmer_name: str, crop: str, disease_hi: str, disease_en: str, conf: float, severity: str, remedy: str):
    db = SessionLocal()
    scan = DiseaseScan(
        farmer_id=farmer_id,
        farmer_name=farmer_name,
        crop=crop,
        disease_name_hi=disease_hi,
        disease_name_en=disease_en,
        confidence_score=conf,
        severity=severity,
        remedy=remedy
    )
    db.add(scan)
    db.commit()
    db.close()

# Auto-initialize tables and seed data
init_db()
