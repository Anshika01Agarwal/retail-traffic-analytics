# AI-Powered Retail Infrastructure Traffic Analytics System

An industrial-grade, full-stack edge computer vision data pipeline. The system intercepts live camera streams, tracks unique visitor identities, calculates real-time storefront dwell engagement metrics, stores logs securely inside a PostgreSQL cluster, and programmatically exports an interactive executive analytics dashboard using Seaborn.

## 📁 Repository Blueprint
* `setup_postgres.py` - Sets connection parameters and initializes relational database schema tables.
* `generate_data.py` - Simulates 30 days of historical retail baseline telemetry logs for dashboard validation.
* `live_tracker.py` - Deploys edge YOLO and DeepSORT algorithms to track real-time webcam telemetry streams.
* `generate_dashboard.py` - Queries the local PostgreSQL instance to output a premium, dark-mode visual interface cockpit.
* `Run_Live_Tracker.bat` - Simple desktop shortcut to activate the live video tracker feed.
* `View_Seaborn_Dashboard.bat` - Simple desktop shortcut to load the analytics dashboard report instantly.
* `Reset_Database_Data.bat` - One-click tool to wipe tables and inject a clean data wave.

## 🚀 Deployment Instructions

### 1. Environment Activation
Ensure you are inside your project root and activate your isolated environment container path:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\env\Scripts\Activate.ps1
```

### 2. Database Schema Creation
Ensure your PostgreSQL server is active, create an empty target database named `retail_db` via pgAdmin, then execute the setup file:
```powershell
& "C:\Program Files\Python313\python.exe" setup_postgres.py
```

### 3. Visual Telemetry Simulation Build
Seed your tables with 30 days of clean historical baseline rows to test your dashboard charts:
```powershell
& "C:\Program Files\Python313\python.exe" generate_data.py
```

### 4. Executing the System Applications
* Double-click **`Run_Live_Tracker.bat`** to run your live webcam YOLO object tracking engine (Press **'q'** to save sessions and exit).
* Double-click **`View_Seaborn_Dashboard.bat`** to open your premium dark-mode executive metrics panel.

## 🛡️ Privacy Preservation
This framework completely respects consumer privacy rules. It implements randomized number-based index trackers (*'Shopper ID: 1'*) instead of utilizing sensitive facial recognition storage layers.
