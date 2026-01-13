import { NavLink } from "react-router-dom";
import { useAuth } from "../auth/auth.context";

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <nav className="col-md-3 col-lg-2 d-md-block bg-transparent border-0 p-3 app-sidebar">
      <h5 className="fw-bold mb-4">Automated Toll</h5>

      <ul className="nav flex-column gap-2">
        {user.role === "admin" && (
          <>
            <li className="nav-item">
              <NavLink className="nav-link" to="/dashboard" end>Dashboard</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/dashboard/transactions">Transactions</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/dashboard/zones">Toll Zones</NavLink>
            </li>
          </>
        )}

        {user.role === "operator" && (
          <>
            <li className="nav-item">
              <NavLink className="nav-link" to="/operator" end>Operator Home</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/operator/zones">Toll Zones</NavLink>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}
