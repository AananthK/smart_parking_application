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
# persistence function to get the current active (UNPAID PARKING) booking for a driver
def get_current_booking_dao(driver_id: int):
    sql = """SELECT tickets.ticket_id,
                    tickets.driver_id,
                    tickets.spot_id,
                    parking_spot.spot_number,
                    parking_spot.lot_id,
                    lot.lot_name,
                    tickets.amount,
                    tickets.issued_at AS start_time,
                    tickets.duration,
                    tickets.status
             FROM tickets
             JOIN parking_spot ON tickets.spot_id = parking_spot.spot_id
             JOIN lot ON parking_spot.lot_id = lot.lot_id
             WHERE tickets.driver_id = %s
               AND tickets.type = 'PARKING'
               AND tickets.status = 'UNPAID'
             ORDER BY tickets.issued_at DESC
             LIMIT 1"""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (driver_id,))
            record = cur.fetchone()

    return record

# persistence function to cancel a booking (set status to CANCELLED)
def cancel_booking_dao(ticket_id: int, driver_id: int):
    sql = """UPDATE tickets
             SET status = 'CANCELLED'
             WHERE ticket_id = %s AND driver_id = %s AND status = 'UNPAID'
             RETURNING ticket_id, spot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (ticket_id, driver_id))
            record = cur.fetchone()

    return record

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