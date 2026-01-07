import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const TollPaymentModal = ({ toll, onClose, onPending, onSuccess, onFailed }) => {
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);

  if (!toll) return null;

  const handleProceed = async () => {
    if (phone.length !== 10) return;

    const formattedPhone = `254${phone.slice(1)}`;

    setLoading(true);
    onPending();

    try {
      const res = await fetch(`${API_BASE}/payments/stk-push`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone: formattedPhone,
          amount: toll.charge_amount
        })
      });

      const data = await res.json();

      if (data.success) {
        onSuccess();
      } else {
        onFailed();
      }
    } catch (err) {
      onFailed();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={overlay}>
      <div style={modal}>
        <button style={closeBtn} onClick={onClose}>×</button>

        <h2>Confirm Toll Payment</h2>
        <p style={subtitle}>Enter your phone number to receive an M-Pesa prompt.</p>

        <div style={summary}>
          <span>{toll.name}</span>
          <strong>KES {toll.charge_amount}</strong>
        </div>

        <label>Phone Number</label>
        <input
          value={phone}
          maxLength={10}
          inputMode="numeric"
          placeholder="07XXXXXXXX"
          onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
          style={input}
        />

        <button style={primaryBtn} onClick={handleProceed} disabled={loading}>
          {loading ? "Payment Pending…" : "Proceed"}
        </button>
      </div>
    </div>
  );
};

export default TollPaymentModal;

/* styles unchanged */
