"""
COMP 2300 Fall 2024 Class Project Secure Drop
Help Menu
"""

from contacts import add_contact, list_contacts, remove_contact
from send import send

# to be fully implemented in the future - for Milestone 4
def menu_options(user_email, tls_sock, sock):    
        menu(user_email, tls_sock, sock)


def menu(user_email, tls_sock, sock):
    while True:
        print("\nMenu:\n")
        print("'ADD' -> Add a new contact")
        print("'LIST' -> List all online contacts")
        print("'SEND' -> Transfer file to contact")
        print("'REMOVE' -> Remove a contact")  
        print("'EXIT' -> Exit SecureDrop\n")

        user_selection = input("Enter One of the Options Above: ").strip().lower()

        if user_selection in ['add', 'a']:
            add_contact(user_email)
        elif user_selection in ['list', 'l']:
            list_contacts(user_email, tls_sock)
        elif user_selection in ['send', 's']:
            send(tls_sock)
        elif user_selection in ['remove', 'r']: 
            remove_contact(user_email)
        elif user_selection in ['exit', 'e']:
            print("Exiting SecureDrop.")
            tls_sock.close()
            sock.close()
            exit()
        else:
            print("Invalid selection.")
