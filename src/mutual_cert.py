from encrypt import encrypt_password, check_password
from user import user_login
import json
import getpass
import threading
import ssl
import socket

USERS_FILE = 'users.json'
SERVER_ADDRESS = ('localhost', 8443)

# server function
def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile='certs/server_cert.pem', keyfile='certs/server_key.pem')
    context.load_verify_locations(cafile='certs/ca_cert.pem')

    with socket.create_server(SERVER_ADDRESS) as server:
        with context.wrap_socket(server, server_side=True) as ssock:
            print('Server started with mutual TLS')
            while True:
                conn, addr = ssock.accept()
                print(f'Connection from {addr} established and client authenticated!')
                handle_client(conn)

# client certificate funtion
def start_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile='certs/client_cert.pem', keyfile='certs/client_key.pem')
    context.load_verify_locations(cafile='certs/ca_cert.pem')

    with socket.create_connection(SERVER_ADDRESS) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            print('Connected to server with mutual TLS')
            ssock.sendall(b'Secure Server')

def handle_client(conn):
# handle client interactions on server side
    try:
        user_login()
    finally:
        conn.close()