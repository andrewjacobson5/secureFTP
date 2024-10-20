import json
import getpass
# from encrypt import encrypt_password

USERS_FILE = 'users.json' 

def register_user():
    # I have commented full name and address out for now, but according to the instructions,
    # we should include these. Commented out for now to make it easier for us to test - PA
    # fullname = input("Enter Full Name: ")
    # email = input("Enter Email Address: ")
    username = input("Enter Username: ")
    # getpass wil hide the password for security purposes
    password = getpass.getpass("Enter Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    password.strip()
    username.strip()

    hashed_password = password

    if(password == confirm_password):
        print("\nPasswords Matched.")

        try:
            with open(USERS_FILE, 'r') as file:
                existing_users = json.load(file)
        except FileNotFoundError:
            existing_users = {}

        existing_users[username] = password

        with open(USERS_FILE, 'w') as file:
            json.dump(existing_users, file, indent=4)
        
        print(f"User {username} Registered Successfully!")
    else:
        print("Passwords Do Not Match. Quitting.")

def user_login():
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    print("Welcome to SecureDrop")

    try:
        with open(USERS_FILE, 'r') as file:
            existing_users = json.load(file)
    except FileNotFoundError:
        existing_users = {}

    if username in existing_users and existing_users[username] == password:
        print(f"User {username} Logged in Successfully!")
    else:
        print("Invalid Username or Password")