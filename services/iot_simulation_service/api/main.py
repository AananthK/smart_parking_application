import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from business.simulation import run_simulation, clear_simulation


def _hourly_scheduler():
    """Runs the simulation once per hour in a background thread."""
    run_simulation()
    timer = threading.Timer(3600, _hourly_scheduler)
    timer.daemon = True
    timer.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the first run immediately, then repeat every hour
    timer = threading.Timer(0, _hourly_scheduler)
    timer.daemon = True
    timer.start()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/simulation/run")
def run_simulation_endpoint():
    return run_simulation()


@app.post("/simulation/clear")
def clear_simulation_endpoint():
    return clear_simulation()
