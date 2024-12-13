import socket
import ssl
import time
import json
import os
import threading
from queue import Queue

# Configuration
SERVER_HOST = '127.0.0.1'
TLS_PORT = 8443

CERTS_DIR = 'certs'
CA_CERT = f'{CERTS_DIR}/ca_cert.pem'
CLIENT_CERT = f'{CERTS_DIR}/client_cert.pem'
CLIENT_KEY = f'{CERTS_DIR}/client_key.pem'

lock = threading.Lock()  # Ensures thread-safe access to the TLS socket
request_queue = Queue()  # Queue to handle specific server responses

def connect():
    # Connects the client to the server, returns socket
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.load_verify_locations(cafile=CA_CERT)

    try:
        sock = socket.create_connection((SERVER_HOST, TLS_PORT))
        tls_sock = context.wrap_socket(sock, server_hostname=SERVER_HOST)
        return tls_sock, sock
    except Exception as e:
        print("Error connecting to server:", e)
        return None, None

def listener_thread(tls_sock):
    # Continuously listens for server messages
    while True:
        try:
            data = tls_sock.recv(4096)
            if not data:
                print("Server disconnected.\n")
                break

            message = data.decode('utf-8').strip()

            # Route specific responses to the queue
            if message.startswith("{"):
                # Put JSON-like responses in the queue for use
                request_queue.put(message)
            else:
                # Process other incoming requests
                process_request(message, tls_sock)
        except Exception as e:
            break

def process_request(request, tls_sock):
    # Processes incoming requests
    from menu_options import menu
    try:
        request = request.strip()
        print(f"\nProcessing request: {request}")

        if request.startswith("SEND_REQUEST"):
            parts = request.split(":", 1)
            if len(parts) < 2:
                print("Invalid SEND_REQUEST format.\n")
                return

            sender_email = parts[1].strip()
            acpt = input(f"{sender_email} wants to send you a file. Accept? (y/n): ")
            response = "SEND_ACCEPT" if acpt.lower() == 'y' else "SEND_DENIED"
            tls_sock.sendall(response.encode('utf-8'))

            if response == "SEND_ACCEPT":
                dataF = tls_sock.recv(4096)
                file_name = dataF.decode('utf-8').strip()
                with open(file_name, 'wb') as file:
                    while True:
                        data = tls_sock.recv(1024)
                        if not data:
                            break
                        file.write(data)
                print(f"File received: {file_name}\n")
        else:
            print(f"Unhandled request: {request}")
    except Exception as e:
        print(f"Error processing request: {e}")

def get_online_users(tls_sock):
    # Fetches user data from the server
    try:
        with lock:
            tls_sock.sendall(b"GET_USERS")
            response = request_queue.get(timeout=5)  # Wait for server response
            return json.loads(response)
    except Exception:
        # will happen when no users are on
        return {}

def send_file(receiver, file_path, tls_sock):
    # Handles sending a file to another user
    if not os.path.isfile(file_path):
        print("No file found.\n")
        return
    try:

        tls_sock.sendall(f"SEND_USER:{receiver}\n".encode('utf-8'))
        data = tls_sock.recv(4096)
        message = data.decode('utf-8').strip()

        if message == "SEND_OFFLINE":
            print(f"{receiver} is offline.\n")
        elif message == "SEND_DENIED":
            print(f"{receiver} denied the file transfer.\n")
        elif message == "SEND_ACCEPT":
            print(f"{receiver} accepted the file transfer.\n")
            file_name = os.path.basename(file_path)
            tls_sock.sendall(file_name.encode('utf-8'))

            with open(file_path, 'rb') as file:
                while chunk := file.read(1024):
                    tls_sock.sendall(chunk)

            print("File sent successfully.\n")
    except Exception as e:
        print(f"Error sending file: {e}")

def send_heartbeat(user_email, tls_sock):
    # Sends a periodic heartbeat to the server
    try:
        while True:
            with lock:
                tls_sock.sendall(user_email.encode('utf-8'))
            time.sleep(5)  # Send heartbeat every 5 seconds
    except Exception as e:
        print(f"Error sending heartbeat: {e}")

def check_online_status(email, tls_sock):
    # Checks if a specific user is online.
    online_users = get_online_users(tls_sock)
    return email in online_users

      
