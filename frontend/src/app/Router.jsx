import { Routes, Route, Navigate } from "react-router-dom";
import RequireRole from "../auth/RequireRole";
import AdminDashboard from "../admin/AdminDashboard";
import OperatorDashboard from "../operator/OperatorDashboard";
import TollZones from "../operator/TollZones";
import { useAuth } from "../auth/auth.context";

function HomeRedirect() {
  const { user } = useAuth();
  return <Navigate to={user.role === "admin" ? "/dashboard" : "/operator"} />;
}

export default function Router() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />

      <Route
        path="/dashboard"
        element={
          <RequireRole allow={["admin"]}>
            <AdminDashboard />
          </RequireRole>
        }
      />

      <Route
        path="/operator"
        element={
          <RequireRole allow={["operator"]}>
            <OperatorDashboard />
          </RequireRole>
        }
      />

      <Route
        path="/operator/zones"
        element={
          <RequireRole allow={["operator"]}>
            <TollZones />
          </RequireRole>
        }
      />
    </Routes>
  );
}
