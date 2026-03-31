import random
from persistence.parking_spot_dao import (
    get_free_parking_spots_by_lot_dao,
    occupy_parking_spot_dao,
    clear_parking_lot_dao,
    clear_all_test_parking_spots_in_lot_dao,
    clear_all_test_parking_spots_dao,
    clear_all_parking_spots_dao
)
from persistence.vehicle_dao import get_all_test_vehicles_dao
from persistence.lot_dao import get_all_lots_dao
from business.vehicle_check import test_vehicle_parked
from business.lot_check import find_lot, lot_open, lot_full_check

# business function to find ids of free parking spots
def find_free_parking(lot_id: int):
    
    if lot_open(lot_id):
        spots = get_free_parking_spots_by_lot_dao(lot_id=lot_id)

        if not spots:
            raise ValueError(f"Lot {lot_id} is full")

        spot_ids = []
        for spot in spots:
            spot_ids.append(spot['spot_id'])

        return spot_ids
    else:
        raise ValueError(f"Lot {lot_id} is closed")

# business function to simulate IoT sensors for parking lot occupation
def simulate_lot_occupancy(lot_id: int, activity_rate: float):
    if not (0 <= activity_rate <= 1):
        raise ValueError("activity_rate must be between 0 and 1")

    # get free parking spot IDs
    free_spot_ids = find_free_parking(lot_id=lot_id)

    # get all test vehicles
    all_test_vehicles = get_all_test_vehicles_dao()

    # get IDs of vehicles not already parked
    available_vehicle_ids = []
    for vehicle in all_test_vehicles:
        vehicle_id = vehicle['driver_id']
        if not test_vehicle_parked(driver_id = vehicle_id):
            available_vehicle_ids.append(vehicle_id)

    # determine how many vehicles to park
    target = int(len(all_test_vehicles) * activity_rate)
    # the number of vehicles parked is the least of available cars(both full and expected) and available spots
    target = min(target, len(free_spot_ids), len(available_vehicle_ids))

    if target == 0:
        return 0

    # randomly selecting parking spots and vehicles
    selected_vehicle_ids = random.sample(available_vehicle_ids, target)
    selected_spot_ids = random.sample(free_spot_ids, target)

    parked_spots = []
    for vehicle_id, spot_id in zip(selected_vehicle_ids, selected_spot_ids):
        result = occupy_parking_spot_dao(spot_id=spot_id, driver_id=vehicle_id)
        if result is not None:
            parked_spots.append(result)

    lot_full_check(lot_id = lot_id)

    return parked_spots

# business function to clear parking lot
def clear_parking_lot(lot_id: int):

    if find_lot(lot_id = lot_id):
        empty_lot = clear_parking_lot_dao(lot_id = lot_id)
        lot_full_check(lot_id = lot_id)

        if not empty_lot:
            return None
        else:
            return empty_lot
    
    else:
        raise ValueError ("Lot does not exist")

# business function to clear all parking spots
def clear_all_parking_spots():
    spots = clear_all_parking_spots_dao()

    lots = get_all_lots_dao()

    for lot in lots:
        lot_full_check(lot_id = lot['lot_id'])

    return spots

# business function to clear all test vehicles in parking lot
def clear_test_vehicles_in_parking_lot(lot_id: int):

    if find_lot(lot_id = lot_id):
        empty_lot = clear_all_test_parking_spots_in_lot_dao(lot_id = lot_id)
        lot_full_check(lot_id = lot_id)

        if not empty_lot:
            return None
        else:
            return empty_lot
    
    else:
        raise ValueError ("Lot does not exist")
    
# business function to clear all test parking spots
def clear_test_vehicles_in_all_parking_spots():
    spots = clear_all_test_parking_spots_dao()

    lots = get_all_lots_dao()

    for lot in lots:
        lot_full_check(lot_id = lot['lot_id'])

    return spots


