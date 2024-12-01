"""
COMP 2300 Fall 2024 Class Project Secure Drop
MAIN
"""

import os
import json
import threading
import sys
import gc
from user import register_user, user_login
from mutual_cert import start_server, start_client
from presence_server import start_presence_server

USERS_FILE = 'users.json'  
running = True
# function to clear any sensitive data when existing the program
def secure_exit():
    global running
    running = False
    # enable debug information for garbage collection
    gc.collect()
    # check if there are remaining objects:
    if gc.garbage:
        print('Unreachable Objects in Memory:')
        for obj in gc.garbage:
            print(f"Type: {type(obj)}, Object: {repr(obj)}")
    sys.exit()

def user_exist(login_or_register):
    
    while login_or_register:
        if login_or_register in ['r', 'y']:
            register_user()
            break
        elif login_or_register == 'l':
            print('LOGIN')
            user_login()
            break
        else:
            print("Invalid choice, please try again.")
            login_or_register = input("\nEnter Correct Selection: ").lower()
            continue


if __name__ == "__main__":
    import threading

    # Start the presence server
    print("Starting the presence server...")
    presence_thread = threading.Thread(target=start_presence_server, daemon=True)
    presence_thread.start()

    # Start the mutual TLS server
    print("Starting the mutual TLS server...")
    tls_server_thread = threading.Thread(target=start_server, daemon=True)
    tls_server_thread.start()

    # Initialize user data
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump({}, file, indent=4)  # Create empty user file if not exists

    while True:
        with open(USERS_FILE, 'r') as file:
            data = json.load(file)

            if not data:  # If no users exist
                print("\nNo users are registered with this client.")
                login_or_register = input("\nDo you want to register a new user (y/n)? ").lower()

                if login_or_register == 'y':
                    user_exist('y')
                    break
                elif login_or_register == 'n':
                    print("QUITTING")
                    break
                else:
                    print("\nInvalid choice, please try again.")
                    continue
            else:
                print("\nA User Exists in This Machine.")
                login_or_register = input("\nEnter 'L' to login, or 'R' to register a new user: ").lower()
                user_exist(login_or_register)
                break

    # Start the client
    print("Starting the client...")
    start_client()

    # Secure exit
    print("Shutting down the application...")
    secure_exit()

