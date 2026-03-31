from persistence.lot_dao import get_lot_by_id_dao, update_lot_status_dao
from persistence.parking_spot_dao import get_free_parking_spots_by_lot_dao

# helper function to find a parking lot
def find_lot(lot_id: int):
    return get_lot_by_id_dao(lot_id)

# helper function to verify if parking lot is free (not full)
def lot_open(lot_id: int):
    
    l = find_lot(lot_id = lot_id)
    if l is None:
        return False
    else:
        return l['lot_status'] != 'CLOSED'
    
def lot_full_check(lot_id: int):
    # No free parking spots left -> change lot status to "FULL"
    if not get_free_parking_spots_by_lot_dao(lot_id = lot_id):
        update_lot_status_dao(lot_id = lot_id, status = 'FULL')
        return True
    else:
        update_lot_status_dao(lot_id = lot_id, status = 'OPEN')
    return False