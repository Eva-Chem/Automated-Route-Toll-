import { useState, useEffect } from "react";
import DashboardLayout from "../../layout/DashboardLayout";
import MapCanvas from "../../map/MapCanvas";
import { useZoneStore } from "../../store/zone.store";
import { useAuth } from "../../auth/auth.context";

export default function TollZones() {
  const { user } = useAuth();
  const { zones, addZone, updateZone, deleteZone, fetchZones } = useZoneStore();
  const [selectedId, setSelectedId] = useState(null);

  // Fetch zones on mount
  useEffect(() => {
    fetchZones();
  }, [fetchZones]);

  const handleCreateZone = (coordinates) => {
    addZone({
      id: Date.now(),
      name: "New Toll Zone",
      charge_amount: 0,
      coordinates,
    });
  };

  const handleUpdateZone = (id, coordinates) => {
    updateZone(id, { coordinates });
  };

  return (
    <DashboardLayout>
      <h3 className="mb-4">Toll Zones</h3>

      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <MapCanvas
            zones={zones}
            mode={user?.role === "operator" ? "operator" : "admin"}
            onCreateZone={user?.role === "operator" ? handleCreateZone : undefined}
            onUpdateZone={user?.role === "operator" ? handleUpdateZone : undefined}
          />
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Zone List</h5>
        </div>
        <table className="table table-bordered mb-0">
          <thead>
            <tr>
              <th>Name</th>
              <th>Charge (Ksh)</th>
              {user?.role === "operator" && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {zones.length === 0 ? (
              <tr>
                <td colSpan={user?.role === "operator" ? 3 : 2} className="text-center text-muted">
                  No zones available
                </td>
              </tr>
            ) : (
              zones.map((zone) => (
                <tr key={zone.id}>
                  <td>{zone.name}</td>
                  <td>{zone.charge_amount}</td>
                  {user?.role === "operator" && (
                    <td>
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() => deleteZone(zone.id)}
                      >
                        Delete
                      </button>
                    </td>
                  )}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </DashboardLayout>
  );
}
