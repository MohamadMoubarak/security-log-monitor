import re

LINE_PATTERN = re.compile(
    r"^(\w{3}\s+\d+ \d{2}:\d{2}:\d{2}) \S+ sshd\[\d+\]: "
    r"(Failed|Accepted) password for (?:invalid user )?(\S+) "
    r"from (\S+) port (\d+)"
)

def parse_line(line):
    match = LINE_PATTERN.search(line)
    if match is None:
        return None
    return {
        "time": match.group(1),
        "status": match.group(2).lower(),
        "user": match.group(3),
        "ip": match.group(4),
        "port": int(match.group(5)),
    }

def read_events(path):
    events = []
    with open(path) as f:
        for line in f:
            event = parse_line(line)
            if event is not None:
                events.append(event)
    return events

if __name__ == "__main__":
    for event in read_events("samples/auth.log"):
        print(event)

