import os
import json

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_user(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)