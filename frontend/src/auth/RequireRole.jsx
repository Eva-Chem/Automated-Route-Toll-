import { Navigate } from "react-router-dom";
import { useAuth } from "./auth.context";

export default function RequireRole({ allow, children }) {
  const { user, isAuthenticated } = useAuth();

  // If not authenticated, redirect to login
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // If user's role is not in the allowed list, redirect to home
  if (!allow.includes(user.role)) {
    return (
      <Navigate to={user.role === "admin" ? "/dashboard" : "/operator"} replace />
    );
  }

  return children;
}
