from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- READ -----
# persistence function to get all test vehicles
def get_all_test_vehicles_dao():
    sql = """SELECT driver_id,license_plate 
             FROM vehicle 
             WHERE vehicle_type = %s
             ORDER BY driver_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('TEST',))
            record = cur.fetchall()
    
    return record

# persistence function to get a test vehicle via id
def get_test_vehicle_by_id_dao(driver_id: int):
    sql = """SELECT driver_id,license_plate 
             FROM vehicle 
             WHERE driver_id = %s AND vehicle_type = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id, 'TEST',))
            record = cur.fetchone()
    
    return record


