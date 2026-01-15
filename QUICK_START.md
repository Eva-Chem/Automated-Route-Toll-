# Quick Start Guide - Login & RBAC System

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- npm or yarn

---

## 📦 Installation

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

✅ Backend will be available at: `http://127.0.0.1:5000`

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend will be available at: `http://localhost:5173`

---

## 🔐 Test Credentials

### Administrator Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Complete system access, all features

### Operator Account
- **Username:** `operator`
- **Password:** `operator123`
- **Access:** Operational features only

---

## 🎯 Quick Test Flow

### 1. Login as Administrator
1. Open http://localhost:5173
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click "Sign In"
5. ✅ You'll be redirected to Admin Dashboard (`/dashboard`)

### 2. Access Admin Features
- View Dashboard
- Manage Toll Zones
- View Transactions
- View Reports

### 3. Logout
1. Click "Logout" button in top-right
2. ✅ Redirected to login page
3. Session is cleared

### 4. Login as Operator
1. Enter username: `operator`
2. Enter password: `operator123`
3. Click "Sign In"
4. ✅ You'll be redirected to Operator Dashboard (`/operator`)

### 5. Try Unauthorized Access
1. While logged in as operator
2. Try accessing `/dashboard`
3. ✅ Automatically redirected back to `/operator`

---

## 🎨 Login Page Features

### UI Elements
- **Split Layout:** Branding on left, form on right
- **Modern Design:** Gradient backgrounds, smooth animations
- **Responsive:** Works on desktop, tablet, and mobile
- **Input Fields:** Username and password with validation
- **Error Messages:** Clear feedback for invalid input
- **Loading State:** Spinner during authentication
- **Demo Credentials:** Built-in reference for testing

### Validations
- ✅ Username required
- ✅ Password required
- ✅ Invalid credentials detection
- ✅ Network error handling
- ✅ Real-time error clearing

---

## 📁 Project Structure

```
Automated-Route-Toll/
├── frontend/
│   └── src/
│       ├── auth/
│       │   ├── Login.jsx (Modern login page)
│       │   ├── auth.context.jsx (Auth state)
│       │   └── RequireRole.jsx (Route protection)
│       ├── app/
│       │   └── Router.jsx (Route configuration)
│       ├── layout/
│       │   └── Topbar.jsx (User info & logout)
│       └── styles/
│           └── login.css (Beautiful login styling)
│
└── backend/
    ├── routes/
    │   └── auth.py (Authentication endpoints)
    ├── app.py (Flask app)
    └── requirements.txt (Dependencies)
```

---

## 🔒 How It Works

### Authentication Flow
```
1. User enters credentials on Login page
2. Form validation happens (client-side)
3. If valid, request sent to backend (/api/auth/login)
4. Backend verifies credentials
5. If correct, JWT token is generated
6. Token & user data stored in localStorage
7. User redirected to role-specific dashboard
```

### Route Protection
```
1. RequireRole wrapper checks each protected route
2. If user not authenticated → redirect to /login
3. If user role not allowed → redirect to their dashboard
4. If authorized → load requested component
```

### Session Management
```
1. On page load, check localStorage for stored session
2. If session exists and valid, auto-login user
3. User can refresh page without losing session
4. Logout clears localStorage and session
```

---

## 🧪 Testing Scenarios

### ✅ Valid Login Test
1. Enter `admin` / `admin123`
2. Observe loading spinner
3. Redirected to `/dashboard`
4. See admin dashboard content

### ❌ Invalid Credentials Test
1. Enter `admin` / `wrongpassword`
2. See error message
3. Stay on login page
4. Try again

### 🛡️ Authorization Test
1. Login as `operator`
2. Navigate to `/dashboard` manually
3. Auto-redirect to `/operator`
4. Cannot access admin features

### 🔓 Session Test
1. Login as any user
2. Refresh page (F5)
3. Session persists, no redirect to login
4. User still logged in

### 🚪 Logout Test
1. Click Logout button
2. Redirected to login page
3. Refresh page - stays on login
4. Session completely cleared

---

## 🎨 UI/UX Highlights

### Modern Login Page
- **Beautiful Gradient:** Blue to purple theme
- **Split Layout:** Branding + Form separation
- **Icons:** Visual indicators for inputs
- **Animations:** Smooth transitions and slide effects
- **Demo Credentials:** Easy reference cards
- **Error Handling:** Clear error messages
- **Loading Feedback:** Spinner animation

### Responsive Design
- **Desktop:** Full side-by-side layout
- **Tablet:** Responsive columns with adjustments
- **Mobile:** Single column, optimized spacing
- **Dark Mode:** Automatic theme detection

---

## 🔑 Key Features

✅ **Secure Authentication**
- Form validation
- Password field masking
- Error message security

✅ **Role-Based Access Control**
- Two distinct roles (Admin, Operator)
- Route-level protection
- Automatic redirects based on role

✅ **Great UX**
- Modern, clean design
- Loading states
- Error messages
- Demo credentials
- Responsive layout

✅ **Session Management**
- Persistent login
- localStorage integration
- Logout functionality
- Auto-redirect for unauthenticated

✅ **Error Handling**
- Form validation errors
- Network error handling
- Invalid credential feedback
- Unauthorized access handling

---

## 📝 Common Tasks

### Change Default Credentials
Edit in `frontend/src/auth/auth.context.jsx` (MOCK_USERS)

```javascript
const MOCK_USERS = {
  admin: {
    username: "admin",
    password: "admin123",  // ← Change here
    name: "Administrator",
    role: "admin",
    email: "admin@tolls.com",
  },
  // ...
};
```

### Customize Login Page Colors
Edit in `frontend/src/styles/login.css` (CSS variables)

```css
:root {
  --primary-color: #2563eb;      /* ← Change blue */
  --primary-dark: #1e40af;       /* ← Change dark blue */
  --secondary-color: #10b981;    /* ← Change green */
}
```

### Add New User Role
1. Add role to mock_users in both frontend and backend
2. Create new role-specific dashboard
3. Add route in Router.jsx with RequireRole wrapper
4. Update navigation to include new role

---

## 🐛 Troubleshooting

### Issue: Login page shows blank
- **Solution:** Check browser console for errors
- Clear cache and refresh
- Verify node_modules are installed (`npm install`)

### Issue: Can't submit login form
- **Solution:** Check backend is running (`python app.py`)
- Verify CORS is enabled
- Check network tab for API errors

### Issue: Page refreshes and lose login
- **Solution:** Check if localStorage is enabled
- Check browser console for storage errors
- Try incognito mode

### Issue: Stuck on login page after logout
- **Solution:** Clear localStorage manually
- Hard refresh page (Ctrl+Shift+R)
- Check browser's Application > Storage

---

## 📚 Additional Resources

- [Full Authentication Documentation](../AUTHENTICATION.md)
- [Backend API Guide](../backend/routes/auth.py)
- [React Router Documentation](https://reactrouter.com)
- [Flask Documentation](https://flask.palletsprojects.com)

---

## ✨ Next Steps

1. **Test the login system** with provided credentials
2. **Explore role-specific dashboards** (Admin vs Operator)
3. **Review security features** implemented
4. **Customize colors** and branding if needed
5. **Read full documentation** for advanced setup

---

## 🎯 Success Indicators

You'll know everything is working when:

✅ Login page loads with beautiful UI
✅ Can login with admin / admin123
✅ Redirected to admin dashboard
✅ Can logout successfully
✅ Can login with operator / operator123
✅ Operator cannot access admin features
✅ Session persists on page refresh
✅ Error messages appear for invalid login

---

**Enjoy your secure, role-based authentication system! 🚀**

Last updated: January 9, 2026
