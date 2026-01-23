import { Navigate } from "react-router-dom";
import { useAuth } from "./use-auth";
import { ROLES } from "../constants/roles";

/**
 * RequireRole Wrapper
 * 
 * Protects routes by role.
 * If user lacks required role, redirects based on role:
 * - admin → /dashboard
 * - toll_operator → /operator
 */
export default function RequireRole({ allow, children }) {
  const { user, isAuthenticated } = useAuth();

  // If not authenticated, redirect to login
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // If user's role is not in the allowed list, redirect to their role's default page
  if (!allow.includes(user.role)) {
    return (
      <Navigate to={user.role === ROLES.ADMIN ? "/dashboard" : "/operator"} replace />
    );
  }

  return children;
}
