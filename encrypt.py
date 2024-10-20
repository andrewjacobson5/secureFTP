import bcrypt
import base64   

def encrypt_password(password):
    # hashing the password, returning as string for storage
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, user_password):
    # Check if the provided password matches the stored hashed password
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))