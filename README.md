# Smart Parking Application

Distributed smart parking system using Python, IoT sensor simulation, real-time occupancy tracking, and dynamic pricing.

## Architecture

The system runs as three independent FastAPI services and a React frontend:

| Service | Port | Responsibilities |
|---|---|---|
| `vehicle_service` | 8001 | Vehicle registration, suspension, ticket viewing |
| `parking_service` | 8002 | Lots, spots, bookings, authentication |
| `iot_simulation_service` | 8003 | Simulates parking occupancy (runs hourly) |
| React frontend | 3000 | Web UI |

---

## Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- pgAdmin (optional, for managing the database)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/AananthK/smart_parking_application.git
cd smart_parking_application
```

### 2. Install Python dependencies

```bash
pip install -r services/requirements.txt
pip install tzdata
```

### 3. Set up the database

In pgAdmin (or the PostgreSQL SQL shell):

1. Create a new database named `smart_parking`
2. Open the Query Tool connected to `smart_parking`
3. Run each of the following files in order:
   - `database/create_tables.sql`
   - `database/insert_lots.sql`
   - `database/insert_parking_spots.sql`
   - `database/insert_vehicles.sql`

### 4. Create `.env` files for each service

Create a file named `.env` in each of the three service directories with your database credentials:

**`services/vehicle_service/.env`**
**`services/parking_service/.env`**
**`services/iot_simulation_service/.env`**

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smart_parking
DB_USERNAME=postgres
DB_PASSWORD=your_password
```

### 5. Install frontend dependencies

```bash
cd frontend
npm install
```

---

## Running the Application

Start each service in a separate terminal, then start the frontend.

**Terminal 1 — vehicle_service:**
```bash
cd services/vehicle_service
uvicorn api.main:app --reload --port 8001
```

**Terminal 2 — parking_service:**
```bash
cd services/parking_service
uvicorn api.main:app --reload --port 8002
```

**Terminal 3 — iot_simulation_service:**
```bash
cd services/iot_simulation_service
uvicorn api.main:app --reload --port 8003
```

**Terminal 4 — frontend:**
```bash
cd frontend
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## Features

- **Register a vehicle** — provide a license plate and optional owner name; receive a one-time password to authenticate future actions
- **Remove a vehicle** — suspend a registered vehicle using your license plate and password
- **Book parking** — browse available lots, view a colour-coded spot grid, and reserve a spot
- **View bookings** — look up your active booking using your license plate and password
- **View tickets** — see all parking tickets associated with your vehicle
- **IoT simulation** — the simulation service automatically runs once per hour, updating spot occupancy based on time-of-day and day-of-week activity rates

---

## Database Schema

| Table | Description |
|---|---|
| `lot` | Parking lots with capacity, pricing, and status |
| `vehicle` | Registered vehicles with hashed access keys |
| `parking_spot` | Individual spots linked to lots, with occupancy status |
| `tickets` | Parking, overcharge, and violation tickets |
