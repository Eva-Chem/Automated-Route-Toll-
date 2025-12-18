import { useEffect, useState } from "react";
import { checkBackendHealth } from "./api";

function App() {
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    checkBackendHealth()
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("backend not reachable"));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Automated Toll Tracker</h1>
      <p>Backend status: {status}</p>
    </div>
  );
}

export default App;
