from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- READ -----
# persistence function to get parking spots by lot
def get_parking_spots_by_lot_id_dao(lot_id: int):
    sql = """SELECT * FROM parking_spot 
             WHERE lot_id = %s
             ORDER BY spot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (lot_id,))
            record = cur.fetchall()
    
    return record

# persistence function to get free parking spots by lot
def get_free_parking_spots_by_lot_dao(lot_id: int):
    sql = """SELECT * FROM parking_spot 
             WHERE lot_id = %s AND status = 'AVAILABLE'
             ORDER BY spot_id
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (lot_id,))
            record = cur.fetchall()
    
    return record

# persistence function to get parking spot by id
def get_parking_spot_by_spot_id_dao(spot_id: int):
    sql = """SELECT * FROM parking_spot 
             WHERE spot_id = %s"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (spot_id,))
            record = cur.fetchone()
    
    return record

# persistence function to get driver who is parked
def get_parked_driver_dao(driver_id: int):
    sql = """SELECT current_vehicle FROM parking_spot 
             WHERE current_vehicle = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id,))
            record = cur.fetchone()
    
    return record

# persistence function to get all parking spots occupied by a test vehicle
def get_all_test_occupied_parking_spots_dao():
    sql = """SELECT spot_id, parking_spot.status, current_vehicle FROM parking_spot 
             JOIN vehicle
             ON parking_spot.current_vehicle = vehicle.driver_id
             WHERE vehicle.vehicle_type = 'TEST'
             AND parking_spot.status = 'OCCUPIED'
             ORDER BY spot_id
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql)
            record = cur.fetchall()
    
    return record

#----- UPDATE -----
# persistence function to occupy parking spots
def occupy_parking_spot_dao(spot_id: int, driver_id: int):
    sql = """UPDATE parking_spot
    SET status = %s, current_vehicle = %s
    WHERE spot_id = %s AND status = 'AVAILABLE'
    RETURNING spot_id, parking_spot.status, current_vehicle"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('OCCUPIED', driver_id, spot_id))
            record = cur.fetchone()

    return record

# persistence function to occupy parking spots
def leave_parking_spot_dao(spot_id: int):
    sql = """UPDATE parking_spot
    SET status = %s, current_vehicle = NULL
    WHERE spot_id = %s AND status = 'OCCUPIED'
    RETURNING spot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('AVAILABLE', spot_id))
            record = cur.fetchone()

    return record

# persistence function to clear a single parking lot
def clear_parking_lot_dao(lot_id: int):
    sql = """UPDATE parking_spot
    SET status = %s, current_vehicle = NULL
    WHERE lot_id = %s AND status = 'OCCUPIED'
    RETURNING lot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('AVAILABLE', lot_id))
            record = cur.fetchall()

    return record

# persistence function to clear all parking lots
def clear_all_parking_spots_dao():
    sql = """UPDATE parking_spot
    SET status = %s, current_vehicle = NULL
    WHERE status = 'OCCUPIED'
    RETURNING spot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('AVAILABLE',))
            record = cur.fetchall()

    return record

# persistence function to clear all test vehicles in a parking lot
def clear_all_test_parking_spots_in_lot_dao(lot_id: int):
    sql = """UPDATE parking_spot
    SET status = %s, current_vehicle = NULL
    FROM vehicle
    WHERE parking_spot.current_vehicle = vehicle.driver_id
    AND parking_spot.lot_id = %s 
    AND parking_spot.status = 'OCCUPIED' 
    AND vehicle.vehicle_type = 'TEST'
    RETURNING spot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('AVAILABLE', lot_id))
            record = cur.fetchall()

    return record

# persistence function to clear all test vehicles in all parking lots
def clear_all_test_parking_spots_dao():
    sql = """UPDATE parking_spot
    SET status = %s, current_vehicle = NULL
    FROM vehicle
    WHERE parking_spot.current_vehicle = vehicle.driver_id
    AND parking_spot.status = 'OCCUPIED' 
    AND vehicle.vehicle_type = 'TEST'
    RETURNING spot_id, parking_spot.status, current_vehicle"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('AVAILABLE',))
            record = cur.fetchall()

    return record


