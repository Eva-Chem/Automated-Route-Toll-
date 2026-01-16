import { Routes, Route, Navigate } from "react-router-dom";
import RequireRole from "../auth/RequireRole";
import AdminDashboard from "../admin/AdminDashboard";
import TransactionsPage from "../admin/TransactionsPage";
import OperatorDashboard from "../operator/OperatorDashboard";
import TollZonesPage from "../components/TollZones/TollZonesPage";
import { useAuth } from "../auth/auth.context";
import Login from "../auth/Login";

function HomeRedirect() {
  const { user } = useAuth();
  return <Navigate to={user.role === "admin" ? "/dashboard" : "/operator"} />;
}

export default function Router() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />

      <Route path="/login" element={<Login />} />

      <Route
        path="/dashboard"
        element={
          <RequireRole allow={["admin"]}>
            <AdminDashboard />
          </RequireRole>
        }
      />

      <Route
        path="/dashboard/transactions"
        element={
          <RequireRole allow={["admin"]}>
            <TransactionsPage />
          </RequireRole>
        }
      />

      <Route
        path="/dashboard/zones"
        element={
          <RequireRole allow={["admin"]}>
            <TollZonesPage />
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
            <TollZonesPage />
          </RequireRole>
        }
      />
    </Routes>
  );
}
