# Frontend-Backend Integration Reference

## Frontend Pages & Routes

### Public Routes
| Page | URL | Component | Auth Required |
|------|-----|-----------|---------------|
| Login | `http://localhost:5173/login` | `Login.jsx` | ❌ No |
| Home/Redirect | `http://localhost:5173/` | `HomeRedirect()` | ✅ Yes |

### Admin Routes (role: `admin`)
| Page | URL | Component | Auth Required |
|------|-----|-----------|---------------|
| Admin Dashboard | `http://localhost:5173/dashboard` | `AdminDashboard.jsx` | ✅ Yes |
| Toll Zones Management | `http://localhost:5173/dashboard/zones` | `TollZonesPage.jsx` | ✅ Yes |
| Transactions History | `http://localhost:5173/dashboard/transactions` | `TransactionsPage.jsx` | ✅ Yes |

### Toll Operator Routes (role: `toll_operator`)
| Page | URL | Component | Auth Required |
|------|-----|-----------|---------------|
| Operator Dashboard | `http://localhost:5173/operator` | `OperatorDashboard.jsx` | ✅ Yes |
| View Zones (Read-Only) | `http://localhost:5173/operator/zones` | `TollZonesPage.jsx` | ✅ Yes |

---

## Backend API Endpoints

### Authentication
| Method | Endpoint | Body | Response | Error Codes |
|--------|----------|------|----------|------------|
| POST | `/api/auth/login` | `{username, password}` | `{token, user: {user_id, username, role}}` | 400, 401, 500 |
| POST | `/api/auth/register` | `{username, password, role}` | `{message, user: {user_id, username, role}}` | 400, 500 |

### Toll Zones
| Method | Endpoint | Body | Response | Auth | Role |
|--------|----------|------|----------|------|------|
| GET | `/api/toll-zones` | - | `{success: true, data: [...]}` | ✅ JWT | Any |
| POST | `/api/toll-zones` | `{zone_name, charge_amount, polygon_coords}` | `{success: true, zone: {...}}` | ✅ JWT | `admin` |
| PUT | `/api/toll-zones/<zone_id>` | `{zone_name?, charge_amount?, polygon_coords?}` | `{success: true, zone: {...}}` | ✅ JWT | `admin` |
| DELETE | `/api/toll-zones/<zone_id>` | - | `{success: true}` | ✅ JWT | `admin` |

### Transactions/Tolls History
| Method | Endpoint | Query | Response | Auth | Role |
|--------|----------|-------|----------|------|------|
| GET | `/api/tolls-history` | optional filters | `{success: true, data: [...]}` | ✅ JWT | Any |

---

## Error Handling & Status Codes

### Authentication Errors
| Error | Status | Message | Action |
|-------|--------|---------|--------|
| Invalid Credentials | 401 | "Invalid username or password" | Show toast, stay on login |
| Missing Credentials | 400 | "Username and password are required" | Show validation error |
| User Not Found | 401 | "Invalid username or password" | Show toast, stay on login |
| Server Error | 500 | Error message | Show toast, retry option |
| Token Expired | 401 | (Automatic) | Clear storage, redirect to `/login` |

### Zone CRUD Errors
| Operation | Error | Status | Message | Action |
|-----------|-------|--------|---------|--------|
| GET | Server Error | 500 | Error details | Show toast, retry |
| POST | Invalid Data | 400 | Missing field errors | Show validation feedback |
| POST | Server Error | 500 | Error details | Show toast, retry |
| PUT | Zone Not Found | 404 | "Toll zone not found" | Show error, refresh list |
| PUT | Invalid Data | 400 | Missing field errors | Show validation feedback |
| DELETE | Zone Not Found | 404 | "Toll zone not found" | Show error, refresh list |
| DELETE | Server Error | 500 | Error details | Show toast, retry |

### RBAC Errors
| Scenario | Route | Response | Action |
|----------|-------|----------|--------|
| toll_operator tries POST zone | `/api/toll-zones` | 403 Forbidden (backend) | Frontend hides UI, shows "Access Denied" |
| toll_operator tries PUT zone | `/api/toll-zones/<zone_id>` | 403 Forbidden (backend) | Frontend hides UI, shows "Access Denied" |
| toll_operator tries DELETE zone | `/api/toll-zones/<zone_id>` | 403 Forbidden (backend) | Frontend hides UI, shows "Access Denied" |
| Unauthenticated tries dashboard | `/dashboard` | Redirect to `/login` | `RequireRole` wrapper redirects |
| toll_operator tries `/dashboard` | `/dashboard` | Redirect to `/operator` | `RequireRole` wrapper redirects |
| admin tries `/operator` | `/operator` | Redirect to `/dashboard` | `RequireRole` wrapper redirects |

---

## Environment Configuration

### Frontend (.env)
```
VITE_USE_MOCK_API=false
VITE_API_URL=https://automated-route-toll.onrender.com
VITE_GOOGLE_MAPS_API_KEY=YOUR_KEY
```

### Backend Configuration (app.py)
```python
# CORS enabled for all origins
CORS(app)

# JWT Secret
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_super_secret_key')

# Database
DATABASE_URL = os.getenv('DATABASE_URL')  # PostgreSQL on Render
```

---

## API Request Flow with Auth

### 1. Login Request
```
POST https://automated-route-toll.onrender.com/api/auth/login
Body: { username: "admin", password: "password123" }
Response: { token: "eyJ...", user: { user_id: "uuid", username: "admin", role: "admin" } }
```

### 2. Authenticated Request (Zones)
```
GET https://automated-route-toll.onrender.com/api/toll-zones
Header: Authorization: Bearer eyJ...
Response: { success: true, data: [{ zone_id: "uuid", zone_name: "...", charge_amount: 100, polygon_coords: [...] }] }
```

### 3. Token Expires
```
Response: 401 Unauthorized
Frontend Action: 
  - Clear localStorage (auth_token, auth_user)
  - Redirect to http://localhost:5173/login
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS Error on login | Incorrect API path | Ensure path is `/api/auth/login` not `/auth/login` |
| 401 Unauthorized | Missing or invalid token | Check `localStorage.getItem('auth_token')` exists and is valid JWT |
| Zone not updating | Incorrect zone_id format | Zone IDs are UUIDs (strings), ensure comparison uses `zone.zone_id` not `zone.id` |
| Role doesn't apply | JWT not decoded | Check `jwtDecode(token)` extracts `role` property correctly |
| Redirect loops | Role name mismatch | Backend uses `toll_operator`, frontend must use `toll_operator` (not `operator`) |
| Mock data showing | Mock API still enabled | Ensure `.env` has `VITE_USE_MOCK_API=false` |
| Transactions page blank | Endpoint not found | Backend must have `/api/tolls-history` endpoint registered |

---

## Testing Checklist

- [ ] Login with admin credentials → redirects to `/dashboard`
- [ ] Login with toll_operator credentials → redirects to `/operator`
- [ ] Invalid credentials → shows error toast
- [ ] Admin can view zones list → GET `/api/toll-zones` returns data
- [ ] Admin can create zone → POST `/api/toll-zones` with valid data
- [ ] Admin can update zone → PUT `/api/toll-zones/<zone_id>` updates state
- [ ] Admin can delete zone → DELETE `/api/toll-zones/<zone_id>` removes from list
- [ ] toll_operator can view zones (read-only) → UI shows no create/edit/delete buttons
- [ ] Admin can view transactions → GET `/api/tolls-history` returns data
- [ ] Logout clears token → localStorage cleared, redirects to `/login`
- [ ] Token expiry → 401 response triggers auto-logout and redirect
- [ ] RBAC enforced → toll_operator can't access `/dashboard`, admin can't access `/operator`
