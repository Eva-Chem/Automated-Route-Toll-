import { useEffect, useState } from "react";
import DashboardLayout from "../layout/DashboardLayout";
import MapCanvas from "../map/MapCanvas";
import { useZoneStore } from "../store/zone.store";
import { getTransactions } from "../components/Transactions/Transactions.api";

export default function AdminDashboard() {
  const { zones, fetchZones } = useZoneStore();
  const [transactions, setTransactions] = useState([]);
  const [loadingTx, setLoadingTx] = useState(false);
  const [errorTx, setErrorTx] = useState("");

  useEffect(() => {
    fetchZones();
  }, [fetchZones]);

  useEffect(() => {
    const load = async () => {
      setLoadingTx(true);
      setErrorTx("");
      try {
        const data = await getTransactions();
        setTransactions(data);
      } catch (err) {
        console.error("Failed to load transactions", err);
        setErrorTx("Transactions unavailable");
      } finally {
        setLoadingTx(false);
      }
    };

    load();
  }, []);

  const completed = transactions.filter((t) => (t.status || "").toUpperCase() === "COMPLETED");
  const failed = transactions.filter((t) => (t.status || "").toUpperCase() === "FAILED");
  const totalRevenue = completed.reduce((s, t) => s + (Number(t.amount) || 0), 0);

  return (
    <DashboardLayout>
      <h3 className="mb-4">Platform Overview</h3>

      <div className="row g-3 mb-4">
        <SummaryCard title="Total Revenue Collected" value={`Ksh ${totalRevenue}`} loading={loadingTx} error={errorTx} />
        <SummaryCard title="Successful Transactions" value={completed.length} loading={loadingTx} error={errorTx} />
        <SummaryCard title="Failed Transactions" value={failed.length} loading={loadingTx} error={errorTx} />
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <MapCanvas zones={zones} mode="admin" />
        </div>
      </div>
    </DashboardLayout>
  );
}

function SummaryCard({ title, value, loading, error }) {
  return (
    <div className="col-md-4">
      <div className="card shadow-sm">
        <div className="card-body">
          <small className="text-muted">{title}</small>
          <h4 className="mt-1 mb-0">
            {loading ? "Loading..." : error ? error : value}
          </h4>
        </div>
      </div>
    </div>
  );
}
