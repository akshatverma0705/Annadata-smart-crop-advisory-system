@echo off
title Annadata - Smart Crop Advisory System
echo ========================================================
echo   Annadata (अन्नदाता) - Smart Crop Advisory System
echo   Starting Backend and Frontend on http://127.0.0.1:8000
echo ========================================================
python -m pip install -r requirements.txt
python run.py
pause
