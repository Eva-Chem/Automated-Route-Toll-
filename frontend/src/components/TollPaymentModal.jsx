import { useState, useRef, useEffect } from "react";
import { API_BASE_URL } from "../config/api";

export default function TollPaymentModal({ toll, onClose, onSuccess }) {
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const pollRef = useRef(null);

  useEffect(() => {
    return () => {
      // Cleanup polling when modal unmounts
      if (pollRef.current) {
        clearInterval(pollRef.current);
      }
    };
  }, []);

  const startPollingStatus = (checkoutRequestId) => {
    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(
          `${API_BASE_URL}/payments/status/${checkoutRequestId}`
        );
        const data = await res.json();

        if (!data.success) return;

        if (data.status === "paid") {
          clearInterval(pollRef.current);
          pollRef.current = null;
          setLoading(false);
          onSuccess(); // ✅ THIS now always fires
        }

        if (data.status === "failed") {
          clearInterval(pollRef.current);
          pollRef.current = null;
          setLoading(false);
          setError("Payment failed or was cancelled.");
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 3000);
  };

  const handlePayNow = async () => {
    setError("");

    if (phone.length !== 9) {
      setError("Enter a valid Safaricom number");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/payments/stk-push`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone: `254${phone}`,
          amount: toll.charge_amount,
          zone_id: toll.zone_id
        })
      });

      const data = await res.json();

      if (data.success && data.response?.CheckoutRequestID) {
        startPollingStatus(data.response.CheckoutRequestID);
      } else {
        setLoading(false);
        setError("Unable to initiate payment.");
      }
    } catch (err) {
      console.error("STK Push error:", err);
      setLoading(false);
      setError("Network error. Please try again.");
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
          <span style={summaryText}>{toll.zone_name}</span>
          <strong style={summaryText}>KES {toll.charge_amount}</strong>
        </div>

        <label style={label}>Phone Number</label>
        <div style={phoneWrap}>
          <span style={prefix}>254</span>
          <input
            style={input}
            placeholder="7XXXXXXXX"
            value={phone}
            disabled={loading}
            onChange={(e) =>
              setPhone(e.target.value.replace(/\D/g, ""))
            }
          />
        </div>

        {error && (
          <p style={{ color: "#DC2626", marginBottom: "12px" }}>
            {error}
          </p>
        )}

        <button
          style={primaryBtn}
          onClick={handlePayNow}
          disabled={loading}
        >
          {loading ? "Sending STK Push..." : "Pay Now"}
        </button>
      </div>
    </div>
  );
}

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

const subtitle = {
  color: "#6B7280",
  marginBottom: "16px",
  textAlign: "left"
};

const summary = {
  display: "flex",
  justifyContent: "space-between",
  marginBottom: "20px"
};

const summaryText = {
  fontSize: "16px",
  fontWeight: 600
};

const label = {
  fontSize: "13px",
  color: "#6B7280",
  marginBottom: "6px",
  display: "block"
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
