DO $$
BEGIN

-- Populating Lot 1 (City Centre)
FOR i in 1..50 LOOP

	-- For Reserved Parking
	IF i < 11 THEN
		INSERT INTO parking_spot (lot_id, spot_number, spot_type, status)
		VALUES (1, i, 'RESERVED', 'AVAILABLE');
	-- For Regular Parking
	ELSE 
		INSERT INTO parking_spot (lot_id, spot_number, spot_type, status)
		VALUES (1, i, 'REGULAR', 'AVAILABLE');
	END IF;
	
END LOOP;

-- Populating Lot 2 (Lindsy Ave. Roadside Parking)
FOR i in 1..20 LOOP

	-- For Regular Parking
	INSERT INTO parking_spot (lot_id, spot_number, spot_type, status)
	VALUES (2, i, 'REGULAR', 'AVAILABLE');
	
END LOOP;

-- Populating Lot 3 (City Bakery Parking)
FOR i in 1..10 LOOP

	-- For Reserved Parking
	IF i < 3 THEN
		INSERT INTO parking_spot (lot_id, spot_number, spot_type, status)
		VALUES (3, i, 'RESERVED', 'AVAILABLE');
	-- For Regular Parking
	ELSE 
		INSERT INTO parking_spot (lot_id, spot_number, spot_type, status)
		VALUES (3, i, 'REGULAR', 'AVAILABLE');
	END IF;
	
END LOOP;

END $$;

SELECT * FROM parking_spot;