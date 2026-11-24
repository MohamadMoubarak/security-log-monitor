from contextlib import asynccontextmanager
from app.setup import setup

from fastapi.staticfiles import StaticFiles
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database import get_alerts, get_events_by_status, get_user, get_alerts_By_IP
from app.security import create_token, read_token, verify_password

@asynccontextmanager
async def lifespan(app):
    setup()
    yield


app = FastAPI(title="Security Log Monitor", lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.mount("/dashboard", StaticFiles(directory="static", html=True), name="dashboard")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        username = read_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user(form.username)
    if user is None or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return {"access_token": create_token(user["username"]), "token_type": "bearer"}

@app.get("/events")
def list_events_by_status(
    user: Annotated[dict, Depends(get_current_user)],
    status: str | None = None,
):
    return get_events_by_status(status)

# @app.get("/alerts")
# def list_alerts(user: Annotated[dict, Depends(get_current_user)]):
#     return get_alerts()

@app.get("/alerts")
def filter_alerts_By_IP(user: Annotated[dict, Depends(get_current_user)], ip : str | None = None,):
    if ip is not None:
        return get_alerts_By_IP(ip)
    return get_alerts()