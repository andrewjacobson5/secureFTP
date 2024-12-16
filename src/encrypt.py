"""
COMP 2300 Fall 2024 Class Project Secure Drop
User registration and log in file
 @version: 1.1-2.26 - Milestone 1-2
"""

import bcrypt
import base64   

def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    #changed this so that the password hash is not stored directly to minimize potential leaks
    return base64.b64encode(hashed).decode('utf-8')

def check_password(hashed_password, user_password):
    # Check if the provided password matches the stored hashed password
    hashed_password_bytes = base64.b64decode(hashed_password.encode('utf-8'))
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password_bytes)