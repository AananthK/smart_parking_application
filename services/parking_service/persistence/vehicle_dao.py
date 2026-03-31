from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- READ -----
# persistence function to get a real (active) vehicle via id
def get_real_vehicle_by_id_dao(driver_id: int):
    sql = """SELECT driver_id,license_plate 
             FROM vehicle 
             WHERE driver_id = %s AND vehicle_type = %s AND status = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id, 'REAL', 'ACTIVE'))
            record = cur.fetchone()
    
    return record

# persistence function to get a real (active) vehicle via license_plate
def get_real_vehicle_by_license_plate_dao(license_plate: int):
    sql = """SELECT driver_id,license_plate 
             FROM vehicle 
             WHERE license_plate = %s AND vehicle_type = %s AND status = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (license_plate, 'REAL', 'ACTIVE'))
            record = cur.fetchone()
    
    return record

