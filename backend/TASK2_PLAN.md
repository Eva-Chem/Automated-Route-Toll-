# Backend Task 2: Role-Based Authorization Middleware

## Status: ✅ JWT Already Includes Role

## Plan to Implement

### 1️⃣ Create Middleware Directory and Decorator
- [ ] Create `middlewares/` directory
- [ ] Create `middlewares/__init__.py`
- [ ] Create `middlewares/roles.py` with @admin_required decorator

### 2️⃣ Update Routes with Role Protection
- [ ] Update `routes/toll_zones.py` - Add @admin_required to create/update/delete routes
- [ ] Update `routes/auth_routes.py` - Already done ✅
- [ ] Update other routes as needed

### 3️⃣ Test the Implementation
- [ ] Create test script to verify admin vs operator access

## Implementation Details

### File: middlewares/roles.py
```python
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        role = claims.get("role")
        
        if role != "admin":
            return jsonify({
                "message": "Forbidden: Admin access required"
            }), 403
        
        return fn(*args, **kwargs)
    return wrapper
```

### Protected Routes Examples:
- `POST /api/toll-zones` → @jwt_required + @admin_required
- `DELETE /api/toll-zones/<id>` → @jwt_required + @admin_required  
- `GET /api/toll-zones` → @jwt_required (admin & operator)

## Expected Behavior:
- ✅ Admin: Full access to all routes
- ⚠️ Operator: Blocked from admin routes (403)
- ❌ No token: Blocked (401)

## Ready to Proceed?

