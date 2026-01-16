import { Link, useLocation } from "react-router-dom";
import "../styles/navbar.css";

export default function TopNav() {
  const location = useLocation();

  return (
    <header className="top-nav">
      <div className="nav-center">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/330px-Flag_of_Kenya.svg.png"
          alt="Kenya Flag"
          className="nav-flag"
        />

        <h1 className="nav-title">Kenya Toll Collection</h1>

        <p className="nav-subtitle">
          Smart, automated toll payments powered by geofencing and M-Pesa.
        </p>
      </div>

      <nav className="nav-tabs">
        <Link className={location.pathname === "/" ? "active" : ""} to="/">
          Home
        </Link>
        <Link className={location.pathname === "/about" ? "active" : ""} to="/about">
          About
        </Link>
        <Link className={location.pathname === "/contact" ? "active" : ""} to="/contact">
          Contact
        </Link>
      </nav>
    </header>
  );
}
