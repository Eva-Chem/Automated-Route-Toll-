import { Link } from "react-router-dom";
import { useAuth } from "../auth/auth.context";

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <nav className="col-md-3 col-lg-2 d-md-block bg-white border-end p-3">
      <h5 className="fw-bold mb-4">Automated Toll</h5>

      <ul className="nav flex-column gap-2">
        {user.role === "admin" && (
          <>
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard">Dashboard</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard/transactions">Transactions</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard/zones">Toll Zones</Link>
            </li>
          </>
        )}

        {user.role === "operator" && (
          <>
            <li className="nav-item">
              <Link className="nav-link" to="/operator">Operator Home</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/operator/zones">Toll Zones</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}
