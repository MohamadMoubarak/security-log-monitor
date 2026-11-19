from fastapi import FastAPI

from app.database import get_alerts, get_events

app = FastAPI(title= "Security Log Monitor")

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/events")
def list_events():
    return get_events()

@app.get("/alerts")
def list_alerts():
    return get_alerts()

