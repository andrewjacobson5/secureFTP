import os
import json
from user import register_user, user_login
users = {}

USERS_FILE = 'users.json'  

def user_exist(login_or_register):
    
    while login_or_register:
        if login_or_register == 'R' or login_or_register == 'r' or login_or_register == 'y' or login_or_register == 'Y' :
            register_user()
            break
        elif login_or_register == 'L' or login_or_register == 'l':
            print('LOGIN')
            user_login()
            break
        else:
            print("Invalid choice, please try again.")
            login_or_register = input("Enter Correct Selection: ")
            continue


if __name__ == "__main__":
    login_or_register = ''

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump({}, file, indent=4)  # This creates the file if it doesn't exist

    while True:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as file:
                # return loaded JSON data
                data = json.load(file)

                if data == {}:
                    print("No users are registered with this client.")
                    login_or_register = input("Do you want to register a new user (y/n)? ")

                    if login_or_register == 'y' or login_or_register == 'Y':
                        user_exist('y' or 'Y')
                        break
                    elif login_or_register == 'n' or login_or_register == 'N':
                        print("QUITTING")
                        break
                    else:
                        print("Invalid choice, please try again.")
                        login_or_register = input("Enter Correct Selection: ")
                        continue
                else:
                    print("An User Exists in This Machine.")
                    login_or_register = input("Enter 'L' to login, or 'R' to register a new user: ")
                    user_exist(login_or_register)
                    break