from getpass import getpass

from app.database import create_tables, save_user
from app.security import hash_password

if __name__ == "__main__":
    create_tables()
    username = input("Username: ")
    password = getpass("Password: ")
    save_user(username, hash_password(password))
    print(f"User '{username}' created")