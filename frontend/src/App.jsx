import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import TopNav from "./components/TopNav";
import MapView from "./components/MapView";
import TollPanel from "./components/TollPanel";
import TollPaymentModal from "./components/TollPaymentModal";
import SuccessModal from "./components/SuccessModal";

import About from "./pages/About";
import Contact from "./pages/Contact";

import "./index.css";

function App() {
  const [activeZone, setActiveZone] = useState(null);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const handleZoneDetected = (zone) => {
    setActiveZone({
      ...zone,
      status: "unpaid"
    });
  };

  const handlePaymentSuccess = () => {
    setActiveZone((prev) =>
      prev ? { ...prev, status: "paid" } : prev
    );
    setShowPaymentModal(false);
    setShowSuccessModal(true);
  };

  return (
    <Router>
      <TopNav />

      <Routes>
        <Route
          path="/"
          element={
            <>
              <main className="app-shell">
                <section className="map-section">
                  <MapView onTollTriggered={handleZoneDetected} />
                </section>

                <section className="toll-section">
                  <TollPanel
                    zone={activeZone}
                    onMakePayment={() => setShowPaymentModal(true)}
                  />
                </section>
              </main>

              {showPaymentModal && activeZone && (
                <TollPaymentModal
                  toll={activeZone}       // ✅ contains zone_id
                  onClose={() => setShowPaymentModal(false)}
                  onSuccess={handlePaymentSuccess}
                />
              )}

              {showSuccessModal && (
                <SuccessModal
                  onDone={() => setShowSuccessModal(false)}
                />
              )}
            </>
          }
        />

        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </Router>
  );
}

export default App;
