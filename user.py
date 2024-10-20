import json
import os
from encrypt import encrypt_password, check_password

def register_user():
    name = input("Enter full name: ")
    email = input("Enter email: ")

    try:
        with open('users.json', 'r') as file:
            existing_users = json.load(file)
    except FileNotFoundError:
        existing_users = {}

    if email in existing_users:
        print("A user is already registered with that email.")
        return

    password = input("Enter password: ")

    hashed_password = encrypt_password(password)

    existing_users[email] = {
        "name": name,
        "password": hashed_password
    }

    save_user(existing_users)
    
    print(f"User {email} registered successfully!")

def save_user(existing_users):
    with open('users.json', 'w') as file:
        json.dump(existing_users, file, indent=4)

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return {}

def user_login():
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        with open('users.json', 'r') as file:
            existing_users = json.load(file)
    except FileNotFoundError:
        existing_users = {}


    if email in existing_users and check_password(existing_users[email]["password"], password):
        print(f"User {email} logged in successfully!")
    else:
        print("Invalid email or password")