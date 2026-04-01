CREATE TABLE fact_vehicle_fueling (
    id SERIAL PRIMARY KEY,
    filling_date DATE NOT NULL,
    odometer_reading INTEGER NOT NULL,
    total_amount_paid NUMERIC(10,2),
    discount_amount NUMERIC(10,2) DEFAULT 0,
    -- volume_liters NUMERIC(10,3) NOT NULL,
    fuel_type VARCHAR(20),
    price_per_liter NUMERIC(10,3),
    
    -- Fidelidade e Recompensa
    kmv_points INTEGER DEFAULT 0,            -- Coluna L
    cashback_amount NUMERIC(10,2) DEFAULT 0, -- Coluna M
    
    gas_station VARCHAR(100),
    
    -- Comparativo de Preços
    comp_fuel_type VARCHAR(20),
    comp_price_per_liter NUMERIC(10,3),
    
    -- Telemetria do Painel
    board_consumption_kml NUMERIC(10,2),
    board_avg_speed_kmh NUMERIC(10,2),
    board_travel_time INTERVAL,
    board_trip_distance_km NUMERIC(10,2),
    board_remaining_range_km NUMERIC(10,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE fact_vehicle_fueling ALTER COLUMN volume_liters DROP NOT NULL;