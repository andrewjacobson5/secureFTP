"""
COMP 2300 Fall 2024 Class Project Secure Drop
User registration and log in file
"""

import getpass
import threading
from menu_options import menu_options
from utils import load_users, save_user
from encrypt import encrypt_password, check_password
from tls_client import send_heartbeat, connect, check_online_status, listen_request


def register_user():
    full_name = input('\nEnter Full Name: ').upper()
    email = input('Enter Email Address: ').lower()
    password = getpass.getpass('Enter Password: ')
    confirm_password = getpass.getpass("Re-Enter Password: ")

    existing_users = load_users()

    if email in existing_users:
        print("A user is already registered with that email.")
        return

    if password == confirm_password:
    #if bcrypt.checkpw(confirm_password.encode(), hashed_password):
        hashed_password = encrypt_password(password)
        #hashed_password = bcrypt.hashpw(password.encode(), salt)
        existing_users[email] = {
            "full_name": full_name,
            "password": hashed_password,
            'contacts': []
        }
        print("\nPasswords Matched.")
        
        del password
        del confirm_password

        save_user(existing_users)  
        print(f"User {full_name} Registered Successfully!\n")

        # The user registration is a one-time process. Once a user is registered on a client, the
        # login module is subsequently activated. After a successful login, a "secure_drop>" shell
        # is initiated.
        exit()
    else:
        print("\nPasswords Do Not Match. Quitting.")
        del password
        del confirm_password
        exit()

def user_login():
    existing_users = load_users()

    for i in range(3):

        # logging in an offline user
        email = input("\nEnter Email Address: ")
        tls_sock, sock = connect()
        while check_online_status(email, tls_sock):
            print("User is already online!")
            return
        
        login_password = getpass.getpass("Enter Password: ")

        if email in existing_users:
            # password is not being stored on a variable to avoid leaking
            if check_password(existing_users[email]['password'], login_password):
                print("\nWELCOME TO SECUREDROP!")
                print(f"User {existing_users[email]['full_name']} Logged in Successfully!")

                # start sending heartbeats to server for presence checking
                threading.Thread(target=send_heartbeat, args=(email, tls_sock, ), daemon=True).start()
                threading.Thread(target=listen_request, args=(tls_sock, ), daemon=True).start()

                # call menu from file menu_options.py
                menu_options(email, tls_sock, sock)
                return True
            else:
                print("\nEmail and Password Combination Invalid.\n")
        else:
            print("\nEmail and Password Combination Invalid.\n")
            continue

        del login_password
