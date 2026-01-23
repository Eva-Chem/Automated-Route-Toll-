import { useState } from "react";
import { jwtDecode } from "jwt-decode";
import axios from "axios";
import { AuthContext } from "./auth-context";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("auth_user");
    const token = localStorage.getItem("auth_token");
    return saved && token ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => {
    return localStorage.getItem("auth_token") || null;
  });

  const login = async (username, password) => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/auth/login`,
        { username, password }
      );

      const { token: authToken, user: userData } = response.data;

      // Decode JWT to verify and extract claims
      const decoded = jwtDecode(authToken);
      
      // Merge backend user data with decoded claims
      const userWithRole = {
        ...userData,
        role: decoded.role || userData.role, // Use role from JWT claims
      };

      setUser(userWithRole);
      setToken(authToken);
      localStorage.setItem("auth_user", JSON.stringify(userWithRole));
      localStorage.setItem("auth_token", authToken);

      return {
        success: true,
        user: userWithRole,
        token: authToken,
      };
    } catch (error) {
      const errorMessage =
        error.response?.data?.error ||
        error.message ||
        "Invalid username or password";

      return {
        success: false,
        error: errorMessage,
      };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("auth_user");
    localStorage.removeItem("auth_token");
  };

  const isAuthenticated = () => {
    return user !== null && token !== null;
  };

  const value = {
    user,
    token,
    login,
    logout,
    isAuthenticated: isAuthenticated(),
  };

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}

export default AuthProvider;
