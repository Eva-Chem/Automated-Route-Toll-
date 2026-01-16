const SuccessModal = ({ onDone }) => (
  <div style={overlay}>
    <div style={modal}>
      <h2>Payment Successful ✅</h2>
      <p>Your toll has been paid.</p>
      <button style={btn} onClick={onDone}>Done</button>
    </div>
  </div>
);

export default SuccessModal;

const overlay = {
  position: "fixed",
  inset: 0,
  background: "rgba(0,0,0,0.6)",
  backdropFilter: "blur(6px)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  zIndex: 9999
};

const modal = {
  background: "#FFFFFF",
  padding: "24px",
  borderRadius: "14px",
  textAlign: "center"
};

const btn = {
  marginTop: "16px",
  padding: "10px 20px",
  background: "#16A34A",
  color: "#FFFFFF",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer"
};
