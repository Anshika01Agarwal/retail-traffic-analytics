@echo off
title Retail Analytics Seaborn Dashboard Engine
echo ========================================================
echo   Fetching Relational Metrics from PostgreSQL Server...
echo ========================================================
"C:\Program Files\Python313\python.exe" generate_dashboard.py
pause
