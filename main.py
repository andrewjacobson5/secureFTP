import os
import json
from user import register_user, user_login
users = {}

USERS_FILE = 'users.json'     

if __name__ == "__main__":
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

                    if login_or_register == 'y':
                        register_user()
                        break
                    elif login_or_register == 'n':
                        user_login()
                        break
                    else:
                        print("Invalid choice, please try again.")
                else:
                    print('Welcome Back!')
                    print('LOGIN')
                    user_login()
                    break