import json
import getpass
import bcrypt
# from encrypt import encrypt_password
from menu_options import help

USERS_FILE = 'users.json' 

def register_user():
    # I have commented full name and address out for now, but according to the instructions,
    # we should include these. Commented out for now to make it easier for us to test - PA
    # fullname = input("Enter Full Name: ")
    # email = input("Enter Email Address: ")
    username = input("\nEnter Username: ")
    # getpass wil hide the password for security purposes
    password = getpass.getpass("Enter Password: ")
    # strip of any spaces
    password.strip()
    username.strip()

    salt = bcrypt.gensalt()
    # bcrypt requires the password to be in bytes and not strings, converting
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    confirm_password = getpass.getpass("Confirm Password: ")

    if bcrypt.checkpw(confirm_password.encode(), hashed_password):
        print("\nPasswords Matched.")

        try:
            with open(USERS_FILE, 'r') as file:
                existing_users = json.load(file)
        except FileNotFoundError:
            existing_users = {}

        existing_users[username] = hashed_password.decode()

        with open(USERS_FILE, 'w') as file:
            json.dump(existing_users, file, indent=4)
        
        print(f"User {username} Registered Successfully!")
    else:
        print("\nPasswords Do Not Match. Quitting.")

def user_login():
    username = input("\nEnter Username: ")
    password = getpass.getpass("Enter Password: ")
    print("\nWELCOME TO SECUREDROP!")
    menu = input("\nType 'H' for help, or press ENTER to continue: ")
    
    while menu:
        if menu == 'H' or menu == 'h':
            help()
            break
        elif menu == '':
            try:
                with open(USERS_FILE, 'r') as file:
                    existing_users = json.load(file)
            except FileNotFoundError:
                existing_users = {}

            if username in existing_users and existing_users[username] == password:
                print(f"User {username} Logged in Successfully!")
            else:
                print("\nInvalid Username or Password")
            break
        else:
            print("Incorrect Entry. Quitting.")
            break