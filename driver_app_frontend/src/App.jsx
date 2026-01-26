import { useState } from "react";
import TopNav from "./components/TopNav";
import MapView from "./components/MapView";
import TollPanel from "./components/TollPanel";
import TollPaymentModal from "./components/TollPaymentModal";
import SuccessModal from "./components/SuccessModal";
import "./index.css";

function App() {
  const [activeZone, setActiveZone] = useState(null);
  const [showPayment, setShowPayment] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleTollDetected = (zone) => {
    setActiveZone((prev) => {
      // ✅ Do NOT overwrite a paid zone
      if (prev?.zone_id === zone.zone_id) return prev;

      return {
        ...zone,
        status: "unpaid"
      };
    });
  };

  const handlePaymentSuccess = () => {
    setActiveZone((prev) => ({
      ...prev,
      status: "paid"
    }));

    setShowPayment(false);
    setShowSuccess(true);
  };

  return (
    <>
      <TopNav />

      <main className="app-shell">
        <section className="map-section">
          <MapView onTollDetected={handleTollDetected} />
        </section>

        <section className="toll-section">
          {activeZone && <TollPanel zone={activeZone} onMakePayment={() => setShowPayment(true)} />}
        </section>
      </main>

      {showPayment && activeZone?.status !== "paid" && (
        <TollPaymentModal
          toll={activeZone}
          onClose={() => setShowPayment(false)}
          onSuccess={handlePaymentSuccess}
        />
      )}

      {showSuccess && (
        <SuccessModal onDone={() => setShowSuccess(false)} />
      )}
    </>
  );
}

export default App;
