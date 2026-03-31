from datetime import datetime
from zoneinfo import ZoneInfo
from business.sim_helper import (
    simulate_lot_occupancy, 
    clear_test_vehicles_in_parking_lot, 
    clear_test_vehicles_in_all_parking_spots)
from persistence.lot_dao import get_all_lots_dao
from persistence.parking_spot_dao import get_all_test_occupied_parking_spots_dao

import random

def get_actvity_rate():

    # boundary values for activity values
    activity_min = 0
    activity_max = 0

    today = datetime.now(ZoneInfo("America/Toronto"))
    time = today.time()

    day = today.isoweekday()
    # converts day to integer (Monday = 1, Sunday = 7)

    # All Days -> 12AM - 6AM: Parking Lots are closed
    # For weekdays, there are 4 major time intervals
    # 6AM - 9AM: Before Work (20% - 30%)
    # 9AM - 5PM: During Work (40% - 60%)
    # 5PM - 10PM: After Work (70% - 90%)
    # 10PM - 12AM: Late Hours (30% - 50%)

    # Weekdays (Monday - Friday)
    if day in range(1,6):
        if 6 <= time.hour < 9:
            activity_min = 20
            activity_max = 30

        elif 9 <= time.hour < 17:
            activity_min = 40
            activity_max = 60
        
        elif 17 <= time.hour < 22:
            activity_min = 70
            activity_max = 90
        
        elif 22 <= time.hour:
            activity_min = 30
            activity_max = 50
        
        # 12AM - 6AM (parking lot closed -> no activity)
        else:
            return 0.0 
    
    # For weekends, there are 3 major time intervals
    # 6AM - 11AM: Early (10% - 40%)
    # 11AM - 6PM: Active (80% - 90%)
    # 6PM - 12AM: Late (60% - 90%)
    
    # Weekends (Saturday, Sunday)
    if day in (6,7):
        if 6 <= time.hour < 11:
            activity_min = 10
            activity_max = 40

        elif 11 <= time.hour < 18:
            activity_min = 80
            activity_max = 90
        
        elif 18 <= time.hour:
            activity_min = 60
            activity_max = 90

        # 12AM - 6AM (parking lot closed -> no activity)
        else:
            return 0.0 

    return float(random.randint(activity_min, activity_max)/100)

# function to run the IoT occupation simulation
def run_simulation():

    # get randomized activity rate
    actv_rate = get_actvity_rate()

    # retrieve all parking lots
    lots = get_all_lots_dao()

    print(lots)

    for lot in lots:
        lot_id = lot['lot_id']

        clear_test_vehicles_in_parking_lot(lot_id = lot_id)
        simulate_lot_occupancy(lot_id = lot_id, activity_rate = actv_rate)
        updated_rows = get_all_test_occupied_parking_spots_dao()

    return [dict(row) for row in updated_rows] # convert DictRow cursor object to python dict

def clear_simulation():
    updated_rows = clear_test_vehicles_in_all_parking_spots()
    return [dict(row) for row in updated_rows]


    
    

