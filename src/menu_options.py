"""
COMP 2300 Fall 2024 Class Project Secure Drop
Help Menu
"""

import json
from contacts import add_contact

# to be fully implemented in the future - for Milestone 4
def menu_options(user_email):    
    while True:
        menu = input("\nType 'help' For Commands: ").lower()

        if menu == 'help':
            help(user_email)
            break
        elif menu == '':
            break
        else:
            print("Incorrect Entry. Quitting.")
            break

def help(user):
    print("\nHelp Menu:\n")

    print("'ADD' -> Add a new contact")
    # print("'LIST' -> List all online contacts")
    # print("'SEND' -> Transfer file to contact")
    # print("'EXIT' -> Exit SecureDrop\n")

    user_selection = input("Enter One of the Options Above: ").lower()
    if user_selection == 'a' or user_selection == "add":
        add_contact(user)
