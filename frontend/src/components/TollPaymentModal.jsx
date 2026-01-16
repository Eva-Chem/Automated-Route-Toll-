import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:5001";

const TollPaymentModal = ({ toll, onClose, onSuccess, onFailed }) => {
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!toll) return null;

  const handleProceed = async () => {
    setError("");

    // ✅ Must be 254XXXXXXXXX (12 digits)
    if (!phone.startsWith("254") || phone.length !== 12) {
      setError("Enter a valid Safaricom number (254XXXXXXXXX)");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/payments/stk-push`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone,
          amount: toll.charge_amount,
          zone_id: toll.id // ✅ THIS FIXES NULL ZONE_ID
        })
      });

      const data = await res.json();

      if (data.success && data.response?.ResponseCode === "0") {
        onSuccess();
      } else {
        setError(
          data.response?.errorMessage ||
          "Payment could not be initiated"
        );
        onFailed?.();
      }
    } catch (err) {
      setError("Network error. Please try again.");
      onFailed?.();
    } finally {
      setLoading(false);
    }
  };

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
            style={phoneInput}
            value={phone.replace(/^254/, "")}
            onChange={(e) =>
              setPhone("254" + e.target.value.replace(/\D/g, ""))
            }
            placeholder="7XXXXXXXX"
            maxLength={9}
            inputMode="numeric"
          />
        </div>

        {error && <p style={errorText}>{error}</p>}

        <button
          style={primaryBtn}
          onClick={handleProceed}
          disabled={loading}
        >
          {loading ? "Sending STK…" : "Pay Now"}
        </button>
      </div>
    </div>
  );
};

export default TollPaymentModal;

/* ================= STYLES ================= */

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
  padding: "36px",
  maxWidth: "420px",
  width: "100%",
  boxShadow: "0 20px 40px rgba(0,0,0,0.25)"
};

const closeBtn = {
  position: "absolute",
  top: "14px",
  right: "18px",
  fontSize: "20px",
  border: "none",
  background: "none",
  cursor: "pointer"
};

const subtitle = { color: "#6B7280", marginBottom: "20px" };

const summary = {
  display: "flex",
  justifyContent: "space-between",
  marginBottom: "20px",
  fontWeight: 600
};

const phoneWrap = {
  display: "flex",
  alignItems: "center",
  border: "1px solid #D1D5DB",
  borderRadius: "10px",
  overflow: "hidden",
  marginBottom: "10px"
};

const prefix = {
  padding: "12px",
  background: "#F3F4F6",
  color: "#6B7280",
  fontWeight: 600
};

const phoneInput = {
  flex: 1,
  border: "none",
  padding: "12px",
  outline: "none"
};

const errorText = {
  color: "#DC2626",
  fontSize: "14px",
  marginBottom: "12px"
};

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
