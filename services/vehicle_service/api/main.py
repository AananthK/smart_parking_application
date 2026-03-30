from fastapi import FastAPI, HTTPException

from business.vehicle_service import (
    register_vehicle,
    suspend_vehicle,
    view_tickets,
    pay_ticket,
    cancel_ticket
)

app = FastAPI()


# ---------- Health ----------

@app.get("/health")
def health():
    return {"status": "running"}


# ---------- Vehicle ----------

@app.post("/vehicle/register")
def register_vehicle_endpoint(license_plate: str, owner_name: str = None):
    try:
        key = register_vehicle(license_plate=license_plate, owner_name=owner_name)
        return {
            "license_plate": license_plate.strip().upper(),
            "access_key": key
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/vehicle/suspend")
def suspend_vehicle_endpoint(license_plate: str, access_key: str):
    try:
        return suspend_vehicle(license_plate=license_plate, access_key=access_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- Tickets ----------

@app.post("/tickets/view")
def view_tickets_endpoint(license_plate: str, access_key: str):
    try:
        return view_tickets(license_plate=license_plate, access_key=access_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tickets/pay")
def pay_ticket_endpoint(license_plate: str, access_key: str, ticket_id: int):
    try:
        return pay_ticket(
            license_plate=license_plate,
            access_key=access_key,
            ticket_id=ticket_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tickets/cancel")
def cancel_ticket_endpoint(license_plate: str, access_key: str, ticket_id: int):
    try:
        return cancel_ticket(
            license_plate=license_plate,
            access_key=access_key,
            ticket_id=ticket_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))