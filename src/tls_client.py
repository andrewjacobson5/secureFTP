import socket
import ssl
import time
import json

# Configuration
SERVER_HOST = '127.0.0.1'
TLS_PORT = 8443

CERTS_DIR = 'certs'
CA_CERT = f'{CERTS_DIR}/ca_cert.pem'
CLIENT_CERT = f'{CERTS_DIR}/client_cert.pem'
CLIENT_KEY = f'{CERTS_DIR}/client_key.pem'

def send_heartbeat(user_email):
    # Send periodic heartbeats to the server.
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.load_verify_locations(cafile=CA_CERT)

    try:
        with socket.create_connection((SERVER_HOST, TLS_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_HOST) as tls_sock:

                while True:
                    tls_sock.sendall(user_email.encode('utf-8'))
                    time.sleep(5)  # Send heartbeat every 5 seconds
                    
    except Exception as e:
        # SERVER SHUTDOWN by one client disconnecting
        print("Error sending heartbeat to server")

def get_online_users():
    # Fetch the online users dictionary from the server.
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.load_verify_locations(cafile=CA_CERT)

    try:
        with socket.create_connection((SERVER_HOST, TLS_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_HOST) as tls_sock:
                tls_sock.sendall(b"GET_USERS")  # Send the query command
                response = tls_sock.recv(4096)  # Receive the response
                online_users = json.loads(response.decode('utf-8'))
                return online_users
    except Exception as e:
        print(f"Error fetching online users: {e}")
        return {}
    

def check_online_status(email):
    if email in get_online_users():
        return 1
    else: 
        return 0