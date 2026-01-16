import { useState } from "react";
import { BrowserRouter as Router } from "react-router-dom";

import TopNav from "./components/TopNav";
import MapView from "./components/MapView";
import TollPanel from "./components/TollPanel";
import TollPaymentModal from "./components/TollPaymentModal";
import SuccessModal from "./components/SuccessModal";

import "./index.css";

function App() {
  const [activeZone] = useState({
    id: "mock-zone-001",
    name: "Nairobi CBD",
    charge_amount: 200,
    status: "unpaid"
  });

  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  return (
    <Router>
      <TopNav />

      <main className="app-shell">
        <section className="map-section">
          <MapView />
        </section>

        <section className="toll-section">
          <TollPanel
            zone={activeZone}
            onMakePayment={() => setShowPaymentModal(true)}
          />
        </section>
      </main>

      {showPaymentModal && (
        <TollPaymentModal
          toll={activeZone}
          onClose={() => setShowPaymentModal(false)}
          onSuccess={() => {
            setShowPaymentModal(false);
            setShowSuccessModal(true);
          }}
        />
      )}

      {showSuccessModal && (
        <SuccessModal onDone={() => setShowSuccessModal(false)} />
      )}
    </Router>
  );
}

export default App;
