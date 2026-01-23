import { Routes, Route, Navigate } from "react-router-dom";
import RequireRole from "../auth/RequireRole";
import AdminDashboard from "../admin/AdminDashboard";
import TransactionsPage from "../admin/TransactionsPage";
import OperatorDashboard from "../operator/OperatorDashboard";
import TollZonesPage from "../components/TollZones/TollZonesPage";
import { useAuth } from "../auth/auth.context";
import Login from "../auth/Login";
import { ROLES } from "../constants/roles";

function HomeRedirect() {
  const { user } = useAuth();
  return <Navigate to={user.role === ROLES.ADMIN ? "/dashboard" : "/operator"} />;
}

export default function Router() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />

      <Route path="/login" element={<Login />} />

      {/* Admin Routes: View-only access to zones and transactions */}
      <Route
        path="/dashboard"
        element={
          <RequireRole allow={[ROLES.ADMIN]}>
            <AdminDashboard />
          </RequireRole>
        }
      />

      <Route
        path="/dashboard/transactions"
        element={
          <RequireRole allow={[ROLES.ADMIN]}>
            <TransactionsPage />
          </RequireRole>
        }
      />

      <Route
        path="/dashboard/zones"
        element={
          <RequireRole allow={[ROLES.ADMIN]}>
            <TollZonesPage />
          </RequireRole>
        }
      />

      {/* Toll Operator Routes: Full CRUD access to zones (except DELETE) */}
      <Route
        path="/operator"
        element={
          <RequireRole allow={[ROLES.TOLL_OPERATOR]}>
            <OperatorDashboard />
          </RequireRole>
        }
      />

      <Route
        path="/operator/zones"
        element={
          <RequireRole allow={[ROLES.TOLL_OPERATOR]}>
            <TollZonesPage />
          </RequireRole>
        }
      />
    </Routes>
  );
}
