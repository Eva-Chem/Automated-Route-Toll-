import { useEffect, useMemo, useState } from "react";
import DashboardLayout from "../layout/DashboardLayout";
import { getTransactions } from "../components/Transactions/Transactions.api";

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await getTransactions();
        setTransactions(data);
      } catch (err) {
        console.error("Failed to load transactions", err);
        setError("Failed to load transactions. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const filtered = useMemo(() => {
    const term = search.toLowerCase();
    return transactions.filter((t) =>
      (t.zone_name || "").toLowerCase().includes(term) ||
      (t.ref || "").toLowerCase().includes(term)
    );
  }, [transactions, search]);

  const formatDateTime = (iso) => {
    if (!iso) return { date: "-", time: "-" };
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return { date: "-", time: "-" };
    return {
      date: d.toLocaleDateString(),
      time: d.toLocaleTimeString(),
    };
  };

  return (
    <DashboardLayout>
      <h3 className="mb-3">Transaction Logs</h3>

      <input
        className="form-control mb-3"
        placeholder="Search by Toll Name or Reference ID"
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <table className="table table-striped">
        <thead>
          <tr>
            <th>Date</th><th>Time</th><th>Toll</th><th>Phone</th>
            <th>Ref</th><th>Amount</th><th>Status</th>
          </tr>
        </thead>
        <tbody>
          {loading && (
            <tr>
              <td colSpan="7" className="text-center">Loading...</td>
            </tr>
          )}
          {error && !loading && (
            <tr>
              <td colSpan="7" className="text-center text-danger">{error}</td>
            </tr>
          )}
          {!loading && !error && filtered.length === 0 && (
            <tr>
              <td colSpan="7" className="text-center text-muted">No transactions found</td>
            </tr>
          )}
          {!loading && !error && filtered.map((t) => {
            const { date, time } = formatDateTime(t.created_at);
            const status = (t.status || "").toUpperCase();
            const badge = status === "COMPLETED" ? "success" : status === "FAILED" ? "danger" : "warning";
            return (
              <tr key={t.id || t.ref}>
                <td>{date}</td>
                <td>{time}</td>
                <td>{t.zone_name || "-"}</td>
                <td>{t.phone || "-"}</td>
                <td>{t.ref || "-"}</td>
                <td>{t.amount}</td>
                <td>
                  <span className={`badge bg-${badge}`}>
                    {status || "UNKNOWN"}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </DashboardLayout>
  );
}
