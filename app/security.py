from pwdlib import PasswordHash
import os 
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

password_hash = PasswordHash.recommended()

def hash_password(password):
    return password_hash.hash(password)

def verify_password(password, hashed):
    return password_hash.verify(password, hashed)


load_dotenv()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
TOKEN_MINUTES = 30

def create_token(username):
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def read_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]