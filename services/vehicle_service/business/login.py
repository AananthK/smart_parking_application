from business.security import verify_key
from persistence.vehicle_dao import (
    vehicle_login_dao, 
    get_real_vehicle_by_license_plate_dao)

def vehicle_login(license_plate: str, access_key: str):
    
    vehicle = vehicle_login_dao(license_plate = license_plate)

    if not vehicle or not verify_key(key = access_key, key_hash = vehicle['access_key_hash']):
        raise ValueError("Invalid credentials")

    auth_vehicle = get_real_vehicle_by_license_plate_dao(license_plate = license_plate)

    return dict(auth_vehicle)