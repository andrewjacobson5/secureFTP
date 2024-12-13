import os
import json
from keygen import encrypt_file, decrypt_file

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}

def safe_load():
    # decrypt json
    decrypt_file(USERS_FILE)
    # get data
    data = load_users()
    # encrypt json
    encrypt_file(USERS_FILE)
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
    