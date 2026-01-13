import { useState } from "react";
import { useAuth } from "./auth.context";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const validateForm = () => {
    const newErrors = {};
    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    }
    if (!formData.password) {
      newErrors.password = "Password is required";
    }
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
    setApiError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setApiError("");

    try {
      // Call login with credentials - the auth context will handle the authentication
      const response = await login(formData.username, formData.password);
      
      if (response.success) {
        // Redirect based on role
        navigate(response.user.role === "admin" ? "/dashboard" : "/operator");
      } else {
        setApiError(response.error || "Login failed. Please try again.");
      }
    } catch (error) {
      setApiError(
        error.response?.data?.message || 
        "An error occurred. Please try again later."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-wrapper">
        {/* Left Side - Branding */}
        <div className="login-branding">
          <div className="branding-content">
            <div className="logo-circle">
              <svg
                className="logo-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M6 9l6-3 6 3v6l-6 3-6-3V9z" />
                <path d="M12 12v6" />
                <path d="M9 10.5l3 1.5 3-1.5" />
              </svg>
            </div>
            <h1 className="branding-title">Toll Route Manager</h1>
            <p className="branding-subtitle">
              Intelligent Route Management System
            </p>
          </div>
          <div className="features-list">
            <div className="feature-item">
              <span className="feature-icon">✓</span>
              <span>Role-Based Access Control</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">✓</span>
              <span>Real-time Toll Monitoring</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">✓</span>
              <span>Secure Authentication</span>
            </div>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="login-form-container">
          <div className="login-form-box">
            <h2 className="login-title">Welcome Back</h2>
            <p className="login-subtitle">
              Sign in to your account to continue
            </p>

            {apiError && (
              <div className="alert alert-error">
                <span className="alert-icon">⚠</span>
                {apiError}
              </div>
            )}

            <form onSubmit={handleSubmit} className="login-form">
              {/* Username Field */}
              <div className="form-group">
                <label htmlFor="username" className="form-label">
                  Username
                </label>
                <div className="input-wrapper">
                  <span className="input-icon">👤</span>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    className={`form-input ${errors.username ? "error" : ""}`}
                    placeholder="Enter your username"
                    value={formData.username}
                    onChange={handleChange}
                    disabled={loading}
                  />
                </div>
                {errors.username && (
                  <span className="error-message">{errors.username}</span>
                )}
              </div>

              {/* Password Field */}
              <div className="form-group">
                <label htmlFor="password" className="form-label">
                  Password
                </label>
                <div className="input-wrapper">
                  <span className="input-icon">🔒</span>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    className={`form-input ${errors.password ? "error" : ""}`}
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleChange}
                    disabled={loading}
                  />
                </div>
                {errors.password && (
                  <span className="error-message">{errors.password}</span>
                )}
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="btn-submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Signing in...
                  </>
                ) : (
                  "Sign In"
                )}
              </button>

              {/* Demo Credentials */}
              <div className="demo-section">
                <p className="demo-title">Demo Credentials</p>
                <div className="demo-cards">
                  <div className="demo-card admin">
                    <div className="demo-role">Administrator</div>
                    <p className="demo-text">
                      <strong>Username:</strong> admin<br />
                      <strong>Password:</strong> admin123
                    </p>
                  </div>
                  <div className="demo-card operator">
                    <div className="demo-role">Operator</div>
                    <p className="demo-text">
                      <strong>Username:</strong> operator<br />
                      <strong>Password:</strong> operator123
                    </p>
                  </div>
                </div>
              </div>
            </form>

            <p className="login-footer">
              Need help?{" "}
              <a href="#" className="link-help">
                Contact support
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
