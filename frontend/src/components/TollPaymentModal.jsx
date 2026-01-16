import { useState } from "react";

export default function TollPaymentModal({ toll, onClose, onSuccess }) {
  const [phone, setPhone] = useState("");

  return (
    <div style={overlay}>
      <div style={modal}>
        <button style={closeBtn} onClick={onClose}>×</button>

        <h2>Confirm Toll Payment</h2>
        <p style={subtitle}>
          Enter your Safaricom number to receive an M-Pesa prompt.
        </p>

        <div style={summary}>
          <span>{toll.name}</span>
          <strong>KES {toll.charge_amount}</strong>
        </div>

        <label>Phone Number</label>
        <div style={phoneWrap}>
          <span style={prefix}>254</span>
          <input
            style={input}
            placeholder="7XXXXXXXX"
            value={phone}
            onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
          />
        </div>

        <button style={primaryBtn} onClick={onSuccess}>
          Pay Now
        </button>
      </div>
    </div>
  );
}

/* ===== styles ===== */

const overlay = {
  position: "fixed",
  inset: 0,
  background: "rgba(0,0,0,0.35)",
  backdropFilter: "blur(6px)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  zIndex: 200
};

const modal = {
  background: "#fff",
  borderRadius: "18px",
  padding: "32px",
  width: "420px",
  position: "relative"
};

const closeBtn = {
  position: "absolute",
  right: "16px",
  top: "12px",
  border: "none",
  background: "transparent",
  fontSize: "22px",
  cursor: "pointer"
};

const subtitle = { color: "#6B7280", marginBottom: "16px" };

const summary = {
  display: "flex",
  justifyContent: "space-between",
  marginBottom: "20px"
};

const phoneWrap = {
  display: "flex",
  border: "1px solid #E5E7EB",
  borderRadius: "10px",
  overflow: "hidden",
  marginBottom: "24px"
};

const prefix = {
  padding: "12px",
  background: "#F3F4F6",
  color: "#6B7280"
};

const input = {
  flex: 1,
  padding: "12px",
  border: "none",
  outline: "none"
};

const primaryBtn = {
  width: "100%",
  padding: "14px",
  background: "#0B1F33",
  color: "#fff",
  borderRadius: "12px",
  border: "none",
  fontSize: "16px",
  cursor: "pointer"
};
