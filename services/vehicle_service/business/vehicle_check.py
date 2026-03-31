from persistence.vehicle_dao import get_real_vehicle_by_license_plate_dao

def license_plate_taken(license_plate: str):
    return get_real_vehicle_by_license_plate_dao(license_plate = license_plate)

    