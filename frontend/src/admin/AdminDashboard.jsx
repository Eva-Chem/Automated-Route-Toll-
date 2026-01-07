import DashboardLayout from "../layout/DashboardLayout";
import GoogleMapCanvas from "../map/GoogleMapCanvas";
import { mockTransactions } from "../mock/transactions.mock";
import { mockZones } from "../mock/zones.mock";

export default function AdminDashboard() {
  const totalRevenue = mockTransactions
    .filter(t => t.status === "Completed")
    .reduce((s, t) => s + t.amount, 0);

  return (
    <DashboardLayout>
      <h3 className="mb-4">Platform Overview</h3>

      <div className="row g-3 mb-4">
        <SummaryCard title="Total Revenue Collected" value={`Ksh ${totalRevenue}`} />
        <SummaryCard title="Successful Transactions" value="123" />
        <SummaryCard title="Failed Transactions" value="50" />
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <GoogleMapCanvas zones={mockZones} readOnly />
        </div>
      </div>
    </DashboardLayout>
  );
}

function SummaryCard({ title, value }) {
  return (
    <div className="col-md-4">
      <div className="card shadow-sm">
        <div className="card-body">
          <small className="text-muted">{title}</small>
          <h4>{value}</h4>
        </div>
      </div>
    </div>
  );
}
