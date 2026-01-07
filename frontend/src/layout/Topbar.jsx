import { useAuth } from "../auth/auth.context";


export default function Topbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar navbar-light bg-white rounded shadow-sm mb-4 px-3">
      <span className="navbar-text ms-auto fw-semibold">
        {user.name} ({user.role})
        <button className="btn btn-sm btn-outline-danger ms-3" onClick={logout}>
          Logout
        </button>
      </span>
    </nav>
  );
}
