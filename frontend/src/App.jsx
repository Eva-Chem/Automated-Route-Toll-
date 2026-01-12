import { useState, useEffect } from "react";
import MapView from "./components/MapView";
import TollPaymentModal from "./components/TollPaymentModal";
import SuccessModal from "./components/SuccessModal";

const App = () => {
  const [activeToll, setActiveToll] = useState(null);
  const [paymentState, setPaymentState] = useState("UNPAID");
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  /**
   * ✅ CRITICAL FIX:
   * Only reset payment state if the toll zone actually changes
   */
  const handleZoneTriggered = (zone) => {
    if (!activeToll || activeToll.id !== zone.id) {
      setActiveToll(zone);
      setPaymentState("UNPAID");
    }
  };

  /* Lock background scroll when any modal is open */
  useEffect(() => {
    document.body.style.overflow =
      showPaymentModal || showSuccessModal ? "hidden" : "auto";
  }, [showPaymentModal, showSuccessModal]);

  return (
    <>
      {/* MAIN PAGE */}
      <div
        style={{
          ...page,
          filter:
            showPaymentModal || showSuccessModal ? "blur(6px)" : "none",
          pointerEvents:
            showPaymentModal || showSuccessModal ? "none" : "auto"
        }}
      >
        <header style={header}>
          <h1>Kenya Toll Collection</h1>
          <p>Automated toll payment based on your location</p>
        </header>

        <section style={mapSection}>
          <MapView onTollTriggered={handleZoneTriggered} />
        </section>

        <section style={infoSection}>
          <div style={card}>
            <h2>Toll Information</h2>

            {activeToll ? (
              <>
                <p>
                  <strong>Location:</strong> {activeToll.name}
                </p>
                <p>
                  <strong>Amount:</strong> KES {activeToll.charge_amount}
                </p>
                <p>
                  <strong>Status:</strong>{" "}
                  <span style={status(paymentState)}>
                    {paymentState}
                  </span>
                </p>

                {/* CTA ONLY shows if UNPAID */}
                {paymentState === "UNPAID" && (
                  <button
                    style={cta}
                    onClick={() => setShowPaymentModal(true)}
                  >
                    Make Payment
                  </button>
                )}
              </>
            ) : (
              <p>Waiting for toll detection…</p>
            )}
          </div>
        </section>
      </div>

      {/* PAYMENT MODAL */}
      {showPaymentModal && (
        <TollPaymentModal
          toll={activeToll}
          onClose={() => setShowPaymentModal(false)}
          onPending={() => setPaymentState("PENDING")}
          onSuccess={() => {
            setShowPaymentModal(false);
            setShowSuccessModal(true);
          }}
          onFailed={() => {
            setPaymentState("FAILED");
            setShowPaymentModal(false);
          }}
        />
      )}

      {/* SUCCESS MODAL */}
      {showSuccessModal && (
        <SuccessModal
          onDone={() => {
            setPaymentState("PAID"); // ✅ PAYMENT STATUS FIX
            setShowSuccessModal(false);
          }}
        />
      )}
    </>
  );
};

export default App;

/* ================= STYLES ================= */

const page = {
  fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
  background: "#F3F4F6",
  minHeight: "100vh"
};

const header = {
  padding: "20px",
  background: "#fff",
  borderBottom: "1px solid #E5E7EB"
};

const mapSection = {
  width: "100%",
  background: "#fff"
};

const infoSection = {
  width: "100%",
  background: "#F3F4F6",
  padding: "16px"
};

const card = {
  width: "100%",
  background: "#fff",
  padding: "24px",
  borderRadius: "16px",
  boxShadow: "0 10px 25px rgba(0,0,0,0.08)"
};

const cta = {
  marginTop: "16px",
  padding: "12px 28px",
  background: "#2563EB",
  color: "#fff",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer",
  fontSize: "16px"
};

const status = (s) => ({
  color: s === "PAID" ? "green" : s === "PENDING" ? "orange" : "red"
});
