import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const TollPaymentModal = ({ toll, onClose, onPending, onSuccess, onFailed }) => {
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!toll) return null;

  const handlePayment = async () => {
    if (phone.length !== 10) {
      setError("Enter a valid Safaricom number");
      return;
    }

    setLoading(true);
    onPending();

    try {
      const res = await fetch(`${API_BASE}/payments/stk-push`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone: `254${phone.slice(1)}`,
          amount: toll.charge_amount
        })
      });

      const data = await res.json();

      data.success ? onSuccess() : onFailed();
    } catch {
      onFailed();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={overlay}>
      <div style={modal}>
        <button style={closeBtn} onClick={onClose}>×</button>

        <h2>Confirm Payment</h2>
        <p>You’ll receive an M-Pesa prompt.</p>

        <input
          placeholder="07XXXXXXXX"
          value={phone}
          onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
          style={input}
        />

        {error && <p style={errorText}>{error}</p>}

        <button style={payBtn} onClick={handlePayment} disabled={loading}>
          {loading ? "Processing…" : "Pay Now"}
        </button>
      </div>
    </div>
  );
};

export default TollPaymentModal;

/* STYLES */

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
  width: "320px",
  position: "relative"
};

const closeBtn = {
  position: "absolute",
  top: "10px",
  right: "12px",
  border: "none",
  background: "transparent",
  fontSize: "20px",
  cursor: "pointer"
};

const input = {
  width: "100%",
  padding: "10px",
  marginTop: "12px",
  borderRadius: "8px",
  border: "1px solid #D1D5DB"
};

const payBtn = {
  marginTop: "16px",
  width: "100%",
  padding: "12px",
  background: "#2563EB",
  color: "#FFFFFF",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer"
};

const errorText = {
  color: "#DC2626",
  fontSize: "13px",
  marginTop: "8px"
};
