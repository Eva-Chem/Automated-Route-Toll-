import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function DashboardLayout({ children }) {
  return (
    <div className="container-fluid">
      <div className="row min-vh-100">
        <Sidebar />
        <main className="col p-4 bg-light">
          <Topbar />
          {children}
        </main>
      </div>
    </div>
  );
}
