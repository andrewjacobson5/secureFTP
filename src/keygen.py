from cryptography.fernet import Fernet

def write_key():
    # Generates a key and save it into a file
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    # Loads the key from the key.key file
    return open("key.key", "rb").read()

def encrypt_file(filename):
    with open(filename, "r") as f:  # Read file in text mode
        data = f.read()

    if not data or data == "{}":
        return
    
    key = load_key()
    fernet = Fernet(key)

    # Encrypt and save as bytes
    encrypted = fernet.encrypt(data.encode("utf-8"))

    with open(filename, "wb") as f:  # Write in binary mode
        f.write(encrypted)


def decrypt_file(filename):
    # if file is empty, leave it
    with open(filename, "rb") as f:  # Read file in binary mode
        data = f.read()

    if not data or data == b"{}":  # Compare with bytes
        return
    
    key = load_key()

    # decrypts the file and writes it
    fernet = Fernet(key)

    # decrypt data
    decrypted_data = fernet.decrypt(data)

    # write the original file
    with open(filename, "w") as file:  # Write in text mode
        file.write(decrypted_data.decode("utf-8"))  # Decode bytes to string
