import socket
import time
import threading
from mutual_cert import start_server, start_client

def run_receiver():
    print("Starting secure receiver...")
    start_server()  # Start the secure server for mutual TLS communication.

def run_sender():
    print("Starting secure sender...")
    start_client()  # Start the secure client for mutual TLS communication.

def send_heartbeat(user_email):
    server_address = ('127.0.0.1', 5005)  # Replace with actual server address
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            client.sendto(user_email.encode('utf-8'), server_address)
            print(f"Heartbeat sent for {user_email}")
            time.sleep(5)  # Send heartbeat every 5 seconds
        except Exception as e:
            print(f"Error sending heartbeat: {e}")
            break

def start_heartbeat(user_email):
    threading.Thread(target=send_heartbeat, args=(user_email,), daemon=True).start()

