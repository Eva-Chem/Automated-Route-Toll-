import { useContext } from "react";
import { AuthContext } from "./auth-context";

/**
 * useAuth Hook
 * 
 * Access authentication context from any component.
 * Must be used within AuthProvider.
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
