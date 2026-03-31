from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- CREATE -----
# persistence function to create a ticket
def book_ticket_dao(driver_id: int, spot_id: int, amount: float, duration: int):
    sql = """INSERT INTO tickets(driver_id, spot_id, amount, duration, type, status)
             VALUES (%s, %s, %s, %s, %s, %s)
             RETURNING ticket_id, driver_id, spot_id
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id, spot_id, amount, duration, 'PARKING', 'UNPAID'))
            record = cur.fetchone()
    
    return record

def create_overcharge_ticket_dao(driver_id: int, spot_id: int, amount: float, duration: int):
    sql = """INSERT INTO tickets(driver_id, spot_id, amount, duration, type, status))
             VALUES (%s, %s, %s, %s, %s, %s)
             RETURNING ticket_id, driver_id, spot_id
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id, spot_id, amount, duration, 'OVERCHARGE', 'UNPAID'))
            record = cur.fetchall()
    
    return record

def create_violation_ticket_dao(driver_id: int, spot_id: int, amount: float, duration: int):
    sql = """INSERT INTO tickets(driver_id, spot_id, amount, duration, type, status)
             VALUES (%s, %s, %s, %s, %s, %s)
             RETURNING ticket_id, driver_id, spot_id
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id, spot_id, amount, duration, 'VIOLATION', 'UNPAID'))
            record = cur.fetchall()
    
    return record

#----- READ -----
# persistence function to a ticket by ticket_id
def get_ticket_by_ticket_id_dao(ticket_id: int):
    sql = """SELECT * 
             FROM tickets 
             WHERE ticket_id = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (ticket_id,))
            record = cur.fetchone()
    
    return record