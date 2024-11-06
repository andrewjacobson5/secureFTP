"""
COMP 2300 Fall 2024 Class Project Secure Drop
Help Menu
"""

# to be fully implemented in the future
def menu_options():
    menu = input("\nType 'help' For Commands: ").lower()
    
    while menu:
        if menu == 'help':
            help()
            break
        elif menu == '':
            break
        else:
            print("Incorrect Entry. Quitting.")
            break

def help():
    print("\nHelp Menu:\n")

    print("'ADD' -> Add a new contact")
    print("'LIST' -> List all online contacts")
    print("'SEND' -> Transfer file to contact")
    print("'EXIT' -> Exit SecureDrop\n")

    # user_selection = input("Enter One of the Options Above: ")

    # if user_selection == 'A' or user_selection == 'a' or user_selection "add":
