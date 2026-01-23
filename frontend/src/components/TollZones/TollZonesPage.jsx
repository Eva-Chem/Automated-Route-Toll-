import { useState, useEffect } from "react";
import DashboardLayout from "../../layout/DashboardLayout";
import MapCanvas from "../../map/MapCanvas";
import { useZoneStore } from "../../store/zone.store";
import { useAuth } from "../../auth/use-auth";
import { ROLES } from "../../constants/roles";
import { geoJSONToLatLngArray } from "../../utils/geo";

const modalStyles = {
  backdrop: {
    position: "fixed",
    inset: 0,
    backgroundColor: "rgba(0, 0, 0, 0.45)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1050,
    padding: "1rem",
  },
  dialog: {
    backgroundColor: "#fff",
    borderRadius: "8px",
    maxWidth: "420px",
    width: "100%",
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
  },
};

/**
 * TollZonesPage
 * 
 * RBAC Rules (enforced):
 * - Admin: view-only (read zones, see on map)
 * - toll_operator: full CRUD (create, read, update zones; DELETE disabled pending backend)
 * 
 * Field mappings (backend contract):
 * - zone_id: zone identifier (UUID from backend)
 * - zone_name: zone display name
 * - charge_amount: toll charge in currency
 * - polygon_coords: array of [lat, lng] pairs
 */
export default function TollZones() {
  const { user } = useAuth();
  const { zones, addZone, updateZone, deleteZone, fetchZones } = useZoneStore();
  const [showForm, setShowForm] = useState(false);
  const [editingZone, setEditingZone] = useState(null);
  const [zoneToDelete, setZoneToDelete] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [formData, setFormData] = useState({
    zone_name: "",
    charge_amount: "",
    polygon_coords: [
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
      zone_name: "New Toll Zone",
      charge_amount: 0,
      polygon_coords: coordinates,
    });
  };

  const handleUpdateZone = (zoneId, coordinates) => {
    updateZone(zoneId, { polygon_coords: coordinates });
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCoordinateChange = (index, field, value) => {
    const newCoords = [...formData.polygon_coords];
    newCoords[index] = { ...newCoords[index], [field]: value };
    setFormData((prev) => ({
      ...prev,
      polygon_coords: newCoords,
    }));
  };

  const addCoordinatePoint = () => {
    setFormData((prev) => ({
      ...prev,
      polygon_coords: [...prev.polygon_coords, { lat: "", lng: "" }],
    }));
  };

  const removeCoordinatePoint = (index) => {
    if (formData.polygon_coords.length > 3) {
      const newCoords = formData.polygon_coords.filter((_, i) => i !== index);
      setFormData((prev) => ({
        ...prev,
        polygon_coords: newCoords,
      }));
    }
  };

  const handleSubmitForm = async (e) => {
    e.preventDefault();
    
    // Validate and convert coordinates
    const polygon_coords = formData.polygon_coords
      .filter((coord) => coord.lat && coord.lng)
      .map((coord) => [parseFloat(coord.lat), parseFloat(coord.lng)]);

    if (polygon_coords.length < 3) {
      alert("Please provide at least 3 coordinate points to form a polygon.");
      return;
    }

    const zoneData = {
      zone_name: formData.zone_name,
      charge_amount: parseFloat(formData.charge_amount),
      polygon_coords: polygon_coords,
    };

    if (editingZone) {
      await updateZone(editingZone.zone_id, zoneData);
    } else {
      await addZone(zoneData);
    }

    // Reset form
    setFormData({
      zone_name: "",
      charge_amount: "",
      polygon_coords: [
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
    const latlngs = geoJSONToLatLngArray(zone.polygon_coords);
    if (!latlngs.length) {
      console.warn("Zone has invalid polygon_coords; skipping edit:", zone.zone_name);
      return;
    }
    setEditingZone(zone);
    setFormData({
      zone_name: zone.zone_name,
      charge_amount: zone.charge_amount?.toString() || "",
      polygon_coords: latlngs.map(([lat, lng]) => ({
        lat: lat.toString(),
        lng: lng.toString(),
      })),
    });
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setFormData({
      zone_name: "",
      charge_amount: "",
      polygon_coords: [
        { lat: "", lng: "" },
        { lat: "", lng: "" },
        { lat: "", lng: "" },
        { lat: "", lng: "" },
      ],
    });
    setShowForm(false);
    setEditingZone(null);
  };

  const handleRequestDelete = (zone) => {
    setZoneToDelete(zone);
  };

  const handleConfirmDelete = async () => {
    if (!zoneToDelete) return;
    setIsDeleting(true);
    try {
      await deleteZone(zoneToDelete.zone_id);
    } catch (error) {
      console.error("Failed to delete zone", error);
      alert("Failed to delete zone. Please try again.");
    } finally {
      setIsDeleting(false);
      setZoneToDelete(null);
    }
  };

  const handleCancelDelete = () => {
    if (isDeleting) return;
    setZoneToDelete(null);
  };

  const isOperator = user?.role === ROLES.TOLL_OPERATOR;

  return (
    <DashboardLayout>
      <h3 className="mb-4">Toll Zones</h3>

      {/* Show form button only for toll operators */}
      {isOperator && (
        <div className="mb-3">
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? "Cancel" : "Add Zone Manually"}
          </button>
        </div>
      )}

      {/* Form visible only for toll operators */}
      {showForm && isOperator && (
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
                    name="zone_name"
                    value={formData.zone_name}
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
                {formData.polygon_coords.map((coord, index) => (
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
                      {formData.polygon_coords.length > 3 && (
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

      {/* Map: show operators with edit mode, admins with view-only */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <MapCanvas
            zones={zones}
            mode={isOperator ? "operator" : "admin"}
            onCreateZone={isOperator ? handleCreateZone : undefined}
            onUpdateZone={isOperator ? handleUpdateZone : undefined}
          />
        </div>
      </div>

      {/* Zone list: show edit/delete for operators, view-only for admin */}
      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Zone List</h5>
        </div>
        <table className="table table-bordered mb-0">
          <thead>
            <tr>
              <th>Name</th>
              <th>Charge (Ksh)</th>
              {isOperator && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {zones.length === 0 ? (
              <tr>
                <td colSpan={isOperator ? 3 : 2} className="text-center text-muted">
                  No zones available
                </td>
              </tr>
            ) : (
              zones.map((zone) => (
                <tr key={zone.zone_id}>
                  <td>{zone.zone_name}</td>
                  <td>{zone.charge_amount}</td>
                  {isOperator && (
                    <td>
                      <button
                        className="btn btn-sm btn-warning"
                        onClick={() => handleEditZone(zone)}
                      >
                        Edit
                      </button>
                      <button
                        className="btn btn-sm btn-danger ms-2"
                        onClick={() => handleRequestDelete(zone)}
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

      {zoneToDelete && (
        <div style={modalStyles.backdrop} role="dialog" aria-modal="true">
          <div style={modalStyles.dialog} className="p-4">
            <h5 className="mb-3">Confirm Delete</h5>
            <p className="mb-4">
              Are you sure you want to delete "{zoneToDelete.zone_name}"? This action cannot be undone.
            </p>
            <div className="d-flex justify-content-end gap-2">
              <button
                className="btn btn-secondary"
                onClick={handleCancelDelete}
                disabled={isDeleting}
              >
                Cancel
              </button>
              <button
                className="btn btn-danger"
                onClick={handleConfirmDelete}
                disabled={isDeleting}
              >
                {isDeleting ? "Deleting..." : "Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
