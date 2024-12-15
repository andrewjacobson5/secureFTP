"""
COMP 2300 Fall 2024 Class Project Secure Drop
User registration and log in file
"""

import getpass
from utils import safe_load, safe_save, check_user_state, set_user_state
from encrypt import encrypt_password, check_password
from tls_client import connect
import re
from utils import secure_exit


def register_user():
    full_name = input('\nEnter Full Name: ').upper()
    email = input('Enter Email Address: ').lower()
    
    existing_users = safe_load()
    
    if email in existing_users:
        print("A user is already registered with that email.")
        return

    while True: 
        password = getpass.getpass('Enter Password: ')
        confirm_password = getpass.getpass("Re-Enter Password: ")
        
        if not secure_password_check(password):
            print("\nPassword is not secure.")
            print("Enter a password with at least:")
            print("- 8 Characters")
            print("- 1 Uppercase Letter")
            print("- 1 Lowercase Letter")
            print("- 1 Digit")
            print("- 1 Special Character (!@#$%^&*)")
            continue
        
        if password == confirm_password:
            # if bcrypt.checkpw(confirm_password.encode(), hashed_password):
            hashed_password = encrypt_password(password)
            # hashed_password = bcrypt.hashpw(password.encode(), salt)
            existing_users[email] = {
                "full_name": full_name,
                "password": hashed_password,
                'contacts': [],
                "is_online": False
            }
            print("\nPasswords Matched.")

            del password
            del confirm_password

            safe_save(existing_users)
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


def user_login(menu_callback):
    existing_users = safe_load()

    max_attempts = 3  # Maximum allowed attempts
    attempts = 0  # Counter for failed attempts

    while attempts < max_attempts:
        email = input("\nEnter Email Address: ").strip().lower()

        # Check if the user is already online
        if check_user_state(email):
            print("User is already online!")
            return

        login_password = getpass.getpass("Enter Password: ")

        if email in existing_users:
            # Check password
            if check_password(existing_users[email]['password'], login_password):
                print("\nWELCOME TO SECUREDROP!")
                print(f"User {existing_users[email]['full_name']} Logged in Successfully!")

                # Mark user as online
                set_user_state(email, True)

                # Establish connection and start the menu
                tls_sock, sock = connect(email)
                menu_callback(email, tls_sock, sock)
                return True
            else:
                print("\nEmail and Password Combination Invalid.\n")
        else:
            print("\nEmail and Password Combination Invalid.\n")

        attempts += 1

    # Kill the program after too many attempts 
    print("\nToo many failed attempts.")
    secure_exit()


# Checks if the user entered a secure password using regex
def secure_password_check(password):
    if(len(password) < 8 or 
       not re.search("[a-z]", password) or
       not re.search("[A-Z]", password) or
       not re.search(r"\d", password) or
       not re.search(r"[!@#$%^&*]", password)):
        return False
    return True
        