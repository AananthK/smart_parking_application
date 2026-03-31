from business.parking_spot_check import *
from business.lot_check import *

from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal

def occupancy_multiplier(lot_id: int):

    lot = find_lot(lot_id = lot_id)

    if lot is None:
        raise ValueError("Lot does not exist")
    else:
        
        free_spots = len(get_all_free_parking_spots_in_lot_dao(lot_id = lot_id))
        occupancy = 1 - float(free_spots/lot['capacity'])

        if occupancy <= 0.4:
            return 0.8
        elif 0.4 < occupancy <= 0.7:
            return 1.0
        elif 0.7 < occupancy <= 0.9:
            return 1.4
        else:
            return 2.0
        
def time_multiplier():

    today = datetime.now(ZoneInfo("America/Toronto"))
    time = today.time()

    if 7 <= time.hour < 9:
        return 1.3

    elif 9 <= time.hour < 17:
        return 1.0
        
    elif 17 <= time.hour < 20:
        return 1.3
        
    elif 20 <= time.hour:
        return 0.9
    else:
        return 0.0 

def find_ticket_amt(lot_id: int, duration: int, ticket_type: str):

    lot = find_lot(lot_id = lot_id)

    if lot is None:
        raise ValueError("Lot does not exist")
    else:
        if ticket_type not in {'PARKING', 'OVERCHARGE', 'VIOLATION'}:
            raise ValueError("Invalid ticket type.")

        if ticket_type == 'PARKING':
            amount = (
                lot['base_price']
                * Decimal(duration)
                * Decimal(occupancy_multiplier(lot_id=lot_id))
                * Decimal(time_multiplier())
            )
        else:
            amount = (
                lot['violation_fee']
                * Decimal(occupancy_multiplier(lot_id=lot_id))
                * Decimal(time_multiplier())
            )

        return amount.quantize(Decimal("0.01")) # round final amount to the nearest 0.01
    

            

