from fastapi import FastAPI

from app.database import get_alerts, get_events, get_events_by_status

app = FastAPI(title= "Security Log Monitor")

@app.get("/")
def home():
    return {"status": "running"}

# @app.get("/events")
# def list_events():
#     return get_events()

@app.get("/alerts")
def list_alerts():
    return get_alerts()

@app.get("/events")
def list_events_by_status(status: str | None = None):
    return get_events_by_status(status)
