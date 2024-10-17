import json

users = {}

def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        with open('users.json', 'r') as file:
            existing_users = json.load(file)
    except FileNotFoundError:
        existing_users = {}

    existing_users[username] = password

    with open('users.json', 'w') as file:
        json.dump(existing_users, file, indent=4)
    
    print(f"User {username} registered successfully!")

def user_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        with open('users.json', 'r') as file:
            existing_users = json.load(file)
    except FileNotFoundError:
        existing_users = {}

    if username in existing_users and existing_users[username] == password:
        print(f"User {username} logged in successfully!")
    else:
        print("Invalid username or password")

if __name__ == "__main__":
    login_or_register = input("Enter 1 to register, 2 to login: ")
    if login_or_register == '1':
        register_user()
    elif login_or_register == '2':
        user_login()
    else:
        print("Invalid choice")
   