import { NavLink as RouterNavLink } from "react-router-dom";

export default function NavLink({ to, children }) {
  return (
    <RouterNavLink
      to={to}
      className={({ isActive }) =>
        `block p-2 rounded transition ${
          isActive
            ? "bg-slate-200 font-medium"
            : "hover:bg-slate-100"
        }`
      }
    >
      {children}
    </RouterNavLink>
  );
}
