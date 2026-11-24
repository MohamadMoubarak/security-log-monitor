# Security Log Monitor

A small security monitoring web app. It reads SSH login logs, detects brute-force attacks, and shows the alerts on a protected dashboard.

![Dashboard](docs/screenshots/dashboard.jpg)
![Dashboard](docs/screenshots/dashboard_2.jpg)

## Features

- Parses SSH `auth.log` lines into structured events with regular expressions
- Detects brute-force attempts: 5 failed logins from the same IP within 60 seconds raises an alert
- Stores events and alerts in a SQL database (SQLite)
- REST API built with FastAPI, with automatic documentation at `/docs`
- Login with Argon2-hashed passwords and JWT tokens
- Web dashboard with alert counters, a chart of failed logins per IP, and event tables
- Runs with Docker Compose; data is kept in a Docker volume

## How it works

```
auth.log --> parser --> detection --> SQLite database --> FastAPI REST API --> dashboard
            (regex)    (sliding window)                  (JWT protected)     (HTML/JS/Chart.js)
```

On startup, the app creates the database tables, creates the admin account from the settings, and loads the sample log if the database is empty.

## Security choices

- **Passwords are never stored**, only Argon2 hashes with a random salt.
- **JWT tokens** expire after 30 minutes; the signing key is kept in a `.env` file that is never committed or built into the image.
- **SQL injection protection:** every query uses parameterized placeholders (`?`).
- **XSS protection:** log data (attacker-controlled usernames) is inserted with `textContent`, never `innerHTML`.
- The login error message does not reveal whether a username exists.

## Tech stack

Python · FastAPI · Uvicorn · SQLite · PyJWT · pwdlib (Argon2) · HTML · CSS · JavaScript · Chart.js · Docker · Docker Compose

## Settings

Copy `.env.example` to `.env` and fill in the values:

```
SECRET_KEY=<random key>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<your password>
```

Generate a secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Run with Docker (recommended)

```bash
git clone https://github.com/MohamadMoubarak/security-log-monitor.git
cd security-log-monitor
cp .env.example .env        # then edit .env
docker compose up -d --build
```

Open http://localhost:8000/dashboard/ and log in with the admin account from `.env`.

Stop it with `docker compose down`. The data stays in the `monitor-data` volume; `docker compose down -v` also deletes it.

## Run without Docker

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1          # on Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Screenshots

| Login | API documentation |
|---|---|
| ![Login](docs/screenshots/login.jpg) | ![API docs](docs/screenshots/api-docs.jpg) |

## Project structure

```
app/
  parser.py        # reads log lines into events
  detection.py     # brute-force detection rule
  database.py      # SQLite tables and queries
  security.py      # password hashing and JWT tokens
  setup.py         # first-run setup: tables, admin user, sample data
  main.py          # FastAPI routes
  ingest.py        # reloads the sample log by hand
  create_user.py   # creates an extra login account
static/            # dashboard (HTML, CSS, JavaScript)
samples/auth.log   # sample log with a simulated attack
Dockerfile         # builds the app image
docker-compose.yml # runs the app with its settings and volume
.env.example       # settings template
```
