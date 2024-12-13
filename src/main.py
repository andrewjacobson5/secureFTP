"""
COMP 2300 Fall 2024 Class Project Secure Drop
MAIN
"""

import os
import json
import sys
import gc
from user import register_user, user_login
from keygen import write_key

USERS_FILE = 'users.json'  
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

def user_exist(login_or_register):
    
    while login_or_register:
        if login_or_register in ['r', 'y']:# decrypt json
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
    # Initialize user data
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump({}, file, indent=4)  # Create empty user file if not exists
        write_key()

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
                while True:
                    print("\nA User Exists in This Machine.")
                    login_or_register = input("\nEnter 'L' to login, 'R' to register a new user, 'E' to exit: ").lower()

                    if (login_or_register == 'e'):
                        break

                    user_exist(login_or_register)
                break

    # Secure exit
    print("Shutting down the application...")
    secure_exit()

