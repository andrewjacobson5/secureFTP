import socket
import ssl
import threading
import time
import queue
from utils import set_user_state, reset_user_state

# Configuration
SERVER_HOST = '127.0.0.1'
TLS_PORT = 8443
CERTS_DIR = 'certs'
SERVER_CERT = f'{CERTS_DIR}/server_cert.pem'
SERVER_KEY = f'{CERTS_DIR}/server_key.pem'
CA_CERT = f'{CERTS_DIR}/ca_cert.pem'

# Tracks connected users: {email: (socket, queue, last_heartbeat)}
connected_users = {}
lock = threading.Lock()

# Handles client communication
def handle_tls_client(client_sock, client_email):
    client_queue = connected_users[client_email][1]  # Get client queue
    while True:
        try:
            request = client_sock.recv(4096).decode('utf-8')
            if not request:  # Client disconnected
                break

            if request.startswith("HEARTBEAT"):  # Update heartbeat
                with lock:
                    parts = client_email.split(":", 1)
                    connected_users[parts[1]] = (
                        client_sock, client_queue, time.time()
                    )
                print(f"Heartbeat received from {client_email}.")
            else:
                print(f"Unknown request from {client_email}: {request}")
        except Exception as e:
            print(f"Error handling client {client_email}: {e}")
            break

    # Cleanup after disconnection
    with lock:
        if client_email in connected_users:
            del connected_users[client_email]
            set_user_state(client_email, False)
            print(f"Client {client_email} removed.")

# Forwards a file from sender to receiver
def forward_file(sender_sock, receiver_sock):
    try:
        file_name = sender_sock.recv(4096).decode('utf-8').strip()
        receiver_sock.sendall(file_name.encode('utf-8'))
        while True:
            chunk = sender_sock.recv(4096)
            if chunk.endswith(b"SEND_COMPLETE"):
                receiver_sock.sendall(chunk)
                break
            receiver_sock.sendall(chunk)
        print("File transfer completed.")
    except Exception as e:
        print(f"Error forwarding file: {e}")

# Receives a file and stores it
def receive_file(client_sock):
    try:
        file_name = client_sock.recv(4096).decode('utf-8').strip()
        with open(file_name, "wb") as file:
            while True:
                data = client_sock.recv(4096)
                if data.endswith(b"SEND_COMPLETE"):
                    file.write(data[:-len(b"SEND_COMPLETE")])
                    break
                file.write(data)
        print(f"File saved as {file_name}")
    except Exception as e:
        print(f"Error receiving file: {e}")

# Processes client request queue
def process_client_queue(client_email):
    client_queue = connected_users[client_email][1]
    client_sock = connected_users[client_email][0]
    while True:
        try:
            request = client_queue.get()
            if request.startswith("SEND_REQUEST:"):
                sender_email = request.split(":")[1].strip()
                message = f"SEND_REQUEST:{sender_email}"
                client_sock.sendall(message.encode('utf-8'))  # Notify recipient
                response = client_sock.recv(4096).decode('utf-8').strip().lower()
                client_queue.put("SEND_ACCEPT" if response == 'y' else "SEND_DENY")
        except Exception as e:
            print(f"Error processing queue for {client_email}: {e}")
            break

# Starts the TLS server
def start_tls_server():
    reset_user_state()  # Reset all users to offline at startup
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    context.load_verify_locations(cafile=CA_CERT)
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.create_server((SERVER_HOST, TLS_PORT)) as server_sock:
        with context.wrap_socket(server_sock, server_side=True) as tls_sock:
            print("Server is running...")

            while True:
                client_sock, addr = tls_sock.accept()
                client_email = client_sock.recv(1024).decode('utf-8').strip()
                print(f"Client {client_email} connected from {addr}")

                with lock:
                    connected_users[client_email] = (client_sock, queue.Queue(), time.time())
                threading.Thread(target=handle_tls_client, args=(client_sock, client_email), daemon=True).start()
                threading.Thread(target=process_client_queue, args=(client_email,), daemon=True).start()

if __name__ == "__main__":
    start_tls_server()
