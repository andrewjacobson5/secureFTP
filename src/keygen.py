from cryptography.fernet import Fernet

def write_key():
    # Generates a key and save it into a file
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    # Loads the key from the current directory named `key.key`
    return open("key.key", "rb").read()

def encrypt_file(filename):
    # if file is empty, leave it
    with open(filename) as f:
        data = f.read()

    if not data or data == "{}":
        return
    
    key = load_key()

    #this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    #this writes your new, encrypted data into a new JSON file
    with open(filename,'wb') as f:
        f.write(encrypted)

def decrypt_file(filename):
    # if file is empty, leave it
    with open(filename) as f:
        data = f.read()

    if not data or data == "{}":
        return
    
    key = load_key()

    # decrypts the file and writes it
    fernet = Fernet(key)

    # decrypt data
    decrypted_data = fernet.decrypt(data)

    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)