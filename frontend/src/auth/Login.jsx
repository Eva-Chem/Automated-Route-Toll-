import { useAuth } from "./auth.context";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="container vh-100 d-flex align-items-center justify-content-center">
      <div className="card shadow-sm p-4" style={{ width: 350 }}>
        <h5 className="mb-3 text-center">Login</h5>

        <button
          className="btn btn-primary w-100 mb-2"
          onClick={() => {
            login("admin");
            navigate("/");
          }}
        >
          Login as Administrator
        </button>

        <button
          className="btn btn-outline-primary w-100"
          onClick={() => {
            login("operator");
            navigate("/");
          }}
        >
          Login as Toll Operator
        </button>
      </div>
    </div>
  );
}
