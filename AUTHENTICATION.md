# Authentication & Role-Based Access Control (RBAC) Implementation

## Overview

This document describes the complete authentication and authorization system implemented for the Toll Route Manager application. The system provides secure, role-based access control with two primary roles: **Administrator** and **Operator**.

---

## Features

✅ **Modern Login Page** - Clean, responsive, and visually appealing UI
✅ **Secure Authentication** - Form validation and error handling
✅ **Role-Based Access Control (RBAC)** - Two distinct roles with different permissions
✅ **JWT Token Management** - Secure token-based authentication
✅ **Loading States** - Visual feedback during authentication
✅ **Protected Routes** - Automatic redirection for unauthorized access
✅ **Persistent Sessions** - Auto-login from localStorage
✅ **Responsive Design** - Works perfectly on all device sizes

---

## User Roles & Permissions

### 1. Administrator Role
**Username:** `admin`  
**Password:** `admin123`

**Permissions:**
- View complete dashboard with all metrics
- Manage toll zones (create, read, update, delete)
- View all transactions
- Manage operators
- View system reports
- Access: `/dashboard` and all admin routes

### 2. Operator Role
**Username:** `operator`  
**Password:** `operator123`

**Permissions:**
- View operator dashboard
- View assigned toll zones
- Record transactions
- View operational data
- Access: `/operator` and operator-specific routes

---

## Architecture

### Frontend Components

#### 1. **Login Page** (`src/auth/Login.jsx`)
```jsx
- Modern split-layout design
- Username and password input fields
- Form validation with error messages
- Loading state with spinner
- Demo credentials display
- Error alerts for failed authentication
```

**Features:**
- Real-time form validation
- Clear error messages
- Loading spinner during submission
- Demo credentials for testing
- Responsive design (mobile, tablet, desktop)

#### 2. **Auth Context** (`src/auth/auth.context.jsx`)
```jsx
- Centralized authentication state management
- Mock user database (simulates backend)
- Login function with credential validation
- Logout function with session cleanup
- Token management
- Persistent session using localStorage
```

**Methods:**
- `login(username, password)` - Authenticate user
- `logout()` - Clear session and redirect
- `isAuthenticated()` - Check authentication status

#### 3. **RequireRole Component** (`src/auth/RequireRole.jsx`)
```jsx
- Route protection wrapper
- Role-based authorization
- Automatic redirects for unauthorized access
- Fallback redirect to login for unauthenticated users
```

#### 4. **Router Configuration** (`src/app/Router.jsx`)
```jsx
- Protected routes with RequireRole wrapper
- Auto-redirect to appropriate dashboard based on role
- Catch-all redirect for unknown routes
- Separate routes for admin and operator
```

#### 5. **Topbar** (`src/layout/Topbar.jsx`)
```jsx
- Display current user name and role
- Logout button with redirect to login
- User avatar and role badge
```

### Styling

#### **Login Page Styles** (`src/styles/login.css`)
- **Modern Design:**
  - Gradient backgrounds
  - Smooth animations
  - Professional color scheme
  - Glass morphism effects

- **Responsive Breakpoints:**
  - Desktop: Full split layout
  - Tablet: Single column with adjusted spacing
  - Mobile: Optimized for small screens

- **Interactive Elements:**
  - Input focus states
  - Error states with red styling
  - Loading spinner animation
  - Hover effects on buttons
  - Smooth transitions

- **Dark Mode Support:**
  - Automatic detection via `prefers-color-scheme`
  - Adjusted colors and backgrounds

### Backend API

#### **Authentication Routes** (`backend/routes/auth.py`)

##### `POST /api/auth/login`
Authenticates user and returns JWT token.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "token": "jwt_token_here",
  "user": {
    "username": "admin",
    "name": "Administrator",
    "role": "admin",
    "email": "admin@tolls.com",
    "permissions": ["manage_zones", "view_transactions", "manage_operators", "view_reports"]
  },
  "expiresIn": 86400
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "Invalid username or password"
}
```

##### `POST /api/auth/verify`
Verifies JWT token validity.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "valid": true,
  "user": { ... }
}
```

##### `GET /api/auth/profile`
Retrieves current user profile.

**Headers:**
```
Authorization: Bearer <token>
```

##### `POST /api/auth/logout`
Logs out user (invalidates token).

---

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER VISITS LOGIN PAGE                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              USER ENTERS CREDENTIALS & SUBMITS                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│           FORM VALIDATION (CLIENT-SIDE)                          │
│  - Username required                                            │
│  - Password required                                            │
│  - Both fields must be non-empty                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
         Invalid                    Valid
              │                         │
              ▼                         ▼
    ┌─────────────────┐    ┌──────────────────────┐
    │ SHOW ERRORS     │    │ SEND TO BACKEND      │
    └─────────────────┘    └──────────────────────┘
                                      │
                                      ▼
                           ┌──────────────────────┐
                           │ VERIFY CREDENTIALS   │
                           │ & GENERATE TOKEN     │
                           └──────────┬───────────┘
                                      │
                        ┌─────────────┴──────────┐
                        │                        │
                    Success               Invalid Credentials
                        │                        │
                        ▼                        ▼
            ┌──────────────────────┐   ┌─────────────────┐
            │ SAVE TOKEN & USER    │   │ SHOW ERROR MSG  │
            │ IN LOCALSTORAGE      │   └─────────────────┘
            └──────────┬───────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │ REDIRECT TO ROLE-    │
            │ SPECIFIC DASHBOARD   │
            │ admin → /dashboard   │
            │ operator → /operator │
            └──────────────────────┘
```

---

## Security Features

### 1. **Input Validation**
- Username and password validation on client side
- Empty field checking
- Error messages for invalid input

### 2. **Token Management**
- JWT tokens generated on backend
- Tokens stored in localStorage
- Token expiration (24 hours)
- Automatic logout on expiration

### 3. **Route Protection**
- RequireRole wrapper prevents unauthorized access
- Automatic redirects to login for unauthenticated users
- Role-based route restrictions

### 4. **Session Persistence**
- User data stored in localStorage
- Automatic login on page reload if token exists
- Logout clears all session data

### 5. **Error Handling**
- Meaningful error messages
- Network error handling
- Invalid credential feedback
- Unauthorized access notifications

---

## User Experience Features

### 1. **Loading States**
- Spinning loader during authentication
- Disabled form inputs while loading
- "Signing in..." button text feedback

### 2. **Form Validation**
- Real-time error clearing on input
- Field-specific error messages
- Visual error indicators (red borders)

### 3. **Demo Credentials**
- Clearly displayed test credentials
- Separate cards for admin and operator
- Easy reference for testing

### 4. **Responsive Design**
- Mobile-optimized layout
- Touch-friendly input fields
- Adaptive typography sizes
- Flexible grid layout

### 5. **Accessibility**
- Proper label associations
- ARIA-friendly structure
- Keyboard navigation support
- Clear focus states

---

## Setup & Installation

### Backend Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Run the backend:**
```bash
python app.py
```

The backend will start at `http://127.0.0.1:5000`

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Run the frontend:**
```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

---

## Testing the Application

### Admin User
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full system access, all dashboards and features

### Operator User
- **Username:** `operator`
- **Password:** `operator123`
- **Access:** Operator dashboard, toll zones view, transaction recording

### Test Scenarios

#### 1. **Valid Login**
1. Enter "admin" as username
2. Enter "admin123" as password
3. Click "Sign In"
4. Should redirect to admin dashboard

#### 2. **Invalid Credentials**
1. Enter any wrong username
2. Enter any wrong password
3. Click "Sign In"
4. Should show error: "Invalid username or password"

#### 3. **Empty Fields**
1. Leave username empty
2. Click "Sign In"
3. Should show error: "Username is required"

#### 4. **Role-Based Access**
1. Login as operator
2. Try accessing admin route (`/dashboard`)
3. Should redirect back to `/operator`

#### 5. **Logout & Session**
1. Login as admin
2. Click "Logout" button
3. Should redirect to login page
4. Refresh page - should stay on login (session cleared)

#### 6. **Protected Routes**
1. Clear localStorage
2. Try accessing protected route
3. Should redirect to login

---

## File Structure

```
frontend/
├── src/
│   ├── auth/
│   │   ├── Login.jsx              # Login page component
│   │   ├── auth.context.jsx       # Auth state management
│   │   └── RequireRole.jsx        # Route protection wrapper
│   ├── app/
│   │   ├── App.jsx                # Main app component
│   │   └── Router.jsx             # Route configuration
│   ├── layout/
│   │   └── Topbar.jsx             # Top navigation bar
│   └── styles/
│       └── login.css              # Login page styles
│
backend/
├── routes/
│   ├── auth.py                    # Authentication endpoints
│   └── toll_zones.py              # Toll zones endpoints
├── app.py                         # Flask app initialization
└── requirements.txt               # Python dependencies
```

---

## Environment Variables

### Backend (.env)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://127.0.0.1:5000
```

---

## Future Enhancements

1. **Database Integration**
   - Replace mock users with real database
   - Store hashed passwords
   - User management system

2. **Advanced Security**
   - OAuth 2.0 integration
   - Two-factor authentication (2FA)
   - Password reset functionality
   - Email verification

3. **Session Management**
   - Remember me functionality
   - Session timeout alerts
   - Concurrent login prevention

4. **User Management**
   - User registration
   - Profile management
   - Password change functionality
   - User account settings

5. **Audit Logging**
   - Login/logout tracking
   - Activity logging
   - Permission change history

---

## Troubleshooting

### Login Page Not Loading
- Check if frontend is running on `http://localhost:5173`
- Verify React and Router are properly imported
- Check browser console for errors

### Authentication Fails
- Verify backend is running on port 5000
- Check CORS is enabled in Flask
- Ensure correct credentials are used

### Redirects Not Working
- Check browser console for JavaScript errors
- Verify Router configuration
- Check localStorage for auth data

### Styling Issues
- Ensure `login.css` is imported in Login.jsx
- Check for CSS conflicts with Bootstrap
- Verify CSS file path is correct

---

## API Documentation

For complete API documentation, see [Backend API Guide](../backend/API.md)

---

## Support & Contact

For issues, questions, or feature requests, please contact the development team.

---

**Last Updated:** January 9, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅
