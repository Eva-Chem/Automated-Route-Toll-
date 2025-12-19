CREATE TABLE IF NOT EXISTS toll_zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    charge_amount NUMERIC(10,2) NOT NULL,
    polygon JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO toll_zones (name, charge_amount, polygon)
VALUES (
  'CBD Toll Zone',
  200.00,
  '[
    {"lat": -1.2921, "lng": 36.8219},
    {"lat": -1.2925, "lng": 36.8225},
    {"lat": -1.2930, "lng": 36.8220},
    {"lat": -1.2921, "lng": 36.8219}
  ]'
);
