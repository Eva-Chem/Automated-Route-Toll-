import { useAuth } from "../auth/auth.context";
import { useNavigate } from "react-router-dom";

export default function Topbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar app-topbar mb-4 px-3">
      <span className="navbar-text ms-auto fw-semibold">
        <span className="me-3">
          👤 {user?.name} <span className="badge bg-primary">{user?.role}</span>
        </span>
        <button 
          className="btn btn-sm btn-outline-danger" 
          onClick={handleLogout}
          title="Sign out and return to login"
        >
          🚪 Logout
        </button>
      </span>
    </nav>
  );
}
