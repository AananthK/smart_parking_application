-- Optional: start fresh
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS parking_spot CASCADE;
DROP TABLE IF EXISTS vehicle CASCADE;
DROP TABLE IF EXISTS lot CASCADE;

-- =========================================
-- LOT
-- =========================================
CREATE TABLE lot (
    lot_id SERIAL PRIMARY KEY,
    lot_name VARCHAR(100) NOT NULL,
    lot_location VARCHAR(255) NOT NULL,
    capacity INT NOT NULL CHECK (capacity >= 0),
	base_price NUMERIC(10,2) NOT NULL CHECK (base_price >= 0),
    violation_fee NUMERIC(10,2) NOT NULL DEFAULT 0.00 CHECK (violation_fee >= 0),
	-- violation for overstaying in parking, parking in the wrong spot, etc..
    lot_status VARCHAR(20) NOT NULL
        CHECK (lot_status IN ('OPEN', 'FULL', 'CLOSED'))
);

-- =========================================
-- VEHICLE
-- driver_id as license plates may change
-- =========================================
CREATE TABLE vehicle (
    driver_id SERIAL PRIMARY KEY,
    license_plate VARCHAR(11) NOT NULL,
    access_key_hash VARCHAR(255),
    owner_name VARCHAR(100),
	vehicle_type VARCHAR(4) NOT NULL DEFAULT 'TEST'
        CHECK (vehicle_type IN ('REAL', 'TEST')),
	-- 'TEST' vehicles are simulated to fill up parking spots (do not generate tickets)
	-- 'REAL' vehicles are registered by client, they do generate tickets
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
        CHECK (status IN ('ACTIVE', 'SUSPENDED'))
	-- 'ACTIVE' vehicles are currently registered to both their driver_id and licesne plate
	-- 'SUSPENDED' vehicles are no longer registered driver_id and license plate 
	-- 		(incase license plate changers or different driver for same car) 
);

-- Partial Index: An index that applies to some rows based on a condition
-- Only one ACTIVE vehicle per license plate
CREATE UNIQUE INDEX uq_active_license_plate
ON vehicle (license_plate)
WHERE status = 'ACTIVE';

-- =========================================
-- PARKING_SPOT
-- current_vehicle references the current vehicle parked there
-- =========================================
CREATE TABLE parking_spot (
    spot_id SERIAL PRIMARY KEY,
    lot_id INT NOT NULL,
    spot_number INT NOT NULL,
    spot_type VARCHAR(20) NOT NULL DEFAULT 'REGULAR'
        CHECK (spot_type IN ('REGULAR', 'RESERVED')),
    status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE'
        CHECK (status IN ('AVAILABLE', 'OCCUPIED', 'OUT_OF_SERVICE')),
    current_vehicle INT NULL,

    CONSTRAINT fk_parking_spot_lot
        FOREIGN KEY (lot_id)
        REFERENCES lot(lot_id)
        ON DELETE CASCADE, -- if lot is deleted, delete parking spot

    CONSTRAINT fk_parking_spot_vehicle
        FOREIGN KEY (current_vehicle)
        REFERENCES vehicle(driver_id)
        ON DELETE SET NULL, -- if vehicle is deleted, set current vehicle to null

    CONSTRAINT uq_lot_spot_number
        UNIQUE (lot_id, spot_number)
);

-- =========================================
-- TICKETS
-- Tied to vehicle and optionally to a specific parking spot
-- =========================================
CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    driver_id INT NOT NULL,
    spot_id INT,
    amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    issued_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    duration INT CHECK (duration >= 0),
    type VARCHAR(20) NOT NULL
        CHECK (type IN ('PARKING', 'OVERCHARGE', 'VIOLATION')),
    status VARCHAR(20) NOT NULL DEFAULT 'UNPAID'
        CHECK (status IN ('UNPAID', 'PAID', 'CANCELLED')),

    CONSTRAINT fk_tickets_driver
        FOREIGN KEY (driver_id)
        REFERENCES vehicle(driver_id)
        ON DELETE RESTRICT, -- keep tickets with driver of vehicle for history, prevent vehicle deletion

    CONSTRAINT fk_tickets_spot
        FOREIGN KEY (spot_id)
        REFERENCES parking_spot(spot_id)
        ON DELETE SET NULL -- if parking spot is deleted, set spot_id to NULL
);