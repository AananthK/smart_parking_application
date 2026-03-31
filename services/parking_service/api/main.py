from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import secrets
import string

from business.parking_service import book_ticket
from business.lot_check import lot_full_check
from business.security import hash_key, verify_key

from persistence.lot_dao import get_all_lots_full_dao, get_lot_by_id_dao
from persistence.parking_spot_dao import get_all_spots_in_lot_dao
from persistence.ticket_dao import get_current_booking_dao, get_ticket_by_ticket_id_dao, cancel_booking_dao
from persistence.vehicle_dao import (
    register_vehicle_dao,
    vehicle_login_dao,
    get_real_vehicle_by_license_plate_dao,
    suspend_vehicle_dao,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Auth helper ───────────────────────────────────────────────────────────────

def authenticate(license_plate: str, access_key: str):
    lp = license_plate.strip().upper()
    row = vehicle_login_dao(license_plate=lp)
    if row is None or not verify_key(access_key, row["access_key_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    vehicle = get_real_vehicle_by_license_plate_dao(license_plate=lp)
    return dict(vehicle)


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "running"}


# ── Vehicles ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    license_plate: str
    owner_name: Optional[str] = None

@app.post("/vehicles/register")
def register_vehicle_endpoint(req: RegisterRequest):
    lp = req.license_plate.strip().upper()

    if len(lp) > 11:
        raise HTTPException(status_code=400, detail="License plate is 11 characters MAX.")
    if not lp.replace(' ', '').replace('-', '').isalnum():
        raise HTTPException(status_code=400, detail="License plate can only contain letters, numbers, spaces, or hyphens.")
    if get_real_vehicle_by_license_plate_dao(license_plate=lp):
        raise HTTPException(status_code=400, detail="License plate already registered.")
    if req.owner_name and len(req.owner_name) > 100:
        raise HTTPException(status_code=400, detail="Owner name is 100 characters MAX.")

    chars = string.ascii_uppercase + string.digits
    key = ''.join(secrets.choice(chars) for _ in range(6))

    row = register_vehicle_dao(
        license_plate=lp,
        access_key_hash=hash_key(key),
        owner_name=req.owner_name,
    )
    return {
        "driver_id": row["driver_id"],
        "license_plate": row["license_plate"],
        "access_key": key,
    }


class SuspendRequest(BaseModel):
    license_plate: str
    access_key: str

@app.post("/vehicles/suspend")
def suspend_vehicle_endpoint(req: SuspendRequest):
    vehicle = authenticate(req.license_plate, req.access_key)
    result = suspend_vehicle_dao(license_plate=vehicle["license_plate"])
    if result is None:
        raise HTTPException(status_code=400, detail="Could not suspend vehicle.")
    return {"message": "Vehicle suspended successfully."}


# ── Lots ──────────────────────────────────────────────────────────────────────

@app.get("/lots")
def get_lots():
    rows = get_all_lots_full_dao()
    return [dict(r) for r in rows]


@app.get("/lots/{lot_id}/spots")
def get_lot_spots(lot_id: int):
    if get_lot_by_id_dao(lot_id=lot_id) is None:
        raise HTTPException(status_code=404, detail="Lot not found.")
    rows = get_all_spots_in_lot_dao(lot_id=lot_id)
    return [dict(r) for r in rows]


# ── Bookings ──────────────────────────────────────────────────────────────────

class BookingRequest(BaseModel):
    license_plate: str
    access_key: str
    spot_id: int
    start_time: str
    duration: int

@app.post("/bookings")
def create_booking(req: BookingRequest):
    if req.duration < 1 or req.duration > 24:
        raise HTTPException(status_code=400, detail="Duration must be between 1 and 24 hours.")

    vehicle = authenticate(req.license_plate, req.access_key)

    try:
        ticket = book_ticket(
            driver_id=vehicle["driver_id"],
            spot_id=req.spot_id,
            duration=req.duration,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    booking = get_current_booking_dao(driver_id=vehicle["driver_id"])
    if booking is None:
        raise HTTPException(status_code=500, detail="Booking created but could not retrieve details.")

    return dict(booking)


@app.get("/bookings/current")
def get_current_booking(license_plate: str, access_key: str):
    vehicle = authenticate(license_plate, access_key)
    booking = get_current_booking_dao(driver_id=vehicle["driver_id"])
    if booking is None:
        raise HTTPException(status_code=404, detail="No active booking found.")
    return dict(booking)


class CancelBookingRequest(BaseModel):
    license_plate: str
    access_key: str

@app.delete("/bookings/{ticket_id}")
def cancel_booking(ticket_id: int, req: CancelBookingRequest):
    vehicle = authenticate(req.license_plate, req.access_key)

    ticket = get_ticket_by_ticket_id_dao(ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Booking not found.")
    if ticket["driver_id"] != vehicle["driver_id"]:
        raise HTTPException(status_code=403, detail="This booking does not belong to you.")
    if ticket["status"] != "UNPAID":
        raise HTTPException(status_code=400, detail="Only unpaid bookings can be cancelled.")

    result = cancel_booking_dao(ticket_id=ticket_id, driver_id=vehicle["driver_id"])
    if result is None:
        raise HTTPException(status_code=400, detail="Could not cancel booking.")

    from persistence.parking_spot_dao import leave_parking_spot_dao
    leave_parking_spot_dao(spot_id=result["spot_id"])

    from persistence.parking_spot_dao import get_parking_spot_by_spot_id_dao
    spot = get_parking_spot_by_spot_id_dao(spot_id=result["spot_id"])
    lot_full_check(lot_id=spot["lot_id"])

    return {"message": "Booking cancelled successfully."}


# ── Tickets ───────────────────────────────────────────────────────────────────

@app.get("/tickets")
def get_tickets(license_plate: str, access_key: str):
    vehicle = authenticate(license_plate, access_key)

    sql_tickets = """SELECT tickets.ticket_id,
                            tickets.spot_id,
                            lot.lot_name,
                            tickets.amount,
                            tickets.issued_at,
                            tickets.duration,
                            tickets.type,
                            tickets.status
                     FROM tickets
                     JOIN parking_spot ON tickets.spot_id = parking_spot.spot_id
                     JOIN lot ON parking_spot.lot_id = lot.lot_id
                     WHERE tickets.driver_id = %s
                     ORDER BY tickets.issued_at DESC"""

    from persistence.db_connection import get_connection
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_tickets, (vehicle["driver_id"],))
            rows = cur.fetchall()

    return {
        "driver_id": vehicle["driver_id"],
        "tickets": [dict(r) for r in rows],
    }
