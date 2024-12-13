import os
import json
import threading
from keygen import encrypt_file, decrypt_file

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            try:
                return json.load(file)  # Attempt to load JSON
            except json.JSONDecodeError:
                return {}  # Return an empty dictionary if file is invalid or empty
    return {}


def safe_load():
    decrypt_file(USERS_FILE)  # Decrypt the file
    data = load_users()  # Load users using the updated function
    encrypt_file(USERS_FILE)  # Re-encrypt the file after loading
    return data


def safe_save(users):
    # decrypt json
    decrypt_file(USERS_FILE)
    # get data
    data = save_user(users)
    # encrypt json
    encrypt_file(USERS_FILE)
    return data


def save_user(users):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump(users, file, indent=4)
    else:
        return
    