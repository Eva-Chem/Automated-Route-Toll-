import DashboardLayout from "../../layout/DashboardLayout";
import { useState } from "react";

export default function Transactions({ transactions }) {
  const [search, setSearch] = useState("");

  const filtered = transactions.filter(t =>
    t.toll.toLowerCase().includes(search.toLowerCase()) ||
    t.ref.toLowerCase().includes(search.toLowerCase())
  );

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
          {filtered.map(t => (
            <tr key={t.id}>
              <td>{t.date}</td>
              <td>{t.time}</td>
              <td>{t.toll}</td>
              <td>{t.phone}</td>
              <td>{t.ref}</td>
              <td>{t.amount}</td>
              <td>
                <span className={`badge bg-${
                  t.status === "Completed" ? "success" :
                  t.status === "Failed" ? "danger" : "warning"
                }`}>
                  {t.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </DashboardLayout>
  );
}