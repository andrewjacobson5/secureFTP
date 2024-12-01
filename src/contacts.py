"""
COMP 2300 Fall 2024 Class Project Secure Drop
Contacts generation
"""

# Contacts:
    # Different contacts based on the user
    # Encrypt the contacts for each person
    # Adding/Removing contacts  

from utils import load_users, save_user
from presence_server import check_online_status

def add_contact(user_email):
    contact_name = input("Enter Contact's Full Name: ").strip()
    contact_email = input("Enter Contact's Email: ").strip()

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

            print(f"Existing Contact UPDATED to {contact_name} for email address: {contact_email}\n")
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

def list_contacts(user_email):
    users = load_users()

    if user_email not in users or 'contacts' not in users[user_email]:
        print(f"No contacts found for {user_email}.")
        return

    user_contacts = users[user_email]['contacts']
    print(f"{user_email}'s contacts:")

    for contact in user_contacts:
        contact_email = contact["contact_email"]
        contact_name = contact["contact_name"]
        reciprocated = False

        # Check if reciprocity exists
        if contact_email in users:
            contact_contacts = users[contact_email].get("contacts", [])
            reciprocated = any(c["contact_email"] == user_email for c in contact_contacts)

        # Check online status
        online = check_online_status(contact_email)

        # Display based on conditions
        if reciprocated and online:
            print(f"- {contact_name} ({contact_email}) [CONTACT RECIPROCATED & ONLINE]")
        elif reciprocated:
            print(f"- {contact_name} ({contact_email}) [CONTACT RECIPROCATED & OFFLINE]")
        else:
            print(f"- {contact_name} ({contact_email}) [CONTACT NOT RECIPROCATED]")
