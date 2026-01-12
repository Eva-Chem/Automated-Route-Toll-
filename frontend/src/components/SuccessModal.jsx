const SuccessModal = ({ onDone }) => {
  return (
    <div style={overlay}>
      <div style={modal}>
        <div style={icon}>✓</div>
        <h2>Successful Payment!</h2>
        <p style={subtitle}>
          Your toll payment was completed successfully.
        </p>
        <button style={primaryBtn} onClick={onDone}>
          Go Back
        </button>
      </div>
    </div>
  );
};

export default SuccessModal;

/* ================= STYLES ================= */

const overlay = {
  position: "fixed",
  inset: 0,
  background: "rgba(0,0,0,0.35)",
  backdropFilter: "blur(6px)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  zIndex: 200,
  fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
};

const modal = {
  background: "#fff",
  borderRadius: "18px",
  padding: "36px",
  maxWidth: "420px",
  width: "100%",
  textAlign: "center",
  boxShadow: "0 20px 40px rgba(0,0,0,0.25)"
};

const icon = {
  width: "72px",
  height: "72px",
  borderRadius: "50%",
  border: "3px solid #22C55E",
  color: "#22C55E",
  fontSize: "32px",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  margin: "0 auto 20px"
};

const subtitle = { color: "#6B7280", marginBottom: "28px" };

const primaryBtn = {
  width: "100%",
  padding: "14px",
  background: "#2563EB",
  color: "#fff",
  borderRadius: "12px",
  border: "none",
  fontSize: "16px",
  cursor: "pointer"
};
