import { Navigate } from "react-router-dom";
import { useAuth } from "./auth.context";

export default function RequireRole({ allow, children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  return allow.includes(user.role) ? children : <Navigate to="/" />;
}
