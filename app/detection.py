from datetime import datetime, timedelta

from app.parser import read_events

def to_datetime(time_text):
    return datetime.strptime(f"2026 {time_text}", "%Y %b %d %H:%M:%S")

def detect_brute_force(events, max_failures=5, window_seconds=60):
    failures_by_ip = {}
    alerts = []
    for event in events:
        if event["status"] != "failed":
            continue
        ip = event["ip"]
        when = to_datetime(event["time"])
        times = failures_by_ip.setdefault(ip, [])
        times.append(when)
        recent = [t for t in times if when - t <= timedelta(seconds=window_seconds)]
        failures_by_ip[ip] = recent
        if len(recent) == max_failures:
            alerts.append({
                "ip": ip,
                "failures": len(recent),
                "first_seen": recent[0],
                "last_seen": when,
            })

    return alerts

if __name__ == "__main__":
    events = read_events("samples/auth.log")
    for a in detect_brute_force(events):
        print(f"ALERT: {a['ip']} - {a['failures']} failed logins "
              f"between {a['first_seen']:%H:%M:%S} and {a['last_seen']:%H:%M:%S}")
        