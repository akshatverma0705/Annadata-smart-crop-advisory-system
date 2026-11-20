# अन्नदाता (Annadata) - Smart Crop Advisory System

> **सही सलाह, बेहतर फसल**  
> An AI and Machine Learning Decision-Support System tailored for Small and Marginal Farmers with PostgreSQL Database and Dedicated Admin Control.

![Annadata Logo](./frontend/assets/annadatalogo.jpg)

---

#Overview & Core Features

1. AI Crop Recommendation: Random Forest Machine Learning model predicting optimal crops (Rice, Wheat, Maize, Cotton, Chickpea, Mustard, Sugarcane, Soybean, etc.) based on Nitrogen (N), Phosphorus (P), Potassium (K), Soil pH, Temperature, Humidity, and Rainfall.
2. Pest & Disease Vision Classifier: Upload or drop leaf photos to diagnose diseases (Leaf Rust, Powdery Mildew, Rice Blast, Early Blight, Leaf Curl, etc.) with confidence scores, organic bio-remedies (Neem oil, Trichoderma), and chemical dosage safety prescriptions.
3. Fertilizer & Soil Nutrient Optimizer: Calculates exact 50kg bags of Urea, DAP, and MOP required for any farm acreage along with split application schedules and cost savings.
4. Yield Estimation Engine: Multi-variable regression model projecting quintals/acre yield curves and influencing factors (soil, weather, irrigation, fertilizers).
5. Agromet Weather Advisory: 5-day agro-meteorological forecast with automated irrigation warnings and pesticide spray window recommendations.
6. Mandi Market Rate Tracker: Real-time APMC mandi commodity prices, MSP comparisons, and trend tracking.
7. Integrated Voice Assistant (TTS): One-click audio narration in Hindi/English for farmers with low digital literacy.
8. Dedicated Admin Portal & PostgreSQL Database: Admin dashboard to manage farmers, audit leaf scans, update mandi rates, and broadcast emergency agricultural alerts.

---

#Repository Directory Structure

```text
annadata_app/
│
├── backend/
│   ├── main.py                  # FastAPI server & REST API routes
│   ├── database.py              # PostgreSQL & SQLAlchemy database layer + seeders
│   ├── annadata.db              # Embedded SQLite fallback database
│   │
│   ├── ml/
│   │   ├── crop_model.py        # Random Forest Crop Recommendation ML Engine
│   │   ├── disease_model.py     # Pathology leaf classifier & treatment advisor
│   │   ├── fertilizer_engine.py # Agronomic NPK deficit & split calculator
│   │   └── yield_engine.py      # Yield curve estimation model
│   │
│   └── services/
│       ├── weather_service.py   # Agromet 5-day forecasts & spray advisories
│       ├── mandi_service.py     # APMC market rates & MSP comparisons
│       └── store.py             # Session and history management
│
├── frontend/
│   ├── index.html               # Farmer Main Dashboard
│   ├── login.html               # Farmer & Admin Authentication Portal
│   ├── admin.html               # Agriculture Officer Admin Dashboard
│   ├── home.css                 # Responsive high-contrast agricultural styles
│   ├── app.js                   # Client-side controller & Web Speech TTS
│   └── assets/                  # Logo, leaf samples, and banner artwork
│       ├── annadatalogo.jpg
│       ├── annadatalogo.png
│       ├── homepageimg.jpg
│       ├── leaf.jpg
│       └── help.png
│
├── run.py                       # Root Python Launcher
├── start.bat                    # Windows 1-Click Batch Launcher
├── test_full_suite.py           # Automated integration test suite
├── requirements.txt             # Python dependencies
└── README.md                    # Platform documentation
```

---

#Quick Start & Installation

#1. Prerequisites
- Python 3.9+ installed
- *(Optional)* PostgreSQL server (Defaults automatically to embedded SQLite if PostgreSQL is not active)

#2. Install Dependencies
```bash
cd annadata_app
pip install -r requirements.txt
```

#3. Run the Application
```bash
python run.py
```
*(Or simply double-click `start.bat` on Windows)*

---

#Portals & Demo Access

| Portal | URL | Demo Credentials |
| :--- | :--- | :--- |
| Farmer Main Dashboard** | [http://127.0.0.1:8000](http://127.0.0.1:8000) | Instant Access |
| Farmer & Admin Login** | [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login) | **Farmer**: `9520412093` / `kisan123`<br/>**Admin**: `admin` / `admin123` |
| Dedicated Admin Portal** | [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) | `admin` / `admin123` |
| Interactive API Docs** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Swagger UI for all REST endpoints |

---

#PostgreSQL Database Configuration

To connect your external PostgreSQL server, set the `DATABASE_URL` environment variable before running:

```bash
# Windows PowerShell
$env:DATABASE_URL="postgresql://postgres:password@localhost:5432/annadata"
python run.py

# Linux / Mac
export DATABASE_URL="postgresql://postgres:password@localhost:5432/annadata"
python run.py
```

The system will automatically initialize all tables and seed default users, mandi rates, and crop rules on startup.

---

#Running Automated Tests

Run the full integration test suite to verify all 10 subsystems:

```bash
python test_full_suite.py
```

---

## 📜 License
Developed for Indian Small and Marginal Farmers under Open Agricultural Decision Support Initiative.
