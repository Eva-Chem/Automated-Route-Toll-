import { useState, useEffect } from "react";
import DashboardLayout from "../../layout/DashboardLayout";
import MapCanvas from "../../map/MapCanvas";
import { useZoneStore } from "../../store/zone.store";
import { useAuth } from "../../auth/auth.context";

export default function TollZones() {
  const { user } = useAuth();
  const { zones, addZone, updateZone, deleteZone, fetchZones } = useZoneStore();
  const [selectedId, setSelectedId] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingZone, setEditingZone] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    charge_amount: "",
    coordinates: [
      { lat: "", lng: "" },
      { lat: "", lng: "" },
      { lat: "", lng: "" },
      { lat: "", lng: "" },
    ],
  });

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

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCoordinateChange = (index, field, value) => {
    const newCoords = [...formData.coordinates];
    newCoords[index] = { ...newCoords[index], [field]: value };
    setFormData((prev) => ({
      ...prev,
      coordinates: newCoords,
    }));
  };

  const addCoordinatePoint = () => {
    setFormData((prev) => ({
      ...prev,
      coordinates: [...prev.coordinates, { lat: "", lng: "" }],
    }));
  };

  const removeCoordinatePoint = (index) => {
    if (formData.coordinates.length > 3) {
      const newCoords = formData.coordinates.filter((_, i) => i !== index);
      setFormData((prev) => ({
        ...prev,
        coordinates: newCoords,
      }));
    }
  };

  const handleSubmitForm = async (e) => {
    e.preventDefault();
    
    // Validate and convert coordinates
    const coordinates = formData.coordinates
      .filter((coord) => coord.lat && coord.lng)
      .map((coord) => [parseFloat(coord.lat), parseFloat(coord.lng)]);

    if (coordinates.length < 3) {
      alert("Please provide at least 3 coordinate points to form a polygon.");
      return;
    }

    const zoneData = {
      name: formData.name,
      charge_amount: parseFloat(formData.charge_amount),
      coordinates,
    };

    if (editingZone) {
      await updateZone(editingZone.id, zoneData);
    } else {
      await addZone({ ...zoneData, id: Date.now() });
    }

    // Reset form
    setFormData({
      name: "",
      charge_amount: "",
      coordinates: [
        { lat: "", lng: "" },
        { lat: "", lng: "" },
        { lat: "", lng: "" },
        { lat: "", lng: "" },
      ],
    });
    setShowForm(false);
    setEditingZone(null);
  };

  const handleEditZone = (zone) => {
    setEditingZone(zone);
    setFormData({
      name: zone.name,
      charge_amount: zone.charge_amount.toString(),
      coordinates: zone.coordinates.map(([lat, lng]) => ({
        lat: lat.toString(),
        lng: lng.toString(),
      })),
    });
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setFormData({
      name: "",
      charge_amount: "",
      coordinates: [
        { lat: "", lng: "" },
        { lat: "", lng: "" },
        { lat: "", lng: "" },
        { lat: "", lng: "" },
      ],
    });
    setShowForm(false);
    setEditingZone(null);
  };

  return (
    <DashboardLayout>
      <h3 className="mb-4">Toll Zones</h3>

      {user?.role === "operator" && (
        <div className="mb-3">
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? "Cancel" : "Add Zone Manually"}
          </button>
        </div>
      )}

      {showForm && user?.role === "operator" && (
        <div className="card shadow-sm mb-4">
          <div className="card-header">
            <h5 className="mb-0">
              {editingZone ? "Edit Toll Zone" : "Create New Toll Zone"}
            </h5>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmitForm}>
              <div className="row mb-3">
                <div className="col-md-6">
                  <label className="form-label">Zone Name *</label>
                  <input
                    type="text"
                    className="form-control"
                    name="name"
                    value={formData.name}
                    onChange={handleFormChange}
                    required
                    placeholder="e.g., CBD Toll Zone"
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Charge Amount (Ksh) *</label>
                  <input
                    type="number"
                    className="form-control"
                    name="charge_amount"
                    value={formData.charge_amount}
                    onChange={handleFormChange}
                    required
                    min="0"
                    step="0.01"
                    placeholder="e.g., 50"
                  />
                </div>
              </div>

              <div className="mb-3">
                <label className="form-label">Coordinates (Polygon Points) *</label>
                <p className="text-muted small">
                  Enter at least 3 points to form a polygon. Format: Latitude, Longitude
                </p>
                {formData.coordinates.map((coord, index) => (
                  <div key={index} className="row mb-2">
                    <div className="col-md-5">
                      <input
                        type="number"
                        className="form-control"
                        placeholder="Latitude (e.g., -1.2833)"
                        value={coord.lat}
                        onChange={(e) =>
                          handleCoordinateChange(index, "lat", e.target.value)
                        }
                        step="any"
                      />
                    </div>
                    <div className="col-md-5">
                      <input
                        type="number"
                        className="form-control"
                        placeholder="Longitude (e.g., 36.8167)"
                        value={coord.lng}
                        onChange={(e) =>
                          handleCoordinateChange(index, "lng", e.target.value)
                        }
                        step="any"
                      />
                    </div>
                    <div className="col-md-2">
                      {formData.coordinates.length > 3 && (
                        <button
                          type="button"
                          className="btn btn-danger btn-sm"
                          onClick={() => removeCoordinatePoint(index)}
                        >
                          Remove
                        </button>
                      )}
                    </div>
                  </div>
                ))}
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={addCoordinatePoint}
                >
                  + Add Point
                </button>
              </div>

              <div className="d-flex gap-2">
                <button type="submit" className="btn btn-success">
                  {editingZone ? "Update Zone" : "Create Zone"}
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleCancelForm}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

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
                        className="btn btn-sm btn-warning me-2"
                        onClick={() => handleEditZone(zone)}
                      >
                        Edit
                      </button>
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
