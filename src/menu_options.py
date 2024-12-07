"""
COMP 2300 Fall 2024 Class Project Secure Drop
Help Menu
"""

from contacts import add_contact, list_contacts

# to be fully implemented in the future - for Milestone 4
def menu_options(user_email):    
        menu(user_email)


def menu(user_email):
    while(True):
        print("\nMenu:\n")

        print("'ADD' -> Add a new contact")
        print("'LIST' -> List all online contacts")
        # print("'SEND' -> Transfer file to contact")
        print("'EXIT' -> Exit SecureDrop\n")

        user_selection = input("Enter One of the Options Above: ").lower()
        if user_selection in ['ADD', 'add', 'a']:
            add_contact(user_email)
        elif user_selection in ['LIST', 'list', 'l']:
            list_contacts(user_email)
        elif user_selection in ['EXIT', 'exit', 'e']:
            print("Exiting SecureDrop.")
            exit()
        else:
            print("Invalid selection.")
