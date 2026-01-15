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
  const [formData, setFormData] = useState({ 
    name: "", 
    charge_amount: "", 
    lat1: "", lng1: "",
    lat2: "", lng2: "",
    lat3: "", lng3: "",
    lat4: "", lng4: ""
  });

  const filteredZones = zones.filter(z =>
    z.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleCreate = () => {
    if (formData.name && formData.charge_amount) {
      const coordinates = [
        parseFloat(formData.lat1), parseFloat(formData.lng1),
        parseFloat(formData.lat2), parseFloat(formData.lng2),
        parseFloat(formData.lat3), parseFloat(formData.lng3),
        parseFloat(formData.lat4), parseFloat(formData.lng4),
      ].filter(coord => !isNaN(coord));
      
      const newZone = {
        id: Math.max(...zones.map(z => z.id)) + 1,
        name: formData.name,
        charge_amount: parseFloat(formData.charge_amount),
        coordinates: coordinates,
      };
      setZones([...zones, newZone]);
      setFormData({ 
        name: "", 
        charge_amount: "", 
        lat1: "", lng1: "",
        lat2: "", lng2: "",
        lat3: "", lng3: "",
        lat4: "", lng4: ""
      });
      setShowCreateForm(false);
    }
  };

  const handleEdit = (zone) => {
    setEditingId(zone.id);
    setFormData({
      name: zone.name,
      charge_amount: zone.charge_amount,
      lat1: zone.coordinates[0] || "",
      lng1: zone.coordinates[1] || "",
      lat2: zone.coordinates[2] || "",
      lng2: zone.coordinates[3] || "",
      lat3: zone.coordinates[4] || "",
      lng3: zone.coordinates[5] || "",
      lat4: zone.coordinates[6] || "",
      lng4: zone.coordinates[7] || "",
    });
  };

  const handleUpdate = () => {
    const coordinates = [
      parseFloat(formData.lat1), parseFloat(formData.lng1),
      parseFloat(formData.lat2), parseFloat(formData.lng2),
      parseFloat(formData.lat3), parseFloat(formData.lng3),
      parseFloat(formData.lat4), parseFloat(formData.lng4),
    ].filter(coord => !isNaN(coord));
    
    setZones(zones.map(z =>
      z.id === editingId
        ? {
            ...z,
            name: formData.name,
            charge_amount: parseFloat(formData.charge_amount),
            coordinates: coordinates,
          }
        : z
    ));
    setEditingId(null);
    setFormData({ 
      name: "", 
      charge_amount: "", 
      lat1: "", lng1: "",
      lat2: "", lng2: "",
      lat3: "", lng3: "",
      lat4: "", lng4: ""
    });
  };

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this toll zone?")) {
      setZones(zones.filter(z => z.id !== id));
    }
  };

  const handleCancel = () => {
    setShowCreateForm(false);
    setEditingId(null);
    setFormData({ 
      name: "", 
      charge_amount: "", 
      lat1: "", lng1: "",
      lat2: "", lng2: "",
      lat3: "", lng3: "",
      lat4: "", lng4: ""
    });
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
            </div>
            <div className="mt-3">
              <h6>Coordinates (4 points for the toll zone polygon)</h6>
              
              <div className="mb-3">
                <h6 className="text-muted">Point 1</h6>
                <div className="row g-2">
                  <div className="col-md-6">
                    <label className="form-label">Latitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., -1.2864"
                      type="number"
                      step="any"
                      value={formData.lat1}
                      onChange={e => setFormData({ ...formData, lat1: e.target.value })}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Longitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., 36.8172"
                      type="number"
                      step="any"
                      value={formData.lng1}
                      onChange={e => setFormData({ ...formData, lng1: e.target.value })}
                    />
                  </div>
                </div>
              </div>
              
              <div className="mb-3">
                <h6 className="text-muted">Point 2</h6>
                <div className="row g-2">
                  <div className="col-md-6">
                    <label className="form-label">Latitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., -1.2864"
                      type="number"
                      step="any"
                      value={formData.lat2}
                      onChange={e => setFormData({ ...formData, lat2: e.target.value })}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Longitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., 36.8172"
                      type="number"
                      step="any"
                      value={formData.lng2}
                      onChange={e => setFormData({ ...formData, lng2: e.target.value })}
                    />
                  </div>
                </div>
              </div>
              
              <div className="mb-3">
                <h6 className="text-muted">Point 3</h6>
                <div className="row g-2">
                  <div className="col-md-6">
                    <label className="form-label">Latitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., -1.2864"
                      type="number"
                      step="any"
                      value={formData.lat3}
                      onChange={e => setFormData({ ...formData, lat3: e.target.value })}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Longitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., 36.8172"
                      type="number"
                      step="any"
                      value={formData.lng3}
                      onChange={e => setFormData({ ...formData, lng3: e.target.value })}
                    />
                  </div>
                </div>
              </div>
              
              <div className="mb-3">
                <h6 className="text-muted">Point 4</h6>
                <div className="row g-2">
                  <div className="col-md-6">
                    <label className="form-label">Latitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., -1.2864"
                      type="number"
                      step="any"
                      value={formData.lat4}
                      onChange={e => setFormData({ ...formData, lat4: e.target.value })}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Longitude</label>
                    <input
                      className="form-control"
                      placeholder="e.g., 36.8172"
                      type="number"
                      step="any"
                      value={formData.lng4}
                      onChange={e => setFormData({ ...formData, lng4: e.target.value })}
                    />
                  </div>
                </div>
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

                {Array.from({ length: zone.coordinates.length / 2 }, (_, i) => (
                  <div key={i} className="small text-muted">
                    Point {i+1}: lat {zone.coordinates[i*2]}, lng {zone.coordinates[i*2+1]}
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