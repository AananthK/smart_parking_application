from persistence.vehicle_dao import get_test_vehicle_by_id_dao
from persistence.parking_spot_dao import get_parked_driver_dao

# helper function to check find vehicle by id
def find_test_vehicle(driver_id: int):
    return get_test_vehicle_by_id_dao(driver_id = driver_id)

# helper function to check if driver is parked 
def test_vehicle_parked(driver_id: int):
    
    d = find_test_vehicle(driver_id = driver_id)

    if d is None:
        return False
    else:
        pd = get_parked_driver_dao(driver_id = d['driver_id'])
        return pd is not None