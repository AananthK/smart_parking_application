from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- READ -----
# persistence function to get all tickets driver_id (for viewing, hence the JOIN statements)
def view_all_tickets_by_driver_id_dao(driver_id: int):
    sql = """SELECT tickets.driver_id, 
                    vehicle.license_plate, 
                    lot.lot_name, 
                    parking_spot.spot_number,
                    tickets.amount,
                    tickets.issued_at,
                    tickets.duration,
                    tickets.type,
                    tickets.status
             FROM tickets 
             JOIN vehicle
                ON tickets.driver_id = vehicle.driver_id
             JOIN parking_spot
                ON tickets.spot_id = parking_spot.spot_id
             JOIN lot
                ON parking_spot.lot_id = lot.lot_id
             WHERE tickets.driver_id = %s 
                AND vehicle.vehicle_type = %s 
                AND vehicle.status = %s
             ORDER BY tickets.issued_at"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id, 'REAL', 'ACTIVE'))
            record = cur.fetchall()
    
    return record

# persistence function to get all tickets for driver (for operational purposes)
def get_all_tickets_by_driver_id(driver_id: int):
    sql = """SELECT ticket_id 
             FROM tickets 
             WHERE driver_id = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id,))
            record = cur.fetchall()
    
    return record

# persistence function to a ticket by ticket_id
def get_ticket_by_ticket_id(ticket_id: int):
    sql = """SELECT ticket_id 
             FROM tickets 
             WHERE ticket_id = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (ticket_id,))
            record = cur.fetchone()
    
    return record

# persistence function to get all unpaid tickets for driver
def get_all_unpaid_tickets_by_driver_id(driver_id: int):
    sql = """SELECT ticket_id 
             FROM tickets 
             WHERE driver_id = %s AND status = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (driver_id, 'UNPAID'))
            record = cur.fetchall()
    
    return record

#----- UPDATE -----
# persistence function to suspend a vehicle
def pay_ticket_dao(ticket_id: int, driver_id: int):
    sql = """UPDATE tickets
             SET status = %s 
             WHERE ticket_id = %s 
             AND driver_id = %s
             AND status = %s 
             RETURNING ticket_id, amount, status
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('PAID', ticket_id, driver_id, 'UNPAID'))
            record = cur.fetchone()
    
    return record

# persistence function to suspend a vehicle
def cancel_ticket_dao(ticket_id: int, driver_id: int):
    sql = """UPDATE tickets
             SET status = %s 
             WHERE ticket_id = %s 
             AND driver_id = %s 
             AND status != %s 
             RETURNING ticket_id, amount, status
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, ('CANCELLED', ticket_id, driver_id, 'CANCELLED'))
            record = cur.fetchone()
    
    return record
