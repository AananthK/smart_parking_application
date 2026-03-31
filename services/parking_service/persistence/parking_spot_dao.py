from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- READ -----
# persistence function to get all parking spots
def get_all_parking_spots_dao():
    sql = """SELECT * FROM parking_spot 
             ORDER BY spot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql)
            record = cur.fetchall()
    
    return record

# persistence function to get all free parking spots
def get_free_parking_spots_dao():
    sql = """SELECT * FROM parking_spot 
             WHERE status = 'AVAILABLE'
             ORDER BY spot_id
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql)
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
    sql = """SELECT spot_id, current_vehicle FROM parking_spot 
             WHERE current_vehicle = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id,))
            record = cur.fetchone()
    
    return record

# persistence function to get all parking spots in a lot
def get_all_free_parking_spots_in_lot_dao(lot_id: int):
    sql = """SELECT * FROM parking_spot 
             WHERE lot_id = %s
             AND status = %s
             ORDER BY spot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (lot_id, 'AVAILABLE'))
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


