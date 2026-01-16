const TollPanel = ({ toll, paymentState, onPay }) => {
  return (
    <aside style={styles.panel}>
      <h2 style={styles.title}>Toll Zone</h2>

      {toll ? (
        <>
          <div style={styles.block}>
            <label>Toll Name</label>
            <strong>{toll.name}</strong>
          </div>

          <div style={styles.block}>
            <label>Amount</label>
            <strong>KES {toll.charge_amount}</strong>
          </div>

          <div style={styles.block}>
            <label>Status</label>
            <span style={styles.status(paymentState)}>
              {paymentState}
            </span>
          </div>

          {paymentState === "UNPAID" && (
            <button style={styles.cta} onClick={onPay}>
              Make Payment
            </button>
          )}
        </>
      ) : (
        <p style={styles.waiting}>Waiting for toll detection…</p>
      )}
    </aside>
  );
};

export default TollPanel;

/* ================= STYLES ================= */

const styles = {
  panel: {
    width: "360px",
    background: "#0F172A",
    color: "#E5E7EB",
    padding: "32px 24px",
    display: "flex",
    flexDirection: "column",
    gap: "24px",
    position: "relative",
    zIndex: 10
  },
  title: {
    fontSize: "20px",
    marginBottom: "16px",
    color: "#ffffff"
  },
  block: {
    display: "flex",
    flexDirection: "column",
    gap: "4px",
    fontSize: "14px"
  },
  status: (s) => ({
    display: "inline-block",
    padding: "6px 12px",
    borderRadius: "999px",
    width: "fit-content",
    background:
      s === "PAID"
        ? "#16A34A"
        : s === "PENDING"
        ? "#D97706"
        : "#DC2626",
    color: "#ffffff",
    fontSize: "13px",
    fontWeight: 600
  }),
  cta: {
    marginTop: "32px",
    padding: "14px",
    background: "#2563EB",
    color: "#ffffff",
    border: "none",
    borderRadius: "10px",
    fontSize: "15px",
    fontWeight: 600
  },
  waiting: {
    color: "#9CA3AF",
    fontSize: "14px"
  }
};
