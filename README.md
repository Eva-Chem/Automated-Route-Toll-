 🚧 Automated Route Toll & Payment Tracker

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
POST /api/check-zone

### M-Pesa Callback
POST /api/mpesa/callback

### Toll History
GET /api/tolls-history

---

## 🚀 Deployment

### Backend (Render)
- Gunicorn WSGI server
- Daraja callback URL registered

### Frontend (Vercel)
- Environment-based API URL
- Google Maps API key configured

---

## 📜 License
Educational & demonstration use only.

---

## 👤 Author
Automated Route Toll & Payment Tracker

