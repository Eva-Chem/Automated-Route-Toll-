# Frontend Architecture Quick Reference

## 🧠 The Golden Rule
1. **Pages** get data from store
2. **Components** receive data via props  
3. **Map** renders data only
4. **Routes** handle paths & roles

---

## 📍 Where Zones Live

```javascript
// ✅ CORRECT: Fetch in page, pass to component
function AdminDashboard() {
  const { zones, fetchZones } = useZoneStore();
  
  useEffect(() => {
    fetchZones(); // Load from store/API
  }, [fetchZones]);
  
  return <MapCanvas zones={zones} mode="admin" />;
}

// ✅ CORRECT: Component receives zones as prop
function MapCanvas({ zones = [] }) {
  return zones.map(z => <Polygon positions={z.coordinates} />);
}
```

```javascript
// ❌ WRONG: Don't read store in component
function MapCanvas() {
  const { zones } = useZoneStore(); // ❌ NO!
  return ...;
}

// ❌ WRONG: Don't keep local copies
function AdminDashboard() {
  const [localZones, setLocalZones] = useState([]); // ❌ NO!
  return ...;
}
```

---

## 🔄 Coordinate Format

```javascript
// ✅ CORRECT: Array of tuples [[lat, lng], ...]
const zone = {
  id: 1,
  name: "CBD Toll Zone",
  coordinates: [
    [-1.2833, 36.8167],
    [-1.2833, 36.8333],
    [-1.3, 36.8333],
    [-1.3, 36.8167],
  ],
};

// React-Leaflet Polygon accepts directly:
<Polygon positions={zone.coordinates} />
```

```javascript
// ❌ WRONG: Flat arrays
coordinates: [-1.2833, 36.8167, -1.2833, 36.8333, ...]
```

---

## 📦 Store Operations

```javascript
import { useZoneStore } from "../store/zone.store";

function MyComponent() {
  const { 
    zones,          // Current zones array
    loading,        // Loading state
    error,          // Error messages
    fetchZones,     // Get zones from API
    addZone,        // Create new zone
    updateZone,     // Modify zone
    deleteZone,     // Remove zone
  } = useZoneStore();

  // Fetch on mount
  useEffect(() => {
    fetchZones();
  }, [fetchZones]);

  // Create
  const handleCreate = async (coords) => {
    await addZone({
      name: "New Zone",
      charge_amount: 50,
      coordinates: coords,
    });
  };

  // Update
  const handleUpdate = async (id, newCoords) => {
    await updateZone(id, { coordinates: newCoords });
  };

  // Delete
  const handleDelete = async (id) => {
    await deleteZone(id);
  };
}
```

---

## 🗺️ MapCanvas API

```javascript
<MapCanvas
  zones={zones}              // Array of zone objects
  mode="admin"               // "admin" or "operator"
  onCreateZone={handleCreate} // (coordinates) => void
  onUpdateZone={handleUpdate} // (id, coordinates) => void
/>
```

**MapCanvas expects:**
- `zones`: Array of `{ id, name, charge_amount, coordinates: [[lat, lng], ...] }`
- `mode`: "admin" (read-only with markers) or "operator" (editable with Leaflet Draw)
- Callbacks receive coordinates in tuple format

---

## 🔌 API Endpoints

All defined in `TollZones.api.js`:

```javascript
// GET zones
const zones = await getZones();

// Create zone
const newZone = await createZone({
  name: "New Zone",
  charge_amount: 50,
  coordinates: [[lat, lng], ...],
});

// Update zone
const updated = await updateZone(id, {
  name: "Updated Zone",
  coordinates: [[lat, lng], ...],
});

// Delete zone
await deleteZone(id);
```

**Paths:**
- `GET /api/toll-zones`
- `POST /api/toll-zones`
- `PUT /api/toll-zones/{id}`
- `DELETE /api/toll-zones/{id}`

---

## 🎯 Common Patterns

### Pattern 1: Read-Only Admin View
```javascript
function AdminDashboard() {
  const { zones, fetchZones } = useZoneStore();
  
  useEffect(() => {
    fetchZones();
  }, [fetchZones]);
  
  return <MapCanvas zones={zones} mode="admin" />;
}
```

### Pattern 2: Editable Operator View
```javascript
function OperatorZones() {
  const { zones, addZone, updateZone, deleteZone, fetchZones } = useZoneStore();
  
  useEffect(() => {
    fetchZones();
  }, [fetchZones]);
  
  return (
    <>
      <MapCanvas
        zones={zones}
        mode="operator"
        onCreateZone={(coords) => addZone({
          name: "New Zone",
          charge_amount: 0,
          coordinates: coords,
        })}
        onUpdateZone={(id, coords) => updateZone(id, { coordinates: coords })}
      />
      <ZonesList zones={zones} onDelete={deleteZone} />
    </>
  );
}
```

### Pattern 3: New Page with Zones
```javascript
function NewPage() {
  const { zones, fetchZones } = useZoneStore();
  
  // Fetch on mount
  useEffect(() => {
    fetchZones();
  }, [fetchZones]);
  
  // zones is ready to use
  return <div>{zones.map(z => <ZoneCard key={z.id} zone={z} />)}</div>;
}
```

---

## ⚠️ Common Mistakes

| ❌ Mistake | ✅ Fix |
|-----------|--------|
| `const [zones, setZones] = useState([])` in component | Use `useZoneStore().zones` instead |
| Import `mockZones` in components | Fetch via `fetchZones()` |
| Pass `zones` as props from Router | Let pages fetch zones |
| Read store in MapCanvas | Accept zones via props |
| Flat coordinate arrays | Use tuples `[[lat, lng], ...]` |
| Multiple sources of zone data | One store, always |

---

## 🚀 Backend Integration

When backend is ready:

1. **Enable real API:**
   ```env
   VITE_USE_MOCK_API=false
   VITE_API_URL=http://localhost:5000
   ```

2. **Ensure endpoints exist:**
   - `GET /api/toll-zones`
   - `POST /api/toll-zones`
   - `PUT /api/toll-zones/{id}`
   - `DELETE /api/toll-zones/{id}`

3. **Backend response format:**
   ```json
   {
     "id": 1,
     "name": "Zone Name",
     "charge_amount": 50,
     "coordinates": [
       {"lat": -1.28, "lng": 36.81},
       {"lat": -1.29, "lng": 36.82}
     ]
   }
   ```

4. **Store auto-transforms coordinates** from `{"lat": x, "lng": y}` to `[x, y]`

5. **No UI changes needed** — everything works!

---

## 🧪 Testing Checklist

- [ ] Admin dashboard loads zones on mount
- [ ] Operator zones page loads zones on mount
- [ ] Operator can draw polygons on map
- [ ] Created zones appear in list immediately
- [ ] Zones sync across admin and operator in real-time
- [ ] No console errors
- [ ] MapCanvas renders polygons correctly
- [ ] Coordinates are tuples `[lat, lng]`
- [ ] No duplicate zones in UI
- [ ] Delete works from list
- [ ] Store has only one source of zones

---

## 📚 File Reference

| File | Purpose | Touches? |
|------|---------|----------|
| `store/zone.store.js` | Zone state management | ✅ Central hub |
| `map/MapCanvas.jsx` | Map rendering | ✅ Props only |
| `components/TollZones/TollZones.jsx` | Zone UI (admin/operator) | ✅ Fetch & pass |
| `admin/AdminDashboard.jsx` | Admin overview | ✅ Fetch zones |
| `components/TollZones/TollZones.api.js` | API gateway | ✅ Endpoints |
| `mock/mockApi.js` | Mock endpoints | ✅ Testing |
| `mock/zones.mock.js` | Mock data | ✅ Initialize |
| `app/Router.jsx` | Routes | ✅ Paths only |

---

## ❓ FAQ

**Q: Where should I fetch zones?**  
A: In page components (AdminDashboard, TollZones) using `useEffect` + `fetchZones()`

**Q: Can MapCanvas read from store?**  
A: No. It should only receive `zones` via props and delegate mutations via callbacks.

**Q: How do zones sync between pages?**  
A: Store is centralized. When one page modifies zones, all pages using the store see updates immediately.

**Q: What format are coordinates?**  
A: Array of tuples: `[[lat, lng], [lat, lng], ...]`

**Q: Do I need to transform coordinates?**  
A: No. Store handles backend format (`[{"lat": x, "lng": y}]`) → frontend format (`[[x, y]]`)

**Q: How do I add a new page with zones?**  
A: Use `useZoneStore()` to get zones, call `fetchZones()` in `useEffect`, pass zones to components as props.

---

✅ **This architecture is production-ready, backend-compatible, and easy to maintain!**
