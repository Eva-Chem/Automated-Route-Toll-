import DashboardLayout from "../layout/DashboardLayout";
import GoogleMapCanvas from "../map/GoogleMapCanvas";
import { useZones } from "../store/zone.store";
import { useState } from "react";

export default function TollZones() {
  const { zones, addZone, updateZone, deleteZone } = useZones();
  const [selected, setSelected] = useState(null);
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");

  return (
    <DashboardLayout>
      <h3 className="mb-4">Toll Zone Management</h3>

      <div className="row g-4">
        <div className="col-lg-8">
          <GoogleMapCanvas
            zones={zones}
            selectedId={selected?.id}
            onSelect={(z) => {
              setSelected(z);
              setName(z.name);
              setAmount(z.amount);
            }}
            onCreate={(coords) =>
              addZone({ name, amount, coordinates: coords })
            }
            onUpdate={updateZone}
          />
        </div>

        <div className="col-lg-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5>{selected ? "Edit Zone" : "Create Zone"}</h5>

              <div className="mb-3">
                <label className="form-label">Zone Name</label>
                <input
                  className="form-control"
                  value={name}
                  onChange={e => setName(e.target.value)}
                />
              </div>

              <div className="mb-3">
                <label className="form-label">Charge (KES)</label>
                <input
                  className="form-control"
                  value={amount}
                  onChange={e => setAmount(e.target.value)}
                />
              </div>

              {selected && (
                <>
                  <button
                    className="btn btn-primary w-100 mb-2"
                    onClick={() =>
                      updateZone(selected.id, { name, amount })
                    }
                  >
                    Update Zone
                  </button>

                  <button
                    className="btn btn-danger w-100"
                    onClick={() => deleteZone(selected.id)}
                  >
                    Delete Zone
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
