"""
COMP 2300 Fall 2024 Class Project Secure Drop
MAIN
"""

"""
GIT TEST COMMENT
"""



import os
import json
from user import register_user, user_login
from keygen import write_key, encrypt_file
from utils import safe_load
from menu_options import menu
from utils import secure_exit

USERS_FILE = 'users.json'

def user_exist(login_or_register):

    while login_or_register:
        if login_or_register in ['r', 'y']:
            register_user()
            break
        elif login_or_register == 'l':
            print('LOGIN')
            user_login(menu)
            break
        else:
            print("Invalid choice, please try again.")
            login_or_register = input("\nEnter Correct Selection: ").lower()
            continue

if __name__ == "__main__":
    # Initialize user data
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump({}, file, indent=4)  # Create an empty JSON structure
        encrypt_file(USERS_FILE)  # Encrypt the new file
        write_key()

    while True:
        try:
            with open(USERS_FILE, 'r') as file:
                data = safe_load()  # changed from json.load(file) to safe_load()

                if not data:  # If no users exist
                    print("\nNo users are registered with this client.")
                    login_or_register = input(
                        "\nDo you want to register a new user (y/n)? ").lower()

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
                        login_or_register = input(
                            "\nEnter 'L' to login, 'R' to register a new user, 'E' to exit: ").lower()

                        if (login_or_register == 'e'):
                            break

                        user_exist(login_or_register)
                    break
        except InterruptedError:
            print("Error: Interrupted Error")
            secure_exit()

    # Secure exit
    print("Shutting down the application...")
    secure_exit()
