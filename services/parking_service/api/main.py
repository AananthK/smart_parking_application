from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from business.parking_service import book_ticket, leave_lot

app = FastAPI()

# request body for booking a ticket
class BookTicketRequest(BaseModel):
    driver_id: int
    spot_id: int
    duration: int

# request body for leaving the lot
class LeaveLotRequest(BaseModel):
    ticket_id: int


# GET /health to confirm API is reachable
@app.get("/health")
def health():
    return {"status": "running"}


# POST endpoint to book a parking ticket
@app.post("/parking/book")
def book_ticket_endpoint(request: BookTicketRequest):
    try:
        return book_ticket(
            driver_id=request.driver_id,
            spot_id=request.spot_id,
            duration=request.duration
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# POST endpoint for driver leaving the lot
@app.post("/parking/leave")
def leave_lot_endpoint(request: LeaveLotRequest):
    try:
        return leave_lot(ticket_id=request.ticket_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))