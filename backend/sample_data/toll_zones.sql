-- Clean SQL schema matching Python model with zone_id as primary key
-- Use this to initialize your PostgreSQL database

CREATE TABLE IF NOT EXISTS toll_zones (
    zone_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    polygon_coords JSONB NOT NULL,
    charge_amount NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nairobi CBD Toll Zone
INSERT INTO toll_zones (zone_id, name, polygon_coords, charge_amount)
VALUES (
    'cbd-zone-001',
    'Nairobi CBD',
    '[
        {"lat": -1.2820, "lng": 36.8140},
        {"lat": -1.2950, "lng": 36.8140},
        {"lat": -1.2950, "lng": 36.8300},
        {"lat": -1.2820, "lng": 36.8300}
    ]'::jsonb,
    200.00
);

-- Thika Road Toll Zone
INSERT INTO toll_zones (zone_id, name, polygon_coords, charge_amount)
VALUES (
    'thika-zone-001',
    'Thika Road',
    '[
        {"lat": -1.2000, "lng": 36.8900},
        {"lat": -1.2100, "lng": 36.9000},
        {"lat": -1.2200, "lng": 36.8800},
        {"lat": -1.2100, "lng": 36.8700}
    ]'::jsonb,
    150.00
);
