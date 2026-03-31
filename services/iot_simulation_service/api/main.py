from fastapi import FastAPI
from business.simulation import run_simulation, clear_simulation

app = FastAPI()

# GET /health to confirm API is reachable by robot
@app.get("/health")
def health():
    return {"status": "running"}

# POST endpoint to run simulation
@app.post("/simulation/run")
def run_simulation_endpoint():
    return run_simulation()
     

# POST endpoint to clear simulation
@app.post("/simulation/clear")
def clear_simulation_endpoint():
    return clear_simulation()

