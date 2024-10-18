from user import register_user, user_login
users = {}

if __name__ == "__main__":
    while True:
        login_or_register = input("Enter 1 to register, 2 to login: ")
        if login_or_register == '1':
            register_user()
            break
        elif login_or_register == '2':
            user_login()
            break
        else:
            print("Invalid choice, please try again.")