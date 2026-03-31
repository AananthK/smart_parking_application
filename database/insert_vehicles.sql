DO $$
BEGIN

-- Creating 70 test cars
FOR i in 1..70 LOOP

	INSERT INTO vehicle (license_plate, vehicle_type, status)
	VALUES (CONCAT('TESTCAR', CAST(i AS VARCHAR(2))), 'TEST', 'ACTIVE');
	
END LOOP;

END $$;

SELECT * FROM vehicle;