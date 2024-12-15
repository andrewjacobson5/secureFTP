import os
import json
import threading
import sys
import gc
from keygen import encrypt_file, decrypt_file

USERS_FILE = 'users.json'
lock = threading.Lock()


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
    
# clear is_online for all users (when debugging code)
def reset_user_state():
    with lock:
        users = safe_load()
        for user in users:
            users[user]["is_online"] = False
            
    safe_save(users)

    
def set_user_state(email, is_online):
    """
    Updates the user's online state in the user storage.
    
    :param email: The email of the user.
    :param is_online: 1 for online, 0 for offline.
    """
    # Example: Update user state in a dictionary or JSON file
    users = safe_load()
    if email in users:
        users[email]['is_online'] = is_online
        safe_save(users)  # Save back to storage
        print(f"Updated {email} to {'online' if is_online else 'offline'}.")
    else:
        print(f"User {email} not found.")

        
def check_user_state(username):
    with lock:
        users = safe_load()
        # Find the user, return status
        user_found = False
        for user in users:
            if user == username:
                return users[user]["is_online"]

        if not user_found:
            print(f"User '{username}' not found in database.")
            return


# function to clear any sensitive data when existing the program
def secure_exit():
    # enable debug information for garbage collection
    gc.collect()
    # check if there are remaining objects:
    if gc.garbage:
        print('Unreachable Objects in Memory:')
        for obj in gc.garbage:
            print(f"Type: {type(obj)}, Object: {repr(obj)}")
    sys.exit()