from persistence.ticket_dao import *
from persistence.parking_spot_dao import(
    occupy_parking_spot_dao,
    leave_parking_spot_dao
)

from business.vehicle_check import *
from business.parking_spot_check import *
from business.lot_check import *
from business.ticket_pricing import find_ticket_amt

# business function to book ticket
def book_ticket(driver_id, spot_id, duration):

    if vehicle_parked(driver_id = driver_id):
        raise ValueError("Vehicle already parked")

    if not parking_spot_free(spot_id = spot_id):
        raise ValueError("Parking spot occupied")
    
    spot = get_parking_spot_by_spot_id_dao(spot_id = spot_id)
    lot_id = spot['lot_id']

    ticket = book_ticket_dao(driver_id = driver_id, 
                             spot_id = spot_id, 
                             amount = find_ticket_amt(lot_id = lot_id, 
                                                      duration = duration, 
                                                      ticket_type = 'PARKING'),
                                                      duration=duration)
    
    # a user books their ticket shortly after they park (ASSUMPTION)
    occupy_parking_spot_dao(spot_id = spot_id, driver_id = driver_id)

    lot_full_check
    return dict(ticket)

# business function if driver leaves parking lot
# ASSUMPTION due to time crunch (assume driver leaves on time)
def leave_lot(ticket_id: int):

    t = get_ticket_by_ticket_id_dao(ticket_id = ticket_id)

    if t is None:
        raise ValueError("Ticket does not exist")
    
    if t['status'] == 'UNPAID':
        raise ValueError("Please pay ticket")

    parking = get_parked_driver_dao(driver_id = t['driver_id'])
    
    if parking is None:
        raise ValueError("Vehicle is not parked")

    spot = leave_parking_spot_dao(spot_id = parking['spot_id'])
    lot_full_check

    return dict(spot)

