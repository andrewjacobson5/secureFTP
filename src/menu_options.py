"""
COMP 2300 Fall 2024 Class Project Secure Drop
Help Menu
"""

from contacts import add_contact, list_contacts, remove_contact
from tls_client import client_send_request


def menu(user_email, tls_sock, sock):
    while True:
        print("\nMenu:\n")
        print("'ADD' -> Add a new contact")
        print("'LIST' -> List all online contacts")
        print("'SEND' -> Transfer file to contact")
        print("'REMOVE' -> Remove a contact")
        print("'EXIT' -> Exit SecureDrop\n")

        user_selection = input(
            "Enter One of the Options Above: ").strip().lower()

        if user_selection in ['add', 'a']:
            add_contact(user_email)
        elif user_selection in ['list', 'l']:
            list_contacts(user_email)
        elif user_selection in ['send', 's']:
            client_send_request(tls_sock, user_email)
        elif user_selection in ['remove', 'r']:
            remove_contact(user_email)
        elif user_selection in ['exit', 'e']:
            print("Exiting SecureDrop.")
            exit()
        else:
            print("Invalid selection.")
