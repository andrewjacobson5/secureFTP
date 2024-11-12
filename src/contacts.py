"""
COMP 2300 Fall 2024 Class Project Secure Drop
Contacts generation
"""

# Contacts:
    # Different contacts based on the user
    # Encrypt the contacts for each person
    # Adding/Removing contacts  

from utils import load_users, save_user

def add_contact(user_email):
    contact_name = input("Enter Contact's Full Name: ")
    contact_email = input("Enter Contact's Email: ")

    users = load_users()

    # ensure the user exists and initialize the contacts list
    if user_email not in users:
        print(f'User {user_email} not found.')
        return
    
    if 'contacts' not in users[user_email]:
        users[user_email]['contacts'] = []
    
    # check if the contact exists
    contact_exists = False
    for contact in users[user_email]["contacts"]:
        if contact["contact_email"] == contact_email:
            contact["contact_name"] = contact_name
            contact_exists = True
            break

    # if the contact does not exist
    if not contact_exists:
        contact_entry = {
            "contact_name": contact_name,
            "contact_email": contact_email
        }

        users[user_email]['contacts'].append(contact_entry)
        print(f"New Contact: {contact_name} with email {contact_email} was added to {user_email}'s contact list\n")

    save_user(users)

# Milestone 4:
# def list_contacts(user_email):
#     users = load_users()

#     # retrieve and display the user's contact is they exist
#     if user_email in users and 'contacts' in users[user_email]:
#         print(f"{user_email}'s contacts: ")
#         for encrypted_contact in users[user_email]['contacts']:
#             print(f"- {encrypted_contact}") # display encrypted contact
#     else:
#         print(f"No contacts found for {user_email}.")