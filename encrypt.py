import bcrypt
import base64   

def encrypt_password(password):
    salt = bcrypt.gensalt()
    # hashing the password, returning as string for storage
    return base64.b64encode(bcrypt.hashpw(password.encode('utf-8'), salt)).decode('utf-8')

def check_password(hashed_password, user_password):
    # Check if the provided password matches the stored hashed password
    hashed_password_bytes = base64.b64decode(hashed_password.encode('utf-8'))
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password_bytes)