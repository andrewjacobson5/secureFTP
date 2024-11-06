# to be fully implemented in the future
def menu_options():
    menu = input("\nType 'H' for help, 'L' to list contacts, or press ENTER to continue: ").lower()
    
    while menu:
        if menu == 'h':
            help()
            break
        elif menu == 'l':
            #listContacts(user) need to get current user and pass to listContacts
            print("Listing contacts:")
            break
        elif menu == '':
            break
        else:
            print("Incorrect Entry. Quitting.")
            break

def help():
    print("\nHelp Menu:\n")

    print("'A' -> Add a new contact")
    print("'C' -> List all online contacts")
    print("'S' -> Transfer file to contact")
    print("'E' -> Exit SecureDrop\n")

    # user_selection = input("Enter One of the Options Above: ")

    # if user_selection == 'A' or user_selection == 'a' or user_selection "add":
