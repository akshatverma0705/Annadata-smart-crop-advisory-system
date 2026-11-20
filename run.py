"""
Annadata (अन्नदाता) - Main Application Launcher
Runs FastAPI Server with Uvicorn on http://127.0.0.1:8000
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add backend to Python path
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

if __name__ == "__main__":
    print("=" * 60)
    print(" 🌾 अन्नदाता (Annadata) - Smart Crop Advisory System")
    print("   सही सलाह, बेहतर फसल")
    print("=" * 60)
    print(" * Farmer Dashboard: http://127.0.0.1:8000")
    print(" * Login & Register: http://127.0.0.1:8000/login")
    print(" * Admin Dashboard:  http://127.0.0.1:8000/admin")
    print(" * API Documentation: http://127.0.0.1:8000/docs")
    print("=" * 60)
    
    os.chdir(str(BACKEND_DIR))
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
