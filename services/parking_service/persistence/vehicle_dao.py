from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- CREATE -----
def register_vehicle_dao(license_plate: str, access_key_hash: str, owner_name: str):
    sql = """INSERT INTO vehicle
             (license_plate, access_key_hash, owner_name, vehicle_type, status)
             VALUES (%s, %s, %s, %s, %s)
             RETURNING driver_id, license_plate, owner_name, status"""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (license_plate, access_key_hash, owner_name, 'REAL', 'ACTIVE'))
            record = cur.fetchone()

    return record

#----- READ -----
# persistence function to get a vehicle for login (includes hash)
def vehicle_login_dao(license_plate: str):
    sql = """SELECT driver_id, license_plate, access_key_hash
             FROM vehicle
             WHERE license_plate = %s AND vehicle_type = %s AND status = %s"""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (license_plate, 'REAL', 'ACTIVE'))
            record = cur.fetchone()

    return record

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
def get_real_vehicle_by_license_plate_dao(license_plate: str):
    sql = """SELECT driver_id, license_plate
             FROM vehicle
             WHERE license_plate = %s AND vehicle_type = %s AND status = %s"""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (license_plate, 'REAL', 'ACTIVE'))
            record = cur.fetchone()

    return record

#----- UPDATE -----
def suspend_vehicle_dao(license_plate: str):
    sql = """UPDATE vehicle
             SET status = %s
             WHERE license_plate = %s AND status = %s
             RETURNING driver_id, license_plate, status"""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, ('SUSPENDED', license_plate, 'ACTIVE'))
            record = cur.fetchone()

    return record
