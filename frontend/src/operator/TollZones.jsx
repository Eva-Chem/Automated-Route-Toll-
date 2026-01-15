import { useAuth } from "../auth/auth.context";
import { mockZones } from "../mock/zones.mock";
import { useState } from "react";
import DashboardLayout from "../layout/DashboardLayout";
import MapCanvas from "../map/MapCanvas";

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
  const [selectedZoneId, setSelectedZoneId] = useState(null);
  const [isDrawingMode, setIsDrawingMode] = useState(false);
  const [currentDrawingPoints, setCurrentDrawingPoints] = useState([]);

  console.log('Operator TollZones rendering, zones:', zones, 'zones length:', zones?.length);

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
      setCurrentDrawingPoints([]);
      setIsDrawingMode(false);
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

  const handleZoneSelect = (zone) => {
    setSelectedZoneId(zone.id);
  };

  const handleZoneCreate = (coordinates) => {
    const newZone = {
      id: Math.max(...zones.map(z => z.id)) + 1,
      name: `New Zone ${zones.length + 1}`,
      charge_amount: 50,
      coordinates: coordinates,
    };
    setZones([...zones, newZone]);
  };

  const handleZoneUpdate = (id, updates) => {
    setZones(zones.map(z =>
      z.id === id ? { ...z, ...updates } : z
    ));
  };

  const handleMapPointSelect = (lat, lng, clear = false) => {
    if (clear) {
      setCurrentDrawingPoints([]);
      return;
    }

    if (lat !== null && lng !== null) {
      const newPoints = [...currentDrawingPoints, [lat, lng]];
      setCurrentDrawingPoints(newPoints);

      // Auto-populate form fields when we have points
      if (newPoints.length >= 1) {
        setFormData(prev => ({
          ...prev,
          lat1: newPoints[0] ? newPoints[0][0].toFixed(6) : prev.lat1,
          lng1: newPoints[0] ? newPoints[0][1].toFixed(6) : prev.lng1,
        }));
      }
      if (newPoints.length >= 2) {
        setFormData(prev => ({
          ...prev,
          lat2: newPoints[1][0].toFixed(6),
          lng2: newPoints[1][1].toFixed(6),
        }));
      }
      if (newPoints.length >= 3) {
        setFormData(prev => ({
          ...prev,
          lat3: newPoints[2][0].toFixed(6),
          lng3: newPoints[2][1].toFixed(6),
        }));
      }
      if (newPoints.length >= 4) {
        setFormData(prev => ({
          ...prev,
          lat4: newPoints[3][0].toFixed(6),
          lng4: newPoints[3][1].toFixed(6),
        }));
        setIsDrawingMode(false); // Auto-disable drawing when complete
      }
    }
  };

  const handleCancel = () => {
    setShowCreateForm(false);
    setEditingId(null);
    setSelectedZoneId(null);
    setIsDrawingMode(false);
    setCurrentDrawingPoints([]);
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
          <div className="d-flex gap-2">
            <button 
              className={`btn ${isDrawingMode ? 'btn-warning' : 'btn-success'}`}
              onClick={() => {
                setIsDrawingMode(!isDrawingMode);
                if (!isDrawingMode) {
                  setCurrentDrawingPoints([]);
                  setShowCreateForm(true);
                }
              }}
            >
              {isDrawingMode ? '🗺️ Exit Map Drawing' : '🖱️ Draw on Map'}
            </button>
            <button className="btn btn-primary" onClick={() => setShowCreateForm(true)}>
              Create Toll
            </button>
          </div>
        )}
      </div>

      {(showCreateForm || editingId) && (
        <div className="card mb-3">
          <div className="card-body">
            <h5>{editingId ? "Edit Toll Zone" : "Create New Toll Zone"}</h5>
            
            {isDrawingMode && (
              <div className="alert alert-info mb-3">
                <strong>Map Drawing Mode Active!</strong> Click on the map below to select polygon points. 
                Points selected: {currentDrawingPoints.length}/4
                {currentDrawingPoints.length === 4 && (
                  <span className="text-success"> ✅ Ready to create zone!</span>
                )}
              </div>
            )}
            
            <div className="row g-3">
              <div className="col-md-6">
                <label className="form-label">Zone Name</label>
                <input
                  className="form-control"
                  placeholder="Enter zone name"
                  value={formData.name}
                  onChange={e => setFormData({ ...formData, name: e.target.value })}
                />
              </div>
              <div className="col-md-6">
                <label className="form-label">Charge Amount</label>
                <input
                  className="form-control"
                  placeholder="Enter charge amount"
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

      <div className="card mb-4">
        <div className="card-body">
          <h5>Toll Zones Map</h5>
          <MapCanvas
            zones={zones}
            selectedId={selectedZoneId}
            onSelect={handleZoneSelect}
            onCreate={handleZoneCreate}
            onUpdate={handleZoneUpdate}
            onPointSelect={handleMapPointSelect}
            isDrawingMode={isDrawingMode}
            currentPoints={currentDrawingPoints}
            mapId="operator-toll-zones"
          />
        </div>
      </div>

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
