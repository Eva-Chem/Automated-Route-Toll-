import { Routes, Route, Navigate } from "react-router-dom";
import RequireRole from "../auth/RequireRole";
import AdminDashboard from "../admin/AdminDashboard";
import Transactions from "../components/Transactions/Transactions";
import OperatorDashboard from "../operator/OperatorDashboard";
import TollZones from "../components/TollZones/TollZones";
import { useAuth } from "../auth/auth.context";
import Login from "../auth/Login";
import { mockTransactions } from "../mock/transactions.mock";
import { mockZones } from "../mock/zones.mock";

function HomeRedirect() {
  const { user, isAuthenticated } = useAuth();
  
  // If not authenticated, redirect to login
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }
  
  // Redirect based on role
  return <Navigate to={user.role === "admin" ? "/dashboard" : "/operator"} replace />;
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
            <AdminDashboard transactions={mockTransactions} zones={mockZones} />
          </RequireRole>
        }
      />

      <Route
        path="/dashboard/transactions"
        element={
          <RequireRole allow={["admin"]}>
            <Transactions transactions={mockTransactions} />
          </RequireRole>
        }
      />

      <Route
        path="/dashboard/zones"
        element={
          <RequireRole allow={["admin"]}>
            <TollZones />
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

      {/* Catch-all: redirect unknown routes to home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
