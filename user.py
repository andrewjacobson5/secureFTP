"""
COMP 2300 Fall 2024 Class Project Secure Drop
User registration and log in file
 @version: 1.1-2.26 - Milestone 1-2
"""

import os
import json
import getpass
from menu_options import menu_options
from contacts import listContacts
from encrypt import encrypt_password, check_password

USERS_FILE = 'users.json' 

full_name = ''
password = ''
email = ''

def register_user():
    # I have commented full name and address out for now, but according to the instructions,
    # we should include these. Commented out for now to make it easier for us to test - PA
    # fullname = input("Enter Full Name: ")
    # email = input("Enter Email Address: ")
    full_name = input('\nEnter Full Name: ')
    email = input('Enter Email Address: ').lower()
    # getpass wil hide the password for security purposes
    password = getpass.getpass('Enter Password: ')
    confirm_password = getpass.getpass("Re-Enter Password: ")
    # strip of any spaces
    password = password.strip()
    confirm_password = confirm_password.strip()
    email.strip()

    try:
        with open(USERS_FILE, 'r') as file:
            existing_users = json.load(file)
    except FileNotFoundError:
        existing_users = {}

    if email in existing_users:
        print("A user is already registered with that email.")
        return

    if password == confirm_password:
    #if bcrypt.checkpw(confirm_password.encode(), hashed_password):
        hashed_password = encrypt_password(password)
        #hashed_password = bcrypt.hashpw(password.encode(), salt)
        existing_users[email] = {
            "full_name": full_name,
            "password": hashed_password
        }
        print("\nPasswords Matched.")

        save_user(existing_users)  
        print(f"User {full_name} Registered Successfully!\n")

        # The user registration is a one-time process. Once a user is registered on a client, the
        # login module is subsequently activated. After a successful login, a "secure_drop>" shell
        # is initiated.
        exit()
    else:
        print("\nPasswords Do Not Match. Quitting.")
        exit()

def save_user(existing):
    with open(USERS_FILE, 'w') as file:
        json.dump(existing, file, indent=4)

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return {}

def user_login():
    try:
        with open(USERS_FILE, 'r') as file:
            existing_users = json.load(file)
    except FileNotFoundError:
        existing_users = {}

    while True:
        email = input("\nEnter Email Address: ")
        password = getpass.getpass("Enter Password: ")

        if email in existing_users and check_password(existing_users[email]['password'], password):
            print("\nWELCOME TO SECUREDROP!")
            print(f"User {existing_users[email]['full_name']} Logged in Successfully!")
            # call menu from file menu_options.py
            menu_options()
            break
        else:
            print("\nEmail and Password Combination Invalid.\n")
            continue
