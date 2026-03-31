from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from business.vehicle_service import (
    register_vehicle,
    suspend_vehicle,
    view_tickets,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    try:
        return register_vehicle(license_plate=req.license_plate, owner_name=req.owner_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class SuspendRequest(BaseModel):
    license_plate: str
    access_key: str

@app.post("/vehicles/suspend")
def suspend_vehicle_endpoint(req: SuspendRequest):
    try:
        suspend_vehicle(license_plate=req.license_plate, access_key=req.access_key)
        return {"message": "Vehicle suspended successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Tickets ───────────────────────────────────────────────────────────────────

@app.get("/tickets")
def get_tickets_endpoint(license_plate: str, access_key: str):
    try:
        tickets = view_tickets(license_plate=license_plate, access_key=access_key)
        return {"tickets": tickets}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
