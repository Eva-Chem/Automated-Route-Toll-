# Fix Plan: fetch_all_toll_zones Error

## Issue Analysis
The error "fetch_all_toll_zones is not defined" occurs because:
1. `routes/check_zone.py` contains mixed route code AND model definitions incorrectly
2. The model definitions should ONLY be in `models/toll_zone.py`
3. The current route code in `routes/check_zone.py` looks correct (uses `TollZone.query.all()`)

## Files to Fix

### 1. `routes/check_zone.py`
- **Problem**: Contains both route code AND model definitions (TollZone, TollPayment models)
- **Solution**: Remove the model definitions from lines 29-72, keep only the route code

### 2. `models/toll_zone.py`
- **Problem**: May have incomplete or inconsistent model definition
- **Solution**: Ensure it has the correct TollZone model with all required fields

## Implementation Steps

### Step 1: Clean up routes/check_zone.py
Remove the model definitions (uuid import, datetime import, db import, TollZone class, TollPayment class) from the route file, keeping only:
- Imports (flask, models.toll_zone, services.geo_fencing)
- Blueprint creation
- check_zone route function

### Step 2: Verify models/toll_zone.py
Ensure it has:
- `zone_id` as primary key (String)
- `name` column (String)
- `polygon_coords` column (JSON)
- `charge_amount` column (Float)
- `__init__` method
- `to_dict()` method

### Step 3: Deploy to Render
Run git commands to push the fix.

## Expected Outcome
The `/check-zone` endpoint will work correctly by querying the database using SQLAlchemy ORM instead of a non-existent function.

