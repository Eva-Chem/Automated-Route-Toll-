import "../styles/home.css";

export default function TollPanel({ zone, onMakePayment }) {
  return (
    <div className="toll-section-inner">
      <div className="toll-card">
        <h2 className="toll-title">Automated Toll Information</h2>

        <div className="toll-row">
          <span className="label">Toll Zone</span>
          <span className="value">{zone.name}</span>
        </div>

        <div className="toll-row">
          <span className="label">Amount</span>
          <span className="value">KES {zone.charge_amount}</span>
        </div>

        <div className="toll-row">
          <span className="label">Status</span>
          <span className="status-pill unpaid">Unpaid</span>
        </div>

        <button className="primary-btn" onClick={onMakePayment}>
          Make Payment
        </button>
      </div>
    </div>
  );
}
