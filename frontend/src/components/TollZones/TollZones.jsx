import { useAuth } from "../../auth/auth.context";
import { mockZones } from "./TollZones.mock";
import { useState } from "react";
import DashboardLayout from "../../layout/DashboardLayout";

export default function TollZones() {
  const { user } = useAuth();
  const [search, setSearch] = useState("");
  const [zones, setZones] = useState(mockZones);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({ name: "", charge_amount: "", coordinates: "" });

  const filteredZones = zones.filter(z =>
    z.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleCreate = () => {
    if (formData.name && formData.charge_amount) {
      const newZone = {
        id: Math.max(...zones.map(z => z.id)) + 1,
        name: formData.name,
        charge_amount: parseFloat(formData.charge_amount),
        coordinates: formData.coordinates ? JSON.parse(formData.coordinates) : [],
      };
      setZones([...zones, newZone]);
      setFormData({ name: "", charge_amount: "", coordinates: "" });
      setShowCreateForm(false);
    }
  };

  const handleEdit = (zone) => {
    setEditingId(zone.id);
    setFormData({
      name: zone.name,
      charge_amount: zone.charge_amount,
      coordinates: JSON.stringify(zone.coordinates),
    });
  };

  const handleUpdate = () => {
    setZones(zones.map(z =>
      z.id === editingId
        ? {
            ...z,
            name: formData.name,
            charge_amount: parseFloat(formData.charge_amount),
            coordinates: formData.coordinates ? JSON.parse(formData.coordinates) : z.coordinates,
          }
        : z
    ));
    setEditingId(null);
    setFormData({ name: "", charge_amount: "", coordinates: "" });
  };

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this toll zone?")) {
      setZones(zones.filter(z => z.id !== id));
    }
  };

  const handleCancel = () => {
    setShowCreateForm(false);
    setEditingId(null);
    setFormData({ name: "", charge_amount: "", coordinates: "" });
  };

  return (
    <DashboardLayout>
      <div className="d-flex justify-content-between mb-3">
        <input
          className="form-control w-50"
          placeholder="Search by Toll Name"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />

        {user.role === "operator" && (
          <button className="btn btn-primary" onClick={() => setShowCreateForm(true)}>
            Create Toll
          </button>
        )}
      </div>

      {(showCreateForm || editingId) && (
        <div className="card mb-3">
          <div className="card-body">
            <h5>{editingId ? "Edit Toll Zone" : "Create New Toll Zone"}</h5>
            <div className="row g-3">
              <div className="col-md-4">
                <input
                  className="form-control"
                  placeholder="Zone Name"
                  value={formData.name}
                  onChange={e => setFormData({ ...formData, name: e.target.value })}
                />
              </div>
              <div className="col-md-4">
                <input
                  className="form-control"
                  placeholder="Charge Amount"
                  type="number"
                  value={formData.charge_amount}
                  onChange={e => setFormData({ ...formData, charge_amount: e.target.value })}
                />
              </div>
              <div className="col-md-4">
                <input
                  className="form-control"
                  placeholder='Coordinates JSON (e.g., [{"lat": -1.2, "lng": 36.8}])'
                  value={formData.coordinates}
                  onChange={e => setFormData({ ...formData, coordinates: e.target.value })}
                />
              </div>
            </div>
            <div className="mt-3">
              <button className="btn btn-success me-2" onClick={editingId ? handleUpdate : handleCreate}>
                {editingId ? "Update" : "Create"}
              </button>
              <button className="btn btn-secondary" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="row g-3">
        {filteredZones.map(zone => (
          <div key={zone.id} className="col-md-4">
            <div className="card shadow-sm h-100">
              <div className="card-body">
                <h5>{zone.name}</h5>
                <p>Ksh {zone.charge_amount}</p>

                {zone.coordinates.map((c, i) => (
                  <div key={i} className="small text-muted">
                    lat: {c.lat} lng: {c.lng}
                  </div>
                ))}

                {user.role === "operator" && (
                  <div className="mt-2">
                    <button className="btn btn-sm btn-outline-primary me-2" onClick={() => handleEdit(zone)}>
                      Edit
                    </button>
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(zone.id)}>
                      Delete
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
}