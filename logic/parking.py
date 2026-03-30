import uuid
import math
import time

class ParkingSession:
    def __init__(self, spot_id):
        self.session_id = str(uuid.uuid4())
        self.spot_id = spot_id
        self.entry_time = time.time()
        self.exit_time = None
        self.active = True

    def end_session(self):
        self.exit_time = time.time()
        self.active = False

class Ticket:
    def __init__(self, session, rate_per_hour=3):
        duration_sec = session.exit_time - session.entry_time
        self.duration_minutes = int(duration_sec / 60)
        hours = math.ceil(duration_sec / 3600)
        self.amount = hours * rate_per_hour
        self.session_id = session.session_id

class ParkingManager:
    def __init__(self):
        self.active_sessions = {}

    def start_session(self, spot_id):
        session = ParkingSession(spot_id)
        self.active_sessions[spot_id] = session
        return session

    def end_session(self, spot_id):
        session = self.active_sessions.get(spot_id)
        if not session or not session.active:
            return None
        session.end_session()
        ticket = Ticket(session)
        self.active_sessions.pop(spot_id)
        return ticket

# --- Test logic ---
if __name__ == "__main__":
    manager = ParkingManager()

    # Start a parking session
    session1 = manager.start_session("A1")
    print(f"Session started at spot {session1.spot_id}, ID: {session1.session_id}")
    
    # Simulate parking time
    time.sleep(2)

    # End session
    ticket1 = manager.end_session("A1")
    print(f"Ticket generated for session {ticket1.session_id}")
    print(f"Duration (min): {ticket1.duration_minutes}")
    print(f"Amount: ${ticket1.amount}")