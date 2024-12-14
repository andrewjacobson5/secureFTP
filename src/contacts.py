"""
COMP 2300 Fall 2024 Class Project Secure Drop
Contacts generation
"""

from utils import safe_load, safe_save, check_user_state


def add_contact(user_email):
    contact_name = input("Enter Contact's Full Name: ").strip()
    contact_email = input("Enter Contact's Email: ").strip()

    users = safe_load()

    # ensure the user exists and initialize the contacts list
    if user_email not in users:
        print(f"User {user_email} not found.")
        return

    if "contacts" not in users[user_email]:
        users[user_email]["contacts"] = []

    # check if the contact already exists
    for contact in users[user_email]["contacts"]:
        if contact["contact_email"] == contact_email:
            contact["contact_name"] = contact_name
            print(f"Existing contact UPDATED to {
                  contact_name} for email address: {contact_email}\n")
            break
    else:  # If no break occurred in the loop, add the new contact
        contact_entry = {
            "contact_name": contact_name,
            "contact_email": contact_email
        }
        users[user_email]["contacts"].append(contact_entry)
        print(f"New contact: {contact_name} with email {
              contact_email} was added to {user_email}'s contact list\n")

    safe_save(users)


def list_contacts(user_email):

    users = safe_load()

    if not users[user_email] or not users[user_email]['contacts']:
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
            reciprocated = any(c["contact_email"] ==
                               user_email for c in contact_contacts)

        # Check online status
        online = check_user_state(contact_email)

        # Display based on conditions online and reciprocated
        if reciprocated and online:
            print(f"- {contact_name} ({contact_email}) [Online]")
        else:
            print(f"No contacts online")


def remove_contact(user_email):
    contact_email = input("Enter the Email of the Contact to Remove: ").strip()

    users = safe_load()

    # make sure the user exists and has a contacts list
    if user_email not in users or "contacts" not in users[user_email]:
        print(f"No contacts found for {user_email}.")
        return

    # Find and remove the contact
    contacts = users[user_email]["contacts"]
    updated_contacts = [
        contact for contact in contacts if contact["contact_email"] != contact_email]

    if len(updated_contacts) == len(contacts):
        print(f"No contact with email {contact_email} found.")
    else:
        users[user_email]["contacts"] = updated_contacts
        safe_save(users)
        print(f"Contact with email {contact_email} has been removed.")
