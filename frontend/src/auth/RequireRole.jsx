import { Navigate } from "react-router-dom";
import { useAuth } from "./auth.context";

export default function RequireRole({ allow, children }) {
  const { user } = useAuth();
  return allow.includes(user.role) ? children : <Navigate to="/" />;
}
