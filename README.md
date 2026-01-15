# 🚧 Automated Route Toll & Payment Tracker

An end-to-end **automated toll collection simulation system** that uses **geo-fencing (Point-in-Polygon)** to detect when a vehicle enters a toll zone and automatically triggers an **M-Pesa C2B STK Push** for payment, with real-time status updates and administrative monitoring.

---

## 📌 Project Overview

The **Automated Route Toll & Payment Tracker** is designed to demonstrate how location-based services, digital payments, and modern web technologies can be combined to automate toll collection.

### 🎯 Core Objectives

- Detect vehicle entry into toll zones using geo-fencing.
- Automatically initiate M-Pesa payments upon zone entry.
- Provide real-time payment feedback to drivers.
- Offer an administrative dashboard for monitoring, auditing, and configuration.

---

## 🧱 System Architecture

```
[ React Frontend (Vercel) ]
          |
          | REST API (Axios)
          |
[ Flask Backend (Render) ]
          |
          | PostgreSQL
          |
[ Toll Zones & Payment Logs ]
          |
          | Safaricom Daraja API
          |
[ M-Pesa STK Push + Callback ]
```

---

## 🛠️ Technology Stack

### Backend
- Python (Flask)
- PostgreSQL
- Shapely
- Requests
- Gunicorn

### Frontend
- React
- Tailwind CSS
- Axios
- Google Maps API

### Payments
- Safaricom Daraja API

### Deployment
- Backend: Render
- Frontend: Vercel

---

## 📂 Project Structure

```
automated-toll-tracker/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── models/
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── tailwind.config.js
│   └── package.json
│
└── README.md
```

---

## 🗄️ Database Design

### toll_zones

| Column | Type | Description |
|------|------|-------------|
| zone_id | UUID | Unique toll zone identifier |
| zone_name | TEXT | Zone name
| charge_amount | INTEGER | Toll amount |
| polygon_coords | JSONB | Polygon vertices |

### tolls_paid

| Column | Type | Description |
|------|------|-------------|
| id | UUID | Payment record ID |
| zone_id | UUID | Associated toll zone |
| amount | INTEGER | Charged amount |
| checkout_request_id | TEXT | M-Pesa reference |
| status | TEXT | Pending / Completed / Failed |
| created_at | TIMESTAMP | Timestamp |

---

## 🔄 Application Flows

### Driver Flow
1. Route & zones displayed on map.
2. Vehicle sends coordinates.
3. Geo-fencing validation.
4. STK Push triggered.
5. Payment approved.
6. Status updated in real time.

### Administrator Flow
1. Secure login.
2. View dashboard.
3. Audit payments & zones.

### Toll Operator Flow
1. Login.
2. Define toll zones.
3. Persist configuration.

---

## 🔐 Security Practices

- Environment variables for M-Pesa credentials
- Protected admin/operator routes
- Callback validation
- CORS configuration

---

## 🔌 API Endpoints

### Geo-Fencing
```
POST /api/check-zone
```

### M-Pesa Callback
```
POST /api/mpesa/callback
```

### Toll History
```
GET /api/tolls-history
```

---

## 🚀 Deployment Instructions

### Deploy Backend to Render

1. Go to [Render Dashboard](https://dashboard.render.com)

2. **New → Web Service**

3. **Connect your GitHub repo:** `Eva-Chem/automated-toll-tracker`

4. **Settings:**
   - **Name:** `toll-tracker-api`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`

5. **Environment Variables:**
   Add the following in the Render dashboard:
   ```
   DATABASE_URL=<your-postgresql-connection-string>
   MPESA_CONSUMER_KEY=<your-mpesa-consumer-key>
   MPESA_CONSUMER_SECRET=<your-mpesa-consumer-secret>
   MPESA_SHORTCODE=<your-mpesa-shortcode>
   MPESA_PASSKEY=<your-mpesa-passkey>
   FLASK_ENV=production
   ```

6. **Deploy**

7. **Backend URL** - `https://automated-route-toll-2.onrender.com/`
`)

---

### Deploy Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)

2. **Add New → Project**

3. **Import** `Eva-Chem/automated-toll-tracker`

4. **Settings:**
   - **Framework Preset:** Create React App
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`

5. **Environment Variables:**
   Add the following:
   ```
   REACT_APP_API_URL=https://toll-tracker-api.onrender.com
   REACT_APP_GOOGLE_MAPS_API_KEY=<your-google-maps-api-key>
   ```

6. **Deploy**

---

## 📝 Post-Deployment Checklist

### Backend
- [ ] Verify backend is accessible at your Render URL
- [ ] Test database connection
- [ ] Register M-Pesa callback URL with Safaricom Daraja
- [ ] Test API endpoints using Postman or curl

### Frontend
- [ ] Verify frontend is accessible at your Vercel URL
- [ ] Check that Google Maps loads correctly
- [ ] Test API connection to backend
- [ ] Verify M-Pesa STK Push flow

### Integration
- [ ] Test end-to-end toll detection flow
- [ ] Verify M-Pesa callback is received
- [ ] Check payment status updates in real-time
- [ ] Test admin dashboard functionality

---

## 🐛 Troubleshooting

### Backend Issues
- **Database connection fails:** Check `DATABASE_URL` environment variable
- **M-Pesa errors:** Verify credentials and callback URL registration
- **CORS errors:** Ensure frontend URL is in allowed origins

### Frontend Issues
- **API calls fail:** Verify `REACT_APP_API_URL` points to correct backend
- **Maps not loading:** Check `REACT_APP_GOOGLE_MAPS_API_KEY`
- **Build errors:** Clear cache and reinstall dependencies

---

## 📜 License

Educational & demonstration use only.

---

## 👤 Author

**Automated Route Toll & Payment Tracker**

For questions or support, please open an issue on GitHub.




