import "../styles/home.css";

export default function TollPanel({ zone, onMakePayment }) {
  return (
    <div className="toll-section-inner">
      <div className="toll-card">
        <h2 className="toll-title">Automated Toll Information</h2>

        <div className="toll-row">
          <span className="label">Toll Zone</span>
          <span className="value">{zone.zone_name}</span>
        </div>

        <div className="toll-row">
          <span className="label">Amount</span>
          <span className="value">KES {zone.charge_amount}</span>
        </div>

        <div className="toll-row">
          <span className="label">Status</span>
          <span className={`status-pill ${zone.status === "paid" ? "paid" : "unpaid"}`}>
            {zone.status === "paid" ? "Paid" : "Unpaid"}
          </span>
        </div>

        {zone.status !== "paid" && (
          <button className="primary-btn" onClick={onMakePayment}>
            Make Payment
          </button>
        )}
      </div>
    </div>
  );
}
