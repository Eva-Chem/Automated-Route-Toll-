import { useState, useEffect } from "react";
import MapView from "./components/MapView";
import TollPanel from "./components/TollPanel";
import TopNav from "./components/TopNav";
import TollPaymentModal from "./components/TollPaymentModal";
import SuccessModal from "./components/SuccessModal";

const App = () => {
  const [activeToll, setActiveToll] = useState(null);
  const [paymentState, setPaymentState] = useState("UNPAID");
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const handleZoneTriggered = (zone) => {
    if (!activeToll || activeToll.id !== zone.id) {
      setActiveToll(zone);
      setPaymentState("UNPAID");
    }
  };

  useEffect(() => {
    document.body.style.overflow =
      showPaymentModal || showSuccessModal ? "hidden" : "hidden";
  }, [showPaymentModal, showSuccessModal]);

  return (
    <>
      <TopNav />

      <div style={styles.layout}>
        <TollPanel
          toll={activeToll}
          paymentState={paymentState}
          onPay={() => setShowPaymentModal(true)}
        />

        <div style={styles.map}>
          <MapView onTollTriggered={handleZoneTriggered} />
        </div>
      </div>

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

      {showSuccessModal && (
        <SuccessModal
          onDone={() => {
            setPaymentState("PAID");
            setShowSuccessModal(false);
          }}
        />
      )}
    </>
  );
};

export default App;

/* ================= STYLES ================= */

const styles = {
  layout: {
    display: "flex",
    width: "100%",
    height: "calc(100vh - 56px)"
  },
  map: {
    flex: 1
  }
};
