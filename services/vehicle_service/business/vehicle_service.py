from persistence.vehicle_dao import(
    get_all_real_vehicles_dao,
    get_real_vehicle_by_license_plate_dao,
    register_vehicle_dao,
    suspend_vehicle_dao
)
from persistence.ticket_dao import(
    view_all_tickets_by_driver_id_dao,
    pay_ticket_dao,
    cancel_ticket_dao
)

from business.vehicle_check import license_plate_taken
from business.ticket_check import ticket_exists, find_unpaid_tickets
from business.security import hash_key
from business.login import vehicle_login

from typing import Optional
import secrets
import string


def register_vehicle(license_plate: str, owner_name: Optional[str] = None):

    license_plate = license_plate.strip().upper()

    if len(license_plate) > 11:
        raise ValueError("License Plate is 11 characters MAX.")
    
    if not license_plate.replace(' ', '').replace('-', '').isalnum():
        raise ValueError("License plate can only contain letters, numbers, spaces, or hyphens.")

    if license_plate_taken(license_plate = license_plate):
        raise ValueError("License Plate is already registered.")
    else:

        # Combine uppercase letters, lowercase letters, and digits
        characters = string.ascii_uppercase + string.digits
        # Randomly select 'length' characters from the combined pool and join them
        key = ''.join(secrets.choice(characters) for _ in range(6))

        if owner_name is not None:
            if len(owner_name) > 100:
                raise ValueError("Owner name is too large. 100 characters MAX.")

        # owner name if not defined (None) will be translated as 'NULL' in the DB
        row = register_vehicle_dao(license_plate = license_plate,
                                   access_key_hash = hash_key(key = key),
                                   owner_name = owner_name)

        return {"driver_id": row["driver_id"], "license_plate": row["license_plate"], "access_key": key}
    
def authenticate_vehicle(license_plate: str, access_key: str):
    license_plate = license_plate.strip().upper()

    vehicle = get_real_vehicle_by_license_plate_dao(license_plate=license_plate)

    if vehicle is None:
        raise ValueError("Plate not registered.")

    if not vehicle_login(license_plate=license_plate, access_key=access_key):
        raise ValueError("Incorrect credentials.")

    return vehicle

def suspend_vehicle(license_plate: str, access_key: str):

    vehicle = authenticate_vehicle(license_plate = license_plate, access_key = access_key)

    # Check for unpaid tickets
    unpaid_tickets = find_unpaid_tickets(driver_id= vehicle['driver_id'])

    if unpaid_tickets:
        raise ValueError("Cannot suspend vehicle with pending ticket payments.")

    sus_vehicle = suspend_vehicle_dao(license_plate = license_plate)
    
    return dict(sus_vehicle)
    
def view_tickets(license_plate: str, access_key: str):

    vehicle = authenticate_vehicle(license_plate = license_plate, access_key = access_key)
    
    tickets = view_all_tickets_by_driver_id_dao(driver_id = vehicle['driver_id'])

    return [dict(t) for t in tickets]

def pay_ticket(license_plate: str, access_key: str, ticket_id: int):

    vehicle = authenticate_vehicle(license_plate = license_plate, access_key = access_key)
    
    t = ticket_exists(ticket_id = ticket_id)

    if t is None:
        raise ValueError("Ticket does not exist")
    elif t['status'] == 'PAID':
        raise ValueError("Ticket already paid")
    elif t['status'] == 'CANCELLED':
        raise ValueError("Ticket cancelled. Cannot pay.")
    
    ticket = pay_ticket_dao(ticket_id = ticket_id, driver_id = vehicle['driver_id'])

    return dict(ticket)

def cancel_ticket(license_plate: str, access_key: str, ticket_id: int):

    vehicle = authenticate_vehicle(license_plate = license_plate, access_key = access_key)
    
    t = ticket_exists(ticket_id = ticket_id)

    if t is None:
        raise ValueError("Ticket does not exist")
    elif t['status'] == 'CANCELLED':
        raise ValueError("Ticket already cancelled")
    elif t['status'] == 'PAID':
        raise ValueError("Ticket paid. Cannot cancel.")

    ticket = cancel_ticket_dao(ticket_id = ticket_id, driver_id = vehicle['driver_id'])

    return dict(ticket)
