import DashboardLayout from "../layout/DashboardLayout";
import Card from "../components/Card";

export default function OperatorDashboard() {
  return (
    <DashboardLayout>
      <h1 className="page-title">Operator Dashboard</h1>
      <div className="grid grid-cols-2 gap-6">
        <Card>
          <h2 className="text-xl font-semibold mb-2">Toll Zones</h2>
          <p>Manage toll zones and geo-fencing.</p>
        </Card>
        <Card>
          <h2 className="text-xl font-semibold mb-2">Transactions</h2>
          <p>View recent transactions.</p>
        </Card>
      </div>
    </DashboardLayout>
  );
}
