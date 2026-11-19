from app.database import create_tables, clear_tables, save_events, save_alerts
from app.detection import detect_brute_force
from app.parser import read_events

if __name__ == "__main__":
    create_tables()
    clear_tables()
    events = read_events("samples/auth.log")
    alerts = detect_brute_force(events)
    save_events(events)
    save_alerts(alerts)
    print(f"Saved {len(events)} events and {len(alerts)} alerts")