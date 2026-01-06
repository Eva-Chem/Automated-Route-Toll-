import DashboardLayout from "../layout/DashboardLayout";
import { mockTransactions } from "../mock/transactions.mock";

export default function AdminDashboard() {
  const revenue = mockTransactions.reduce((s, t) => s + t.amount, 0);

  return (
    <DashboardLayout>
      <h3 className="mb-4">Admin Dashboard</h3>

      <div className="row g-4 mb-4">
        <div className="col-md-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h6>Total Revenue</h6>
              <h4>KES {revenue}</h4>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h6>Completed</h6>
              <h4>120</h4>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h6>Failed</h6>
              <h4>15</h4>
            </div>
          </div>
        </div>
      </div>

      <div className="card shadow-sm">
        <div className="card-header fw-semibold">Transactions</div>
        <table className="table table-striped mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {mockTransactions.map(t => (
              <tr key={t.id}>
                <td>{t.id}</td>
                <td>KES {t.amount}</td>
                <td>
                  <span className={`badge bg-${t.status === "Completed" ? "success" : "danger"}`}>
                    {t.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardLayout>
  );
}
