import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

// Mock user database - In production, this would be handled by the backend
const MOCK_USERS = {
  admin: {
    username: "admin",
    password: "admin123",
    name: "Administrator",
    role: "admin",
    email: "admin@tolls.com",
  },
  operator: {
    username: "operator",
    password: "operator123",
    name: "Toll Operator",
    role: "operator",
    email: "operator@tolls.com",
  },
};

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
    return new Promise((resolve) => {
      setTimeout(() => {
        // Find user by username
        const userRecord = Object.values(MOCK_USERS).find(
          (u) => u.username === username
        );

        if (!userRecord) {
          resolve({
            success: false,
            error: "Invalid username or password",
          });
          return;
        }

        // Verify password
        if (userRecord.password !== password) {
          resolve({
            success: false,
            error: "Invalid username or password",
          });
          return;
        }

        // Create user session (exclude password)
        const { password: _, ...userData } = userRecord;
        const authToken = btoa(`${username}:${password}:${Date.now()}`); // Simple token generation

        setUser(userData);
        setToken(authToken);
        localStorage.setItem("auth_user", JSON.stringify(userData));
        localStorage.setItem("auth_token", authToken);

        resolve({
          success: true,
          user: userData,
          token: authToken,
        });
      }, 800); // Simulate network delay
    });
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

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
