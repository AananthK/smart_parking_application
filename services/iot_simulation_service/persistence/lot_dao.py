from persistence.db_connection import get_connection

# DAO = data access object
# This file contains the code that executes sql commands on db

#----- READ -----
# persistence function to get a lot via id
def get_lot_by_id_dao(lot_id: int):
    sql = """SELECT * 
             FROM lot 
             WHERE lot_id = %s
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (lot_id,))
            record = cur.fetchone()
    
    return record

# persistence function to get all lots
def get_all_lots_dao():
    sql = """SELECT lot_id 
             FROM lot 
             """

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql)
            record = cur.fetchall()
    
    return record

#----- UPDATE -----
#persistence function to update lot status
def update_lot_status_dao(lot_id: int, status: str):
    sql = """UPDATE lot
    SET lot_status = %s
    WHERE lot_id = %s
    RETURNING lot_id"""

    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(sql, (status, lot_id))
            record = cur.fetchone()

    return record


