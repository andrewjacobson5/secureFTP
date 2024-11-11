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

USERS_FILE = 'users.json'  

# function to clear any sensitive data when existing the program
def secure_exit():
    # enable debug information for garbage collection
    # gc.set_debug(gc.DEBUG_LEAK)
    # force garbage collection. Milestone 2-2
    # print('Forcing Garbage Collection...')
    gc.collect()
    # print(f'\nGarbage Collection Completed. Unreachable Objects: {collected}')

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
    users = {}
    login_or_register = ''
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump({}, file, indent=4)  # This creates the file if it doesn't exist

    while True:
        # if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            # return loaded JSON data
            data = json.load(file)

            if data == {}:
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
                    login_or_register = input("\nEnter Correct Selection: ").lower()
                    continue
            else:
                print("\nAn User Exists in This Machine.")
                login_or_register = input("\nEnter 'L' to login, or 'R' to register a new user: ").lower()
                user_exist(login_or_register)
                break

    start_client()
    secure_exit()
