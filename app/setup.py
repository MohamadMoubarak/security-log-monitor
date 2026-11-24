import os

from app.database import create_tables, get_events, get_user, save_alerts, save_events, save_user
from app.detection import detect_brute_force
from app.parser import read_events
from app.security import hash_password

def setup():
    create_tables()

    username = os.environ.get("ADMIN_USERNAME")
    password = os.environ.get("ADMIN_PASSWORD")
    if username and password and get_user(username) is None:
        save_user(username, hash_password(password))

    if not get_events():
        events = read_events("samples/auth.log")
        save_events(events)
        save_alerts(detect_brute_force(events))