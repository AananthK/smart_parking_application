from persistence.parking_spot_dao import get_parking_spot_by_spot_id_dao

# helper function to find a parking spot
def find_parking_spot(spot_id: int):
    return get_parking_spot_by_spot_id_dao(spot_id)

# helper function to verify if parking spot is free
def parking_spot_free(spot_id: int):
    
    p = find_parking_spot(spot_id = spot_id)
    if p is None:
        return False
    else:
        return p['status'] == 'AVAILABLE'
            
